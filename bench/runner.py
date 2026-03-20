"""Core benchmark runner — evaluates by case (batch) to minimize API calls."""

import json
import random
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from tqdm import tqdm

from bench.evaluate import calculate_accuracy, extract_batch_answers
from bench.models import create_client
from bench.models.base import ModelClient
from bench.prompts import build_batch_prompt, get_system_prompt

PROJECT_ROOT = Path(__file__).parent.parent


@dataclass
class BenchmarkConfig:
    model_name: str
    mode: str = "baseline"
    sample: int | None = None
    seed: int = 42
    workers: int = 4
    data_path: str = "data/combined.json"
    output_dir: str = "results"
    category: str | None = None
    source: str | None = None


@dataclass
class QuestionResult:
    question_id: str
    source: str
    category: str
    question: str
    correct_answer: str
    predicted_answer: str | None
    correct: bool
    response: str
    response_time: float
    error: str | None = None


def load_questions(config: BenchmarkConfig) -> list[dict]:
    """Load and optionally filter/sample questions."""
    data_path = PROJECT_ROOT / config.data_path
    with open(data_path, encoding="utf-8") as f:
        data = json.load(f)

    questions = data["questions"]

    if config.category:
        questions = [q for q in questions if q.get("category") == config.category]

    if config.source:
        questions = [q for q in questions if config.source in q.get("source", "")]

    if config.sample and config.sample < len(questions):
        rng = random.Random(config.seed)
        questions = rng.sample(questions, config.sample)

    return questions


def group_by_case(questions: list[dict]) -> list[list[dict]]:
    """Group questions by case_id so each case is one API call."""
    cases: dict[str, list[dict]] = defaultdict(list)
    for q in questions:
        key = q.get("case_id", q["id"])
        cases[key].append(q)
    return list(cases.values())


def evaluate_case(
    client: ModelClient,
    case_questions: list[dict],
    mode: str,
) -> list[QuestionResult]:
    """Evaluate all questions for one case in a single API call."""
    prompt = build_batch_prompt(case_questions, mode=mode)
    system = get_system_prompt(mode)

    start = time.time()
    error = None
    response = ""

    try:
        response = client.generate(prompt, system=system)
    except Exception as e:
        error = str(e)

    elapsed = time.time() - start

    if error:
        answers = [None] * len(case_questions)
    else:
        answers = extract_batch_answers(response, len(case_questions))

    results = []
    for q, predicted in zip(case_questions, answers):
        correct = predicted == q["answer"] if predicted else False
        results.append(QuestionResult(
            question_id=q["id"],
            source=q.get("source", "unknown"),
            category=q.get("category", "unknown"),
            question=q["question"],
            correct_answer=q["answer"],
            predicted_answer=predicted,
            correct=correct,
            response=response,
            response_time=round(elapsed, 2),
            error=error,
        ))

    return results


def run_benchmark(config: BenchmarkConfig) -> dict[str, Any]:
    """Run the full benchmark and return results."""
    questions = load_questions(config)
    if not questions:
        raise ValueError("No questions to evaluate after filtering.")

    cases = group_by_case(questions)
    client = create_client(config.model_name)
    results: list[QuestionResult] = []

    print(f"Running FateryBench: {config.model_name} / {config.mode} mode")
    print(f"Questions: {len(questions)} | Cases: {len(cases)} | Workers: {config.workers}")
    print("-" * 60)

    if config.workers <= 1:
        for case_qs in tqdm(cases, desc="Evaluating"):
            results.extend(evaluate_case(client, case_qs, config.mode))
    else:
        with ThreadPoolExecutor(max_workers=config.workers) as executor:
            futures = {
                executor.submit(evaluate_case, client, case_qs, config.mode): case_qs
                for case_qs in cases
            }
            for future in tqdm(
                as_completed(futures), total=len(futures), desc="Evaluating"
            ):
                results.extend(future.result())

    results.sort(key=lambda r: r.question_id)

    result_dicts = [
        {
            "question_id": r.question_id,
            "source": r.source,
            "category": r.category,
            "question": r.question,
            "correct_answer": r.correct_answer,
            "predicted_answer": r.predicted_answer,
            "correct": r.correct,
            "response": r.response,
            "response_time": r.response_time,
            "error": r.error,
        }
        for r in results
    ]

    metrics = calculate_accuracy(result_dicts)

    output = {
        "benchmark": "FateryBench",
        "version": "1.1",
        "model": config.model_name,
        "mode": config.mode,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "config": {
            "sample": config.sample,
            "seed": config.seed,
            "workers": config.workers,
            "category_filter": config.category,
            "source_filter": config.source,
        },
        "metrics": metrics,
        "results": result_dicts,
    }

    out_dir = PROJECT_ROOT / config.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    safe_model = config.model_name.replace("/", "_")
    out_path = out_dir / f"{safe_model}_{config.mode}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    # Print summary
    print("\n" + "=" * 60)
    print(f"Model: {config.model_name} | Mode: {config.mode}")
    print(f"Overall: {metrics['correct']}/{metrics['total']} = {metrics['accuracy']:.1%}")
    print("\nBy Category:")
    for cat, stats in metrics["by_category"].items():
        print(f"  {cat}: {stats['correct']}/{stats['total']} = {stats['accuracy']:.1%}")
    if metrics.get("by_source"):
        print("\nBy Source:")
        for src, stats in metrics["by_source"].items():
            print(f"  {src}: {stats['correct']}/{stats['total']} = {stats['accuracy']:.1%}")
    print(f"\nResults saved to: {out_path}")

    return output
