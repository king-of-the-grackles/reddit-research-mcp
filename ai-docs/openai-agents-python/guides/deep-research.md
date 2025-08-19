# OpenAI Deep Research Guide

## Introduction

Deep research is OpenAI's agentic capability that conducts multi-step research on the internet for complex tasks. It accomplishes in tens of minutes what would take a human many hours.

Deep research can find, analyze, and synthesize hundreds of online sources to create a comprehensive report at the level of a research analyst. Powered by a version of the upcoming OpenAI o3 model that's optimized for web browsing and data analysis, it leverages reasoning to search, interpret, and analyze massive amounts of text, images, and PDFs on the internet, pivoting as needed in reaction to information it encounters.

The ability to synthesize knowledge is a prerequisite for creating new knowledge. For this reason, deep research marks a significant step toward OpenAI's broader goal of developing AGI, which they have long envisioned as capable of producing novel scientific research.

## Why Deep Research Was Built

Deep research is built for people who do intensive knowledge work in areas like finance, science, policy, and engineering and need thorough, precise, and reliable research. It can be equally useful for discerning shoppers looking for hyper-personalized recommendations on purchases that typically require careful research, like cars, appliances, and furniture. 

Every output is fully documented, with clear citations and a summary of its thinking, making it easy to reference and verify the information. It is particularly effective at finding niche, non-intuitive information that would require browsing numerous websites. Deep research frees up valuable time by allowing you to offload and expedite complex, time-intensive web research with just one query.

Deep research independently discovers, reasons about, and consolidates insights from across the web. To accomplish this, it was trained on real-world tasks requiring browser and Python tool use, using the same reinforcement learning methods behind OpenAI o1, their first reasoning model.

## How to Use Deep Research

### Getting Started

1. In ChatGPT, select 'deep research' in the message composer
2. Enter your query
3. Tell ChatGPT what you need—whether it's a competitive analysis on streaming platforms or a personalized report on the best commuter bike
4. You can attach files or spreadsheets to add context to your question
5. Once it starts running, a sidebar appears with a summary of the steps taken and sources used

### Execution Process

- Deep research may take anywhere from 5 to 30 minutes to complete its work, taking the time needed to dive deep into the web
- In the meantime, you can step away or work on other tasks—you'll get a notification once the research is complete
- The final output arrives as a report within the chat
- In the next few weeks, OpenAI will also be adding embedded images, data visualizations, and other analytic outputs in these reports for additional clarity and context

### When to Use Deep Research vs GPT-4o

- **GPT-4o**: Ideal for real-time, multimodal conversations
- **Deep Research**: For multi-faceted, domain-specific inquiries where depth and detail are critical, deep research's ability to conduct extensive exploration and cite each claim is the difference between a quick summary and a well-documented, verified answer that can be usable as a work product

## How It Works

Deep research was trained using end-to-end reinforcement learning on hard browsing and reasoning tasks across a range of domains. Through that training, it learned to:

- Plan and execute a multi-step trajectory to find the data it needs
- Backtrack and react to real-time information where necessary
- Browse over user uploaded files
- Plot and iterate on graphs using the Python tool
- Embed both generated graphs and images from websites in its responses
- Cite specific sentences or passages from its sources

As a result of this training, it reaches new highs on a number of public evaluations focused on real-world problems.

## Performance Benchmarks

### Humanity's Last Exam

On Humanity's Last Exam, a recently released evaluation that tests AI across a broad range of subjects on expert-level questions, the model powering deep research scores a new high at 26.6% accuracy. This test consists of over 3,000 multiple choice and short answer questions across more than 100 subjects from linguistics to rocket science, classics to ecology.

Compared to OpenAI o1, the largest gains appeared in chemistry, humanities and social sciences, and mathematics. The model powering deep research showcased a human-like approach by effectively seeking out specialized information when necessary.

| Model | Accuracy (%) |
|-------|-------------|
| GPT-4o | 3.3 |
| Grok-2 | 3.8 |
| Claude 3.5 Sonnet | 4.3 |
| Gemini Thinking | 6.2 |
| OpenAI o1 | 9.1 |
| DeepSeek-R1* | 9.4 |
| OpenAI o3-mini (medium)* | 10.5 |
| OpenAI o3-mini (high)* | 13.0 |
| OpenAI deep research** | 26.6 |

\* Model is not multi-modal, evaluated on text-only subset.
\*\*with browsing + python tools

### GAIA Benchmark

On GAIA, a public benchmark that evaluates AI on real-world questions, the model powering deep research reaches a new state of the art (SOTA), topping the external leaderboard. Encompassing questions across three levels of difficulty, successful completion of these tasks requires abilities including reasoning, multi-modal fluency, web browsing, and tool-use proficiency.

| GAIA | Level 1 | Level 2 | Level 3 | Avg. |
|------|---------|---------|---------|------|
| Previous SOTA | 67.92 | 67.44 | 42.31 | 63.64 |
| Deep Research (pass@1) | 74.29 | 69.06 | 47.6 | 67.36 |
| Deep Research (cons@64) | 78.66 | 73.21 | 58.03 | 72.57 |

### Expert-Level Tasks

In an internal evaluation of expert-level tasks across a range of areas, deep research was rated by domain experts to have automated multiple hours of difficult, manual investigation.

