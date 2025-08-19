# Submission (Complete API Reference)

**class** `praw.models.Submission(reddit: praw.Reddit, id: str | None = None, url: str | None = None, _data: Dict[str, Any] | None = None)`

A class for submissions to Reddit.

## Table of Contents
- [Class Definition](#class-definition)
- [Typical Attributes](#typical-attributes)
- [Methods](#methods)
- [Properties](#properties)
- [Code Examples](#code-examples)

## Class Definition

The `Submission` class represents a Reddit submission (post). It can be initialized with either a submission ID or a URL.

## Typical Attributes

**Note:** This table describes attributes that typically belong to objects of this class. PRAW dynamically provides the attributes that Reddit returns via the API. Since those attributes are subject to change on Reddit's end, PRAW makes no effort to document any new/removed/changed attributes, other than to instruct you on how to discover what is available. As a result, this table of attributes may not be complete. See [Determine Available Attributes of an Object](https://praw.readthedocs.io/en/stable/getting_started/quick_start.html#determine-available-attributes-of-an-object) for detailed information.

| Attribute | Type | Description |
|-----------|------|-------------|
| `author` | `Redditor` | Provides an instance of `Redditor`. |
| `author_flair_css_class` | `str` | CSS class for author's flair. |
| `author_flair_text` | `str` | The text content of the author's flair, or `None` if not flaired. |
| `clicked` | `bool` | Whether or not the submission has been clicked by the client. |
| `comments` | `CommentForest` | Provides an instance of `CommentForest`. |
| `created_utc` | `float` | Time the submission was created, represented in [Unix Time](https://en.wikipedia.org/wiki/Unix_time). |
| `distinguished` | `str` | Whether or not the submission is distinguished. |
| `domain` | `str` | The domain of the submission's link. |
| `edited` | `bool | float` | Whether or not the submission has been edited. |
| `gilded` | `int` | Number of times the submission has been gilded. |
| `hidden` | `bool` | Whether the submission is hidden by the user. |
| `id` | `str` | ID of the submission. |
| `is_original_content` | `bool` | Whether or not the submission has been set as original content. |
| `is_self` | `bool` | Whether or not the submission is a selfpost (text-only). |
| `link_flair_template_id` | `str` | The link flair's ID. |
| `link_flair_text` | `str` | The link flair's text content, or `None` if not flaired. |
| `locked` | `bool` | Whether or not the submission has been locked. |
| `media` | `dict` | Media associated with the submission. |
| `media_embed` | `dict` | Embedded media details. |
| `name` | `str` | Fullname of the submission. |
| `num_comments` | `int` | The number of comments on the submission. |
| `num_crossposts` | `int` | Number of times the submission has been crossposted. |
| `over_18` | `bool` | Whether or not the submission has been marked as NSFW. |
| `permalink` | `str` | A permalink for the submission. |
| `poll_data` | `PollData` | A `PollData` object representing the data of this submission, if it is a poll submission. |
| `preview` | `dict` | Preview information for the submission. |
| `quarantine` | `bool` | Whether the submission is from a quarantined subreddit. |
| `removal_reason` | `str` | Reason for removal, if applicable. |
| `saved` | `bool` | Whether or not the submission is saved. |
| `score` | `int` | The number of upvotes for the submission. |
| `secure_media` | `dict` | Secure media associated with the submission. |
| `secure_media_embed` | `dict` | Secure media embed details. |
| `selftext` | `str` | The submissions' selftext - an empty string if a link post. |
| `spoiler` | `bool` | Whether or not the submission has been marked as a spoiler. |
| `stickied` | `bool` | Whether or not the submission is stickied. |
| `subreddit` | `Subreddit` | Provides an instance of `Subreddit`. |
| `suggested_sort` | `str` | Suggested comment sorting method. |
| `title` | `str` | The title of the submission. |
| `upvote_ratio` | `float` | The percentage of upvotes from all votes on the submission. |
| `url` | `str` | The URL the submission links to, or the permalink if a selfpost. |

## Methods

### `__init__(reddit: praw.Reddit, id: str | None = None, url: str | None = None, _data: Dict[str, Any] | None = None)`

Initialize a `Submission` instance.

**Parameters:**
- **reddit** – An instance of `Reddit`.
- **id** – A reddit base36 submission ID, e.g., `"2gmzqe"`.
- **url** – A URL supported by `id_from_url()`.

Either `id` or `url` can be provided, but not both.

**Example usage:**
```python
# Initialize with ID
submission = reddit.submission("2gmzqe")

# Initialize with URL
submission = reddit.submission(url="https://www.reddit.com/r/redditdev/comments/2gmzqe/praw_https/")
```

### `_edit_experimental(body: str, *, preserve_inline_media=False, inline_media: Dict[str, praw.models.InlineMedia] | None = None) → praw.models.Submission`

Replace the body of the object with `body`.

**Parameters:**
- **body** – The Markdown formatted content for the updated object.
- **preserve_inline_media** – Attempt to preserve inline media in `body`.
- **inline_media** – A dict of `InlineMedia` objects where the key is the placeholder name in `body`.

**Returns:** The current instance after updating its attributes.

**Warning:** This method is experimental. It is reliant on undocumented API endpoints and may result in existing inline media not displaying correctly and/or creating a malformed body. Use at your own risk. This method may be removed in the future without warning.

**Example usage:**
```python
from praw.models import InlineGif, InlineImage, InlineVideo

submission = reddit.submission("5or86n")
gif = InlineGif(path="path/to/image.gif", caption="optional caption")
image = InlineImage(path="path/to/image.jpg", caption="optional caption")
video = InlineVideo(path="path/to/video.mp4", caption="optional caption")
body = "New body with a gif {gif1} an image {image1} and a video {video1} inline"
media = {"gif1": gif, "image1": image, "video1": video}
submission._edit_experimental(submission.selftext + body, inline_media=media)
```

### `add_fetch_param(key, value)`

Add a parameter to be used for the next fetch.

**Parameters:**
- **key** – The key of the fetch parameter.
- **value** – The value of the fetch parameter.

**Example usage:**
```python
submission = reddit.submission("mcqjl8")
submission.add_fetch_param("rtj", "all")
print(submission.rtjson)
```

### `award(*, gild_type: str = 'gid_2', is_anonymous: bool = True, message: str = None) → dict`

Award the author of the item.

**Parameters:**
- **gild_type** – Type of award to give. See table below for currently known global award types.
- **is_anonymous** – If `True`, the authenticated user's username will not be revealed to the recipient.
- **message** – Message to include with the award.

**Returns:** A dict containing info about the award transaction.

**Warning:** Requires the authenticated user to own Reddit Coins. Calling this method will consume Reddit Coins.

**Example usage:**
```python
# Award the gold award anonymously
submission = reddit.submission("8dmv8z")
submission.award()

# Award the platinum award with message and reveal username
submission.award(gild_type="gid_3", message="Nice!", is_anonymous=False)
```

### `clear_vote()`

Clear the authenticated user's vote on the object.

**Note:** Votes must be cast by humans. That is, API clients proxying a human's action one-for-one are OK, but bots deciding how to vote on content or amplifying a human's vote are not. See the [reddit rules](https://www.redditinc.com/policies/content-policy) for more details on what constitutes vote manipulation.

**Example usage:**
```python
submission = reddit.submission("5or86n")
submission.clear_vote()
```

### `crosspost(subreddit: praw.models.Subreddit, *, flair_id: str | None = None, flair_text: str | None = None, nsfw: bool = False, send_replies: bool = True, spoiler: bool = False, title: str | None = None) → praw.models.Submission`

Crosspost the submission to a subreddit.

**Note:** Be aware you have to be subscribed to the target subreddit.

**Parameters:**
- **subreddit** – Name of the subreddit or `Subreddit` object to crosspost into.
- **flair_id** – The flair template to select (default: `None`).
- **flair_text** – If the template's `flair_text_editable` value is `True`, this value will set a custom text (default: `None`).
- **nsfw** – Whether the submission should be marked NSFW (default: `False`).
- **send_replies** – When `True`, messages will be sent to the created submission's author when comments are made to the submission (default: `True`).
- **spoiler** – Whether the submission should be marked as a spoiler (default: `False`).
- **title** – Title of the submission. Will use this submission's title if `None` (default: `None`).

**Returns:** A `Submission` object for the newly created submission.

**Example usage:**
```python
submission = reddit.submission("5or86n")
cross_post = submission.crosspost("learnprogramming", send_replies=False)
```

### `delete()`

Delete the object.

**Example usage:**
```python
submission = reddit.submission("8dmv8z")
submission.delete()
```

### `disable_inbox_replies()`

Disable inbox replies for the item.

**Example usage:**
```python
submission = reddit.submission("8dmv8z")
submission.disable_inbox_replies()
```

**See also:** `enable_inbox_replies()`

### `downvote()`

Downvote the object.

**Note:** Votes must be cast by humans. That is, API clients proxying a human's action one-for-one are OK, but bots deciding how to vote on content or amplifying a human's vote are not. See the [reddit rules](https://www.redditinc.com/policies/content-policy) for more details on what constitutes vote manipulation.

**Example usage:**
```python
submission = reddit.submission("5or86n")
submission.downvote()
```

**See also:** `upvote()`

### `duplicates(**generator_kwargs: str | int | Dict[str, str]) → Iterator[praw.models.Submission]`

Return a `ListingGenerator` for the submission's duplicates.

Additional keyword arguments are passed in the initialization of `ListingGenerator`.

**Example usage:**
```python
submission = reddit.submission("5or86n")

for duplicate in submission.duplicates():
    # process each duplicate
    print(duplicate.title)
```

### `edit(body: str) → praw.models.Comment | praw.models.Submission`

Replace the body of the object with `body`.

**Parameters:**
- **body** – The Markdown formatted content for the updated object.

**Returns:** The current instance after updating its attributes.

**Example usage:**
```python
submission = reddit.submission("5or86n")
# Edit a text post
edited_body = submission.selftext + "\n\nEdit: thanks for the gold!"
submission.edit(edited_body)
```

### `enable_inbox_replies()`

Enable inbox replies for the item.

**Example usage:**
```python
submission = reddit.submission("8dmv8z")
submission.enable_inbox_replies()
```

**See also:** `disable_inbox_replies()`

### `flair() → SubmissionFlair`

Provide an instance of `SubmissionFlair`.

This attribute is used to work with flair as a regular user of the subreddit the submission belongs to. Moderators can directly use `flair()`.

**Example usage:**
```python
choices = submission.flair.choices()
template_id = next(x for x in choices if x["flair_text_editable"])["flair_template_id"]
submission.flair.select(template_id, text="my custom value")
```

### `gild() → dict`

Alias for `award()` to maintain backwards compatibility.

### `hide(*, other_submissions: List[praw.models.Submission] | None = None)`

Hide `Submission`.

**Parameters:**
- **other_submissions** – When provided, additionally hide this list of `Submission` instances as part of a single request (default: `None`).

**Example usage:**
```python
submission = reddit.submission("5or86n")
submission.hide()
```

**See also:** `unhide()`

### `mark_visited()`

Mark submission as visited.

This method requires a subscription to reddit premium.

**Example usage:**
```python
submission = reddit.submission("5or86n")
submission.mark_visited()
```

### `mod() → SubmissionModeration`

Provide an instance of `SubmissionModeration`.

**Example usage:**
```python
submission = reddit.submission("8dmv8z")
submission.mod.approve()
```

### `parse(data: Dict[str, Any], reddit: praw.Reddit) → Any` (Class Method)

Return an instance of `cls` from `data`.

**Parameters:**
- **data** – The structured data.
- **reddit** – An instance of `Reddit`.

### `reply(body: str) → praw.models.Comment | praw.models.Message | None`

Reply to the object.

**Parameters:**
- **body** – The Markdown formatted content for a comment.

**Returns:** A `Comment` or `Message` object for the newly created comment or message or `None` if Reddit doesn't provide one.

**Raises:** `prawcore.exceptions.Forbidden` when attempting to reply to some items, such as locked submissions/comments or non-replyable messages.

A `None` value can be returned if the target is a comment or submission in a quarantined subreddit and the authenticated user has not opt-ed into viewing the content. When this happens the comment will be successfully created on Reddit and can be retried by drawing the comment from the user's comment history.

**Example usage:**
```python
submission = reddit.submission("5or86n")
submission.reply("This is a great post!")
```

### `report(reason: str)`

Report this object to the moderators of its subreddit.

**Parameters:**
- **reason** – The reason for reporting.

**Raises:** `RedditAPIException` if `reason` is longer than 100 characters.

**Example usage:**
```python
submission = reddit.submission("5or86n")
submission.report("Spam content")
```

### `save(*, category: str | None = None)`

Save the object.

**Parameters:**
- **category** – The category to save to. If the authenticated user does not have Reddit Premium this value is ignored by Reddit (default: `None`).

**Example usage:**
```python
submission = reddit.submission("5or86n")
submission.save(category="view later")
```

**See also:** `unsave()`

### `unhide(*, other_submissions: List[praw.models.Submission] | None = None)`

Unhide `Submission`.

**Parameters:**
- **other_submissions** – When provided, additionally unhide this list of `Submission` instances as part of a single request (default: `None`).

**Example usage:**
```python
submission = reddit.submission("5or86n")
submission.unhide()
```

**See also:** `hide()`

### `unsave()`

Unsave the object.

**Example usage:**
```python
submission = reddit.submission("5or86n")
submission.unsave()
```

**See also:** `save()`

### `upvote()`

Upvote the object.

**Note:** Votes must be cast by humans. That is, API clients proxying a human's action one-for-one are OK, but bots deciding how to vote on content or amplifying a human's vote are not. See the [reddit rules](https://www.redditinc.com/policies/content-policy) for more details on what constitutes vote manipulation.

**Example usage:**
```python
submission = reddit.submission("5or86n")
submission.upvote()
```

**See also:** `downvote()`

## Properties

### `comments: CommentForest`

Provide an instance of `CommentForest`.

This attribute can be used, for example, to obtain a flat list of comments, with any `MoreComments` removed:

```python
submission.comments.replace_more(limit=0)
comments = submission.comments.list()
```

Sort order and comment limit can be set with the `comment_sort` and `comment_limit` attributes before comments are fetched, including any call to `replace_more()`:

```python
submission.comment_sort = "new"
comments = submission.comments.list()
```

**Note:** The appropriate values for `"comment_sort"` include `"confidence"`, `"controversial"`, `"new"`, `"old"`, `"q&a"`, and `"top"`

See [Extracting comments with PRAW](https://praw.readthedocs.io/en/stable/tutorials/comments.html) for more on working with a `CommentForest`.

### `fullname: str`

Return the object's fullname.

A fullname is an object's kind mapping like `t3` followed by an underscore and the object's base36 ID, e.g., `t3_c5s96e0`.

### `shortlink: str`

Return a shortlink to the submission.

For example, [https://redd.it/eorhm](https://redd.it/eorhm) is a shortlink for [https://www.reddit.com/r/announcements/comments/eorhm/reddit_30_less_typing/](https://www.reddit.com/r/announcements/comments/eorhm/reddit_30_less_typing/).

## Static Methods

### `id_from_url(url: str) → str`

Return the ID contained within a submission URL.

**Parameters:**
- **url** – A url to a submission in one of the following formats (http urls will also work):
  - `"https://redd.it/2gmzqe"`
  - `"https://reddit.com/comments/2gmzqe/"`
  - `"https://www.reddit.com/r/redditdev/comments/2gmzqe/praw_https/"`
  - `"https://www.reddit.com/gallery/2gmzqe"`

**Raises:** `InvalidURL` if `url` is not a valid submission URL.

**Example usage:**
```python
submission_id = Submission.id_from_url("https://www.reddit.com/r/redditdev/comments/2gmzqe/praw_https/")
print(submission_id)  # Output: "2gmzqe"
```

## Code Examples

### Basic Submission Operations

```python
import praw

# Initialize Reddit instance
reddit = praw.Reddit(
    client_id="your_client_id",
    client_secret="your_client_secret",
    username="your_username",
    password="your_password",
    user_agent="your_user_agent"
)

# Get a submission
submission = reddit.submission("2gmzqe")

# Access basic attributes
print(f"Title: {submission.title}")
print(f"Author: {submission.author}")
print(f"Score: {submission.score}")
print(f"Number of comments: {submission.num_comments}")

# Check if it's a self post
if submission.is_self:
    print(f"Self text: {submission.selftext}")
else:
    print(f"URL: {submission.url}")
```

### Working with Comments

```python
# Get all comments (flattened)
submission.comments.replace_more(limit=0)
all_comments = submission.comments.list()

print(f"Total comments: {len(all_comments)}")

# Access top-level comments
for top_level_comment in submission.comments:
    if hasattr(top_level_comment, 'body'):  # Skip MoreComments objects
        print(f"Comment by {top_level_comment.author}: {top_level_comment.body[:100]}...")
```

### Interacting with Submissions

```python
# Vote on submission
submission.upvote()
# or
submission.downvote()
# or
submission.clear_vote()

# Save submission
submission.save()

# Reply to submission
new_comment = submission.reply("This is my reply!")

# Report submission
submission.report("This violates the rules")

# Crosspost to another subreddit
crosspost = submission.crosspost("another_subreddit", title="Crosspost title")
```

### Moderator Actions

```python
# Moderate submission (requires moderator permissions)
submission.mod.approve()
submission.mod.remove()
submission.mod.distinguish()
submission.mod.sticky()
```

### Working with Submission Flair

```python
# Get available flair choices
flair_choices = submission.flair.choices()

# Select a flair
if flair_choices:
    template_id = flair_choices[0]['flair_template_id']
    submission.flair.select(template_id)
```

---

*This documentation covers the complete API reference for the PRAW Submission model. For more information, visit the [official PRAW documentation](https://praw.readthedocs.io/).*