# Configuration Options

PRAW's configuration options are broken down into the following categories:

- [Basic Configuration Options](https://praw.readthedocs.io/en/stable/getting_started/configuration/options.html#basic-options)
- [OAuth Configuration Options](https://praw.readthedocs.io/en/stable/getting_started/configuration/options.html#oauth-options)
- [Reddit Site Configuration Options](https://praw.readthedocs.io/en/stable/getting_started/configuration/options.html#site-options)
- [Miscellaneous Configuration Options](https://praw.readthedocs.io/en/stable/getting_started/configuration/options.html#misc-options)
- [Custom Configuration Options](https://praw.readthedocs.io/en/stable/getting_started/configuration/options.html#custom-options)

All of these options can be provided in any of the ways mentioned in
[Configuring PRAW](https://praw.readthedocs.io/en/stable/getting_started/configuration.html#configuration).

## Basic Configuration Options

check_for_updates:

When `true`, check for new versions of PRAW. When a newer version
of PRAW is available a message is reported via standard error (default: `true`).

user_agent:

(Required) A unique description of your application. The following format
is recommended according to [Reddit's API Rules](https://github.com/reddit/reddit/wiki/API#rules): `<platform>:<app ID>:<version
string> (by u/<reddit username>)`.

## OAuth Configuration Options

client_id:

(Required) The OAuth client ID associated with your registered Reddit
application. See [Authenticating via OAuth](https://praw.readthedocs.io/en/stable/getting_started/authentication.html#oauth) for instructions on registering a Reddit application.

client_secret:

The OAuth client secret associated with your registered Reddit
application. This option is required for all application types, however, the value
must be set to `None` for **installed** applications.

redirect_uri:

The redirect URI associated with your registered Reddit application. This
field is unused for **script** applications and is only needed for both **web**
applications, and **installed** applications when the [`url()`](https://praw.readthedocs.io/en/stable/code_overview/other/auth.html#praw.models.Auth.url "praw.models.Auth.url") method is used.

password:

The password of the Reddit account associated with your registered Reddit
**script** application. This field is required for **script** applications, and PRAW
assumes it is working with a **script** application by its presence.

username:

The username of the Reddit account associated with your registered Reddit
**script** application. This field is required for **script** applications, and PRAW
assumes it is working with a **script** application by its presence.

## Reddit Site Configuration Options

PRAW can be configured to work with instances of Reddit which are not hosted at
[reddit.com](https://www.reddit.com/). The following options may need to be updated in
order to successfully access a third-party Reddit site:

comment_kind:

The type prefix for comments on the [`Reddit`](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit") instance (default:
`t1_`).

message_kind:

The type prefix for messages on the [`Reddit`](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit") instance (default:
`t4_`).

oauth_url:

The URL used to access the [`Reddit`](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit") instance's API (default:
`https://oauth.reddit.com`).

reddit_url:

The URL used to access the [`Reddit`](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit") instance. PRAW assumes the
endpoints for establishing OAuth authorization are accessible under this URL
(default: `https://www.reddit.com`).

redditor_kind:

The type prefix for redditors on the [`Reddit`](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit") instance (default:
`t2_`).

short_url:

The URL used to generate short links on the [`Reddit`](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit") instance
(default: `https://redd.it`).

submission_kind:

The type prefix for submissions on the [`Reddit`](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit") instance
(default: `t3_`).

subreddit_kind:

The type prefix for subreddits on the [`Reddit`](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit") instance
(default: `t5_`).

## Miscellaneous Configuration Options

These are options that do not belong in another category, but still play a part in PRAW.

check_for_async:

When `true`, check if PRAW is being ran in an asynchronous
environment whenever a request is made. If so, a warning will be logged recommending
the usage of [Async PRAW](https://asyncpraw.readthedocs.io/) (default: `true`).

ratelimit_seconds:

Controls the maximum number of seconds PRAW will capture ratelimits
returned in JSON data. Because this can be as high as 14 minutes, only ratelimits of
up to 5 seconds are captured and waited on by default.

Note

PRAW sleeps for the ratelimit value plus 1 second.

See [Ratelimits](https://praw.readthedocs.io/en/stable/getting_started/ratelimits.html#ratelimits) for more info.

timeout:

Controls the amount of time PRAW will wait for a request from Reddit to
complete before throwing an exception. By default, PRAW waits 16 seconds before
throwing an exception.

warn_comment_sort:

When `true`, log a warning when the `comment_sort` attribute of
a submission is updated after `_fetch()` has been called (default: `true`).

## Custom Configuration Options

Your application can utilize PRAW's configuration system in order to provide its own
custom settings.

For instance you might want to add an `app_debugging: true` option to your
application's `praw.ini` file. To retrieve the value of this custom option from an
instance of [`Reddit`](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit") you can execute:

```python
reddit.config.custom["app_debugging"]
```

Note

Custom PRAW configuration environment variables are not supported. You can directly
access environment variables via `os.getenv`.