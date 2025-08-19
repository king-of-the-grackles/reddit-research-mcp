# Agent Reference

## Type Aliases

### ToolsToFinalOutputFunction

```python
ToolsToFinalOutputFunction: TypeAlias = Callable[
    [RunContextWrapper[TContext], list[FunctionToolResult]],
    MaybeAwaitable[ToolsToFinalOutputResult],
]
```

A function that takes a run context and a list of tool results, and returns a `ToolsToFinalOutputResult`.

## Classes

### ToolsToFinalOutputResult

```python
@dataclass
class ToolsToFinalOutputResult:
    is_final_output: bool
    """Whether this is the final output. If False, the LLM will run again and receive the tool call output."""
    
    final_output: Any | None = None
    """The final output. Can be None if `is_final_output` is False, otherwise must match the `output_type` of the agent."""
```

### StopAtTools

```python
class StopAtTools(TypedDict):
    stop_at_tool_names: list[str]
    """A list of tool names, any of which will stop the agent from running further."""
```

### MCPConfig

Configuration for MCP servers.

```python
class MCPConfig(TypedDict):
    convert_schemas_to_strict: NotRequired[bool]
    """If True, we will attempt to convert the MCP schemas to strict-mode schemas. 
    This is a best-effort conversion, so some schemas may not be convertible. Defaults to False."""
```

### AgentBase

Base class for `Agent` and `RealtimeAgent`.

```python
@dataclass
class AgentBase(Generic[TContext]):
    name: str
    """The name of the agent."""
    
    handoff_description: str | None = None
    """A description of the agent. This is used when the agent is used as a handoff, 
    so that an LLM knows what it does and when to invoke it."""
    
    tools: list[Tool] = field(default_factory=list)
    """A list of tools that the agent can use."""
    
    mcp_servers: list[MCPServer] = field(default_factory=list)
    """A list of Model Context Protocol servers that the agent can use. 
    Every time the agent runs, it will include tools from these servers in the list of available tools.
    NOTE: You are expected to manage the lifecycle of these servers. Specifically, you must call
    `server.connect()` before passing it to the agent, and `server.cleanup()` when the server is no longer needed."""
    
    mcp_config: MCPConfig = field(default_factory=lambda: MCPConfig())
    """Configuration for MCP servers."""
    
    async def get_mcp_tools(self, run_context: RunContextWrapper[TContext]) -> list[Tool]:
        """Fetches the available tools from the MCP servers."""
    
    async def get_all_tools(self, run_context: RunContextWrapper[TContext]) -> list[Tool]:
        """All agent tools, including MCP tools and function tools."""
```

### Agent

An agent is an AI model configured with instructions, tools, guardrails, handoffs and more.

