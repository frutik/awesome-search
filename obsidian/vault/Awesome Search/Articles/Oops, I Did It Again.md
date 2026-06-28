---
title: "Oops, I Did It Again"
source: "https://frutik.medium.com/oops-i-did-it-76ff089ac7e4"
author:
  - "[[Andrew Kornilov]]"
published: 2025-02-01
created: 2026-06-28
description: "The workaround to the vector-search-in-Quepid problem: generate a full Quepid case file with embeddings baked into query options, sidestepping per-query input limits."
tags:
  - search
  - search-evaluation
  - vector-search
  - medium
concepts:
  - Vector Search Evaluation
  - Quepid
  - Judgment Lists
topics:
  - Search Quality Assurance
---

# Oops, I Did It Again

The sequel to [[Why Setting Up Quepid for Vector Search Evaluation Went Wrong]]. Having hit query-length and JSON-validity walls, [[Andrew Kornilov]] finds a workaround that supports much higher-dimensional vectors: stop typing queries into [[Quepid]] one by one, and instead generate a complete **case file** with embeddings baked in.

---

## The Approach

Rather than adding queries through the UI, generate a Quepid-compatible **case JSON** that contains, per query:
- the query text, and
- its associated embedding (OpenAI `text-embedding-3-large`, 94 dims — see [[Matryoshka Embeddings]])

Eight sample product queries are used (e.g. "Bushcraft Survival Manual", "Scrub Top").

## Steps

1. Generate embeddings via the OpenAI API
2. Structure queries with embedded vectors in Quepid-compatible JSON
3. Upload the case file to Quepid
4. Configure the [[Elasticsearch]] backend to use the vectors in search requests
5. Begin the relevance judgment workflow

By carrying the vector inside the case's query options, the per-query input limit that broke the first attempt no longer applies — enabling higher dimensionality.

## Limitations & What's Next

- Storing embeddings in query options currently requires generating a *whole* case file — there's no per-query API to add one at a time. The author is building an **unofficial Quepid API** to close that gap (later realized as `frutik777/quepid-api-unofficial`).
- The same technique extends beyond pure semantic search to [[Hybrid Search]] and vector-based re-ranking.

## Related Concepts
- [[Vector Search Evaluation]] — the problem being solved
- [[Quepid]] · [[Judgment Lists]] · [[Search Evaluation]]
- [[Matryoshka Embeddings]] — 94-dim reduced embeddings
- [[Hybrid Search]] — applicable beyond semantic search

## Related Articles
- [[Why Setting Up Quepid for Vector Search Evaluation Went Wrong]] — the problem
- [[How to Evaluate Image Search in Qdrant Using Quepid Part 1]] — the technique applied to images
- [[How to Evaluate Image Search in Qdrant Using Quepid Part 2]] — the API realized

## People
- [[Andrew Kornilov]] — author

## Tools
- [[Quepid]] · [[Elasticsearch]]
