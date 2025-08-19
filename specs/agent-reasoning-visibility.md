# Deep Agent Reasoning Visibility with Streaming

## Understanding the Goal
You want to see the actual LLM reasoning process (thinking tokens) for each agent, streamed in real-time to debug logs, similar to how you see UV's debug output.

## Proposed Implementation

### 1. Enable OpenAI Agents SDK Streaming & Tracing
```python
from agents import Runner, RunConfig
from agents.streaming import StreamingRunResult
import logging

# Configure logging for agent traces
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('reddit_research_agent')

async def execute_reddit_research(query: str):
    # Enable tracing and streaming
    run_config = RunConfig(
        model="gpt-4",
        trace_metadata={"query": query},
        workflow_name="reddit_research",
        # Enable detailed tracing
        trace_include_sensitive_data=True,
    )
    
    # Use streaming runner for real-time output
    logger.debug(f"🎯 ORCHESTRATOR starting for query: {query}")
    
    # Stream orchestrator reasoning
    orchestrator_stream = await Runner.run_streamed(
        orchestrator, 
        query,
        run_config=run_config
    )
    
    # Process streaming events
    async for event in orchestrator_stream.stream_events():
        if event.type == "reasoning":
            logger.debug(f"[ORCHESTRATOR THINKING] {event.content}")
        elif event.type == "tool_call":
            logger.debug(f"[ORCHESTRATOR ACTION] Calling: {event.tool_name}")
    
    search_plan = orchestrator_stream.final_output_as(SearchTaskPlan)
```

### 2. Add Custom Context Wrapper for Reasoning Capture
```python
class ReasoningCapture:
    """Capture and log agent reasoning in real-time"""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.logger = logging.getLogger(f'agent.{agent_name}')
    
    async def wrap_agent_run(self, agent, input_data, context=None):
        self.logger.debug(f"[{self.agent_name}] Starting with input: {input_data[:100]}...")
        
        # Run with streaming to capture reasoning
        result = await Runner.run_streamed(agent, input_data, context=context)
        
        reasoning_tokens = []
        async for event in result.stream_events():
            if event.type in ["reasoning", "thinking"]:
                reasoning_tokens.append(event.content)
                self.logger.debug(f"[{self.agent_name} REASONING] {event.content}")
            elif event.type == "output":
                self.logger.debug(f"[{self.agent_name} OUTPUT] {event.content[:200]}...")
        
        # Log summary
        self.logger.info(f"[{self.agent_name}] Complete. Reasoning tokens: {len(reasoning_tokens)}")
        
        return result
```

### 3. Environment Variable for Debug Mode
```python
import os

# Add debug mode toggle
DEBUG_AGENTS = os.getenv("DEBUG_AGENTS", "false").lower() == "true"
STREAM_REASONING = os.getenv("STREAM_REASONING", "false").lower() == "true"

async def get_reddit_instance(debug=False):
    # Only show auth debug if DEBUG_AGENTS is enabled
    if debug and DEBUG_AGENTS:
        print(f"🔐 Reddit Auth Debug:...")
```

### 4. Run Script with Debug Flags
```bash
# In the script header, add environment variable support
#!/usr/bin/env -S DEBUG_AGENTS=true STREAM_REASONING=true uv run --verbose --script

# Or run with:
DEBUG_AGENTS=true STREAM_REASONING=true uv run --verbose reddit_research_agent.py
```

### 5. Structured Logging Output
```python
# Configure different log levels for different components
logging.getLogger('agent.orchestrator').setLevel(logging.DEBUG)
logging.getLogger('agent.search_worker').setLevel(logging.INFO)
logging.getLogger('agent.discovery_worker').setLevel(logging.INFO)
logging.getLogger('agent.validation_worker').setLevel(logging.INFO)
logging.getLogger('agent.synthesizer').setLevel(logging.DEBUG)
logging.getLogger('asyncpraw').setLevel(logging.WARNING)  # Reduce Reddit noise
```

### 6. Custom Debug Output Format
```python
class AgentDebugFormatter(logging.Formatter):
    """Custom formatter for agent debug output"""
    
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'REASONING': '\033[35m', # Magenta
    }
    RESET = '\033[0m'
    
    def format(self, record):
        # Add colors for terminal output
        if hasattr(record, 'reasoning'):
            color = self.COLORS.get('REASONING', '')
            record.msg = f"{color}[THINKING] {record.msg}{self.RESET}"
        
        return super().format(record)

# Apply formatter
handler = logging.StreamHandler()
handler.setFormatter(AgentDebugFormatter(
    '%(asctime)s | %(name)s | %(message)s'
))
logging.root.addHandler(handler)
```

## Expected Output with Deep Visibility:
```
$ DEBUG_AGENTS=true STREAM_REASONING=true uv run --verbose reddit_research_agent.py

2024-01-15 10:23:45 | agent.orchestrator | [ORCHESTRATOR THINKING] The user is asking about Trump and Putin in Alaska. I need to identify:
2024-01-15 10:23:45 | agent.orchestrator | [ORCHESTRATOR THINKING] 1. Core entities: Trump (person), Putin (person), Alaska (location)
2024-01-15 10:23:46 | agent.orchestrator | [ORCHESTRATOR THINKING] 2. These are political figures, so political subreddits would be relevant
2024-01-15 10:23:46 | agent.orchestrator | [ORCHESTRATOR THINKING] 3. For direct searches, I'll use single terms like "trump", "putin", "alaska"
2024-01-15 10:23:47 | agent.orchestrator | [ORCHESTRATOR OUTPUT] SearchTaskPlan(direct_searches=['trump', 'putin', 'alaska'], ...)

2024-01-15 10:23:48 | agent.search_worker | [SEARCH_WORKER THINKING] I received terms: trump, putin, alaska
2024-01-15 10:23:48 | agent.search_worker | [SEARCH_WORKER THINKING] These are potential subreddit names. I'll search each one.
2024-01-15 10:23:49 | agent.search_worker | [SEARCH_WORKER ACTION] Calling search_subreddits_tool(query='trump')
2024-01-15 10:23:50 | reddit.api | Searching for communities matching: 'trump'
2024-01-15 10:23:51 | reddit.api | Found 24 communities
```

## Benefits:
1. **Real thinking tokens**: See actual LLM reasoning, not just formatted output
2. **Streaming visibility**: Watch agents think in real-time
3. **Debug control**: Toggle verbosity with environment variables
4. **Performance metrics**: Track reasoning token usage per agent
5. **Structured logs**: Filter by agent or log level
6. **UV integration**: Works alongside UV's --verbose flag

## Alternative: OpenAI Tracing Dashboard
The OpenAI Agents SDK also supports sending traces to their dashboard:
```python
# Traces will appear at https://platform.openai.com/traces
run_config = RunConfig(
    workflow_name="reddit_research",
    trace_id=f"reddit_{timestamp}",
    trace_metadata={"query": query, "version": "1.0"}
)
```

This gives you a web UI to explore agent reasoning after execution.

## Implementation Priority
1. Start with environment variable debug flags (easiest)
2. Add structured logging with custom formatter
3. Implement streaming for orchestrator and synthesizer (most valuable)
4. Add streaming for worker agents if needed
5. Consider OpenAI dashboard for production monitoring