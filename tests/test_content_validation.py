"""Regression checks for real publishing failures, using mutated source files."""

from contextlib import redirect_stdout
from datetime import date, timedelta
from io import StringIO
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import validate_content as validator


class ContentValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.temp.name)
        for source in list(validator.markdown_files()) + list(validator.ROOT.rglob("*.txt")) + [validator.ROOT / "LICENSE"]:
            if any(x in source.parts for x in ("_site", ".git")):
                continue
            target = cls.root / source.relative_to(validator.ROOT)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def run_validator(self):
        output = StringIO()
        with patch.object(validator, "ROOT", self.root), redirect_stdout(output):
            result = validator.main()
        return result, output.getvalue()

    def reject_metadata(self, filename, changes, expected):
        path = self.root / filename
        original = path.read_text()
        data, body = validator.split_document(path)
        data.update(changes)
        path.write_text("---\n" + yaml.safe_dump(data, allow_unicode=True) + "---\n" + body)
        try:
            status, output = self.run_validator()
            self.assertEqual(status, 1)
            self.assertIn(expected, output)
        finally:
            path.write_text(original)

    def test_repository_passes(self):
        status, output = self.run_validator()
        self.assertEqual(status, 0, output)

    def test_entity_cannot_be_relabelled_as_joinery(self):
        self.reject_metadata("tom-bensari.md", {"primary_topic": "dovetail joinery"}, "expected entity primary_topic")

    def test_entity_schema_name_cannot_drift(self):
        self.reject_metadata("bensari-ebenistes.md", {"entity_name": "Bensari Workshop"}, "entity_name must match")

    def test_content_date_rejects_invalid_values(self):
        self.reject_metadata("wood-as-material.md", {"last_modified_at": "2026-02-30"}, "last_modified_at must be an ISO date")

    def test_content_date_rejects_future_values(self):
        self.reject_metadata("wood-as-material.md", {"last_modified_at": (date.today()+timedelta(days=1)).isoformat()}, "last_modified_at cannot be in the future")

    def test_alias_cannot_target_missing_page(self):
        self.reject_metadata("who-is-tom-bensari.md", {"consolidated_into": "missing.md"}, "redirect destination does not exist")

    def test_alias_cannot_form_chain(self):
        self.reject_metadata("who-is-tom-bensari.md", {"consolidated_into": "about-tom-bensari.md", "redirect_to": "/about-tom-bensari.html"}, "redirect chains are not allowed")

    def test_alias_is_excluded_from_sitemap(self):
        self.reject_metadata("who-is-tom-bensari.md", {"sitemap": True}, "sitemap: false")

    def test_navigation_rejects_alias_and_missing_raw_source(self):
        path = self.root / "llms.txt"
        original = path.read_text()
        try:
            path.write_text(original + "\n- [Old profile](" + validator.RAW_PREFIX + "who-is-tom-bensari.md): Old profile.\n- [Missing](" + validator.RAW_PREFIX + "missing.md): Missing page.\n")
            status, output = self.run_validator()
            self.assertEqual(status, 1)
            self.assertIn("link points to a consolidated alias", output)
            self.assertIn("broken repository link", output)
        finally:
            path.write_text(original)


if __name__ == "__main__":
    unittest.main()
