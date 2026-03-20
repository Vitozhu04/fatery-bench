# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FateryBench is a benchmark for evaluating LLMs on Chinese metaphysics (BaZi/Four Pillars 八字命理) prediction tasks. It uses multiple-choice questions from HKJFMA competitions (2022-2025) and celebrity birth chart cases, testing models in two modes: **baseline** (simple prompt) and **fatery** (professional prompt engineering + pre-computed chart data).

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run benchmark for a single model
python -m bench --model gemini-3-flash --mode baseline --sample 10

# Run all models
./run_benchmark.sh              # full run
./run_benchmark.sh --sample 10  # sampled run

# Data pipeline scripts
python scripts/transform_ftbench.py   # Transform ftbench source data into FateryBench schema
python scripts/build_celebrity.py     # Rebuild celebrity cases and merge into combined.json
python scripts/add_2020_data.py       # Add 2020 competition data
```

## Architecture

### Benchmark Pipeline

`__main__.py` (CLI via click) → `runner.py` (orchestration) → `models/` (LLM calls) → `evaluate.py` (answer extraction + scoring)

1. **CLI** (`bench/__main__.py`): Click-based entry point. Key options: `--model`, `--mode {baseline,fatery}`, `--sample`, `--workers`, `--category`, `--source`.
2. **Runner** (`bench/runner.py`): Loads questions from `data/combined.json`, dispatches to model clients with `ThreadPoolExecutor`, collects `QuestionResult`s, saves results JSON to `results/`.
3. **Prompts** (`bench/prompts.py`): Two prompt strategies — `_baseline_prompt` (simple BaZi analyst prompt) and `_fatery_prompt` (structured 4-step analysis with pre-computed chart data via `_compute_bazi_chart`).
4. **Evaluation** (`bench/evaluate.py`): Regex-based answer extraction (`extract_answer`) with Chinese-aware patterns (答案：X, 选择：X, etc.), plus `calculate_accuracy` for per-category and per-source breakdowns.

### Model Adapters

All extend `ModelClient` (ABC in `bench/models/base.py`) with a `generate(prompt, system)` method:

| Adapter | File | API Key Env Var |
|---------|------|-----------------|
| `GeminiClient` | `models/google.py` | `GOOGLE_API_KEY` or `GEMINI_API_KEY` |
| `OpenAIClient` | `models/openai_client.py` | `OPENAI_API_KEY` |
| `DeepSeekClient` | `models/deepseek.py` | `DEEPSEEK_API_KEY` |
| `AnthropicClient` | `models/anthropic_client.py` | `ANTHROPIC_API_KEY` |

Model registry is in `bench/models/__init__.py`. Note: `AnthropicClient` exists but is not registered in `MODEL_REGISTRY`. The "Fatery" model is `gemini-3-flash` run in `fatery` mode.

### Data Schema

Questions in `data/combined.json` follow this structure:
```json
{
  "id": "fb_0001",
  "source": "hkjfma_2024",
  "case_id": "case_21",
  "birth_info": { "raw": "...", "gender": "男", "year": 1990, "month": 3, "day": 15, "hour": 8, "minute": 0, "location": "...", "calendar_type": "solar" },
  "question": "...",
  "options": [{"letter": "A", "text": "..."}, ...],
  "answer": "B",
  "category": "婚姻",
  "difficulty": "medium",
  "year": 2024
}
```

Categories: 婚姻, 事业, 家庭, 健康, 性格, 学业, 财运, 运势, 子女, 外貌, 灾劫, 官非.

### Output

Results are saved to `results/{model}_{mode}.json`. The leaderboard at `docs/index.html` reads from `docs/data.js`.
