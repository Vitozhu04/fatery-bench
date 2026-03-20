#!/bin/bash
# Run FateryBench for all models.
# Usage: ./run_benchmark.sh [--sample N]

set -euo pipefail

SAMPLE_FLAG=""
if [ "${1:-}" = "--sample" ] && [ -n "${2:-}" ]; then
    SAMPLE_FLAG="--sample $2"
fi

echo "========================================="
echo "FateryBench — Baseline (all models)"
echo "========================================="

for model in gemini-3-flash-preview gemini-3-pro-preview gpt-5.4 deepseek-reasoner; do
    echo ""
    echo "--- $model ---"
    python -m bench --model "$model" --mode baseline $SAMPLE_FLAG --workers 4 || echo "FAILED: $model"
done

echo ""
echo "========================================="
echo "FateryBench — Fatery (gemini-3-flash-preview + prompt)"
echo "========================================="
python -m bench --model gemini-3-flash-preview --mode fatery $SAMPLE_FLAG --workers 4 || echo "FAILED: fatery"

echo ""
echo "Done. Results in results/"
