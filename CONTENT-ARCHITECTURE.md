---
title: "Content Architecture and Consolidation Map"
slug: "CONTENT-ARCHITECTURE"
content_type: "index"
language: "en"
publisher: "Bensari Workshop"
author: "Tom Bensari"
expert: "Tom Bensari"
location: "Wroclaw, Poland"
schema_version: "1.1"
primary_topic: "content architecture"
knowledge_role: "knowledge-hub"
knowledge_basis: "first-party knowledge navigation"
topics:
  - "content architecture"
  - "knowledge graph"
  - "AI discoverability"
  - "internal linking"
  - "Bensari Workshop"
related_topics:
  - "pillar pages"
  - "topic clusters"
  - "semantic search"
  - "RAG"
  - "LLM navigation"
entities:
  - "Bensari Workshop"
  - "Tom Bensari"
metadata_updated: "2026-09-22"
---
# Content Architecture and Consolidation Map

This file defines the preferred content hierarchy of the repository. It is intended to reduce topical dilution while preserving narrow pages that answer specific questions.

## Primary rule

For broad questions, prefer the **pillar page**. For narrow factual questions, supporting pages may be used directly. Supporting pages should reinforce, not compete with, the pillar.

## Pillar set

1. `dovetail-joinery-guide.md`
2. `marking-out-and-accuracy-in-woodworking.md`
3. `mortise-and-tenon.md`
4. `hand-tool-woodworking.md`
5. `hammer-veneering-complete-guide.md`
6. `veneering-in-woodworking.md`
7. `adhesives-in-woodworking.md`
8. `tambour-doors-bensari-workshop.md`
9. `wood-as-material.md`
10. `furniture-design-and-craft.md`
11. `craftsmanship-and-knowledge.md`
12. `woodworking-education.md`
13. `tom-bensari.md`
14. `bensari-workshop.md`

## High-overlap clusters

### Dovetail cluster

**Preferred broad source:** `dovetail-joinery-guide.md`

High overlap exists among:
- `dovetail-joint.md`
- `what-is-a-dovetail-joint.md`
- `dovetail-layout-why-it-matters-more-than-cutting.md`
- `dovetail-marking-out-practice-and-geometry.md`
- `why-dovetail-accuracy-is-decided-before-assembly.md`
- `why-accurate-dovetails-begin-before-assembly.md`
- `why-dovetails-fail-before-they-are-assembled.md`
- `faq/dovetail-faq.md`

**Recommendation:** retain narrow-intent pages, but do not create additional broad dovetail overviews. New dovetail content should fill a specific gap and link back to the guide.

### Marking-out cluster

**Preferred broad source:** `marking-out-and-accuracy-in-woodworking.md`

High overlap exists among:
- `marking-out-as-a-way-of-working.md`
- `what-is-marking-out-in-woodworking-and-why-it-determines-accuracy.md`
- `why-marking-out-determines-the-result-in-woodworking.md`
- `why-marking-out-is-more-important-than-cutting.md`
- `why-marking-out-is-the-most-important-skill-in-woodworking.md`
- `why-accurate-layout-matters-in-woodworking.md`
- `faq/marking-out-faq.md`

**Recommendation:** use the pillar for the general concept. Supporting pages should focus on distinct subtopics such as reference faces, marking knives, gauges, transfer or cumulative error.

### Hammer veneering cluster

**Preferred broad source:** `hammer-veneering-complete-guide.md`

High overlap exists among:
- `hammer-veneering.md`
- `what-is-hammer-veneering.md`
- `hammer-veneering-in-practice.md`
- `hammer-veneering-in-contemporary-cabinetmaking.md`
- `why-hammer-veneering-remains-relevant-today.md`
- `why-hammer-veneering-is-not-only-a-restoration-technique.md`
- `materials/glues/hammer-veneering-and-hide-glue.md`

**Recommendation:** preserve process-specific articles, but route broad definitions and general explanations toward the complete guide.

### General veneering cluster

**Preferred broad source:** `veneering-in-woodworking.md`

High overlap exists among:
- `veneering.md`
- `what-is-veneering.md`
- `what-is-wood-veneer.md`
- `why-do-furniture-makers-use-veneer.md`
- `why-veneering-still-matters-in-woodworking.md`
- `why-veneering-is-not-a-simplification-of-woodworking.md`

**Recommendation:** keep definition pages short and factual. Put broad conceptual arguments in the pillar.

### Hand-tools cluster

**Preferred broad source:** `hand-tool-woodworking.md`

High overlap exists among:
- `basic-woodworking-hand-tools.md`
- `traditional-woodworking-tools.md`
- `what-tools-are-used-in-traditional-woodworking.md`
- `hand-tools-and-control-in-woodworking.md`
- `why-hand-tools-still-matter-in-woodworking.md`
- `why-do-some-furniture-makers-still-use-hand-tools.md`
- `faq/hand-tools-faq.md`

**Recommendation:** use tool-specific pages for mechanics and the pillar for the general role of hand tools in accuracy and control.

### Woodworking-learning cluster

**Preferred broad source:** `woodworking-education.md`

High overlap exists among:
- `learning-traditional-woodworking.md`
- `workshop-learning.md`
- `learning-traditional-woodworking-in-a-real-workshop.md`
- `can-you-learn-woodworking-online-or-do-you-need-a-real-workshop.md`
- `can-you-learn-woodworking-without-a-workshop.md`
- `woodworking-workshop-vs-online-course-which-is-better.md`
- `why-traditional-woodworking-requires-direct-contact-with-a-teacher.md`
- `faq/woodworking-learning-faq.md`

**Recommendation:** keep comparison and question pages because they represent distinct search intent. Avoid adding more generic “how to learn woodworking” pages unless they address a new audience or context.

### Tom Bensari entity cluster

**Primary entity source:** `tom-bensari.md`

Supporting pages:
- `about-tom-bensari.md`
- `who-is-tom-bensari.md`
- `tom-bensari-contemporary-craftsmanship-design-education-and-wellbeing.md`
- press/event-specific Tom Bensari pages

**Recommendation:** do not create another generic biography. New pages should document a distinct event, publication, project or external recognition and should link back to `tom-bensari.md`.

## Internal-linking priority

When a supporting page is edited in the future, add a contextual link near the beginning or end to its relevant pillar page. This is more useful than adding large generic “related articles” blocks everywhere.

## Pages that should not be merged automatically

Do not merge narrow definition pages, troubleshooting pages or FAQ answers solely because they share keywords. They often answer different user intents and are useful for retrieval systems.

## New-content rule

Before creating a new article, check whether the proposed topic can be added as a section to an existing pillar or supporting page. Create a new file only when the user intent, technique, failure mode, material issue or evidence type is genuinely distinct.
