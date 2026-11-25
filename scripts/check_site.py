#!/usr/bin/env python3
"""Check the actual Jekyll output: links, structured data, aliases and sitemap."""

from __future__ import annotations

from html.parser import HTMLParser
import json
from pathlib import Path
import sys
from urllib.parse import unquote, urljoin, urlparse
import xml.etree.ElementTree as ET

import yaml

from validate_content import ROOT, markdown_files, split_document


class Page(HTMLParser):
    def __init__(self, text: str):
        super().__init__()
        self.links = []
        self.canonicals = []
        self.refreshes = []
        self.schemas = []
        self.schema_parts = None
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a" and "href" in attrs:
            self.links.append(attrs["href"])
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonicals.append(attrs.get("href"))
        if tag == "meta" and attrs.get("http-equiv", "").lower() == "refresh":
            self.refreshes.append(attrs.get("content", ""))
        if tag == "script" and attrs.get("type") == "application/ld+json":
            self.schema_parts = []

    def handle_data(self, data):
        if self.schema_parts is not None:
            self.schema_parts.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self.schema_parts is not None:
            self.schemas.append(json.loads("".join(self.schema_parts)))
            self.schema_parts = None


def check(site_dir: Path) -> list[str]:
    errors = []
    config = yaml.safe_load((ROOT / "_config.yml").read_text())
    site_url = config["url"]
    baseurl = config["baseurl"].rstrip("/")
    host = urlparse(site_url).netloc
    sitemap = site_dir / "sitemap.xml"
    if not sitemap.exists():
        return ["sitemap.xml was not generated"]
    sitemap_urls = {node.text for node in ET.parse(sitemap).iter()
                    if node.tag.endswith("}loc")}
    excluded = set(config.get("exclude", []))
    for source in markdown_files():
        rel = source.relative_to(ROOT)
        if rel.as_posix() in excluded or rel.parts[0] in excluded:
            continue
        data, _ = split_document(source)
        candidates = [site_dir / rel.with_suffix(".html")]
        if rel.name == "README.md":
            candidates.append(site_dir / rel.parent / "index.html")
        output = next((p for p in candidates if p.exists()), None)
        if output is None:
            errors.append(f"{rel}: published page was not generated")
            continue
        page_path = "/" + output.relative_to(site_dir).as_posix()
        url = site_url + baseurl + page_path
        try:
            page = Page(output.read_text())
        except (ValueError, json.JSONDecodeError) as exc:
            errors.append(f"{rel}: invalid rendered JSON-LD: {exc}")
            continue
        if data["content_type"] == "redirect":
            expected = site_url + baseurl + data["redirect_to"]
            if page.canonicals != [expected]:
                errors.append(f"{rel}: rendered alias has the wrong canonical URL")
            if page.refreshes != ["0; url=" + baseurl + data["redirect_to"]]:
                errors.append(f"{rel}: rendered alias has no immediate redirect")
            if url in sitemap_urls:
                errors.append(f"{rel}: consolidated alias was included in sitemap")
        elif data["content_type"] != "index":
            kind = "ProfilePage" if data["content_type"] == "entity-profile" else "Article"
            schemas = [s for s in page.schemas if s.get("@type") == kind]
            if len(schemas) != 1:
                errors.append(f"{rel}: expected one rendered {kind} schema")
            else:
                schema = schemas[0]
                if schema.get("dateModified") != str(data["last_modified_at"]):
                    errors.append(f"{rel}: dateModified does not match the content date")
                if schema.get("inLanguage") != data["language"]:
                    errors.append(f"{rel}: wrong schema language")
                if kind == "ProfilePage":
                    entity = schema.get("mainEntity", {})
                    if entity.get("name") != data["entity_name"]:
                        errors.append(f"{rel}: wrong entity name in rendered schema")
                    if entity.get("@type") != data["entity_type"]:
                        errors.append(f"{rel}: wrong entity type in rendered schema")
                elif schema.get("about", {}).get("name") != data["primary_topic"]:
                    errors.append(f"{rel}: wrong about subject in rendered schema")
        for target in page.links:
            parsed = urlparse(urljoin(url, target))
            if parsed.netloc != host or not parsed.path.startswith(baseurl + "/"):
                continue
            relative = unquote(parsed.path[len(baseurl) + 1:])
            candidate = site_dir / relative
            if candidate.is_dir():
                candidate = candidate / "index.html"
            if not candidate.is_file():
                errors.append(f"{rel}: broken rendered link: {target}")
    return sorted(set(errors))


if __name__ == "__main__":
    errors = check(Path(sys.argv[1] if len(sys.argv) > 1 else "_site"))
    for error in errors:
        print(error)
    if not errors:
        print("Rendered links, JSON-LD, redirects and sitemap passed.")
    sys.exit(bool(errors))
