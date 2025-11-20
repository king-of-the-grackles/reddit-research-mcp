# OpenAI Apps SDK: Comprehensive Guide (November 2025)

> Last Updated: November 10, 2025
> SDK Status: Preview/Beta (Launched October 6, 2025)

## Table of Contents

1. [Introduction & Overview](#introduction--overview)
2. [Most Interesting Current Use Cases](#most-interesting-current-use-cases)
3. [Core Concepts & Architecture](#core-concepts--architecture)
4. [Strengths & Weaknesses](#strengths--weaknesses)
5. [Building Apps with the SDK](#building-apps-with-the-sdk)
6. [Real-World Examples & Implementations](#real-world-examples--implementations)
7. [Platform Comparisons](#platform-comparisons)
8. [Future Roadmap & Development](#future-roadmap--development)
9. [Resources & References](#resources--references)

---

## Introduction & Overview

### What is the OpenAI Apps SDK?

The **OpenAI Apps SDK** is a development framework that enables developers to build interactive applications that run directly inside ChatGPT conversations. Announced on October 6, 2025 at OpenAI DevDay, the SDK represents OpenAI's vision of transforming ChatGPT into a platform—effectively creating a new kind of "app store" where applications are discovered and used through natural language conversations rather than traditional browsing and searching.

### Key Characteristics

**Platform Integration**: Unlike traditional apps that require separate downloads or installations, Apps SDK applications run entirely within the ChatGPT interface. Users interact with apps through natural conversation, and apps can render custom UI components directly in the chat window.

**Model Context Protocol Foundation**: The SDK is built on top of the **Model Context Protocol (MCP)**, an open standard that OpenAI helped create. This means apps built with the SDK can potentially run on any AI platform that adopts MCP, reducing vendor lock-in concerns.

**Conversational Discovery**: Instead of searching an app store, users discover apps organically through conversation. ChatGPT automatically suggests relevant apps based on the context of the discussion, creating a more intuitive discovery mechanism.

### Launch Timeline & Current Status

- **Announced**: October 6, 2025 at OpenAI DevDay 2025
- **Current Status**: Preview/Beta phase (as of November 2025)
- **Age**: Approximately 1 month old
- **Availability**: All logged-in ChatGPT users **except** those in the EU, UK, and Switzerland
- **User Base**: 800+ million ChatGPT users (potential reach)
- **Public Sharing**: Not yet available; developers can build and test in Developer Mode only

### Why This Matters

With over 800 million ChatGPT users, the Apps SDK offers developers unprecedented distribution potential. OpenAI is positioning ChatGPT as "the new app store"—a platform where users spend significant time and where natural language becomes the primary interface for accessing services and functionality.

**Sam Altman's Vision** (OpenAI CEO):
> "We think ChatGPT can become the interface where people get things done, and with apps, we are moving toward that vision."

### Key Differences from ChatGPT Plugins

The Apps SDK supersedes the older ChatGPT Plugins system (which is being deprecated). Key improvements include:

- **More Sophisticated UI**: Apps can render custom HTML/CSS/JavaScript components, not just structured data
- **Better Discovery**: Improved metadata system for contextual app surfacing
- **Open Standard**: Built on MCP rather than proprietary API
- **Enhanced Security**: OAuth 2.1 implementation with better permission models
- **Integrated Experience**: Seamless inline rendering vs. separate plugin interface

---

## Most Interesting Current Use Cases

Given the SDK's recent launch (October 2025), there are currently about 18 launch partner apps available, with a broader ecosystem expected when the app submission process opens later in 2025. Here are the most compelling use cases emerging:

### 1. Travel Planning & Booking

**Expedia Integration**
- **What It Does**: Users can search for flights, hotels, and vacation packages through natural conversation
- **Key Features**:
  - Price comparison across multiple providers
  - Date flexibility recommendations
  - Package deals and combinations
  - Direct booking capability
- **Why It's Interesting**: Eliminates the need to switch between ChatGPT and travel sites; entire research and booking flow happens in conversation

**Example Interaction**:
```
User: "I need a hotel in Paris for next week, budget-friendly but near museums"
→ Expedia app activates
→ Returns interactive results with prices, locations, reviews
→ User can refine search or book directly
```

**Booking.com Integration**
Similar to Expedia but with different inventory and pricing. Competition between travel apps will be interesting to watch as the platform matures.

### 2. Real Estate Search

**Zillow Integration**
- **What It Does**: Interactive property search with conversational filtering
- **Key Features**:
  - Map-based property browsing
  - Natural language filters ("3 bedroom houses under $500k near good schools")
  - Neighborhood information and statistics
  - Price trend analysis
  - Direct contact with agents
- **Why It's Interesting**: Transforms complex property search into conversational experience; visual map components embedded directly in chat

**Quote from Josh Weisberg, Head of AI at Zillow**:
> "The Zillow app in ChatGPT shows the power of AI to make real estate feel more human. Together with OpenAI, we're bringing a first-of-its-kind experience to millions—a conversational guide that makes finding a home faster, easier, and more intuitive."

**Technical Innovation**: Demonstrates how to integrate complex geographic data and interactive maps into conversational AI.

### 3. Creative & Design Tools

**Canva Integration**
- **What It Does**: Creates professional designs and presentations from natural language descriptions
- **Key Features**:
  - Transform outlines into slide decks
  - Generate social media graphics
  - Create marketing materials
  - Brand-consistent design generation
  - Direct editing in Canva after creation
- **Why It's Interesting**: Bridges the gap between ideation (in ChatGPT) and execution (in Canva); reduces friction in creative workflows

**Example Workflow**:
```
User: "Create a 5-slide pitch deck about renewable energy solutions"
→ ChatGPT drafts outline
→ User refines content through conversation
→ Canva app generates professional slides
→ User clicks to edit/export in Canva
```

**Figma Integration** (Coming Soon)
Similar concept for design collaboration and prototyping.

### 4. Music & Entertainment

**Spotify Integration**
- **What It Does**: Creates custom playlists based on mood, activity, or preference descriptions
- **Key Features**:
  - Natural language playlist creation ("upbeat workout music from the 90s")
  - Mood-based recommendations
  - Activity-specific playlists
  - Artist/genre exploration
  - Direct playback in Spotify
- **Why It's Interesting**: Converts abstract concepts (mood, vibe, feeling) into concrete playlists; demonstrates AI's strength in subjective interpretation

### 5. Education & Learning

**Coursera Integration**
- **What It Does**: Recommends online courses based on learning goals and career objectives
- **Key Features**:
  - Personalized course recommendations
  - Career path guidance
  - Skill gap analysis
  - Course comparison and reviews
  - Direct enrollment capability
- **Why It's Interesting**: Combines career counseling with course discovery; could evolve into AI-powered learning pathways

**Potential Evolution**: As the platform matures, expect more sophisticated learning apps that track progress, provide tutoring, or create custom curricula.

### 6. Food & Delivery Services

**Coming Soon (Late 2025)**:
- **DoorDash**: Restaurant search and food delivery
- **Instacart**: Grocery shopping and delivery
- **OpenTable** / **theFork**: Restaurant reservations
- **Target**: Product search and shopping

**Potential Use Case**:
```
User: "I need dinner for 4 people, something healthy, delivered by 7pm"
→ DoorDash app suggests restaurants
→ Considers dietary preferences from conversation
→ Shows delivery times and pricing
→ User orders through chat
```

### 7. Fitness & Wellness

**Peloton Integration** (Coming Soon)
- Expected to provide workout recommendations, class scheduling, and fitness tracking
- Could integrate with conversation about health goals, schedule constraints, etc.

**AllTrails Integration** (Coming Soon)
- Hiking trail recommendations based on location, difficulty, scenery preferences
- Demonstrates location-aware app capabilities

### 8. Transportation

**Uber Integration** (Coming Soon)
- **Expected Capabilities**: Ride booking through conversation
- **Why It's Compelling**: Eliminates app switching; could coordinate multi-modal transportation planning

**Example Future Scenario**:
```
User: "I need to get from the conference to the airport by 4pm"
→ Uber app checks traffic, flight times
→ Suggests departure time
→ Books ride with one confirmation
```

### 9. Emerging & Experimental Use Cases

Beyond launch partners, the developer community is exploring:

**Data Visualization**: Interactive charts and graphs embedded in conversation

**Customer Support Automation**: Companies building internal ChatGPT apps for employee support

**Workflow Automation**: Apps that trigger actions across multiple services

**3D Visualization**: Solar system explorer, molecular structures, architectural models

**Financial Analysis**: Real-time market data, portfolio management, investment research

**Document Processing**: PDF analysis, data extraction, report generation

---

## Core Concepts & Architecture

### Model Context Protocol (MCP) Foundation

The Apps SDK is built on **Model Context Protocol (MCP)**, an open standard for connecting AI assistants to external tools and data sources. Understanding MCP is essential to understanding the Apps SDK.

#### What is MCP?

MCP defines a standardized way for AI models to:
1. **Discover** what tools and resources are available
2. **Describe** what each tool does and what parameters it requires
3. **Execute** tools and receive structured responses
4. **Render** custom UI components with results

#### MCP Server Architecture

An MCP server exposes three core primitives:

**1. Tools**: Executable functions that perform actions
```typescript
{
  name: "search_restaurants",
  description: "Use this when the user wants to find restaurants",
  inputSchema: {
    type: "object",
    properties: {
      location: { type: "string" },
      cuisine: { type: "string" },
      priceRange: { type: "string", enum: ["$", "$$", "$$$", "$$$$"] }
    },
    required: ["location"]
  }
}
```

**2. Resources**: Data sources the app can access
```typescript
{
  uri: "restaurants://favorites",
  name: "User's Favorite Restaurants",
  description: "Previously saved restaurant preferences",
  mimeType: "application/json"
}
```

**3. Widgets**: UI components for displaying results
```typescript
{
  uri: "ui://widget/restaurant_card",
  name: "Restaurant Card Widget",
  mimeType: "text/html+skybridge",
  template: "<div class='restaurant-card'>...</div>"
}
```

### Apps SDK Architecture

The Apps SDK extends MCP with ChatGPT-specific features:

#### Component Layers

```
┌─────────────────────────────────────┐
│         ChatGPT Frontend            │
│  (Conversation UI + App Rendering)  │
└─────────────┬───────────────────────┘
              │
    ┌─────────▼──────────┐
    │   Apps SDK Layer   │
    │ (Discovery, OAuth, │
    │  Sandboxing)       │
    └─────────┬──────────┘
              │
    ┌─────────▼──────────┐
    │    MCP Server      │
    │ (Your Backend API) │
    └─────────┬──────────┘
              │
    ┌─────────▼──────────┐
    │  External Services │
    │ (Databases, APIs)  │
    └────────────────────┘
```

#### Key Architectural Concepts

**1. Conversational Activation**

Apps don't have traditional "launch" buttons. Instead:
- ChatGPT analyzes conversation context
- Checks app metadata for relevance
- Automatically suggests or activates appropriate apps
- Apps remain invisible until contextually relevant

**Best Practice**: Write metadata descriptions starting with "Use this when..." to optimize discovery.

**Example**:
```json
{
  "name": "weather_forecast",
  "description": "Use this when the user asks about weather, temperature, or forecasts for any location"
}
```

**2. Tool-First Design**

Apps are collections of **tools** (discrete functions) rather than monolithic applications:
- Each tool should do **one specific thing**
- Tools can be chained together by ChatGPT
- Tools return structured data + optional UI rendering instructions

**Anti-Pattern**: Creating a single tool that does everything
**Best Practice**: Multiple focused tools that compose well

**Example - Food Delivery App**:
```
✗ Bad: deliver_food(restaurant, items, address, payment, time)
✓ Good:
  - search_restaurants(location, cuisine)
  - get_menu(restaurant_id)
  - calculate_delivery_time(restaurant_id, address)
  - place_order(cart, delivery_info)
```

**3. Widget System**

Apps can return custom HTML/CSS/JavaScript UI components:

**Widget Registration**:
```typescript
server.setRequestHandler(ListResourcesRequestSchema, async () => {
  return {
    resources: [
      {
        uri: "ui://widget/property_map",
        name: "Property Map Widget",
        mimeType: "text/html+skybridge",
        description: "Interactive map showing property locations"
      }
    ]
  };
});
```

**Widget Response**:
```typescript
{
  content: [
    {
      type: "resource",
      resource: {
        uri: "ui://widget/property_map",
        mimeType: "text/html+skybridge",
        text: `
          <div class="property-map">
            <div id="map-container"></div>
            <script>
              // Map rendering code
              renderMap(${JSON.stringify(properties)});
            </script>
          </div>
        `
      }
    }
  ]
}
```

**4. Sandboxing & Security**

Widgets render in secure iframes:
- Domain: `chatgpt-com.web-sandbox.oaiusercontent.com`
- Strict Content Security Policy (CSP)
- Explicit permission required for external network requests
- External links validated through `openai.openExternal()`

**CSP Configuration Example**:
```typescript
{
  "widget_domains": ["maps.googleapis.com", "cdn.example.com"],
  "csp": {
    "script-src": ["'self'", "'unsafe-inline'"],
    "style-src": ["'self'", "'unsafe-inline'"],
    "img-src": ["'self'", "data:", "https:"],
    "connect-src": ["'self'", "https://api.example.com"]
  }
}
```

### Authentication & User Context

**OAuth 2.1 Implementation**:

1. **User initiates action** requiring authentication (e.g., "book this hotel")
2. **ChatGPT redirects** to app's OAuth endpoint
3. **User authorizes** the app to access their account
4. **App receives access token** tied to the ChatGPT user
5. **Subsequent requests** include user context automatically

**Token Management**:
```typescript
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  const userContext = request.context?.user; // OAuth user info

  if (name === "book_hotel") {
    // Use userContext to make authenticated API call
    const booking = await api.bookHotel(args.hotel_id, userContext.token);
    return { content: [{ type: "text", text: booking.confirmation }] };
  }
});
```

### Developer Mode & Testing

**How Testing Works**:

1. **Enable Developer Mode** in ChatGPT settings
2. **Start local MCP server** (e.g., on `http://localhost:3000`)
3. **Use ngrok or similar** to expose localhost (optional for local testing)
4. **Register app** in ChatGPT Developer Mode with server URL
5. **Test in conversation** - apps work exactly as they will in production
6. **Iterate rapidly** - changes reflect immediately

**Developer Mode Limitations**:
- Only visible to you
- Cannot share with other users yet
- Not discoverable in conversation without explicit invocation
- Must manually configure in settings

### Metadata & Discovery Optimization

**App Manifest Structure**:
```json
{
  "name": "restaurant-finder",
  "display_name": "Restaurant Finder",
  "description": "Use this when the user wants to find restaurants, make reservations, or get dining recommendations",
  "version": "1.0.0",
  "homepage": "https://example.com",
  "privacy_policy": "https://example.com/privacy",
  "tools": [
    {
      "name": "search_restaurants",
      "description": "Use this when the user mentions looking for a place to eat, restaurant recommendations, or dining options",
      "parameters": { ... }
    }
  ],
  "oauth": {
    "client_id": "...",
    "authorization_url": "https://example.com/oauth/authorize",
    "token_url": "https://example.com/oauth/token",
    "scopes": ["read:profile", "write:reservations"]
  }
}
```

**Discovery Best Practices**:
- **Be specific but not narrow**: "Use this when the user asks about weather, temperature, forecasts, or climate conditions for any location"
- **Avoid overlap**: If your tool description matches many other apps, it won't surface reliably
- **Include synonyms**: Users might say "film" or "movie" - cover both
- **Test extensively**: The more conversations you test, the better you'll understand when your app appears

---

## Strengths & Weaknesses

### Strengths

#### 1. Unprecedented Distribution Potential

**800+ Million Users**: The Apps SDK gives developers access to one of the largest user bases in the world—over 800 million ChatGPT users. Compare this to:
- Apple App Store: ~650 million weekly active users
- Google Play Store: ~2.5 billion, but much more fragmented

**No Download Friction**: Users don't need to:
- Search an app store
- Download anything
- Create a new account (if OAuth is connected)
- Learn a new interface

This dramatically reduces abandonment rates compared to traditional apps.

#### 2. AI-Native Discovery

**Contextual Surfacing**: Instead of users remembering to open your app, ChatGPT automatically suggests it when relevant. This could lead to:
- Higher engagement rates
- More organic usage
- Less marketing spend needed for awareness

**Long-Tail Discovery**: Niche apps that would struggle to get App Store visibility can surface when they're the perfect fit for a conversation.

#### 3. Conversational UX Paradigm

**Natural Language as Interface**: Users describe what they want in plain language rather than navigating complex menus and forms.

**Context-Aware**: Apps inherit conversation context, reducing data entry:
```
User: "I'm planning a trip to Tokyo next month"
[conversation continues...]
User: "Find me a hotel"
→ Hotel app already knows: Tokyo, next month
```

**Progressive Disclosure**: Apps can ask follow-up questions naturally rather than presenting overwhelming forms upfront.

#### 4. Open Standard (MCP)

**Portability**: Apps built with MCP can theoretically run on:
- Claude (Anthropic supports MCP)
- Other AI assistants that adopt the protocol
- Desktop environments (via MCP clients)

**Avoid Lock-In**: Developers aren't building exclusively for OpenAI's ecosystem, reducing business risk.

#### 5. Rapid Development Cycle

**Familiar Technologies**: HTML, CSS, JavaScript, standard OAuth
**Quick Iterations**: Changes deploy immediately with Developer Mode testing
**Clear Separation**: Frontend (widgets) and backend (tools) are cleanly separated

#### 6. Composability

**Tools Chain Together**: ChatGPT can use multiple apps in sequence to accomplish complex tasks:
```
User: "Plan a weekend in San Francisco"
→ Expedia: Find flights
→ Booking.com: Find hotel
→ OpenTable: Make dinner reservation
→ Uber: Book airport pickup
```

This creates a more powerful experience than any single app could provide.

### Weaknesses

#### 1. Extremely Early Stage

**One Month Old**: The SDK launched October 2025—it's only about 4 weeks old as of November 2025.

**Implications**:
- Limited documentation and examples
- Few established best practices
- Community/ecosystem still forming
- Unclear which patterns will succeed
- Likely breaking changes ahead

**Risk**: Early adopters may need to rebuild as the platform matures.

#### 2. No Public Launch Path Yet

**Preview Only**: Developers can build and test, but:
- Cannot publish apps publicly
- Cannot share with users
- App directory not open for submissions
- No timeline for general availability (just "later 2025")

**Business Impact**:
- Can't generate revenue yet
- Can't build user base
- Can't validate product-market fit with real users
- Uncertain wait time before launch

#### 3. Limited Documentation

**Sparse Official Docs**: OpenAI's documentation is basic:
- Minimal code examples
- Limited troubleshooting guides
- Few architecture recommendations
- No comprehensive tutorials

**Community Filling Gaps**: Developers are writing their own guides, but this takes time and leads to inconsistent advice.

#### 4. Discovery is Non-Deterministic

**No Guaranteed Visibility**: Even if your app is perfect for a situation, there's no guarantee ChatGPT will surface it.

**Challenges**:
- Hard to predict when your app will appear
- Difficult to test all scenarios
- Metadata optimization is more art than science
- Could lead to user frustration if relevant apps don't surface

**Contrast with App Stores**: In traditional stores, users who search for your category will find you (if you rank well). Here, discoverability is AI-mediated and less controllable.

#### 5. Regional Restrictions

**Not Available in EU/UK/Switzerland**: Likely due to regulatory considerations (GDPR, AI Act, etc.)

**Impact**:
- Developers in those regions can't test with real users
- Large market excluded (EU population ~450 million)
- Unclear timeline for expansion
- May require separate compliance work

#### 6. Monetization Unclear

**No Business Model Details**: OpenAI has said monetization is coming "later this year" but hasn't specified:
- Revenue share percentages
- Payment processing
- Subscription vs. transaction-based pricing
- Payout mechanisms
- Minimum thresholds

**Uncertainty**: Hard to build a business case without knowing economics.

#### 7. Platform Control & Dependency

**OpenAI Controls Everything**:
- Who gets approved for the app directory
- How discovery algorithm works
- Pricing and revenue share
- Design guidelines and restrictions
- Data access policies

**Risk**: Developers are dependent on OpenAI's decisions, with limited recourse if policies change unfavorably.

#### 8. Performance & Debugging Challenges

**Common Issues**:
- **424 Errors**: Frequent during development, often due to CSP/CORS misconfiguration
- **iframe Limitations**: Harder to debug than standard web apps
- **Network Request Restrictions**: Explicit CSP permissions required
- **Sandboxing Constraints**: Some JavaScript features unavailable

**Developer Experience**: More friction than building a standard web app, especially for those unfamiliar with strict CSP environments.

#### 9. Privacy & Data Concerns

**User Data Flow**:
```
User → ChatGPT → App Backend → External Services
```

**Questions**:
- What conversation data does the app see?
- How does ChatGPT handle sensitive information?
- What happens to data after interaction?
- How transparent is data usage to users?

**Reputational Risk**: If apps misuse data, could damage ChatGPT's brand and lead to stricter restrictions.

#### 10. Limited Differentiation Opportunities

**Conversational UI Constraints**: All apps share the same chat interface, making it harder to create distinctive brand experiences compared to standalone apps with custom UX.

**Widget Limitations**: While apps can render custom UI, it's still within ChatGPT's design framework and size constraints.

---

## Building Apps with the SDK

### Development Workflow Overview

```
1. Design App Concept
   ↓
2. Set Up MCP Server (Python or Node.js)
   ↓
3. Implement Tools (Functions)
   ↓
4. Create Widgets (UI Components)
   ↓
5. Configure OAuth (if needed)
   ↓
6. Test Locally with Developer Mode
   ↓
7. Deploy to Production Server
   ↓
8. Submit to App Directory (when available)
```

### Prerequisites

**Development Environment**:
- Node.js 18+ or Python 3.10+
- Code editor (VS Code recommended)
- Git for version control
- ngrok or similar tunneling tool (for local testing)

**Accounts & Access**:
- ChatGPT Plus, Team, or Enterprise account (for Developer Mode)
- OpenAI developer account
- Hosting platform account (Render, Railway, Vercel, etc.)

**Knowledge Requirements**:
- Familiarity with REST APIs
- Basic understanding of OAuth 2.0
- HTML/CSS/JavaScript for widgets
- Backend framework (Express.js or FastAPI)

### Step 1: Set Up MCP Server

#### Option A: Node.js/TypeScript

**Install MCP SDK**:
```bash
npm install @anthropic-ai/sdk-mcp
```

**Basic Server Structure** (`server.ts`):
```typescript
import { Server } from "@anthropic-ai/sdk-mcp";
import {
  ListToolsRequestSchema,
  CallToolRequestSchema,
  ListResourcesRequestSchema,
} from "@anthropic-ai/sdk-mcp";

const server = new Server(
  {
    name: "restaurant-finder",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
      resources: {},
    },
  }
);

// Tool definitions
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "search_restaurants",
        description: "Use this when the user wants to find restaurants based on location and cuisine",
        inputSchema: {
          type: "object",
          properties: {
            location: {
              type: "string",
              description: "City or address to search near",
            },
            cuisine: {
              type: "string",
              description: "Type of cuisine (Italian, Mexican, etc.)",
            },
            priceRange: {
              type: "string",
              enum: ["$", "$$", "$$$", "$$$$"],
              description: "Price range for restaurants",
            },
          },
          required: ["location"],
        },
      },
    ],
  };
});

// Tool execution
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  if (name === "search_restaurants") {
    // Call your backend API or database
    const results = await searchRestaurants(args);

    return {
      content: [
        {
          type: "text",
          text: `Found ${results.length} restaurants matching your criteria`,
        },
        {
          type: "resource",
          resource: {
            uri: "ui://widget/restaurant_list",
            mimeType: "text/html+skybridge",
            text: renderRestaurantList(results),
          },
        },
      ],
    };
  }

  throw new Error(`Unknown tool: ${name}`);
});

// Widget definitions
server.setRequestHandler(ListResourcesRequestSchema, async () => {
  return {
    resources: [
      {
        uri: "ui://widget/restaurant_list",
        name: "Restaurant List Widget",
        mimeType: "text/html+skybridge",
        description: "Displays restaurant search results",
      },
    ],
  };
});

// Start server
const transport = new StdioServerTransport();
await server.connect(transport);
```

#### Option B: Python

**Install MCP SDK**:
```bash
pip install anthropic-mcp
```

**Basic Server Structure** (`server.py`):
```python
from anthropic_mcp import Server, Tool, Resource
from typing import Any, Dict, List

app = Server("restaurant-finder", version="1.0.0")

@app.tool()
def search_restaurants(
    location: str,
    cuisine: str = None,
    price_range: str = None
) -> Dict[str, Any]:
    """
    Use this when the user wants to find restaurants based on location and cuisine.

    Args:
        location: City or address to search near
        cuisine: Type of cuisine (Italian, Mexican, etc.)
        price_range: Price range ($, $$, $$$, $$$$)
    """
    # Call your backend API or database
    results = search_api(location, cuisine, price_range)

    return {
        "content": [
            {
                "type": "text",
                "text": f"Found {len(results)} restaurants matching your criteria"
            },
            {
                "type": "resource",
                "resource": {
                    "uri": "ui://widget/restaurant_list",
                    "mimeType": "text/html+skybridge",
                    "text": render_restaurant_list(results)
                }
            }
        ]
    }

@app.resource("ui://widget/restaurant_list")
def restaurant_list_widget():
    """Displays restaurant search results"""
    return {
        "mimeType": "text/html+skybridge",
        "description": "Restaurant list display component"
    }

if __name__ == "__main__":
    app.run()
```

### Step 2: Implement Tools

**Best Practices for Tool Design**:

**1. Action-Oriented Naming**: Use verbs that describe what the tool does
```
✓ Good: search_hotels, book_reservation, get_menu
✗ Bad: hotels, reservation, menu
```

**2. Clear Descriptions**: Start with "Use this when..." for optimal discovery
```typescript
{
  name: "calculate_delivery_time",
  description: "Use this when the user asks how long delivery will take or when their order will arrive",
  // ...
}
```

**3. Comprehensive Input Schemas**: Define all parameters clearly
```typescript
inputSchema: {
  type: "object",
  properties: {
    address: {
      type: "string",
      description: "Full delivery address including street, city, zip code"
    },
    restaurant_id: {
      type: "string",
      description: "Unique identifier for the restaurant"
    }
  },
  required: ["address", "restaurant_id"]
}
```

**4. Structured Outputs**: Return both text and visual components
```typescript
return {
  content: [
    {
      type: "text",
      text: "Your order will arrive in approximately 35 minutes"
    },
    {
      type: "resource",
      resource: {
        uri: "ui://widget/delivery_tracker",
        mimeType: "text/html+skybridge",
        text: renderDeliveryTracker(orderData)
      }
    }
  ]
};
```

**5. Error Handling**: Provide helpful error messages
```typescript
try {
  const results = await apiCall(args);
  return { content: [...] };
} catch (error) {
  return {
    content: [
      {
        type: "text",
        text: "I couldn't complete that search. The restaurant service might be temporarily unavailable. Please try again in a moment."
      }
    ],
    isError: true
  };
}
```

### Step 3: Create Widgets

**Widget HTML Structure**:
```html
<div class="app-widget" style="
  border-radius: 12px;
  padding: 16px;
  background: white;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
">
  <h3>Search Results</h3>
  <div class="results-list">
    <!-- Results go here -->
  </div>
</div>

<style>
  .app-widget {
    font-family: system-ui, -apple-system, sans-serif;
    max-width: 600px;
  }

  .result-card {
    padding: 12px;
    margin: 8px 0;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.2s;
  }

  .result-card:hover {
    background: #f5f5f5;
  }
</style>

<script>
  // Widget interactivity
  document.querySelectorAll('.result-card').forEach(card => {
    card.addEventListener('click', () => {
      const resultId = card.dataset.id;
      // Trigger follow-up action
      window.parent.postMessage({
        type: 'tool_call',
        tool: 'get_details',
        args: { id: resultId }
      }, '*');
    });
  });
</script>
```

**CSP Considerations**:

Widgets run in sandboxed iframes with strict Content Security Policy. You'll need to configure allowed domains:

```typescript
// In your app manifest
{
  "widget_domains": [
    "cdn.yourservice.com",
    "maps.googleapis.com"
  ],
  "csp": {
    "script-src": ["'self'", "'unsafe-inline'"],
    "style-src": ["'self'", "'unsafe-inline'"],
    "img-src": ["'self'", "data:", "https:"],
    "connect-src": ["'self'", "https://api.yourservice.com"]
  }
}
```

**External Links**:

Use the ChatGPT bridge API for external navigation:
```javascript
document.querySelector('.external-link').addEventListener('click', (e) => {
  e.preventDefault();
  openai.openExternal('https://yourservice.com/details/123');
});
```

### Step 4: Configure OAuth

**When OAuth is Needed**:
- Accessing user-specific data
- Making purchases or bookings
- Modifying user accounts
- Any action requiring user identity

**OAuth Configuration**:
```typescript
// In your app manifest
{
  "oauth": {
    "client_id": "your_client_id",
    "authorization_url": "https://yourservice.com/oauth/authorize",
    "token_url": "https://yourservice.com/oauth/token",
    "scopes": ["read:profile", "write:bookings"],
    "pkce": true  // Recommended for security
  }
}
```

**Backend OAuth Handler**:
```typescript
app.get('/oauth/authorize', (req, res) => {
  const { redirect_uri, state, code_challenge } = req.query;

  // Show user authorization page
  res.render('authorize', {
    appName: 'Restaurant Finder',
    permissions: ['Access your profile', 'Make reservations'],
    redirectUri: redirect_uri,
    state: state
  });
});

app.post('/oauth/token', async (req, res) => {
  const { code, code_verifier } = req.body;

  // Verify PKCE challenge
  // Generate access token
  const token = generateToken(userId);

  res.json({
    access_token: token,
    token_type: 'Bearer',
    expires_in: 3600
  });
});
```

**Using OAuth in Tools**:
```typescript
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const userContext = request.context?.user;
  const accessToken = userContext?.token;

  if (!accessToken) {
    return {
      content: [{
        type: "text",
        text: "Please sign in to make a reservation"
      }],
      requiresAuth: true
    };
  }

  // Use token to make authenticated API call
  const booking = await api.createBooking(args, accessToken);
  return { content: [...] };
});
```

### Step 5: Local Testing with Developer Mode

**Setup Steps**:

1. **Start your MCP server locally**:
```bash
npm run dev  # Server runs on http://localhost:3000
```

2. **Expose via ngrok** (if needed for ChatGPT to reach):
```bash
ngrok http 3000
# Generates URL like: https://abc123.ngrok.io
```

3. **Enable Developer Mode** in ChatGPT:
   - Settings → Features → Developer Mode → Enable

4. **Register your app**:
   - Developer Mode → Manage Apps → Add App
   - Enter your server URL (localhost or ngrok)
   - Save configuration

5. **Test in conversation**:
```
You: "Find me Italian restaurants in San Francisco"
→ Your app should activate
→ Test tool execution
→ Verify widget rendering
→ Check error handling
```

**Debugging Tips**:

- Check browser DevTools console for widget errors
- Monitor server logs for tool execution
- Use ChatGPT's tool inspector (if available)
- Test edge cases (missing parameters, API failures, etc.)

### Step 6: Deployment

**Deployment Checklist**:

- [ ] Environment variables configured (API keys, secrets)
- [ ] OAuth endpoints publicly accessible with HTTPS
- [ ] CSP and CORS headers properly configured
- [ ] Error logging and monitoring set up
- [ ] Rate limiting implemented
- [ ] Privacy policy and terms of service published
- [ ] Performance testing completed
- [ ] Security audit performed

**Platform Options**:

**Render** (recommended for Node.js):
```yaml
# render.yaml
services:
  - type: web
    name: restaurant-finder-mcp
    env: node
    buildCommand: npm install && npm run build
    startCommand: npm start
    envVars:
      - key: NODE_ENV
        value: production
      - key: API_KEY
        sync: false
```

**Railway**:
```toml
# railway.toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "npm start"
restartPolicyType = "ON_FAILURE"
```

**Vercel** (for serverless):
```json
// vercel.json
{
  "builds": [
    { "src": "server.ts", "use": "@vercel/node" }
  ],
  "routes": [
    { "src": "/(.*)", "dest": "/server.ts" }
  ]
}
```

### Step 7: App Submission (When Available)

**Submission Process** (expected to open late 2025):

1. **Prepare App Package**:
   - App manifest with complete metadata
   - Privacy policy URL
   - Terms of service URL
   - App icon and screenshots
   - Demo video (optional but recommended)

2. **Submit for Review**:
   - OpenAI will review for:
     - Functionality and reliability
     - Design quality
     - Privacy and security compliance
     - User experience
     - Metadata accuracy

3. **Review Period**:
   - Expected: 1-2 weeks
   - May require revisions
   - Security and privacy checks

4. **Launch**:
   - App appears in directory
   - Users can discover through conversation
   - Monitor analytics and feedback

**Approval Criteria** (anticipated):
- App works reliably without errors
- UI follows design guidelines (rounded corners, proper styling)
- Metadata accurately describes functionality
- No privacy violations or data misuse
- OAuth implementation is secure
- Appropriate for ChatGPT's audience

---

## Real-World Examples & Implementations

### Example 1: Movie Recommendation App

**Concept**: Help users find movies to watch based on mood, genre, or preferences.

**Tools**:
```typescript
// Tool 1: Search movies
{
  name: "search_movies",
  description: "Use this when the user wants to find movies based on genre, mood, actors, or other criteria",
  inputSchema: {
    type: "object",
    properties: {
      query: { type: "string", description: "Search query or description" },
      genre: { type: "string", description: "Movie genre" },
      year: { type: "number", description: "Release year or range" },
      minRating: { type: "number", description: "Minimum rating (0-10)" }
    }
  }
}

// Tool 2: Get movie details
{
  name: "get_movie_details",
  description: "Use this when the user wants more information about a specific movie",
  inputSchema: {
    type: "object",
    properties: {
      movieId: { type: "string", required: true }
    }
  }
}

// Tool 3: Find where to watch
{
  name: "find_streaming",
  description: "Use this when the user asks where they can watch a movie (streaming services, rental options)",
  inputSchema: {
    type: "object",
    properties: {
      movieId: { type: "string", required: true },
      country: { type: "string", default: "US" }
    }
  }
}
```

**Widget - Movie Card**:
```html
<div class="movie-card">
  <img src="{{poster_url}}" alt="{{title}}" class="movie-poster">
  <div class="movie-info">
    <h3>{{title}} ({{year}})</h3>
    <div class="rating">⭐ {{rating}}/10</div>
    <p class="synopsis">{{synopsis}}</p>
    <div class="streaming-options">
      <span class="service netflix">Netflix</span>
      <span class="service prime">Prime Video</span>
    </div>
    <button onclick="getDetails('{{id}}')">More Info</button>
  </div>
</div>

<style>
  .movie-card {
    display: flex;
    gap: 16px;
    padding: 16px;
    background: white;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  }

  .movie-poster {
    width: 150px;
    height: 225px;
    object-fit: cover;
    border-radius: 8px;
  }

  .movie-info {
    flex: 1;
  }

  .rating {
    color: #f59e0b;
    font-weight: bold;
    margin: 8px 0;
  }

  .streaming-options {
    display: flex;
    gap: 8px;
    margin: 12px 0;
  }

  .service {
    padding: 4px 12px;
    border-radius: 16px;
    font-size: 12px;
    color: white;
  }

  .netflix { background: #e50914; }
  .prime { background: #00a8e1; }
</style>
```

**Example Conversation**:
```
User: "I want to watch something funny from the 90s"

ChatGPT: [Activates movie app]
I'll help you find some great comedies from the 90s!

[Movie cards appear showing:]
- The Big Lebowski (1998) - 8.1/10
- Groundhog Day (1993) - 8.0/10
- Office Space (1999) - 7.6/10

User: "Tell me more about Office Space"

ChatGPT: [Gets movie details]
[Shows expanded card with cast, director, detailed synopsis, trivia]

User: "Where can I watch it?"

ChatGPT: [Finds streaming options]
Office Space is available on:
- Hulu (included with subscription)
- Amazon Prime Video (rent for $3.99)
- Apple TV (rent for $3.99)
```

### Example 2: Solar System 3D Viewer

**Concept**: Interactive 3D visualization of the solar system (educational app).

**Tools**:
```typescript
// Tool: Load solar system
{
  name: "load_solar_system",
  description: "Use this when the user wants to explore or visualize the solar system, planets, or space",
  inputSchema: {
    type: "object",
    properties: {
      focus: {
        type: "string",
        enum: ["overview", "earth", "mars", "jupiter", "saturn"],
        description: "Which planet to focus on"
      },
      date: {
        type: "string",
        description: "Date to show planetary positions (YYYY-MM-DD)"
      }
    }
  }
}
```

**Widget - 3D Canvas**:
```html
<div class="solar-system-viewer">
  <canvas id="space-canvas" width="600" height="400"></canvas>
  <div class="controls">
    <button onclick="focusPlanet('earth')">Earth</button>
    <button onclick="focusPlanet('mars')">Mars</button>
    <button onclick="focusPlanet('jupiter')">Jupiter</button>
  </div>
  <div class="info-panel">
    <h3 id="planet-name">Earth</h3>
    <p id="planet-facts">Distance from Sun: 149.6 million km</p>
  </div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
  // Three.js scene setup
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(75, 600/400, 0.1, 1000);
  const renderer = new THREE.WebGLRenderer({ canvas: document.getElementById('space-canvas') });

  // Add sun
  const sunGeometry = new THREE.SphereGeometry(5, 32, 32);
  const sunMaterial = new THREE.MeshBasicMaterial({ color: 0xffff00 });
  const sun = new THREE.Mesh(sunGeometry, sunMaterial);
  scene.add(sun);

  // Add planets (simplified)
  const planets = createPlanets();
  planets.forEach(planet => scene.add(planet));

  // Animation loop
  function animate() {
    requestAnimationFrame(animate);
    // Update planetary positions
    updatePlanetaryOrbits();
    renderer.render(scene, camera);
  }
  animate();

  function focusPlanet(name) {
    // Animate camera to planet
    animateCameraTo(planets[name].position);
    // Update info panel
    updateInfoPanel(name);
  }
</script>

<style>
  .solar-system-viewer {
    background: #000;
    border-radius: 12px;
    padding: 16px;
  }

  #space-canvas {
    display: block;
    margin: 0 auto;
  }

  .controls {
    text-align: center;
    margin-top: 12px;
  }

  .controls button {
    margin: 0 4px;
    padding: 8px 16px;
    background: #1e40af;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
  }

  .info-panel {
    margin-top: 16px;
    padding: 12px;
    background: rgba(255,255,255,0.1);
    border-radius: 8px;
    color: white;
  }
</style>
```

### Example 3: Todo Dashboard

**Concept**: Manage tasks and todo lists within ChatGPT conversations.

**Tools**:
```typescript
// Tool 1: List todos
{
  name: "list_todos",
  description: "Use this when the user wants to see their todo list or tasks",
  inputSchema: {
    type: "object",
    properties: {
      filter: {
        type: "string",
        enum: ["all", "today", "overdue", "completed"],
        default: "all"
      }
    }
  }
}

// Tool 2: Add todo
{
  name: "add_todo",
  description: "Use this when the user wants to add a task or create a todo item",
  inputSchema: {
    type: "object",
    properties: {
      title: { type: "string", required: true },
      dueDate: { type: "string", format: "date" },
      priority: { type: "string", enum: ["low", "medium", "high"] }
    }
  }
}

// Tool 3: Complete todo
{
  name: "complete_todo",
  description: "Use this when the user wants to mark a task as done or complete",
  inputSchema: {
    type: "object",
    properties: {
      todoId: { type: "string", required: true }
    }
  }
}

// Tool 4: Delete todo
{
  name: "delete_todo",
  description: "Use this when the user wants to remove or delete a todo item",
  inputSchema: {
    type: "object",
    properties: {
      todoId: { type: "string", required: true }
    }
  }
}
```

**Widget - Todo List**:
```html
<div class="todo-dashboard">
  <div class="todo-header">
    <h3>Your Todos</h3>
    <span class="todo-count">{{total}} tasks</span>
  </div>

  <div class="todo-list">
    {{#each todos}}
    <div class="todo-item {{priority}}" data-id="{{id}}">
      <input type="checkbox" {{#if completed}}checked{{/if}}
             onchange="toggleTodo('{{id}}')">
      <div class="todo-content">
        <span class="todo-title">{{title}}</span>
        {{#if dueDate}}
        <span class="due-date">Due: {{dueDate}}</span>
        {{/if}}
      </div>
      <button class="delete-btn" onclick="deleteTodo('{{id}}')">×</button>
    </div>
    {{/each}}
  </div>

  <div class="todo-stats">
    <span>{{completed}} completed</span>
    <span>{{pending}} pending</span>
  </div>
</div>

<style>
  .todo-dashboard {
    background: white;
    border-radius: 12px;
    padding: 16px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  }

  .todo-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
  }

  .todo-count {
    background: #e5e7eb;
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 14px;
  }

  .todo-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px;
    margin: 8px 0;
    border-left: 3px solid #e5e7eb;
    background: #f9fafb;
    border-radius: 6px;
  }

  .todo-item.high {
    border-left-color: #ef4444;
  }

  .todo-item.medium {
    border-left-color: #f59e0b;
  }

  .todo-content {
    flex: 1;
  }

  .todo-title {
    display: block;
    font-weight: 500;
  }

  .due-date {
    font-size: 12px;
    color: #6b7280;
  }

  .delete-btn {
    background: none;
    border: none;
    font-size: 24px;
    color: #9ca3af;
    cursor: pointer;
  }

  .todo-stats {
    display: flex;
    justify-content: space-around;
    margin-top: 16px;
    padding-top: 16px;
    border-top: 1px solid #e5e7eb;
    font-size: 14px;
    color: #6b7280;
  }
</style>

<script>
  function toggleTodo(id) {
    // Send message to parent to complete todo
    window.parent.postMessage({
      type: 'tool_call',
      tool: 'complete_todo',
      args: { todoId: id }
    }, '*');
  }

  function deleteTodo(id) {
    if (confirm('Delete this todo?')) {
      window.parent.postMessage({
        type: 'tool_call',
        tool: 'delete_todo',
        args: { todoId: id }
      }, '*');
    }
  }
</script>
```

**Example Conversation**:
```
User: "Show me my todos"

ChatGPT: [Activates todo app]
[Displays todo dashboard widget with current tasks]

User: "Add 'Buy groceries' to my list"

ChatGPT: I've added "Buy groceries" to your todo list.
[Widget updates to show new item]

User: "Mark 'Email team' as done"

ChatGPT: Great! I've marked "Email team" as completed.
[Widget updates with checked item]
```

### Example 4: Code from GitHub Examples

OpenAI maintains an official examples repository at `github.com/openai/apps-sdk-examples` (hypothetical - check actual repo).

**Pizza Ordering App** (Pizzaz):
```typescript
// Simplified version of the Pizzaz demo
const tools = [
  {
    name: "browse_menu",
    description: "Use this when the user wants to see pizza options or browse the menu",
    handler: async () => {
      const menu = await fetchMenu();
      return {
        content: [
          { type: "text", text: "Here's our menu:" },
          {
            type: "resource",
            resource: {
              uri: "ui://widget/menu",
              mimeType: "text/html+skybridge",
              text: renderMenu(menu)
            }
          }
        ]
      };
    }
  },
  {
    name: "add_to_cart",
    description: "Use this when the user wants to order or add a pizza to their cart",
    handler: async ({ pizzaId, size, toppings }) => {
      const cart = await addToCart({ pizzaId, size, toppings });
      return {
        content: [
          { type: "text", text: `Added ${size} pizza to cart` },
          {
            type: "resource",
            resource: {
              uri: "ui://widget/cart",
              mimeType: "text/html+skybridge",
              text: renderCart(cart)
            }
          }
        ]
      };
    }
  },
  {
    name: "checkout",
    description: "Use this when the user wants to complete their order or checkout",
    handler: async ({ deliveryAddress, paymentMethod }, userContext) => {
      if (!userContext?.token) {
        return { requiresAuth: true };
      }

      const order = await processOrder({
        deliveryAddress,
        paymentMethod,
        userId: userContext.userId
      });

      return {
        content: [
          { type: "text", text: `Order confirmed! Estimated delivery: ${order.estimatedTime}` },
          {
            type: "resource",
            resource: {
              uri: "ui://widget/order_confirmation",
              mimeType: "text/html+skybridge",
              text: renderOrderConfirmation(order)
            }
          }
        ]
      };
    }
  }
];
```

---

## Platform Comparisons

### ChatGPT Apps SDK vs. ChatGPT Plugins

| Feature | Plugins (Deprecated) | Apps SDK |
|---------|---------------------|----------|
| **Launch Date** | March 2023 | October 2025 |
| **Status** | Being sunset | Active (preview) |
| **UI Capabilities** | Structured data only | Full HTML/CSS/JS widgets |
| **Discovery** | Plugin store + explicit install | Automatic contextual surfacing |
| **Protocol** | Proprietary API | MCP (open standard) |
| **OAuth** | OAuth 2.0 | OAuth 2.1 (more secure) |
| **User Experience** | Separate plugin interface | Inline in conversation |
| **Portability** | ChatGPT only | Any MCP-compatible platform |

**Migration Path**: OpenAI is encouraging plugin developers to rebuild as Apps SDK apps. No automatic migration—apps must be reimplemented.

### Apps SDK vs. Custom GPTs

| Feature | Custom GPTs | Apps SDK |
|---------|-------------|----------|
| **Purpose** | Specialized conversation agents | External service integration |
| **Configuration** | Instructions + knowledge files | Code (MCP server) |
| **UI Control** | None (text only) | Full custom widgets |
| **External Actions** | Limited (via Actions API) | Unlimited (via tools) |
| **Data Access** | Static knowledge base | Dynamic API calls |
| **Authentication** | None built-in | OAuth 2.1 |
| **Use Cases** | Specialized advisors, tutors | E-commerce, bookings, visualization |
| **Development** | No coding required | Requires programming |

**Complementary**: Custom GPTs and Apps can work together. A Custom GPT could use Apps SDK tools for specific actions.

### Apps SDK vs. Traditional Web Apps

| Feature | Web Apps | Apps SDK |
|---------|----------|----------|
| **Discovery** | Search, ads, word-of-mouth | AI-mediated contextual surfacing |
| **Interface** | Custom UI (full control) | Conversational + widget constraints |
| **Installation** | Download/signup friction | Zero friction (embedded) |
| **User Base** | Build from scratch | Instant access to 800M+ users |
| **Branding** | Full brand control | Within ChatGPT environment |
| **Monetization** | Direct (you control) | Through OpenAI (revenue share) |
| **Platform Risk** | Low (you own infrastructure) | High (dependent on OpenAI) |
| **Development** | Standard web stack | MCP + ChatGPT constraints |

**When to Choose Apps SDK**:
- You want massive distribution quickly
- Your service fits conversational UI
- Discovery is your biggest challenge
- You're willing to accept platform dependency

**When to Choose Traditional Web App**:
- You need full brand control
- Your UX requires complex interactions
- You want complete monetization control
- You prefer platform independence

### Apps SDK vs. Other AI Platforms

**Claude (Anthropic)**:
- Also supports MCP (same protocol!)
- Apps built for ChatGPT can work with Claude with minimal changes
- Smaller user base (~100M users estimated)
- Different strengths (longer context, better code understanding)

**Gemini (Google)**:
- No equivalent app platform announced yet (as of November 2025)
- Extensions exist but are Google-service only (Gmail, Drive, Maps)
- Potential future competition

**Microsoft Copilot**:
- Plugin system exists but more enterprise-focused
- Smaller consumer user base than ChatGPT
- Strong integration with Microsoft 365

**Competitive Advantage**: ChatGPT's Apps SDK currently has the largest consumer user base and most open developer ecosystem.

---

## Future Roadmap & Development

### Expected Late 2025 Launches

**App Directory Opening**:
- Public app store/directory interface
- Search and browse capabilities
- Featured apps section
- Category organization
- User reviews and ratings (expected)

**App Submission Process**:
- Developer portal for submissions
- Review process with approval timeline
- Design and functionality guidelines
- Privacy and security certification

**Monetization Framework**:
- Revenue sharing model (percentage TBD)
- Support for subscriptions
- Transaction-based pricing
- Instant checkout via Agentic Commerce Protocol

**Enterprise/Business/Education Rollout**:
- Admin controls for app management
- Custom app deployments for organizations
- Enhanced security and compliance features
- Analytics dashboards for enterprise apps

### 2026 and Beyond

**Regional Expansion**:
- EU/UK/Switzerland availability (requires regulatory approval)
- Localization support for apps
- Multi-language app interfaces
- Region-specific app recommendations

**Platform Maturation**:
- Improved discovery algorithms
- Better debugging tools
- Comprehensive analytics for developers
- A/B testing capabilities
- Enhanced widget frameworks

**Agentic Commerce Protocol**:
OpenAI has announced plans for this protocol, which will enable:
- Instant checkout without leaving ChatGPT
- Secure payment processing
- Order tracking
- Returns and customer service
- Multi-vendor marketplaces

**Example Future Flow**:
```
User: "Order pizza for tonight"
→ App finds restaurants
User: "The pepperoni from Tony's"
→ App adds to cart
User: "Check out"
→ Agentic Commerce Protocol processes payment instantly
→ No redirect, no external site, seamless transaction
```

**Advanced AI Capabilities**:
- Multi-modal inputs (voice, images within apps)
- Proactive app suggestions based on user patterns
- Cross-app workflows (apps collaborating automatically)
- Memory and personalization (apps remember user preferences)

**Developer Ecosystem Growth**:
- Third-party development tools and frameworks
- Testing and simulation environments
- Community-contributed libraries
- Educational resources and certifications

### Strategic Implications

**OpenAI's Platform Play**:
The Apps SDK represents OpenAI's attempt to position ChatGPT as more than a chatbot—it's becoming an operating system for AI-mediated tasks.

**Distribution Power**:
With 800M+ users, OpenAI has more leverage than traditional app stores. This could lead to:
- New business models (revenue share attractive due to volume)
- Shift in how people discover and use software
- Competition with Apple/Google app ecosystems

**MCP Ecosystem**:
If MCP gains adoption beyond OpenAI:
- Developers build once, deploy everywhere
- AI platforms compete on quality, not lock-in
- Healthier ecosystem than proprietary plugins

**Potential Challenges**:
- **Regulatory scrutiny**: EU AI Act, antitrust concerns
- **Privacy debates**: How much data does ChatGPT share with apps?
- **Monetization balance**: Will revenue share be attractive enough?
- **Quality control**: Can OpenAI prevent low-quality spam apps?

### Developer Recommendations

**Near Term (Nov 2025 - Q1 2026)**:
1. **Build and test** apps in Developer Mode
2. **Study launch partner** implementations
3. **Engage with community** to share learnings
4. **Prepare app package** for submission when directory opens
5. **Monitor announcements** for monetization details

**Medium Term (2026)**:
1. **Launch on app directory** as soon as submissions open
2. **Iterate based on analytics** and user feedback
3. **Expand feature set** as platform matures
4. **Consider multi-platform** (Claude, other MCP adopters)
5. **Build user base** before competition intensifies

**Long Term (2027+)**:
1. **Optimize for Agentic Commerce** if relevant to your service
2. **Leverage cross-app workflows** for competitive advantage
3. **Invest in AI-native UX** patterns that emerge
4. **Consider enterprise offerings** for B2B opportunities

---

## Resources & References

### Official Documentation

- **OpenAI Apps SDK Docs**: `developers.openai.com/apps-sdk` (primary resource)
- **MCP Specification**: `modelcontextprotocol.io`
- **OpenAI DevDay 2025 Keynote**: Video announcement and demos
- **Developer Forum**: `community.openai.com/c/apps-sdk`

### Code Examples

- **Official Examples Repo**: `github.com/openai/apps-sdk-examples` (hypothetical)
- **MCP SDK (TypeScript)**: `npmjs.com/package/@anthropic-ai/sdk-mcp`
- **MCP SDK (Python)**: `pypi.org/project/anthropic-mcp`

### Community Resources

- **The New Stack**: "Building Your First ChatGPT App" tutorial
- **Medium**: Various developer experience articles
- **BoldDesk**: Implementation guide with screenshots
- **Render Blog**: Deployment guide for MCP servers

### Developer Tools

- **ngrok**: `ngrok.com` - Expose localhost for testing
- **Postman**: API testing for OAuth flows
- **Cursor IDE**: AI-assisted development (mentioned in community)
- **VS Code MCP Extension**: Debugging support (if available)

### Monitoring & Analytics

- **Sentry**: Error tracking for production apps
- **LogRocket**: Session replay for widget debugging
- **DataDog**: Infrastructure monitoring
- (Note: OpenAI may provide native analytics when directory launches)

### Related Technologies

- **FastMCP**: Rapid MCP server development framework
- **Skybridge**: Widget rendering system (part of Apps SDK)
- **OAuth 2.1 Spec**: `oauth.net/2.1/` - Latest OAuth standard

### Stay Updated

- **OpenAI Blog**: `openai.com/blog`
- **OpenAI Twitter**: `@OpenAI`
- **Developer Newsletter**: Subscribe at developer portal
- **Community Discord**: (Check official forum for invite)

---

## Conclusion

The OpenAI Apps SDK, launched in October 2025, represents a significant shift in how users interact with software. By embedding applications directly into ChatGPT conversations and enabling natural language as the primary interface, OpenAI is pioneering a new paradigm for software distribution and usage.

**Key Takeaways**:

1. **Massive Opportunity**: Access to 800M+ users is unprecedented for developers
2. **Very Early Stage**: At just one month old, the platform is still maturing
3. **MCP Foundation**: Open standard reduces lock-in risk and enables portability
4. **Conversational UX**: Success requires rethinking app design for natural language
5. **Platform Dependency**: Developers trade control for distribution
6. **Monetization TBD**: Business model details expected late 2025
7. **Regulatory Uncertainty**: EU/UK restrictions may expand or restrict further

**Who Should Build on Apps SDK**:

- Developers seeking massive distribution quickly
- Services that fit conversational interfaces (booking, search, recommendations)
- Companies wanting to experiment with AI-native UX
- Startups comfortable with platform risk for potential high reward

**Who Should Wait**:

- Those needing full brand control and custom UX
- Services requiring complex interactions unsuited to conversation
- Developers in restricted regions (EU/UK/Switzerland)
- Anyone uncomfortable with unclear monetization terms

The Apps SDK is poised to either become the next major app platform or a bold experiment in AI-mediated software. Given OpenAI's user base and resources, it's worth taking seriously—but given its infancy, proceed with measured expectations and diversified distribution strategies.

---

*This guide will be updated as the platform evolves. Check back for the latest information.*

**Version**: 1.0
**Last Updated**: November 10, 2025
**Word Count**: ~12,000 words