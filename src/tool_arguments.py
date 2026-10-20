"""Repair argument shapes clients commonly send, before FastMCP validates them.

Validation runs before a tool body executes, so these fixes cannot live inside
the tools themselves.
"""
from fastmcp.server.middleware import Middleware

OPERATION_TOOLS = {"get_operation_schema", "execute_operation"}


def normalize_arguments(tool, arguments):
    if tool not in OPERATION_TOOLS:
        return arguments
    arguments = dict(arguments)
    if "operation" in arguments and "operation_id" not in arguments:
        arguments["operation_id"] = arguments.pop("operation")
    if tool == "execute_operation" and isinstance(arguments.get("parameters", {}), dict):
        # Operation parameters sent beside operation_id instead of inside
        # `parameters`. Explicitly nested values win over duplicates.
        extra = {k: arguments.pop(k) for k in list(arguments) if k not in ("operation_id", "parameters")}
        if extra:
            arguments["parameters"] = {**extra, **arguments.get("parameters", {})}
    return arguments


class ArgumentNormalization(Middleware):
    async def on_call_tool(self, context, call_next):
        arguments = normalize_arguments(context.message.name, context.message.arguments or {})
        message = context.message.model_copy(update={"arguments": arguments})
        return await call_next(context.copy(message=message))
