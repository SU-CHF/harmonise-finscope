#!/usr/bin/env python3
"""
Generate a harmonised FinScope time series using simple CSV mappings.

Usage:
    python scripts/harmonise.py
    python scripts/harmonise.py --mapping-file mappings/harmonised_questions.csv --output outputs/finscope_harmonised.csv
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, Iterable, List

import numpy as np
import pandas as pd

# Allow importing project-level utilities when running the script directly
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from utils import load_finscope_data  # noqa: E402


def parse_codes(raw: str) -> List:
    """Split a pipe- or semicolon-delimited list of codes and cast numerics when possible."""
    if pd.isna(raw) or raw == "":
        return []
    codes = []
    for chunk in str(raw).replace(";", "|").split("|"):
        item = chunk.strip()
        if item == "":
            continue
        try:
            # Attempt numeric conversion so 3 matches both string and numeric columns.
            casted = pd.to_numeric(item)
            codes.append(casted)
            # Also keep the original string form in case the column is object-typed.
            codes.append(item)
        except (ValueError, TypeError):
            codes.append(item)
    # Remove duplicates while preserving order
    seen = set()
    ordered_codes = []
    for code in codes:
        if code in seen:
            continue
        seen.add(code)
        ordered_codes.append(code)
    return ordered_codes


def resolve_columns(df: pd.DataFrame, row: pd.Series) -> List[str]:
    """Return a list of columns described by a mapping row."""
    field_type = row["field_type"]
    field = row["field"]
    exclude_raw = row.get("exclude_fields", "")
    exclude: Iterable[str] = []
    if isinstance(exclude_raw, str) and exclude_raw.strip():
        exclude = [col.strip() for col in exclude_raw.replace(";", "|").split("|") if col.strip()]

    if field_type == "column":
        columns = [col.strip() for col in str(field).split(";") if col.strip()]
    elif field_type == "prefix":
        prefix = str(field)
        columns = [col for col in df.columns if col.startswith(prefix)]
    else:
        raise ValueError(f"Unsupported field_type '{field_type}' in mapping row:\n{row}")

    columns = [col for col in columns if col not in exclude]
    if not columns:
        raise KeyError(f"No columns matched for mapping row:\n{row}")
    return columns


def build_indicator(df: pd.DataFrame, row: pd.Series) -> pd.Series:
    """Create an indicator Series from mapping instructions."""
    columns = resolve_columns(df, row)
    codes = parse_codes(row["positive_codes"])
    aggregation = row.get("aggregation", "single")

    if aggregation == "single":
        if len(columns) != 1:
            raise ValueError(
                f"'single' aggregation expects exactly one column, got {columns} for mapping row:\n{row}"
            )
        series = df[columns[0]].isin(codes)
    elif aggregation == "any":
        frame = df[columns]
        if codes:
            series = frame.isin(codes).any(axis=1)
        else:
            series = frame.any(axis=1)
    elif aggregation == "all":
        frame = df[columns]
        if codes:
            series = frame.isin(codes).all(axis=1)
        else:
            series = frame.all(axis=1)
    else:
        raise ValueError(f"Unsupported aggregation '{aggregation}' in mapping row:\n{row}")

    return series.astype(int)


def load_weights(weights_path: Path) -> Dict[int, str]:
    """Read the year-to-weight-variable mapping CSV."""
    weights = pd.read_csv(weights_path)
    if "year" not in weights or "weight_var" not in weights:
        raise ValueError("Weight metadata must include 'year' and 'weight_var' columns.")
    weight_map: Dict[int, str] = {}
    for entry in weights.itertuples(index=False):
        year = int(entry.year)
        weight_var = getattr(entry, "weight_var", "")
        weight_map[year] = str(weight_var) if isinstance(weight_var, str) and weight_var else ""
    return weight_map


def weighted_mean(series: pd.Series, weights: pd.Series) -> float:
    """Return a weighted mean handling missing values gracefully."""
    aligned = pd.concat([series, weights], axis=1).dropna()
    if aligned.empty:
        return float("nan")
    weight_values = aligned.iloc[:, 1]
    total_weight = weight_values.sum()
    if total_weight == 0:
        return float("nan")
    return float(np.average(aligned.iloc[:, 0], weights=weight_values))


def harmonise(
    mapping_path: Path,
    weights_path: Path,
    output_path: Path,
    long_output_path: Path | None = None,
) -> pd.DataFrame:
    """Create harmonised indicators for each year and persist wide/long outputs."""
    mapping = pd.read_csv(mapping_path)
    weight_map = load_weights(weights_path)

    required_cols = {"indicator_id", "indicator_label", "year", "field_type", "field", "positive_codes"}
    missing = required_cols - set(mapping.columns)
    if missing:
        raise ValueError(f"Mapping file is missing required columns: {', '.join(sorted(missing))}")

    output_records = []
    long_records = []

    for year, year_mapping in mapping.groupby("year"):
        year = int(year)
        print(f"Harmonising {year}…")
        df, _metadata = load_finscope_data(year)

        label_lookup = (
            year_mapping.drop_duplicates(subset=["indicator_id"])
            .set_index("indicator_id")["indicator_label"]
            .to_dict()
        )

        for row in year_mapping.itertuples(index=False):
            row_series = pd.Series(row._asdict())
            indicator_id = str(row_series["indicator_id"])
            indicator_label = label_lookup[indicator_id]
            indicator_series = build_indicator(df, row_series)
            df[indicator_id] = indicator_series

            long_records.append(
                {
                    "year": year,
                    "indicator_id": indicator_id,
                    "indicator_label": indicator_label,
                    "value": indicator_series.mean(),
                    "weighting": "unweighted",
                }
            )

        # Weighted summary for the year
        year_record: Dict[str, float | int] = {"year": year}
        weight_var = weight_map.get(year, "")
        weight_series = df[weight_var] if weight_var and weight_var in df.columns else None

        for indicator_id in year_mapping["indicator_id"].unique():
            indicator_series = df[indicator_id].astype(float)
            if weight_series is not None:
                value = weighted_mean(indicator_series, weight_series)
                long_records.append(
                    {
                        "year": year,
                        "indicator_id": indicator_id,
                        "indicator_label": label_lookup[indicator_id],
                        "value": value,
                        "weighting": "weighted",
                    }
                )
            else:
                value = indicator_series.mean()

            year_record[indicator_id] = value

        output_records.append(year_record)

    wide = pd.DataFrame(output_records).sort_values("year").reset_index(drop=True)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    wide.to_csv(output_path, index=False)
    try:
        rel_output = output_path.resolve().relative_to(REPO_ROOT)
    except ValueError:
        rel_output = output_path
    print(f"Wrote wide harmonised table to {rel_output}")

    if long_output_path:
        long_df = pd.DataFrame(long_records)
        long_output_path.parent.mkdir(parents=True, exist_ok=True)
        long_df.to_csv(long_output_path, index=False)
        try:
            rel_long = long_output_path.resolve().relative_to(REPO_ROOT)
        except ValueError:
            rel_long = long_output_path
        print(f"Wrote long harmonised table to {rel_long}")

    return wide


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create a harmonised FinScope series.")
    parser.add_argument(
        "--mapping-file",
        default=REPO_ROOT / "mappings" / "harmonised_questions.csv",
        type=Path,
        help="CSV with per-year mapping instructions.",
    )
    parser.add_argument(
        "--weights-file",
        default=REPO_ROOT / "mappings" / "year_weights.csv",
        type=Path,
        help="CSV mapping survey year to the appropriate weight variable.",
    )
    parser.add_argument(
        "--output",
        default=REPO_ROOT / "outputs" / "finscope_harmonised.csv",
        type=Path,
        help="Path for the wide harmonised output.",
    )
    parser.add_argument(
        "--long-output",
        type=Path,
        default=None,
        help="Optional path for a long-format table (indicator per row).",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    harmonise(
        mapping_path=args.mapping_file,
        weights_path=args.weights_file,
        output_path=args.output,
        long_output_path=args.long_output,
    )


if __name__ == "__main__":
    main()
