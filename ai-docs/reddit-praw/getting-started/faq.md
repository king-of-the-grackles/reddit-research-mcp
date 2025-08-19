# Frequently Asked Questions

Q: How can I refresh a comment/subreddit/submission?

A: Directly calling the constructors will refresh the value:

```python
reddit.comment(comment.id)
reddit.subreddit(subreddit.display_name)
reddit.submission(submission.id)
```

Q: Whenever I try to do anything, I get an `invalid_grant` error. What is the cause?

A: This means that either you provided the wrong password and/or the account you are
trying to sign in with has 2FA enabled, and as such, either needs a 2FA token or a
refresh token to sign in. A refresh token is preferred, because then you will not need
to enter a 2FA token in order to sign in, and the session will last for longer than an
hour. Refer to [Two-Factor Authentication](https://praw.readthedocs.io/en/stable/getting_started/authentication.html#fa) and [Working with Refresh Tokens](https://praw.readthedocs.io/en/stable/tutorials/refresh_token.html#refresh-token) in order to use the respective auth
methods.

Q: Some options (like getting moderator logs from r/mod) keep on timing out. How can I
extend the timeout?

A: Set the timeout config option or initialize [`Reddit`](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit") with a timeout of your
choosing. Another option is to construct a [`Subreddit`](https://praw.readthedocs.io/en/stable/code_overview/models/subreddit.html#praw.models.Subreddit "praw.models.Subreddit") instance with a subset of
subreddits (concatenated with `+`) that you want logs from like so:

```python
reddit.subreddit("pics+LifeProTips")
```

Q: Help, I keep on getting redirected to `/r/subreddit/login/`!

Q2: I keep on getting this exception:

```
prawcore.exceptions.Redirect: Redirect to /r/subreddit/login/ (You may be trying to perform a non-read-only action via a read-only instance.)
```

A: PRAW is most likely in read-only mode. This normally occurs when PRAW is
authenticated without a username and password or a refresh token. In order to perform
this action, the [`Reddit`](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit") instance needs to be authenticated. See
[OAuth Configuration Options](https://praw.readthedocs.io/en/stable/getting_started/configuration/options.html#oauth-options) to see the available authentication methods.

Q: Help, searching for URLs keeps on redirecting me to `/submit`!

Q2: I keep on getting this exception: `prawcore.exceptions.Redirect: Redirect to
/submit`

A: Reddit redirects URL searches to the submit page of the URL. To search for the URL,
prefix `url:` to the url and surround the url in quotation marks.

For example, the code block:

```python
reddit.subreddit("all").search("https://google.com")
```

Will become this code block:

```python
reddit.subreddit("all").search('url:"https://google.com"')
```