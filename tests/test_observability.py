import asyncio
import json
import logging
import pytest


@pytest.fixture(autouse=True)
def capture_runtime(caplog):
    from src.observability import logger
    logger.addHandler(caplog.handler)
    yield
    logger.removeHandler(caplog.handler)


async def test_sampler_stops_at_lifespan_end_and_reports_current_resources(caplog):
    from src.observability import RuntimeMetrics
    metrics = RuntimeMetrics()
    with caplog.at_level(logging.INFO, logger="reddit_mcp.runtime"):
        async with metrics.sampling(interval=.02):
            metrics.inflight_operations = 2
            await asyncio.sleep(.06)
        count = len(caplog.records)
        await asyncio.sleep(.04)
    assert len(caplog.records) == count
    samples = [json.loads(r.message) for r in caplog.records if '"runtime_sample"' in r.message]
    assert samples
    assert samples[-1]["inflight_operations"] == 2
    assert samples[-1]["rss_bytes"] > 0
    assert samples[-1]["event_loop_lag_ms"] >= 0
    assert set(samples[-1]) == {"event", "boot_id", "uptime_seconds", "rss_bytes",
                               "task_count", "inflight_operations", "event_loop_lag_ms"}


def test_operation_outcomes_do_not_include_input_or_exception_text(caplog):
    from src.observability import RuntimeMetrics
    metrics = RuntimeMetrics()
    with caplog.at_level(logging.INFO, logger="reddit_mcp.runtime"):
        metrics.record_operation("fetch_posts", 1.5, "upstream_timeout")
    assert json.loads(caplog.records[-1].message)["outcome"] == "upstream_timeout"


def test_health_is_unavailable_when_initialization_failed(monkeypatch):
    from src import server
    from starlette.testclient import TestClient
    def unavailable():
        raise ValueError("missing credentials")
    monkeypatch.setattr(server, "get_reddit_client", unavailable)
    with TestClient(server.mcp.http_app()) as client:
        assert client.get("/health").status_code == 503


def test_operation_records_caller_identity_when_authenticated(caplog):
    from src.observability import RuntimeMetrics
    metrics = RuntimeMetrics()
    with caplog.at_level(logging.INFO, logger="reddit_mcp.runtime"):
        metrics.record_operation("search_subreddit", .2, "success",
                                 user_id="U2abc123xyz789", client_id="claude-code-dcr-441")
    record = json.loads(caplog.records[-1].message)
    assert record["user_id"] == "U2abc123xyz789"
    assert record["client_id"] == "claude-code-dcr-441"
    assert record["operation"] == "search_subreddit"


def test_operation_omits_identity_fields_when_caller_is_anonymous(caplog):
    from src.observability import RuntimeMetrics
    metrics = RuntimeMetrics()
    with caplog.at_level(logging.INFO, logger="reddit_mcp.runtime"):
        metrics.record_operation("fetch_posts", .1, "success")
    record = json.loads(caplog.records[-1].message)
    assert "user_id" not in record and "client_id" not in record


def test_identity_prefers_subject_claim_over_client_id():
    from src.server import current_caller_identity
    class Token:
        client_id = "claude-code-dcr-441"
        claims = {"sub": "U2abc123xyz789", "client_id": "claude-code-dcr-441"}
    assert current_caller_identity(lambda: Token()) == ("U2abc123xyz789", "claude-code-dcr-441")


def test_identity_is_empty_for_unauthenticated_requests():
    from src.server import current_caller_identity
    assert current_caller_identity(lambda: None) == (None, None)


def test_identity_never_propagates_token_lookup_failures():
    from src.server import current_caller_identity
    def exploding():
        raise RuntimeError("no active request context")
    assert current_caller_identity(exploding) == (None, None)


def test_identity_tolerates_token_without_subject_claim():
    from src.server import current_caller_identity
    class Token:
        client_id = "legacy-client"
        claims = {}
    assert current_caller_identity(lambda: Token()) == (None, "legacy-client")


def test_recorded_identity_is_never_the_bearer_token(caplog):
    from src.observability import RuntimeMetrics
    metrics = RuntimeMetrics()
    with caplog.at_level(logging.INFO, logger="reddit_mcp.runtime"):
        metrics.record_operation("fetch_comments", .1, "success",
                                 user_id="U2abc", client_id="cid")
    assert "eyJ" not in caplog.records[-1].message


async def test_executed_operation_is_attributed_to_the_authenticated_caller(caplog, monkeypatch):
    """End-to-end: a real execute_operation call carries identity into the log line."""
    import fastmcp.server.dependencies as deps
    from src import server
    from src.observability import RuntimeMetrics

    class Token:
        client_id = "claude-code-dcr-441"
        claims = {"sub": "U2abc123xyz789"}

    monkeypatch.setattr(deps, "get_access_token", lambda: Token())

    metrics = RuntimeMetrics()
    ctx = type("Ctx", (), {"lifespan_context": {"metrics": metrics}})()

    with caplog.at_level(logging.INFO, logger="reddit_mcp.runtime"):
        # Missing required parameters fails fast, well before any upstream call,
        # but still runs the finally block that records the operation.
        await server.execute_operation("search_subreddit", {}, ctx=ctx)

    completions = [json.loads(r.message) for r in caplog.records
                   if '"operation_complete"' in r.message]
    assert completions, "operation_complete was never emitted"
    assert completions[-1]["user_id"] == "U2abc123xyz789"
    assert completions[-1]["client_id"] == "claude-code-dcr-441"


def broken_fetch_posts(monkeypatch, exc):
    from src import server
    def fetch_posts(**kwargs):
        raise exc
    monkeypatch.setattr(server, "fetch_subreddit_posts", fetch_posts)
    return server


def server_errors(caplog):
    return [r for r in caplog.records if r.name == "src.server" and r.levelno >= logging.ERROR]


async def test_unexpected_operation_failure_is_logged_with_its_traceback(caplog, monkeypatch):
    server = broken_fetch_posts(monkeypatch, RuntimeError("boom"))
    with caplog.at_level(logging.ERROR, logger="src.server"):
        result = await server.execute_operation("fetch_posts", {"subreddit_name": "python"}, ctx=None)
    assert result["success"] is False
    errors = server_errors(caplog)
    assert errors and errors[-1].exc_info[0] is RuntimeError
    assert "fetch_posts" in errors[-1].getMessage()


async def test_invalid_input_is_not_logged_as_a_server_error(caplog, monkeypatch):
    server = broken_fetch_posts(monkeypatch, TypeError("unexpected keyword argument 'x'"))
    with caplog.at_level(logging.ERROR, logger="src.server"):
        await server.execute_operation("fetch_posts", {"subreddit_name": "python"}, ctx=None)
    assert server_errors(caplog) == []


async def test_operation_reporting_an_unclassified_error_is_logged(caplog, monkeypatch):
    from src import server
    monkeypatch.setattr(server, "fetch_subreddit_posts", lambda **kwargs: {"error": "Reddit server error"})
    with caplog.at_level(logging.ERROR, logger="src.server"):
        await server.execute_operation("fetch_posts", {"subreddit_name": "python"}, ctx=None)
    errors = server_errors(caplog)
    assert errors and "fetch_posts" in errors[-1].getMessage()
    assert "Reddit server error" in errors[-1].getMessage()
