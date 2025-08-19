# Glossary

- `Access Token`: A temporary token to allow access to the Reddit API. Lasts for one
hour.

- `Creddit`: Back when the only award was `Reddit Gold`, a creddit was equal to one
month of Reddit Gold. Creddits have been converted to `Reddit Coins`. See [this](https://praw.readthedocs.io/en/stable/package_info/glossary.html#gild) for more info about the old Reddit Gold system.

- `Fullname`: The fullname of an object is the object's type followed by an underscore
and its base-36 id. An example would be `t3_1h4f3`, where the `t3` signals that it
is a [`Submission`](https://praw.readthedocs.io/en/stable/code_overview/models/submission.html#praw.models.Submission "praw.models.Submission"), and the submission ID is `1h4f3`.

Here is a list of the six different types of objects returned from Reddit:

  - `t1` These object represent [`Comment`](https://praw.readthedocs.io/en/stable/code_overview/models/comment.html#praw.models.Comment "praw.models.Comment") s.
  - `t2` These object represent [`Redditor`](https://praw.readthedocs.io/en/stable/code_overview/models/redditor.html#praw.models.Redditor "praw.models.Redditor") s.
  - `t3` These object represent [`Submission`](https://praw.readthedocs.io/en/stable/code_overview/models/submission.html#praw.models.Submission "praw.models.Submission") s.
  - `t4` These object represent [`Message`](https://praw.readthedocs.io/en/stable/code_overview/models/message.html#praw.models.Message "praw.models.Message") s.
  - `t5` These object represent [`Subreddit`](https://praw.readthedocs.io/en/stable/code_overview/models/subreddit.html#praw.models.Subreddit "praw.models.Subreddit") s.
  - `t6` These object represent `Award` s, such as `Reddit Gold` or `Reddit
    Silver`.

- `Gild`: Back when the only award was `Reddit Gold`, gilding a post meant awarding
one month of Reddit Gold. Currently, gilding means awarding one month of `Reddit
Platinum`, or giving a `Platinum` award.

- `Websocket`: A special connection type that supports both a client and a server (the
running program and Reddit respectively) sending multiple messages to each other.
Reddit uses websockets to notify clients when an image or video submission is
completed, as well as certain types of asset uploads, such as subreddit banners.