import json
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

from flows.library_flow import browse_library


class LibraryFlowTests(unittest.TestCase):
    def test_search_and_export_matching_packs(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            for pack_id, prompt in [("one", "A red mountain"), ("two", "A blue ocean")]:
                pack_dir = Path(temp_dir) / pack_id
                pack_dir.mkdir()
                image_path = pack_dir / "final_image.jpg"
                image_path.write_bytes(b"image")
                (pack_dir / "manifest.json").write_text(
                    json.dumps(
                        {
                            "pack_id": pack_id,
                            "prompt": prompt,
                            "caption": f"Caption for {prompt}",
                            "alt_text": prompt,
                            "hashtags": ["#nature"],
                            "final_image_path": str(image_path),
                        }
                    ),
                    encoding="utf-8",
                )

            archive_path = Path(temp_dir) / "export.zip"
            result = browse_library(temp_dir, query="red", export_path=str(archive_path))

            self.assertEqual(result["total"], 1)
            self.assertEqual(result["packs"][0]["pack_id"], "one")
            with ZipFile(archive_path) as archive:
                self.assertEqual(
                    sorted(archive.namelist()),
                    ["one/final_image.jpg", "one/manifest.json"],
                )

    def test_empty_library_is_searchable(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            self.assertEqual(browse_library(temp_dir)["total"], 0)


if __name__ == "__main__":
    unittest.main()
