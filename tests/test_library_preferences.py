import json
import tempfile
import unittest
from pathlib import Path

from storage.library_preferences import FavoritesStore


class FavoritesStoreTests(unittest.TestCase):
    def test_favorites_persist_between_store_instances(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            store = FavoritesStore(temp_dir)
            self.assertFalse(store.is_favorite("pack-1"))

            store.set_favorite("pack-1", True)

            self.assertTrue(FavoritesStore(temp_dir).is_favorite("pack-1"))
            data = json.loads((Path(temp_dir) / ".library_preferences.json").read_text(encoding="utf-8"))
            self.assertEqual(data["favorites"], ["pack-1"])

    def test_unfavorite_removes_pack_from_preferences(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            store = FavoritesStore(temp_dir)
            store.set_favorite("pack-1", True)
            store.set_favorite("pack-1", False)

            self.assertFalse(store.is_favorite("pack-1"))
            self.assertEqual(store.favorites(), set())


if __name__ == "__main__":
    unittest.main()
