---
title: "Federated Search"
aliases: ["distributed information retrieval", "distributed IR", "metasearch", "collection selection", "federated retrieval"]
tags:
  - concept
  - search
  - architecture
created: 2026-06-23
---

# Federated Search

Querying multiple independent collections or search engines from a single entry point, then merging their results into one ranked list. The defining constraint: the broker does **not** own a single unified index — it routes a query out to autonomous sources and reconciles what comes back.

This is the classic IR subfield of **distributed information retrieval (DIR)** / **metasearch**. It is distinct from [[Knowledge Graph Search|federated *graph* search]], which unifies heterogeneous entity types into one searchable structure — that is a data-modeling concern, not the retrieval problem below.

## The Three Sub-Problems

Federated search decomposes into three stages, each its own research thread:

1. **Resource (collection) selection** — given a query, decide *which* sources are worth querying. You rarely fan out to all of them (cost, latency, relevance). Classic approaches: CORI, ReDDE, and query-likelihood models that score each collection from sampled documents.
2. **Query routing / dispatch** — translate and send the query to each chosen source, respecting its native syntax and capabilities.
3. **Results merging (fusion)** — combine the returned ranked lists into one. The hard part: scores from different engines are **incomparable** (different scales, or scores hidden entirely). See [[Reciprocal Rank Fusion]], which merges on rank position alone and is the workhorse here.

## Why It's Hard

| Challenge | Root cause |
|-----------|-----------|
| Uncooperative sources | No access to corpus stats or term frequencies — only the result list |
| Score incomparability | Each engine has its own scoring; raw scores can't be added |
| Collection representation | You must estimate what each source contains without indexing it (query-based sampling) |
| Latency tail | Fan-out is gated by the slowest source; partial-result strategies needed |
| Coverage vs. cost | Querying more sources raises recall but multiplies cost and latency |

## Cooperative vs. Uncooperative

- **Cooperative** environments expose collection statistics (term counts, sizes), making selection and score normalization tractable.
- **Uncooperative** environments (the general web-metasearch case) expose only ranked result lists, forcing **query-based sampling** to build a representation of each source and **rank-based fusion** for merging.

## Where It Shows Up

- **Multilingual search** — per-language indexes queried in parallel and merged; see [[Multilingual Search]] (the "Per-Language Indexes + Federated Search" pattern).
- **Enterprise search** — fanning a query across email, wikis, ticketing, code, and drives, each with its own connector and index; see [[Enterprise Search]].
- **Hybrid retrieval** — the same merging machinery (RRF, linear fusion) reconciles lexical and semantic result lists; see [[Hybrid Search]]. Hybrid is federation over *representation spaces* rather than over *collections*.
- **Sharded indexes** — a single logical index split across shards is the degenerate, cooperative case: fan out, gather, merge.

## Relationship to Hybrid Search

Hybrid search and federated search share the **results-merging** stage but differ upstream: hybrid queries *one corpus through multiple retrieval methods* ([[BM25]] + [[Dense Vector Retrieval]]), while federated search queries *multiple corpora/engines*. Both lean on score-agnostic fusion like [[Reciprocal Rank Fusion]] precisely because the candidate scores don't share a scale.

## Related Concepts

- [[Reciprocal Rank Fusion]]
- [[Hybrid Search]]
- [[Retrieval Pipeline]]
- [[Search Architecture]]
- [[Multilingual Search]]
- [[Enterprise Search]]
- [[Knowledge Graph Search]]
