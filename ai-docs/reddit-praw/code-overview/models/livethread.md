# LiveThread

_class_ praw.models.LiveThread( _reddit:[praw.Reddit](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit")_, _id:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_, _\_data:[Dict](https://docs.python.org/3/library/typing.html#typing.Dict "(in Python v3.11)")\[ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)"), [Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")\]\| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_)

An individual [`LiveThread`](https://praw.readthedocs.io/en/stable/code_overview/models/livethread.html#praw.models.LiveThread "praw.models.LiveThread") object.

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
| `created_utc` | The creation time of the live thread, in [Unix Time](https://en.wikipedia.org/wiki/Unix_time). |
| `description` | Description of the live thread, as Markdown. |
| `description_html` | Description of the live thread, as HTML. |
| `id` | The ID of the live thread. |
| `nsfw` | A `bool` representing whether or not the live thread is marked as NSFW. |

## Methods

### \_\_getitem\_\_( _update\_id:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_)→[praw.models.LiveUpdate](https://praw.readthedocs.io/en/stable/code_overview/models/liveupdate.html#praw.models.LiveUpdate "praw.models.LiveUpdate")

Return a lazy [`LiveUpdate`](https://praw.readthedocs.io/en/stable/code_overview/models/liveupdate.html#praw.models.LiveUpdate "praw.models.LiveUpdate") instance.

Parameters:
- **update\_id** – A live update ID, e.g., `"7827987a-c998-11e4-a0b9-22000b6a88d2"`.

Usage:

```python
thread = reddit.live("ukaeu1ik4sw5")
update = thread["7827987a-c998-11e4-a0b9-22000b6a88d2"]
update.thread  # LiveThread(id="ukaeu1ik4sw5")
update.id  # "7827987a-c998-11e4-a0b9-22000b6a88d2"
update.author  # "umbrae"
```

### \_\_init\_\_( _reddit:[praw.Reddit](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit")_, _id:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_, _\_data:[Dict](https://docs.python.org/3/library/typing.html#typing.Dict "(in Python v3.11)")\[ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)"), [Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")\]\| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_)

Initialize a [`LiveThread`](https://praw.readthedocs.io/en/stable/code_overview/models/livethread.html#praw.models.LiveThread "praw.models.LiveThread") instance.

Parameters:
- **reddit** – An instance of [`Reddit`](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit").
- **id** – A live thread ID, e.g., `"ukaeu1ik4sw5"`

### contrib()→[praw.models.reddit.live.LiveThreadContribution](https://praw.readthedocs.io/en/stable/code_overview/other/livethreadcontribution.html#praw.models.reddit.live.LiveThreadContribution "praw.models.reddit.live.LiveThreadContribution")

Provide an instance of [`LiveThreadContribution`](https://praw.readthedocs.io/en/stable/code_overview/other/livethreadcontribution.html#praw.models.reddit.live.LiveThreadContribution "praw.models.reddit.live.LiveThreadContribution").

Usage:

```python
thread = reddit.live("ukaeu1ik4sw5")
thread.contrib.add("### update")
```

### contributor()→[praw.models.reddit.live.LiveContributorRelationship](https://praw.readthedocs.io/en/stable/code_overview/other/livecontributorrelationship.html#praw.models.reddit.live.LiveContributorRelationship "praw.models.reddit.live.LiveContributorRelationship")

Provide an instance of [`LiveContributorRelationship`](https://praw.readthedocs.io/en/stable/code_overview/other/livecontributorrelationship.html#praw.models.reddit.live.LiveContributorRelationship "praw.models.reddit.live.LiveContributorRelationship").

You can call the instance to get a list of contributors which is represented as
[`RedditorList`](https://praw.readthedocs.io/en/stable/code_overview/other/redditorlist.html#praw.models.RedditorList "praw.models.RedditorList") instance consists of [`Redditor`](https://praw.readthedocs.io/en/stable/code_overview/models/redditor.html#praw.models.Redditor "praw.models.Redditor") instances. Those
[`Redditor`](https://praw.readthedocs.io/en/stable/code_overview/models/redditor.html#praw.models.Redditor "praw.models.Redditor") instances have `permissions` attributes as contributors:

```python
thread = reddit.live("ukaeu1ik4sw5")
for contributor in thread.contributor():
    # prints `Redditor(name="Acidtwist") ["all"]`
    print(contributor, contributor.permissions)
```

### discussions( _\*\*generator\_kwargs:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [int](https://docs.python.org/3/library/functions.html#int "(in Python v3.11)") \| [Dict](https://docs.python.org/3/library/typing.html#typing.Dict "(in Python v3.11)")\[ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)"), [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")\]_)→[Iterator](https://docs.python.org/3/library/typing.html#typing.Iterator "(in Python v3.11)")\[ [praw.models.Submission](https://praw.readthedocs.io/en/stable/code_overview/models/submission.html#praw.models.Submission "praw.models.Submission")\]

Get submissions linking to the thread.

Parameters:
- **generator\_kwargs** – keyword arguments passed to [`ListingGenerator`](https://praw.readthedocs.io/en/stable/code_overview/other/listinggenerator.html#praw.models.ListingGenerator "praw.models.ListingGenerator") constructor.

Returns: A [`ListingGenerator`](https://praw.readthedocs.io/en/stable/code_overview/other/listinggenerator.html#praw.models.ListingGenerator "praw.models.ListingGenerator") object which yields [`Submission`](https://praw.readthedocs.io/en/stable/code_overview/models/submission.html#praw.models.Submission "praw.models.Submission") objects.

Additional keyword arguments are passed in the initialization of
[`ListingGenerator`](https://praw.readthedocs.io/en/stable/code_overview/other/listinggenerator.html#praw.models.ListingGenerator "praw.models.ListingGenerator").

Usage:

```python
thread = reddit.live("ukaeu1ik4sw5")
for submission in thread.discussions(limit=None):
    print(submission.title)
```

### _classmethod_ parse( _data:[Dict](https://docs.python.org/3/library/typing.html#typing.Dict "(in Python v3.11)")\[ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)"), [Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")\]_, _reddit:[praw.Reddit](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit")_)→[Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")

Return an instance of `cls` from `data`.

Parameters:
- **data** – The structured data.
- **reddit** – An instance of [`Reddit`](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit").

### report( _type:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_)

Report the thread violating the Reddit rules.

Parameters:
- **type** – One of `"spam"`, `"vote-manipulation"`, `"personal-information"`, `"sexualizing-minors"`, or `"site-breaking"`.

Usage:

```python
thread = reddit.live("xyu8kmjvfrww")
thread.report("spam")
```

### stream()→[praw.models.reddit.live.LiveThreadStream](https://praw.readthedocs.io/en/stable/code_overview/other/livethreadstream.html#praw.models.reddit.live.LiveThreadStream "praw.models.reddit.live.LiveThreadStream")

Provide an instance of [`LiveThreadStream`](https://praw.readthedocs.io/en/stable/code_overview/other/livethreadstream.html#praw.models.reddit.live.LiveThreadStream "praw.models.reddit.live.LiveThreadStream").

Streams are used to indefinitely retrieve new updates made to a live thread,
like:

```python
for live_update in reddit.live("ta535s1hq2je").stream.updates():
    print(live_update.body)
```

Updates are yielded oldest first as [`LiveUpdate`](https://praw.readthedocs.io/en/stable/code_overview/models/liveupdate.html#praw.models.LiveUpdate "praw.models.LiveUpdate"). Up to 100 historical
updates will initially be returned. To only retrieve new updates starting from
when the stream is created, pass `skip_existing=True`:

```python
live_thread = reddit.live("ta535s1hq2je")
for live_update in live_thread.stream.updates(skip_existing=True):
    print(live_update.author)
```

### updates( _\*\*generator\_kwargs:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [int](https://docs.python.org/3/library/functions.html#int "(in Python v3.11)") \| [Dict](https://docs.python.org/3/library/typing.html#typing.Dict "(in Python v3.11)")\[ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)"), [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")\]_)→[Iterator](https://docs.python.org/3/library/typing.html#typing.Iterator "(in Python v3.11)")\[ [praw.models.LiveUpdate](https://praw.readthedocs.io/en/stable/code_overview/models/liveupdate.html#praw.models.LiveUpdate "praw.models.LiveUpdate")\]

Return a [`ListingGenerator`](https://praw.readthedocs.io/en/stable/code_overview/other/listinggenerator.html#praw.models.ListingGenerator "praw.models.ListingGenerator") yields [`LiveUpdate`](https://praw.readthedocs.io/en/stable/code_overview/models/liveupdate.html#praw.models.LiveUpdate "praw.models.LiveUpdate") s.

Parameters:
- **generator\_kwargs** – keyword arguments passed to [`ListingGenerator`](https://praw.readthedocs.io/en/stable/code_overview/other/listinggenerator.html#praw.models.ListingGenerator "praw.models.ListingGenerator") constructor.

Returns: A [`ListingGenerator`](https://praw.readthedocs.io/en/stable/code_overview/other/listinggenerator.html#praw.models.ListingGenerator "praw.models.ListingGenerator") object which yields [`LiveUpdate`](https://praw.readthedocs.io/en/stable/code_overview/models/liveupdate.html#praw.models.LiveUpdate "praw.models.LiveUpdate") objects.

Additional keyword arguments are passed in the initialization of
[`ListingGenerator`](https://praw.readthedocs.io/en/stable/code_overview/other/listinggenerator.html#praw.models.ListingGenerator "praw.models.ListingGenerator").

Usage:

```python
thread = reddit.live("ukaeu1ik4sw5")
after = "LiveUpdate_fefb3dae-7534-11e6-b259-0ef8c7233633"
for submission in thread.updates(limit=5, params={"after": after}):
    print(submission.body)
```