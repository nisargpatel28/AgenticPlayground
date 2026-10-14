import tempfile
import unittest
import csv
from pathlib import Path

from content_library import (
    build_stats,
    filter_packs,
    validate_packs,
    write_csv_export,
    write_html_report,
)


class ContentLibraryTests(unittest.TestCase):
    def test_validate_packs_reports_missing_assets_and_prompt(self):
        issues = validate_packs(
            [
                {
                    "pack_id": "broken",
                    "image_path": "missing.jpg",
                    "manifest_path": "missing.json",
                    "prompt": "",
                }
            ]
        )