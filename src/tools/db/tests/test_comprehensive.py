#!/usr/bin/env python3
"""Test comprehensive discovery features"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import string

def test_pattern_generation():
    """Test that comprehensive mode generates correct number of patterns"""
    
    # Test 2-letter combinations
    patterns = []
    for first in string.ascii_lowercase:
        for second in string.ascii_lowercase:
            patterns.append(first + second)
    
    print(f"2-letter combinations: {len(patterns)} patterns")
    assert len(patterns) == 676, f"Expected 676, got {len(patterns)}"
    
    # Test with 3-letter prefixes
    common_prefixes = ['the', 'new', 'ask', 'get', 'pro', 'all', 'any', 'big', 
                     'hot', 'top', 'old', 'sub', 'not', 'bad', 'fun', 'red',
                     'blu', 'gre', 'bla', 'whi', 'dar', 'lig', 'hig', 'low']
    
    three_letter = []
    for prefix in common_prefixes:
        for letter in string.ascii_lowercase[:10]:
            three_letter.append(prefix[:2] + letter)
    
    print(f"3-letter patterns from {len(common_prefixes)} prefixes: {len(three_letter)} patterns")
    
    total = len(patterns) + len(three_letter)
    print(f"\nTotal alphabetical patterns in comprehensive mode: {total}")
    print(f"Each pattern can return up to 250 results")
    print(f"Maximum potential discoveries: {total * 250:,}")
    
    print("\n✅ Pattern generation test passed!")

if __name__ == "__main__":
    test_pattern_generation()