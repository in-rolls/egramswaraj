"""Offline checks for parsing rules and the published data contract."""

import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd
from pandera.errors import SchemaErrors

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "bin"))

import build_er  # noqa: E402


class ParserTests(unittest.TestCase):
    def test_ward_numbers_do_not_infer_from_place_names(self):
        for name, expected in [
            ("Ward No. 12", 12),
            ("3", 3),
            ("Bambooflat-2", None),
            (pd.NA, None),
        ]:
            with self.subTest(name=name):
                self.assertEqual(build_er.ward_no(name), expected)

    def test_placeholder_names(self):
        for name in [pd.NA, "1234", "  SARPANCH  ", "xxxx"]:
            with self.subTest(name=name):
                self.assertTrue(build_er.is_placeholder(name))
        self.assertFalse(build_er.is_placeholder("Example Person"))

    def test_alternate_block_counts_preserve_zero(self):
        self.assertEqual(build_er.site_er({"gperCount": None, "bperCount": 9}), 9)
        self.assertEqual(build_er.site_er({"gperCount": 0, "bperCount": 9}), 0)

    def test_only_complete_states_are_built(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory)
            (source / "run.out").write_text(
                "state 2: 5/5 GPs saved\nstate 6: 3/5 GPs saved\ninterrupted\n"
            )
            self.assertEqual(build_er.finished_states(source), {2: 5})


class PublishedDataTests(unittest.TestCase):
    def test_published_tables_match_their_schemas(self):
        for name, dtypes in [("gps", build_er.GPS_DTYPES), ("members", build_er.MEMBERS_DTYPES)]:
            with self.subTest(table=name):
                frame = build_er.validate(
                    ROOT / "data" / f"{name}.parquet",
                    ROOT / "schema" / f"{name}.schema.json",
                    dtypes,
                )
                self.assertGreater(len(frame), 0)

    def test_schema_rejects_duplicate_primary_keys(self):
        row = pd.read_parquet(ROOT / "data" / "members.parquet").head(1)
        with tempfile.TemporaryDirectory() as directory:
            duplicate = Path(directory) / "members.parquet"
            pd.concat([row, row], ignore_index=True).to_parquet(duplicate)
            with self.assertRaises(SchemaErrors):
                build_er.validate(
                    duplicate, ROOT / "schema" / "members.schema.json", build_er.MEMBERS_DTYPES
                )
