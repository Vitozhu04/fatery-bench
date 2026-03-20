# FateryBench 🔮

**The most comprehensive Chinese metaphysics (命理) prediction benchmark for LLMs.**

FateryBench evaluates how well large language models can analyze Chinese metaphysics (BaZi/Four Pillars) birth charts and make accurate predictions — a task that requires deep domain knowledge, logical reasoning, and pattern recognition.

## Key Numbers

- **300+** multiple-choice questions
- **6** major LLM models tested
- **4** evaluation modes (Vanilla, CoT, Astro-Enhanced, Fatery-Enhanced)
- **12** prediction categories (marriage, career, health, personality, etc.)

## Data Sources

| Source | Questions | Years |
|--------|-----------|-------|
| HKJFMA Competition | 200+ | 2020-2025 |
| Celebrity Cases | 40+ | Verified public figures |

All questions are based on real birth data with verified life events.

## Evaluation Modes

1. **Vanilla** — Raw question, no guidance
2. **Chain-of-Thought (CoT)** — Explicit reasoning before answering
3. **Astro-Enhanced** — Pre-computed birth chart data provided
4. **Fatery-Enhanced** — Professional prompt engineering + pre-computed data (Fatery's proprietary approach)

## Models Tested

| Model | Provider | Notes |
|-------|----------|-------|
| **Fatery** | Fatery.me | Gemini 3 Flash + Fatery-Enhanced prompt |
| Gemini 3 Flash | Google | Fatery base model |
| Gemini 3 Pro | Google | Google's flagship reasoning model |
| GPT-5.3 | OpenAI | OpenAI's latest |
| DeepSeek Thinking | DeepSeek | Reasoning model, Chinese language specialist |

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run benchmark (small sample)
python -m bench --model gemini-3-flash --mode vanilla --sample 10

# Run full benchmark
python -m bench --model gemini-3-flash --mode all

# View results
open docs/index.html
```

## Project Structure

```
fatery-bench/
├── data/
│   ├── hkjfma/           # HKJFMA competition questions by year
│   ├── celebrity/         # Celebrity birth chart cases
│   └── combined.json      # Merged dataset
├── bench/                 # Python benchmark runner
│   ├── runner.py          # Core benchmark logic
│   ├── models/            # Model adapters
│   ├── prompts.py         # Prompt templates (4 modes)
│   └── evaluate.py        # Answer extraction + scoring
├── results/               # Benchmark results (JSON)
├── docs/                  # GitHub Pages leaderboard
└── scripts/               # Data collection scripts
```

## Leaderboard

Visit the [live leaderboard](https://fatery.me/fatery-bench) to see the latest results.

## Citation

If you use FateryBench in your research, please cite:

```bibtex
@misc{faterybench2025,
  title={FateryBench: A Comprehensive Chinese Metaphysics Prediction Benchmark for LLMs},
  author={Fatery Team},
  year={2025},
  url={https://github.com/fatery/fatery-bench}
}
```

## License

MIT License. Data sourced from public HKJFMA competitions and verified public records.

## Credits

- [ftbench](https://github.com/DestinyLinker/ftbench) — Original inspiration and base dataset
- [HKJFMA](https://hkjfma.org) — Hong Kong Junior Fengshui Master Association competition data
- [Fatery.me](https://fatery.me) — Professional Chinese metaphysics analysis platform
