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