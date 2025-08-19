# Keyword Arguments to `Reddit`

Most of PRAW's documentation will demonstrate configuring PRAW through the use of
keyword arguments when initializing instances of [`Reddit`](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit"). All of the
[Configuration Options](https://praw.readthedocs.io/en/stable/getting_started/configuration/options.html#configuration-options) can be specified using a keyword argument of the same name.

For example, if we wanted to explicitly pass the information for `bot3` defined in
[the praw.ini custom site example](https://praw.readthedocs.io/en/stable/getting_started/configuration/prawini.html#custom-site-example) without using the `bot3`
site, we would initialize [`Reddit`](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit") as:

```python
reddit = praw.Reddit(
    client_id="SI8pN3DSbt0zor",
    client_secret="xaxkj7HNh8kwg8e5t4m6KvSrbTI",
    password="1guiwevlfo00esyy",
    user_agent="testscript by u/fakebot3",
    username="fakebot3",
)
```