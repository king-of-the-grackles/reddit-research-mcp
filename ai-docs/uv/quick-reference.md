# uv Quick Reference

## Installation

```bash
# Install uv (macOS/Linux)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install uv (Windows)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Update uv
uv self update
```

## Project Management

```bash
# Create a new project
uv init my-project
cd my-project

# Initialize in current directory
uv init

# Add dependencies
uv add requests numpy pandas
uv add 'django>=4.0'
uv add git+https://github.com/user/repo

# Remove dependencies
uv remove requests

# Update dependencies
uv lock --upgrade-package requests

# Sync environment with lockfile
uv sync

# Run commands in project environment
uv run python script.py
uv run pytest
uv run -- flask run -p 3000

# Build project
uv build
```

## Python Management

```bash
# Install Python
uv python install          # Latest version
uv python install 3.12     # Specific version
uv python install 3.11 3.12  # Multiple versions

# List Python versions
uv python list

# Pin Python version for project
uv python pin 3.11

# Upgrade Python
uv python upgrade 3.12
```

## Scripts

```bash
# Run a script
uv run script.py

# Run with dependencies
uv run --with requests script.py

# Create script with inline metadata
uv init --script example.py --python 3.12

# Add dependencies to script
uv add --script example.py requests rich

# Lock script dependencies
uv lock --script example.py
```

## Tools

```bash
# Run tool without installing (uvx = uv tool run)
uvx ruff check
uvx pycowsay "Hello!"
uvx --from httpie http httpbin.org/get

# Run specific version
uvx ruff@0.3.0 check
uvx ruff@latest check

# Install tool persistently
uv tool install ruff
uv tool install mkdocs --with mkdocs-material

# Upgrade tools
uv tool upgrade ruff
uv tool upgrade --all

# List installed tools
uv tool list
```

## pip Interface

```bash
# Create virtual environment
uv venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate      # Windows

# Install packages
uv pip install requests
uv pip install -r requirements.txt

# Compile requirements
uv pip compile requirements.in -o requirements.txt
uv pip compile requirements.in --universal  # Platform-independent

# Sync environment
uv pip sync requirements.txt

# List packages
uv pip list
uv pip freeze > requirements.txt

# Uninstall packages
uv pip uninstall requests
```

## Common Workflows

### Starting a New Project
```bash
uv init my-app
cd my-app
uv add fastapi uvicorn
uv run -- uvicorn main:app --reload
```

### Working with Existing Project
```bash
git clone https://github.com/user/project
cd project
uv sync
uv run pytest
```

### Running Jupyter Notebooks
```bash
uv add jupyter notebook
uv run jupyter notebook
```

### Using with Docker
```dockerfile
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen
COPY . .
CMD ["uv", "run", "python", "app.py"]
```

### CI/CD with GitHub Actions
```yaml
- name: Install uv
  uses: astral-sh/setup-uv@v4
  
- name: Install dependencies
  run: uv sync
  
- name: Run tests
  run: uv run pytest
```

## Environment Variables

```bash
# Disable automatic Python downloads
export UV_PYTHON_DOWNLOADS=never

# Use system Python only
export UV_SYSTEM_PYTHON=true

# Set cache directory
export UV_CACHE_DIR=/path/to/cache

# Disable progress bars
export UV_NO_PROGRESS=1
```

## Tips & Tricks

1. **Speed up installs**: uv uses a global cache, so packages are only downloaded once
2. **Reproducible builds**: Always commit `uv.lock` to version control
3. **Python versions**: uv automatically downloads Python if needed
4. **Tool isolation**: Tools installed with `uv tool` don't interfere with projects
5. **Script dependencies**: Use inline metadata for self-contained scripts
6. **Platform-specific**: Use `--universal` for cross-platform requirements

## Common Commands Summary

| Task | Command |
|------|---------|
| Create project | `uv init` |
| Add dependency | `uv add package` |
| Run script | `uv run script.py` |
| Install tool | `uv tool install package` |
| Run tool | `uvx tool` |
| Install Python | `uv python install` |
| Create venv | `uv venv` |
| Install packages | `uv pip install` |
| Update lockfile | `uv lock` |
| Sync environment | `uv sync` |