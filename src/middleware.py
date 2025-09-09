"""
Middleware for handling parameter validation issues with AI clients.
"""

from fastmcp.server.middleware import Middleware, MiddlewareContext


class EmptyParameterCleanerMiddleware(Middleware):
    """Removes empty parameters from tool calls to parameterless functions.
    
    Some AI clients (particularly those using OpenAI function calling patterns)
    incorrectly send empty parameters to tools that don't accept any. This
    middleware cleans those parameters before they reach the tool handler.
    """
    
    # List of tools that should have no parameters
    NO_PARAM_TOOLS = ["discover_operations"]
    
    async def on_call_tool(self, context: MiddlewareContext, call_next):
        """Intercept tool calls and clean empty parameters.
        
        Args:
            context: The middleware context containing request information
            call_next: The next handler in the middleware chain
            
        Returns:
            The result from the tool execution
        """
        if context.params and "name" in context.params:
            tool_name = context.params["name"]
            
            if tool_name in self.NO_PARAM_TOOLS:
                args = context.params.get("arguments", {})
                
                # Remove arguments if they are:
                # - Empty dict {}
                # - Dict with all None values {"properties": None}
                # - Dict with empty string values {"properties": ""}
                if isinstance(args, dict):
                    has_real_values = any(
                        v is not None and v != "" 
                        for v in args.values()
                    )
                    if not has_real_values:
                        # Remove the arguments entirely from the params
                        context.params.pop("arguments", None)
        
        # Continue with cleaned parameters
        return await call_next(context)