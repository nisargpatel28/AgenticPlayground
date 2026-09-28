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