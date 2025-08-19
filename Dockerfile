FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv for faster dependency management
RUN pip install uv

# Copy project files
COPY pyproject.toml .
COPY src/ ./src/

# Copy the vector database (20k+ indexed subreddits)
# This is essential for semantic search functionality
COPY src/tools/db/data/ ./src/tools/db/data/

# Install Python dependencies
RUN uv sync --frozen --no-dev

# Set environment variables for Smithery deployment
ENV MCP_TRANSPORT=streamable-http
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Expose the port
EXPOSE 8080

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health').read()" || exit 1

# Run the server
CMD ["uv", "run", "python", "-m", "src.server"]