```python
@dataclass
class Agent(AgentBase, Generic[TContext]):
    instructions: str | Callable[[RunContextWrapper[TContext], Agent[TContext]], MaybeAwaitable[str]] | None = None
    """The instructions for the agent. Will be used as the "system prompt" when this agent is invoked. 
    Can either be a string, or a function that dynamically generates instructions for the agent."""
    
    prompt: Prompt | DynamicPromptFunction | None = None
    """A prompt object (or a function that returns a Prompt). Prompts allow you to dynamically
    configure the instructions, tools and other config for an agent outside of your code. 
    Only usable with OpenAI models, using the Responses API."""
    
    handoffs: list[Agent[Any] | Handoff[TContext, Any]] = field(default_factory=list)
    """Handoffs are sub-agents that the agent can delegate to. You can provide a list of handoffs,
    and the agent can choose to delegate to them if relevant."""
    
    model: str | Model | None = None
    """The model implementation to use when invoking the LLM.
    By default, if not set, the agent will use the default model configured in
    `openai_provider.DEFAULT_MODEL` (currently "gpt-4o")."""
    
    model_settings: ModelSettings = field(default_factory=ModelSettings)
    """Configures model-specific tuning parameters (e.g. temperature, top_p)."""
    
    input_guardrails: list[InputGuardrail[TContext]] = field(default_factory=list)
    """A list of checks that run in parallel to the agent's execution, before generating a response. 
    Runs only if the agent is the first agent in the chain."""
    
    output_guardrails: list[OutputGuardrail[TContext]] = field(default_factory=list)
    """A list of checks that run on the final output of the agent, after generating a response.
    Runs only if the agent produces a final output."""
    
    output_type: type[Any] | AgentOutputSchemaBase | None = None
    """The type of the output object. If not provided, the output will be `str`. 
    In most cases, you should pass a regular Python type (e.g. a dataclass, Pydantic model, TypedDict, etc)."""
    
    hooks: AgentHooks[TContext] | None = None
    """A class that receives callbacks on various lifecycle events for this agent."""
    
    tool_use_behavior: Literal["run_llm_again", "stop_on_first_tool"] | StopAtTools | ToolsToFinalOutputFunction = "run_llm_again"
    """This lets you configure how tool use is handled:
    - "run_llm_again": The default behavior. Tools are run, and then the LLM receives the results and gets to respond.
    - "stop_on_first_tool": The output of the first tool call is used as the final output.
    - A StopAtTools object: The agent will stop running if any of the tools listed in stop_at_tool_names is called.
    - A function: It will be called with the run context and the list of tool results."""
    
    reset_tool_choice: bool = True
    """Whether to reset the tool choice to the default value after a tool has been called. 
    Defaults to True. This ensures that the agent doesn't enter an infinite loop of tool usage."""
```

## Methods

### Agent.clone()

Make a copy of the agent, with the given arguments changed.

```python
def clone(self, **kwargs: Any) -> Agent[TContext]:
    """Make a copy of the agent, with the given arguments changed.
    
    Notes:
        - Uses `dataclasses.replace`, which performs a **shallow copy**.
        - Mutable attributes like `tools` and `handoffs` are shallow-copied:
          new list objects are created only if overridden, but their contents
          (tool functions and handoff objects) are shared with the original.
        - To modify these independently, pass new lists when calling `clone()`.
    
    Example:
        new_agent = agent.clone(instructions="New instructions")
    """
```

### Agent.as_tool()

Transform this agent into a tool, callable by other agents.

```python
def as_tool(
    self,
    tool_name: str | None,
    tool_description: str | None,
    custom_output_extractor: Callable[[RunResult], Awaitable[str]] | None = None,
    is_enabled: bool | Callable[[RunContextWrapper[Any], AgentBase[Any]], MaybeAwaitable[bool]] = True,
) -> Tool:
    """Transform this agent into a tool, callable by other agents.
    
    This is different from handoffs in two ways:
    1. In handoffs, the new agent receives the conversation history. 
       In this tool, the new agent receives generated input.
    2. In handoffs, the new agent takes over the conversation. 
       In this tool, the new agent is called as a tool, and the conversation is continued by the original agent.
    
    Args:
        tool_name: The name of the tool. If not provided, the agent's name will be used.
        tool_description: The description of the tool, which should indicate what it does and when to use it.
        custom_output_extractor: A function that extracts the output from the agent. 
                                If not provided, the last message from the agent will be used.
        is_enabled: Whether the tool is enabled. Can be a bool or a callable that takes the run
                   context and agent and returns whether the tool is enabled. 
                   Disabled tools are hidden from the LLM at runtime.
    """
```

### Agent.get_system_prompt()

Get the system prompt for the agent.

```python
async def get_system_prompt(self, run_context: RunContextWrapper[TContext]) -> str | None:
    """Get the system prompt for the agent, either from instructions string or function."""
```

### Agent.get_prompt()

Get the prompt for the agent.

```python
async def get_prompt(self, run_context: RunContextWrapper[TContext]) -> ResponsePromptParam | None:
    """Get the prompt for the agent."""
```