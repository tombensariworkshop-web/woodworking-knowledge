"""A routine catalog check must not invent fresh modification dates."""

from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import generate_catalog as catalog


class CatalogDateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.output = self.root / "catalog.md"
        self.source = self.root / "example.md"
        self.source.write_text("---\ntitle: Example\ndescription: A source description.\nprimary_topic: hand tools\n---\n# Example\n")
        self.root_patch = patch.object(catalog, "ROOT", self.root)
        self.output_patch = patch.object(catalog, "OUTPUT", self.output)
        self.root_patch.start()
        self.output_patch.start()
        self.output.write_text(catalog.render("2026-01-01", "2026-01-01"))

    def tearDown(self):
        self.output_patch.stop()
        self.root_patch.stop()
        self.temp.cleanup()

    def test_no_change_preserves_dates(self):
        self.assertFalse(catalog.write_catalog("2026-11-25"))
        self.assertEqual(catalog.load_frontmatter(self.output)["last_modified_at"], "2026-01-01")

    def test_changed_article_listing_updates_content_date(self):
        self.source.write_text(self.source.read_text().replace("A source description.", "A revised source description."))
        self.assertTrue(catalog.write_catalog("2026-11-25"))
        self.assertEqual(catalog.load_frontmatter(self.output)["last_modified_at"], "2026-11-25")

    def test_metadata_correction_preserves_content_date(self):
        self.output.write_text(self.output.read_text().replace('slug: "catalog"', 'slug: "old-catalog"'))
        self.assertTrue(catalog.write_catalog("2026-11-25"))
        data = catalog.load_frontmatter(self.output)
        self.assertEqual(data["metadata_updated"], "2026-11-25")
        self.assertEqual(data["last_modified_at"], "2026-01-01")


if __name__ == "__main__":
    unittest.main()
