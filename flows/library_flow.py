"""High-level workflow for browsing and exporting content packs."""
from typing import Any, Dict, Iterable, Optional

from storage.library_preferences import FavoritesStore
from storage.pack_catalog import PackCatalog
from storage.pack_exporter import export_packs


def browse_library(
    output_dir: str = "output",
    query: str = "",
    pack_ids: Optional[Iterable[str]] = None,
    export_path: Optional[str] = None,
    favorites_only: bool = False,
) -> Dict[str, Any]:
    """Search the local pack library and optionally export selected results."""
    catalog = PackCatalog(output_dir)
    records = catalog.search(query)
    if pack_ids is not None:
        selected_ids = set(pack_ids)
        records = [record for record in records if record.pack_id in selected_ids]

    favorites = FavoritesStore(output_dir).favorites()
    if favorites_only:
        records = [record for record in records if record.pack_id in favorites]

    result: Dict[str, Any] = {
        "total": len(records),
        "packs": [
            {**record.to_dict(), "is_favorite": record.pack_id in favorites}
            for record in records
        ],
    }
    if export_path:
        result["export_path"] = export_packs(records, export_path)
    return result


def delete_packs(output_dir: str, pack_ids: Iterable[str]) -> Dict[str, Any]:
    """Delete explicitly selected packs from the configured library."""
    selected_ids = list(dict.fromkeys(pack_ids))
    if not selected_ids:
        raise ValueError("select at least one pack to delete")
    result = PackCatalog(output_dir).delete_many(selected_ids)
    preferences = FavoritesStore(output_dir)
    for pack_id in result["deleted"]:
        preferences.set_favorite(pack_id, False)
    return result


def set_pack_favorite(output_dir: str, pack_id: str, favorite: bool) -> Dict[str, Any]:
    """Mark an existing pack as favorite or remove it from favorites."""
    if PackCatalog(output_dir).get(pack_id) is None:
        raise LookupError(f"Pack not found: {pack_id}")
    favorites = FavoritesStore(output_dir).set_favorite(pack_id, favorite)
    return {"pack_id": pack_id, "is_favorite": pack_id in favorites}
