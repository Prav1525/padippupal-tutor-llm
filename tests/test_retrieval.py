from app.retrieval import retrieve


def test_retrieves_matching_syllabus_section(tmp_path):
    (tmp_path / "math.md").write_text(
        "# Mathematics\n\n## Fractions\nA fraction represents equal parts of a whole.\n",
        encoding="utf-8",
    )
    results = retrieve("explain fractions", str(tmp_path))
    assert results
    assert results[0]["title"] == "Fractions"
    assert "equal parts" in results[0]["text"]


def test_returns_empty_for_no_matching_terms(tmp_path):
    (tmp_path / "math.md").write_text(
        "## Fractions\nA fraction represents equal parts of a whole.\n",
        encoding="utf-8",
    )
    assert retrieve("volcanoes", str(tmp_path)) == []
