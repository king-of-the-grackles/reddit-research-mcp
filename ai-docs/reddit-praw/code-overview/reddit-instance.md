# The Reddit Instance

_class_ praw.Reddit( _site\_name:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_, _\*_, _config\_interpolation:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_, _requestor\_class:[Type](https://docs.python.org/3/library/typing.html#typing.Type "(in Python v3.11)")\[Requestor\]\| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_, _requestor\_kwargs:[Dict](https://docs.python.org/3/library/typing.html#typing.Dict "(in Python v3.11)")\[ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)"), [Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")\]\| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_, _token\_manager:[BaseTokenManager](https://praw.readthedocs.io/en/stable/code_overview/other/token_manager.html#praw.util.token_manager.BaseTokenManager "praw.util.token_manager.BaseTokenManager") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_, _\*\*config\_settings:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.11)") \| [int](https://docs.python.org/3/library/functions.html#int "(in Python v3.11)") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")_)

The Reddit class provides convenient access to Reddit's API.

Instances of this class are the gateway to interacting with Reddit's API through
PRAW. The canonical way to obtain an instance of this class is via:

```python
import praw

reddit = praw.Reddit(
    client_id="CLIENT_ID",
    client_secret="CLIENT_SECRET",
    password="PASSWORD",
    user_agent="USERAGENT",
    username="USERNAME",
)
```

## Initialization

\_\_init\_\_( _site\_name:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_, _\*_, _config\_interpolation:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_, _requestor\_class:[Type](https://docs.python.org/3/library/typing.html#typing.Type "(in Python v3.11)")\[Requestor\]\| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_, _requestor\_kwargs:[Dict](https://docs.python.org/3/library/typing.html#typing.Dict "(in Python v3.11)")\[ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)"), [Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")\]\| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_, _token\_manager:[BaseTokenManager](https://praw.readthedocs.io/en/stable/code_overview/other/token_manager.html#praw.util.token_manager.BaseTokenManager "praw.util.token_manager.BaseTokenManager") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_, _\*\*config\_settings:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.11)") \| [int](https://docs.python.org/3/library/functions.html#int "(in Python v3.11)") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")_)

Initialize a [`Reddit`](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit") instance.

Parameters:

- **site\_name** – The name of a section in your `praw.ini` file from which to
load settings from. This parameter, in tandem with an appropriately
configured `praw.ini`, file is useful if you wish to easily save
credentials for different applications, or communicate with other servers
running Reddit. If `site_name` is `None`, then the site name will be
looked for in the environment variable `praw_site`. If it is not found
there, the `DEFAULT` site will be used (default: `None`).

- **config\_interpolation** – Config parser interpolation type that will be
passed to [`Config`](https://praw.readthedocs.io/en/stable/code_overview/other/config.html#praw.config.Config "praw.config.Config") (default: `None`).

- **requestor\_class** – A class that will be used to create a requestor. If not
set, use `prawcore.Requestor` (default: `None`).

- **requestor\_kwargs** – Dictionary with additional keyword arguments used to
initialize the requestor (default: `None`).

- **token\_manager** – When provided, the passed instance, a subclass of
[`BaseTokenManager`](https://praw.readthedocs.io/en/stable/code_overview/other/token_manager.html#praw.util.token_manager.BaseTokenManager "praw.util.token_manager.BaseTokenManager"), will manage tokens via two callback functions.
This parameter must be provided in order to work with refresh tokens
(default: `None`).


Additional keyword arguments will be used to initialize the [`Config`](https://praw.readthedocs.io/en/stable/code_overview/other/config.html#praw.config.Config "praw.config.Config")
object. This can be used to specify configuration settings during instantiation
of the [`Reddit`](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit") instance. For more details, please see
[Configuring PRAW](https://praw.readthedocs.io/en/stable/getting_started/configuration.html#configuration).

Required settings are:

- `client_id`
- `client_secret` (for installed applications set this value to `None`)
- `user_agent`

The `requestor_class` and `requestor_kwargs` allow for customization of the
requestor [`Reddit`](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit") will use. This allows, e.g., easily adding behavior
to the requestor or wrapping its [`Session`](https://2.python-requests.org/en/master/api/#requests.Session) in a caching layer. Example usage:

```python
import json

import betamax
import requests
from prawcore import Requestor

from praw import Reddit

class JSONDebugRequestor(Requestor):
    def request(self, *args, **kwargs):
        response = super().request(*args, **kwargs)
        print(json.dumps(response.json(), indent=4))
        return response

my_session = betamax.Betamax(requests.Session())
reddit = Reddit(
    ..., requestor_class=JSONDebugRequestor, requestor_kwargs={"session": my_session}
)
```

## Properties and Attributes

### auth

An instance of [`Auth`](https://praw.readthedocs.io/en/stable/code_overview/other/auth.html#praw.models.Auth "praw.models.Auth").

Provides the interface for interacting with installed and web applications.

See also

[Obtain the Authorization URL](https://praw.readthedocs.io/en/stable/getting_started/authentication.html#auth-url)

### drafts

An instance of [`DraftHelper`](https://praw.readthedocs.io/en/stable/code_overview/reddit/drafts.html#praw.models.DraftHelper "praw.models.DraftHelper").

Provides the interface for working with [`Draft`](https://praw.readthedocs.io/en/stable/code_overview/models/draft.html#praw.models.Draft "praw.models.Draft") instances.

For example, to list the currently authenticated user's drafts:

```python
drafts = reddit.drafts()
```

To create a draft on r/test run:

```python
reddit.drafts.create(title="title", selftext="selftext", subreddit="test")
```

### front

An instance of [`Front`](https://praw.readthedocs.io/en/stable/code_overview/reddit/front.html#praw.models.Front "praw.models.Front").

Provides the interface for interacting with front page listings. For example:

```python
for submission in reddit.front.hot():
    print(submission)
```

### inbox

An instance of [`Inbox`](https://praw.readthedocs.io/en/stable/code_overview/reddit/inbox.html#praw.models.Inbox "praw.models.Inbox").

Provides the interface to a user's inbox which produces [`Message`](https://praw.readthedocs.io/en/stable/code_overview/models/message.html#praw.models.Message "praw.models.Message"),
[`Comment`](https://praw.readthedocs.io/en/stable/code_overview/models/comment.html#praw.models.Comment "praw.models.Comment"), and [`Submission`](https://praw.readthedocs.io/en/stable/code_overview/models/submission.html#praw.models.Submission "praw.models.Submission") instances. For example, to iterate
through comments which mention the authorized user run:

```python
for comment in reddit.inbox.mentions():
    print(comment)
```

### live

An instance of [`LiveHelper`](https://praw.readthedocs.io/en/stable/code_overview/reddit/live.html#praw.models.LiveHelper "praw.models.LiveHelper").

Provides the interface for working with [`LiveThread`](https://praw.readthedocs.io/en/stable/code_overview/models/livethread.html#praw.models.LiveThread "praw.models.LiveThread") instances. At
present only new live threads can be created.

```python
reddit.live.create(title="title", description="description")
```

### multireddit

An instance of [`MultiredditHelper`](https://praw.readthedocs.io/en/stable/code_overview/reddit/multireddit.html#praw.models.MultiredditHelper "praw.models.MultiredditHelper").

Provides the interface to working with [`Multireddit`](https://praw.readthedocs.io/en/stable/code_overview/models/multireddit.html#praw.models.Multireddit "praw.models.Multireddit") instances. For
example, you can obtain a [`Multireddit`](https://praw.readthedocs.io/en/stable/code_overview/models/multireddit.html#praw.models.Multireddit "praw.models.Multireddit") instance via:

```python
reddit.multireddit(redditor="samuraisam", name="programming")
```

### notes

An instance of [`RedditModNotes`](https://praw.readthedocs.io/en/stable/code_overview/other/reddit_mod_notes.html#praw.models.RedditModNotes "praw.models.RedditModNotes").

Provides the interface for working with [`ModNote`](https://praw.readthedocs.io/en/stable/code_overview/other/mod_note.html#praw.models.ModNote "praw.models.ModNote") s for multiple
redditors across multiple subreddits.

Note

The authenticated user must be a moderator of the provided subreddit(s).

For example, the latest note for u/spez in r/redditdev and r/test, and for
u/bboe in r/redditdev can be iterated through like so:

```python
redditor = reddit.redditor("bboe")
subreddit = reddit.subreddit("redditdev")

pairs = [(subreddit, "spez"), ("test", "spez"), (subreddit, redditor)]

for note in reddit.notes(pairs=pairs):
    print(f"{note.label}: {note.note}")
```

### read_only

Return `True` when using the `ReadOnlyAuthorizer`.

### redditors

An instance of [`Redditors`](https://praw.readthedocs.io/en/stable/code_overview/reddit/redditors.html#praw.models.Redditors "praw.models.Redditors").

Provides the interface for [`Redditor`](https://praw.readthedocs.io/en/stable/code_overview/models/redditor.html#praw.models.Redditor "praw.models.Redditor") discovery. For example, to iterate
over the newest Redditors, run:

```python
for redditor in reddit.redditors.new(limit=None):
    print(redditor)
```

### subreddit

An instance of [`SubredditHelper`](https://praw.readthedocs.io/en/stable/code_overview/reddit/subreddit.html#praw.models.SubredditHelper "praw.models.SubredditHelper").

Provides the interface to working with [`Subreddit`](https://praw.readthedocs.io/en/stable/code_overview/models/subreddit.html#praw.models.Subreddit "praw.models.Subreddit") instances. For
example to create a [`Subreddit`](https://praw.readthedocs.io/en/stable/code_overview/models/subreddit.html#praw.models.Subreddit "praw.models.Subreddit") run:

```python
reddit.subreddit.create(name="coolnewsubname")
```

To obtain a lazy [`Subreddit`](https://praw.readthedocs.io/en/stable/code_overview/models/subreddit.html#praw.models.Subreddit "praw.models.Subreddit") instance run:

```python
reddit.subreddit("test")
```

Multiple subreddits can be combined and filtered views of r/all can also be used
just like a subreddit:

```python
reddit.subreddit("redditdev+learnpython+botwatch")
reddit.subreddit("all-redditdev-learnpython")
```

### subreddits

An instance of [`Subreddits`](https://praw.readthedocs.io/en/stable/code_overview/reddit/subreddits.html#praw.models.Subreddits "praw.models.Subreddits").

Provides the interface for [`Subreddit`](https://praw.readthedocs.io/en/stable/code_overview/models/subreddit.html#praw.models.Subreddit "praw.models.Subreddit") discovery. For example, to
iterate over the set of default subreddits run:

```python
for subreddit in reddit.subreddits.default(limit=None):
    print(subreddit)
```

### user

An instance of [`User`](https://praw.readthedocs.io/en/stable/code_overview/reddit/user.html#praw.models.User "praw.models.User").

Provides the interface to the currently authorized [`Redditor`](https://praw.readthedocs.io/en/stable/code_overview/models/redditor.html#praw.models.Redditor "praw.models.Redditor"). For
example to get the name of the current user run:

```python
print(reddit.user.me())
```

### validate_on_submit

Get validate\_on\_submit.

Deprecated since version 7.0: If property [`validate_on_submit`](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit.validate_on_submit "praw.Reddit.validate_on_submit") is set to `False`, the behavior is
deprecated by Reddit. This attribute will be removed around May-June 2020.

## Methods

### comment()

comment( _id:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_, _\*_, _url:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_)

Return a lazy instance of [`Comment`](https://praw.readthedocs.io/en/stable/code_overview/models/comment.html#praw.models.Comment "praw.models.Comment").

Parameters:

- **id** – The ID of the comment.
- **url** – A permalink pointing to the comment.

Note

If you want to obtain the comment's replies, you will need to call
[`refresh()`](https://praw.readthedocs.io/en/stable/code_overview/models/comment.html#praw.models.Comment.refresh "praw.models.Comment.refresh") on the returned [`Comment`](https://praw.readthedocs.io/en/stable/code_overview/models/comment.html#praw.models.Comment "praw.models.Comment").

### delete()

delete( _path:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_, _\*_, _data:[Dict](https://docs.python.org/3/library/typing.html#typing.Dict "(in Python v3.11)")\[ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)"), [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")\]\| [bytes](https://docs.python.org/3/library/stdtypes.html#bytes "(in Python v3.11)") \| [IO](https://docs.python.org/3/library/typing.html#typing.IO "(in Python v3.11)") \| [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_, _json:[Dict](https://docs.python.org/3/library/typing.html#typing.Dict "(in Python v3.11)")\[ [Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)"), [Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")\]\| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_, _params:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [Dict](https://docs.python.org/3/library/typing.html#typing.Dict "(in Python v3.11)")\[ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)"), [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")\]\| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_)

Return parsed objects returned from a DELETE request to `path`.

Parameters:

- **path** – The path to fetch.
- **data** – Dictionary, bytes, or file-like object to send in the body of the
request (default: `None`).
- **json** – JSON-serializable object to send in the body of the request with a
Content-Type header of application/json (default: `None`). If `json` is
provided, `data` should not be.
- **params** – The query parameters to add to the request (default: `None`).

### domain()

domain( _domain:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_)

Return an instance of [`DomainListing`](https://praw.readthedocs.io/en/stable/code_overview/other/domainlisting.html#praw.models.DomainListing "praw.models.DomainListing").

Parameters:

**domain** – The domain to obtain submission listings for.

### get()

get( _path:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_, _\*_, _params:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [Dict](https://docs.python.org/3/library/typing.html#typing.Dict "(in Python v3.11)")\[ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)"), [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [int](https://docs.python.org/3/library/functions.html#int "(in Python v3.11)")\]\| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_)

Return parsed objects returned from a GET request to `path`.

Parameters:

- **path** – The path to fetch.
- **params** – The query parameters to add to the request (default: `None`).

### info()

info( _\*_, _fullnames:[Iterable](https://docs.python.org/3/library/typing.html#typing.Iterable "(in Python v3.11)")\[ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")\]\| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_, _subreddits:[Iterable](https://docs.python.org/3/library/typing.html#typing.Iterable "(in Python v3.11)")\[ [praw.models.Subreddit](https://praw.readthedocs.io/en/stable/code_overview/models/subreddit.html#praw.models.Subreddit "praw.models.Subreddit") \| [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")\]\| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_, _url:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_)

Fetch information about each item in `fullnames`, `url`, or `subreddits`.

Parameters:

- **fullnames** – A list of fullnames for comments, submissions, and/or
subreddits.
- **subreddits** – A list of subreddit names or [`Subreddit`](https://praw.readthedocs.io/en/stable/code_overview/models/subreddit.html#praw.models.Subreddit "praw.models.Subreddit") objects to
retrieve subreddits from.
- **url** – A url (as a string) to retrieve lists of link submissions from.

Returns:

A generator that yields found items in their relative order.

Items that cannot be matched will not be generated. Requests will be issued in
batches for each 100 fullnames.

Note

For comments that are retrieved via this method, if you want to obtain its
replies, you will need to call [`refresh()`](https://praw.readthedocs.io/en/stable/code_overview/models/comment.html#praw.models.Comment.refresh "praw.models.Comment.refresh") on the yielded
[`Comment`](https://praw.readthedocs.io/en/stable/code_overview/models/comment.html#praw.models.Comment "praw.models.Comment").

Note

When using the URL option, it is important to be aware that URLs are treated
literally by Reddit's API. As such, the URLs `"youtube.com"` and
`"https://www.youtube.com"` will provide a different set of submissions.

### patch(), post(), put(), request()

[Additional HTTP methods with similar parameter patterns...]

### random_subreddit()

random\_subreddit( _\*_, _nsfw:[bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.11)")=False_)

Return a random lazy instance of [`Subreddit`](https://praw.readthedocs.io/en/stable/code_overview/models/subreddit.html#praw.models.Subreddit "praw.models.Subreddit").

Parameters:

**nsfw** – Return a random NSFW (not safe for work) subreddit (default:
`False`).

### redditor()

redditor( _name:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_, _\*_, _fullname:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_)

Return a lazy instance of [`Redditor`](https://praw.readthedocs.io/en/stable/code_overview/models/redditor.html#praw.models.Redditor "praw.models.Redditor").

Parameters:

- **name** – The name of the redditor.
- **fullname** – The fullname of the redditor, starting with `t2_`.

Either `name` or `fullname` can be provided, but not both.

### submission()

submission( _id:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_, _\*_, _url:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_)

Return a lazy instance of [`Submission`](https://praw.readthedocs.io/en/stable/code_overview/models/submission.html#praw.models.Submission "praw.models.Submission").

Parameters:

- **id** – A Reddit base36 submission ID, e.g., `"2gmzqe"`.
- **url** – A URL supported by [`Submission.id_from_url()`](https://praw.readthedocs.io/en/stable/code_overview/models/submission.html#praw.models.Submission.id_from_url "praw.models.Submission.id_from_url").

Either `id` or `url` can be provided, but not both.

### username_available()

username\_available( _name:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_)

Check to see if the username is available.

For example, to check if the username `bboe` is available, try:

```python
reddit.username_available("bboe")
```

## Helper Classes

The Reddit instance provides access to various helper classes:

- [reddit.drafts](https://praw.readthedocs.io/en/stable/code_overview/reddit/drafts.html) - [`DraftHelper`](https://praw.readthedocs.io/en/stable/code_overview/reddit/drafts.html#praw.models.DraftHelper)
- [reddit.front](https://praw.readthedocs.io/en/stable/code_overview/reddit/front.html) - [`Front`](https://praw.readthedocs.io/en/stable/code_overview/reddit/front.html#praw.models.Front)
- [reddit.inbox](https://praw.readthedocs.io/en/stable/code_overview/reddit/inbox.html) - [`Inbox`](https://praw.readthedocs.io/en/stable/code_overview/reddit/inbox.html#praw.models.Inbox)
- [reddit.live](https://praw.readthedocs.io/en/stable/code_overview/reddit/live.html) - [`LiveHelper`](https://praw.readthedocs.io/en/stable/code_overview/reddit/live.html#praw.models.LiveHelper)
- [reddit.multireddit](https://praw.readthedocs.io/en/stable/code_overview/reddit/multireddit.html) - [`MultiredditHelper`](https://praw.readthedocs.io/en/stable/code_overview/reddit/multireddit.html#praw.models.MultiredditHelper)
- [reddit.redditors](https://praw.readthedocs.io/en/stable/code_overview/reddit/redditors.html) - [`Redditors`](https://praw.readthedocs.io/en/stable/code_overview/reddit/redditors.html#praw.models.Redditors)
- [reddit.subreddit](https://praw.readthedocs.io/en/stable/code_overview/reddit/subreddit.html) - [`SubredditHelper`](https://praw.readthedocs.io/en/stable/code_overview/reddit/subreddit.html#praw.models.SubredditHelper)
- [reddit.subreddits](https://praw.readthedocs.io/en/stable/code_overview/reddit/subreddits.html) - [`Subreddits`](https://praw.readthedocs.io/en/stable/code_overview/reddit/subreddits.html#praw.models.Subreddits)
- [reddit.user](https://praw.readthedocs.io/en/stable/code_overview/reddit/user.html) - [`User`](https://praw.readthedocs.io/en/stable/code_overview/reddit/user.html#praw.models.User)