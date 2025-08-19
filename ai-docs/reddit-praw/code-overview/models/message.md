# Message

_class_ praw.models.Message(_reddit: praw.Reddit_, _\_data: Dict[str, Any]_)

A class for private messages.

## Typical Attributes

> **Note:** This table describes attributes that typically belong to objects of this class. PRAW dynamically provides the attributes that Reddit returns via the API. Since those attributes are subject to change on Reddit's end, PRAW makes no effort to document any new/removed/changed attributes, other than to instruct you on how to discover what is available. As a result, this table of attributes may not be complete. See [Determine Available Attributes of an Object](../../getting-started/quick-start.md#determine-available-attributes-of-an-object) for detailed information.

| Attribute | Description |
| --- | --- |
| `author` | Provides an instance of `Redditor`. |
| `body` | The body of the message, as Markdown. |
| `body_html` | The body of the message, as HTML. |
| `created_utc` | Time the message was created, represented in [Unix Time](https://en.wikipedia.org/wiki/Unix_time). |
| `dest` | Provides an instance of `Redditor`. The recipient of the message. |
| `id` | The ID of the message. |
| `name` | The full ID of the message, prefixed with `t4_`. |
| `subject` | The subject of the message. |
| `was_comment` | Whether or not the message was a comment reply. |

## Methods

### \_\_init\_\_(_reddit: praw.Reddit_, _\_data: Dict[str, Any]_)

Initialize a `Message` instance.

### block()

Block the user who sent the item.

> **Note:** This method pertains only to objects which were retrieved via the inbox.

Example usage:

```python
comment = reddit.comment("dkk4qjd")
comment.block()

# or, identically:

comment.author.block()
```

### collapse()

Mark the item as collapsed.

> **Note:** This method pertains only to objects which were retrieved via the inbox.

Example usage:

```python
inbox = reddit.inbox()

# select first inbox item and collapse it
message = next(inbox)
message.collapse()
```

See also: `uncollapse()`

### delete()

Delete the message.

> **Note:** Reddit does not return an indication of whether or not the message was successfully deleted.

For example, to delete the most recent message in your inbox:

```python
next(reddit.inbox.all()).delete()
```

### _property_ fullname _: str_

Return the object's fullname.

A fullname is an object's kind mapping like `t3` followed by an underscore and the object's base36 ID, e.g., `t1_c5s96e0`.

### mark_read()

Mark a single inbox item as read.

> **Note:** This method pertains only to objects which were retrieved via the inbox.

Example usage:

```python
inbox = reddit.inbox.unread()

for message in inbox:
    # process unread messages
    ...
```

See also: `mark_unread()`

To mark the whole inbox as read with a single network request, use `Inbox.mark_all_read()`

### mark_unread()

Mark the item as unread.

> **Note:** This method pertains only to objects which were retrieved via the inbox.

Example usage:

```python
inbox = reddit.inbox(limit=10)

for message in inbox:
    # process messages
    ...
```

See also: `mark_read()`

### _property_ parent _: praw.models.Message | None_

Return the parent of the message if it exists.

### _classmethod_ parse(_data: Dict[str, Any]_, _reddit: praw.Reddit_)

Return an instance of `Message` or `SubredditMessage` from `data`.

Parameters:
- **data** – The structured data.
- **reddit** – An instance of `Reddit`.

### reply(_body: str_) → praw.models.Comment | praw.models.Message | None

Reply to the object.

Parameters:
- **body** – The Markdown formatted content for a comment.

Returns:
- A `Comment` or `Message` object for the newly created comment or message or `None` if Reddit doesn't provide one.

Raises:
- `prawcore.exceptions.Forbidden` when attempting to reply to some items, such as locked submissions/comments or non-replyable messages.

A `None` value can be returned if the target is a comment or submission in a quarantined subreddit and the authenticated user has not opt-ed into viewing the content. When this happens the comment will be successfully created on Reddit and can be retried by drawing the comment from the user's comment history.

Example usage:

```python
submission = reddit.submission("5or86n")
submission.reply("reply")

comment = reddit.comment("dxolpyc")
comment.reply("reply")
```

### unblock_subreddit()

Unblock a subreddit.

> **Note:** This method pertains only to objects which were retrieved via the inbox.

For example, to unblock all blocked subreddits that you can find by going through your inbox:

```python
from praw.models import SubredditMessage

subs = set()
for item in reddit.inbox.messages(limit=None):
    if isinstance(item, SubredditMessage):
        if (
            item.subject == "[message from blocked subreddit]"
            and str(item.subreddit) not in subs
        ):
            item.unblock_subreddit()
            subs.add(str(item.subreddit))
```

### uncollapse()

Mark the item as uncollapsed.

> **Note:** This method pertains only to objects which were retrieved via the inbox.

Example usage:

```python
inbox = reddit.inbox()

# select first inbox item and uncollapse it
message = next(inbox)
message.uncollapse()
```

See also: `collapse()`