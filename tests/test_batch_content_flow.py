import json
import tempfile
import unittest
from pathlib import Path

from flows.batch_content_flow import run_batch_content_packs


class BatchContentFlowTests(unittest.TestCase):
    def test_run_batch_content_packs_creates_manifest_and_pack_dirs(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            source_image = Path(temp_dir) / "source.jpg"
            source_image.write_bytes(b"fake image")

            def fake_pack_runner(prompt, output_dir, watermark, **kwargs):
                pack_dir = Path(output_dir)
                pack_dir.mkdir(parents=True, exist_ok=True)
                image_path = pack_dir / "final_image.jpg"
                image_path.write_bytes(b"fake image")
                return {
                    "prompt": prompt,
                    "final_image_path": str(image_path),
                    "caption": f"Caption for {prompt}",
                    "hashtags": ["#demo"],
                    "alt_text": f"Alt text for {prompt}",
                    "manifest_path": str(pack_dir / "manifest.json"),
                    "pack_id": "pack-1",
                }