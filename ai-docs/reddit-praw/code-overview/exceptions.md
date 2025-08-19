# Exceptions in PRAW

In addition to exceptions under the `praw.exceptions` namespace shown below,
exceptions might be raised that inherit from `prawcore.PrawcoreException`. Please see
the following resource for information on those exceptions:
[https://github.com/praw-dev/prawcore/blob/master/prawcore/exceptions.py](https://github.com/praw-dev/prawcore/blob/master/prawcore/exceptions.py)

## praw.exceptions

PRAW exception classes.

Includes two main exceptions: [`RedditAPIException`](https://praw.readthedocs.io/en/stable/code_overview/exceptions.html#praw.exceptions.RedditAPIException "praw.exceptions.RedditAPIException") for when something goes wrong
on the server side, and [`ClientException`](https://praw.readthedocs.io/en/stable/code_overview/exceptions.html#praw.exceptions.ClientException "praw.exceptions.ClientException") when something goes wrong on the
client side. Both of these classes extend [`PRAWException`](https://praw.readthedocs.io/en/stable/code_overview/exceptions.html#praw.exceptions.PRAWException "praw.exceptions.PRAWException").

All other exceptions are subclassed from [`ClientException`](https://praw.readthedocs.io/en/stable/code_overview/exceptions.html#praw.exceptions.ClientException "praw.exceptions.ClientException").

### APIException (Deprecated)

_exception_ praw.exceptions.APIException( _items:[List](https://docs.python.org/3/library/typing.html#typing.List "(in Python v3.11)")\[ [RedditErrorItem](https://praw.readthedocs.io/en/stable/code_overview/exceptions.html#praw.exceptions.RedditErrorItem "praw.exceptions.RedditErrorItem") \| [List](https://docs.python.org/3/library/typing.html#typing.List "(in Python v3.11)")\[ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")\]\| [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")\]\| [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_, _\*optional\_args:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_)

Old class preserved for alias purposes.

Deprecated since version 7.0: Class [`APIException`](https://praw.readthedocs.io/en/stable/code_overview/exceptions.html#praw.exceptions.APIException "praw.exceptions.APIException") has been deprecated in favor of
[`RedditAPIException`](https://praw.readthedocs.io/en/stable/code_overview/exceptions.html#praw.exceptions.RedditAPIException "praw.exceptions.RedditAPIException"). This class will be removed in PRAW 8.0.

### ClientException

_exception_ praw.exceptions.ClientException

Indicate exceptions that don't involve interaction with Reddit's API.

### DuplicateReplaceException

_exception_ praw.exceptions.DuplicateReplaceException

Indicate exceptions that involve the replacement of [`MoreComments`](https://praw.readthedocs.io/en/stable/code_overview/models/more.html#praw.models.MoreComments "praw.models.MoreComments").

### InvalidFlairTemplateID

_exception_ praw.exceptions.InvalidFlairTemplateID( _template\_id:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_)

Indicate exceptions where an invalid flair template ID is given.

### InvalidImplicitAuth

_exception_ praw.exceptions.InvalidImplicitAuth

Indicate exceptions where an implicit auth type is used incorrectly.

### InvalidURL

_exception_ praw.exceptions.InvalidURL( _url:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_, _\*_, _message:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")='InvalidURL:{}'_)

Indicate exceptions where an invalid URL is entered.

Parameters:

- **url** – The invalid URL.
- **message** – The message to display. Must contain a format identifier ( `{}`
or `{0}`) (default: `"Invalid URL: {}"`).

### MediaPostFailed

_exception_ praw.exceptions.MediaPostFailed

Indicate exceptions where media uploads failed.

### MissingRequiredAttributeException

_exception_ praw.exceptions.MissingRequiredAttributeException

Indicate exceptions caused by not including a required attribute.

### PRAWException

_exception_ praw.exceptions.PRAWException

The base PRAW Exception that all other exception classes extend.

### ReadOnlyException

_exception_ praw.exceptions.ReadOnlyException

Raised when a method call requires [`read_only`](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit.read_only "praw.Reddit.read_only") mode to be disabled.

### RedditAPIException

_exception_ praw.exceptions.RedditAPIException( _items:[List](https://docs.python.org/3/library/typing.html#typing.List "(in Python v3.11)")\[ [RedditErrorItem](https://praw.readthedocs.io/en/stable/code_overview/exceptions.html#praw.exceptions.RedditErrorItem "praw.exceptions.RedditErrorItem") \| [List](https://docs.python.org/3/library/typing.html#typing.List "(in Python v3.11)")\[ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")\]\| [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")\]\| [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_, _\*optional\_args:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_)

Container for error messages from Reddit's API.

### RedditErrorItem

_class_ praw.exceptions.RedditErrorItem( _error\_type:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_, _\*_, _field:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_, _message:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")=None_)

Represents a single error returned from Reddit's API.

Parameters:

- **error\_type** – The error type set on Reddit's end.
- **field** – The input field associated with the error, if available.
- **message** – The associated message for the error.

#### error_message

_property_ error\_message _: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_

Get the completed error message string.

### TooLargeMediaException

_exception_ praw.exceptions.TooLargeMediaException( _\*_, _actual:[int](https://docs.python.org/3/library/functions.html#int "(in Python v3.11)")_, _maximum\_size:[int](https://docs.python.org/3/library/functions.html#int "(in Python v3.11)")_)

Indicate exceptions from uploading media that's too large.

Parameters:

- **actual** – The actual size of the uploaded media.
- **maximum\_size** – The maximum size of the uploaded media.

### WebSocketException

_exception_ praw.exceptions.WebSocketException( _message:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_, _exception:[Exception](https://docs.python.org/3/library/exceptions.html#Exception "(in Python v3.11)") \| [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")_)

Indicate exceptions caused by use of WebSockets.

Parameters:

- **message** – The exception message.
- **exception** – The exception thrown by the websocket library.

Note

This parameter is deprecated. It will be removed in PRAW 8.0.