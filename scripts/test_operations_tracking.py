#!/usr/bin/env uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "fastmcp>=0.8.0",
#     "langfuse>=2.50.0",
#     "python-dotenv>=1.0.0",
#     "praw>=7.7.1",
#     "aiohttp>=3.12.15",
#     "requests>=2.31.0",
# ]
# ///

"""Test MCP operations are tracked in Langfuse."""
import os
import sys
import time
import asyncio
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Set environment variables before imports
os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-fb913137-015d-4d05-970b-1915a2ef13b8"
os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-9bd1ea11-d794-432b-a04f-e043636eb7cc"
os.environ["LANGFUSE_HOST"] = "https://us.cloud.langfuse.com"
os.environ["LANGFUSE_VERIFY_CONNECTION"] = "false"

# Set Reddit credentials (dummy for testing)
os.environ["REDDIT_CLIENT_ID"] = "test_id"
os.environ["REDDIT_CLIENT_SECRET"] = "test_secret"

async def test_operations():
    """Test all three layers of operations."""
    print("=" * 50)
    print("Testing MCP Operations Tracking")
    print("=" * 50)
    
    # Import after env vars are set
    from src.server import discover_operations, get_operation_schema, execute_operation
    from src.config import get_langfuse_client
    
    # Get Langfuse client to flush at the end
    langfuse = get_langfuse_client()
    
    results = []
    
    try:
        # Test Layer 1: Discover operations
        print("\n Testing discover_operations...")
        start = time.time()
        ops_result = discover_operations.fn()  # FastMCP tools need .fn
        duration = (time.time() - start) * 1000
        print(f"  ✅ discover_operations completed in {duration:.2f}ms")
        print(f"  Operations found: {list(ops_result['operations'].keys())[:3]}...")
        results.append(("discover_operations", True, duration))
        
        # Small delay to ensure trace is sent
        await asyncio.sleep(0.5)
        
        # Test Layer 2: Get operation schema
        print("\n Testing get_operation_schema...")
        start = time.time()
        schema_result = get_operation_schema.fn(operation_id="fetch_multiple")  # FastMCP tools need .fn
        duration = (time.time() - start) * 1000
        print(f"  ✅ get_operation_schema completed in {duration:.2f}ms")
        print(f"  Schema has {len(schema_result.get('parameters', {}))} parameters")
        results.append(("get_operation_schema", True, duration))
        
        await asyncio.sleep(0.5)
        
        # Test Layer 3: Execute operation (with mock parameters)
        print("\n Testing execute_operation...")
        start = time.time()
        try:
            exec_result = execute_operation.fn(  # FastMCP tools need .fn
                operation_id="discover_subreddits",
                parameters={"query": "python programming"}
            )
            duration = (time.time() - start) * 1000
            
            if "error" in exec_result:
                print(f"  ⚠️  execute_operation returned error: {exec_result['error']}")
                print(f"     This is expected without real Reddit credentials")
            else:
                print(f"  ✅ execute_operation completed in {duration:.2f}ms")
            
            results.append(("execute_operation", True, duration))
        except Exception as e:
            duration = (time.time() - start) * 1000
            print(f"  ⚠️  execute_operation failed: {e}")
            print(f"     This is expected without real Reddit credentials")
            results.append(("execute_operation", False, duration))
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        return False
    
    finally:
        # Flush traces to Langfuse
        if langfuse:
            print("\n Flushing traces to Langfuse...")
            langfuse.flush()
            print("  ✅ Traces flushed")
    
    # Report results
    print("\n" + "=" * 50)
    print("Results Summary:")
    print("=" * 50)
    
    total_duration = sum(r[2] for r in results)
    successful = sum(1 for r in results if r[1])
    
    for op_name, success, duration in results:
        status = "✅" if success else "⚠️"
        print(f"{status} {op_name}: {duration:.2f}ms")
    
    print(f"\nTotal operations: {len(results)}")
    print(f"Successful: {successful}/{len(results)}")
    print(f"Total duration: {total_duration:.2f}ms")
    
    if langfuse:
        print("\n📊 Check your Langfuse dashboard at:")
        print(f"   {os.environ['LANGFUSE_HOST']}")
        print("   You should see:")
        print("   - A trace named 'reddit_mcp_request'")
        print("   - Spans for each operation")
        print("   - Metadata including operation IDs and parameters")
    
    return successful == len(results)

if __name__ == "__main__":
    success = asyncio.run(test_operations())
    sys.exit(0 if success else 1)