#!/usr/bin/env python3
"""
Critical MCP Server Functionality Tests
Tests core server operations required for production deployment.
"""

import sys
import os
from pathlib import Path
import unittest
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.server import discover_operations, get_operation_schema, execute_operation, suggest_recovery


class TestCriticalMCPFunctionality(unittest.TestCase):
    """Test critical MCP server functions that must work in production."""
    
    def test_server_imports_without_error(self):
        """Test that server can be imported without crashes."""
        try:
            import src.server
            import src.config
            import src.middleware.langfuse_middleware
            self.assertTrue(True, "All imports successful")
        except Exception as e:
            self.fail(f"Failed to import server modules: {e}")
    
    def test_discover_operations_returns_valid_structure(self):
        """Test Layer 1: discover_operations returns correct structure."""
        # FastMCP tools are wrapped, need to call .fn
        result = discover_operations.fn()
        
        # Verify required keys exist
        self.assertIn("operations", result)
        self.assertIn("recommended_workflows", result)
        self.assertIn("next_step", result)
        
        # Verify operations list
        operations = result["operations"]
        self.assertIn("discover_subreddits", operations)
        self.assertIn("fetch_multiple", operations)
        self.assertIn("fetch_comments", operations)
        
        # Verify structure is complete
        self.assertIsInstance(operations, dict)
        self.assertTrue(len(operations) >= 5, "Should have at least 5 operations")
        
        print("✅ discover_operations returns valid structure")
    
    def test_get_operation_schema_all_operations(self):
        """Test Layer 2: get_operation_schema works for all operations."""
        operations_to_test = [
            "discover_subreddits",
            "search_subreddit", 
            "fetch_posts",
            "fetch_multiple",
            "fetch_comments"
        ]
        
        for op_id in operations_to_test:
            with self.subTest(operation=op_id):
                result = get_operation_schema.fn(op_id)
                
                # Should not have error
                self.assertNotIn("error", result)
                
                # Should have required schema fields
                self.assertIn("description", result)
                self.assertIn("parameters", result)
                
                # Parameters should be properly structured
                params = result["parameters"]
                self.assertIsInstance(params, dict)
                
                print(f"✅ get_operation_schema('{op_id}') returns valid schema")
    
    def test_get_operation_schema_invalid_operation(self):
        """Test get_operation_schema handles invalid operation gracefully."""
        result = get_operation_schema.fn("invalid_operation")
        
        # Should return error with helpful info
        self.assertIn("error", result)
        self.assertIn("available", result)
        self.assertIn("hint", result)
        
        # Available operations should be listed
        self.assertIsInstance(result["available"], list)
        self.assertTrue(len(result["available"]) >= 5)
        
        print("✅ get_operation_schema handles invalid operations gracefully")
    
    @patch('src.server.reddit')
    def test_execute_operation_handles_success(self, mock_reddit):
        """Test Layer 3: execute_operation handles successful execution."""
        # Mock discover_subreddits to avoid ChromaDB dependency
        with patch('src.server.discover_subreddits') as mock_discover:
            mock_discover.return_value = {
                "subreddits": [
                    {"name": "Python", "confidence": 0.95},
                    {"name": "learnpython", "confidence": 0.85}
                ]
            }
            
            result = execute_operation.fn(
                operation_id="discover_subreddits",
                parameters={"query": "python programming"}
            )
            
            # Should return success
            self.assertIn("success", result)
            self.assertTrue(result["success"])
            self.assertIn("data", result)
            
            print("✅ execute_operation handles successful execution")
    
    def test_execute_operation_handles_errors(self):
        """Test execute_operation handles errors with recovery suggestions."""
        # Test with missing Reddit client
        with patch('src.server.reddit', None):
            result = execute_operation.fn(
                operation_id="fetch_posts",
                parameters={"subreddit_name": "test"}
            )
            
            # Should return error with recovery
            self.assertIn("success", result)
            self.assertFalse(result["success"])
            self.assertIn("error", result)
            self.assertIn("recovery", result)
            
            # Recovery should be helpful
            self.assertIsInstance(result["recovery"], str)
            self.assertTrue(len(result["recovery"]) > 10)
            
            print("✅ execute_operation handles errors with recovery suggestions")
    
    def test_execute_operation_invalid_operation(self):
        """Test execute_operation handles invalid operation ID."""
        result = execute_operation.fn(
            operation_id="nonexistent_operation",
            parameters={}
        )
        
        # Should return error
        self.assertIn("success", result)
        self.assertFalse(result["success"])
        self.assertIn("error", result)
        self.assertIn("available_operations", result)
        
        print("✅ execute_operation rejects invalid operations")
    
    def test_suggest_recovery_provides_helpful_messages(self):
        """Test that recovery suggestions are helpful."""
        test_cases = [
            (Exception("404 Not Found"), "not found"),
            (Exception("429 Rate Limited"), "rate"),
            (Exception("403 Forbidden"), "private"),
            (Exception("Invalid parameter"), "invalid"),
            (Exception("Random error"), "check parameters")
        ]
        
        for error, expected_keyword in test_cases:
            with self.subTest(error=str(error)):
                recovery = suggest_recovery("test_op", error)
                self.assertIsInstance(recovery, str)
                self.assertTrue(len(recovery) > 10)
                self.assertIn(expected_keyword.lower(), recovery.lower())
        
        print("✅ suggest_recovery provides helpful messages")
    
    def test_server_handles_missing_reddit_credentials(self):
        """Test server handles missing Reddit credentials gracefully."""
        with patch.dict(os.environ, {}, clear=True):
            # Remove any existing credentials
            for key in ["REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET", "REDDIT_USER_AGENT"]:
                os.environ.pop(key, None)
            
            # Server should handle this without crashing
            from src.config import get_reddit_client
            
            try:
                client = get_reddit_client()
                # If we get here, credentials were found elsewhere (.env file)
                self.assertIsNotNone(client)
            except ValueError as e:
                # This is expected and OK - server should handle it
                self.assertIn("credentials not found", str(e).lower())
                print("✅ Server correctly identifies missing Reddit credentials")
    
    def test_no_blocking_operations_in_imports(self):
        """Test that server imports don't block or hang."""
        import signal
        import time
        
        def timeout_handler(signum, frame):
            raise TimeoutError("Import took too long")
        
        # Set a 5-second timeout
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(5)
        
        try:
            # Import server module
            import src.server
            signal.alarm(0)  # Cancel alarm
            print("✅ Server imports complete quickly without blocking")
        except TimeoutError:
            self.fail("Server import blocked for too long")
        finally:
            signal.alarm(0)  # Ensure alarm is cancelled


def run_critical_tests():
    """Run all critical MCP tests and report results."""
    print("=" * 60)
    print("CRITICAL MCP SERVER FUNCTIONALITY TESTS")
    print("=" * 60)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestCriticalMCPFunctionality)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Report summary
    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print("✅ ALL CRITICAL MCP TESTS PASSED!")
        print(f"   Ran {result.testsRun} tests successfully")
    else:
        print("❌ SOME TESTS FAILED!")
        print(f"   Failures: {len(result.failures)}")
        print(f"   Errors: {len(result.errors)}")
    print("=" * 60)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_critical_tests()
    sys.exit(0 if success else 1)