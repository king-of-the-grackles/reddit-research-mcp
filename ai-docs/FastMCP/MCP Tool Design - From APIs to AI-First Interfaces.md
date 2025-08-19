# MCP Tool Design - From APIs to AI-First Interfaces

**Author**: Sjoerd Tiemensma  
**Source**: [Use AI Substack](https://useai.substack.com/p/mcp-tool-design-from-apis-to-ai-first)  
**Date**: July 01, 2025  
**Tags**: #MCP #AI #ToolDesign #API #ModelContextProtocol

---

> Why MCPs aren't just APIs with descriptions, and how you should design them instead

After spending months building and refining MCP (Model Context Protocol) servers for various use cases, I've learned that the difference between a tool that technically works and one that AI models can actually use effectively comes down to design decisions that might seem trivial at first glance.

With LLM it's an incredibly common theme that it's easy to get AI to work at a demo level. Think coding projects, prompting in general, agentic systems, RAG, etc. Tool design in MCP's is no different. By adjusting your approach to the strength and weaknesses of the AI system you can squeeze out that last 20%. That's what this article will be going over, with a practical example added in around community management.

## Why MCPs Aren't Just APIs with Descriptions

Here's a mistake I see constantly: taking an existing API, slapping some descriptions on it, and calling it an MCP server. This is the approach of most MCP servers found on websites like Glama or Smithery. This approach leads to mediocre results at best, and complete failure at worst.

The fundamental difference? APIs are designed for developers who can take their time to understand a system, read documentation, and carefully implement specific workflows. MCPs are used by AI models that need to instantly understand what tools to use and how to chain them together based on natural language requests.

### Why AI Models Are Different

Modern LLMs have impressive general knowledge - they can write code, explain complex topics, and reason through problems. But they have critical limitations when it comes to using APIs:

**No persistent learning**: When a developer encounters an unfamiliar API, they read docs, experiment, and build mental models that persist. Each interaction builds on the last. For an AI model, every conversation starts from scratch. It can't "remember" how on a platform, different terms like "spaces", "groups", "community" and "topics" relate to one another.

**Limited exploration**: Code can systematically try different endpoints, parse error messages, and adapt. Developers can browse documentation, check examples, and search Stack Overflow. AI models only have what you provide in that moment - if the tool description doesn't explain it, it doesn't exist. It can try a few things, but that's both costly and unreliable.

**Context, not comprehension**: While LLMs can process information, they don't truly "understand" systems the way developers do. They pattern-match based on their training and your descriptions. If your tool descriptions use ambiguous terms or assume external knowledge, the model is essentially guessing.

This is why a developer can work with minimal API descriptions - they'll figure out the rest and have access to a large amount of context. But for AI models, every single interaction must be self-contained and crystal clear. The model can't learn from its mistakes across sessions or gradually build understanding. It needs to get it right based solely on what you provide right now.

### Token Explosion and Conceptual Confusion

Converting an API directly leads to two immediate problems:

**Token explosion**: Each tool needs a JSON schema (50-100 tokens), a meaningful description (100-200 tokens), and parameter descriptions (20-50 tokens each). A typical API with 80 endpoints would consume ~24,000 tokens just for tool definitions - before the AI even starts working!

**Conceptual confusion**: APIs use technical terms that make sense to developers but confuse AI models. What's the difference between a "resource", "entity", and "object"? When should you use `community_members` vs `space_members`? The AI has no context for these distinctions.

## The General Approach: Think Like a Model, Not a Developer

When I first started building MCP tools, I made the classic developer mistake: I designed them the way I would want to use them. Clean, modular, following all the best practices of API design. The problem? AI models don't think like developers.

Here's what actually matters:

**Start with user intent, not API operations** - This is THE fundamental shift. Tools should represent what users want to accomplish, not how your system is structured internally.

**Every response guides the next action** - Since models operate statelessly, each response must not just report what happened but suggest what to do next. This encompasses error handling, success responses, and general feedback.

**Balance context with efficiency** - This addresses both the need to explain domain concepts (since models can't read docs) and the practical reality of token limits. It ties into smart consolidation, pagination, and knowing what to include in descriptions.

## Writing Tool Descriptions: The Art of Guided Discovery

Here's a counterintuitive truth: the best tool descriptions aren't always the most detailed ones. After months of iteration, I've learned that the most effective approach combines structured descriptions with intelligent error handling that guides models toward correct usage.

### The XML Structure That Works

I've found that using XML tags to structure descriptions provides clarity without overwhelming the model. Instead of a wall of text, break it into two clear sections:

- `<usecase>` tells the model WHAT the tool does and WHEN to use it
- `<instructions>` covers HOW to use it correctly

This separation helps models quickly understand if a tool is relevant before diving into the details.

### The 90/10 Rule: When Less Description is More

Here's where I disagree with conventional wisdom: you don't always need exhaustive descriptions. If your error handling can guide the model to correct usage 90% of the time, lean on that instead of bloating your descriptions.

For example, instead of listing every possible field and format requirement upfront, provide the essentials and let your error messages teach the edge cases. If a model forgets to include an ID for an update operation, a helpful error like "No ID provided for update. Use searchRecords() to find record IDs" is more effective than a paragraph of preemptive instructions.

### Every Response is a Prompt Injection Opportunity

This philosophy extends beyond error handling. Every single response - success or failure - is a chance to guide the model's next action. When returning search results, don't just return the data. Add a message like "Found 5 results. Use getDetails() for full information on any result." This gentle guidance helps models understand the natural flow of operations.

## Error Handling That Actually Helps

The worst error message is one that doesn't help the model correct its behavior. Structure your errors to include:

- **What went wrong** (clear, specific)
- **Why it went wrong** (brief context)
- **What to do instead** (actionable suggestion)
- **Example of correct usage** (when helpful)

## Consolidation Strategy: Finding the Sweet Spot

When converting APIs to MCPs, resist the urge to either:

1. Create one tool per API endpoint (too granular)
2. Create one mega-tool that does everything (too complex and risky)

Instead, consolidate based on user intent. Group operations that serve a common purpose, but keep distinct concepts separate. Self-evident operations (like sending a simple message) can stay standalone - not everything needs consolidation.

There is another challenge, and that's around potentially destructive or "risky" calls. Take a notes MCP, when creating or updating notes, you might have "note", "tags" and "source" parameters. Instead of explaining each parameter for different tools, where each does something different (create, read, update or delete), you could put all the operations in one single tool with an "action" parameter that determines whether you're creating, reading, updating or deleting a note.

However, you might want to separate the delete and update tool to prevent costly mistakes. What if the model misinterprets a request? It's becoming more common that you give the model free reigns to use certain tools (take read and create) while requiring approval for others (update and delete). That way, you give up some token savings, while staying in control.

## A Real-World Example: Circle.so Community Platform

Having an AI assistant help with community management - automatically welcoming new members, identifying engaged users, or moderating content - could save hours of repetitive work. Let's see how to transform Circle's 80-endpoint API into effective MCP tools.

### The Challenge of Dynamic Tool Usage

Imagine a user asks their AI assistant:

_"Can you find the most active members in our JavaScript community who haven't attended any of our recent workshops?"_

With a direct API conversion, the model would face a maze of decisions. In Circle, communities have "spaces" (topic areas), "space groups" (collections of spaces), members with different activity types, and events that might be workshops, meetups, or Q&As.

Using the raw API, the model would need to chain 7-8 different calls:

- Search for the "JavaScript" space
- Get all members of that space
- Check each member's activity individually
- Find all events in the space
- Check which events are workshops
- Get attendance for each workshop
- Cross-reference everything manually

A developer would read Circle's documentation to understand these relationships. But the AI only has your tool descriptions.

### The MCP Way: Natural Tool Chaining

Instead of 80 granular endpoints, we can create ~12 intent-based tools that work together naturally. Here's how that same query would work:

**Step 1: Find the right space**

The model uses a `findSpaces` tool that searches by name or topic. Here's what this tool looks like:

```javascript
{
  name: "findSpaces",
  description: `<usecase>
  Searches for spaces by name or topic. Returns matching spaces with basic info.
  </usecase>

  <instructions>
  Partial matches work (e.g., "java" matches "JavaScript")
  Returns up to 10 matches ordered by member count
  </instructions>`,

  inputSchema: {
    type: "object",
    properties: {
      query: {
        type: "string",
        description: "Search term for space name or topic"
      }
    },
    required: ["query"]
  }
}
```

When called with `{ query: "javascript" }`, it returns:

```javascript
{
  spaces: [
    { id: "space_123", name: "JavaScript", memberCount: 1240 },
    { id: "space_456", name: "Java Development", memberCount: 890 }
  ],
  message: "Found 2 spaces matching 'javascript'. Use the space ID with getSpaceActivity()."
}
```

**Step 2: Get member activity**

The `getSpaceActivity` tool returns members with structured activity data:

```javascript
{
  name: "getSpaceActivity",
  description: `<usecase>
  Retrieves member activity summary for a space including posts, comments, and events attended.
  Perfect for identifying active members and understanding participation patterns.
  </usecase>

  <instructions>
  Returns members sorted by total activity
  Includes last 30 days by default
  </instructions>`,

  inputSchema: {
    type: "object",
    properties: {
      spaceId: {
        type: "string",
        description: "Space ID from findSpaces"
      },
      period: {
        type: "string",
        description: "Time period like '7d', '30d', '90d'",
        default: "30d"
      }
    },
    required: ["spaceId"]
  }
}
```

The response includes everything needed for the next step:

```javascript
{
  members: [
    {
      id: "user_789",
      name: "Alice Chen",
      posts: 5,
      comments: 23,
      eventsAttended: ["event_101", "event_102"],
      lastActive: "2024-01-25"
    },
    {
      id: "user_790",
      name: "Bob Smith",
      posts: 12,
      comments: 45,
      eventsAttended: [],  // Haven't attended any events
      lastActive: "2024-01-24"
    }
  ],
  totalMembers: 47,
  message: "Showing members with any activity. Use getSpaceEvents() to identify which events were workshops."
}
```

**Step 3: Identify workshops**

The final tool filters events by type and guides the completion:

```javascript
{
  events: [
    { id: "event_101", title: "Intro to React Hooks", type: "workshop", date: "2024-01-10" },
    { id: "event_103", title: "Advanced TypeScript", type: "workshop", date: "2024-01-17" }
  ],
  message: "Found 2 workshops. Cross-reference event IDs with member.eventsAttended to find non-attendees."
}
```

The model chains these 3 tools naturally, using its own logic for the final filtering. Compare this to the 7-8 API calls required with direct conversion.

### Another Example: Welcoming New Members

_"Send a welcome message to everyone who joined the Python space this week but hasn't posted yet"_

With well-designed tools, this becomes a natural 2-step process:

**Step 1**: The `getSpaceMembers` tool finds new members:

```javascript
{
  name: "getSpaceMembers",
  description: `<usecase>
  Retrieves members of a space with join date and activity summary.
  Can filter by join date to find new members.
  </usecase>

  <instructions>
  joinedAfter accepts relative dates like "7d", "1w", "2024-01-01"
  Returns members with basic activity counts
  </instructions>`,

  inputSchema: {
    type: "object",
    properties: {
      space: {
        type: "string",
        description: "Space name or ID"
      },
      joinedAfter: {
        type: "string",
        description: "Filter by join date (e.g., '7d' for last 7 days)"
      }
    },
    required: ["space"]
  }
}
```

When called with `{ space: "python", joinedAfter: "7d" }`, it returns:

```javascript
{
  members: [
    {
      id: "user_201",
      name: "Carol Davis",
      email: "carol@example.com",
      joinedSpace: "2024-01-23",
      stats: { posts: 0, comments: 2 }
    },
    {
      id: "user_202",
      name: "Dan Wilson",
      email: "dan@example.com",
      joinedSpace: "2024-01-24",
      stats: { posts: 0, comments: 0 }
    }
  ],
  newMemberCount: 5,
  withoutPosts: 3,
  message: "Found 5 new members, 3 haven't posted. Use bulkMessage() to send welcomes."
}
```

**Step 2**: The `bulkMessage` tool sends personalized messages:

```javascript
{
  name: "bulkMessage",
  description: `<usecase>
  Sends personalized direct messages to multiple members.
  Supports templates with variable substitution from member data.
  </usecase>

  <instructions>
  Template variables: Use ${variableName} to insert member data
  Recipients: Pass member IDs from previous tool results
  </instructions>`,

  inputSchema: {
    type: "object",
    properties: {
      recipients: {
        type: "array",
        items: { type: "string" },
        description: "Array of member IDs"
      },
      template: {
        type: "string",
        description: "Message template with ${variables}"
      }
    },
    required: ["recipients", "template"]
  }
}
```

The magic is in how these tools connect - the first tool's output is perfectly structured for the second tool's input.

### The Final Tool Set

Those 80 Circle endpoints become ~12 intent-based MCP tools:

- **Finding things**: `findContent`, `findMembers`, `findSpaces` (replaces ~15 endpoints)
- **Understanding activity**: `getSpaceActivity`, `getSpaceEvents` (replaces ~20 endpoints)
- **Taking action**: `publishContent`, `moderateContent`, `manageMembership` (replaces ~25 endpoints)
- **Communication**: `sendDirectMessage`, `bulkMessage` (replaces ~10 endpoints)
- **Automation**: `watchForChanges`, `exportData` (replaces ~10 endpoints)

Each tool represents a complete user intent, not a technical operation. The model can answer real questions without needing to understand Circle's internal data model.

## Key Takeaways

Building effective MCP tools is less about technical sophistication and more about understanding how AI models think and operate.

The best tools are those that:

1. **Communicate clearly** - Every response tells a complete story
2. **Fail gracefully** - Errors are opportunities to guide the model
3. **Stay focused** - Do a few things well rather than many things adequately
4. **Think in workflows** - Anticipate what the model will want to do next

Remember: you're not building for developers who can read documentation and debug issues. You're building for AI models that rely entirely on what you tell them in descriptions and responses. Make every word count.

The MCP ecosystem is still evolving, and we're all learning together. What patterns have you found that work well? What challenges are you facing? I'd love to hear about your experiences building tools that AI models actually want to use.

---

## Related Links
- [[MCP]]
- [[AI Tool Design]]
- [[API Design]]
- [[LLM Integration]]