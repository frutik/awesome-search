---
title: "How to Evaluate Image Search in Qdrant Using Quepid Part 2 (Hacks)"
source: "https://frutik.medium.com/how-to-evaluate-image-search-in-qdrant-using-quepid-and-the-hacks-it-takes-part-2-hacks-39ed553cd97a"
author:
  - "[[Andrew Kornilov]]"
published: 2026-04-10
created: 2026-06-28
description: "Part 2: wiring Qdrant into Quepid as a custom search endpoint via an unofficial API, injecting CLIP query vectors through query options, and the hacks (and a PR) needed to render image results in the rating UI."
tags:
  - search
  - search-evaluation
  - vector-search
  - multimodal
  - medium
concepts:
  - Vector Search Evaluation
  - Multimodal Embeddings
  - Quepid
topics:
  - Search Quality Assurance
---

# How to Evaluate Image Search in Qdrant Using Quepid Part 2 (Hacks)

The payoff of the series: actually measuring image-search quality. [[Andrew Kornilov]] registers [[Qdrant Vector DB]] as a custom [[Quepid]] search endpoint, loads 200 CLIP queries with embeddings, and computes NDCG@10 — plus the hacks (and one upstream PR) needed to make image results judgeable. Builds on [[How to Evaluate Image Search in Qdrant Using Quepid Part 1|Part 1]] and the case-file trick from [[Oops, I Did It Again]].

---

## Infrastructure (three containers)

1. **Qdrant** — REST :6333, gRPC :6334; embeddings + image metadata.
2. **Quepid** — MySQL 8.4.4 backend + Quepid v8.3.6 app (:3000); judgment management and IR metrics.
3. **Quepid HTTP API wrapper** — the author's unofficial API (`frutik777/quepid-api-unofficial`, :8081) for programmatic case/query creation.

Init steps: DB migrations, seed data, admin user, API key. Python deps: `pandas`, `requests`, `tqdm`.

## Building the Evaluation Case

1. **Team** — created via the API to group evaluations.
2. **Search endpoint** — register Qdrant as a custom backend with a JavaScript mapper that turns Qdrant responses into Quepid's format (doc IDs, thumbnails, titles from the payload). The key trick: inject the query embedding from options with `"vector": "#$qOption.clip##"`.
3. **Cases & queries** — load the 200 pre-selected queries with their CLIP embeddings; Quepid computes **NDCG@10** as judges rate.

## Image-as-Query Case

A separate use case: sample 25 random products and use *their image vectors* as queries — image→image visual-similarity evaluation, in its own case.

## The Hacks

- **Hack 1 — scorer-level rendering.** Inject JavaScript into Quepid's scorer to render image URLs as actual `<img>` elements:
  `const customHTML = \`<img width="75" src="${originalText}"/>\`;`
  Limits: only the first results page; breaks pagination; no page control.
- **Hack 2 — fix it properly upstream.** Rather than maintain fragile JS, the author opened **Quepid PR #1683** to add native image-query rendering.

## Achievements

1. Qdrant configured as a Quepid endpoint
2. A case of 200 text queries with embeddings
3. Query-construction + result-parsing infrastructure
4. Explored UI customization for image visualization
5. Documented platform limitations needing native fixes

## Key Insight

Creative workarounds can extend a platform, but sustainable solutions mean contributing fixes upstream rather than nursing JavaScript hacks.

## Future Direction

Next: automated judgement generation via Quepid's **LLM-as-a-judge** ([[LLM as Judge]]), to cut manual annotation.

## Related Concepts
- [[Vector Search Evaluation]] — the realized pipeline
- [[Multimodal Embeddings]] — CLIP text/image vectors; image→image search
- [[Quepid]] · [[Judgment Lists]] · [[NDCG]] · [[Search Evaluation]]
- [[LLM as Judge]] — teased follow-up

## Related Articles
- [[How to Evaluate Image Search in Qdrant Using Quepid Part 1]] — data prep
- [[Oops, I Did It Again]] — the case-file / query-options technique
- [[Why Setting Up Quepid for Vector Search Evaluation Went Wrong]] — original blockers
- [[Creating Judgement Lists with Quepid]] — the conventional (text) workflow

## People
- [[Andrew Kornilov]] — author

## Tools
- [[Qdrant Vector DB]] · [[Quepid]]
