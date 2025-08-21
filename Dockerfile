FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Set working directory
WORKDIR /app

# Enable bytecode compilation for better performance
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Copy dependency files first for better caching
COPY pyproject.toml uv.lock ./

# Install dependencies (using cache mount for efficiency)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Copy project source code
COPY src/ ./src/
COPY README.md ./

# Install the project itself
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Set up environment paths
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app:$PYTHONPATH"

# Set environment for HTTP transport
ENV TRANSPORT=http
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

# Set default proxy URL for vector database access
ENV CHROMA_PROXY_URL=https://reddit-mcp-vector-db.onrender.com

# Expose port for HTTP mode
EXPOSE 8080

# Run the server directly with Python
CMD ["python", "/app/src/server.py"]