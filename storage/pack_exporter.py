"""Export selected content packs as portable ZIP archives."""
from pathlib import Path
from typing import Iterable
from zipfile import ZIP_DEFLATED, ZipFile

from models.pack_record import PackRecord


def export_packs(records: Iterable[PackRecord], zip_path: str) -> str:
    """Write manifests and available images into a portable ZIP archive."""
    selected = list(records)
    if not selected:
        raise ValueError("at least one pack is required for export")

    destination = Path(zip_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(destination, "w", compression=ZIP_DEFLATED) as archive:
        for record in selected:
            folder = record.pack_id or "pack"
            manifest_path = Path(record.manifest_path)
            archive.write(manifest_path, f"{folder}/manifest.json")
            image_path = Path(record.image_path)
            if image_path.is_file():
                archive.write(image_path, f"{folder}/{image_path.name}")

    return str(destination)
