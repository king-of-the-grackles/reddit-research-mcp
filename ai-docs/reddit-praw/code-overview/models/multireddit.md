# Multireddit

_class_ praw.models.Multireddit( _reddit:[praw.Reddit](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit")_, _\_data:[Dict](https://docs.python.org/3/library/typing.html#typing.Dict "(in Python v3.11)")\[ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)"), [Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")\]_)

A class for users' multireddits.

This is referred to as a "Custom Feed" on the Reddit UI.

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
| `can_edit` | A `bool` representing whether or not the authenticated user may edit the multireddit. |
| `copied_from` | The multireddit that the multireddit was copied from, if it exists, otherwise `None`. |
| `created_utc` | When the multireddit was created, in [Unix Time](https://en.wikipedia.org/wiki/Unix_time). |
| `description_html` | The description of the multireddit, as HTML. |
| `description_md` | The description of the multireddit, as Markdown. |
| `display_name` | The display name of the multireddit. |
| `name` | The name of the multireddit. |
| `over_18` | A `bool` representing whether or not the multireddit is restricted for users over 18. |
| `subreddits` | A list of [`Subreddit`](https://praw.readthedocs.io/en/stable/code_overview/models/subreddit.html#praw.models.Subreddit "praw.models.Subreddit") s that make up the multireddit. |
| `visibility` | The visibility of the multireddit, either `"private"`, `"public"`, or `"hidden"`. |

## Methods

### \_\_init\_\_( _reddit:[praw.Reddit](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit")_, _\_data:[Dict](https://docs.python.org/3/library/typing.html#typing.Dict "(in Python v3.11)")\[ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)"), [Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")\]_)

Initialize a [`Multireddit`](https://praw.readthedocs.io/en/stable/code_overview/models/multireddit.html#praw.models.Multireddit "praw.models.Multireddit") instance.

### add( _subreddit:[praw.models.Subreddit](https://praw.readthedocs.io/en/stable/code_overview/models/subreddit.html#praw.models.Subreddit "praw.models.Subreddit")_)

Add a subreddit to this multireddit.

Parameters:
- **subreddit** – The subreddit to add to this multi.

For example, to add r/test to multireddit `bboe/test`:

```python
subreddit = reddit.subreddit("test")
reddit.multireddit(redditor="bboe", name="test").add(subreddit)
```

### comments()→[CommentHelper](https://praw.readthedocs.io/en/stable/code_overview/other/commenthelper.html#praw.models.listing.mixins.subreddit.CommentHelper "praw.models.listing.mixins.subreddit.CommentHelper")

Provide an instance of [`CommentHelper`](https://praw.readthedocs.io/en/stable/code_overview/other/commenthelper.html#praw.models.listing.mixins.subreddit.CommentHelper "praw.models.listing.mixins.subreddit.CommentHelper").

For example, to output the author of the 25 most recent comments of r/test
execute:

```python
for comment in reddit.subreddit("test").comments(limit=25):
    print(comment.author)
```

### controversial( _\*_, _time\_filter:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")='all'_, _\*\*generator\_kwargs:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [int](https://docs.python.org/3/library/functions.html#int "(in Python v3.11)") \| [Dict](https://docs.python.org/3/library/typing.html#typing.Dict "(in Python v3.11)")\[ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)"), [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")\]_)→[Iterator](https://docs.python.org/3/library/typing.html#typing.Iterator "(in Python v3.11)")\[ [Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")\]

Return a [`ListingGenerator`](https://praw.readthedocs.io/en/stable/code_overview/other/listinggenerator.html#praw.models.ListingGenerator "praw.models.ListingGenerator") for controversial items.

Parameters:
- **time\_filter** – Can be one of: `"all"`, `"day"`, `"hour"`, `"month"`, `"week"`, or `"year"` (default: `"all"`).

Raises: [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError "(in Python v3.11)") if `time_filter` is invalid.

Additional keyword arguments are passed in the initialization of
[`ListingGenerator`](https://praw.readthedocs.io/en/stable/code_overview/other/listinggenerator.html#praw.models.ListingGenerator "praw.models.ListingGenerator").

This method can be used like:

```python
reddit.domain("imgur.com").controversial(time_filter="week")
reddit.multireddit(redditor="samuraisam", name="programming").controversial(
    time_filter="day"
)
reddit.redditor("spez").controversial(time_filter="month")
reddit.redditor("spez").comments.controversial(time_filter="year")
reddit.redditor("spez").submissions.controversial(time_filter="all")
reddit.subreddit("all").controversial(time_filter="hour")
```

### copy( _\*_, _display\_name:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_)→[praw.models.Multireddit](https://praw.readthedocs.io/en/stable/code_overview/models/multireddit.html#praw.models.Multireddit "praw.models.Multireddit")

Copy this multireddit and return the new multireddit.

Parameters:
- **display\_name** – The display name for the copied multireddit. Reddit will generate the `name` field from this display name. When not provided the copy will use the same display name and name as this multireddit.

To copy the multireddit `bboe/test` with a name of `"testing"`:

```python
reddit.multireddit(redditor="bboe", name="test").copy(display_name="testing")
```

### delete()

Delete this multireddit.

For example, to delete multireddit `bboe/test`:

```python
reddit.multireddit(redditor="bboe", name="test").delete()
```

### gilded( _\*\*generator\_kwargs:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [int](https://docs.python.org/3/library/functions.html#int "(in Python v3.11)") \| [Dict](https://docs.python.org/3/library/typing.html#typing.Dict "(in Python v3.11)")\[ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)"), [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")\]_)→[Iterator](https://docs.python.org/3/library/typing.html#typing.Iterator "(in Python v3.11)")\[ [Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")\]

Return a [`ListingGenerator`](https://praw.readthedocs.io/en/stable/code_overview/other/listinggenerator.html#praw.models.ListingGenerator "praw.models.ListingGenerator") for gilded items.

Additional keyword arguments are passed in the initialization of
[`ListingGenerator`](https://praw.readthedocs.io/en/stable/code_overview/other/listinggenerator.html#praw.models.ListingGenerator "praw.models.ListingGenerator").

For example, to get gilded items in r/test:

```python
for item in reddit.subreddit("test").gilded():
    print(item.id)
```

### hot( _\*\*generator\_kwargs:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [int](https://docs.python.org/3/library/functions.html#int "(in Python v3.11)") \| [Dict](https://docs.python.org/3/library/typing.html#typing.Dict "(in Python v3.11)")\[ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)"), [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")\]_)→[Iterator](https://docs.python.org/3/library/typing.html#typing.Iterator "(in Python v3.11)")\[ [Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")\]

Return a [`ListingGenerator`](https://praw.readthedocs.io/en/stable/code_overview/other/listinggenerator.html#praw.models.ListingGenerator "praw.models.ListingGenerator") for hot items.

Additional keyword arguments are passed in the initialization of
[`ListingGenerator`](https://praw.readthedocs.io/en/stable/code_overview/other/listinggenerator.html#praw.models.ListingGenerator "praw.models.ListingGenerator").

This method can be used like:

```python
reddit.domain("imgur.com").hot()
reddit.multireddit(redditor="samuraisam", name="programming").hot()
reddit.redditor("spez").hot()
reddit.redditor("spez").comments.hot()
reddit.redditor("spez").submissions.hot()
reddit.subreddit("all").hot()
```

### new( _\*\*generator\_kwargs:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [int](https://docs.python.org/3/library/functions.html#int "(in Python v3.11)") \| [Dict](https://docs.python.org/3/library/typing.html#typing.Dict "(in Python v3.11)")\[ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)"), [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")\]_)→[Iterator](https://docs.python.org/3/library/typing.html#typing.Iterator "(in Python v3.11)")\[ [Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")\]

Return a [`ListingGenerator`](https://praw.readthedocs.io/en/stable/code_overview/other/listinggenerator.html#praw.models.ListingGenerator "praw.models.ListingGenerator") for new items.

Additional keyword arguments are passed in the initialization of
[`ListingGenerator`](https://praw.readthedocs.io/en/stable/code_overview/other/listinggenerator.html#praw.models.ListingGenerator "praw.models.ListingGenerator").

This method can be used like:

```python
reddit.domain("imgur.com").new()
reddit.multireddit(redditor="samuraisam", name="programming").new()
reddit.redditor("spez").new()
reddit.redditor("spez").comments.new()
reddit.redditor("spez").submissions.new()
reddit.subreddit("all").new()
```

### random\_rising( _\*\*generator\_kwargs:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [int](https://docs.python.org/3/library/functions.html#int "(in Python v3.11)") \| [Dict](https://docs.python.org/3/library/typing.html#typing.Dict "(in Python v3.11)")\[ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)"), [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")\]_)→[Iterator](https://docs.python.org/3/library/typing.html#typing.Iterator "(in Python v3.11)")\[ [praw.models.Submission](https://praw.readthedocs.io/en/stable/code_overview/models/submission.html#praw.models.Submission "praw.models.Submission")\]

Return a [`ListingGenerator`](https://praw.readthedocs.io/en/stable/code_overview/other/listinggenerator.html#praw.models.ListingGenerator "praw.models.ListingGenerator") for random rising submissions.

Additional keyword arguments are passed in the initialization of
[`ListingGenerator`](https://praw.readthedocs.io/en/stable/code_overview/other/listinggenerator.html#praw.models.ListingGenerator "praw.models.ListingGenerator").

For example, to get random rising submissions for r/test:

```python
for submission in reddit.subreddit("test").random_rising():
    print(submission.title)
```

### remove( _subreddit:[praw.models.Subreddit](https://praw.readthedocs.io/en/stable/code_overview/models/subreddit.html#praw.models.Subreddit "praw.models.Subreddit")_)

Remove a subreddit from this multireddit.

Parameters:
- **subreddit** – The subreddit to remove from this multi.

For example, to remove r/test from multireddit `bboe/test`:

```python
subreddit = reddit.subreddit("test")
reddit.multireddit(redditor="bboe", name="test").remove(subreddit)
```

### rising( _\*\*generator\_kwargs:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [int](https://docs.python.org/3/library/functions.html#int "(in Python v3.11)") \| [Dict](https://docs.python.org/3/library/typing.html#typing.Dict "(in Python v3.11)")\[ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)"), [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")\]_)→[Iterator](https://docs.python.org/3/library/typing.html#typing.Iterator "(in Python v3.11)")\[ [praw.models.Submission](https://praw.readthedocs.io/en/stable/code_overview/models/submission.html#praw.models.Submission "praw.models.Submission")\]

Return a [`ListingGenerator`](https://praw.readthedocs.io/en/stable/code_overview/other/listinggenerator.html#praw.models.ListingGenerator "praw.models.ListingGenerator") for rising submissions.

Additional keyword arguments are passed in the initialization of
[`ListingGenerator`](https://praw.readthedocs.io/en/stable/code_overview/other/listinggenerator.html#praw.models.ListingGenerator "praw.models.ListingGenerator").

For example, to get rising submissions for r/test:

```python
for submission in reddit.subreddit("test").rising():
    print(submission.title)
```

### _static_ sluggify( _title:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_)

Return a slug version of the title.

Parameters:
- **title** – The title to make a slug of.

Adapted from Reddit's utils.py.

### stream()→[SubredditStream](https://praw.readthedocs.io/en/stable/code_overview/other/subredditstream.html#praw.models.reddit.subreddit.SubredditStream "praw.models.reddit.subreddit.SubredditStream")

Provide an instance of [`SubredditStream`](https://praw.readthedocs.io/en/stable/code_overview/other/subredditstream.html#praw.models.reddit.subreddit.SubredditStream "praw.models.reddit.subreddit.SubredditStream").

Streams can be used to indefinitely retrieve new comments made to a multireddit,
like:

```python
for comment in reddit.multireddit(redditor="spez", name="fun").stream.comments():
    print(comment)
```

Additionally, new submissions can be retrieved via the stream. In the following
example all new submissions to the multireddit are fetched:

```python
for submission in reddit.multireddit(
    redditor="bboe", name="games"
).stream.submissions():
    print(submission)
```

### top( _\*_, _time\_filter:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")='all'_, _\*\*generator\_kwargs:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [int](https://docs.python.org/3/library/functions.html#int "(in Python v3.11)") \| [Dict](https://docs.python.org/3/library/typing.html#typing.Dict "(in Python v3.11)")\[ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)"), [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")\]_)→[Iterator](https://docs.python.org/3/library/typing.html#typing.Iterator "(in Python v3.11)")\[ [Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")\]

Return a [`ListingGenerator`](https://praw.readthedocs.io/en/stable/code_overview/other/listinggenerator.html#praw.models.ListingGenerator "praw.models.ListingGenerator") for top items.

Parameters:
- **time\_filter** – Can be one of: `"all"`, `"day"`, `"hour"`, `"month"`, `"week"`, or `"year"` (default: `"all"`).

Raises: [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError "(in Python v3.11)") if `time_filter` is invalid.

Additional keyword arguments are passed in the initialization of
[`ListingGenerator`](https://praw.readthedocs.io/en/stable/code_overview/other/listinggenerator.html#praw.models.ListingGenerator "praw.models.ListingGenerator").

This method can be used like:

```python
reddit.domain("imgur.com").top(time_filter="week")
reddit.multireddit(redditor="samuraisam", name="programming").top(time_filter="day")
reddit.redditor("spez").top(time_filter="month")
reddit.redditor("spez").comments.top(time_filter="year")
reddit.redditor("spez").submissions.top(time_filter="all")
reddit.subreddit("all").top(time_filter="hour")
```

### update( _\*\*updated\_settings:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [List](https://docs.python.org/3/library/typing.html#typing.List "(in Python v3.11)")\[ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [praw.models.Subreddit](https://praw.readthedocs.io/en/stable/code_overview/models/subreddit.html#praw.models.Subreddit "praw.models.Subreddit") \| [Dict](https://docs.python.org/3/library/typing.html#typing.Dict "(in Python v3.11)")\[ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)"), [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")\]\]_)

Update this multireddit.

Keyword arguments are passed for settings that should be updated. They can any of:

Parameters:
- **display\_name** – The display name for this multireddit. Must be no longer than 50 characters.
- **subreddits** – Subreddits for this multireddit.
- **description\_md** – Description for this multireddit, formatted in Markdown.
- **icon\_name** – Can be one of: `"art and design"`, `"ask"`, `"books"`, `"business"`, `"cars"`, `"comics"`, `"cute animals"`, `"diy"`, `"entertainment"`, `"food and drink"`, `"funny"`, `"games"`, `"grooming"`, `"health"`, `"life advice"`, `"military"`, `"models pinup"`, `"music"`, `"news"`, `"philosophy"`, `"pictures and gifs"`, `"science"`, `"shopping"`, `"sports"`, `"style"`, `"tech"`, `"travel"`, `"unusual stories"`, `"video"`, or `None`.
- **key\_color** – RGB hex color code of the form `"#FFFFFF"`.
- **visibility** – Can be one of: `"hidden"`, `"private"`, or `"public"`.
- **weighting\_scheme** – Can be one of: `"classic"` or `"fresh"`.

For example, to rename multireddit `"bboe/test"` to `"bboe/testing"`:

```python
reddit.multireddit(redditor="bboe", name="test").update(display_name="testing")
```