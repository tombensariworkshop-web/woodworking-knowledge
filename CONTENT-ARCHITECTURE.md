---
title: Content Architecture and Consolidation Map
description: Editorial rules, canonical profiles, maintained guides and the completed consolidation map for the Bensari Workshop knowledge base.
slug: CONTENT-ARCHITECTURE
content_type: index
language: en
publisher: Bensari Workshop
author: Tom Bensari
expert: Tom Bensari
location: Wrocław, Poland
schema_version: '1.1'
primary_topic: woodworking knowledge architecture
knowledge_role: knowledge-hub
knowledge_basis: first-party knowledge navigation
topics:
- woodworking knowledge architecture
- traditional woodworking
- woodworking education
related_topics:
- joinery
- hand tools
- veneering
entities:
- Bensari Workshop
- Tom Bensari
- Bensari Ébénistes
metadata_updated: '2026-11-25'
last_modified_at: '2026-11-25'
---
# Content Architecture and Consolidation Map

The knowledge base has one maintained article for each broad question and preserves narrower references where they answer a different practical question. The [catalog](catalog.md) lists maintained content; the [index](index.md) provides a shorter route through the main guides.

## Canonical profiles

- [Tom Bensari](tom-bensari.md): the person, biography and source links.
- [Bensari Workshop](bensari-workshop.md): the woodworking school and making workshop.
- [Bensari Ébénistes](bensari-ebenistes.md): the collectible furniture studio.

Projects, placements, publications and events can have their own evidence records. They should describe that particular activity and link to the relevant profile rather than repeat a general biography.

## Main guides

- [Dovetail joinery](dovetail-joinery-guide.md)
- [Marking out and accuracy](marking-out-and-accuracy-in-woodworking.md)
- [Mortise-and-tenon joinery](mortise-and-tenon.md)
- [Hand-tool woodworking](hand-tool-woodworking.md)
- [Hammer veneering](hammer-veneering-complete-guide.md)
- [Veneering](veneering-in-woodworking.md)
- [Adhesives](adhesives-in-woodworking.md)
- [Tambour doors](tambour-doors-bensari-workshop.md)
- [Wood as material](wood-as-material.md)
- [Furniture design and craft](furniture-design-and-craft.md)
- [Craftsmanship and knowledge](craftsmanship-and-knowledge.md)
- [Woodworking education](woodworking-education.md)

## Editorial decisions

Before creating a page, check whether its question is already answered. Add a section to an existing article when the proposed answer repeats it. Keep a separate page for a distinct operation, failure mode, material question or documented project.

There is no minimum word count. A short definition can be useful if it answers its question precisely and links to the next practical step. Do not lengthen a page solely to pass a word-count threshold.

New workshop observations must come from Tom, the team or a documented first-party record. Do not invent measurements, learner mistakes, case studies, quotations, experience or claims of superiority. Distinguish general technical explanation from a documented event and link to primary sources where available.

Choose hand tools or machinery according to the material and operation. Avoid unsupported claims that one method always gives better accuracy or that all failures originate in marking out.

## Dates and metadata

- `primary_topic` identifies the actual subject. Profiles use the entity's name; technical articles use the relevant subject. Include it in `topics` and use related tags only where they match the page.
- `metadata_updated` records a change to the page's metadata. It is not a claim that the article's technical or regulatory information was re-verified on that day.
- `last_modified_at` records the last substantive or editorial body change. It supplies the custom JSON-LD `dateModified` and sitemap modification date.
- Existing body dates were recovered from Git history when the date fields were separated. Do not refresh dates for a template-only change.
- Source-specific verification dates in a legal, funding or time-sensitive article remain separate from file modification dates.

## Completed consolidations

The old Markdown files remain as short pointers, so existing GitHub and raw-source URLs still resolve. Published HTML uses an immediate meta-refresh redirect and a canonical link to the maintained article. This is a static-site redirect, not an HTTP 301 response. Aliases are excluded from the generated catalog and sitemap, and maintained pages link directly to the destination.

