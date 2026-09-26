"""Data contract for generated content packs."""
from dataclasses import asdict, dataclass
from typing import Any, Dict, List


@dataclass
class ContentPack:
    """All user-facing assets produced for one creative prompt."""

    pack_id: str
    prompt: str
    blurb: str
    image_prompt: str
    final_image_path: str
    alt_text: str
    caption: str
    hashtags: List[str]

    def to_dict(self) -> Dict[str, Any]:
        """Return a JSON-serializable representation of the pack."""
        return asdict(self)
