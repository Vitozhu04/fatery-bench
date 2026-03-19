"""CLI entry point: python -m bench.runner [options]"""

import click

from bench.runner import BenchmarkConfig, run_benchmark


@click.command()
@click.option("--model", required=True, help="Model name (e.g., gemini-2.5-flash, gpt-4o)")
@click.option("--mode", default="vanilla", type=click.Choice(["vanilla", "cot", "astro", "fatery", "all"]))
@click.option("--sample", default=None, type=int, help="Number of questions to sample")
@click.option("--seed", default=42, type=int)
@click.option("--workers", default=4, type=int, help="Concurrent workers")
@click.option("--category", default=None, help="Filter by category (e.g., 婚姻, 事业)")
@click.option("--source", default=None, help="Filter by source (e.g., hkjfma_2025, celebrity)")
@click.option("--data", default="data/combined.json", help="Path to data file")
def main(model, mode, sample, seed, workers, category, source, data):
    """Run FateryBench evaluation."""
    modes = ["vanilla", "cot", "astro", "fatery"] if mode == "all" else [mode]

    for m in modes:
        config = BenchmarkConfig(
            model_name=model,
            mode=m,
            sample=sample,
            seed=seed,
            workers=workers,
            data_path=data,
            category=category,
            source=source,
        )
        run_benchmark(config)
        print()


if __name__ == "__main__":
    main()
