#!/usr/bin/env python3
"""Generate per-question detail data for the FateryBench detail explorer.

Reads all result JSON files and combined.json to produce docs/details_data.js
with per-question data showing each model's predicted answer and correctness.
"""

import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = ROOT / "results"
DATA_FILE = ROOT / "data" / "combined.json"
OUTPUT_FILE = ROOT / "docs" / "details_data.js"

# Models to include (full runs only, skip partial runs)
# Map: result filename -> display info
MODELS = {
    "gemini-3-flash-preview_fatery.json": {
        "key": "fatery",
        "name": "Fatery",
        "provider": "Fatery.me",
        "mode": "fatery",
        "baseModel": "Gemini 3 Flash",
    },
    "gpt-5.4_baseline.json": {
        "key": "gpt54",
        "name": "GPT-5.4",
        "provider": "OpenAI",
        "mode": "baseline",
    },
    "gemini-3.1-flash-lite-preview_baseline.json": {
        "key": "gemini31fl",
        "name": "Gemini 3.1 Flash Lite",
        "provider": "Google",
        "mode": "baseline",
    },
    "gpt-5.3-chat-latest_baseline.json": {
        "key": "gpt53",
        "name": "GPT-5.3",
        "provider": "OpenAI",
        "mode": "baseline",
    },
    "gemini-3.1-pro-preview_baseline.json": {
        "key": "gemini31pro",
        "name": "Gemini 3.1 Pro",
        "provider": "Google",
        "mode": "baseline",
    },
    "gemini-3-pro-preview_baseline.json": {
        "key": "gemini3pro",
        "name": "Gemini 3 Pro",
        "provider": "Google",
        "mode": "baseline",
    },
    "gemini-3-flash-preview_baseline.json": {
        "key": "gemini3flash",
        "name": "Gemini 3 Flash",
        "provider": "Google",
        "mode": "baseline",
    },
    "gemini-3.1-pro-preview_fatery.json": {
        "key": "gemini31pro_f",
        "name": "Gemini 3.1 Pro",
        "provider": "Google",
        "mode": "fatery",
    },
    "gpt-5.4_fatery.json": {
        "key": "gpt54_f",
        "name": "GPT-5.4",
        "provider": "OpenAI",
        "mode": "fatery",
    },
    "gpt-5.3-chat-latest_fatery.json": {
        "key": "gpt53_f",
        "name": "GPT-5.3",
        "provider": "OpenAI",
        "mode": "fatery",
    },
}


def load_questions():
    """Load questions from combined.json, filter to competition only."""
    with open(DATA_FILE) as f:
        data = json.load(f)
    questions = data["questions"]
    # Filter to competition questions only
    return [q for q in questions if not q["source"].startswith("celebrity")]


def load_model_results(filename):
    """Load model results and return dict keyed by question_id."""
    filepath = RESULTS_DIR / filename
    if not filepath.exists():
        return {}
    with open(filepath) as f:
        data = json.load(f)
    results = data.get("results", [])
    # Filter to competition only
    return {
        r["question_id"]: r
        for r in results
        if not r.get("source", "").startswith("celebrity")
    }


def source_label(source):
    """Convert source id to display label."""
    mapping = {
        "hkjfma_2022": "HKJFMA 2022",
        "hkjfma_2023": "HKJFMA 2023",
        "hkjfma_2024": "HKJFMA 2024",
        "hkjfma_2025": "HKJFMA 2025",
    }
    return mapping.get(source, source)


def main():
    questions = load_questions()
    print(f"Loaded {len(questions)} competition questions")

    # Load all model results
    all_results = {}
    for filename, info in MODELS.items():
        results = load_model_results(filename)
        all_results[info["key"]] = results
        comp_correct = sum(1 for r in results.values() if r.get("correct", False))
        print(f"  {info['name']} ({info['mode']}): {comp_correct}/{len(results)}")

    # Build model metadata list (sorted by accuracy descending)
    model_meta = []
    for filename, info in MODELS.items():
        results = all_results[info["key"]]
        correct = sum(1 for r in results.values() if r.get("correct", False))
        total = len(results)
        model_meta.append({
            "key": info["key"],
            "name": info["name"],
            "provider": info["provider"],
            "mode": info["mode"],
            "correct": correct,
            "total": total,
            "accuracy": round(correct / total, 4) if total > 0 else 0,
        })
    model_meta.sort(key=lambda m: -m["accuracy"])

    # Build per-question detail data
    detail_questions = []
    for q in questions:
        qid = q["id"]
        birth_raw = q.get("birth_info", {}).get("raw", "")
        options_text = [f"{o['letter']}. {o['text']}" for o in q.get("options", [])]

        # Gather each model's answer for this question
        model_answers = {}
        for _filename, info in MODELS.items():
            key = info["key"]
            r = all_results[key].get(qid)
            if r:
                model_answers[key] = {
                    "predicted": r.get("predicted_answer", "?"),
                    "correct": r.get("correct", False),
                }
            else:
                model_answers[key] = {"predicted": "-", "correct": False}

        detail_questions.append({
            "id": qid,
            "source": source_label(q["source"]),
            "year": q.get("year", 0),
            "caseId": q.get("case_id", ""),
            "birth": birth_raw,
            "question": q["question"],
            "options": options_text,
            "answer": q["answer"],
            "category": q["category"],
            "models": model_answers,
        })

    # Group by case for case-level browsing
    cases = {}
    for q in detail_questions:
        case_key = f"{q['source']}_{q['caseId']}"
        if case_key not in cases:
            cases[case_key] = {
                "source": q["source"],
                "caseId": q["caseId"],
                "birth": q["birth"],
                "questions": [],
            }
        cases[case_key]["questions"].append(q)

    output = {
        "models": model_meta,
        "questions": detail_questions,
        "totalQuestions": len(detail_questions),
    }

    # Write as JS
    js_content = (
        "/**\n"
        " * FateryBench per-question detail data.\n"
        f" * Generated from {len(MODELS)} model results.\n"
        f" * {len(detail_questions)} competition questions.\n"
        " */\n\n"
        f"const DETAIL_DATA = {json.dumps(output, indent=2, ensure_ascii=False)};\n"
    )

    with open(OUTPUT_FILE, "w") as f:
        f.write(js_content)

    print(f"\nWrote {OUTPUT_FILE} ({len(js_content)} bytes)")


if __name__ == "__main__":
    main()
