---
title: "Why Setting Up Quepid for Vector Search Evaluation Went Wrong"
source: "https://frutik.medium.com/why-setting-up-quepid-for-vector-search-evaluation-went-wrong-5fd0a90621f4"
author:
  - "[[Andrew Kornilov]]"
published: 2024-12-30
created: 2026-06-28
description: "First attempt at configuring Quepid for vector search — and the three things that broke: query length limits, JSON-validity vs. valid-query catch-22, and unreadable vector queries."
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

# Why Setting Up Quepid for Vector Search Evaluation Went Wrong

[[Andrew Kornilov]]'s first attempt to bend [[Quepid]] — a tool built for lexical search — toward [[Vector Search Evaluation]]. The plan: vectorize data outside the [[Elasticsearch]] ingest pipeline so embeddings from any source can be evaluated. It mostly went wrong, in instructive ways.

---

## The Setup

- **Index**: an Elasticsearch index with a `dense_vector` field (3072 dims) plus keyword fields for product name and image.
- **Data**: products from the [[Amazon ESCI Dataset]] (US subset).
- **Embeddings**: OpenAI `text-embedding-3-large`.
- **Pipeline**: a Python script (`tqdm`, `elasticsearch`, `openai`) iterates JSON records, embeds product titles, and indexes them with metadata.

## What Broke

### 1. Query length limit
Quepid caps query input at **2048 characters**. A full 3072-dim embedding far exceeds that. Workaround: use OpenAI's dimensionality reduction ([[Matryoshka Embeddings]]) to compress vectors to **94 dimensions** so they fit.

### 2. JSON validity vs. a valid query (the catch-22)
Quepid requires the query template to be valid JSON. A raw vector array breaks that validation. Wrapping the vector in quotes satisfies Quepid — but then produces a *malformed* Elasticsearch query. Neither configuration fully works.

### 3. Vectors aren't human-readable
Even if the query runs, raters can't judge results against a query that is just an array of floats. The query needs a human-interpretable **label** alongside the vector.

## Proposed Fixes (to Quepid)

- Allow "invalid" JSON in advanced settings for specialized query templates
- A richer query entity: label + vector + metadata together
- Better visualization for non-textual search
- First-class support for hybrid (lexical + vector) scenarios

## Outcome

A documented dead end — the sequel ([[Oops, I Did It Again]]) finds a workaround by generating a complete Quepid **case file** with embeddings baked in, sidestepping the per-query input limits.

## Related Concepts
- [[Vector Search Evaluation]] — the central challenge set
- [[Matryoshka Embeddings]] — dimension reduction to fit the 2048-char limit
- [[Quepid]] · [[Judgment Lists]] · [[Search Evaluation]]
- [[Hybrid Search]] — the unsupported scenario the author wanted

## Related Articles
- [[Oops, I Did It Again]] — the workaround
- [[Creating Judgement Lists with Quepid]] — how Quepid works for *text* queries
- [[How to Evaluate Image Search in Qdrant Using Quepid Part 1]]

## People
- [[Andrew Kornilov]] — author

## Tools
- [[Quepid]] · [[Elasticsearch]]
