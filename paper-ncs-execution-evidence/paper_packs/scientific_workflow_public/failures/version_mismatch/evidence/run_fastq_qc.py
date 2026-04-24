#!/usr/bin/env python3
from __future__ import annotations

import argparse
import gzip
import json
from pathlib import Path
from typing import TextIO


def open_fastq(path: Path) -> TextIO:
    if path.name.endswith((".fastq.gz", ".fq.gz", ".fastqsanger.gz")):
        return gzip.open(path, "rt", encoding="utf-8")
    return path.open("r", encoding="utf-8")


def sample_name(path: Path) -> str:
    name = path.name
    for suffix in (".fastqsanger.gz", ".fastq.gz", ".fq.gz", ".fastq", ".fq"):
        if name.endswith(suffix):
            return name[: -len(suffix)]
    return path.stem


def empty_accumulator() -> dict[str, int]:
    return {
        "base_count": 0,
        "gc_count": 0,
        "max_read_length": 0,
        "min_read_length": 0,
        "n_count": 0,
        "quality_sum": 0,
        "read_count": 0,
        "valid_base_count": 0,
    }


def add_record(accumulator: dict[str, int], sequence: str, quality: str) -> None:
    read_length = len(sequence)
    accumulator["read_count"] += 1
    accumulator["base_count"] += read_length
    accumulator["quality_sum"] += sum(ord(char) - 33 for char in quality)

    if accumulator["read_count"] == 1:
        accumulator["min_read_length"] = read_length
        accumulator["max_read_length"] = read_length
    else:
        accumulator["min_read_length"] = min(accumulator["min_read_length"], read_length)
        accumulator["max_read_length"] = max(accumulator["max_read_length"], read_length)

    for base in sequence.upper():
        if base == "N":
            accumulator["n_count"] += 1
        elif base in {"A", "C", "G", "T"}:
            accumulator["valid_base_count"] += 1
            if base in {"G", "C"}:
                accumulator["gc_count"] += 1


def finalize_metrics(accumulator: dict[str, int]) -> dict[str, float | int]:
    read_count = accumulator["read_count"]
    base_count = accumulator["base_count"]
    valid_base_count = accumulator["valid_base_count"]
    gc_count = accumulator["gc_count"]
    return {
        "base_count": base_count,
        "gc_count": gc_count,
        "gc_fraction": gc_count / valid_base_count if valid_base_count else 0.0,
        "max_read_length": accumulator["max_read_length"] if read_count else 0,
        "mean_phred_quality": accumulator["quality_sum"] / base_count if base_count else 0.0,
        "mean_read_length": base_count / read_count if read_count else 0.0,
        "min_read_length": accumulator["min_read_length"] if read_count else 0,
        "n_count": accumulator["n_count"],
        "read_count": read_count,
        "valid_base_count": valid_base_count,
    }


def parse_fastq_metrics(path: Path) -> dict[str, float | int | str]:
    accumulator = empty_accumulator()
    line_count = 0
    with open_fastq(path) as handle:
        while True:
            header = handle.readline()
            if not header:
                break
            sequence = handle.readline()
            plus = handle.readline()
            quality = handle.readline()
            line_count += 4
            if not sequence or not plus or not quality:
                raise ValueError(f"FASTQ record is incomplete near line {line_count}: {path}")

            header = header.rstrip("\n\r")
            sequence = sequence.rstrip("\n\r")
            plus = plus.rstrip("\n\r")
            quality = quality.rstrip("\n\r")
            record_number = line_count // 4
            if not header.startswith("@"):
                raise ValueError(f"Record {record_number} header does not start with @")
            if not plus.startswith("+"):
                raise ValueError(f"Record {record_number} separator does not start with +")
            if len(sequence) != len(quality):
                raise ValueError(f"Record {record_number} sequence and quality lengths differ")
            add_record(accumulator, sequence, quality)

    metrics = finalize_metrics(accumulator)
    metrics["filename"] = path.name
    metrics["sample_name"] = sample_name(path)
    return metrics


def parse_fastq(path: Path) -> list[tuple[str, str, str]]:
    records: list[tuple[str, str, str]] = []
    line_count = 0
    with open_fastq(path) as handle:
        while True:
            header = handle.readline()
            if not header:
                break
            sequence = handle.readline()
            plus = handle.readline()
            quality = handle.readline()
            line_count += 4
            if not sequence or not plus or not quality:
                raise ValueError(f"FASTQ record is incomplete near line {line_count}: {path}")

            header = header.rstrip("\n\r")
            sequence = sequence.rstrip("\n\r")
            plus = plus.rstrip("\n\r")
            quality = quality.rstrip("\n\r")
            record_number = line_count // 4
            if not header.startswith("@"):
                raise ValueError(f"Record {record_number} header does not start with @")
            if not plus.startswith("+"):
                raise ValueError(f"Record {record_number} separator does not start with +")
            if len(sequence) != len(quality):
                raise ValueError(f"Record {record_number} sequence and quality lengths differ")
            records.append((header[1:], sequence.upper(), quality))
    return records


