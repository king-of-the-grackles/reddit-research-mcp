FROM ghcr.io/astral-sh/uv:python3.12-alpine

# Set working directory
WORKDIR /app

# Enable bytecode compilation for better performance
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Install system dependencies if needed
RUN apk add --no-cache gcc musl-dev python3-dev

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

# Copy the vector database (20k+ indexed subreddits)
COPY src/tools/db/data/ ./src/tools/db/data/

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

# Expose port for HTTP mode
EXPOSE 8080

# Run the server directly with Python
CMD ["python", "/app/src/server.py"]