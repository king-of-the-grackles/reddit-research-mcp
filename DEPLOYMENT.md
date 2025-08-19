# 🚀 Smithery Deployment Guide

This guide explains how to deploy the Reddit Research MCP Server on Smithery.

## 📋 Prerequisites

1. **Reddit API Credentials**
   - Go to https://www.reddit.com/prefs/apps
   - Click "Create App" or "Create Another App"
   - Choose "script" as the app type
   - Note your `client_id` and `client_secret`

2. **Smithery Account**
   - Sign up at https://smithery.ai
   - Have your GitHub account ready for connection

## 🧪 Local Testing

### Test with HTTP Transport

1. **Test the server locally with HTTP transport:**
```bash
TRANSPORT=http PORT=8080 \
REDDIT_CLIENT_ID=your_id \
REDDIT_CLIENT_SECRET=your_secret \
uv run python -m src.server
```

2. **Test with Docker:**
```bash
# Build the image
docker build -t reddit-research-mcp .

# Run with environment variables
docker run -p 8080:8080 \
  -e REDDIT_CLIENT_ID=your_id \
  -e REDDIT_CLIENT_SECRET=your_secret \
  reddit-research-mcp

# Or use docker-compose
docker-compose up --build
```

3. **Test the endpoint:**
```bash
# Health check
curl http://localhost:8080/health

# MCP endpoint (Smithery will pass config as query params)
curl "http://localhost:8080/mcp?REDDIT_CLIENT_ID=your_id&REDDIT_CLIENT_SECRET=your_secret"
```

## 📦 Deployment to Smithery

### Step 1: Prepare Repository

1. **Commit all deployment files:**
```bash
git add Dockerfile smithery.yaml .dockerignore docker-compose.yml DEPLOYMENT.md
git add src/server.py src/config.py  # Updated files
git commit -m "Add Smithery deployment configuration

- Add Dockerfile with HTTP transport support
- Add smithery.yaml with configuration schema
- Update server.py to support streamable-http transport
- Update config.py to handle query parameters from Smithery
- Add .dockerignore to optimize image size

🚀 Ready for Smithery deployment"
git push origin main
```

### Step 2: Connect to Smithery

1. **Log in to Smithery** at https://smithery.ai
2. **Navigate to "Deployments"** section
3. **Click "Deploy New Server"**
4. **Select "Custom Deploy"** (for Docker-based deployment)
5. **Connect your GitHub repository**
   - Repository: `king-of-the-grackles/reddit-research-mcp`
   - Branch: `main`

### Step 3: Configure Deployment

1. **Smithery will read `smithery.yaml`** automatically
2. **Configure your Reddit API credentials:**
   - `REDDIT_CLIENT_ID`: Your Reddit app ID
   - `REDDIT_CLIENT_SECRET`: Your Reddit app secret (marked as sensitive)
   - `REDDIT_USER_AGENT`: Optional, defaults to "RedditResearchMCP/1.0 (Smithery)"

### Step 4: Deploy

1. **Click "Deploy"**
2. Smithery will:
   - Build the Docker image
   - Deploy to their infrastructure
   - Make it available at a public URL
   - Handle SSL/TLS automatically

### Step 5: Verify Deployment

Once deployed, your server will be available at:
```
https://your-server-name.smithery.ai/mcp
```

Test with:
```bash
curl https://your-server-name.smithery.ai/health
```

## 🔧 Configuration Options

### Environment Variables

The server supports configuration through multiple methods (in order of precedence):

1. **Query Parameters** (Smithery deployment)
2. **Environment Variables** (Docker/local)
3. **.env file** (local development only)

### smithery.yaml Configuration

The `smithery.yaml` file defines:
- **name**: Server identifier on Smithery
- **config.schema**: Configuration parameters users must provide
- **capabilities**: MCP tools, prompts, and resources
- **deployment**: Docker settings and health checks
- **resources**: Memory and CPU requirements

## 📊 Resource Usage

- **Memory**: ~512MB (includes 50MB vector database)
- **CPU**: 0.5 cores
- **Storage**: ~200MB Docker image
- **Vector DB**: 20,000+ indexed subreddits

## 🐛 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| "Port already in use" | Change PORT env var or stop conflicting service |
| "Reddit credentials not found" | Check REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET |
| "Cannot connect to Reddit" | Verify credentials are correct |
| "Health check failing" | Check server logs with `docker logs` |
| "Vector DB not found" | Ensure src/tools/db/data/ is copied in Dockerfile |

### Debugging

**View Docker logs:**
```bash
docker logs reddit-research-mcp
```

**Check health endpoint:**
```bash
curl -v http://localhost:8080/health
```

**Test MCP endpoint:**
```bash
curl -X POST http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -d '{"method": "tools/list"}'
```

## 🔄 Updates

To update your deployment:

1. Push changes to GitHub
2. In Smithery dashboard, click "Redeploy"
3. Smithery will rebuild and redeploy automatically

## 📈 Monitoring

Smithery provides:
- Request logs
- Error tracking
- Usage metrics
- Health status

Access these in your Smithery dashboard under your deployment.

## 🔐 Security Notes

- Reddit API credentials are stored securely in Smithery
- Never commit credentials to Git
- Use the `secret: true` flag in smithery.yaml for sensitive fields
- The server runs in read-only mode (no Reddit write access)

## 📚 Additional Resources

- [Smithery Documentation](https://smithery.ai/docs)
- [FastMCP HTTP Transport](https://github.com/modelcontextprotocol/python-sdk#streamable-http-transport)
- [Reddit API Documentation](https://www.reddit.com/dev/api)
- [Project README](README.md)