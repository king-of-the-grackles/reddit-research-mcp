# Subreddit

_class_ praw.models.Subreddit( _reddit:[praw.Reddit](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit")_, _display\_name:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_, _\_data:[Dict](https://docs.python.org/3/library/typing.html#typing.Dict "(in Python v3.11)")\[ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)"), [Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")\]\| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_)

A class for Subreddits.

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
| `can_assign_link_flair` | Whether or not the authenticated user can assign link flair. |
| `can_assign_user_flair` | Whether or not the authenticated user can assign user flair. |
| `created_utc` | Time the subreddit was created, represented in [Unix Time](https://en.wikipedia.org/wiki/Unix_time). |
| `description` | Description of the subreddit. |
| `description_html` | Description of the subreddit, as HTML. |
| `display_name` | Name of the subreddit. |
| `id` | The subreddit's ID. |
| `name` | The subreddit's fullname. |
| `over18` | Whether or not the subreddit is NSFW. |
| `public_description` | Description of the subreddit shown in searches and on the "You must be invited to visit this community" page. |
| `spoilers_enabled` | Whether or not the subreddit has spoilers enabled. |
| `subscribers` | Count of subscribers. |
| `user_can_flair_in_sr` | Whether or not the authenticated user can edit their flair in this subreddit. |
| `user_flair_text` | The authenticated user's flair text. |
| `user_has_favorited` | Whether or not the authenticated user has favorited the subreddit. |
| `user_is_banned` | Whether or not the authenticated user is banned from the subreddit. |
| `user_is_moderator` | Whether or not the authenticated user is a moderator of the subreddit. |
| `user_is_subscriber` | Whether or not the authenticated user is subscribed to the subreddit. |

## Key Methods

### submit( _title:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_, _\*\*kwargs_)→[praw.models.Submission](https://praw.readthedocs.io/en/stable/code_overview/models/submission.html#praw.models.Submission "praw.models.Submission")
Add a submission to the Subreddit.

Parameters:
- **title** – The title of the submission.

Returns: A [`Submission`](https://praw.readthedocs.io/en/stable/code_overview/models/submission.html#praw.models.Submission "praw.models.Submission") object for the newly created submission.

Example usage:
```python
# Submit a selfpost
submission = subreddit.submit(title="My Title", selftext="My content")

# Submit a link
submission = subreddit.submit(title="My Title", url="https://example.com")
```

### subscribe( _other\_subreddits:[List](https://docs.python.org/3/library/typing.html#typing.List "(in Python v3.11)")\[ [praw.models.Subreddit](https://praw.readthedocs.io/en/stable/code_overview/models/subreddit.html#praw.models.Subreddit "praw.models.Subreddit")\]\| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_)
Subscribe to the subreddit.

Parameters:
- **other\_subreddits** – When provided, also subscribe to this list of subreddits.

Example usage:
```python
subreddit.subscribe()
```

### unsubscribe( _other\_subreddits:[List](https://docs.python.org/3/library/typing.html#typing.List "(in Python v3.11)")\[ [praw.models.Subreddit](https://praw.readthedocs.io/en/stable/code_overview/models/subreddit.html#praw.models.Subreddit "praw.models.Subreddit")\]\| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_)
Unsubscribe from the subreddit.

Parameters:
- **other\_subreddits** – When provided, also unsubscribe from this list of subreddits.

Example usage:
```python
subreddit.unsubscribe()
```

### search( _query:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_, _\*_, _sort:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")='relevance'_, _time\_filter:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")='all'_, _\*\*generator\_kwargs_)→[Iterator](https://docs.python.org/3/library/typing.html#typing.Iterator "(in Python v3.11)")\[ [praw.models.Submission](https://praw.readthedocs.io/en/stable/code_overview/models/submission.html#praw.models.Submission "praw.models.Submission")\]
Return a [`ListingGenerator`](https://praw.readthedocs.io/en/stable/code_overview/other/listinggenerator.html#praw.models.ListingGenerator "praw.models.ListingGenerator") for items that match query.

Parameters:
- **query** – The query string to search for.
- **sort** – Can be one of: `"relevance"`, `"hot"`, `"top"`, `"new"`, or `"comments"` (default: `"relevance"`).
- **time\_filter** – Can be one of: `"all"`, `"day"`, `"hour"`, `"month"`, `"week"`, or `"year"` (default: `"all"`).

Example usage:
```python
for submission in subreddit.search("python", limit=10):
    print(submission.title)
```

### hot( _\*\*generator\_kwargs_)→[Iterator](https://docs.python.org/3/library/typing.html#typing.Iterator "(in Python v3.11)")\[ [praw.models.Submission](https://praw.readthedocs.io/en/stable/code_overview/models/submission.html#praw.models.Submission "praw.models.Submission")\]
Return a [`ListingGenerator`](https://praw.readthedocs.io/en/stable/code_overview/other/listinggenerator.html#praw.models.ListingGenerator "praw.models.ListingGenerator") for hot items.

Example usage:
```python
for submission in subreddit.hot(limit=5):
    print(submission.title)
```

### new( _\*\*generator\_kwargs_)→[Iterator](https://docs.python.org/3/library/typing.html#typing.Iterator "(in Python v3.11)")\[ [praw.models.Submission](https://praw.readthedocs.io/en/stable/code_overview/models/submission.html#praw.models.Submission "praw.models.Submission")\]
Return a [`ListingGenerator`](https://praw.readthedocs.io/en/stable/code_overview/other/listinggenerator.html#praw.models.ListingGenerator "praw.models.ListingGenerator") for new items.

Example usage:
```python
for submission in subreddit.new(limit=10):
    print(submission.title)
```

### top( _\*_, _time\_filter:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")='all'_, _\*\*generator\_kwargs_)→[Iterator](https://docs.python.org/3/library/typing.html#typing.Iterator "(in Python v3.11)")\[ [praw.models.Submission](https://praw.readthedocs.io/en/stable/code_overview/models/submission.html#praw.models.Submission "praw.models.Submission")\]
Return a [`ListingGenerator`](https://praw.readthedocs.io/en/stable/code_overview/other/listinggenerator.html#praw.models.ListingGenerator "praw.models.ListingGenerator") for top items.

Parameters:
- **time\_filter** – Can be one of: `"all"`, `"day"`, `"hour"`, `"month"`, `"week"`, or `"year"` (default: `"all"`).

Example usage:
```python
for submission in subreddit.top(time_filter="week", limit=5):
    print(submission.title)
```

### controversial( _\*_, _time\_filter:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")='all'_, _\*\*generator\_kwargs_)→[Iterator](https://docs.python.org/3/library/typing.html#typing.Iterator "(in Python v3.11)")\[ [praw.models.Submission](https://praw.readthedocs.io/en/stable/code_overview/models/submission.html#praw.models.Submission "praw.models.Submission")\]
Return a [`ListingGenerator`](https://praw.readthedocs.io/en/stable/code_overview/other/listinggenerator.html#praw.models.ListingGenerator "praw.models.ListingGenerator") for controversial items.

Parameters:
- **time\_filter** – Can be one of: `"all"`, `"day"`, `"hour"`, `"month"`, `"week"`, or `"year"` (default: `"all"`).

Example usage:
```python
for submission in subreddit.controversial(time_filter="day", limit=5):
    print(submission.title)
```

### random()→[praw.models.Submission](https://praw.readthedocs.io/en/stable/code_overview/models/submission.html#praw.models.Submission "praw.models.Submission") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")
Return a random [`Submission`](https://praw.readthedocs.io/en/stable/code_overview/models/submission.html#praw.models.Submission "praw.models.Submission").

Returns: A [`Submission`](https://praw.readthedocs.io/en/stable/code_overview/models/submission.html#praw.models.Submission "praw.models.Submission") object, or `None` if unsuccessful.

Example usage:
```python
random_submission = subreddit.random()
```

### modmail()
Provide an instance of [`SubredditModmail`](https://praw.readthedocs.io/en/stable/code_overview/other/subredditmodmail.html#praw.models.reddit.subreddit.SubredditModmail "praw.models.reddit.subreddit.SubredditModmail").

Example usage:
```python
for conversation in subreddit.modmail.conversations():
    print(conversation.subject)
```

### wiki()
Provide an instance of [`SubredditWiki`](https://praw.readthedocs.io/en/stable/code_overview/other/subredditwiki.html#praw.models.reddit.subreddit.SubredditWiki "praw.models.reddit.subreddit.SubredditWiki").

Example usage:
```python
for page in subreddit.wiki:
    print(page)
```

### mod()
Provide an instance of [`SubredditModeration`](https://praw.readthedocs.io/en/stable/code_overview/other/subredditmoderation.html#praw.models.reddit.subreddit.SubredditModeration "praw.models.reddit.subreddit.SubredditModeration").

Example usage:
```python
for item in subreddit.mod.log():
    print(item)
```

### flair()
Provide an instance of [`SubredditFlair`](https://praw.readthedocs.io/en/stable/code_overview/other/subredditflair.html#praw.models.reddit.subreddit.SubredditFlair "praw.models.reddit.subreddit.SubredditFlair").

Example usage:
```python
for flair in subreddit.flair():
    print(flair)
```

Note: This is a condensed version of the Subreddit class documentation. The full documentation contains many more methods and detailed explanations. For complete information, visit the original PRAW documentation.