def compute_metrics(records: list[tuple[str, str, str]]) -> dict[str, float | int]:
    accumulator = empty_accumulator()
    for _, sequence, quality in records:
        add_record(accumulator, sequence, quality)
    return finalize_metrics(accumulator)


def compute_aggregate(sample_metrics: list[dict[str, float | int | str]]) -> dict[str, float | int]:
    total_read_count = sum(int(item["read_count"]) for item in sample_metrics)
    total_base_count = sum(int(item["base_count"]) for item in sample_metrics)
    total_valid_base_count = sum(int(item["valid_base_count"]) for item in sample_metrics)
    total_gc_count = sum(int(item["gc_count"]) for item in sample_metrics)
    total_n_count = sum(int(item["n_count"]) for item in sample_metrics)
    quality_sum = sum(
        float(item["mean_phred_quality"]) * int(item["base_count"]) for item in sample_metrics
    )
    min_lengths = [int(item["min_read_length"]) for item in sample_metrics if item["read_count"]]
    max_lengths = [int(item["max_read_length"]) for item in sample_metrics if item["read_count"]]
    return {
        "aggregate_gc_fraction": total_gc_count / total_valid_base_count
        if total_valid_base_count
        else 0.0,
        "max_read_length": max(max_lengths) if max_lengths else 0,
        "mean_phred_quality": quality_sum / total_base_count if total_base_count else 0.0,
        "mean_read_length": total_base_count / total_read_count if total_read_count else 0.0,
        "min_read_length": min(min_lengths) if min_lengths else 0,
        "sample_count": len(sample_metrics),
        "total_base_count": total_base_count,
        "total_gc_count": total_gc_count,
        "total_n_count": total_n_count,
        "total_read_count": total_read_count,
        "total_valid_base_count": total_valid_base_count,
    }


def build_metrics(paths: list[Path]) -> dict[str, object]:
    samples = [parse_fastq_metrics(path) for path in paths]
    aggregate = compute_aggregate(samples)
    metrics: dict[str, object] = {
        "aggregate": aggregate,
        "samples": samples,
    }
    # Backwards-compatible aliases used by the smoke-pack builder.
    metrics.update(
        {
            "base_count": aggregate["total_base_count"],
            "gc_count": aggregate["total_gc_count"],
            "gc_fraction": aggregate["aggregate_gc_fraction"],
            "max_read_length": aggregate["max_read_length"],
            "mean_phred_quality": aggregate["mean_phred_quality"],
            "mean_read_length": aggregate["mean_read_length"],
            "min_read_length": aggregate["min_read_length"],
            "n_count": aggregate["total_n_count"],
            "read_count": aggregate["total_read_count"],
            "valid_base_count": aggregate["total_valid_base_count"],
        }
    )
    return metrics


def write_report(metrics: dict[str, object], path: Path) -> None:
    lines = [
        "FASTQ QC report",
        "Deterministic Phred+33 FASTQ QC metrics.",
        "",
        "Aggregate",
    ]
    aggregate = metrics.get("aggregate")
    if isinstance(aggregate, dict):
        for key in sorted(aggregate):
            lines.append(f"{key}: {aggregate[key]}")
    else:
        for key in sorted(metrics):
            lines.append(f"{key}: {metrics[key]}")

    lines.append("")
    lines.append("Samples")
    samples = metrics.get("samples")
    if isinstance(samples, list):
        for sample in samples:
            if not isinstance(sample, dict):
                continue
            lines.append(f"- {sample.get('sample_name')} ({sample.get('filename')})")
            for key in sorted(k for k in sample if k not in {"filename", "sample_name"}):
                lines.append(f"  {key}: {sample[key]}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run deterministic FASTQ QC.")
    parser.add_argument("--input", required=True, action="append", type=Path)
    parser.add_argument("--metrics", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    args = parser.parse_args()

    metrics = build_metrics(args.input)

    args.metrics.parent.mkdir(parents=True, exist_ok=True)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.metrics.write_text(
        json.dumps(metrics, sort_keys=True, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    write_report(metrics, args.report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
