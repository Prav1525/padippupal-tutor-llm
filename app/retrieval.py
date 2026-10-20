from pathlib import Path
import re
from typing import Iterable


def _terms(text: str) -> set[str]:
    return {t for t in re.findall(r"[a-zA-Z0-9]+", text.lower()) if len(t) > 1}


def retrieve(query: str, syllabus_dir: str, limit: int = 3) -> list[dict[str, str]]:
    """Return relevant syllabus sections using a simple lexical baseline."""
    root = Path(syllabus_dir)
    results: list[dict[str, str]] = []
    q_terms = _terms(query)
    if not root.exists():
        return results
    for path in root.rglob("*.md"):
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        sections = re.split(r"(?m)(?=^##?\s+)", text)
        for section in sections:
            section = section.strip()
            if not section:
                continue
            title = section.splitlines()[0].lstrip("# ").strip()
            terms = _terms(section)
            overlap = len(q_terms & terms)
            if overlap:
                results.append({"source": path.name, "title": title, "text": section[:5000], "score": str(overlap)})
    results.sort(key=lambda item: int(item["score"]), reverse=True)
    return results[:limit]
