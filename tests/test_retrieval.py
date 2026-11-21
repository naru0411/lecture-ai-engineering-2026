"""検索方式のテスト。外部APIは呼び出さない。"""

from app import retrieval


def test_graph_seeds_cover_individual_questions(monkeypatch):
    results = {
        "全体。二問目？": [
            {"page_id": "combined-1"},
            {"page_id": "combined-2"},
        ],
        "全体。": [
            {"page_id": "first-1"},
            {"page_id": "combined-1"},
        ],
        "二問目？": [
            {"page_id": "second-1"},
            {"page_id": "combined-2"},
        ],
    }
    calls = []

    def fake_search(query):
        calls.append(query)
        return results[query]

    monkeypatch.setattr(retrieval, "search", fake_search)

    seeds = retrieval._search_graph_seeds("全体。二問目？")

    assert calls == list(results)
    assert [seed["page_id"] for seed in seeds] == [
        "combined-1",
        "first-1",
        "second-1",
    ]


def test_graph_keeps_single_query_search_order(monkeypatch):
    hits = [{"page_id": "first"}, {"page_id": "second"}]
    calls = []

    def fake_search(query):
        calls.append(query)
        return hits

    monkeypatch.setattr(retrieval, "search", fake_search)

    assert retrieval._search_graph_seeds("単一の質問") == hits
    assert calls == ["単一の質問"]


def test_graph_uses_each_space_separated_concept_as_a_seed(monkeypatch):
    results = {
        "コンパクション": [
            {"page_id": "shared"},
            {"page_id": "compaction"},
        ],
        "セッション": [{"page_id": "shared"}, {"page_id": "session"}],
        "長期メモリ": [{"page_id": "long-term"}, {"page_id": "shared"}],
    }
    calls = []

    def fake_search(query):
        calls.append(query)
        return results[query]

    monkeypatch.setattr(retrieval, "search", fake_search)

    seeds = retrieval._search_graph_seeds("コンパクション セッション 長期メモリ")

    assert calls == list(results)
    assert [seed["page_id"] for seed in seeds] == [
        "shared",
        "long-term",
        "compaction",
    ]
