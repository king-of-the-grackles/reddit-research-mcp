# Quick Start

In this section, we go over everything you need to know to start building scripts or bots using PRAW, the Python Reddit API Wrapper. It's fun and easy. Let's get started.

## Prerequisites

**Python Knowledge:**

You need to know at least a little Python to use PRAW. PRAW supports [Python 3.7+](https://docs.python.org/3/tutorial/index.html). If you are stuck on a problem, [r/learnpython](https://www.reddit.com/r/learnpython/) is a great place to ask for help.

**Reddit Knowledge:**

A basic understanding of how Reddit works is a must. In the event you are not already familiar with Reddit start at [Reddit Help](https://www.reddithelp.com/en).

**Reddit Account:**

A Reddit account is required to access Reddit's API. Create one at [reddit.com](https://www.reddit.com/).

**Client ID & Client Secret:**

These two values are needed to access Reddit's API as a **script** application (see [Authenticating via OAuth](authentication.md) for other application types). If you don't already have a client ID and client secret, follow Reddit's [First Steps Guide](https://github.com/reddit/reddit/wiki/OAuth2-Quick-Start-Example#first-steps) to create them.

**User Agent:**

A user agent is a unique identifier that helps Reddit determine the source of network requests. To use Reddit's API, you need a unique and descriptive user agent. The recommended format is `<platform>:<app ID>:<version string> (by u/<Reddit username>)`. For example, `android:com.example.myredditapp:v1.2.3 (by u/kemitche)`. Read more about user agents at [Reddit's API wiki page](https://github.com/reddit/reddit/wiki/API).

With these prerequisites satisfied, you are ready to learn how to do some of the most common tasks with Reddit's API.

## Common Tasks

### Obtain a Reddit Instance

> **Warning:** For the sake of brevity, the following examples pass authentication information via arguments to `praw.Reddit()`. If you do this, you need to be careful not to reveal this information to the outside world if you share your code. It is recommended to use a [praw.ini file](configuration.md#praw-ini) in order to keep your authentication information separate from your code.

You need an instance of the `Reddit` class to do _anything_ with PRAW. There are two distinct states a `Reddit` instance can be in: read-only, and authorized.

#### Read-only Reddit Instances

To create a read-only `Reddit` instance, you need three pieces of information:

1. Client ID
2. Client secret
3. User agent

You may choose to provide these by passing in three keyword arguments when calling the initializer of the `Reddit` class: `client_id`, `client_secret`, `user_agent` (see [Configuring PRAW](configuration.md) for other methods of providing this information). For example:

```python
import praw

reddit = praw.Reddit(
    client_id="my client id",
    client_secret="my client secret",
    user_agent="my user agent",
)
```

Just like that, you now have a read-only `Reddit` instance.

```python
print(reddit.read_only)
# Output: True
```

With a read-only instance, you can do something like obtaining 10 "hot" submissions from `r/test`:

```python
# continued from code above

for submission in reddit.subreddit("test").hot(limit=10):
    print(submission.title)

# Output: 10 submissions
```

If you want to do more than retrieve public information from Reddit, then you need an authorized `Reddit` instance.

> **Note:** In the above example we are limiting the results to `10`. Without the `limit` parameter PRAW should yield as many results as it can with a single request. For most endpoints this results in 100 items per request. If you want to retrieve as many as possible pass in `limit=None`.

#### Authorized Reddit Instances

In order to create an authorized `Reddit` instance, two additional pieces of information are required for **script** applications (see [Authenticating via OAuth](authentication.md) for other application types):

4. Your Reddit username, and
5. Your Reddit password

Again, you may choose to provide these by passing in keyword arguments `username` and `password` when you call the `Reddit` initializer, like the following:

```python
import praw

reddit = praw.Reddit(
    client_id="my client id",
    client_secret="my client secret",
    password="my password",
    user_agent="my user agent",
    username="my username",
)

print(reddit.read_only)
# Output: False
```

Now you can do whatever your Reddit account is authorized to do. And you can switch back to read-only mode whenever you want:

```python
# continued from code above
reddit.read_only = True
```

> **Note:** If you are uncomfortable hard-coding your credentials into your program, there are some options available to you. Please see: [Configuring PRAW](configuration.md).

### Obtain a Subreddit

To obtain a `Subreddit` instance, pass the subreddit's name when calling `subreddit` on your `Reddit` instance. For example:

```python
# assume you have a praw.Reddit instance bound to variable `reddit`
subreddit = reddit.subreddit("redditdev")

print(subreddit.display_name)
# Output: redditdev
print(subreddit.title)
# Output: reddit development
print(subreddit.description)
# Output: a subreddit for discussion of ...
```

### Obtain Submission Instances from a Subreddit

Now that you have a `Subreddit` instance, you can iterate through some of its submissions, each bound to an instance of `Submission`. There are several sorts that you can iterate through:

- controversial
- gilded
- hot
- new
- rising
- top

Each of these methods will immediately return a `ListingGenerator`, which is to be iterated through. For example, to iterate through the first 10 submissions based on the `hot` sort for a given subreddit try:

```python
# assume you have a Subreddit instance bound to variable `subreddit`
for submission in subreddit.hot(limit=10):
    print(submission.title)
    # Output: the submission's title
    print(submission.score)
    # Output: the submission's score
    print(submission.id)
    # Output: the submission's ID
    print(submission.url)
    # Output: the URL the submission points to or the submission's URL if it's a self post
```

> **Note:** The act of calling a method that returns a `ListingGenerator` does not result in any network requests until you begin to iterate through the `ListingGenerator`.

You can create `Submission` instances in other ways too:

```python
# assume you have a praw.Reddit instance bound to variable `reddit`
submission = reddit.submission("39zje0")
print(submission.title)
# Output: reddit will soon only be available ...

# or
submission = reddit.submission(url="https://www.reddit.com/...")
```

### Obtain Redditor Instances

There are several ways to obtain a redditor (a `Redditor` instance). Two of the most common ones are:

- via the `author` attribute of a `Submission` or `Comment` instance
- via the `redditor()` method of `Reddit`

For example:

```python
# assume you have a Submission instance bound to variable `submission`
redditor1 = submission.author
print(redditor1.name)
# Output: name of the redditor

# assume you have a praw.Reddit instance bound to variable `reddit`
redditor2 = reddit.redditor("bboe")
print(redditor2.link_karma)
# Output: u/bboe's karma
```

### Obtain Comment Instances

Submissions have a `comments` attribute that is a `CommentForest` instance. That instance is iterable and represents the top-level comments of the submission by the default comment sort (`confidence`). If you instead want to iterate over _all_ comments as a flattened list you can call the `list()` method on a `CommentForest` instance. For example:

```python
# assume you have a praw.Reddit instance bound to variable `reddit`
top_level_comments = list(submission.comments)
all_comments = submission.comments.list()
```

> **Note:** The comment sort order can be changed by updating the value of `comment_sort` on the `Submission` instance prior to accessing `comments` (see: [/api/set_suggested_sort](https://www.reddit.com/dev/api#POST_api_set_suggested_sort) for possible values). For example to have comments sorted by `new` try something like:

```python
# assume you have a praw.Reddit instance bound to variable `reddit`
submission = reddit.submission("39zje0")
submission.comment_sort = "new"
top_level_comments = list(submission.comments)
```

As you may be aware there will periodically be `MoreComments` instances scattered throughout the forest. Replace those `MoreComments` instances at any time by calling `replace_more()` on a `CommentForest` instance. Calling `replace_more()` access `comments`, and so must be done after `comment_sort` is updated. See [Extracting comments with PRAW](../tutorials/comments.md) for an example.

### Determine Available Attributes of an Object

If you have a PRAW object, e.g., `Comment`, `Message`, `Redditor`, or `Submission`, and you want to see what attributes are available along with their values, use the built-in `vars()` function of python. For example:

```python
import pprint

# assume you have a praw.Reddit instance bound to variable `reddit`
submission = reddit.submission("39zje0")
print(submission.title)  # to make it non-lazy
pprint.pprint(vars(submission))
```

Note the line where we print the title. PRAW uses lazy objects so that network requests to Reddit's API are only issued when information is needed. Here, before the print line, `submission` points to a lazy `Submission` object. When we try to print its title, additional information is needed, thus a network request is made, and the instances ceases to be lazy. Outputting all the attributes of a lazy object will result in fewer attributes than expected.