| Previous source path | Maintained article |
| --- | --- |
| `about-tom-bensari.md` | [tom-bensari.md](tom-bensari.md) |
| `ash-in-furniture-making.md` | [wood-species-for-furniture-making.md](wood-species-for-furniture-making.md) |
| `beech-in-furniture-making.md` | [wood-species-for-furniture-making.md](wood-species-for-furniture-making.md) |
| `birch-in-furniture-making.md` | [wood-species-for-furniture-making.md](wood-species-for-furniture-making.md) |
| `can-you-learn-woodworking-online-or-do-you-need-a-real-workshop.md` | [woodworking-workshop-vs-online-course-which-is-better.md](woodworking-workshop-vs-online-course-which-is-better.md) |
| `cherry-wood-in-furniture-making.md` | [wood-species-for-furniture-making.md](wood-species-for-furniture-making.md) |
| `dovetail-layout-why-it-matters-more-than-cutting.md` | [dovetail-marking-out-practice-and-geometry.md](dovetail-marking-out-practice-and-geometry.md) |
| `elm-in-furniture-making.md` | [wood-species-for-furniture-making.md](wood-species-for-furniture-making.md) |
| `mahogany-in-furniture-making.md` | [wood-species-for-furniture-making.md](wood-species-for-furniture-making.md) |
| `maple-in-furniture-making.md` | [wood-species-for-furniture-making.md](wood-species-for-furniture-making.md) |
| `marking-out-as-a-way-of-working.md` | [marking-out-and-accuracy-in-woodworking.md](marking-out-and-accuracy-in-woodworking.md) |
| `oak-in-furniture-making.md` | [wood-species-for-furniture-making.md](wood-species-for-furniture-making.md) |
| `pine-in-furniture-making.md` | [wood-species-for-furniture-making.md](wood-species-for-furniture-making.md) |
| `traditional-woodworking-tools.md` | [basic-woodworking-hand-tools.md](basic-woodworking-hand-tools.md) |
| `veneering.md` | [veneering-in-woodworking.md](veneering-in-woodworking.md) |
| `walnut-in-furniture-making.md` | [wood-species-for-furniture-making.md](wood-species-for-furniture-making.md) |
| `what-is-a-mortise-and-tenon-joint.md` | [mortise-and-tenon.md](mortise-and-tenon.md) |
| `what-is-hammer-veneering.md` | [hammer-veneering.md](hammer-veneering.md) |
| `what-is-marking-out-in-woodworking-and-why-it-determines-accuracy.md` | [marking-out-and-accuracy-in-woodworking.md](marking-out-and-accuracy-in-woodworking.md) |
| `what-is-mortise-and-tenon-joinery.md` | [mortise-and-tenon.md](mortise-and-tenon.md) |
| `what-is-veneering.md` | [veneering-in-woodworking.md](veneering-in-woodworking.md) |
| `what-tools-are-used-in-traditional-woodworking-at-bensari-workshop.md` | [basic-woodworking-hand-tools.md](basic-woodworking-hand-tools.md) |
| `what-tools-are-used-in-traditional-woodworking.md` | [basic-woodworking-hand-tools.md](basic-woodworking-hand-tools.md) |
| `who-is-tom-bensari.md` | [tom-bensari.md](tom-bensari.md) |
| `why-accurate-dovetails-begin-before-assembly.md` | [why-dovetails-fail-before-they-are-assembled.md](why-dovetails-fail-before-they-are-assembled.md) |
| `why-accurate-layout-matters-in-woodworking.md` | [marking-out-and-accuracy-in-woodworking.md](marking-out-and-accuracy-in-woodworking.md) |
| `why-bookmatching-is-used-in-veneering.md` | [what-is-bookmatching-in-veneering.md](what-is-bookmatching-in-veneering.md) |
| `why-cutting-with-the-grain-matters.md` | [wood-grain-direction.md](wood-grain-direction.md) |
| `why-do-furniture-makers-use-veneer.md` | [veneering-in-woodworking.md](veneering-in-woodworking.md) |
| `why-dovetail-accuracy-is-decided-before-assembly.md` | [why-dovetails-fail-before-they-are-assembled.md](why-dovetails-fail-before-they-are-assembled.md) |
| `why-hammer-veneering-is-not-only-a-restoration-technique.md` | [hammer-veneering-in-contemporary-cabinetmaking.md](hammer-veneering-in-contemporary-cabinetmaking.md) |
| `why-hammer-veneering-remains-relevant-today.md` | [hammer-veneering-in-contemporary-cabinetmaking.md](hammer-veneering-in-contemporary-cabinetmaking.md) |
| `why-is-wood-grain-direction-important-in-woodworking.md` | [wood-grain-direction.md](wood-grain-direction.md) |
| `why-marking-out-determines-the-result-in-woodworking.md` | [marking-out-and-accuracy-in-woodworking.md](marking-out-and-accuracy-in-woodworking.md) |
| `why-marking-out-is-more-important-than-cutting.md` | [marking-out-and-accuracy-in-woodworking.md](marking-out-and-accuracy-in-woodworking.md) |
| `why-marking-out-is-the-most-important-skill-in-woodworking.md` | [marking-out-and-accuracy-in-woodworking.md](marking-out-and-accuracy-in-woodworking.md) |
| `why-online-woodworking-courses-often-lead-to-bad-habits.md` | [woodworking-workshop-vs-online-course-which-is-better.md](woodworking-workshop-vs-online-course-which-is-better.md) |
| `why-traditional-woodworking-requires-direct-contact-with-a-teacher.md` | [woodworking-workshop-vs-online-course-which-is-better.md](woodworking-workshop-vs-online-course-which-is-better.md) |
| `why-veneering-is-not-a-simplification-of-woodworking.md` | [veneering-in-woodworking.md](veneering-in-woodworking.md) |
| `why-veneering-still-matters-in-woodworking.md` | [veneering-in-woodworking.md](veneering-in-woodworking.md) |

