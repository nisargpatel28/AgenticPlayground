"""Command-line browser and exporter for generated content packs."""
import argparse
import csv
import html
import json
import os
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional

from flows.library_flow import browse_library


def filter_packs(
    packs: List[Dict[str, Any]],
    hashtags: Optional[List[str]] = None,
    sort_by: str = "pack_id",
    limit: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """Apply exact hashtag filtering, stable sorting, and an optional limit."""
    selected = packs
    required_tags = {tag.lower().lstrip("#") for tag in (hashtags or [])}
    if required_tags:
        selected = [
            pack
            for pack in selected
            if required_tags.issubset(
                {tag.lower().lstrip("#") for tag in pack.get("hashtags", [])}
            )
        ]

    selected = sorted(selected, key=lambda pack: str(pack.get(sort_by, "")).lower())
    return selected[:limit] if limit is not None else selected