#!/usr/bin/env python3
"""
End-to-End Smoke Test
Simulates real MCP client usage to verify the complete workflow.
"""

import sys
import os
from pathlib import Path
import time
import json
from unittest.mock import patch, Mock

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def simulate_mcp_workflow():
    """Simulate a complete MCP client workflow."""
    print("=" * 60)
    print("END-TO-END SMOKE TEST - MCP WORKFLOW")
    print("=" * 60)
    
    results = {
        "steps": [],
        "errors": [],
        "warnings": [],
        "langfuse_trace": None,
        "memory_baseline": None,
        "memory_after": None
    }
    
    # Track memory usage
    import psutil
    import os
    process = psutil.Process(os.getpid())
    results["memory_baseline"] = process.memory_info().rss / 1024 / 1024  # MB
    
    print(f"\n📊 Memory baseline: {results['memory_baseline']:.2f} MB")
    
    try:
        # Step 1: Initialize server components
        print("\n1️⃣ Initializing server components...")
        start_time = time.time()
        
        from src.server import (
            discover_operations,
            get_operation_schema,
            execute_operation,
            mcp
        )
        from src.config import get_langfuse_client, get_reddit_client
        
        init_time = time.time() - start_time
        results["steps"].append({
            "step": "Server initialization",
            "status": "success",
            "duration_ms": init_time * 1000
        })
        print(f"   ✅ Server initialized in {init_time*1000:.2f}ms")
        
        # Check Langfuse status
        langfuse_client = get_langfuse_client()
        if langfuse_client:
            print("   ✅ Langfuse client available")
            results["langfuse_available"] = True
        else:
            print("   ⚠️  Langfuse not configured (observability disabled)")
            results["warnings"].append("Langfuse not configured")
            results["langfuse_available"] = False
        
        # Check Reddit status
        try:
            reddit_client = get_reddit_client()
            print("   ✅ Reddit client available")
            results["reddit_available"] = True
        except Exception as e:
            print(f"   ⚠️  Reddit client not available: {e}")
            results["warnings"].append(f"Reddit not configured: {e}")
            results["reddit_available"] = False
        
        # Step 2: Discover operations (Layer 1)
        print("\n2️⃣ Testing Layer 1: discover_operations...")
        start_time = time.time()
        
        # FastMCP tools need to use .fn to call the actual function
        operations = discover_operations.fn()
        
        discover_time = time.time() - start_time
        results["steps"].append({
            "step": "discover_operations",
            "status": "success",
            "duration_ms": discover_time * 1000,
            "operations_count": len(operations.get("operations", {}))
        })
        
        print(f"   ✅ Discovered {len(operations['operations'])} operations in {discover_time*1000:.2f}ms")
        print(f"   Operations: {', '.join(list(operations['operations'].keys())[:3])}...")
        
        # Step 3: Get operation schema (Layer 2)
        print("\n3️⃣ Testing Layer 2: get_operation_schema...")
        test_operations = ["discover_subreddits", "fetch_multiple", "fetch_comments"]
        
        for op_id in test_operations:
            start_time = time.time()
            schema = get_operation_schema.fn(op_id)
            schema_time = time.time() - start_time
            
            if "error" not in schema:
                results["steps"].append({
                    "step": f"get_operation_schema({op_id})",
                    "status": "success",
                    "duration_ms": schema_time * 1000,
                    "param_count": len(schema.get("parameters", {}))
                })
                print(f"   ✅ Schema for '{op_id}' retrieved in {schema_time*1000:.2f}ms")
            else:
                results["errors"].append(f"Failed to get schema for {op_id}")
                print(f"   ❌ Failed to get schema for '{op_id}'")
        
        # Step 4: Execute operation (Layer 3)
        print("\n4️⃣ Testing Layer 3: execute_operation...")
        
        # Test with discover_subreddits (doesn't require Reddit client)
        start_time = time.time()
        exec_result = execute_operation.fn(
            operation_id="discover_subreddits",
            parameters={"query": "python programming", "limit": 5}
        )
        exec_time = time.time() - start_time
        
        if exec_result.get("success"):
            results["steps"].append({
                "step": "execute_operation(discover_subreddits)",
                "status": "success",
                "duration_ms": exec_time * 1000
            })
            print(f"   ✅ Operation executed successfully in {exec_time*1000:.2f}ms")
            
            # Check if we got results
            if "data" in exec_result and "subreddits" in exec_result["data"]:
                subreddit_count = len(exec_result["data"]["subreddits"])
                print(f"   📊 Found {subreddit_count} subreddits")
        else:
            error_msg = exec_result.get("error", "Unknown error")
            recovery = exec_result.get("recovery", "No recovery suggestion")
            results["warnings"].append(f"Operation failed: {error_msg}")
            print(f"   ⚠️  Operation failed: {error_msg}")
            print(f"   💡 Recovery: {recovery}")
        
        # Step 5: Test error handling
        print("\n5️⃣ Testing error handling...")
        start_time = time.time()
        
        # Test with invalid operation
        error_result = execute_operation.fn(
            operation_id="invalid_operation",
            parameters={}
        )
        
        if not error_result.get("success") and "error" in error_result:
            results["steps"].append({
                "step": "Error handling test",
                "status": "success",
                "duration_ms": (time.time() - start_time) * 1000
            })
            print(f"   ✅ Error handling works correctly")
            print(f"   📝 Error message: {error_result['error'][:50]}...")
        else:
            results["errors"].append("Error handling did not work as expected")
            print(f"   ❌ Error handling failed")
        
        # Step 6: Memory check
        print("\n6️⃣ Checking memory usage...")
        results["memory_after"] = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = results["memory_after"] - results["memory_baseline"]
        
        print(f"   📊 Memory after tests: {results['memory_after']:.2f} MB")
        print(f"   📈 Memory increase: {memory_increase:.2f} MB")
        
        if memory_increase < 50:  # Less than 50MB increase
            print(f"   ✅ Memory usage acceptable")
        else:
            results["warnings"].append(f"High memory increase: {memory_increase:.2f} MB")
            print(f"   ⚠️  High memory increase detected")
        
        # Step 7: Langfuse trace verification
        if langfuse_client:
            print("\n7️⃣ Verifying Langfuse traces...")
            try:
                # Flush traces
                langfuse_client.flush()
                results["langfuse_trace"] = "Flushed successfully"
                print(f"   ✅ Traces flushed to Langfuse")
                print(f"   📊 Check dashboard at: {os.environ.get('LANGFUSE_HOST', 'https://cloud.langfuse.com')}")
            except Exception as e:
                results["warnings"].append(f"Langfuse flush error: {e}")
                print(f"   ⚠️  Could not flush traces: {e}")
        
    except Exception as e:
        results["errors"].append(f"Unexpected error: {str(e)}")
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
    
    # Generate summary
    print("\n" + "=" * 60)
    print("SMOKE TEST SUMMARY")
    print("=" * 60)
    
    successful_steps = len([s for s in results["steps"] if s.get("status") == "success"])
    total_steps = len(results["steps"])
    
    print(f"\n✅ Successful steps: {successful_steps}/{total_steps}")
    
    if results["errors"]:
        print(f"\n❌ Errors ({len(results['errors'])}):")
        for error in results["errors"]:
            print(f"   - {error}")
    
    if results["warnings"]:
        print(f"\n⚠️  Warnings ({len(results['warnings'])}):")
        for warning in results["warnings"]:
            print(f"   - {warning}")
    
    # Performance summary
    total_duration = sum(s.get("duration_ms", 0) for s in results["steps"])
    print(f"\n⏱️  Total execution time: {total_duration:.2f}ms")
    
    # Final verdict
    print("\n" + "=" * 60)
    if not results["errors"] and successful_steps == total_steps:
        print("🎉 SMOKE TEST PASSED - READY FOR PRODUCTION!")
        return True
    elif not results["errors"]:
        print("✅ SMOKE TEST PASSED WITH WARNINGS")
        print("   Server is functional but check warnings above")
        return True
    else:
        print("❌ SMOKE TEST FAILED - FIX ERRORS BEFORE PRODUCTION")
        return False


def main():
    """Run the smoke test."""
    # Set minimal test environment if not already set
    if not os.environ.get("REDDIT_CLIENT_ID"):
        print("ℹ️  No Reddit credentials found, using test mode")
        os.environ["REDDIT_CLIENT_ID"] = "test_id"
        os.environ["REDDIT_CLIENT_SECRET"] = "test_secret"
    
    success = simulate_mcp_workflow()
    
    print("\n" + "=" * 60)
    print("Next steps:")
    if success:
        print("1. Check Langfuse dashboard for traces (if configured)")
        print("2. Test with real MCP client (Claude or MCP Inspector)")
        print("3. Run security tests: python test_security_critical.py")
        print("4. Deploy to production! 🚀")
    else:
        print("1. Fix errors identified above")
        print("2. Re-run smoke test")
        print("3. Check logs for more details")
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())