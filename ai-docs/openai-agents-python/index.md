# OpenAI Agents Python Documentation

This directory contains the complete documentation for the OpenAI Agents Python SDK, scraped and organized for offline reference.

## Quick Start

- [**Quickstart Guide**](quickstart/quickstart.md) - Get started with the Agents SDK in minutes

## Core Concepts

- [**Agents**](core/agents.md) - The core building block - LLMs configured with instructions and tools
- [**Tools**](tools/tools.md) - Enable agents to take actions: fetch data, run code, call APIs
- [**Running Agents**](core/running_agents.md) - Execute agents with Runner class and handle results
- [**Configuration**](core/config.md) - Set up API keys, clients, tracing, and logging
- [**Models**](core/models.md) - Use OpenAI and non-OpenAI models with the SDK
- [**Context Management**](core/context.md) - Manage local and LLM context for your agents

## Advanced Topics

- [**Streaming**](advanced/streaming.md) - Subscribe to real-time updates during agent execution
- [**Sessions**](advanced/sessions.md) - Built-in conversation history management
- [**Model Context Protocol (MCP)**](advanced/mcp.md) - Standardized way to provide tools and context
- [**Results**](advanced/results.md) - Understanding and working with agent run results

## Reference

- [**Agent Reference**](reference/agent.md) - Complete Agent class API reference
- [**Tool Reference**](reference/tool.md) - All tool types and function tool creation
- [**Function Schema**](reference/function_schema.md) - How functions are converted to tool schemas
- [**Exceptions**](reference/exceptions.md) - Error handling and exception types

## Directory Structure

```
openai-agents-python/
├── index.md                    # This file
├── quickstart/
│   └── quickstart.md           # Getting started guide
├── core/
│   ├── agents.md               # Agent configuration and usage
│   ├── tools.md                # Tools documentation
│   ├── running_agents.md       # Running agents with Runner
│   ├── config.md               # SDK configuration
│   ├── models.md               # Model providers and configuration
│   └── context.md              # Context management
├── tools/
│   └── tools.md                # Detailed tools documentation
├── advanced/
│   ├── streaming.md            # Streaming responses
│   ├── sessions.md             # Conversation memory
│   ├── mcp.md                  # Model Context Protocol
│   └── results.md              # Working with results
└── reference/
    ├── agent.md                # Agent API reference
    ├── tool.md                 # Tool API reference
    ├── function_schema.md      # Function schema reference
    └── exceptions.md           # Exception reference
```

## Key Features

### 🤖 Agents
- Configure LLMs with instructions, tools, and guardrails
- Support for structured outputs with Pydantic models
- Dynamic instructions and lifecycle hooks
- Agent cloning and composition

### 🛠️ Tools
- **Hosted tools**: Web search, file search, computer use, code interpreter
- **Function tools**: Use any Python function as a tool
- **Agents as tools**: Orchestrate multiple specialized agents
- **MCP servers**: Integrate with Model Context Protocol servers

### 🔄 Handoffs
- Seamlessly transfer control between specialized agents
- Build complex multi-agent workflows
- Maintain context across agent transitions

### 🛡️ Guardrails
- Input validation before processing
- Output validation before delivery
- Custom guardrail functions
- Tripwire mechanisms for blocking unsafe content

### 💾 Sessions
- Automatic conversation history management
- SQLite-based persistence
- Custom session implementations
- Multi-session support

### 🌊 Streaming
- Real-time token streaming
- Progress updates during execution
- Event-based architecture

### 🔌 Model Support
- OpenAI models (Responses API and Chat Completions)
- Non-OpenAI models via LiteLLM
- Custom model providers
- Mix and match models in workflows

## Getting Started

1. **Installation**:
   ```bash
   pip install openai-agents
   ```

2. **Set API Key**:
   ```bash
   export OPENAI_API_KEY=sk-...
   ```

3. **Create Your First Agent**:
   ```python
   from agents import Agent, Runner
   
   agent = Agent(
       name="Assistant",
       instructions="You are a helpful assistant"
   )
   
   result = await Runner.run(agent, "Hello!")
   print(result.final_output)
   ```

## Learn More

- [Official GitHub Repository](https://github.com/openai/openai-agents-python)
- [OpenAI Platform Documentation](https://platform.openai.com/docs)
- [Model Context Protocol](https://modelcontextprotocol.io)

## Notes

This documentation was scraped from the official OpenAI Agents Python documentation for offline reference. For the most up-to-date information, please refer to the [official documentation](https://openai.github.io/openai-agents-python/).