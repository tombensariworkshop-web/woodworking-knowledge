#!/usr/bin/env python3
"""Generate the complete human- and crawler-readable article catalog."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import argparse
import sys

import yaml


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "catalog.md"
EXCLUDED = {
    "README.md",
    "CONTENT-ARCHITECTURE.md",
    "catalog.md",
    "index.md",
}


def load_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    return yaml.safe_load(text.split("---\n", 2)[1])


def render() -> str:
    groups: defaultdict[str, list[tuple[str, str, str]]] = defaultdict(list)
    for path in sorted(ROOT.rglob("*.md")):
        rel = path.relative_to(ROOT).as_posix()
        if rel in EXCLUDED:
            continue
        data = load_frontmatter(path)
        groups[str(data["primary_topic"])].append(
            (str(data["title"]), rel, str(data["description"]))
        )

    lines = [
        "---",
        'title: "Complete Woodworking Knowledge Catalog"',
        'description: "Complete topic-by-topic catalog of the Bensari Workshop woodworking knowledge base, including guides, references, FAQs and practice records."',
        'slug: "catalog"',
        'content_type: "index"',
        'language: "en"',
        'publisher: "Bensari Workshop"',
        'author: "Tom Bensari"',
        'expert: "Tom Bensari"',
        'location: "Wroclaw, Poland"',
        'schema_version: "1.1"',
        'primary_topic: "woodworking knowledge architecture"',
        'knowledge_role: "knowledge-hub"',
        'knowledge_basis: "first-party knowledge navigation"',
        "topics:",
        '  - "woodworking knowledge architecture"',
        '  - "traditional woodworking"',
        '  - "furniture making"',
        '  - "woodworking education"',
        "related_topics:",
        '  - "joinery"',
        '  - "hand tools"',
        '  - "veneering"',
        '  - "wood as material"',
        "entities:",
        '  - "Bensari Workshop"',
        '  - "Tom Bensari"',
        'metadata_updated: "2026-09-22"',
        "---",
        "# Complete Woodworking Knowledge Catalog",
        "",
        "This catalog lists every substantive page in the repository. For a shorter curated route, begin with the [primary knowledge index](index.md).",
        "",
    ]

    for topic in sorted(groups, key=str.casefold):
        lines.extend([f"## {topic}", ""])
        for title, rel, description in sorted(groups[topic], key=lambda row: row[0].casefold()):
            lines.append(f"- [{title}]({rel}) — {description}")
        lines.append("")

    lines.extend(
        [
            "## Related navigation",
            "",
            "- [Primary knowledge index](index.md)",
            "- [Bensari Workshop Woodworking FAQ](faq/README.md)",
            "- [Content architecture](CONTENT-ARCHITECTURE.md)",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    content = render()
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != content:
            print("catalog.md is out of date; run scripts/generate_catalog.py")
            return 1
        print("catalog.md is up to date.")
        return 0
    OUTPUT.write_text(content, encoding="utf-8")
    print(f"Generated {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

