# MoreComments

_class_ praw.models.MoreComments( _reddit:[praw.Reddit](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit")_, _\_data:[Dict](https://docs.python.org/3/library/typing.html#typing.Dict "(in Python v3.11)")\[ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)"), [Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")\]_)

A class indicating there are more comments.

## Methods

### \_\_init\_\_( _reddit:[praw.Reddit](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit")_, _\_data:[Dict](https://docs.python.org/3/library/typing.html#typing.Dict "(in Python v3.11)")\[ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)"), [Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")\]_)

Initialize a [`MoreComments`](https://praw.readthedocs.io/en/stable/code_overview/models/more.html#praw.models.MoreComments "praw.models.MoreComments") instance.

### comments( _\*_, _update:[bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.11)")=True_)→[List](https://docs.python.org/3/library/typing.html#typing.List "(in Python v3.11)")\[ [praw.models.Comment](https://praw.readthedocs.io/en/stable/code_overview/models/comment.html#praw.models.Comment "praw.models.Comment")\]

Fetch and return the comments for a single [`MoreComments`](https://praw.readthedocs.io/en/stable/code_overview/models/more.html#praw.models.MoreComments "praw.models.MoreComments") object.

### _classmethod_ parse( _data:[Dict](https://docs.python.org/3/library/typing.html#typing.Dict "(in Python v3.11)")\[ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)"), [Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")\]_, _reddit:[praw.Reddit](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit")_)→[Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")

Return an instance of `cls` from `data`.

Parameters:
- **data** – The structured data.
- **reddit** – An instance of [`Reddit`](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit").