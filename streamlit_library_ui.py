from pathlib import Path

import streamlit as st

from flows.library_flow import browse_library, delete_packs, set_pack_favorite


st.set_page_config(page_title="Content Pack Library", page_icon="📚")
st.title("Content Pack Library")

root_dir = st.text_input("Library directory", value="output")
query = st.text_input("Search packs", placeholder="Try a topic, caption, or hashtag")
favorites_only = st.checkbox("Show favorites only")

result = browse_library(root_dir, query=query, favorites_only=favorites_only)
st.caption(f"{result['total']} matching pack(s)")

selected_ids = []
for pack in result["packs"]:
    with st.container(border=True):
        checked = st.checkbox(pack["prompt"], key=f"select_{pack['pack_id']}")
        if checked:
            selected_ids.append(pack["pack_id"])
        st.write(pack["caption"] or pack["alt_text"])
        st.write(" ".join(pack["hashtags"]))
        favorite_label = "Remove favorite" if pack["is_favorite"] else "Add favorite"
        if st.button(favorite_label, key=f"favorite_{pack['pack_id']}"):
            try:
                set_pack_favorite(root_dir, pack["pack_id"], not pack["is_favorite"])
                st.rerun()
            except Exception as exc:  # pragma: no cover - UI-level safety
                st.error(f"Could not update favorite: {exc}")
        image_path = Path(pack["image_path"])
        if image_path.is_file():
            st.image(str(image_path), width=240)

export_path = st.text_input("ZIP export path", value="output/content-packs.zip")
if st.button("Export selected packs"):
    if not selected_ids:
        st.warning("Select at least one pack first.")
    else:
        try:
            exported = browse_library(
                root_dir,
                query=query,
                pack_ids=selected_ids,
                export_path=export_path,
            )
            st.success(f"Exported {exported['total']} pack(s) to {exported['export_path']}")
        except Exception as exc:  # pragma: no cover - UI-level safety
            st.error(f"Export failed: {exc}")

st.divider()
confirm_delete = st.checkbox("I understand selected pack files will be permanently deleted")
if st.button("Delete selected packs", disabled=not confirm_delete):
    if not selected_ids:
        st.warning("Select at least one pack first.")
    else:
        try:
            result = delete_packs(root_dir, selected_ids)
            st.success(f"Deleted {len(result['deleted'])} pack(s).")
            if result["not_found"]:
                st.info("Some selected packs were already missing: " + ", ".join(result["not_found"]))
            st.rerun()
        except Exception as exc:  # pragma: no cover - UI-level safety
            st.error(f"Deletion failed: {exc}")
