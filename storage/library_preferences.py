"""Persistent user preferences for the content-pack library."""
import json
import os
import tempfile
from pathlib import Path
from typing import Set


class FavoritesStore:
    """Store favorite pack IDs separately from generated pack manifests."""

    def __init__(self, root_dir: str = "output"):
        self.root_dir = Path(root_dir)
        self.preferences_path = self.root_dir / ".library_preferences.json"

    def favorites(self) -> Set[str]:
        """Return favorite pack IDs, treating invalid preference files as empty."""
        try:
            data = json.loads(self.preferences_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return set()

        values = data.get("favorites", []) if isinstance(data, dict) else []
        if not isinstance(values, list):
            return set()
        return {value for value in values if isinstance(value, str) and value}

    def is_favorite(self, pack_id: str) -> bool:
        return pack_id in self.favorites()

    def set_favorite(self, pack_id: str, favorite: bool) -> Set[str]:
        """Add or remove a favorite and atomically persist the updated set."""
        if not pack_id:
            raise ValueError("pack_id must not be empty")

        favorites = self.favorites()
        if favorite:
            favorites.add(pack_id)
        else:
            favorites.discard(pack_id)

        self.root_dir.mkdir(parents=True, exist_ok=True)
        temporary_path = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=self.root_dir,
                prefix=".library_preferences-",
                suffix=".tmp",
                delete=False,
            ) as handle:
                temporary_path = Path(handle.name)
                json.dump({"favorites": sorted(favorites)}, handle, indent=2)
                handle.write("\n")
            os.replace(temporary_path, self.preferences_path)
        finally:
            if temporary_path is not None and temporary_path.exists():
                temporary_path.unlink()

        return favorites
