# Reddit MCP Server Test Suite

## Quick Start

Run all critical tests:
```bash
# From project root
./run_critical_tests.sh
```

## Test Files

### Critical Tests (`/tests/`)

#### 1. `test_mcp_critical.py`
**Purpose:** Core MCP functionality validation
- Server imports without crashes
- Three-layer architecture (discover → schema → execute)
- Error handling and recovery messages
- Handles missing credentials gracefully

```bash
python tests/test_mcp_critical.py
```

#### 2. `test_langfuse_critical.py`
**Purpose:** Langfuse observability testing
- Client initialization
- W3C-compliant trace ID generation
- Server works without Langfuse (optional feature)
- Memory cleanup for traces
- Non-blocking operations

```bash
python tests/test_langfuse_critical.py
```

#### 3. `test_security_critical.py`
**Purpose:** Security validation
- No credential leaks to stdout/stderr
- No credentials in error messages
- Reddit client is read-only
- Environment variable security
- No hardcoded credentials

```bash
python tests/test_security_critical.py
```

#### 4. `test_e2e_smoke.py`
**Purpose:** End-to-end workflow simulation
- Complete MCP client workflow
- Memory usage tracking
- Performance metrics
- All three layers working together
- Error handling verification

```bash
python tests/test_e2e_smoke.py
```

### Diagnostic Scripts (`/scripts/`)

#### 1. `test_observability.py`
**Purpose:** Quick Langfuse configuration check
- Verifies Langfuse credentials
- Tests middleware integration
- Validates trace ID generation

```bash
python scripts/test_observability.py
```

#### 2. `test_operations_tracking.py`
**Purpose:** Detailed operations tracking with Langfuse
- Tests all three MCP layers with timing
- Creates actual Langfuse traces
- Verifies trace metadata
- Useful for debugging observability

```bash
python scripts/test_operations_tracking.py
```

## Environment Variables

### Required for Full Testing:
```bash
# Reddit API (Required for operations)
export REDDIT_CLIENT_ID="your_client_id"
export REDDIT_CLIENT_SECRET="your_secret"
export REDDIT_USER_AGENT="RedditMCP/1.0"

# Langfuse (Optional but recommended)
export LANGFUSE_PUBLIC_KEY="pk-lf-..."
export LANGFUSE_SECRET_KEY="sk-lf-..."
export LANGFUSE_HOST="https://us.cloud.langfuse.com"
```

### Test Mode (No Real Credentials):
Tests will use dummy credentials automatically if none are set:
```bash
# Just run the tests - they'll use test credentials
./run_critical_tests.sh
```

## Running Individual Test Suites

### Core Functionality Only:
```bash
python tests/test_mcp_critical.py
```

### Security Tests Only:
```bash
python tests/test_security_critical.py
```

### Observability Tests Only:
```bash
python tests/test_langfuse_critical.py
python scripts/test_observability.py
```

### Performance/E2E Tests:
```bash
python tests/test_e2e_smoke.py
```

## Test Coverage

| Component | Test File | Coverage |
|-----------|-----------|----------|
| MCP Operations | `test_mcp_critical.py` | ✅ Full |
| Error Handling | `test_mcp_critical.py` | ✅ Full |
| Security | `test_security_critical.py` | ✅ Full |
| Langfuse Integration | `test_langfuse_critical.py` | ✅ Full |
| E2E Workflow | `test_e2e_smoke.py` | ✅ Full |
| Memory Management | `test_e2e_smoke.py` | ✅ Full |

## Production Readiness Checklist

Before deploying to production, ensure:
- [ ] All tests pass: `./run_critical_tests.sh`
- [ ] Reddit credentials are set (real ones)
- [ ] Langfuse credentials are set (optional)
- [ ] Security test passes
- [ ] E2E smoke test passes
- [ ] Memory usage is acceptable (<100MB increase)

## Typical Test Output

### Successful Run:
```
✅ ALL CRITICAL TESTS PASSED!
✅ Server is ready for production deployment!
```

### With Warnings (Still OK):
```
✅ SMOKE TEST PASSED WITH WARNINGS
⚠️ Langfuse not configured (optional)
```

### Failed (Fix Before Production):
```
❌ SOME TESTS FAILED!
Please fix the issues above before deploying to production.
```

## Debugging Tips

1. **Import Errors:** Check dependencies with `pip install -e ".[dev]"`
2. **Credential Issues:** Verify environment variables are exported
3. **Langfuse Not Working:** Check credentials and network connection
4. **High Memory Usage:** Normal to see ~50MB increase during operations
5. **Test Timeouts:** Some operations take 2-3 seconds (ChromaDB proxy)

## Maintenance

- Tests use FastMCP's `.fn` attribute to call wrapped functions
- All tests are independent and can run in any order
- Tests clean up after themselves (no state persistence)
- Langfuse traces are flushed automatically

## CI/CD Integration

Add to your CI pipeline:
```yaml
- name: Run Critical Tests
  run: |
    export REDDIT_CLIENT_ID=${{ secrets.REDDIT_CLIENT_ID }}
    export REDDIT_CLIENT_SECRET=${{ secrets.REDDIT_CLIENT_SECRET }}
    ./run_critical_tests.sh
```