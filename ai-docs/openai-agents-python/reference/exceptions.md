# Exceptions Reference

## Overview

The SDK raises exceptions in certain cases. All exceptions inherit from [`AgentsException`](#agentsexception), which is the base class for all exceptions raised within the SDK.

## Exception Hierarchy

```
AgentsException (base)
├── MaxTurnsExceeded
├── ModelBehaviorError
├── UserError
├── InputGuardrailTripwireTriggered
└── OutputGuardrailTripwireTriggered
```

## Exception Classes

### AgentsException

Base class for all exceptions in the Agents SDK.

```python
class AgentsException(Exception):
    """Base class for all exceptions in the Agents SDK."""
    run_data: RunErrorDetails | None
```

This is the base class from which all other specific exceptions are derived. It may contain `run_data` with details about the agent run when the exception occurred.

### MaxTurnsExceeded

Exception raised when the agent's run exceeds the `max_turns` limit.

```python
class MaxTurnsExceeded(AgentsException):
    """Exception raised when the maximum number of turns is exceeded."""
    message: str
```

This indicates that the agent could not complete its task within the specified number of interaction turns.

**Example:**
```python
try:
    result = await Runner.run(agent, input, max_turns=5)
except MaxTurnsExceeded as e:
    print(f"Agent exceeded turn limit: {e.message}")
    # Access run data if needed
    if e.run_data:
        print(f"Last agent: {e.run_data.last_agent.name}")
```

### ModelBehaviorError

Exception raised when the model produces unexpected or invalid outputs.

```python
class ModelBehaviorError(AgentsException):
    """Exception raised when the model does something unexpected."""
    message: str
```

This can include:
- Malformed JSON when the model provides invalid JSON for tool calls or structured outputs
- Calling a tool that doesn't exist
- Unexpected tool-related failures
- Invalid output when an `output_type` is defined

**Example:**
```python
try:
    result = await Runner.run(agent, input)
except ModelBehaviorError as e:
    print(f"Model produced invalid output: {e.message}")
```

### UserError

Exception raised when there's an error in how the SDK is being used.

```python
class UserError(AgentsException):
    """Exception raised when the user makes an error using the SDK."""
    message: str
```

This typically results from:
- Incorrect code implementation
- Invalid configuration
- Misuse of the SDK's API
- Type mismatches in context or tool functions

**Example:**
```python
try:
    # Invalid agent configuration
    agent = Agent(
        name=123,  # Should be a string
        instructions="Help the user"
    )
except UserError as e:
    print(f"Configuration error: {e.message}")
```

### InputGuardrailTripwireTriggered

Exception raised when an input guardrail's conditions are met.

```python
class InputGuardrailTripwireTriggered(AgentsException):
    """Exception raised when a guardrail tripwire is triggered."""
    guardrail_result: InputGuardrailResult
```

Input guardrails check incoming messages before processing. When a tripwire is triggered, processing stops.

**Example:**
```python
from agents import Agent, InputGuardrail, GuardrailFunctionOutput

async def content_filter(ctx, agent, input_data):
    if "blocked_word" in input_data:
        return GuardrailFunctionOutput(
            output_info={"reason": "Blocked content detected"},
            tripwire_triggered=True
        )
    return GuardrailFunctionOutput(
        output_info={},
        tripwire_triggered=False
    )

agent = Agent(
    name="Safe Agent",
    instructions="Help the user",
    input_guardrails=[
        InputGuardrail(guardrail_function=content_filter)
    ]
)

try:
    result = await Runner.run(agent, "message with blocked_word")
except InputGuardrailTripwireTriggered as e:
    print(f"Input blocked: {e.guardrail_result}")
```

### OutputGuardrailTripwireTriggered

Exception raised when an output guardrail's conditions are met.

```python
class OutputGuardrailTripwireTriggered(AgentsException):
    """Exception raised when a guardrail tripwire is triggered."""
    guardrail_result: OutputGuardrailResult
```

Output guardrails check the agent's final response before delivery. When a tripwire is triggered, the response is blocked.

**Example:**
```python
from agents import Agent, OutputGuardrail, GuardrailFunctionOutput

async def quality_check(ctx, agent, output_data):
    if len(output_data) < 10:
        return GuardrailFunctionOutput(
            output_info={"reason": "Response too short"},
            tripwire_triggered=True
        )
    return GuardrailFunctionOutput(
        output_info={},
        tripwire_triggered=False
    )

agent = Agent(
    name="Quality Agent",
    instructions="Provide detailed responses",
    output_guardrails=[
        OutputGuardrail(guardrail_function=quality_check)
    ]
)

try:
    result = await Runner.run(agent, "Hi")
except OutputGuardrailTripwireTriggered as e:
    print(f"Output blocked: {e.guardrail_result}")
```

## RunErrorDetails

When an exception occurs, it may contain `run_data` with details about the agent run:

```python
@dataclass
class RunErrorDetails:
    """Data collected from an agent run when an exception occurs."""
    input: str | list[TResponseInputItem]
    new_items: list[RunItem]
    raw_responses: list[ModelResponse]
    last_agent: Agent[Any]
    context_wrapper: RunContextWrapper[Any]
    input_guardrail_results: list[InputGuardrailResult]
    output_guardrail_results: list[OutputGuardrailResult]
```

This provides comprehensive information about the state of the run when the exception occurred:

```python
try:
    result = await Runner.run(agent, input)
except AgentsException as e:
    if e.run_data:
        print(f"Input: {e.run_data.input}")
        print(f"Last agent: {e.run_data.last_agent.name}")
        print(f"Items generated: {len(e.run_data.new_items)}")
        for item in e.run_data.new_items:
            print(f"  - {item.type}")
```

## Best Practices

1. **Catch specific exceptions**: Handle specific exceptions when you need different behavior for different error types.

2. **Use run_data**: Access `run_data` when available to understand what happened during the failed run.

3. **Retry logic**: For `ModelBehaviorError`, consider implementing retry logic as these errors may be transient.

4. **Guardrail handling**: Handle guardrail exceptions gracefully to provide user feedback about why their request was blocked.

5. **Logging**: Log exception details for debugging and monitoring purposes.

```python
import logging

logger = logging.getLogger(__name__)

async def safe_run(agent, input):
    try:
        return await Runner.run(agent, input)
    except MaxTurnsExceeded as e:
        logger.warning(f"Max turns exceeded: {e.message}")
        # Maybe try with higher max_turns
        return await Runner.run(agent, input, max_turns=20)
    except ModelBehaviorError as e:
        logger.error(f"Model error: {e.message}")
        # Maybe retry with different model settings
        raise
    except InputGuardrailTripwireTriggered as e:
        logger.info(f"Input blocked by guardrail")
        return {"error": "Input not allowed", "reason": e.guardrail_result}
    except UserError as e:
        logger.error(f"Configuration error: {e.message}")
        raise
```