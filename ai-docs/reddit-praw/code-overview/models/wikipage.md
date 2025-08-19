# WikiPage

_class_ praw.models.reddit.wikipage.WikiPage( _reddit:[praw.Reddit](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit")_, _subreddit:[praw.models.Subreddit](https://praw.readthedocs.io/en/stable/code_overview/models/subreddit.html#praw.models.Subreddit "praw.models.Subreddit")_, _name:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_, _revision:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_, _\_data:[Dict](https://docs.python.org/3/library/typing.html#typing.Dict "(in Python v3.11)")\[ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)"), [Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")\]\| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_)

An individual [`WikiPage`](https://praw.readthedocs.io/en/stable/code_overview/models/wikipage.html#praw.models.reddit.wikipage.WikiPage "praw.models.reddit.wikipage.WikiPage") object.

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
| `content_html` | The contents of the wiki page, as HTML. |
| `content_md` | The contents of the wiki page, as Markdown. |
| `may_revise` | A `bool` representing whether or not the authenticated user may edit the wiki page. |
| `name` | The name of the wiki page. |
| `revision_by` | The [`Redditor`](https://praw.readthedocs.io/en/stable/code_overview/models/redditor.html#praw.models.Redditor "praw.models.Redditor") who authored this revision of the wiki page. |
| `revision_date` | The time of this revision, in [Unix Time](https://en.wikipedia.org/wiki/Unix_time). |
| `subreddit` | The [`Subreddit`](https://praw.readthedocs.io/en/stable/code_overview/models/subreddit.html#praw.models.Subreddit "praw.models.Subreddit") this wiki page belongs to. |

## Methods

### \_\_init\_\_( _reddit:[praw.Reddit](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit")_, _subreddit:[praw.models.Subreddit](https://praw.readthedocs.io/en/stable/code_overview/models/subreddit.html#praw.models.Subreddit "praw.models.Subreddit")_, _name:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_, _revision:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_, _\_data:[Dict](https://docs.python.org/3/library/typing.html#typing.Dict "(in Python v3.11)")\[ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)"), [Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")\]\| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_)

Initialize a [`WikiPage`](https://praw.readthedocs.io/en/stable/code_overview/models/wikipage.html#praw.models.reddit.wikipage.WikiPage "praw.models.reddit.wikipage.WikiPage") instance.

Parameters:
- **revision** – A specific revision ID to fetch. By default, fetches the most recent revision.

### discussions( _\*\*generator\_kwargs:[Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")_)→[Iterator](https://docs.python.org/3/library/typing.html#typing.Iterator "(in Python v3.11)")\[ [praw.models.Submission](https://praw.readthedocs.io/en/stable/code_overview/models/submission.html#praw.models.Submission "praw.models.Submission")\]

Return a [`ListingGenerator`](https://praw.readthedocs.io/en/stable/code_overview/other/listinggenerator.html#praw.models.ListingGenerator "praw.models.ListingGenerator") for discussions of a wiki page.

Discussions are site-wide links to a wiki page.

Additional keyword arguments are passed in the initialization of
[`ListingGenerator`](https://praw.readthedocs.io/en/stable/code_overview/other/listinggenerator.html#praw.models.ListingGenerator "praw.models.ListingGenerator").

To view the titles of discussions of the page `"praw_test"` in r/test, try:

```python
for submission in reddit.subreddit("test").wiki["praw_test"].discussions():
    print(submission.title)
```

### edit( _\*_, _content:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_, _reason:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_, _\*\*other\_settings:[Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")_)

Edit this wiki page's contents.

Parameters:
- **content** – The updated Markdown content of the page.
- **reason** – The reason for the revision.
- **other\_settings** – Additional keyword arguments to pass.

For example, to replace the first wiki page of r/test with the phrase `"test wiki page"`:

```python
page = next(iter(reddit.subreddit("test").wiki))
page.edit(content="test wiki page")
```

### mod()→[WikiPageModeration](https://praw.readthedocs.io/en/stable/code_overview/other/wikipagemoderation.html#praw.models.reddit.wikipage.WikiPageModeration "praw.models.reddit.wikipage.WikiPageModeration")

Provide an instance of [`WikiPageModeration`](https://praw.readthedocs.io/en/stable/code_overview/other/wikipagemoderation.html#praw.models.reddit.wikipage.WikiPageModeration "praw.models.reddit.wikipage.WikiPageModeration").

For example, to add u/spez as an editor on the wikipage `"praw_test"` try:

```python
reddit.subreddit("test").wiki["praw_test"].mod.add("spez")
```

### _classmethod_ parse( _data:[Dict](https://docs.python.org/3/library/typing.html#typing.Dict "(in Python v3.11)")\[ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)"), [Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")\]_, _reddit:[praw.Reddit](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit")_)→[Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")

Return an instance of `cls` from `data`.

Parameters:
- **data** – The structured data.
- **reddit** – An instance of [`Reddit`](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit").

### revision( _revision:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_)

Return a specific version of this page by revision ID.

To view revision `"1234abc"` of `"praw_test"` in r/test:

```python
page = reddit.subreddit("test").wiki["praw_test"].revision("1234abc")
```

### revisions( _\*\*generator\_kwargs:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [int](https://docs.python.org/3/library/functions.html#int "(in Python v3.11)") \| [Dict](https://docs.python.org/3/library/typing.html#typing.Dict "(in Python v3.11)")\[ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)"), [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")\]_)→[Generator](https://docs.python.org/3/library/typing.html#typing.Generator "(in Python v3.11)")\[ [WikiPage](https://praw.readthedocs.io/en/stable/code_overview/models/wikipage.html#praw.models.reddit.wikipage.WikiPage "praw.models.reddit.wikipage.WikiPage"), [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)"), [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")\]

Return a [`ListingGenerator`](https://praw.readthedocs.io/en/stable/code_overview/other/listinggenerator.html#praw.models.ListingGenerator "praw.models.ListingGenerator") for page revisions.

Additional keyword arguments are passed in the initialization of
[`ListingGenerator`](https://praw.readthedocs.io/en/stable/code_overview/other/listinggenerator.html#praw.models.ListingGenerator "praw.models.ListingGenerator").

To view the wiki revisions for `"praw_test"` in r/test try:

```python
for item in reddit.subreddit("test").wiki["praw_test"].revisions():
    print(item)
```

To get [`WikiPage`](https://praw.readthedocs.io/en/stable/code_overview/models/wikipage.html#praw.models.reddit.wikipage.WikiPage "praw.models.reddit.wikipage.WikiPage") objects for each revision:

```python
for item in reddit.subreddit("test").wiki["praw_test"].revisions():
    print(item["page"])
```