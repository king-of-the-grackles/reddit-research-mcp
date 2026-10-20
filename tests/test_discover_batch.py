"""Batch discovery costs one vector-DB request, not one per query."""
from src.tools.discover import discover_subreddits


class RecordingCollection:
    """Answers like Chroma: one metadata/distance list per query text, in order."""

    def __init__(self, by_query=None, error=None):
        self.by_query, self.error, self.calls = by_query or {}, error, []

    def query(self, query_texts, n_results):
        self.calls.append(list(query_texts))
        if self.error:
            raise self.error
        return {"metadatas": [self.by_query[q][0] for q in query_texts],
                "distances": [self.by_query[q][1] for q in query_texts]}


def use_collection(monkeypatch, collection):
    monkeypatch.setattr("src.tools.discover._get_vector_collection", lambda name: collection)


async def test_batch_discovery_sends_all_queries_in_one_vector_db_request(monkeypatch):
    collection = RecordingCollection({
        "python": ([{"name": "Python", "subscribers": 1_500_000, "nsfw": False}], [0.2]),
        "rust": ([{"name": "rust", "subscribers": 300_000, "nsfw": False}], [0.25]),
    })
    use_collection(monkeypatch, collection)
    result = await discover_subreddits(queries=["python", "rust"])
    assert collection.calls == [["python", "rust"]]
    assert result["api_calls_made"] == 1
    assert [s["name"] for s in result["results"]["python"]["subreddits"]] == ["Python"]
    assert [s["name"] for s in result["results"]["rust"]["subreddits"]] == ["rust"]


async def test_failed_batch_request_reports_the_error_for_every_query(monkeypatch):
    use_collection(monkeypatch, RecordingCollection(error=ConnectionError("Rate limit exceeded")))
    result = await discover_subreddits(queries=["python", "rust"])
    for query in ("python", "rust"):
        assert "Rate limit exceeded" in result["results"][query]["error"]
        assert result["results"][query]["subreddits"] == []
