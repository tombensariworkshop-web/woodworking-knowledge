---
title: Website integration and search discovery
description: Prepared links and navigation for bensariworkshop.com, with sitemap submission steps and clear limits on claims about AI discovery.
slug: website-integration
content_type: index
language: en
publisher: Bensari Workshop
author: Tom Bensari
expert: Tom Bensari
location: Wrocław, Poland
schema_version: '1.1'
primary_topic: woodworking knowledge architecture
knowledge_role: knowledge-hub
knowledge_basis: publication and navigation instructions
topics:
- woodworking knowledge architecture
- woodworking education
related_topics:
- Bensari Workshop
- Tom Bensari
entities:
- Bensari Workshop
- Tom Bensari
metadata_updated: '2026-11-25'
last_modified_at: '2026-11-25'
---
# Website integration and search discovery

The repository publishes maintained knowledge and practical records. The official website remains the source for current courses, prices, dates and reservations. These instructions prepare the connections between them; they do not mean that changes have already been made in WordPress or Search Console.

## Visible website link

Add a relevant link on the website's learning resources or About page. A footer link can supplement it, but hundreds of repeated links are unnecessary.

Polish wording:

```html
<a href="https://tombensariworkshop-web.github.io/woodworking-knowledge/">
  Baza wiedzy stolarskiej Bensari Workshop — materiały po angielsku
</a>
```

English wording:

```html
<a href="https://tombensariworkshop-web.github.io/woodworking-knowledge/">
  Bensari Workshop woodworking knowledge base
</a>
```

The source repository can be linked separately as [woodworking-knowledge on GitHub](https://github.com/tombensariworkshop-web/woodworking-knowledge).

## Optional root-domain navigation file

The prepared [root-domain llms.txt](bensariworkshop-com/llms.txt) can be published at `/llms.txt` on the official website. If that address already has a maintained file, merge the relevant links rather than replacing its content blindly.

This file is an optional navigation aid for systems that choose to use it. It is not a requirement for Google Search or its generative AI features, and it does not guarantee citations, indexing or training use. Google explains this in its [generative AI optimization guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide).

## Sitemap submission

The project's sitemap address is:

`https://tombensariworkshop-web.github.io/woodworking-knowledge/sitemap.xml`

1. Verify the matching URL-prefix property in Search Console, using an available verification method. A `bensariworkshop.com` property does not cover the separate GitHub Pages host.
2. Submit the sitemap in the Sitemaps report.
3. Inspect the main index and a small selection of maintained guides and profiles.
4. Review the report for actual indexing decisions, processing errors and later search performance.

A robots.txt declaration is not required to submit a sitemap. A `robots.txt` file under the project path cannot control the root `github.io` host. Root-host configuration would require a separate user-site repository or a suitable custom-domain setup. There is no need to create one solely to submit this sitemap.

See Google's [sitemap-submission documentation](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap). Submission is a discovery hint and does not guarantee indexing.

## What to measure

Use Search Console for indexed URLs, queries, impressions and clicks on the Pages property. Use website analytics for visits arriving from the knowledge base and AI services. Server access logs, when available, can help establish crawler visits; a visit does not prove inclusion in a model's training data or future answers.

The [content architecture](../CONTENT-ARCHITECTURE.md) explains the maintained guides, aliases, source dates and editorial rules.