The more the model browses and thinks about what it's browsing, the better it does, which is why giving it time to think is important. Pass rate improves with increasing max tool calls.

Estimated economic value of task is more correlated with pass rate than number of hours it would take a human – the things that models find difficult are different to what humans find time-consuming.

## Limitations

Deep research unlocks significant new capabilities, but it's still early and has limitations:

- It can sometimes hallucinate facts in responses or make incorrect inferences, though at a notably lower rate than existing ChatGPT models, according to internal evaluations
- It may struggle with distinguishing authoritative information from rumors
- Currently shows weakness in confidence calibration, often failing to convey uncertainty accurately
- At launch, there may be minor formatting errors in reports and citations
- Tasks may take longer to kick off
- OpenAI expects all these issues to quickly improve with more usage and time

## Access and Availability

### Current Access

Deep research in ChatGPT is currently very compute intensive. The longer it takes to research a query, the more inference compute is required.

**Access Tiers:**
- **Pro users**: Available today with up to 100 queries per month (initially), now 250 queries per month
- **Plus and Team users**: 25 queries per month
- **Enterprise and Edu users**: 25 queries per month
- **Free users**: 5 queries per month

### Lightweight Version

As of April 24, 2025: OpenAI is significantly increasing how often you can use deep research through a new lightweight version powered by a version of o4-mini, designed to be more cost-efficient while preserving high quality. Once you reach your limit for the full version, your queries will automatically switch to the lightweight version.

### Geographic Availability

- Initially available in select countries
- As of February 5, 2025: Available to Pro users in the United Kingdom, Switzerland, and the European Economic Area
- As of February 25, 2025: Available to all Plus users

### Platform Support

- Available today on ChatGPT web
- Will be rolled out to mobile and desktop apps within the month

## Future Developments

### Near-term Improvements

- Embedded images in reports
- Data visualizations
- Other analytic outputs for additional clarity and context
- Connection to more specialized data sources
- Access to subscription-based or internal resources

### Long-term Vision

Looking further ahead, OpenAI envisions agentic experiences coming together in ChatGPT for asynchronous, real-world research and execution. The combination of deep research, which can perform asynchronous online investigation, and Operator, which can take real-world action, will enable ChatGPT to carry out increasingly sophisticated tasks for users.

## Agent Mode Update (July 17, 2025)

Deep research can now go even deeper and broader with access to a visual browser as part of ChatGPT agent. To access these updated capabilities:
1. Select "agent mode" from the dropdown in the composer
2. Enter your query directly

The original deep research functionality remains available via the "deep research" option in the tools menu.

## Data Sources and Privacy

### Available Data Sources

By default, Deep Research can access:
- The open web
- Any files you upload
- Connected supported apps (when relevant and permitted)

### Data Handling

- Deep Research follows the same data handling and privacy settings as ChatGPT
- You can manage retention and training preferences in your data controls
- Results remain in your conversation history unless you delete the chat
- Deleting the chat also deletes associated Deep Research outputs

## Best Practices

### When to Use Deep Research

Use Deep Research for:
- Multi-step or in-depth questions that require aggregation and synthesis across multiple sources
- Complex research tasks in finance, science, policy, and engineering
- Hyper-personalized recommendations on purchases requiring careful research
- Tasks that would typically require hours of manual research

### When Not to Use Deep Research

For quick lookups or short conversations, standard chat or Search may be faster. If you see "Get a quick answer", that's a sign your query may not require Deep Research.

### Search vs Deep Research

- **Search**: Quickly pulls recent web information and returns a short summary with links
- **Deep Research**: Takes more time to read and analyze many sources, then produces a detailed, documented report

Use Search for quick facts; use Deep Research for depth and thoroughness.

## Safety and Governance

OpenAI conducted rigorous safety testing, preparedness evaluations, and governance reviews on the early version of o3 that powers deep research, identifying it as Medium risk. They also ran additional safety testing to better understand incremental risks associated with deep research's ability to browse the web, and have added new mitigations. OpenAI will continue to thoroughly test and closely monitor the current limited release and will share safety insights and safeguards for deep research in a system card when they widen access to Plus users.

## Technical Details

### Model Architecture

- Powered by a version of the upcoming OpenAI o3 model
- Optimized for web browsing and data analysis
- Uses reasoning to search, interpret, and analyze content
- Trained using the same reinforcement learning methods behind OpenAI o1

### Capabilities

- Multi-modal processing (text, images, PDFs)
- Dynamic pivoting based on encountered information
- Python tool use for data analysis
- Browser tool use for web research
- Citation and source tracking

### Training Methodology

- End-to-end reinforcement learning
- Trained on real-world tasks requiring browser and Python tool use
- Focus on hard browsing and reasoning tasks across diverse domains
- Learned to plan and execute multi-step trajectories
- Developed ability to backtrack and adapt to real-time information

## Conclusion

Deep research represents a significant advancement in AI-assisted research capabilities, bridging the gap between quick information retrieval and comprehensive, human-level research analysis. It demonstrates OpenAI's progress toward developing AGI capable of producing novel scientific research, while providing immediate practical value for knowledge workers, researchers, and anyone needing thorough, well-documented research on complex topics.