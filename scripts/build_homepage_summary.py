#!/usr/bin/env python3
"""
Generate the homepage chart summary JSON from the harmonised wide table.

Usage:
    python scripts/build_homepage_summary.py \
        --input outputs/finscope_harmonised.csv \
        --mapping-file mappings/harmonised_questions.csv \
        --output docs/assets/data/harmonised-summary.json
"""

import argparse
import csv
import json
from pathlib import Path
from typing import Dict, Iterable, List, Optional


def build_indicator_labels(mapping_path: Path, indicators: Iterable[str]) -> Dict[str, str]:
    """Return a mapping of indicator ids to human-readable labels."""
    if not mapping_path.exists():
        return {indicator: indicator.replace("_", " ").title() for indicator in indicators}

    labels: Dict[str, str] = {}
    with mapping_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            indicator_id = row.get("indicator_id")
            indicator_label = row.get("indicator_label")
            if not indicator_id:
                continue
            labels.setdefault(indicator_id, indicator_label or indicator_id.replace("_", " ").title())

    return {indicator: labels.get(indicator, indicator.replace("_", " ").title()) for indicator in indicators}


def format_value(value: Optional[float]) -> Optional[float]:
    """Convert a share to a rounded percentage."""
    if value is None:
        return None
    return round(float(value) * 100, 1)


def read_harmonised_rows(input_path: Path) -> List[Dict[str, Optional[float]]]:
    """Load the harmonised wide CSV without third-party dependencies."""
    with input_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError("Harmonised table is missing header row.")

        indicator_cols = [col for col in reader.fieldnames if col != "year"]
        if not indicator_cols:
            raise ValueError("No indicator columns found in the harmonised wide table.")

        records: List[Dict[str, Optional[float]]] = []
        for row in reader:
            entry: Dict[str, Optional[float]] = {}
            try:
                entry["year"] = int(float(row["year"]))
            except (TypeError, ValueError):
                continue

            for indicator in indicator_cols:
                raw_value = row.get(indicator)
                if raw_value in (None, "", "NA"):
                    entry[indicator] = None
                    continue
                try:
                    entry[indicator] = float(raw_value)
                except ValueError:
                    entry[indicator] = None

            records.append(entry)

    return records


def build_summary(input_path: Path, mapping_path: Path) -> Dict[str, List[Dict]]:
    """Read the harmonised wide CSV and return metadata plus series records."""
    if not input_path.exists():
        raise FileNotFoundError(f"Harmonised table not found: {input_path}")

    records = read_harmonised_rows(input_path)
    if not records:
        raise ValueError("No rows found in the harmonised wide table.")

    indicator_cols = [key for key in records[0].keys() if key != "year"]

    labels = build_indicator_labels(mapping_path, indicator_cols)

    series = []
    for record in records:
        entry = {"year": int(record["year"])}
        for indicator in indicator_cols:
            entry[indicator] = format_value(record.get(indicator))
        series.append(entry)

    return {"indicator_labels": labels, "series": series}


def write_summary(summary: Dict, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, indent=2))
    print(f"Wrote homepage summary JSON to {output_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build homepage summary data for the docs chart.")
    parser.add_argument("--input", type=Path, required=True, help="Path to the harmonised wide CSV.")
    parser.add_argument(
        "--mapping-file",
        type=Path,
        default=Path("mappings/harmonised_questions.csv"),
        help="Mapping file used to derive indicator labels.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("docs/assets/data/harmonised-summary.json"),
        help="Destination for the generated JSON file.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = build_summary(args.input, args.mapping_file)
    write_summary(summary, args.output)


if __name__ == "__main__":
    main()
