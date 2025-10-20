#!/usr/bin/env python3
"""
Quick helper to inspect or export summaries from the harmonised table.

Examples:
    python scripts/summary_table.py
    python scripts/summary_table.py --long-output outputs/finscope_harmonised_long.csv
"""

import argparse
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Summarise the harmonised FinScope dataset.")
    parser.add_argument(
        "--input",
        type=Path,
        default=REPO_ROOT / "outputs" / "finscope_harmonised.csv",
        help="Path to the wide harmonised CSV.",
    )
    parser.add_argument(
        "--long-output",
        type=Path,
        default=None,
        help="Optional path to write a long (tidy) version of the table.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    table = pd.read_csv(args.input)
    table_sorted = table.sort_values("year").reset_index(drop=True)
    print("Harmonised indicators (weighted shares unless otherwise noted):")
    print(table_sorted.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    if args.long_output:
        long_df = table_sorted.melt(id_vars="year", var_name="indicator_id", value_name="value")
        args.long_output.parent.mkdir(parents=True, exist_ok=True)
        long_df.to_csv(args.long_output, index=False)
        rel_path = args.long_output.relative_to(REPO_ROOT)
        print(f"Wrote long-format table to {rel_path}")


if __name__ == "__main__":
    main()
