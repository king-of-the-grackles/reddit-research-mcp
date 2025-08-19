# Runner Reference

## Runner

The Runner class provides methods to execute agent workflows.

### Methods

#### run (async, classmethod)
```python
@classmethod
async def run(
    starting_agent: Agent[TContext],
    input: str | list[TResponseInputItem],
    *,
    context: TContext | None = None,
    max_turns: int = DEFAULT_MAX_TURNS,
    hooks: RunHooks[TContext] | None = None,
    run_config: RunConfig | None = None,
    previous_response_id: str | None = None,
    session: Session | None = None,
) -> RunResult
```

Run a workflow starting at the given agent. The agent will run in a loop until a final output is generated. 

The loop runs like so:
1. The agent is invoked with the given input.
2. If there is a final output (i.e. the agent produces something of type `agent.output_type`), the loop terminates.
3. If there's a handoff, we run the loop again, with the new agent.
4. Else, we run tool calls (if any), and re-run the loop.

In two cases, the agent may raise an exception:
1. If the max_turns is exceeded, a MaxTurnsExceeded exception is raised.
2. If a guardrail tripwire is triggered, a GuardrailTripwireTriggered exception is raised.

Note that only the first agent's input guardrails are run.

**Args:**
- `starting_agent`: The starting agent to run.
- `input`: The initial input to the agent. You can pass a single string for a user message, or a list of input items.
- `context`: The context to run the agent with.
- `max_turns`: The maximum number of turns to run the agent for. A turn is defined as one AI invocation (including any tool calls that might occur).
- `hooks`: An object that receives callbacks on various lifecycle events.
- `run_config`: Global settings for the entire agent run.
- `previous_response_id`: The ID of the previous response, if using OpenAI models via the Responses API, this allows you to skip passing in input from the previous turn.
- `session`: Session object for maintaining conversation history.

**Returns:**
- A run result containing all the inputs, guardrail results and the output of the last agent. Agents may perform handoffs, so we don't know the specific type of the output.

#### run_sync (classmethod)
```python
@classmethod
def run_sync(
    starting_agent: Agent[TContext],
    input: str | list[TResponseInputItem],
    *,
    context: TContext | None = None,
    max_turns: int = DEFAULT_MAX_TURNS,
    hooks: RunHooks[TContext] | None = None,
    run_config: RunConfig | None = None,
    previous_response_id: str | None = None,
    session: Session | None = None,
) -> RunResult
```

Run a workflow synchronously, starting at the given agent. Note that this just wraps the `run` method, so it will not work if there's already an event loop (e.g. inside an async function, or in a Jupyter notebook or async context like FastAPI). For those cases, use the `run` method instead.

The agent will run in a loop until a final output is generated (same behavior as `run`).

**Args:** Same as `run` method.

**Returns:** Same as `run` method.

#### run_streamed (classmethod)
```python
@classmethod
def run_streamed(
    starting_agent: Agent[TContext],
    input: str | list[TResponseInputItem],
    context: TContext | None = None,
    max_turns: int = DEFAULT_MAX_TURNS,
    hooks: RunHooks[TContext] | None = None,
    run_config: RunConfig | None = None,
    previous_response_id: str | None = None,
    session: Session | None = None,
) -> RunResultStreaming
```

Run a workflow starting at the given agent in streaming mode. The returned result object contains a method you can use to stream semantic events as they are generated.

The agent will run in a loop until a final output is generated (same behavior as `run`).

**Args:** Same as `run` method.

**Returns:**
- A result object that contains data about the run, as well as a method to stream events.

## RunConfig (dataclass)

Configures settings for the entire agent run.

### Attributes

#### model (class-attribute, instance-attribute)
```python
model: str | Model | None = None
```
The model to use for the entire agent run. If set, will override the model set on every agent. The model_provider passed in below must be able to resolve this model name.

#### model_provider (class-attribute, instance-attribute)
```python
model_provider: ModelProvider = field(default_factory=MultiProvider)
```
The model provider to use when looking up string model names. Defaults to OpenAI.

#### model_settings (class-attribute, instance-attribute)
```python
model_settings: ModelSettings | None = None
```
Configure global model settings. Any non-null values will override the agent-specific model settings.

