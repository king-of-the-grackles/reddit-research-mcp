# ModmailConversation

_class_ praw.models.reddit.modmail.ModmailConversation( _reddit:[praw.Reddit](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit")_, _id:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_, _mark\_read:[bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.11)")=False_, _\_data:[Dict](https://docs.python.org/3/library/typing.html#typing.Dict "(in Python v3.11)")\[ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)"), [Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")\]\| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_)

A class for modmail conversations.

**Typical Attributes**

Note: This table describes attributes that typically belong to objects of this class. PRAW
dynamically provides the attributes that Reddit returns via the API. Since those
attributes are subject to change on Reddit's end, PRAW makes no effort to document
any new/removed/changed attributes, other than to instruct you on how to discover
what is available. As a result, this table of attributes may not be complete. See
[Determine Available Attributes of an Object](https://praw.readthedocs.io/en/stable/getting_started/quick_start.html#determine-available-attributes-of-an-object) for detailed information.

If you would like to add an attribute to this table, feel free to open a [pull request](https://github.com/praw-dev/praw/pulls).

| Attribute | Description |
| --- | --- |
| `authors` | Provides an ordered list of [`Redditor`](https://praw.readthedocs.io/en/stable/code_overview/models/redditor.html#praw.models.Redditor "praw.models.Redditor") instances. The authors of each message in the modmail conversation. |
| `id` | The ID of the [`ModmailConversation`](https://praw.readthedocs.io/en/stable/code_overview/models/modmailconversation.html#praw.models.reddit.modmail.ModmailConversation "praw.models.reddit.modmail.ModmailConversation"). |
| `is_highlighted` | Whether or not the [`ModmailConversation`](https://praw.readthedocs.io/en/stable/code_overview/models/modmailconversation.html#praw.models.reddit.modmail.ModmailConversation "praw.models.reddit.modmail.ModmailConversation") is highlighted. |
| `is_internal` | Whether or not the [`ModmailConversation`](https://praw.readthedocs.io/en/stable/code_overview/models/modmailconversation.html#praw.models.reddit.modmail.ModmailConversation "praw.models.reddit.modmail.ModmailConversation") is a private mod conversation. |
| `last_mod_update` | Time of the last mod message reply, represented in the [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) standard with timezone. |
| `last_updated` | Time of the last message reply, represented in the [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) standard with timezone. |
| `last_user_update` | Time of the last user message reply, represented in the [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) standard with timezone. |
| `num_messages` | The number of messages in the [`ModmailConversation`](https://praw.readthedocs.io/en/stable/code_overview/models/modmailconversation.html#praw.models.reddit.modmail.ModmailConversation "praw.models.reddit.modmail.ModmailConversation"). |
| `obj_ids` | Provides a list of dictionaries representing mod actions on the [`ModmailConversation`](https://praw.readthedocs.io/en/stable/code_overview/models/modmailconversation.html#praw.models.reddit.modmail.ModmailConversation "praw.models.reddit.modmail.ModmailConversation"). Each dict contains attributes of `"key"` and `"id"`. The key can be either `""messages"` or `"ModAction"`. `"ModAction"` represents archiving/highlighting etc. |
| `owner` | Provides an instance of [`Subreddit`](https://praw.readthedocs.io/en/stable/code_overview/models/subreddit.html#praw.models.Subreddit "praw.models.Subreddit"). The subreddit that the [`ModmailConversation`](https://praw.readthedocs.io/en/stable/code_overview/models/modmailconversation.html#praw.models.reddit.modmail.ModmailConversation "praw.models.reddit.modmail.ModmailConversation") belongs to. |
| `participant` | Provides an instance of [`Redditor`](https://praw.readthedocs.io/en/stable/code_overview/models/redditor.html#praw.models.Redditor "praw.models.Redditor"). The participating user in the [`ModmailConversation`](https://praw.readthedocs.io/en/stable/code_overview/models/modmailconversation.html#praw.models.reddit.modmail.ModmailConversation "praw.models.reddit.modmail.ModmailConversation"). |
| `subject` | The subject of the [`ModmailConversation`](https://praw.readthedocs.io/en/stable/code_overview/models/modmailconversation.html#praw.models.reddit.modmail.ModmailConversation "praw.models.reddit.modmail.ModmailConversation"). |

## Methods

### \_\_init\_\_( _reddit:[praw.Reddit](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit")_, _id:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_, _mark\_read:[bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.11)")=False_, _\_data:[Dict](https://docs.python.org/3/library/typing.html#typing.Dict "(in Python v3.11)")\[ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)"), [Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")\]\| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_)

Initialize a [`ModmailConversation`](https://praw.readthedocs.io/en/stable/code_overview/models/modmailconversation.html#praw.models.reddit.modmail.ModmailConversation "praw.models.reddit.modmail.ModmailConversation") instance.

Parameters:
- **mark\_read** – If `True`, conversation is marked as read (default: `False`).

### archive()

Archive the conversation.

For example:

```python
reddit.subreddit("test").modmail("2gmz").archive()
```

### highlight()

Highlight the conversation.

For example:

```python
reddit.subreddit("test").modmail("2gmz").highlight()
```

### mute( _\*_, _num\_days=3_)

Mute the non-mod user associated with the conversation.

Parameters:
- **num\_days** – Duration of mute in days. Valid options are `3`, `7`, or `28` (default: `3`).

For example:

```python
reddit.subreddit("test").modmail("2gmz").mute()
```

To mute for 7 days:

```python
reddit.subreddit("test").modmail("2gmz").mute(num_days=7)
```

### _classmethod_ parse( _data:[Dict](https://docs.python.org/3/library/typing.html#typing.Dict "(in Python v3.11)")\[ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)"), [Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")\]_, _reddit:[praw.Reddit](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit")_, _convert\_objects:[bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.11)")=True_)

Return an instance of [`ModmailConversation`](https://praw.readthedocs.io/en/stable/code_overview/models/modmailconversation.html#praw.models.reddit.modmail.ModmailConversation "praw.models.reddit.modmail.ModmailConversation") from `data`.

Parameters:
- **data** – The structured data.
- **reddit** – An instance of [`Reddit`](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit").
- **convert\_objects** – If `True`, convert message and mod action data into objects (default: `True`).

### read( _\*_, _other\_conversations:[List](https://docs.python.org/3/library/typing.html#typing.List "(in Python v3.11)")\[ [ModmailConversation](https://praw.readthedocs.io/en/stable/code_overview/models/modmailconversation.html#praw.models.reddit.modmail.ModmailConversation "praw.models.reddit.modmail.ModmailConversation")\]\| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_)

Mark the conversation(s) as read.

Parameters:
- **other\_conversations** – A list of other conversations to mark (default: `None`).

For example, to mark the conversation as read along with other recent
conversations from the same user:

```python
subreddit = reddit.subreddit("test")
conversation = subreddit.modmail.conversation("2gmz")
conversation.read(other_conversations=conversation.user.recent_convos)
```

### reply( _\*_, _author\_hidden:[bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.11)")=False_, _body:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_, _internal:[bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.11)")=False_)→[ModmailMessage](https://praw.readthedocs.io/en/stable/code_overview/other/modmailmessage.html#praw.models.ModmailMessage "praw.models.reddit.modmail.ModmailMessage")

Reply to the conversation.

Parameters:
- **author\_hidden** – When `True`, author is hidden from non-moderators (default: `False`).
- **body** – The Markdown formatted content for a message.
- **internal** – When `True`, message is a private moderator note, hidden from non-moderators (default: `False`).

Returns: A [`ModmailMessage`](https://praw.readthedocs.io/en/stable/code_overview/other/modmailmessage.html#praw.models.ModmailMessage "praw.models.reddit.modmail.ModmailMessage") object for the newly created message.

For example, to reply to the non-mod user while hiding your username:

```python
conversation = reddit.subreddit("test").modmail("2gmz")
conversation.reply(body="Message body", author_hidden=True)
```

To create a private moderator note on the conversation:

```python
conversation.reply(body="Message body", internal=True)
```

### unarchive()

Unarchive the conversation.

For example:

```python
reddit.subreddit("test").modmail("2gmz").unarchive()
```

### unhighlight()

Un-highlight the conversation.

For example:

```python
reddit.subreddit("test").modmail("2gmz").unhighlight()
```

### unmute()

Unmute the non-mod user associated with the conversation.

For example:

```python
reddit.subreddit("test").modmail("2gmz").unmute()
```

### unread( _\*_, _other\_conversations:[List](https://docs.python.org/3/library/typing.html#typing.List "(in Python v3.11)")\[ [ModmailConversation](https://praw.readthedocs.io/en/stable/code_overview/models/modmailconversation.html#praw.models.reddit.modmail.ModmailConversation "praw.models.reddit.modmail.ModmailConversation")\]\| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_)

Mark the conversation(s) as unread.

Parameters:
- **other\_conversations** – A list of other conversations to mark (default: `None`).

For example, to mark the conversation as unread along with other recent
conversations from the same user:

```python
subreddit = reddit.subreddit("test")
conversation = subreddit.modmail.conversation("2gmz")
conversation.unread(other_conversations=conversation.user.recent_convos)
```