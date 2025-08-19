# Draft

_class_ praw.models.Draft( _reddit:[praw.Reddit](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit")_, _id:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_, _\_data:[Dict](https://docs.python.org/3/library/typing.html#typing.Dict "(in Python v3.11)")\[ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)"), [Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")\]=None_)

A class that represents a Reddit submission draft.

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
| `link_flair_template_id` | The link flair's ID. |
| `link_flair_text` | The link flair's text content, or `None` if not flaired. |
| `modified` | Time the submission draft was modified, represented in [Unix Time](https://en.wikipedia.org/wiki/Unix_time). |
| `original_content` | Whether the submission draft will be set as original content. |
| `selftext` | The submission draft's selftext. `None` if a link submission draft. |
| `spoiler` | Whether the submission will be marked as a spoiler. |
| `subreddit` | Provides an instance of [`Subreddit`](https://praw.readthedocs.io/en/stable/code_overview/models/subreddit.html#praw.models.Subreddit "praw.models.Subreddit") or [`UserSubreddit`](https://praw.readthedocs.io/en/stable/code_overview/other/usersubreddit.html#praw.models.UserSubreddit "praw.models.UserSubreddit") (if set). |
| `title` | The title of the submission draft. |
| `url` | The URL the submission draft links to. |

## Methods

### \_\_init\_\_( _reddit:[praw.Reddit](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit")_, _id:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_, _\_data:[Dict](https://docs.python.org/3/library/typing.html#typing.Dict "(in Python v3.11)")\[ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)"), [Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")\]=None_)

Initialize a [`Draft`](https://praw.readthedocs.io/en/stable/code_overview/models/draft.html#praw.models.Draft "praw.models.Draft") instance.

### delete()

Delete the [`Draft`](https://praw.readthedocs.io/en/stable/code_overview/models/draft.html#praw.models.Draft "praw.models.Draft").

Example usage:

```python
draft = reddit.drafts("124862bc-e1e9-11eb-aa4f-e68667a77cbb")
draft.delete()
```

### _classmethod_ parse( _data:[Dict](https://docs.python.org/3/library/typing.html#typing.Dict "(in Python v3.11)")\[ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)"), [Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")\]_, _reddit:[praw.Reddit](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit")_)→[Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")

Return an instance of `cls` from `data`.

Parameters:
- **data** – The structured data.
- **reddit** – An instance of [`Reddit`](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit").

### submit( _\*_, _flair\_id:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_, _flair\_text:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_, _nsfw:[bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.11)") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_, _selftext:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_, _spoiler:[bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.11)") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_, _subreddit:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [praw.models.Subreddit](https://praw.readthedocs.io/en/stable/code_overview/models/subreddit.html#praw.models.Subreddit "praw.models.Subreddit") \| [praw.models.UserSubreddit](https://praw.readthedocs.io/en/stable/code_overview/other/usersubreddit.html#praw.models.UserSubreddit "praw.models.UserSubreddit") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_, _title:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_, _url:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_, _\*\*submit\_kwargs_)→[praw.models.Submission](https://praw.readthedocs.io/en/stable/code_overview/models/submission.html#praw.models.Submission "praw.models.Submission")

Submit a draft.

Parameters:
- **flair\_id** – The flair template to select (default: `None`).
- **flair\_text** – If the template's `flair_text_editable` value is `True`, this value will set a custom text (default: `None`). `flair_id` is required when `flair_text` is provided.
- **nsfw** – Whether or not the submission should be marked NSFW (default: `None`).
- **selftext** – The Markdown formatted content for a `text` submission. Use an empty string, `""`, to make a title-only submission (default: `None`).
- **spoiler** – Whether or not the submission should be marked as a spoiler (default: `None`).
- **subreddit** – The subreddit to submit the draft to. This accepts a subreddit display name, [`Subreddit`](https://praw.readthedocs.io/en/stable/code_overview/models/subreddit.html#praw.models.Subreddit "praw.models.Subreddit") object, or [`UserSubreddit`](https://praw.readthedocs.io/en/stable/code_overview/other/usersubreddit.html#praw.models.UserSubreddit "praw.models.UserSubreddit") object.
- **title** – The title of the submission (default: `None`).
- **url** – The URL for a `link` submission (default: `None`).

Returns: A [`Submission`](https://praw.readthedocs.io/en/stable/code_overview/models/submission.html#praw.models.Submission "praw.models.Submission") object for the newly created submission.

Note: Parameters set here will override their respective [`Draft`](https://praw.readthedocs.io/en/stable/code_overview/models/draft.html#praw.models.Draft "praw.models.Draft") attributes.

Additional keyword arguments are passed to the [`Subreddit.submit()`](https://praw.readthedocs.io/en/stable/code_overview/models/subreddit.html#praw.models.Subreddit.submit "praw.models.Subreddit.submit") method.

For example, to submit a draft as is:

```python
draft = reddit.drafts("5f87d55c-e4fb-11eb-8965-6aeb41b0880e")
submission = draft.submit()
```

For example, to submit a draft but use a different title than what is set:

```python
draft = reddit.drafts("5f87d55c-e4fb-11eb-8965-6aeb41b0880e")
submission = draft.submit(title="New Title")
```

See also:
- [`submit()`](https://praw.readthedocs.io/en/stable/code_overview/models/subreddit.html#praw.models.Subreddit.submit "praw.models.Subreddit.submit") to submit url posts and selftexts
- [`submit_gallery()`](https://praw.readthedocs.io/en/stable/code_overview/models/subreddit.html#praw.models.Subreddit.submit_gallery "praw.models.Subreddit.submit_gallery"). to submit more than one image in the same post
- [`submit_image()`](https://praw.readthedocs.io/en/stable/code_overview/models/subreddit.html#praw.models.Subreddit.submit_image "praw.models.Subreddit.submit_image") to submit images
- [`submit_poll()`](https://praw.readthedocs.io/en/stable/code_overview/models/subreddit.html#praw.models.Subreddit.submit_poll "praw.models.Subreddit.submit_poll") to submit polls
- [`submit_video()`](https://praw.readthedocs.io/en/stable/code_overview/models/subreddit.html#praw.models.Subreddit.submit_video "praw.models.Subreddit.submit_video") to submit videos and videogifs

### update( _\*_, _flair\_id:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_, _flair\_text:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_, _is\_public\_link:[bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.11)") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_, _nsfw:[bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.11)") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_, _original\_content:[bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.11)") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_, _selftext:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_, _send\_replies:[bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.11)") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_, _spoiler:[bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.11)") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_, _subreddit:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [praw.models.Subreddit](https://praw.readthedocs.io/en/stable/code_overview/models/subreddit.html#praw.models.Subreddit "praw.models.Subreddit") \| [praw.models.UserSubreddit](https://praw.readthedocs.io/en/stable/code_overview/other/usersubreddit.html#praw.models.UserSubreddit "praw.models.UserSubreddit") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_, _title:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_, _url:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_, _\*\*draft\_kwargs_)

Update the [`Draft`](https://praw.readthedocs.io/en/stable/code_overview/models/draft.html#praw.models.Draft "praw.models.Draft").

Note: Only provided values will be updated.

Parameters:
- **flair\_id** – The flair template to select.
- **flair\_text** – If the template's `flair_text_editable` value is `True`, this value will set a custom text. `flair_id` is required when `flair_text` is provided.
- **is\_public\_link** – Whether to enable public viewing of the draft before it is submitted.
- **nsfw** – Whether the draft should be marked NSFW.
- **original\_content** – Whether the submission should be marked as original content.
- **selftext** – The Markdown formatted content for a text submission draft. Use `None` to make a title-only submission draft. `selftext` can not be provided if `url` is provided.
- **send\_replies** – When `True`, messages will be sent to the submission author when comments are made to the submission.
- **spoiler** – Whether the submission should be marked as a spoiler.
- **subreddit** – The subreddit to create the draft for. This accepts a subreddit display name, [`Subreddit`](https://praw.readthedocs.io/en/stable/code_overview/models/subreddit.html#praw.models.Subreddit "praw.models.Subreddit") object, or [`UserSubreddit`](https://praw.readthedocs.io/en/stable/code_overview/other/usersubreddit.html#praw.models.UserSubreddit "praw.models.UserSubreddit") object.
- **title** – The title of the draft.
- **url** – The URL for a `link` submission draft. `url` can not be provided if `selftext` is provided.

Additional keyword arguments can be provided to handle new parameters as Reddit introduces them.

For example, to update the title of a draft do:

```python
draft = reddit.drafts("5f87d55c-e4fb-11eb-8965-6aeb41b0880e")
draft.update(title="New title")
```