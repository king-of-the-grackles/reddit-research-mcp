"""
Test suite for Phase 2a vector database enhancements.

Tests all four enhancements:
- 2a.1: Distance scores in response
- 2a.2: Match tier classification
- 2a.3: Confidence threshold filtering
- 2a.4: Confidence statistics and tier distribution
"""

import pytest
import sys
import os
from unittest.mock import Mock, patch, AsyncMock
from fastmcp import Context

# Add project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.tools.discover import (
    discover_subreddits,
    classify_match_tier,
    calculate_confidence_stats,
    calculate_tier_distribution
)


class TestPhase2aEnhancements:
    """Tests for all Phase 2a enhancements."""

    @pytest.fixture
    def mock_collection(self):
        """Create a mock ChromaDB collection with realistic data."""
        collection = Mock()

        # Mock query response with realistic distances
        collection.query.return_value = {
            'ids': [['MachineLearning', 'deeplearning', 'artificial', 'learnmachinelearning', 'datascience']],
            'distances': [[0.15, 0.28, 0.55, 0.72, 0.95]],  # Varied distances for tier testing
            'documents': [['ML subreddit', 'Deep learning', 'AI', 'Learning ML', 'Data science']],
            'metadatas': [[
                {
                    'name': 'MachineLearning',
                    'subscribers': 825000,
                    'nsfw': False,
                    'url': 'https://reddit.com/r/MachineLearning'
                },
                {
                    'name': 'deeplearning',
                    'subscribers': 285000,
                    'nsfw': False,
                    'url': 'https://reddit.com/r/deeplearning'
                },
                {
                    'name': 'artificial',
                    'subscribers': 125000,
                    'nsfw': False,
                    'url': 'https://reddit.com/r/artificial'
                },
                {
                    'name': 'learnmachinelearning',
                    'subscribers': 45000,
                    'nsfw': False,
                    'url': 'https://reddit.com/r/learnmachinelearning'
                },
                {
                    'name': 'datascience',
                    'subscribers': 650000,
                    'nsfw': False,
                    'url': 'https://reddit.com/r/datascience'
                }
            ]]
        }

        return collection

    @pytest.mark.asyncio
    async def test_2a1_distance_scores_exposed(self, mock_collection):
        """Enhancement 2a.1: Distance scores in response."""
        with patch('src.tools.discover.get_chroma_client'), \
             patch('src.tools.discover.get_collection', return_value=mock_collection):

            response = await discover_subreddits("machine learning", limit=5)

            # Verify response structure
            assert 'subreddits' in response
            assert len(response['subreddits']) > 0

            # Check each subreddit has distance field
            for subreddit in response['subreddits']:
                assert 'distance' in subreddit, "Distance field missing"
                assert isinstance(subreddit['distance'], float), "Distance should be float"
                assert 0.0 <= subreddit['distance'] <= 2.0, "Distance out of valid range"

    @pytest.mark.asyncio
    async def test_2a2_match_tier_labels(self, mock_collection):
        """Enhancement 2a.2: Match tier classification."""
        with patch('src.tools.discover.get_chroma_client'), \
             patch('src.tools.discover.get_collection', return_value=mock_collection):

            response = await discover_subreddits("machine learning", limit=5)

            valid_tiers = {'exact', 'semantic', 'adjacent', 'peripheral'}

            # Check each subreddit has match_tier field
            for subreddit in response['subreddits']:
                assert 'match_tier' in subreddit, "Match tier field missing"
                assert subreddit['match_tier'] in valid_tiers, f"Invalid tier: {subreddit['match_tier']}"

    @pytest.mark.asyncio
    async def test_2a2_tier_distance_alignment(self, mock_collection):
        """Verify tiers match distance thresholds."""
        with patch('src.tools.discover.get_chroma_client'), \
             patch('src.tools.discover.get_collection', return_value=mock_collection):

            response = await discover_subreddits("machine learning", limit=5)

            for subreddit in response['subreddits']:
                distance = subreddit['distance']
                tier = subreddit['match_tier']

                # Verify tier matches distance thresholds
                if tier == 'exact':
                    assert distance < 0.2, f"Exact tier but distance {distance} >= 0.2"
                elif tier == 'semantic':
                    assert 0.2 <= distance < 0.35, f"Semantic tier but distance {distance} not in [0.2, 0.35)"
                elif tier == 'adjacent':
                    assert 0.35 <= distance < 0.65, f"Adjacent tier but distance {distance} not in [0.35, 0.65)"
                else:  # peripheral
                    assert distance >= 0.65, f"Peripheral tier but distance {distance} < 0.65"

    @pytest.mark.asyncio
    async def test_2a3_min_confidence_parameter(self, mock_collection):
        """Enhancement 2a.3: Confidence threshold filtering."""
        with patch('src.tools.discover.get_chroma_client'), \
             patch('src.tools.discover.get_collection', return_value=mock_collection):

            # Get all results (no filter)
            all_results = await discover_subreddits("machine learning", limit=10)
            all_count = len(all_results['subreddits'])

            # Get filtered results
            filtered = await discover_subreddits("machine learning", limit=10, min_confidence=0.7)
            filtered_count = len(filtered['subreddits'])

            # Verify filtering works
            assert filtered_count <= all_count, "Filtered count should be <= all count"

            # Verify all returned results meet threshold
            for subreddit in filtered['subreddits']:
                assert subreddit['confidence'] >= 0.7, \
                    f"Subreddit {subreddit['name']} has confidence {subreddit['confidence']} < 0.7"

    @pytest.mark.asyncio
    async def test_2a3_confidence_threshold_default(self, mock_collection):
        """Default min_confidence should be 0.0 (no filtering)."""
        with patch('src.tools.discover.get_chroma_client'), \
             patch('src.tools.discover.get_collection', return_value=mock_collection):

            results1 = await discover_subreddits("machine learning", limit=5)
            results2 = await discover_subreddits("machine learning", limit=5, min_confidence=0.0)

            # Should return same number of results
            assert len(results1['subreddits']) == len(results2['subreddits'])

    @pytest.mark.asyncio
    async def test_2a4_confidence_statistics(self, mock_collection):
        """Enhancement 2a.4: Confidence distribution statistics."""
        with patch('src.tools.discover.get_chroma_client'), \
             patch('src.tools.discover.get_collection', return_value=mock_collection):

            response = await discover_subreddits("machine learning", limit=5)

            assert 'summary' in response
            assert 'confidence_stats' in response['summary']

            stats = response['summary']['confidence_stats']

            # Verify all stats present
            assert 'mean' in stats
            assert 'median' in stats
            assert 'min' in stats
            assert 'max' in stats
            assert 'std_dev' in stats

            # Verify logical relationships
            assert stats['min'] <= stats['median'] <= stats['max'], \
                "Stats order should be min <= median <= max"
            assert 0.0 <= stats['min'] <= 1.0, "Min out of range"
            assert 0.0 <= stats['max'] <= 1.0, "Max out of range"

    @pytest.mark.asyncio
    async def test_2a4_tier_distribution(self, mock_collection):
        """Tier distribution counts should match returned count."""
        with patch('src.tools.discover.get_chroma_client'), \
             patch('src.tools.discover.get_collection', return_value=mock_collection):

            response = await discover_subreddits("machine learning", limit=5)

            assert 'summary' in response
            assert 'tier_distribution' in response['summary']

            tiers = response['summary']['tier_distribution']

            # Verify all tiers present
            assert all(tier in tiers for tier in ['exact', 'semantic', 'adjacent', 'peripheral'])

            # Verify counts sum correctly
            total_tiers = sum(tiers.values())
            returned = response['summary']['returned']

            assert total_tiers == returned, \
                f"Tier distribution sum {total_tiers} != returned count {returned}"

    @pytest.mark.asyncio
    async def test_backward_compatibility(self, mock_collection):
        """All changes must be backward compatible."""
        with patch('src.tools.discover.get_chroma_client'), \
             patch('src.tools.discover.get_collection', return_value=mock_collection):

            response = await discover_subreddits("machine learning")

            # Old fields should still exist
            assert 'subreddits' in response
            assert 'summary' in response

            for subreddit in response['subreddits']:
                # Original fields
                assert 'name' in subreddit
                assert 'confidence' in subreddit
                assert 'url' in subreddit
                assert 'subscribers' in subreddit

                # New fields (Phase 2a)
                assert 'distance' in subreddit
                assert 'match_tier' in subreddit

            # Summary original fields
            assert 'total_found' in response['summary']
            assert 'returned' in response['summary']
            assert 'has_more' in response['summary']

            # Summary new fields (Phase 2a)
            assert 'confidence_stats' in response['summary']
            assert 'tier_distribution' in response['summary']

    @pytest.mark.asyncio
    async def test_all_enhancements_together(self, mock_collection):
        """Test all Phase 2a features in one response."""
        with patch('src.tools.discover.get_chroma_client'), \
             patch('src.tools.discover.get_collection', return_value=mock_collection):

            response = await discover_subreddits(
                "machine learning",
                limit=5,
                min_confidence=0.5
            )

            # Verify all features present
            for subreddit in response['subreddits']:
                # 2a.1 & 2a.2
                assert 'distance' in subreddit
                assert 'match_tier' in subreddit
                # 2a.3 applied
                assert subreddit['confidence'] >= 0.5

            # 2a.4
            assert 'confidence_stats' in response['summary']
            assert 'tier_distribution' in response['summary']


