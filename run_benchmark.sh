#!/bin/bash
# Run FateryBench for all models and modes.
# Usage: ./run_benchmark.sh [--sample N]

set -euo pipefail

SAMPLE_FLAG=""
if [ "${1:-}" = "--sample" ] && [ -n "${2:-}" ]; then
    SAMPLE_FLAG="--sample $2"
fi

MODELS=(
    "gemini-3-flash"
    "gemini-3-pro"
    "gpt-5.3"
    "deepseek-reasoner"
)

MODES=("vanilla" "cot" "astro" "fatery")

for model in "${MODELS[@]}"; do
    for mode in "${MODES[@]}"; do
        echo "========================================"
        echo "Model: $model | Mode: $mode"
        echo "========================================"
        python -m bench --model "$model" --mode "$mode" $SAMPLE_FLAG --workers 4 || echo "FAILED: $model/$mode"
        echo
    done
done

echo "All benchmarks complete. Results in results/"
echo ""
echo "Note: Fatery = gemini-3-flash + fatery mode (fatery-enhanced prompt)"
