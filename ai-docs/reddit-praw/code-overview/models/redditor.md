# Redditor

_class_ praw.models.Redditor( _reddit:[praw.Reddit](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit")_, _name:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_, _fullname:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_, _\_data:[Dict](https://docs.python.org/3/library/typing.html#typing.Dict "(in Python v3.11)")\[ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)"), [Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")\]\| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_)

A class for Reddit users.

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
| `comment_karma` | The comment karma for the Redditor. |
| `created_utc` | Time the account was created, represented in [Unix Time](https://en.wikipedia.org/wiki/Unix_time). |
| `has_verified_email` | Whether or not the Redditor has verified their email. |
| `icon_img` | The url of the Redditors's avatar. |
| `id` | The ID of the Redditor. |
| `is_employee` | Whether or not the Redditor is a Reddit employee. |
| `is_friend` | Whether or not the Redditor is friends with the authenticated user. |
| `is_mod` | Whether or not the Redditor moderates a subreddit. |
| `is_gold` | Whether or not the Redditor has active Reddit Premium status. |
| `link_karma` | The link karma for the Redditor. |
| `name` | The Redditor's username. |

## Key Methods

### block()
Block the Redditor.

Example usage:
```python
redditor.block()
```

### unblock()
Unblock the Redditor.

Example usage:
```python
redditor.unblock()
```

### friend( _note:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_)
Friend the Redditor.

Parameters:
- **note** – A note to save along with the relationship. Requires Reddit Premium (default: None).

Example usage:
```python
redditor.friend()
redditor.friend(note="My favorite redditor")
```

### message( _subject:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_, _message:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_, _from\_subreddit:[praw.models.Subreddit](https://praw.readthedocs.io/en/stable/code_overview/models/subreddit.html#praw.models.Subreddit "praw.models.Subreddit") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_)
Send a message to the Redditor.

Parameters:
- **subject** – The subject of the message.
- **message** – The message content.
- **from\_subreddit** – A [`Subreddit`](https://praw.readthedocs.io/en/stable/code_overview/models/subreddit.html#praw.models.Subreddit "praw.models.Subreddit") instance to send the message on behalf of. The authenticated user must be a moderator of the provided Subreddit.

Example usage:
```python
redditor.message("Subject", "Hello!")
```

### stream()
Provide an instance of [`RedditorStream`](https://praw.readthedocs.io/en/stable/code_overview/other/redditorstream.html#praw.models.reddit.redditor.RedditorStream "praw.models.reddit.redditor.RedditorStream").

Example usage:
```python
for comment in redditor.stream.comments():
    print(comment.body)
```

### comments()
Provide an instance of [`RedditorListingMixin`](https://praw.readthedocs.io/en/stable/code_overview/other/redditorlistingmixin.html#praw.models.listing.mixins.redditor.RedditorListingMixin "praw.models.listing.mixins.redditor.RedditorListingMixin").

Example usage:
```python
for comment in redditor.comments.new(limit=10):
    print(comment.body)
```

### submissions()
Provide an instance of [`RedditorListingMixin`](https://praw.readthedocs.io/en/stable/code_overview/other/redditorlistingmixin.html#praw.models.listing.mixins.redditor.RedditorListingMixin "praw.models.listing.mixins.redditor.RedditorListingMixin").

Example usage:
```python
for submission in redditor.submissions.new(limit=10):
    print(submission.title)
```

### hot( _\*\*generator\_kwargs_)→[Iterator](https://docs.python.org/3/library/typing.html#typing.Iterator "(in Python v3.11)")\[ [Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")\]
Return a [`ListingGenerator`](https://praw.readthedocs.io/en/stable/code_overview/other/listinggenerator.html#praw.models.ListingGenerator "praw.models.ListingGenerator") for hot items.

Example usage:
```python
for item in redditor.hot(limit=10):
    print(item)
```

### new( _\*\*generator\_kwargs_)→[Iterator](https://docs.python.org/3/library/typing.html#typing.Iterator "(in Python v3.11)")\[ [Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")\]
Return a [`ListingGenerator`](https://praw.readthedocs.io/en/stable/code_overview/other/listinggenerator.html#praw.models.ListingGenerator "praw.models.ListingGenerator") for new items.

Example usage:
```python
for item in redditor.new(limit=10):
    print(item)
```

### top( _\*_, _time\_filter:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")='all'_, _\*\*generator\_kwargs_)→[Iterator](https://docs.python.org/3/library/typing.html#typing.Iterator "(in Python v3.11)")\[ [Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")\]
Return a [`ListingGenerator`](https://praw.readthedocs.io/en/stable/code_overview/other/listinggenerator.html#praw.models.ListingGenerator "praw.models.ListingGenerator") for top items.

Parameters:
- **time\_filter** – Can be one of: `"all"`, `"day"`, `"hour"`, `"month"`, `"week"`, or `"year"` (default: `"all"`).

Example usage:
```python
for item in redditor.top(time_filter="week", limit=5):
    print(item)
```

### controversial( _\*_, _time\_filter:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")='all'_, _\*\*generator\_kwargs_)→[Iterator](https://docs.python.org/3/library/typing.html#typing.Iterator "(in Python v3.11)")\[ [Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")\]
Return a [`ListingGenerator`](https://praw.readthedocs.io/en/stable/code_overview/other/listinggenerator.html#praw.models.ListingGenerator "praw.models.ListingGenerator") for controversial items.

Parameters:
- **time\_filter** – Can be one of: `"all"`, `"day"`, `"hour"`, `"month"`, `"week"`, or `"year"` (default: `"all"`).

Example usage:
```python
for item in redditor.controversial(time_filter="day", limit=5):
    print(item)
```

### unfriend()
Unfriend the Redditor.

Example usage:
```python
redditor.unfriend()
```

### _property_ fullname _: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_
Return the Redditor's fullname.

A Redditor's fullname is their kind mapping, `t2_`, followed by their base36 ID, e.g., t2_1ef5e.

Example usage:
```python
print(redditor.fullname)
```

Note: This is a condensed version of the Redditor class documentation. The full documentation contains many more methods and detailed explanations. For complete information, visit the original PRAW documentation.