"""Clients that misplace tool arguments still reach the operation they meant."""
import json

import httpx
from fastmcp.server.auth.providers.jwt import StaticTokenVerifier

from tests.http_support import initialize, live_server


def call_tool(monkeypatch, name, arguments):
    from src import server
    monkeypatch.setattr(server.mcp, "auth", StaticTokenVerifier(tokens={"test": {"client_id": "test", "scopes": []}}))
    with live_server(server.mcp.http_app()) as url, httpx.Client(
            base_url=url, headers={"Authorization": "Bearer test"}) as client:
        headers = initialize(client)
        response = client.post("/mcp", headers=headers, json={"jsonrpc": "2.0", "id": 2, "method": "tools/call",
                                                              "params": {"name": name, "arguments": arguments}})
        response.raise_for_status()
        client.delete("/mcp", headers=headers)
    replies = [json.loads(line[5:]) for line in response.text.splitlines() if line.startswith("data:")]
    reply = next(r for r in replies if r.get("id") == 2)
    assert "error" not in reply and not reply["result"].get("isError"), reply
    return reply["result"]["structuredContent"]


def record_fetch_posts(monkeypatch):
    from src import server
    received = {}
    def fetch_posts(**kwargs):
        received.update({k: v for k, v in kwargs.items() if k not in ("reddit", "ctx")})
        return {"done": True}
    monkeypatch.setattr(server, "fetch_subreddit_posts", fetch_posts)
    return received


def test_schema_request_naming_operation_instead_of_operation_id(monkeypatch):
    result = call_tool(monkeypatch, "get_operation_schema", {"operation": "fetch_posts"})
    assert result["description"] == "Get posts from a single subreddit"


def test_execute_with_operation_parameters_at_top_level(monkeypatch):
    received = record_fetch_posts(monkeypatch)
    result = call_tool(monkeypatch, "execute_operation",
                       {"operation_id": "fetch_posts", "subreddit_name": "python", "limit": 3})
    assert result["success"] is True
    assert received == {"subreddit_name": "python", "limit": 3}


def test_nested_parameters_win_over_top_level_duplicates(monkeypatch):
    received = record_fetch_posts(monkeypatch)
    call_tool(monkeypatch, "execute_operation",
              {"operation": "fetch_posts", "parameters": {"subreddit_name": "python", "limit": 5}, "limit": 10})
    assert received == {"subreddit_name": "python", "limit": 5}
