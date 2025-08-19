# Working with Refresh Tokens

## Reddit OAuth2 Scopes

Before working with refresh tokens you should decide which scopes your application
requires. If you want to use all scopes, you can use the special scope `*`.

To get an up-to-date listing of all Reddit scopes and their descriptions run the
following:

```python
import requests

response = requests.get(
    "https://www.reddit.com/api/v1/scopes.json",
    headers={"User-Agent": "fetch-scopes by u/bboe"},
)

for scope, data in sorted(response.json().items()):
    print(f"{scope:>18s}  {data['description']}")
```

As of February 2021, the available scopes are:

| Scope | Description |
| --- | --- |
| account | Update preferences and related account information. Will not have access to your email or password. |
| creddits | Spend my reddit gold creddits on giving gold to other users. |
| edit | Edit and delete my comments and submissions. |
| flair | Select my subreddit flair. Change link flair on my submissions. |
| history | Access my voting history and comments or submissions I've saved or hidden. |
| identity | Access my reddit username and signup date. |
| livemanage | Manage settings and contributors of live threads I contribute to. |
| modconfig | Manage the configuration, sidebar, and CSS of subreddits I moderate. |
| modcontributors | Add/remove users to approved user lists and ban/unban or mute/unmute users from subreddits I moderate. |
| modflair | Manage and assign flair in subreddits I moderate. |
| modlog | Access the moderation log in subreddits I moderate. |
| modmail | Access and manage modmail via mod.reddit.com. |
| modothers | Invite or remove other moderators from subreddits I moderate. |
| modposts | Approve, remove, mark nsfw, and distinguish content in subreddits I moderate. |
| modself | Accept invitations to moderate a subreddit. Remove myself as a moderator or contributor of subreddits I moderate or contribute to. |
| modtraffic | Access traffic stats in subreddits I moderate. |
| modwiki | Change editors and visibility of wiki pages in subreddits I moderate. |
| mysubreddits | Access the list of subreddits I moderate, contribute to, and subscribe to. |
| privatemessages | Access my inbox and send private messages to other users. |
| read | Access posts and comments through my account. |
| report | Report content for rules violations. Hide & show individual submissions. |
| save | Save and unsave comments and submissions. |
| structuredstyles | Edit structured styles for a subreddit I moderate. |
| submit | Submit links and comments from my account. |
| subscribe | Manage my subreddit subscriptions. Manage "friends" - users whose content I follow. |
| vote | Submit and change my votes on comments and submissions. |
| wikiedit | Edit wiki pages on my behalf |
| wikiread | Read wiki pages through my account |

## Obtaining Refresh Tokens

The following program can be used to obtain a refresh token with the desired scopes:

```python
#!/usr/bin/env python

"""This example demonstrates the flow for retrieving a refresh token.

This tool can be used to conveniently create refresh tokens for later use with your web
application OAuth2 credentials.

To create a Reddit application visit the following link while logged into the account
you want to create a refresh token for: https://www.reddit.com/prefs/apps/

Create a "web app" with the redirect uri set to: http://localhost:8080

After the application is created, take note of:

- REDDIT_CLIENT_ID; the line just under "web app" in the upper left of the Reddit
  Application
- REDDIT_CLIENT_SECRET; the value to the right of "secret"

Usage:

    EXPORT praw_client_id=<REDDIT_CLIENT_ID>
    EXPORT praw_client_secret=<REDDIT_CLIENT_SECRET>
    python3 obtain_refresh_token.py

"""
import random
import socket
import sys

import praw

def main():
    """Provide the program's entry point when directly executed."""
    scope_input = input(
        "Enter a comma separated list of scopes, or '*' for all scopes: "
    )
    scopes = [scope.strip() for scope in scope_input.strip().split(",")]

    reddit = praw.Reddit(
        redirect_uri="http://localhost:8080",
        user_agent="obtain_refresh_token/v0 by u/bboe",
    )
    state = str(random.randint(0, 65000))
    url = reddit.auth.url(duration="permanent", scopes=scopes, state=state)
    print(f"Now open this url in your browser: {url}")

    client = receive_connection()
    data = client.recv(1024).decode("utf-8")
    param_tokens = data.split(" ", 2)[1].split("?", 1)[1].split("&")
    params = {
        key: value for (key, value) in [token.split("=") for token in param_tokens]
    }

    if state != params["state"]:
        send_message(
            client,
            f"State mismatch. Expected: {state} Received: {params['state']}",
        )
        return 1
    elif "error" in params:
        send_message(client, params["error"])
        return 1

    refresh_token = reddit.auth.authorize(params["code"])
    send_message(client, f"Refresh token: {refresh_token}")
    return 0

def receive_connection():
    """Wait for and then return a connected socket..

    Opens a TCP connection on port 8080, and waits for a single client.

    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("localhost", 8080))
    server.listen(1)
    client = server.accept()[0]
    server.close()
    return client

def send_message(client, message):
    """Send message to client and close the connection."""
    print(message)
    client.send(f"HTTP/1.1 200 OK\r\n\r\n{message}".encode("utf-8"))
    client.close()

if __name__ == "__main__":
    sys.exit(main())
```

This script assumes you have configured your application's `redirect uri` to
`localhost:8080`

When you execute this script interactively:

1. You will be prompted to provide a comma-separated list of scopes.

2. You will be given a URL that will take you through the auth flow on Reddit.

3. When you open the provided link in your browser, Reddit will ask you for permission
to grant the application permissions to the scopes requested.

4. After clicking allow, you will have a new authorized application configured.

5. You will be redirected to another page (the application's `redirect uri`) where
your refresh token will be displayed and will be printed to the command line.


You only have to run this script once for each refresh token. The refresh token (along
with the application's `client_id`, `client_secret`) are valid credentials until
manually revoked by the user.