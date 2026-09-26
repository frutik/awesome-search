---
type: video
title: "Qdrant Vector Search and Hybrid Routing"
speaker: "[[Andrei Cristea]]"
company: "[[Qdrant]]"
medium: talk / video
url: https://www.youtube.com/watch?v=nVtYPMvu8cc
published: 2026-09-22
conference: "[[Haystack EU]]"
duration: "5:05"
tags:
  - video
  - lightning-talk
  - hybrid-search
  - query-routing
  - query-classification
topics:
  - "[[Query Classification]]"
concepts:
  - "[[Query Routing]]"
  - "[[Hybrid Search]]"
  - "[[Reciprocal Rank Fusion]]"
  - "[[Sparse Vector Retrieval]]"
  - "[[Dense Vector Retrieval]]"
  - "[[Query Types]]"
  - "[[NDCG]]"
  - "[[Hit Rate at K]]"
tools:
  - "[[Qdrant Vector DB]]"
people:
  - "[[Andrei Cristea]]"
created: 2026-09-26
---

# Qdrant Vector Search and Hybrid Routing

📺 **Watch:** https://www.youtube.com/watch?v=nVtYPMvu8cc
🔗 Session page: https://haystackconf.com/session/lightning-talks/

Five-minute lightning talk by [[Andrei Cristea]] (developer relations engineer, [[Qdrant]]) at [[Haystack EU]]. The argument: [[Reciprocal Rank Fusion]] is the default everyone reaches for in [[Hybrid Search]], and it is a good default but not the best one — on some queries the fused ranking is worse than sparse-only or dense-only retrieval. Instead of always fusing, train a small classifier that looks at the query and **routes** it to the sparse retriever, the dense retriever, or RRF.

## Key Moments

| Time | Topic |
|---|---|
| [00:25](https://www.youtube.com/watch?v=nVtYPMvu8cc&t=25s) | The problem: RRF can rank below sparse-only or dense-only |
| [01:15](https://www.youtube.com/watch?v=nVtYPMvu8cc&t=75s) | Step 1: identify what kinds of queries exist |
| [01:37](https://www.youtube.com/watch?v=nVtYPMvu8cc&t=97s) | The query taxonomy: pattern-, metrics- and language-based |
| [02:04](https://www.youtube.com/watch?v=nVtYPMvu8cc&t=124s) | Step 2: dataset construction and labelling |
| [02:13](https://www.youtube.com/watch?v=nVtYPMvu8cc&t=133s) | 230,000 labelled queries and the route mix |
| [02:52](https://www.youtube.com/watch?v=nVtYPMvu8cc&t=172s) | Classifier architecture |
| [03:26](https://www.youtube.com/watch?v=nVtYPMvu8cc&t=206s) | Results on a held-out dataset vs hybrid RRF |
| [04:05](https://www.youtube.com/watch?v=nVtYPMvu8cc&t=245s) | Why not an LLM router: it mostly fell back to RRF |

---

## The Problem

RRF merges the sparse and dense result lists by rank alone, so it cannot tell when one side is simply right for a given query. The failure the team kept hitting: RRF would fail to put the most important results from *either* strategy at the top, and on some queries the hybrid ranking came out below what a single retriever would have returned on its own. That gap — fusion underperforming one of its own inputs — was the motivation for a per-query router. It is the same limitation the RRF note records as "does not account for query-type variance".

## Step 1 — A Query Taxonomy

To train a model that recognises query type, the team first needed a varied query set, and to pick queries they built a taxonomy with three families of signals:

- **Pattern-based** — structural patterns in the query string
- **Metrics-based** — measurable properties of the query
- **Language-based** — linguistic characteristics

Combined, these were used to select a diverse spread of queries from several source datasets. Compare the e-commerce and academic taxonomies in [[Query Types]].

## Step 2 — Dataset and Labels

The labelled set is about **230,000 queries**, each carrying a route label. The resulting route mix is lopsided: roughly **61% sparse, 36% dense, 3% RRF** — on this data, fusion was the chosen route for only a small minority of queries. Cristea's finding while building it: a better-balanced label distribution produced a better classifier.

## The Classifier

Deliberately simple. Three input sources feed a small neural network that outputs the route class:

1. An **encoder** embedding of the query
2. **N-gram** features, converted to dense numbers via **SVD** (see [[Dimensionality Reduction]])
3. A set of **lexical "shape" signals** describing the surface form of the query

## Results

Evaluated on a dataset not used in training, the router beat hybrid RRF on relevance, on hit@1 ([[Hit Rate at K]]) and on [[NDCG]]. The talk shows the comparison as a chart; no figures are read out.

## Why Not an LLM?

The team had tried an LLM-based router first. It mostly routed back to RRF — i.e. it played safe and collapsed to the default — so they moved to a dedicated classifier. This matches the cost ordering in [[Query Routing]]'s router-type table, where a trained classifier sits well below an LLM call.

## Related

- [[Query Routing]] — this is a retrieval-strategy router: sparse vs dense vs fused
- [[Query Classification]] — the router is a query classifier whose label picks the retriever
- [[Hybrid Search]] · [[Reciprocal Rank Fusion]] — the default being replaced per query
- [[Sparse Vector Retrieval]] · [[Dense Vector Retrieval]] — the two routes
- [[Query Types]] — other query taxonomies
- [[NDCG]] · [[Hit Rate at K]] — the reported metrics
- [[Qdrant]] · [[Qdrant Vector DB]] · [[Haystack EU]]
- Other Qdrant talks: [[Evgeniya Sukhodolskaya - Relevance Feedback Inside the Search Engine]] · [[Evgeniya Sukhodolskaya - Fine-Tuning Sparse Neural Retrievers for E-Commerce]]