#### handoff_input_filter (class-attribute, instance-attribute)
```python
handoff_input_filter: HandoffInputFilter | None = None
```
A global input filter to apply to all handoffs. If `Handoff.input_filter` is set, then that will take precedence. The input filter allows you to edit the inputs that are sent to the new agent. See the documentation in `Handoff.input_filter` for more details.

#### input_guardrails (class-attribute, instance-attribute)
```python
input_guardrails: list[InputGuardrail[Any]] | None = None
```
A list of input guardrails to run on the initial run input.

#### output_guardrails (class-attribute, instance-attribute)
```python
output_guardrails: list[OutputGuardrail[Any]] | None = None
```
A list of output guardrails to run on the final output of the run.

#### tracing_disabled (class-attribute, instance-attribute)
```python
tracing_disabled: bool = False
```
Whether tracing is disabled for the agent run. If disabled, we will not trace the agent run.

#### trace_include_sensitive_data (class-attribute, instance-attribute)
```python
trace_include_sensitive_data: bool = True
```
Whether we include potentially sensitive data (for example: inputs/outputs of tool calls or LLM generations) in traces. If False, we'll still create spans for these events, but the sensitive data will not be included.

#### workflow_name (class-attribute, instance-attribute)
```python
workflow_name: str = 'Agent workflow'
```
The name of the run, used for tracing. Should be a logical name for the run, like "Code generation workflow" or "Customer support agent".

#### trace_id (class-attribute, instance-attribute)
```python
trace_id: str | None = None
```
A custom trace ID to use for tracing. If not provided, we will generate a new trace ID.

#### group_id (class-attribute, instance-attribute)
```python
group_id: str | None = None
```
A grouping identifier to use for tracing, to link multiple traces from the same conversation or process. For example, you might use a chat thread ID.

#### trace_metadata (class-attribute, instance-attribute)
```python
trace_metadata: dict[str, Any] | None = None
```
An optional dictionary of additional metadata to include with the trace.

#### call_model_input_filter (class-attribute, instance-attribute)
```python
call_model_input_filter: CallModelInputFilter | None = None
```
Optional callback that is invoked immediately before calling the model. It receives the current agent, context and the model input (instructions and input items), and must return a possibly modified `ModelInputData` to use for the model call.

This allows you to edit the input sent to the model e.g. to stay within a token limit. For example, you can use this to add a system prompt to the input.

## Usage Examples

### Basic Usage
```python
from agents import Agent, Runner

agent = Agent(name="Assistant", instructions="You are a helpful assistant.")

# Async execution
result = await Runner.run(agent, "Hello, how are you?")
print(result.final_output)

# Sync execution (not in async context)
result = Runner.run_sync(agent, "Hello, how are you?")
print(result.final_output)
```

### Streaming Usage
```python
from agents import Agent, Runner

agent = Agent(name="Assistant", instructions="You are a helpful assistant.")

# Get streaming result
result = Runner.run_streamed(agent, "Tell me a story")

# Stream events
async for event in result.stream():
    if event.type == "text":
        print(event.content, end="")
```

### With Configuration
```python
from agents import Agent, Runner, RunConfig

agent = Agent(name="Assistant", instructions="You are a helpful assistant.")

config = RunConfig(
    model="gpt-4",
    max_turns=10,
    workflow_name="Customer Support",
    trace_id="trace_abc123",
    tracing_disabled=False,
    trace_include_sensitive_data=False
)

result = await Runner.run(
    agent,
    "Help me with my order",
    run_config=config,
    max_turns=5  # This overrides the config's max_turns
)
```

### With Session Memory
```python
from agents import Agent, Runner
from agents.memory import SQLiteSession

# Create a persistent session
session = SQLiteSession(
    session_id="user_123",
    db_path="conversations.db"
)

agent = Agent(name="Assistant", instructions="You are a helpful assistant.")

# First conversation
result1 = await Runner.run(agent, "My name is Alice", session=session)

# Second conversation - agent remembers previous context
result2 = await Runner.run(agent, "What's my name?", session=session)
# Agent should respond with "Alice"
```

### With Hooks
```python
from agents import Agent, Runner, RunHooks

class MyHooks(RunHooks):
    async def on_agent_start(self, context, agent):
        print(f"Starting: {agent.name}")
    
    async def on_agent_end(self, context, agent, output):
        print(f"Finished: {agent.name}")

agent = Agent(name="Assistant", instructions="You are a helpful assistant.")

result = await Runner.run(
    agent,
    "Hello",
    hooks=MyHooks()
)
```