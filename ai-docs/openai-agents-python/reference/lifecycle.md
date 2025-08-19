# Lifecycle Reference

## Module Attributes

### RunHooks (module-attribute)
```python
RunHooks = RunHooksBase[TContext, Agent]
```
Run hooks when using `Agent`.

### AgentHooks (module-attribute)
```python
AgentHooks = AgentHooksBase[TContext, Agent]
```
Agent hooks for `Agent`s.

## RunHooksBase

Bases: `Generic[TContext, TAgent]`

A class that receives callbacks on various lifecycle events in an agent run. Subclass and override the methods you need.

### Methods

#### on_llm_start(async)
```python
async def on_llm_start(
    context: RunContextWrapper[TContext],
    agent: Agent[TContext],
    system_prompt: Optional[str],
    input_items: list[TResponseInputItem],
) -> None
```
Called just before invoking the LLM for this agent.

#### on_llm_end(async)
```python
async def on_llm_end(
    context: RunContextWrapper[TContext],
    agent: Agent[TContext],
    response: ModelResponse,
) -> None
```
Called immediately after the LLM call returns for this agent.

#### on_agent_start(async)
```python
async def on_agent_start(
    context: RunContextWrapper[TContext], 
    agent: TAgent
) -> None
```
Called before the agent is invoked. Called each time the current agent changes.

#### on_agent_end(async)
```python
async def on_agent_end(
    context: RunContextWrapper[TContext],
    agent: TAgent,
    output: Any,
) -> None
```
Called when the agent produces a final output.

#### on_handoff(async)
```python
async def on_handoff(
    context: RunContextWrapper[TContext],
    from_agent: TAgent,
    to_agent: TAgent,
) -> None
```
Called when a handoff occurs.

#### on_tool_start(async)
```python
async def on_tool_start(
    context: RunContextWrapper[TContext],
    agent: TAgent,
    tool: Tool,
) -> None
```
Called concurrently with tool invocation.

#### on_tool_end(async)
```python
async def on_tool_end(
    context: RunContextWrapper[TContext],
    agent: TAgent,
    tool: Tool,
    result: str,
) -> None
```
Called after a tool is invoked.

## AgentHooksBase

Bases: `Generic[TContext, TAgent]`

A class that receives callbacks on various lifecycle events for a specific agent. You can set this on `agent.hooks` to receive events for that specific agent.

Subclass and override the methods you need.

### Methods

#### on_start(async)
```python
async def on_start(
    context: RunContextWrapper[TContext], 
    agent: TAgent
) -> None
```
Called before the agent is invoked. Called each time the running agent is changed to this agent.

#### on_end(async)
```python
async def on_end(
    context: RunContextWrapper[TContext],
    agent: TAgent,
    output: Any,
) -> None
```
Called when the agent produces a final output.

#### on_handoff(async)
```python
async def on_handoff(
    context: RunContextWrapper[TContext],
    agent: TAgent,
    source: TAgent,
) -> None
```
Called when the agent is being handed off to. The `source` is the agent that is handing off to this agent.

#### on_tool_start(async)
```python
async def on_tool_start(
    context: RunContextWrapper[TContext],
    agent: TAgent,
    tool: Tool,
) -> None
```
Called concurrently with tool invocation.

#### on_tool_end(async)
```python
async def on_tool_end(
    context: RunContextWrapper[TContext],
    agent: TAgent,
    tool: Tool,
    result: str,
) -> None
```
Called after a tool is invoked.

#### on_llm_start(async)
```python
async def on_llm_start(
    context: RunContextWrapper[TContext],
    agent: Agent[TContext],
    system_prompt: Optional[str],
    input_items: list[TResponseInputItem],
) -> None
```
Called immediately before the agent issues an LLM call.

#### on_llm_end(async)
```python
async def on_llm_end(
    context: RunContextWrapper[TContext],
    agent: Agent[TContext],
    response: ModelResponse,
) -> None
```
Called immediately after the agent receives the LLM response.

## Usage Examples

### Creating Custom Run Hooks

```python
from agents import RunHooks, Agent, Runner

class MyRunHooks(RunHooks):
    async def on_agent_start(self, context, agent):
        print(f"Agent {agent.name} is starting")
    
    async def on_agent_end(self, context, agent, output):
        print(f"Agent {agent.name} completed with output: {output}")
    
    async def on_tool_start(self, context, agent, tool):
        print(f"Tool {tool.name} is being invoked")
    
    async def on_tool_end(self, context, agent, tool, result):
        print(f"Tool {tool.name} returned: {result}")

# Use the hooks
agent = Agent(name="My Agent")
result = await Runner.run(
    agent, 
    "Hello", 
    hooks=MyRunHooks()
)
```

### Creating Custom Agent Hooks

```python
from agents import AgentHooks, Agent

class MyAgentHooks(AgentHooks):
    async def on_start(self, context, agent):
        print(f"Starting {agent.name}")
    
    async def on_end(self, context, agent, output):
        print(f"Finished {agent.name}")
    
    async def on_handoff(self, context, agent, source):
        print(f"Received handoff from {source.name}")

# Attach hooks to a specific agent
agent = Agent(
    name="My Agent",
    hooks=MyAgentHooks()
)
```

## Notes

- All hook methods are async and should be defined as `async def`
- Hook methods are optional - only override the ones you need
- RunHooks receive events for all agents in the run
- AgentHooks only receive events for the specific agent they're attached to
- Hooks are useful for logging, monitoring, debugging, and adding custom behavior
- Exceptions raised in hooks will propagate and interrupt the agent execution