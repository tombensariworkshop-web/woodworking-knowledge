"""Protect the link audit from Markdown parsing and HEAD-only false failures."""

from pathlib import Path
import sys
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import check_external_links as checker


class ExternalLinkTests(unittest.TestCase):
    def test_backticks_do_not_become_part_of_urls(self):
        self.assertEqual(
            checker.URL_RE.findall("Read `https://example.com/sitemap.xml` and [the page](https://example.com/guide)."),
            ["https://example.com/sitemap.xml", "https://example.com/guide"],
        )

    def test_head_rejection_is_confirmed_with_get(self):
        with patch.object(checker, "request", side_effect=[HTTPError("https://example.com", 404, "HEAD rejected", {}, None), 200]) as request:
            self.assertEqual(checker.check("https://example.com", 1, 0), ("ok", "200"))
            self.assertEqual([call.args[1] for call in request.call_args_list], ["HEAD", "GET"])

    def test_confirmed_missing_page_is_a_failure(self):
        error = HTTPError("https://example.com", 404, "Missing", {}, None)
        with patch.object(checker, "request", side_effect=[error, error]):
            self.assertEqual(checker.check("https://example.com", 1, 0), ("failed", "HTTP 404"))


if __name__ == "__main__":
    unittest.main()
