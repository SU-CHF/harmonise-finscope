#!/usr/bin/env python3
"""
Lightweight wrapper to pull a single FinScope wave into `outputs/`.

The script intentionally stays simple so domain experts can tweak it:
    python scripts/clean_year.py 2019
    python scripts/clean_year.py 2019 --keep-columns H3a_13 i1_10 --output-format parquet
"""

import argparse
import sys
from pathlib import Path
from typing import Iterable, List, Optional

import pandas as pd

# Allow importing project-level utilities when running the script directly
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from utils import load_finscope_data  # noqa: E402


def parse_keep_columns(columns: Optional[List[str]]) -> Optional[List[str]]:
    if not columns:
        return None
    parsed = []
    for entry in columns:
        parsed.extend(part.strip() for part in entry.split(",") if part.strip())
    return parsed or None


def ensure_columns(df: pd.DataFrame, columns: Iterable[str]) -> List[str]:
    missing = [col for col in columns if col not in df.columns]
    if missing:
        raise KeyError(f"Missing columns in FinScope dataset: {', '.join(missing)}")
    return list(columns)


def save_dataframe(df: pd.DataFrame, output_path: Path, output_format: str) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_format == "csv":
        df.to_csv(output_path, index=False)
    elif output_format == "parquet":
        df.to_parquet(output_path, index=False)
    else:
        raise ValueError(f"Unsupported output format '{output_format}'.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Export a processed FinScope wave.")
    parser.add_argument("year", type=int, help="Survey year to process (e.g. 2019).")
    parser.add_argument(
        "--keep-columns",
        nargs="*",
        default=None,
        help="Optional list of columns to retain (comma- or space-separated).",
    )
    parser.add_argument(
        "--output-format",
        choices=("csv", "parquet"),
        default="csv",
        help="File format for the processed output.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=REPO_ROOT / "outputs",
        help="Directory to write the processed file.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    df, metadata = load_finscope_data(args.year)
    print(f"Loaded FinScope {args.year}: {len(df):,} rows, {len(df.columns)} columns")

    keep_columns = parse_keep_columns(args.keep_columns)
    if keep_columns:
        keep_columns = ensure_columns(df, keep_columns)
        df = df[keep_columns]
        print(f"Keeping {len(keep_columns)} columns: {', '.join(keep_columns)}")

    output_dir = args.output_dir
    output_path = output_dir / f"finscope_{args.year}_clean.{args.output_format}"
    save_dataframe(df, output_path, args.output_format)

    print(f"Wrote processed file to {output_path.relative_to(REPO_ROOT)}")
    print(f"Variable dictionary is available via metadata.variable_labels (length {len(metadata.variable_labels)})")


if __name__ == "__main__":
    main()
