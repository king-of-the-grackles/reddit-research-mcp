# UV Documentation

This directory contains scraped documentation from the official UV documentation site (https://docs.astral.sh/uv/). UV is an extremely fast Python package and project manager, written in Rust.

## Documentation Structure

### [Core Concepts](./concepts/index.md)
Comprehensive documentation on UV's core concepts and features:

#### Project Management
- **[Dependencies](./concepts/dependencies.md)** - Managing project dependencies, sources, optional dependencies, and development dependencies
- **[Project Configuration](./concepts/config.md)** - Configuring projects, build systems, entry points, and package settings
- **[Project Layout](./concepts/layout.md)** - Project structure, pyproject.toml, project environment, and lockfiles
- **[Workspaces](./concepts/workspaces.md)** - Managing multiple interconnected packages within a single repository

#### Python Management
- **[Python Versions](./concepts/python-versions.md)** - Managing Python installations, version discovery, and version requirements
- **[Tools](./concepts/tools.md)** - Command-line tools management with uv tool interface, execution vs installation

#### Resolution & Caching
- **[Resolution](./concepts/resolution.md)** - Dependency resolution, platform markers, universal vs platform-specific resolution
- **[Cache](./concepts/cache.md)** - Dependency caching, cache management, and caching strategies

#### Security & Configuration
- **[Authentication](./concepts/authentication.md)** - Git authentication, HTTP authentication, and custom CA certificates
- **[Configuration Files](./concepts/configuration-files.md)** - Project and user-level configuration, uv.toml and pyproject.toml settings

### [Guides](./guides/index.md)
Practical guides for integrating UV with various tools and workflows:

#### Integration Guides
- **[Docker Integration](./guides/integration/docker.md)** - Complete guide for using UV in Docker containers, including image selection, optimization strategies, and development workflows

## Key Features of UV

- **Lightning Fast**: 10-100x faster than pip and pip-tools
- **Drop-in Replacement**: Compatible with pip, pip-tools, and virtualenv commands
- **All-in-One Tool**: Manages Python versions, virtual environments, and dependencies
- **Cross-Platform**: Works on macOS, Linux, and Windows
- **Rust-Powered**: Built for speed and reliability

## Quick Start

### Installation
```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with pip
pip install uv
```

### Basic Usage
```bash
# Create a new project
uv init my-project

# Add dependencies
uv add requests pandas

# Sync dependencies
uv sync

# Run commands in the project environment
uv run python script.py
```

## Additional Resources

Due to the extensive nature of UV's documentation, some sections (CLI reference, settings reference) were too large to scrape completely. For the most up-to-date and complete documentation, visit:

- **Official Documentation**: https://docs.astral.sh/uv/
- **GitHub Repository**: https://github.com/astral-sh/uv
- **Discord Community**: https://discord.gg/astral-sh

## Documentation Status

This collection includes the most critical UV documentation for offline reference and LLM context:
- ✅ Core concepts (dependencies, configuration, workspaces, Python management)
- ✅ Resolution and caching mechanisms
- ✅ Authentication and security
- ✅ Docker integration guide
- ⚠️ CLI reference (too large - refer to online docs)
- ⚠️ Settings reference (too large - refer to online docs)

The scraped documentation provides comprehensive coverage of UV's core functionality and should give LLMs sufficient context to assist with most UV-related tasks and questions.