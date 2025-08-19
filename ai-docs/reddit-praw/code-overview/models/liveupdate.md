# LiveUpdate

_class_ praw.models.LiveUpdate( _reddit:[praw.Reddit](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit")_, _thread\_id:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_, _update\_id:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_, _\_data:[Dict](https://docs.python.org/3/library/typing.html#typing.Dict "(in Python v3.11)")\[ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)"), [Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")\]\| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_)

An individual [`LiveUpdate`](https://praw.readthedocs.io/en/stable/code_overview/models/liveupdate.html#praw.models.LiveUpdate "praw.models.LiveUpdate") object.

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
| `author` | The [`Redditor`](https://praw.readthedocs.io/en/stable/code_overview/models/redditor.html#praw.models.Redditor "praw.models.Redditor") who made the update. |
| `body` | Body of the update, as Markdown. |
| `body_html` | Body of the update, as HTML. |
| `created_utc` | The time the update was created, as [Unix Time](https://en.wikipedia.org/wiki/Unix_time). |
| `stricken` | A `bool` representing whether or not the update was stricken (see [`strike()`](https://praw.readthedocs.io/en/stable/code_overview/other/liveupdatecontribution.html#praw.models.reddit.live.LiveUpdateContribution.strike "praw.models.reddit.live.LiveUpdateContribution.strike")). |

## Methods

### \_\_init\_\_( _reddit:[praw.Reddit](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit")_, _thread\_id:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_, _update\_id:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_, _\_data:[Dict](https://docs.python.org/3/library/typing.html#typing.Dict "(in Python v3.11)")\[ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)"), [Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")\]\| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_)

Initialize a [`LiveUpdate`](https://praw.readthedocs.io/en/stable/code_overview/models/liveupdate.html#praw.models.LiveUpdate "praw.models.LiveUpdate") instance.

Either `thread_id` and `update_id`, or `_data` must be provided.

Parameters:
- **reddit** – An instance of [`Reddit`](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit").
- **thread\_id** – A live thread ID, e.g., `"ukaeu1ik4sw5"`.
- **update\_id** – A live update ID, e.g., `"7827987a-c998-11e4-a0b9-22000b6a88d2"`.

Usage:

```python
update = LiveUpdate(reddit, "ukaeu1ik4sw5", "7827987a-c998-11e4-a0b9-22000b6a88d2")
update.thread  # LiveThread(id="ukaeu1ik4sw5")
update.id  # "7827987a-c998-11e4-a0b9-22000b6a88d2"
update.author  # "umbrae"
```

### contrib()→[praw.models.reddit.live.LiveUpdateContribution](https://praw.readthedocs.io/en/stable/code_overview/other/liveupdatecontribution.html#praw.models.reddit.live.LiveUpdateContribution "praw.models.reddit.live.LiveUpdateContribution")

Provide an instance of [`LiveUpdateContribution`](https://praw.readthedocs.io/en/stable/code_overview/other/liveupdatecontribution.html#praw.models.reddit.live.LiveUpdateContribution "praw.models.reddit.live.LiveUpdateContribution").

Usage:

```python
thread = reddit.live("ukaeu1ik4sw5")
update = thread["7827987a-c998-11e4-a0b9-22000b6a88d2"]
update.contrib  # LiveUpdateContribution instance
```

### _property_ fullname _: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_

Return the object's fullname.

A fullname is an object's kind mapping like `t3` followed by an underscore and
the object's base36 ID, e.g., `t1_c5s96e0`.

### _classmethod_ parse( _data:[Dict](https://docs.python.org/3/library/typing.html#typing.Dict "(in Python v3.11)")\[ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)"), [Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")\]_, _reddit:[praw.Reddit](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit")_)→[Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")

Return an instance of `cls` from `data`.

Parameters:
- **data** – The structured data.
- **reddit** – An instance of [`Reddit`](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit").

### _property_ thread _: [LiveThread](https://praw.readthedocs.io/en/stable/code_overview/models/livethread.html#praw.models.LiveThread "praw.models.reddit.live.LiveThread")_

Return [`LiveThread`](https://praw.readthedocs.io/en/stable/code_overview/models/livethread.html#praw.models.LiveThread "praw.models.LiveThread") object the update object belongs to.