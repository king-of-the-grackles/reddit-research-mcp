# Function Schema Reference

## Classes

### FuncSchema

Captures the schema for a Python function, in preparation for sending it to an LLM as a tool.

```python
@dataclass
class FuncSchema:
    name: str
    """The name of the function."""
    
    description: str | None
    """The description of the function."""
    
    params_pydantic_model: type[BaseModel]
    """A Pydantic model that represents the function's parameters."""
    
    params_json_schema: dict[str, Any]
    """The JSON schema for the function's parameters, derived from the Pydantic model."""
    
    signature: inspect.Signature
    """The signature of the function."""
    
    takes_context: bool = False
    """Whether the function takes a RunContextWrapper argument (must be the first argument)."""
    
    strict_json_schema: bool = True
    """Whether the JSON schema is in strict mode. We strongly recommend setting this to True."""
    
    def to_call_args(self, data: BaseModel) -> tuple[list[Any], dict[str, Any]]:
        """
        Converts validated data from the Pydantic model into (args, kwargs), 
        suitable for calling the original function.
        """
```

### FuncDocumentation

Contains metadata about a Python function, extracted from its docstring.

```python
@dataclass
class FuncDocumentation:
    name: str
    """The name of the function, via `__name__`."""
    
    description: str | None
    """The description of the function, derived from the docstring."""
    
    param_descriptions: dict[str, str] | None
    """The parameter descriptions of the function, derived from the docstring."""
```

## Functions

### generate_func_documentation

Extracts metadata from a function docstring, in preparation for sending it to an LLM as a tool.

```python
def generate_func_documentation(
    func: Callable[..., Any], 
    style: DocstringStyle | None = None
) -> FuncDocumentation:
    """
    Extracts metadata from a function docstring.
    
    Args:
        func: The function to extract documentation from.
        style: The style of the docstring to use for parsing. 
               If not provided, we will attempt to auto-detect the style.
    
    Returns:
        A FuncDocumentation object containing the function's name, description, 
        and parameter descriptions.
    """
```

### function_schema

Given a Python function, extracts a `FuncSchema` from it, capturing the name, description, parameter descriptions, and other metadata.

```python
def function_schema(
    func: Callable[..., Any],
    docstring_style: DocstringStyle | None = None,
    name_override: str | None = None,
    description_override: str | None = None,
    use_docstring_info: bool = True,
    strict_json_schema: bool = True,
) -> FuncSchema:
    """
    Given a Python function, extracts a `FuncSchema` from it.
    
    Args:
        func: The function to extract the schema from.
        docstring_style: The style of the docstring to use for parsing. 
                        If not provided, we will attempt to auto-detect the style.
        name_override: If provided, use this name instead of the function's `__name__`.
        description_override: If provided, use this description instead of the one 
                            derived from the docstring.
        use_docstring_info: If True, uses the docstring to generate the description 
                          and parameter descriptions.
        strict_json_schema: Whether the JSON schema is in strict mode. If True, we'll 
                          ensure that the schema adheres to the "strict" standard the 
                          OpenAI API expects. We strongly recommend setting this to True.
    
    Returns:
        A `FuncSchema` object containing the function's name, description, 
        parameter descriptions, and other metadata.
    """
```

## How It Works

The function schema extraction works through the following steps:

1. **Docstring Parsing**: If `use_docstring_info` is True, the function's docstring is parsed to extract:
   - Function description
   - Parameter descriptions
   - Supports multiple docstring formats (Google, Sphinx, NumPy)

2. **Signature Inspection**: The function's signature is analyzed to:
   - Identify parameter names, types, and defaults
   - Detect if the function takes a `RunContextWrapper` or `ToolContext` as the first argument
   - Handle special parameter types (*args, **kwargs)

3. **Type Processing**: Type hints are evaluated and processed:
   - Missing type hints default to `Any`
   - Variadic arguments (*args) are converted to lists
   - Keyword arguments (**kwargs) are converted to dictionaries

4. **Pydantic Model Generation**: A dynamic Pydantic model is created representing the function's parameters:
   - Required parameters (no default value)
   - Optional parameters (with default values)
   - Field descriptions from docstrings

5. **JSON Schema Creation**: The Pydantic model is converted to a JSON schema:
   - Optionally applies strict mode for better LLM compatibility
   - Ensures schema adheres to OpenAI's requirements

## Example Usage

```python
from agents.function_schema import function_schema

def calculate_area(
    length: float, 
    width: float, 
    unit: str = "meters"
) -> float:
    """
    Calculate the area of a rectangle.
    
    Args:
        length: The length of the rectangle.
        width: The width of the rectangle.
        unit: The unit of measurement (default: meters).
    
    Returns:
        The area of the rectangle.
    """
    return length * width

# Extract schema
schema = function_schema(calculate_area)

print(schema.name)  # "calculate_area"
print(schema.description)  # "Calculate the area of a rectangle."
print(schema.params_json_schema)  # JSON schema for the parameters
```

## Special Parameters

### Context Parameters

If the first parameter of a function is typed as `RunContextWrapper` or `ToolContext`, it will be automatically handled:

```python
from agents import RunContextWrapper

def my_tool(ctx: RunContextWrapper[MyContext], query: str) -> str:
    # ctx is automatically provided by the framework
    # query comes from the LLM
    return f"Processing {query} for user {ctx.context.user}"
```

### Variadic Parameters

The schema extraction handles *args and **kwargs:

```python
def flexible_function(*items: str, **options: bool):
    # *items becomes a list[str] in the schema
    # **options becomes a dict[str, bool] in the schema
    pass
```