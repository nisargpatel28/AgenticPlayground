"""Normalized metadata for a generated content pack."""
from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass(frozen=True)
class PackRecord:
    pack_id: str
    prompt: str
    caption: str
    alt_text: str
    hashtags: List[str]
    image_path: str
    manifest_path: str

    @classmethod
    def from_manifest(cls, manifest: Dict[str, Any], manifest_path: str) -> "PackRecord":
        return cls(
            pack_id=str(manifest.get("pack_id", "")),
            prompt=str(manifest.get("prompt", "")),
            caption=str(manifest.get("caption", "")),
            alt_text=str(manifest.get("alt_text", "")),
            hashtags=[str(tag) for tag in manifest.get("hashtags", [])],
            image_path=str(manifest.get("final_image_path", "")),
            manifest_path=manifest_path,
        )