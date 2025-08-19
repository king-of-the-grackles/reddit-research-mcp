# Guardrails Reference

## GuardrailFunctionOutput (dataclass)

The output of a guardrail function.

### Attributes

#### output_info (instance-attribute)
```python
output_info: Any
```
Optional information about the guardrail's output. For example, the guardrail could include information about the checks it performed and granular results.

#### tripwire_triggered (instance-attribute)
```python
tripwire_triggered: bool
```
Whether the tripwire was triggered. If triggered, the agent's execution will be halted.

## InputGuardrailResult (dataclass)

The result of a guardrail run.

### Attributes

#### guardrail (instance-attribute)
```python
guardrail: InputGuardrail[Any]
```
The guardrail that was run.

#### output (instance-attribute)
```python
output: GuardrailFunctionOutput
```
The output of the guardrail function.

## OutputGuardrailResult (dataclass)

The result of a guardrail run.

### Attributes

#### guardrail (instance-attribute)
```python
guardrail: OutputGuardrail[Any]
```
The guardrail that was run.

#### agent_output (instance-attribute)
```python
agent_output: Any
```
The output of the agent that was checked by the guardrail.

#### agent (instance-attribute)
```python
agent: Agent[Any]
```
The agent that was checked by the guardrail.

#### output (instance-attribute)
```python
output: GuardrailFunctionOutput
```
The output of the guardrail function.

## InputGuardrail (dataclass)

Bases: `Generic[TContext]`

Input guardrails are checks that run in parallel to the agent's execution. They can be used to do things like:
- Check if input messages are off-topic
- Take over control of the agent's execution if an unexpected input is detected

You can use the `@input_guardrail()` decorator to turn a function into an `InputGuardrail`, or create an `InputGuardrail` manually.

Guardrails return a `GuardrailResult`. If `result.tripwire_triggered` is `True`, the agent's execution will immediately stop, and an `InputGuardrailTripwireTriggered` exception will be raised.

### Attributes

#### guardrail_function (instance-attribute)
```python
guardrail_function: Callable[
    [RunContextWrapper[TContext], Agent[Any], str | list[TResponseInputItem]],
    MaybeAwaitable[GuardrailFunctionOutput],
]
```
A function that receives the agent input and the context, and returns a `GuardrailResult`. The result marks whether the tripwire was triggered, and can optionally include information about the guardrail's output.

#### name (class-attribute, instance-attribute)
```python
name: str | None = None
```
The name of the guardrail, used for tracing. If not provided, we'll use the guardrail function's name.

### Methods

#### get_name()
Returns the name of the guardrail.

#### run(async)
Runs the guardrail function with the provided agent, input, and context.

## OutputGuardrail (dataclass)

Bases: `Generic[TContext]`

Output guardrails are checks that run on the final output of an agent. They can be used to check if the output passes certain validation criteria.

You can use the `@output_guardrail()` decorator to turn a function into an `OutputGuardrail`, or create an `OutputGuardrail` manually.

Guardrails return a `GuardrailResult`. If `result.tripwire_triggered` is `True`, an `OutputGuardrailTripwireTriggered` exception will be raised.

### Attributes

#### guardrail_function (instance-attribute)
```python
guardrail_function: Callable[
    [RunContextWrapper[TContext], Agent[Any], Any],
    MaybeAwaitable[GuardrailFunctionOutput],
]
```
A function that receives the final agent, its output, and the context, and returns a `GuardrailResult`. The result marks whether the tripwire was triggered, and can optionally include information about the guardrail's output.

#### name (class-attribute, instance-attribute)
```python
name: str | None = None
```
The name of the guardrail, used for tracing. If not provided, we'll use the guardrail function's name.

### Methods

#### get_name()
Returns the name of the guardrail.

#### run(async)
Runs the guardrail function with the provided context, agent, and agent output.

## Decorators

### input_guardrail

```python
input_guardrail(
    func: _InputGuardrailFuncSync[TContext_co] | _InputGuardrailFuncAsync[TContext_co] | None = None,
    *,
    name: str | None = None,
) -> InputGuardrail[TContext_co] | Callable[...]
```

Decorator that transforms a sync or async function into an `InputGuardrail`. It can be used directly (no parentheses) or with keyword args, e.g.:

```python
@input_guardrail
def my_sync_guardrail(...): ...

@input_guardrail(name="guardrail_name")
async def my_async_guardrail(...): ...
```

### output_guardrail

```python
output_guardrail(
    func: _OutputGuardrailFuncSync[TContext_co] | _OutputGuardrailFuncAsync[TContext_co] | None = None,
    *,
    name: str | None = None,
) -> OutputGuardrail[TContext_co] | Callable[...]
```

Decorator that transforms a sync or async function into an `OutputGuardrail`. It can be used directly (no parentheses) or with keyword args, e.g.:

```python
@output_guardrail
def my_sync_guardrail(...): ...

@output_guardrail(name="guardrail_name")
async def my_async_guardrail(...): ...
```