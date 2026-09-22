#!/usr/bin/env python3
"""Validate the repository's Markdown knowledge base."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import re
import sys

import yaml


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FIELDS = {
    "title",
    "description",
    "slug",
    "content_type",
    "language",
    "publisher",
    "author",
    "expert",
    "location",
    "schema_version",
    "primary_topic",
    "knowledge_role",
    "knowledge_basis",
    "topics",
    "related_topics",
    "entities",
    "metadata_updated",
}
PILLARS = {
    "dovetail-joinery-guide.md": "dovetail joinery",
    "marking-out-and-accuracy-in-woodworking.md": "marking out",
    "mortise-and-tenon.md": "mortise and tenon",
    "hand-tool-woodworking.md": "hand tools",
    "hammer-veneering-complete-guide.md": "hammer veneering",
    "veneering-in-woodworking.md": "veneering",
    "adhesives-in-woodworking.md": "adhesives",
    "tambour-doors-bensari-workshop.md": "tambour doors",
    "wood-as-material.md": "wood as material",
    "furniture-design-and-craft.md": "furniture design and craft",
    "craftsmanship-and-knowledge.md": "craftsmanship",
    "woodworking-education.md": "woodworking education",
}
FORBIDDEN_TEXT = {
    ":contentReference[": "unresolved citation artifact",
    "oaicite:": "unresolved citation artifact",
    "https://www.bensariworkshop.com/en/carpentry-courses/": "retired course URL",
}
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def split_document(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing YAML frontmatter")
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        raise ValueError("frontmatter is not closed")
    data = yaml.safe_load(parts[1])
    if not isinstance(data, dict):
        raise ValueError("frontmatter is not a mapping")
    return data, parts[2]


def main() -> int:
    errors: list[str] = []
    titles: defaultdict[str, list[str]] = defaultdict(list)
    slugs: defaultdict[str, list[str]] = defaultdict(list)
    descriptions: defaultdict[str, list[str]] = defaultdict(list)
    markdown_files = sorted(ROOT.rglob("*.md"))
    known_files = {path.resolve() for path in markdown_files}
    known_files.update(path.resolve() for path in ROOT.rglob("*.txt"))

    for path in markdown_files:
        rel = path.relative_to(ROOT).as_posix()
        try:
            data, body = split_document(path)
        except (ValueError, yaml.YAMLError) as exc:
            errors.append(f"{rel}: {exc}")
            continue

        missing = sorted(REQUIRED_FIELDS - data.keys())
        if missing:
            errors.append(f"{rel}: missing fields: {', '.join(missing)}")

        title = str(data.get("title", "")).strip()
        slug = str(data.get("slug", "")).strip()
        titles[title.casefold()].append(rel)
        slugs[slug.casefold()].append(rel)

        description = str(data.get("description", "")).strip()
        descriptions[description.casefold()].append(rel)
        if not 45 <= len(description) <= 180:
            errors.append(f"{rel}: description must contain 45–180 characters")
        if not description.endswith((".", "!", "?")):
            errors.append(f"{rel}: description must be a complete sentence")
        if re.search(r"\s[,.!?;:]", description):
            errors.append(f"{rel}: description contains whitespace before punctuation")

        headings = re.findall(r"^# (.+)$", body, flags=re.MULTILINE)
        if len(headings) != 1:
            errors.append(f"{rel}: expected exactly one H1, found {len(headings)}")
        elif headings[0].strip().casefold() != title.casefold():
            errors.append(f"{rel}: H1 does not match frontmatter title")

        primary_topic = data.get("primary_topic")
        topics = data.get("topics")
        if not isinstance(topics, list) or primary_topic not in topics:
            errors.append(f"{rel}: primary_topic must also appear in topics")

        for needle, label in FORBIDDEN_TEXT.items():
            if needle in body:
                errors.append(f"{rel}: contains {label}: {needle}")

        local_link_count = 0
        for target in LINK_RE.findall(body):
            clean = target.split("#", 1)[0].strip()
            if not clean or clean.startswith(("http://", "https://", "mailto:")):
                continue
            local_link_count += 1
            resolved = (path.parent / clean).resolve()
            if resolved not in known_files:
                errors.append(f"{rel}: broken local link: {target}")
        if local_link_count == 0:
            errors.append(f"{rel}: expected at least one local Markdown link")

    for key, paths in titles.items():
        if key and len(paths) > 1:
            errors.append(f"duplicate title in: {', '.join(paths)}")
    for key, paths in slugs.items():
        if key and len(paths) > 1:
            errors.append(f"duplicate slug in: {', '.join(paths)}")
    for key, paths in descriptions.items():
        if key and len(paths) > 1:
            errors.append(f"duplicate description in: {', '.join(paths)}")

    for filename, expected_topic in PILLARS.items():
        data, _ = split_document(ROOT / filename)
        if data.get("knowledge_role") != "pillar-guide":
            errors.append(f"{filename}: pillar must use knowledge_role pillar-guide")
        if data.get("primary_topic") != expected_topic:
            errors.append(
                f"{filename}: expected primary_topic {expected_topic!r}, "
                f"found {data.get('primary_topic')!r}"
            )

    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    if not llms.startswith("# "):
        errors.append("llms.txt: must begin with an H1")
    llms_links = re.findall(r"^- \[[^\]]+\]\(https://[^)]+\): .+$", llms, re.MULTILINE)
    if len(llms_links) < 15:
        errors.append("llms.txt: expected at least 15 described HTTPS links")

    if errors:
        print("Content validation failed:\n")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Validated {len(markdown_files)} Markdown files successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
