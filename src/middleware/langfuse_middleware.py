#!/usr/bin/env uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "fastmcp>=0.8.0",
#     "langfuse>=2.50.0",
# ]
# ///

"""Langfuse observability middleware for Reddit MCP server."""
import time
import json
import secrets
from typing import Any, Dict, Optional
from fastmcp.server.middleware import Middleware, MiddlewareContext

class LangfuseMiddleware(Middleware):
    """Middleware for tracking MCP operations with Langfuse."""
    
    def __init__(self, langfuse_client):
        """Initialize with Langfuse client."""
        self.langfuse = langfuse_client
        self.active_traces = {}
    
    async def on_call_tool(self, context: MiddlewareContext, call_next):
        """Track tool calls with enhanced metadata extraction."""
        start_time = time.perf_counter()
        tool_name = context.message.name if hasattr(context.message, 'name') else 'unknown'
        
        # Create or get trace for this request
        trace_id = self._get_or_create_trace(context)
        
        # Enhanced: Access tool metadata via FastMCP context
        tool_metadata = await self._extract_tool_metadata(context, tool_name)
        
        # Start a span for this tool call
        span = self.langfuse.span(
            trace_id=trace_id,
            name=f"tool_{tool_name}",
            input=self._extract_input(context),
            metadata={
                "tool": tool_name,
                "method": context.method,
                "source": context.source,
                **tool_metadata  # Include FastMCP tool metadata
            }
        )
        
        try:
            # Execute the tool
            result = await call_next(context)
            
            # Calculate duration
            duration_ms = (time.perf_counter() - start_time) * 1000
            
            # Extract Reddit-specific metadata from result
            reddit_metadata = await self._extract_reddit_metadata(tool_name, context, result)
            
            # Update span with output
            span.update(
                output=self._extract_output(result),
                metadata={
                    "duration_ms": duration_ms,
                    "success": True,
                    **tool_metadata,
                    **reddit_metadata
                }
            )
            
            # End the span
            span.end()
            
            return result
            
        except Exception as e:
            # Track error
            duration_ms = (time.perf_counter() - start_time) * 1000
            
            span.update(
                output={"error": str(e)},
                metadata={
                    "duration_ms": duration_ms,
                    "success": False,
                    "error_type": type(e).__name__
                },
                level="ERROR"
            )
            
            span.end()
            raise
    
    async def on_request(self, context: MiddlewareContext, call_next):
        """Track all MCP requests."""
        # Only create top-level trace for non-tool calls
        if not self._is_tool_call(context):
            trace_id = self._get_or_create_trace(context)
            
            # Enhance trace with server metadata if available
            enhanced_metadata = await self._extract_enhanced_metadata(context)
            
            # Update trace with request metadata
            trace = self.langfuse.trace(id=trace_id)
            trace.update(
                metadata={
                    "mcp_method": context.method,
                    "request_type": context.type,
                    "source": context.source,
                    **enhanced_metadata
                }
            )
        
        return await call_next(context)
    
    def _get_or_create_trace(self, context: MiddlewareContext) -> str:
        """Get existing trace or create new one with W3C-compliant ID."""
        # Use context ID or timestamp as trace key
        context_id = id(context)
        
        if context_id not in self.active_traces:
            # Generate W3C-compliant trace ID (32 hex chars)
            trace_id = self._ensure_w3c_trace_id()
            
            trace = self.langfuse.trace(
                id=trace_id,
                name="reddit_mcp_request",
                input={"method": context.method},
                metadata={
                    "mcp_version": "1.0",
                    "server": "reddit-research-mcp"
                },
                tags=["reddit", "mcp"]
            )
            self.active_traces[context_id] = trace.id
            
            # Clean up old traces (simple memory management)
            if len(self.active_traces) > 100:
                # Remove oldest traces
                self.active_traces = dict(list(self.active_traces.items())[-50:])
        
        return self.active_traces[context_id]
    
    def _ensure_w3c_trace_id(self) -> str:
        """Generate W3C-compliant trace ID (32 hex chars)."""
        # W3C format: 32 lowercase hex characters (16 bytes)
        return secrets.token_hex(16)
    
    def _is_tool_call(self, context: MiddlewareContext) -> bool:
        """Check if this is a tool call."""
        return context.method == "tools/call"
    
    async def _extract_tool_metadata(self, context: MiddlewareContext, tool_name: str) -> Dict[str, Any]:
        """Extract tool metadata using FastMCP context."""
        metadata = {}
        
        if context.fastmcp_context:
            try:
                # Access the tool object to check its metadata
                tool = await context.fastmcp_context.fastmcp.get_tool(tool_name)
                
                metadata = {
                    "tool_tags": tool.tags if hasattr(tool, 'tags') else [],
                    "tool_enabled": tool.enabled if hasattr(tool, 'enabled') else True,
                    "tool_description": tool.description[:100] if hasattr(tool, 'description') else None
                }
            except Exception:
                # Tool not found or error accessing metadata
                pass
        
        return metadata
    
    async def _extract_enhanced_metadata(self, context: MiddlewareContext) -> Dict[str, Any]:
        """Extract enhanced metadata using FastMCP context."""
        metadata = {}
        
        if context.fastmcp_context:
            try:
                # Access server-level information
                server = context.fastmcp_context.fastmcp
                
                # Get basic server stats
                metadata["server_info"] = {
                    "name": server.name if hasattr(server, 'name') else "unknown",
                    "has_tools": hasattr(server, 'list_tools'),
                    "has_resources": hasattr(server, 'list_resources'),
                    "has_prompts": hasattr(server, 'list_prompts')
                }
            except Exception as e:
                metadata["metadata_error"] = str(e)
        
        return metadata
    
    def _extract_input(self, context: MiddlewareContext) -> Dict[str, Any]:
        """Extract input data from context."""
        try:
            if hasattr(context.message, 'arguments'):
                return context.message.arguments
            elif hasattr(context, 'message'):
                return {"raw": str(context.message)}
            return {}
        except Exception:
            return {}
    
    def _extract_output(self, result: Any) -> Dict[str, Any]:
        """Extract output data from result."""
        try:
            if isinstance(result, dict):
                return result
            elif hasattr(result, '__dict__'):
                return result.__dict__
            else:
                return {"result": str(result)}
        except Exception:
            return {"result": "Unable to serialize"}
    
    async def _extract_reddit_metadata(self, tool_name: str, context: MiddlewareContext, result: Any) -> Dict[str, Any]:
        """Extract Reddit-specific metadata based on tool."""
        metadata = {}
        
        try:
            # Extract based on tool name
            if tool_name == "discover_operations":
                metadata["operation_type"] = "discovery"
                
            elif tool_name == "get_operation_schema":
                if hasattr(context.message, 'arguments'):
                    metadata["operation_id"] = context.message.arguments.get("operation_id")
                    metadata["operation_type"] = "schema"
                    
            elif tool_name == "execute_operation":
                if hasattr(context.message, 'arguments'):
                    args = context.message.arguments
                    metadata["operation_id"] = args.get("operation_id")
                    metadata["operation_type"] = "execution"
                    
                    # Extract parameters details
                    params = args.get("parameters", {})
                    
                    # Track subreddit operations
                    if "subreddit_name" in params:
                        metadata["subreddit"] = params["subreddit_name"]
                    elif "subreddit_names" in params:
                        metadata["subreddits"] = params["subreddit_names"]
                        metadata["subreddit_count"] = len(params["subreddit_names"])
                    
                    # Track query operations
                    if "query" in params:
                        metadata["search_query"] = params["query"]
                    
                    # Track limits
                    if "limit" in params:
                        metadata["limit"] = params["limit"]
                    
                    # Extract results metadata
                    if isinstance(result, dict):
                        data = result.get("data", {})
                        if isinstance(data, dict):
                            # Track confidence scores for discovery
                            if "subreddits" in data and isinstance(data["subreddits"], list):
                                confidences = [s.get("confidence", 0) for s in data["subreddits"] if isinstance(s, dict)]
                                if confidences:
                                    metadata["avg_confidence"] = sum(confidences) / len(confidences)
                                    metadata["max_confidence"] = max(confidences)
                            
                            # Track post counts
                            if "posts" in data:
                                metadata["post_count"] = len(data.get("posts", []))
                            
                            # Track error recovery
                            if "recovery" in result:
                                metadata["recovery_suggestion"] = result["recovery"]
        
        except Exception as e:
            metadata["metadata_extraction_error"] = str(e)
        
        return metadata