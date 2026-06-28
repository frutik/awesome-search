---
title: "How to Evaluate Image Search in Qdrant Using Quepid Part 1 (No Hacks)"
source: "https://frutik.medium.com/how-to-evaluate-image-search-in-qdrant-using-quepid-and-the-hacks-it-takes-part-1-f8167ec5cba3"
author:
  - "[[Andrew Kornilov]]"
published: 2026-02-15
created: 2026-06-28
description: "Part 1 of evaluating image search: data preparation. Building a CLIP-based cross-modal image search over Amazon shopping products in Qdrant, before wiring up evaluation."
tags:
  - search
  - search-evaluation
  - vector-search
  - multimodal
  - medium
concepts:
  - Vector Search Evaluation
  - Multimodal Embeddings
  - Dense Vector Retrieval
topics:
  - Search Quality Assurance
---

# How to Evaluate Image Search in Qdrant Using Quepid Part 1 (No Hacks)

Part 1 of a series on building a pipeline to evaluate vector retrieval quality with IR metrics. This installment is **data preparation** — the search itself is kept intentionally simple. The hacks come in [[How to Evaluate Image Search in Qdrant Using Quepid Part 2|Part 2]].

---

## Stack

- **[[Qdrant Vector DB]]** — vector search engine
- **[[Quepid]]** — evaluation / metric calculation (wired up in Part 2)
- **Data** — Amazon's Shopping Queries Dataset + extended metadata ([[Amazon ESCI Dataset]] / [[ESCI-S Dataset]])

## Data Preparation

1. **Queries** — load the shopping-queries dataset into a Pandas DataFrame.
2. **Product selection** — from 1M+ US products: drop books, drop products without images, sample 40,000 and download images, keep ~**21,589** products with valid image URLs.
3. **Embeddings** ([[Multimodal Embeddings]] via CLIP, using Qdrant's `fastembed`):
   - Images → `Qdrant/clip-ViT-B-32-vision` → 512-dim vectors
   - Queries → `Qdrant/clip-ViT-B-32-text` (same space) → enables **cross-modal** text→image search
4. **Query filtering** — keep the **top 200** most frequent queries as the evaluation set.

## Qdrant Implementation

- Collection set up via Docker, cosine distance.
- Products indexed with payloads (title, image URL).
- Cross-modal validation: the text query "reclining leather sectional" successfully retrieved matching furniture images — "we just found those images by searching with text query."

## Part 2 Preview

Integrating Quepid with this image-search system requires non-standard workarounds — the "cheats and hacks" of the series title.

## Related Concepts
- [[Vector Search Evaluation]] — the goal of the series
- [[Multimodal Embeddings]] — CLIP text + vision encoders in a shared space
- [[Dense Vector Retrieval]] — what's being built
- [[Quepid]] · [[Judgment Lists]] · [[Search Evaluation]]

## Related Articles
- [[How to Evaluate Image Search in Qdrant Using Quepid Part 2]] — the hacks + evaluation
- [[Oops, I Did It Again]] — the case-file technique reused here
- [[Why Setting Up Quepid for Vector Search Evaluation Went Wrong]]

## People
- [[Andrew Kornilov]] — author

## Tools
- [[Qdrant Vector DB]] · [[Quepid]]
