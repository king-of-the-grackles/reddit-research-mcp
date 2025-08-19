# Working with PRAW's Models

This section provides comprehensive documentation for all PRAW model classes. Each model represents a different Reddit entity (comments, submissions, subreddits, etc.) and includes detailed API references with methods, properties, and usage examples.

## Core Models

### Content Models
- **[Comment](models/comment.md)** - Represents Reddit comments with methods for replying, editing, voting, and moderation
- **[Submission](models/submission.md)** - Represents Reddit posts/submissions with comprehensive interaction capabilities
- **[MoreComments](models/more-comments.md)** - Handles expanding collapsed comment trees

### Community Models
- **[Subreddit](models/subreddit.md)** - Complete subreddit management including posts, moderation, settings, and wikis
- **[Multireddit](models/multireddit.md)** - Custom feeds combining multiple subreddits
- **[WikiPage](models/wikipage.md)** - Subreddit wiki page management

### User Models
- **[Redditor](models/redditor.md)** - Reddit user accounts with profile data, submissions, comments, and messaging
- **[Message](models/message.md)** - Private messages between users

### Live Content Models
- **[LiveThread](models/livethread.md)** - Real-time event coverage threads
- **[LiveUpdate](models/liveupdate.md)** - Individual updates within live threads

### Moderation Models
- **[ModmailConversation](models/modmailconversation.md)** - Modmail conversations and moderation communication
- **[Draft](models/draft.md)** - Draft posts saved for later submission

## Quick Reference

Each model documentation includes:
- **Class definition** with constructor parameters
- **Typical attributes** available on instances
- **Methods** with signatures and examples
- **Usage patterns** and best practices

For general usage patterns and examples, see the [Quick Start Guide](../getting-started/quick-start.md).