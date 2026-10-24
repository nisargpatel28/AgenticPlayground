"""Index and search generated content-pack manifests."""
import json
import shutil
from pathlib import Path
from typing import Iterable, List, Optional

from models.pack_record import PackRecord


class PackCatalog:
    """Discover, search, and retrieve packs stored below a directory."""

    def __init__(self, root_dir: str = "output"):
        self.root_dir = Path(root_dir)

    def scan(self) -> List[PackRecord]:
        records: List[PackRecord] = []
        if not self.root_dir.exists():
            return records

        for manifest_path in sorted(self.root_dir.glob("**/manifest.json")):
            try:
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                record = PackRecord.from_manifest(manifest, str(manifest_path))
            except (OSError, json.JSONDecodeError, TypeError):
                continue
            if record.pack_id:
                records.append(record)
        return records

    def search(self, query: str = "") -> List[PackRecord]:
        records = self.scan()
        normalized_query = query.strip().lower()
        if not normalized_query:
            return records

        def matches(record: PackRecord) -> bool:
            searchable = " ".join(
                [record.pack_id, record.prompt, record.caption, record.alt_text, *record.hashtags]
            ).lower()
            return normalized_query in searchable

        return [record for record in records if matches(record)]

    def get(self, pack_id: str) -> Optional[PackRecord]:
        return next((record for record in self.scan() if record.pack_id == pack_id), None)

    def get_many(self, pack_ids: Iterable[str]) -> List[PackRecord]:
        requested = set(pack_ids)
        return [record for record in self.scan() if record.pack_id in requested]

    def delete_many(self, pack_ids: Iterable[str]) -> dict:
        """Delete selected pack directories after checking root containment."""
        requested = set(pack_ids)
        records = self.get_many(requested)
        root = self.root_dir.resolve()
        directories = []

        for record in records:
            manifest = Path(record.manifest_path).resolve()
            if manifest.name != "manifest.json" or not manifest.is_file():
                raise ValueError(f"Invalid manifest for pack {record.pack_id}")
            pack_dir = manifest.parent
            try:
                pack_dir.relative_to(root)
            except ValueError as exc:
                raise ValueError(
                    f"Pack {record.pack_id} is outside the library root"
                ) from exc
            if pack_dir == root:
                raise ValueError("Refusing to delete the library root")
            directories.append((record.pack_id, pack_dir))

        deleted = []
        for pack_id, pack_dir in directories:
            shutil.rmtree(pack_dir)
            if pack_id not in deleted:
                deleted.append(pack_id)

        found = {record.pack_id for record in records}
        return {
            "deleted": deleted,
            "not_found": sorted(requested - found),
        }
