# PRAW Environment Variables

The second-highest priority configuration options can be passed to a program via
environment variables prefixed with `praw_`.

For example, you can invoke your script as follows:

```
praw_username=bboe praw_password=not_my_password python my_script.py
```

The `username` and `password` provided via environment variables will override any
values contained in a `praw.ini` file, but not any variables passed in through
[`Reddit`](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit").

All [Configuration Options](https://praw.readthedocs.io/en/stable/getting_started/configuration/options.html#configuration-options) can be provided in this manner, except for custom
options.