import json
import os
import tempfile
import unittest
from pathlib import Path

from flows.content_pack_flow import run_content_pack


class ContentPackFlowTests(unittest.TestCase):
    def test_run_content_pack_saves_image_and_manifest(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            source_image = Path(temp_dir) / "source.jpg"
            source_image.write_bytes(b"fake image")

            def fake_image_flow(context):
                return {
                    "content": "A bright test scene.",
                    "image_prompt": "A bright test scene",
                    "final_image_path": str(source_image),
                    "alt_text": "A bright test scene.",
                }

            result = run_content_pack(
                "A bright test scene",
                output_dir=temp_dir,
                image_flow=fake_image_flow,
                text_generator=lambda _: '{"caption": "Test caption", "hashtags": ["#test"]}',
            )

            manifest_path = Path(result["manifest_path"])
            image_path = Path(result["final_image_path"])
            self.assertTrue(manifest_path.is_file())
            self.assertTrue(image_path.is_file())
            self.assertEqual(result["caption"], "Test caption")
            self.assertEqual(result["hashtags"], ["#test"])

            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(manifest["prompt"], "A bright test scene")
            self.assertEqual(manifest["final_image_path"], str(image_path))

    def test_empty_prompt_is_rejected(self):
        with self.assertRaises(ValueError):
            run_content_pack("   ")


if __name__ == "__main__":
    unittest.main()