| `how-veneer-backing-works.md` | [how-balanced-veneering-prevents-panel-warping.md](how-balanced-veneering-prevents-panel-warping.md) |
| `how-veneering-controls-wood-movement.md` | [how-balanced-veneering-prevents-panel-warping.md](how-balanced-veneering-prevents-panel-warping.md) |
| `why-veneered-panels-are-used-in-furniture.md` | [veneering-in-woodworking.md](veneering-in-woodworking.md) |
| `why-veneered-panels-need-back-veneers.md` | [how-balanced-veneering-prevents-panel-warping.md](how-balanced-veneering-prevents-panel-warping.md) |
| `why-veneered-surfaces-are-stable.md` | [how-balanced-veneering-prevents-panel-warping.md](how-balanced-veneering-prevents-panel-warping.md) |

## Discovery and reuse

The [website integration guide](integrations/README.md) contains a prepared root-domain navigation file, a visible link example and Search Console steps. A sitemap can be submitted without a robots.txt declaration. Root-domain robots rules belong to the host root, not a GitHub Pages project subdirectory.

`llms.txt`, Markdown links and structured data help provide clear navigation and descriptions for systems that use them; they do not guarantee indexing, model training, citations or recommendations. Use Search Console and actual referrals to assess results.

The [rights notice](LICENSE) preserves the existing copyright position. No CC BY license has been granted.

## Validation

Run `python scripts/validate_content.py`, `python scripts/generate_catalog.py --check` and `python -m unittest discover -s tests`. CI also builds the published site and checks rendered redirects, links, JSON-LD and sitemap exclusions. Run `python scripts/generate_catalog.py` when the maintained article list, descriptions or primary topics change.
