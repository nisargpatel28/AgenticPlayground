"""Filesystem persistence for generated content packs."""
import json
import os
import shutil
from dataclasses import replace
from typing import Any, Dict

from models.content_pack import ContentPack


class ArtifactStore:
    """Save packs as portable directories containing an image and manifest."""

    def save_pack(self, pack: ContentPack, output_dir: str) -> Dict[str, Any]:
        pack_dir = os.path.join(output_dir, pack.pack_id)
        os.makedirs(pack_dir, exist_ok=True)

        image_path = os.path.join(pack_dir, "final_image.jpg")
        if os.path.abspath(pack.final_image_path) != os.path.abspath(image_path):
            shutil.copy2(pack.final_image_path, image_path)

        stored_pack = replace(pack, final_image_path=image_path)
        manifest_path = os.path.join(pack_dir, "manifest.json")
        with open(manifest_path, "w", encoding="utf-8") as manifest_file:
            json.dump(stored_pack.to_dict(), manifest_file, indent=2)

        return {
            "pack": stored_pack,
            "pack_dir": pack_dir,
            "manifest_path": manifest_path,
        }
