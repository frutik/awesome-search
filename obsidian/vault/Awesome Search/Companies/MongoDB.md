---
title: "MongoDB"
type: company
tags:
  - company
  - database
  - vector-search
  - search
website: "https://www.mongodb.com/"
category: technology-provider
industry: database / AI infrastructure
products: ["MongoDB Atlas", "Atlas Search", "Atlas Vector Search"]
search_domain: [vector search, hybrid search, full-text search]
created: 2026-05-19
---

# MongoDB

Database platform company. Relevant to search via **MongoDB Atlas Search** — a full-text and vector search capability built on Apache Lucene, embedded inside Atlas (MongoDB's managed cloud database).

## Search Contributions

**Semantic Boosting** — a two-phase hybrid retrieval technique named and described by [[Erik Hatcher]]: run vector search first, inject results as boost clauses into a final lexical `$search` query. Preserves native faceting, highlighting, and pagination.

**Atlas Search** — Lucene-powered full-text search integrated directly into the MongoDB document model. Supports `$search` (lexical), `$vectorSearch` (dense ANN), and `$rankFusion` / `$scoreFusion` fusion operators.

### Fusion aggregation stages

| Stage | Purpose |
|---|---|
| `$rankFusion` | [[Reciprocal Rank Fusion\|RRF]] over named input pipelines, with per-pipeline `combination.weights` |
| `$scoreFusion` | [[Relative Score Fusion\|RSF]] with `input.normalization` (`none` / `sigmoid` / `minMaxScaler`) and `combination.method` (`avg` or a custom expression) |
| `$score` | Places a computed value into `$meta.score` for pipelines that don't already produce one; optionally normalizes |
| `$meta: 'scoreDetails'` | Exposes the full per-pipeline computation — rank or raw score, weight, and contribution — for [[Search Results Explainability\|explainability]] |

Because the 60 in the RRF denominator is a fixed built-in, a weight of 30 on each of two pipelines
conveniently rescales the fused score into a ~0.0–1.0 range. `$vectorSearch` scores already arrive
in 0.0–1.0, while lexical `$search` [[BM25]] scores are unbounded — so [[Score Normalization]]
matters far more on the lexical leg. Worked through in
[[Reciprocal Rank Fusion and Relative Score Fusion]].

## People
- [[Erik Hatcher]]

## Articles

The MongoDB Hybrid Search series by [[Erik Hatcher]]:

1. [[Survey of the Hybrid Search Landscape]]
2. [[Reciprocal Rank Fusion and Relative Score Fusion]]
3. [[Hybrid Search Blueprint Series Semantic Boosting]]

## Key Concepts
- [[Semantic Boosting]]
- [[Hybrid Search]]
- [[Reciprocal Rank Fusion]]
- [[Relative Score Fusion]]
- [[Score Normalization]]
- [[Search Results Explainability]]
