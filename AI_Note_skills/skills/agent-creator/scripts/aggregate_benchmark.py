#!/usr/bin/env python3
"""
Aggregate agent evaluation results into benchmark summary statistics.

Reads grading.json files from run directories and produces:
- run_summary with mean, stddev, min, max for each metric
- delta between with_skill and without_skill configurations

Usage:
    python -m scripts.aggregate_benchmark <benchmark_dir> --skill-name agent-creator

Directory layout:
    <benchmark_dir>/
    └── eval-N/
        ├── eval_metadata.json
        ├── with_skill/
        │   ├── outputs/
        │   ├── grading.json
        │   └── timing.json
        └── without_skill/
            ├── outputs/
            ├── grading.json
            └── timing.json
"""

import argparse
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path


def calculate_stats(values: list[float]) -> dict:
    """Calculate mean, stddev, min, max for a list of values."""
    if not values:
        return {"mean": 0.0, "stddev": 0.0, "min": 0.0, "max": 0.0}

    n = len(values)
    mean = sum(values) / n

    if n > 1:
        variance = sum((x - mean) ** 2 for x in values) / (n - 1)
        stddev = math.sqrt(variance)
    else:
        stddev = 0.0

    return {
        "mean": round(mean, 4),
        "stddev": round(stddev, 4),
        "min": round(min(values), 4),
        "max": round(max(values), 4),
    }


def load_run_results(benchmark_dir: Path) -> dict:
    """Load all run results from a benchmark directory.

    Returns dict keyed by config name, each containing a list of run results.
    """
    results: dict[str, list] = {}

    for eval_dir in sorted(benchmark_dir.glob("eval-*")):
        if not eval_dir.is_dir():
            continue

        # Read eval metadata
        metadata_path = eval_dir / "eval_metadata.json"
        eval_id = 0
        eval_name = eval_dir.name
        if metadata_path.exists():
            try:
                with open(metadata_path) as f:
                    meta = json.load(f)
                eval_id = meta.get("eval_id", 0)
                eval_name = meta.get("eval_name", eval_dir.name)
            except (json.JSONDecodeError, OSError):
                pass

        # Discover config directories
        for config_dir in sorted(eval_dir.iterdir()):
            if not config_dir.is_dir():
                continue

            # Check for grading.json directly or in run-N subdirs
            grading_files = list(config_dir.glob("grading.json"))
            grading_files.extend(config_dir.glob("run-*/grading.json"))

            if not grading_files:
                continue

            config = config_dir.name
            if config not in results:
                results[config] = []

            for grading_file in grading_files:
                try:
                    with open(grading_file) as f:
                        grading = json.load(f)
                except (json.JSONDecodeError, OSError) as e:
                    print(f"Warning: Cannot read {grading_file}: {e}")
                    continue

                summary = grading.get("summary", {})
                result = {
                    "eval_id": eval_id,
                    "eval_name": eval_name,
                    "configuration": config,
                    "pass_rate": summary.get("pass_rate", 0.0),
                    "passed": summary.get("passed", 0),
                    "failed": summary.get("failed", 0),
                    "total": summary.get("total", 0),
                    "expectations": grading.get("expectations", []),
                }

                # Load timing data
                timing_file = grading_file.parent / "timing.json"
                if timing_file.exists():
                    try:
                        with open(timing_file) as f:
                            timing = json.load(f)
                        result["time_seconds"] = timing.get("total_duration_seconds", 0.0)
                        result["tokens"] = timing.get("total_tokens", 0)
                    except (json.JSONDecodeError, OSError):
                        result["time_seconds"] = 0.0
                        result["tokens"] = 0
                else:
                    result["time_seconds"] = 0.0
                    result["tokens"] = 0

                results[config].append(result)

    return results


def aggregate_results(results: dict) -> dict:
    """Aggregate run results into summary statistics."""
    run_summary = {}
    configs = list(results.keys())

    for config in configs:
        runs = results.get(config, [])
        if not runs:
            run_summary[config] = {
                "pass_rate": calculate_stats([]),
                "time_seconds": calculate_stats([]),
                "tokens": calculate_stats([]),
            }
            continue

        run_summary[config] = {
            "pass_rate": calculate_stats([r["pass_rate"] for r in runs]),
            "time_seconds": calculate_stats([r["time_seconds"] for r in runs]),
            "tokens": calculate_stats([r.get("tokens", 0) for r in runs]),
        }

    # Calculate delta between first two configs
    if len(configs) >= 2:
        primary = run_summary.get(configs[0], {})
        baseline = run_summary.get(configs[1], {})
        delta_pr = primary.get("pass_rate", {}).get("mean", 0) - baseline.get("pass_rate", {}).get("mean", 0)
        delta_time = primary.get("time_seconds", {}).get("mean", 0) - baseline.get("time_seconds", {}).get("mean", 0)
        delta_tokens = primary.get("tokens", {}).get("mean", 0) - baseline.get("tokens", {}).get("mean", 0)
        run_summary["delta"] = {
            "pass_rate": f"{delta_pr:+.2f}",
            "time_seconds": f"{delta_time:+.1f}",
            "tokens": f"{delta_tokens:+.0f}",
        }

    return run_summary


