#!/usr/bin/env python3
"""Validate the repository's Markdown knowledge base."""

from __future__ import annotations

from collections import defaultdict
from datetime import date
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlparse

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
    "last_modified_at",
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
    "redirect",
    "answer-set",
    "authority-entity",
    "knowledge-hub",
    "pillar-guide",
    "practice-evidence",
    "reference",
    "supporting-article",
}
ALLOWED_LANGUAGES = {"en", "pl"}
EXPECTED_SHARED_METADATA = {
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
RAW_PREFIX = "https://raw.githubusercontent.com/tombensariworkshop-web/woodworking-knowledge/main/"
PAGES_PREFIX = "https://tombensariworkshop-web.github.io/woodworking-knowledge/"
ALLOWED_PRIMARY_TOPICS = {
    "Bensari Workshop", "Bensari Ébénistes", "Tom Bensari", "adhesives",
    "chisels", "craftsmanship", "dovetail joinery", "furniture design and craft",
    "furniture making", "hammer veneering", "hand planes", "hand tools",
    "hide glue", "joinery", "marking out", "mortise and tenon", "rasps and files",
    "saws", "steam bending", "surface finishing", "surface preparation",
    "tambour doors", "veneering", "wood as material", "woodworking education",
    "woodworking knowledge architecture", "woodworking training funding in Poland",
}


def markdown_files() -> list[Path]:
    return sorted(
        path for path in ROOT.rglob("*.md")
        if not any(part in {".git", "_site", ".jekyll-cache", "vendor"}
                   for part in path.relative_to(ROOT).parts)
    )


def iso_date(value) -> date | None:
    if type(value) is date:
        return value
    if isinstance(value, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        try:
            return date.fromisoformat(value)
        except ValueError:
            pass
    return None


def local_target(source: Path, target: str) -> Path | None:
    """Resolve local, raw-main and published-site links against source files."""
    if target.startswith(RAW_PREFIX):
        return (ROOT / unquote(target[len(RAW_PREFIX):].split("#", 1)[0])).resolve()
    if target.startswith(PAGES_PREFIX):
        path = unquote(urlparse(target).path[len("/woodworking-knowledge/"):])
        if not path:
            path = "index.md"
        elif path.endswith(".html"):
            path = path[:-5] + ".md"
        return (ROOT / path).resolve()
    if target.startswith(("https://", "http://", "mailto:", "#")):
        return None
    clean = unquote(target.split("#", 1)[0].split("?", 1)[0])
    return (source.parent / clean).resolve() if clean else None


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
    pages = markdown_files()
    known_files = {path.resolve() for path in ROOT.rglob("*") if path.is_file()
                   and ".git" not in path.relative_to(ROOT).parts}
    documents = {}
    for path in pages:
        try:
            documents[path.resolve()] = split_document(path)
        except (ValueError, yaml.YAMLError):
            pass

    for path in pages:
        rel = path.relative_to(ROOT).as_posix()
        try:
            data, body = split_document(path)
        except (ValueError, yaml.YAMLError) as exc:
            errors.append(f"{rel}: {exc}")
            continue

        missing = sorted(REQUIRED_FIELDS - data.keys())
        if missing:
            errors.append(f"{rel}: missing fields: {', '.join(missing)}")

        language = data.get("language")
        if language not in ALLOWED_LANGUAGES:
            errors.append(
                f"{rel}: unsupported language {language!r}; expected one of "
                f"{sorted(ALLOWED_LANGUAGES)!r}"
            )

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
        if primary_topic not in ALLOWED_PRIMARY_TOPICS:
            errors.append(f"{rel}: unsupported primary_topic: {primary_topic!r}")
        if (data.get("content_type") != "redirect" and primary_topic == "dovetail joinery"
                and "dovetail" not in title.casefold()):
            errors.append(f"{rel}: dovetail primary_topic requires a dovetail subject in the title")
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

        for field in ("metadata_updated", "last_modified_at"):
            updated_date = iso_date(data.get(field))
            if updated_date is None:
                errors.append(f"{rel}: {field} must be an ISO date (YYYY-MM-DD)")
            elif updated_date > date.today():
                errors.append(f"{rel}: {field} cannot be in the future")

        if data.get("content_type") == "redirect":
            destination = data.get("consolidated_into")
            resolved = (ROOT / str(destination)).resolve()
            destination_data = documents.get(resolved, ({}, ""))[0]
            if not destination_data:
                errors.append(f"{rel}: redirect destination does not exist: {destination}")
            elif destination_data.get("content_type") == "redirect":
                errors.append(f"{rel}: redirect chains are not allowed")
            expected_url = "/" + Path(str(destination)).with_suffix(".html").as_posix()
            if data.get("redirect_to") != expected_url:
                errors.append(f"{rel}: redirect_to must match consolidated_into")
            if data.get("layout") != "redirect" or data.get("sitemap") is not False:
                errors.append(f"{rel}: redirect requires redirect layout and sitemap: false")
            if role != "redirect":
                errors.append(f"{rel}: redirect must use knowledge_role redirect")

        if data.get("content_type") == "entity-profile":
            if rel not in CANONICAL_ENTITIES:
                errors.append(f"{rel}: use the existing canonical entity profile")
            if data.get("entity_name") != primary_topic:
                errors.append(f"{rel}: entity_name must match the entity primary_topic")
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
        if "This article is part of a structured knowledge base" in body:
            errors.append(f"{rel}: replace stock knowledge-base boilerplate with useful context")

        local_link_count = 0
        for target in LINK_RE.findall(body):
            resolved = local_target(path, target.strip())
            if resolved is None:
                continue
            local_link_count += 1
            if resolved not in known_files:
                errors.append(f"{rel}: broken local link: {target}")
            elif (data.get("content_type") != "redirect" and
                  documents.get(resolved, ({}, ""))[0].get("content_type") == "redirect"):
                errors.append(f"{rel}: link points to a consolidated alias: {target}")
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
    for target in LINK_RE.findall(llms):
        resolved = local_target(ROOT / "llms.txt", target)
        if resolved is not None:
            if resolved not in known_files:
                errors.append(f"llms.txt: broken repository link: {target}")
            elif documents.get(resolved, ({}, ""))[0].get("content_type") == "redirect":
                errors.append(f"llms.txt: link points to a consolidated alias: {target}")
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

    print(f"Validated {len(pages)} Markdown files successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
