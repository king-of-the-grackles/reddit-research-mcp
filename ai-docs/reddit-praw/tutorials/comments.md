# Comment Extraction and Parsing

A common use for Reddit's API is to extract comments from submissions and use them to
perform keyword or phrase analysis.

As always, you need to begin by creating an instance of [`Reddit`](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit"):

```python
import praw

reddit = praw.Reddit(
    client_id="CLIENT_ID",
    client_secret="CLIENT_SECRET",
    password="PASSWORD",
    user_agent="Comment Extraction (by u/USERNAME)",
    username="USERNAME",
)
```

Note

If you are only analyzing public comments, entering a username and password is
optional.

In this document, we will detail the process of finding all the comments for a given
submission. If you instead want to process all comments on Reddit, or comments belonging
to one or more specific subreddits, please see [`SubredditStream.comments()`](https://praw.readthedocs.io/en/stable/code_overview/other/subredditstream.html#praw.models.reddit.subreddit.SubredditStream.comments "praw.models.reddit.subreddit.SubredditStream.comments").

## Extracting comments with PRAW

Assume we want to process the comments for this submission:
[https://www.reddit.com/r/funny/comments/3g1jfi/buttons/](https://www.reddit.com/r/funny/comments/3g1jfi/buttons/)

We first need to obtain a submission object. We can do that either with the entire URL:

```python
url = "https://www.reddit.com/r/funny/comments/3g1jfi/buttons/"
submission = reddit.submission(url=url)
```

or with the submission's ID which comes after `comments/` in the URL:

```python
submission = reddit.submission("3g1jfi")
```

With a submission object we can then interact with its [`CommentForest`](https://praw.readthedocs.io/en/stable/code_overview/other/commentforest.html#praw.models.comment_forest.CommentForest "praw.models.comment_forest.CommentForest") through
the submission's [`Submission.comments`](https://praw.readthedocs.io/en/stable/code_overview/models/submission.html#praw.models.Submission.comments "praw.models.Submission.comments") attribute. A [`CommentForest`](https://praw.readthedocs.io/en/stable/code_overview/other/commentforest.html#praw.models.comment_forest.CommentForest "praw.models.comment_forest.CommentForest") is a
list of top-level comments each of which contains a [`CommentForest`](https://praw.readthedocs.io/en/stable/code_overview/other/commentforest.html#praw.models.comment_forest.CommentForest "praw.models.comment_forest.CommentForest") of replies.

If we wanted to output only the `body` of the top-level comments in the thread we
could do:

```python
for top_level_comment in submission.comments:
    print(top_level_comment.body)
```

While running this you will most likely encounter the exception `AttributeError:
'MoreComments' object has no attribute 'body'`. This submission's comment forest
contains a number of [`MoreComments`](https://praw.readthedocs.io/en/stable/code_overview/models/more.html#praw.models.MoreComments "praw.models.MoreComments") objects. These objects represent the "load
more comments", and "continue this thread" links encountered on the website. While we
could ignore [`MoreComments`](https://praw.readthedocs.io/en/stable/code_overview/models/more.html#praw.models.MoreComments "praw.models.MoreComments") in our code, like so:

```python
from praw.models import MoreComments

for top_level_comment in submission.comments:
    if isinstance(top_level_comment, MoreComments):
        continue
    print(top_level_comment.body)
```

## The `replace_more` method

In the previous snippet, we used [`isinstance()`](https://docs.python.org/3/library/functions.html#isinstance "(in Python v3.11)") to check whether the item in the
comment list was a [`MoreComments`](https://praw.readthedocs.io/en/stable/code_overview/models/more.html#praw.models.MoreComments "praw.models.MoreComments") so that we could ignore it. But there is a
better way: the [`CommentForest`](https://praw.readthedocs.io/en/stable/code_overview/other/commentforest.html#praw.models.comment_forest.CommentForest "praw.models.comment_forest.CommentForest") object has a method called
[`replace_more()`](https://praw.readthedocs.io/en/stable/code_overview/other/commentforest.html#praw.models.comment_forest.CommentForest.replace_more "praw.models.comment_forest.CommentForest.replace_more"), which replaces or removes [`MoreComments`](https://praw.readthedocs.io/en/stable/code_overview/models/more.html#praw.models.MoreComments "praw.models.MoreComments") objects from the
forest.

Each replacement requires one network request, and its response may yield additional
[`MoreComments`](https://praw.readthedocs.io/en/stable/code_overview/models/more.html#praw.models.MoreComments "praw.models.MoreComments") instances. As a result, by default, [`replace_more()`](https://praw.readthedocs.io/en/stable/code_overview/other/commentforest.html#praw.models.comment_forest.CommentForest.replace_more "praw.models.comment_forest.CommentForest.replace_more") only
replaces at most 32 [`MoreComments`](https://praw.readthedocs.io/en/stable/code_overview/models/more.html#praw.models.MoreComments "praw.models.MoreComments") instances – all other instances are simply
removed. The maximum number of instances to replace can be configured via the `limit`
parameter. Additionally a `threshold` parameter can be set to only perform replacement
of [`MoreComments`](https://praw.readthedocs.io/en/stable/code_overview/models/more.html#praw.models.MoreComments "praw.models.MoreComments") instances that represent a minimum number of comments; it
defaults to `0`, meaning all [`MoreComments`](https://praw.readthedocs.io/en/stable/code_overview/models/more.html#praw.models.MoreComments "praw.models.MoreComments") instances will be replaced up to
`limit`.

A `limit` of `0` simply removes all [`MoreComments`](https://praw.readthedocs.io/en/stable/code_overview/models/more.html#praw.models.MoreComments "praw.models.MoreComments") from the forest. The
previous snippet can thus be simplified:

```python
submission.comments.replace_more(limit=0)
for top_level_comment in submission.comments:
    print(top_level_comment.body)
```

Note

Calling [`replace_more()`](https://praw.readthedocs.io/en/stable/code_overview/other/commentforest.html#praw.models.comment_forest.CommentForest.replace_more "praw.models.comment_forest.CommentForest.replace_more") is destructive. Calling it again on the same
submission instance has no effect.

Meanwhile, a `limit` of `None` means that all [`MoreComments`](https://praw.readthedocs.io/en/stable/code_overview/models/more.html#praw.models.MoreComments "praw.models.MoreComments") objects will be
replaced until there are none left, as long as they satisfy the `threshold`.

```python
submission.comments.replace_more(limit=None)
for top_level_comment in submission.comments:
    print(top_level_comment.body)
```

Now we are able to successfully iterate over all the top-level comments. What about
their replies? We could output all second-level comments like so:

```python
submission.comments.replace_more(limit=None)
for top_level_comment in submission.comments:
    for second_level_comment in top_level_comment.replies:
        print(second_level_comment.body)
```

However, the comment forest can be arbitrarily deep, so we'll want a more robust
solution. One way to iterate over a tree, or forest, is via a breadth-first traversal
using a queue:

```python
submission.comments.replace_more(limit=None)
comment_queue = submission.comments[:]  # Seed with top-level
while comment_queue:
    comment = comment_queue.pop(0)
    print(comment.body)
    comment_queue.extend(comment.replies)
```

The above code will output all the top-level comments, followed by second-level,
third-level, etc. While it is awesome to be able to do your own breadth-first
traversals, [`CommentForest`](https://praw.readthedocs.io/en/stable/code_overview/other/commentforest.html#praw.models.comment_forest.CommentForest "praw.models.comment_forest.CommentForest") provides a convenience method, [`list()`](https://praw.readthedocs.io/en/stable/code_overview/other/commentforest.html#praw.models.comment_forest.CommentForest.list "praw.models.comment_forest.CommentForest.list"), which
returns a list of comments traversed in the same order as the code above. Thus the above
can be rewritten as:

```python
submission.comments.replace_more(limit=None)
for comment in submission.comments.list():
    print(comment.body)
```

You can now properly extract and parse all (or most) of the comments belonging to a
single submission. Combine this with [submission iteration](https://praw.readthedocs.io/en/stable/getting_started/quick_start.html#submission-iteration)
and you can build some really cool stuff.

Finally, note that the value of `submission.num_comments` may not match up 100% with
the number of comments extracted via PRAW. This discrepancy is normal as that count
includes deleted, removed, and spam comments.