def generate_benchmark(benchmark_dir: Path, skill_name: str = "") -> dict:
    """Generate complete benchmark.json from run results."""
    results = load_run_results(benchmark_dir)
    run_summary = aggregate_results(results)

    runs = []
    for config in results:
        for r in results[config]:
            runs.append({
                "eval_id": r["eval_id"],
                "eval_name": r["eval_name"],
                "configuration": config,
                "result": {
                    "pass_rate": r["pass_rate"],
                    "passed": r["passed"],
                    "failed": r["failed"],
                    "total": r["total"],
                    "time_seconds": r["time_seconds"],
                    "tokens": r.get("tokens", 0),
                },
                "expectations": r["expectations"],
            })

    return {
        "metadata": {
            "skill_name": skill_name or "agent-creator",
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "evals_run": sorted(set(r["eval_id"] for c in results.values() for r in c)),
        },
        "runs": runs,
        "run_summary": run_summary,
        "notes": [],
    }


def generate_markdown(benchmark: dict) -> str:
    """Generate human-readable benchmark.md."""
    meta = benchmark["metadata"]
    summary = benchmark["run_summary"]
    configs = [k for k in summary if k != "delta"]

    lines = [
        f"# Agent-Creator Benchmark: {meta['skill_name']}",
        "",
        f"**Date**: {meta['timestamp']}",
        f"**Evals**: {', '.join(map(str, meta['evals_run']))}",
        "",
        "## Summary",
        "",
    ]

    if len(configs) >= 2:
        a, b = configs[0], configs[1]
        delta = summary.get("delta", {})
        la = a.replace("_", " ").title()
        lb = b.replace("_", " ").title()

        lines.append(f"| Metric | {la} | {lb} | Delta |")
        lines.append("|--------|------|------|-------|")

        for metric, fmt in [("pass_rate", ".0%"), ("time_seconds", ".1f"), ("tokens", ".0f")]:
            av = summary[a].get(metric, {})
            bv = summary[b].get(metric, {})
            if "%" in fmt:
                lines.append(
                    f"| {metric} | {av.get('mean', 0) * 100:.0f}% ± {av.get('stddev', 0) * 100:.0f}% "
                    f"| {bv.get('mean', 0) * 100:.0f}% ± {bv.get('stddev', 0) * 100:.0f}% "
                    f"| {delta.get(metric, '—')} |"
                )
            else:
                lines.append(
                    f"| {metric} | {av.get('mean', 0):{fmt}} ± {av.get('stddev', 0):{fmt}} "
                    f"| {bv.get('mean', 0):{fmt}} ± {bv.get('stddev', 0):{fmt}} "
                    f"| {delta.get(metric, '—')} |"
                )

    if benchmark.get("notes"):
        lines.extend(["", "## Notes", ""])
        for note in benchmark["notes"]:
            lines.append(f"- {note}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Aggregate agent benchmark results")
    parser.add_argument("benchmark_dir", type=Path, help="Benchmark directory path")
    parser.add_argument("--skill-name", default="agent-creator")
    parser.add_argument("--output", "-o", type=Path)

    args = parser.parse_args()

    if not args.benchmark_dir.exists():
        print(f"Directory not found: {args.benchmark_dir}")
        sys.exit(1)

    benchmark = generate_benchmark(args.benchmark_dir, args.skill_name)

    output_json = args.output or (args.benchmark_dir / "benchmark.json")
    output_md = output_json.with_suffix(".md")

    with open(output_json, "w") as f:
        json.dump(benchmark, f, indent=2)
    print(f"Generated: {output_json}")

    md = generate_markdown(benchmark)
    with open(output_md, "w") as f:
        f.write(md)
    print(f"Generated: {output_md}")


if __name__ == "__main__":
    main()
