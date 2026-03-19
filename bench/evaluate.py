"""Answer extraction and accuracy calculation."""

import re


ANSWER_PATTERNS = [
    re.compile(r"答案[：:]\s*([A-Da-d])"),
    re.compile(r"答案是[：:]\s*([A-Da-d])"),
    re.compile(r"选择[：:]\s*([A-Da-d])"),
    re.compile(r"选[：:]\s*([A-Da-d])"),
    re.compile(r"^([A-Da-d])$", re.MULTILINE),
    re.compile(r"[。，,.]([A-Da-d])[。.]?\s*$", re.MULTILINE),
    re.compile(r"\b([A-Da-d])\b"),
]


def extract_answer(response: str) -> str | None:
    """Extract the answer letter from an LLM response."""
    if not response:
        return None

    for pattern in ANSWER_PATTERNS:
        match = pattern.search(response)
        if match:
            return match.group(1).upper()

    # Last resort: find all standalone letters and take the last valid one
    all_letters = re.findall(r"\b([A-Da-d])\b", response)
    valid = [l.upper() for l in all_letters if l.upper() in "ABCD"]
    return valid[-1] if valid else None


def calculate_accuracy(results: list[dict]) -> dict:
    """Calculate accuracy metrics from evaluation results."""
    total = len(results)
    if total == 0:
        return {"total": 0, "correct": 0, "accuracy": 0.0, "by_category": {}}

    correct = sum(1 for r in results if r.get("correct"))

    # Per-category breakdown
    by_category: dict[str, dict] = {}
    for r in results:
        cat = r.get("category", "unknown")
        if cat not in by_category:
            by_category[cat] = {"total": 0, "correct": 0}
        by_category[cat]["total"] += 1
        if r.get("correct"):
            by_category[cat]["correct"] += 1

    for cat_stats in by_category.values():
        cat_stats["accuracy"] = (
            cat_stats["correct"] / cat_stats["total"]
            if cat_stats["total"] > 0
            else 0.0
        )

    # Per-source breakdown
    by_source: dict[str, dict] = {}
    for r in results:
        src = r.get("source", "unknown")
        if src not in by_source:
            by_source[src] = {"total": 0, "correct": 0}
        by_source[src]["total"] += 1
        if r.get("correct"):
            by_source[src]["correct"] += 1

    for src_stats in by_source.values():
        src_stats["accuracy"] = (
            src_stats["correct"] / src_stats["total"]
            if src_stats["total"] > 0
            else 0.0
        )

    return {
        "total": total,
        "correct": correct,
        "accuracy": correct / total,
        "by_category": dict(sorted(by_category.items(), key=lambda x: -x[1]["total"])),
        "by_source": dict(sorted(by_source.items())),
    }