class TestHelperFunctions:
    """Test helper functions directly."""

    def test_classify_match_tier_exact(self):
        """Test exact tier classification (distance < 0.2)."""
        assert classify_match_tier(0.1) == "exact"
        assert classify_match_tier(0.19) == "exact"

    def test_classify_match_tier_semantic(self):
        """Test semantic tier classification (0.2 <= distance < 0.35)."""
        assert classify_match_tier(0.2) == "semantic"
        assert classify_match_tier(0.3) == "semantic"

    def test_classify_match_tier_adjacent(self):
        """Test adjacent tier classification (0.35 <= distance < 0.65)."""
        assert classify_match_tier(0.35) == "adjacent"
        assert classify_match_tier(0.5) == "adjacent"

    def test_classify_match_tier_peripheral(self):
        """Test peripheral tier classification (distance >= 0.65)."""
        assert classify_match_tier(0.65) == "peripheral"
        assert classify_match_tier(1.0) == "peripheral"

    def test_calculate_confidence_stats_normal(self):
        """Test confidence statistics with normal data."""
        scores = [0.9, 0.8, 0.7, 0.6, 0.5]
        stats = calculate_confidence_stats(scores)

        assert stats['mean'] == 0.7
        assert stats['median'] == 0.7
        assert stats['min'] == 0.5
        assert stats['max'] == 0.9
        assert stats['std_dev'] > 0  # Should have some variance

    def test_calculate_confidence_stats_empty(self):
        """Test confidence statistics with empty list."""
        stats = calculate_confidence_stats([])

        assert stats['mean'] == 0.0
        assert stats['median'] == 0.0
        assert stats['min'] == 0.0
        assert stats['max'] == 0.0
        assert stats['std_dev'] == 0.0

    def test_calculate_confidence_stats_single(self):
        """Test confidence statistics with single value."""
        scores = [0.75]
        stats = calculate_confidence_stats(scores)

        assert stats['mean'] == 0.75
        assert stats['median'] == 0.75
        assert stats['min'] == 0.75
        assert stats['max'] == 0.75
        assert stats['std_dev'] == 0.0  # No variance with single value

    def test_calculate_tier_distribution(self):
        """Test tier distribution calculation."""
        results = [
            {'match_tier': 'exact'},
            {'match_tier': 'exact'},
            {'match_tier': 'semantic'},
            {'match_tier': 'adjacent'},
            {'match_tier': 'peripheral'}
        ]

        dist = calculate_tier_distribution(results)

        assert dist['exact'] == 2
        assert dist['semantic'] == 1
        assert dist['adjacent'] == 1
        assert dist['peripheral'] == 1

    def test_calculate_tier_distribution_empty(self):
        """Test tier distribution with empty results."""
        dist = calculate_tier_distribution([])

        assert dist['exact'] == 0
        assert dist['semantic'] == 0
        assert dist['adjacent'] == 0
        assert dist['peripheral'] == 0


