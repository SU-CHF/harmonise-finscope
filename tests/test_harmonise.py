import unittest

import pandas as pd

from scripts.harmonise import build_indicator


def mapping_row(**overrides):
    values = {
        "field_type": "column",
        "field": "answer",
        "positive_codes": "1",
        "aggregation": "single",
        "exclude_fields": "",
        "missing_policy": "legacy",
    }
    values.update(overrides)
    return pd.Series(values)


class BuildIndicatorMissingPolicyTests(unittest.TestCase):
    def test_legacy_policy_treats_missing_as_negative(self):
        frame = pd.DataFrame({"answer": [1, 2, None]})

        result = build_indicator(frame, mapping_row())

        self.assertEqual(result.tolist(), [1, 0, 0])
        self.assertEqual(str(result.dtype), "int64")

    def test_exclude_policy_preserves_single_field_missing_values(self):
        frame = pd.DataFrame({"answer": [1, 2, None]})

        result = build_indicator(
            frame, mapping_row(missing_policy="exclude")
        )

        self.assertEqual(result.iloc[:2].tolist(), [1, 0])
        self.assertTrue(pd.isna(result.iloc[2]))
        self.assertEqual(str(result.dtype), "Int64")

    def test_exclude_policy_only_excludes_rows_where_all_fields_are_missing(self):
        frame = pd.DataFrame(
            {
                "first": [1, None, None],
                "second": [None, 2, None],
            }
        )
        row = mapping_row(
            field="first;second",
            aggregation="any",
            missing_policy="exclude",
        )

        result = build_indicator(frame, row)

        self.assertEqual(result.iloc[:2].tolist(), [1, 0])
        self.assertTrue(pd.isna(result.iloc[2]))

    def test_unknown_missing_policy_is_rejected(self):
        frame = pd.DataFrame({"answer": [1]})

        with self.assertRaisesRegex(ValueError, "Unsupported missing_policy"):
            build_indicator(frame, mapping_row(missing_policy="unknown"))


if __name__ == "__main__":
    unittest.main()
