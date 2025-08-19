# uv Documentation

An extremely fast Python package and project manager, written in Rust.

## Documentation Structure

This directory contains the UV documentation from Astral, organized into the following sections:

### Getting Started
- [Installation](./getting-started/installation.md) - How to install uv on various platforms
- [First Steps](./getting-started/first-steps.md) - Quick introduction to using uv
- [Features](./getting-started/features.md) - Overview of uv's capabilities

### Core Concepts
- [Projects](./concepts/projects.md) - Working with uv projects
- [Python Versions](./concepts/python-versions.md) - Managing Python installations
- [Dependencies](./concepts/dependencies.md) - Dependency management
- [Configuration](./concepts/configuration.md) - Configuring uv behavior
- [Cache](./concepts/cache.md) - Understanding uv's caching system
- [Tools](./concepts/tools.md) - Running and installing Python tools

### Guides
- [Working with Projects](./guides/projects.md) - Project management guide
- [Scripts](./guides/scripts.md) - Running Python scripts with dependencies
- [Tools](./guides/tools.md) - Using Python tools with uv
- [Package Building](./guides/package.md) - Building and publishing packages
- [Installing Python](./guides/install-python.md) - Python version management

### Integration Guides
- [Docker](./guides/integration/docker.md) - Using uv in Docker containers
- [GitHub Actions](./guides/integration/github.md) - CI/CD with GitHub Actions
- [FastAPI](./guides/integration/fastapi.md) - Using uv with FastAPI
- [Jupyter](./guides/integration/jupyter.md) - Jupyter notebook integration

### pip Interface
- [Overview](./pip/index.md) - Using uv as a pip replacement
- [Environments](./pip/environments.md) - Virtual environment management
- [Dependencies](./pip/dependencies.md) - Dependency declaration
- [Locking](./pip/compile.md) - Creating lockfiles

### Reference
- [CLI Commands](./reference/cli.md) - Complete command reference
- [Settings](./reference/settings.md) - Configuration options
- [Environment Variables](./reference/environment.md) - Environment variable reference

## Quick Links

- [Official Documentation](https://docs.astral.sh/uv/)
- [GitHub Repository](https://github.com/astral-sh/uv)
- [Astral Website](https://astral.sh/)

## Highlights

- 🚀 A single tool to replace `pip`, `pip-tools`, `pipx`, `poetry`, `pyenv`, `twine`, `virtualenv`, and more
- ⚡️ 10-100x faster than `pip`
- 🗂️ Comprehensive project management with universal lockfile
- ❇️ Runs scripts with inline dependency metadata
- 🐍 Installs and manages Python versions
- 🛠️ Runs and installs tools published as Python packages
- 🔩 pip-compatible interface for familiar workflows
- 🏢 Cargo-style workspaces for scalable projects
- 💾 Disk-space efficient with global cache
- ⏬ Installable without Rust or Python
- 🖥️ Supports macOS, Linux, and Windows