"""High-level workflow for browsing and exporting content packs."""
from typing import Any, Dict, Iterable, Optional

from storage.pack_catalog import PackCatalog
from storage.pack_exporter import export_packs


def browse_library(
    output_dir: str = "output",
    query: str = "",
    pack_ids: Optional[Iterable[str]] = None,
    export_path: Optional[str] = None,
) -> Dict[str, Any]:
    """Search the local pack library and optionally export selected results."""
    catalog = PackCatalog(output_dir)
    records = catalog.search(query)
    if pack_ids is not None:
        selected_ids = set(pack_ids)
        records = [record for record in records if record.pack_id in selected_ids]

    result: Dict[str, Any] = {
        "total": len(records),
        "packs": [record.to_dict() for record in records],
    }
    if export_path:
        result["export_path"] = export_packs(records, export_path)
    return result
