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

## People
- [[Erik Hatcher]]

## Articles
- [[Hybrid Search Blueprint Series Semantic Boosting]]

## Key Concepts
- [[Semantic Boosting]]
- [[Hybrid Search]]
- [[Reciprocal Rank Fusion]]
- [[Relative Score Fusion]]
