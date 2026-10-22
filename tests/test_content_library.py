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

        self.assertEqual(len(issues), 3)
        self.assertTrue(any("image not found" in issue["issue"] for issue in issues))
        self.assertTrue(any("manifest not found" in issue["issue"] for issue in issues))
        self.assertTrue(any(issue["issue"] == "missing prompt" for issue in issues))

    def test_write_csv_export_preserves_pack_metadata(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_path = Path(temp_dir) / "exports" / "packs.csv"
            write_csv_export(
                [
                    {
                        "pack_id": "pack-1",
                        "prompt": "A city",
                        "caption": "A caption, with comma",
                        "alt_text": "A city image",
                        "hashtags": ["#city", "#night"],
                        "image_path": "output/pack-1/final_image.jpg",
                        "manifest_path": "output/pack-1/manifest.json",
                    }
                ],
                str(csv_path),
            )

            with csv_path.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))

            self.assertEqual(rows[0]["pack_id"], "pack-1")
            self.assertEqual(rows[0]["caption"], "A caption, with comma")
            self.assertEqual(rows[0]["hashtags"], "#city #night")

    def test_filter_packs_and_build_stats(self):
        packs = [
            {"pack_id": "b", "prompt": "Ocean", "caption": "B", "hashtags": ["#Travel"], "image_path": "b.jpg"},
            {"pack_id": "a", "prompt": "Mountain", "caption": "A", "hashtags": ["#travel", "#nature"], "image_path": "a.jpg"},
        ]

        selected = filter_packs(packs, hashtags=["nature"], sort_by="prompt", limit=1)

        self.assertEqual([pack["pack_id"] for pack in selected], ["a"])
        self.assertEqual(build_stats(selected), {"total": 1, "with_images": 1, "hashtags": {"#travel": 1, "#nature": 1}})

    def test_write_html_report_creates_gallery_with_escaped_metadata(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            image_path = Path(temp_dir) / "final_image.jpg"
            image_path.write_bytes(b"image")
            report_path = Path(temp_dir) / "reports" / "index.html"

            result = write_html_report(
                [
                    {
                        "pack_id": "pack-1",
                        "prompt": "A test prompt",
                        "caption": "Caption <safe>",
                        "alt_text": "Alt text",
                        "hashtags": ["#test"],
                        "image_path": str(image_path),
                    }
                ],
                str(report_path),
            )

            document = report_path.read_text(encoding="utf-8")
            self.assertEqual(result, str(report_path))
            self.assertIn("Caption &lt;safe&gt;", document)
            self.assertNotIn("Caption <safe>", document)
            self.assertIn("pack-1", document)
            self.assertIn("Manifest unavailable", document)
            self.assertTrue(report_path.is_file())

if __name__ == "__main__":
    unittest.main()
