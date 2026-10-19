#!/usr/bin/env python3
"""Validate the repository's Markdown knowledge base."""

from __future__ import annotations

from collections import defaultdict
from datetime import date
from pathlib import Path
import re
import sys
from urllib.parse import urlparse

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
CANONICAL_ENTITIES = {
    "tom-bensari.md": ("Tom Bensari", "Person"),
    "bensari-workshop.md": ("Bensari Workshop", "Organization"),
    "bensari-ebenistes.md": ("Bensari Ébénistes", "Organization"),
}
ALLOWED_KNOWLEDGE_ROLES = {
    "answer-set",
    "authority-entity",
    "knowledge-hub",
    "pillar-guide",
    "practice-evidence",
    "reference",
    "supporting-article",
}
EXPECTED_SHARED_METADATA = {
    "language": "en",
    "publisher": "Bensari Workshop",
    "author": "Tom Bensari",
    "expert": "Tom Bensari",
    "location": "Wrocław, Poland",
    "schema_version": "1.1",
}
WEAK_DESCRIPTION_PREFIXES = (
    "an overview of ",
    "learn about ",
    "explore ",
    "this article ",
    "this page ",
)
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

        for field, expected in EXPECTED_SHARED_METADATA.items():
            if data.get(field) != expected:
                errors.append(
                    f"{rel}: expected {field} {expected!r}, found {data.get(field)!r}"
                )

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
        if description.casefold().startswith(WEAK_DESCRIPTION_PREFIXES):
            errors.append(f"{rel}: description must state the subject directly")

        headings = re.findall(r"^# (.+)$", body, flags=re.MULTILINE)
        if len(headings) != 1:
            errors.append(f"{rel}: expected exactly one H1, found {len(headings)}")
        elif headings[0].strip().casefold() != title.casefold():
            errors.append(f"{rel}: H1 does not match frontmatter title")

        primary_topic = data.get("primary_topic")
        topics = data.get("topics")
        if not isinstance(topics, list) or primary_topic not in topics:
            errors.append(f"{rel}: primary_topic must also appear in topics")

        related_topics = data.get("related_topics")
        if not isinstance(related_topics, list) or not related_topics:
            errors.append(f"{rel}: related_topics must be a non-empty list")

        entities = data.get("entities")
        if (
            not isinstance(entities, list)
            or not entities
            or any(not isinstance(entity, str) or not entity.strip() for entity in entities)
        ):
            errors.append(f"{rel}: entities must be a non-empty list of names")

        role = data.get("knowledge_role")
        if role not in ALLOWED_KNOWLEDGE_ROLES:
            errors.append(f"{rel}: unsupported knowledge_role: {role!r}")

        updated = data.get("metadata_updated")
        if isinstance(updated, date):
            updated_date = updated
        elif isinstance(updated, str):
            try:
                updated_date = date.fromisoformat(updated)
            except ValueError:
                updated_date = None
        else:
            updated_date = None
        if updated_date is None:
            errors.append(f"{rel}: metadata_updated must be an ISO date (YYYY-MM-DD)")
        elif updated_date > date.today():
            errors.append(f"{rel}: metadata_updated cannot be in the future")

        if data.get("content_type") == "entity-profile":
            entity_type = data.get("entity_type")
            if entity_type not in {"Person", "Organization"}:
                errors.append(f"{rel}: entity profile requires Person or Organization entity_type")
            official_url = str(data.get("official_url", ""))
            if urlparse(official_url).scheme != "https":
                errors.append(f"{rel}: entity profile requires an HTTPS official_url")
            same_as = data.get("same_as")
            if (
                not isinstance(same_as, list)
                or not same_as
                or any(urlparse(str(url)).scheme != "https" for url in same_as)
            ):
                errors.append(f"{rel}: entity profile requires a non-empty HTTPS same_as list")
            if role != "authority-entity":
                errors.append(f"{rel}: entity profile must use knowledge_role authority-entity")

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
        path = ROOT / filename
        if not path.exists():
            errors.append(f"{filename}: required pillar is missing")
            continue
        data, _ = split_document(path)
        if data.get("knowledge_role") != "pillar-guide":
            errors.append(f"{filename}: pillar must use knowledge_role pillar-guide")
        if data.get("primary_topic") != expected_topic:
            errors.append(
                f"{filename}: expected primary_topic {expected_topic!r}, "
                f"found {data.get('primary_topic')!r}"
            )

    for filename, (expected_topic, expected_type) in CANONICAL_ENTITIES.items():
        path = ROOT / filename
        if not path.exists():
            errors.append(f"{filename}: required canonical entity is missing")
            continue
        data, _ = split_document(path)
        if data.get("primary_topic") != expected_topic:
            errors.append(
                f"{filename}: expected entity primary_topic {expected_topic!r}, "
                f"found {data.get('primary_topic')!r}"
            )
        if data.get("entity_type") != expected_type:
            errors.append(
                f"{filename}: expected entity_type {expected_type!r}, "
                f"found {data.get('entity_type')!r}"
            )
        if expected_topic not in data.get("entities", []):
            errors.append(f"{filename}: canonical entity must name itself in entities")

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