class TestEdgeCases:
    """Test edge cases and error handling."""

    @pytest.mark.asyncio
    async def test_min_confidence_filters_all(self):
        """Test min_confidence that filters all results."""
        collection = Mock()
        collection.query.return_value = {
            'ids': [['test']],
            'distances': [[0.9]],  # Low confidence result
            'documents': [['test']],
            'metadatas': [[{
                'name': 'test',
                'subscribers': 1000,
                'nsfw': False,
                'url': 'https://reddit.com/r/test'
            }]]
        }

        with patch('src.tools.discover.get_chroma_client'), \
             patch('src.tools.discover.get_collection', return_value=collection):

            # Set min_confidence very high
            response = await discover_subreddits("test", limit=10, min_confidence=0.99)

            # Should return empty or very few results
            assert len(response['subreddits']) == 0

    @pytest.mark.asyncio
    async def test_batch_mode_with_min_confidence(self):
        """Test batch mode respects min_confidence parameter."""
        collection = Mock()
        collection.query.return_value = {
            'ids': [['test1', 'test2']],
            'distances': [[0.5, 0.9]],
            'documents': [['test1', 'test2']],
            'metadatas': [[
                {'name': 'test1', 'subscribers': 1000, 'nsfw': False, 'url': 'https://reddit.com/r/test1'},
                {'name': 'test2', 'subscribers': 2000, 'nsfw': False, 'url': 'https://reddit.com/r/test2'}
            ]]
        }

        with patch('src.tools.discover.get_chroma_client'), \
             patch('src.tools.discover.get_collection', return_value=collection):

            response = await discover_subreddits(
                queries=["query1", "query2"],
                limit=10,
                min_confidence=0.6
            )

            # Verify batch mode
            assert 'batch_mode' in response
            assert response['batch_mode'] is True

            # Each query should respect min_confidence
            for query, result in response['results'].items():
                for subreddit in result['subreddits']:
                    assert subreddit['confidence'] >= 0.6
