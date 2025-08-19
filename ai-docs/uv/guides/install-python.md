# Installing Python

If Python is already installed on your system, uv will detect and use it without configuration. However, uv can also install and manage Python versions. uv automatically installs missing Python versions as needed — you don't need to install Python to get started.

## Getting started

To install the latest Python version:

```bash
$ uv python install
```

> **Note**: Python does not publish official distributable binaries. As such, uv uses distributions from the Astral [`python-build-standalone`](https://github.com/astral-sh/python-build-standalone) project. See the Python distributions documentation for more details.

Once Python is installed, it will be used by `uv` commands automatically. uv also adds the installed version to your `PATH`:

```bash
$ python3.13
```

uv only installs a _versioned_ executable by default. To install `python` and `python3` executables, include the experimental `--default` option:

```bash
$ uv python install --default
```

> **Tip**: See the documentation on installing Python executables for more details.

## Installing a specific version

To install a specific Python version:

```bash
$ uv python install 3.12
```

To install multiple Python versions:

```bash
$ uv python install 3.11 3.12
```

To install an alternative Python implementation, e.g., PyPy:

```bash
$ uv python install pypy@3.10
```

## Reinstalling Python

To reinstall uv-managed Python versions, use `--reinstall`, e.g.:

```bash
$ uv python install --reinstall
```

This will reinstall all previously installed Python versions. Improvements are constantly being added to the Python distributions, so reinstalling may resolve bugs even if the Python version does not change.

## Viewing Python installations

To view available and installed Python versions:

```bash
$ uv python list
```

## Automatic Python downloads

Python does not need to be explicitly installed to use uv. By default, uv will automatically download Python versions when they are required. For example, the following would download Python 3.12 if it was not installed:

```bash
$ uvx python@3.12 -c "print('hello world')"
```

Even if a specific Python version is not requested, uv will download the latest version on demand. For example, if there are no Python versions on your system, the following will install Python before creating a new virtual environment:

```bash
$ uv venv
```

> **Tip**: Automatic Python downloads can be easily disabled if you want more control over when Python is downloaded.

## Using existing Python versions

uv will use existing Python installations if present on your system. There is no configuration necessary for this behavior: uv will use the system Python if it satisfies the requirements of the command invocation. See the Python discovery documentation for details.

To force uv to use the system Python, provide the `--no-managed-python` flag. See the Python version preference documentation for more details.

## Upgrading Python versions

> **Important**: Support for upgrading Python patch versions is in _preview_. This means the behavior is experimental and subject to change.

To upgrade a Python version to the latest supported patch release:

```bash
$ uv python upgrade 3.12
```

To upgrade all uv-managed Python versions:

```bash
$ uv python upgrade
```

## Next steps

To learn more about `uv python`, see the Python version concept page and the command reference.

Or, read on to learn how to run scripts and invoke Python with uv.