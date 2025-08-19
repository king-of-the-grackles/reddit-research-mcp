# Configuring PRAW

- [Configuration Options](https://praw.readthedocs.io/en/stable/getting_started/configuration/options.html)
  - [Basic Configuration Options](https://praw.readthedocs.io/en/stable/getting_started/configuration/options.html#basic-configuration-options)
  - [OAuth Configuration Options](https://praw.readthedocs.io/en/stable/getting_started/configuration/options.html#oauth-configuration-options)
  - [Reddit Site Configuration Options](https://praw.readthedocs.io/en/stable/getting_started/configuration/options.html#reddit-site-configuration-options)
  - [Miscellaneous Configuration Options](https://praw.readthedocs.io/en/stable/getting_started/configuration/options.html#miscellaneous-configuration-options)
  - [Custom Configuration Options](https://praw.readthedocs.io/en/stable/getting_started/configuration/options.html#custom-configuration-options)

Configuration options can be provided to PRAW in one of three ways:

- [praw.ini Files](https://praw.readthedocs.io/en/stable/getting_started/configuration/prawini.html)
- [Keyword Arguments to `Reddit`](https://praw.readthedocs.io/en/stable/getting_started/configuration/reddit_initialization.html)
- [PRAW Environment Variables](https://praw.readthedocs.io/en/stable/getting_started/configuration/environment_variables.html)

Environment variables have the highest priority, followed by keyword arguments to
[`Reddit`](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit"), and finally settings in `praw.ini` files.

## Using an HTTP or HTTPS proxy with PRAW

PRAW internally relies upon the [requests](https://requests.readthedocs.io/) package to handle HTTP requests. Requests
supports use of `HTTP_PROXY` and `HTTPS_PROXY` environment variables in order to
proxy HTTP and HTTPS requests respectively [ [ref](https://requests.readthedocs.io/en/master/user/advanced/#proxies)].

Given that PRAW exclusively communicates with Reddit via HTTPS, only the `HTTPS_PROXY`
option should be required.

For example, if you have a script named `prawbot.py`, the `HTTPS_PROXY` environment
variable can be provided on the command line like so:

```
HTTPS_PROXY=http://localhost:3128 ./prawbot.py
```

## Configuring a custom requests Session

PRAW uses [requests](https://requests.readthedocs.io/) to handle networking. If your use-case requires custom
configuration, it is possible to configure a custom [Session](https://2.python-requests.org/en/master/api/#requests.Session) instance and then use it
with PRAW.

For example, some networks use self-signed SSL certificates when connecting to HTTPS
sites. By default, this would raise an exception in [requests](https://requests.readthedocs.io/). To use a self-signed SSL
certificate without an exception from [requests](https://requests.readthedocs.io/), first export the certificate as a
`.pem` file. Then configure PRAW like so:

```python
import praw
from requests import Session

session = Session()
session.verify = "/path/to/certfile.pem"
reddit = praw.Reddit(
    client_id="SI8pN3DSbt0zor",
    client_secret="xaxkj7HNh8kwg8e5t4m6KvSrbTI",
    password="1guiwevlfo00esyy",
    requestor_kwargs={"session": session},  # pass the custom Session instance
    user_agent="testscript by u/fakebot3",
    username="fakebot3",
)
```

The code above creates a custom [Session](https://2.python-requests.org/en/master/api/#requests.Session) instance and [configures it to use a custom
certificate](https://requests.readthedocs.io/en/master/user/advanced/#ssl-cert-verification), then
passes it as a parameter when creating the [`Reddit`](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit") instance. Note that the
example above uses a [Password Flow](https://praw.readthedocs.io/en/stable/getting_started/authentication.html#password-flow) authentication type, but this method will work
for any authentication type.