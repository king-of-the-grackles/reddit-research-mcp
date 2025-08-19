# Authenticating via OAuth

PRAW supports all three types of applications that can be registered on Reddit. Those
are:

- [Web Applications](https://github.com/reddit-archive/reddit/wiki/OAuth2-App-Types#web-app)
- [Installed Applications](https://github.com/reddit-archive/reddit/wiki/OAuth2-App-Types#installed-app)
- [Script Applications](https://github.com/reddit-archive/reddit/wiki/OAuth2-App-Types#script-app)

Before you can use any one of these with PRAW, you must first [register](https://old.reddit.com/prefs/apps/) an application of the appropriate type on Reddit.

If your application does not require a user context, it is [read-only](https://praw.readthedocs.io/en/stable/getting_started/authentication.html#read-only-application).

PRAW supports the flows that each of these applications can use. The following table
defines which application types can use which flows:

| Application Type | Script | Web | Installed |
| --- | --- | --- | --- |
| Default Flow | [Password](https://praw.readthedocs.io/en/stable/getting_started/authentication.html#password-flow) | [Code](https://praw.readthedocs.io/en/stable/getting_started/authentication.html#code-flow) |
| Alternative Flows | [Code](https://praw.readthedocs.io/en/stable/getting_started/authentication.html#code-flow) | [Application-Only (Client Credentials)](https://praw.readthedocs.io/en/stable/getting_started/authentication.html#application-only-client-credentials-flow) | [Implicit](https://praw.readthedocs.io/en/stable/getting_started/authentication.html#implicit-flow) |
| [Application-Only (Client Credentials)](https://praw.readthedocs.io/en/stable/getting_started/authentication.html#application-only-client-credentials-flow) |
| [Application-Only (Installed Client)](https://praw.readthedocs.io/en/stable/getting_started/authentication.html#application-only-installed-client-flow) |

Warning

For the sake of brevity, the following examples pass authentication information via
arguments to [`Reddit`](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit"). If you do this, you need to be careful not to reveal
this information to the outside world if you share your code. It is recommended to
use a [praw.ini file](https://praw.readthedocs.io/en/stable/getting_started/configuration/prawini.html#praw-ini) in order to keep your authentication
information separate from your code.

## Password Flow

**Password Flow** is the simplest type of authentication flow to work with because no
callback process is involved in obtaining an `access_token`.

While **password flow** applications do not involve a redirect URI, Reddit still
requires that you provide one when registering your script application –
`http://localhost:8080` is a simple one to use.

In order to use a **password flow** application with PRAW you need four pieces of
information:

client_id:

The client ID is at least a 14-character string listed just under "personal
use script" for the desired [developed application](https://www.reddit.com/prefs/apps/)

client_secret:

The client secret is at least a 27-character string listed adjacent to
`secret` for the application.

password:

The password for the Reddit account used to register the application.

username:

The username of the Reddit account used to register the application.

With this information authorizing as `username` using a **password flow** app is as
simple as:

```python
reddit = praw.Reddit(
    client_id="SI8pN3DSbt0zor",
    client_secret="xaxkj7HNh8kwg8e5t4m6KvSrbTI",
    password="1guiwevlfo00esyy",
    user_agent="testscript by u/fakebot3",
    username="fakebot3",
)
```

To verify that you are authenticated as the correct user run:

```python
print(reddit.user.me())
```

The output should contain the same name as you entered for `username`.

Note

If the following exception is raised, double-check your credentials, and ensure that
that the username and password you are using are for the same user with which the
application is associated:

```
OAuthException: invalid_grant error processing request
```

### Two-Factor Authentication

A 2FA token can be used by joining it to the password with a colon:

```python
reddit = praw.Reddit(
    client_id="SI8pN3DSbt0zor",
    client_secret="xaxkj7HNh8kwg8e5t4m6KvSrbTI",
    password="1guiwevlfo00esyy:955413",
    user_agent="testscript by u/fakebot3",
    username="fakebot3",
)
```

However, for such an app there is little benefit to using 2FA. The token must be
refreshed after one hour; therefore, the 2FA secret would have to be stored along with
the rest of the credentials in order to generate the token, which defeats the point of
having an extra credential beyond the password.

If you do choose to use 2FA, you must handle the `prawcore.OAuthException` that will
be raised by API calls after one hour.

## Code Flow

A **code flow** application is useful for two primary purposes:

- You have an application and want to be able to access Reddit from your users'
accounts.

- You have a personal-use script application and you either want to

  - limit the access one of your PRAW-based programs has to Reddit

  - avoid the hassle of 2FA (described above)

  - not pass your username and password to PRAW (and thus not keep it in memory)

When registering your application you must provide a valid redirect URI. If you are
running a website you will want to enter the appropriate callback URL and configure that
endpoint to complete the code flow.

If you aren't actually running a website, you can follow the [Working with Refresh Tokens](https://praw.readthedocs.io/en/stable/tutorials/refresh_token.html#refresh-token)
tutorial to learn how to obtain and use the initial refresh token.

Whether or not you follow the [Working with Refresh Tokens](https://praw.readthedocs.io/en/stable/tutorials/refresh_token.html#refresh-token) tutorial there are two processes
involved in obtaining access or refresh tokens.

### Obtain the Authorization URL

The first step to completing the **code flow** is to obtain the authorization URL. You
can do that as follows:

```python
reddit = praw.Reddit(
    client_id="SI8pN3DSbt0zor",
    client_secret="xaxkj7HNh8kwg8e5t4m6KvSrbTI",
    redirect_uri="http://localhost:8080",
    user_agent="testscript by u/fakebot3",
)
print(reddit.auth.url(scopes=["identity"], state="...", duration="permanent"))
```

The above will output an authorization URL for a permanent token (i.e., the resulting
authorization will include both a short-lived `access_token`, and a longer-lived,
single use `refresh_token`) that has only the `identity` scope. See [`url()`](https://praw.readthedocs.io/en/stable/code_overview/other/auth.html#praw.models.Auth.url "praw.models.Auth.url") for
more information on these parameters.

This URL should be accessed by the account that desires to authorize their Reddit access
to your application. On completion of that flow, the user's browser will be redirected
to the specified `redirect_uri`. After verifying the `state` and extracting the
`code` you can obtain the refresh token via:

```python
print(reddit.auth.authorize(code))
print(reddit.user.me())
```

The first line of output is the `refresh_token`. You can save this for later use (see
[Using a Saved Refresh Token](https://praw.readthedocs.io/en/stable/getting_started/authentication.html#using-refresh-tokens)).

The second line of output reveals the name of the [`Redditor`](https://praw.readthedocs.io/en/stable/code_overview/models/redditor.html#praw.models.Redditor "praw.models.Redditor") that completed the
code flow. It also indicates that the [`Reddit`](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit") instance is now associated with
that account.

The code flow can be used with an **installed** application just as described above with
one change: set the value of `client_secret` to `None` when initializing
[`Reddit`](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit").

## Implicit Flow

The **implicit flow** requires a similar instantiation of the [`Reddit`](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit") class as
done in [Code Flow](https://praw.readthedocs.io/en/stable/getting_started/authentication.html#code-flow), however, the token is returned directly as part of the
redirect. For the implicit flow call [`url()`](https://praw.readthedocs.io/en/stable/code_overview/other/auth.html#praw.models.Auth.url "praw.models.Auth.url") like so:

```python
print(reddit.auth.url(scopes=["identity"], state="...", implicit=True))
```

Then use [`implicit()`](https://praw.readthedocs.io/en/stable/code_overview/other/auth.html#praw.models.Auth.implicit "praw.models.Auth.implicit") to provide the authorization to the [`Reddit`](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit")
instance.

## Read-Only Mode

All application types support a read-only mode. Read-only mode provides access to Reddit
like a logged out user would see including the default subreddits in the
`reddit.front` listings.

In the absence of a `refresh_token` both [Code Flow](https://praw.readthedocs.io/en/stable/getting_started/authentication.html#code-flow) and [Implicit Flow](https://praw.readthedocs.io/en/stable/getting_started/authentication.html#implicit-flow)
applications start in the **read-only** mode. With such applications **read-only** mode
is disabled when [`authorize()`](https://praw.readthedocs.io/en/stable/code_overview/other/auth.html#praw.models.Auth.authorize "praw.models.Auth.authorize"), or [`implicit()`](https://praw.readthedocs.io/en/stable/code_overview/other/auth.html#praw.models.Auth.implicit "praw.models.Auth.implicit") are successfully called.
[Password Flow](https://praw.readthedocs.io/en/stable/getting_started/authentication.html#password-flow) applications start up with **read-only** mode disabled.

Read-only mode can be toggled via:

```python
# Enable read-only mode
reddit.read_only = True

# Disable read-only mode (must have a valid authorization)
reddit.read_only = False
```

### Application-Only Flows

The following flows are the **read-only mode** flows for Reddit applications

#### Application-Only (Client Credentials)

This is the default flow for **read-only mode** in script and web applications. The idea
behind this is that Reddit _can_ trust these applications as coming from a given
developer, however the application requires no logged-in user context.

An installed application _cannot_ use this flow, because Reddit requires a
`client_secret` to be given if this flow is being used. In other words, installed
applications are not considered confidential clients.

#### Application-Only (Installed Client)

This is the default flow for **read-only mode** in installed applications. The idea
behind this is that Reddit _might not be able_ to trust these applications as coming
from a given developer. This would be able to happen if someone other than the developer
can potentially replicate the client information and then pretend to be the application,
such as in installed applications where the end user could retrieve the `client_id`.

Note

No benefit is really gained from this in script or web apps. The one exception is
for when a script or web app has multiple end users, this will allow you to give
Reddit the information needed in order to distinguish different users of your app
from each other (as the supplied device ID _should_ be a unique string per both
device (in the case of a web app, server) and user (in the case of a web app,
browser session).

## Using a Saved Refresh Token

A saved refresh token can be used to immediately obtain an authorized instance of
[`Reddit`](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit") like so:

```python
reddit = praw.Reddit(
    client_id="SI8pN3DSbt0zor",
    client_secret="xaxkj7HNh8kwg8e5t4m6KvSrbTI",
    refresh_token="WeheY7PwgeCZj4S3QgUcLhKE5S2s4eAYdxM",
    user_agent="testscript by u/fakebot3",
)
print(reddit.auth.scopes())
```

The output from the above code displays which scopes are available on the
[`Reddit`](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit "praw.Reddit") instance.

Note

Observe that `redirect_uri` does not need to be provided in such cases. It is only
needed when [`url()`](https://praw.readthedocs.io/en/stable/code_overview/other/auth.html#praw.models.Auth.url "praw.models.Auth.url") is used.