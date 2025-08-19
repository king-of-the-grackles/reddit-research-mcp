# Tool Reference

## Type Aliases

### Tool

```python
Tool = Union[
    FunctionTool,
    FileSearchTool,
    WebSearchTool,
    ComputerTool,
    HostedMCPTool,
    LocalShellTool,
    ImageGenerationTool,
    CodeInterpreterTool,
]
```

A tool that can be used in an agent.

### MCPToolApprovalFunction

```python
MCPToolApprovalFunction = Callable[
    [MCPToolApprovalRequest],
    MaybeAwaitable[MCPToolApprovalFunctionResult],
]
```

A function that approves or rejects a tool call.

### LocalShellExecutor

```python
LocalShellExecutor = Callable[
    [LocalShellCommandRequest], MaybeAwaitable[str]
]
```

A function that executes a command on a shell.

## Classes

### FunctionTool

A tool that wraps a function. In most cases, you should use the `function_tool` helpers to create a FunctionTool.

```python
@dataclass
class FunctionTool:
    name: str
    """The name of the tool, as shown to the LLM. Generally the name of the function."""
    
    description: str
    """A description of the tool, as shown to the LLM."""
    
    params_json_schema: dict[str, Any]
    """The JSON schema for the tool's parameters."""
    
    on_invoke_tool: Callable[[ToolContext[Any], str], Awaitable[Any]]
    """A function that invokes the tool with the given context and parameters."""
    
    strict_json_schema: bool = True
    """Whether the JSON schema is in strict mode. We strongly recommend setting this to True."""
    
    is_enabled: bool | Callable[[RunContextWrapper[Any], AgentBase], MaybeAwaitable[bool]] = True
    """Whether the tool is enabled. Can be dynamic based on context/state."""
```

### FileSearchTool

A hosted tool that lets the LLM search through a vector store. Currently only supported with OpenAI models, using the Responses API.

```python
@dataclass
class FileSearchTool:
    vector_store_ids: list[str]
    """The IDs of the vector stores to search."""
    
    max_num_results: int | None = None
    """The maximum number of results to return."""
    
    include_search_results: bool = False
    """Whether to include the search results in the output produced by the LLM."""
    
    ranking_options: RankingOptions | None = None
    """Ranking options for search."""
    
    filters: Filters | None = None
    """A filter to apply based on file attributes."""
```

### WebSearchTool

A hosted tool that lets the LLM search the web. Currently only supported with OpenAI models, using the Responses API.

```python
@dataclass
class WebSearchTool:
    user_location: UserLocation | None = None
    """Optional location for the search. Lets you customize results to be relevant to a location."""
    
    search_context_size: Literal["low", "medium", "high"] = "medium"
    """The amount of context to use for the search."""
```

### ComputerTool

A hosted tool that lets the LLM control a computer.

```python
@dataclass
class ComputerTool:
    computer: Computer | AsyncComputer
    """The computer implementation, which describes the environment and dimensions of the computer."""
    
    on_safety_check: Callable[[ComputerToolSafetyCheckData], MaybeAwaitable[bool]] | None = None
    """Optional callback to acknowledge computer tool safety checks."""
```

### HostedMCPTool

A tool that allows the LLM to use a remote MCP server.

```python
@dataclass
class HostedMCPTool:
    tool_config: Mcp
    """The MCP tool config, which includes the server URL and other settings."""
    
    on_approval_request: MCPToolApprovalFunction | None = None
    """An optional function that will be called if approval is requested for an MCP tool."""
```

### CodeInterpreterTool

A tool that allows the LLM to execute code in a sandboxed environment.

```python
@dataclass
class CodeInterpreterTool:
    tool_config: CodeInterpreter
    """The tool config, which includes the container and other settings."""
```

### ImageGenerationTool

A tool that allows the LLM to generate images.

```python
@dataclass
class ImageGenerationTool:
    tool_config: ImageGeneration
    """The tool config, which image generation settings."""
```

### LocalShellTool

A tool that allows the LLM to execute commands on a shell.

```python
@dataclass
class LocalShellTool:
    executor: LocalShellExecutor
    """A function that executes a command on a shell."""
```

## Functions

### function_tool

Decorator to create a FunctionTool from a function.

```python
def function_tool(
    func: ToolFunction[...] | None = None,
    *,
    name_override: str | None = None,
    description_override: str | None = None,
    docstring_style: DocstringStyle | None = None,
    use_docstring_info: bool = True,
    failure_error_function: ToolErrorFunction | None = default_tool_error_function,
    strict_mode: bool = True,
    is_enabled: bool | Callable[[RunContextWrapper[Any], AgentBase], MaybeAwaitable[bool]] = True,
) -> FunctionTool | Callable[[ToolFunction[...]], FunctionTool]:
    """
    Decorator to create a FunctionTool from a function. By default, we will:
    1. Parse the function signature to create a JSON schema for the tool's parameters.
    2. Use the function's docstring to populate the tool's description.
    3. Use the function's docstring to populate argument descriptions.
    
    Args:
        func: The function to wrap.
        name_override: If provided, use this name for the tool instead of the function's name.
        description_override: If provided, use this description for the tool.
        docstring_style: If provided, use this style for the tool's docstring.
        use_docstring_info: If True, use the function's docstring to populate descriptions.
        failure_error_function: Function to generate an error message when the tool call fails.
        strict_mode: Whether to enable strict mode for the tool's JSON schema.
        is_enabled: Whether the tool is enabled. Can be dynamic based on context.
    """
```

### default_tool_error_function

The default tool error function, which returns a generic error message.

```python
def default_tool_error_function(ctx: RunContextWrapper[Any], error: Exception) -> str:
    """The default tool error function, which just returns a generic error message."""
    return f"An error occurred while running the tool. Please try again. Error: {str(error)}"
```

## Support Classes

### FunctionToolResult

```python
@dataclass
class FunctionToolResult:
    tool: FunctionTool
    """The tool that was run."""
    
    output: Any
    """The output of the tool."""
    
    run_item: RunItem
    """The run item that was produced as a result of the tool call."""
```

### ComputerToolSafetyCheckData

```python
@dataclass
class ComputerToolSafetyCheckData:
    ctx_wrapper: RunContextWrapper[Any]
    """The run context."""
    
    agent: Agent[Any]
    """The agent performing the computer action."""
    
    tool_call: ResponseComputerToolCall
    """The computer tool call."""
    
    safety_check: PendingSafetyCheck
    """The pending safety check to acknowledge."""
```

### MCPToolApprovalRequest

```python
@dataclass
class MCPToolApprovalRequest:
    ctx_wrapper: RunContextWrapper[Any]
    """The run context."""
    
    data: McpApprovalRequest
    """The data from the MCP tool approval request."""
```

### MCPToolApprovalFunctionResult

```python
class MCPToolApprovalFunctionResult(TypedDict):
    approve: bool
    """Whether to approve the tool call."""
    
    reason: NotRequired[str]
    """An optional reason, if rejected."""
```

### LocalShellCommandRequest

```python
@dataclass
class LocalShellCommandRequest:
    ctx_wrapper: RunContextWrapper[Any]
    """The run context."""
    
    data: LocalShellCall
    """The data from the local shell tool call."""
```