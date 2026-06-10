---
title: "WAND and Block-Max WAND: Efficient Algorithms for Top-k Document Retrieval"
type: article
source: "https://medium.com/@jithendrasaikilaru/wand-and-block-max-wand-efficient-algorithms-for-top-k-document-retrieval-5dfca4b84499"
author:
  - "[[Jithendrasaikilaru]]"
published: 2025-10-31
created: 2026-06-02
tags: [article, retrieval, wand, block-max-wand, top-k, information-retrieval, paywalled]
concepts:
  - "[[WAND]]"
  - "[[Block-Max WAND]]"
  - "[[BM25]]"
  - "[[Learning to Rank]]"
  - "[[Sparse Vector Retrieval]]"
topics:
  - "[[Search Platforms]]"
note: "Paywalled — content extracted from publicly visible summary."
---

# WAND and Block-Max WAND: Efficient Algorithms for Top-k Document Retrieval

**Author:** [[Jithendrasaikilaru]]
**Published:** 2025-10-31
**Source:** https://medium.com/@jithendrasaikilaru/wand-and-block-max-wand-efficient-algorithms-for-top-k-document-retrieval-5dfca4b84499

> **Note:** This article is paywalled on Medium. The content below is reconstructed from the publicly visible summary.

An accessible introduction to the two core dynamic pruning algorithms for top-k document retrieval from large inverted indexes: [[WAND]] and [[Block-Max WAND]].

---

## Core Problem

Efficient document retrieval is a central challenge in large-scale information retrieval systems such as web search engines. Scoring every document in a billion-item corpus is impractical — these algorithms identify only the top-k most relevant results by safely skipping candidates that cannot make the final ranking.

## WAND (Weak AND)

[[WAND]], introduced by Broder et al. (2003), is an exact top-k retrieval method. It maintains document pointers across posting lists and identifies a **pivot document** — the smallest document ID where accumulated upper bounds can exceed the current top-k threshold. Documents failing this test are skipped without scoring.

Key properties:
- Exact top-k guarantees (no approximation)
- Operates on inverted indexes with per-term global upper bound scores
- Reduces full score evaluations to a small fraction of the corpus

## Block-Max WAND (BMW)

[[Block-Max WAND]], developed by Ding & Suel (2011), enhances WAND by dividing posting lists into fixed-size blocks with precomputed maximum scores per block. Entire blocks are skipped if their maximum contribution cannot surpass the current k-th threshold.

Key properties:
- Tighter per-block upper bounds → more aggressive skipping than standard WAND
- Block-level and disk I/O-level skipping
- BMW typically outperforms WAND through block-level pruning

## Compared Methods

| Algorithm | Year | Bound granularity | Skipping |
|---|---|---|---|
| MaxScore (Turtle & Flood) | 1995 | Per-term global | Term-level |
| WAND (Broder et al.) | 2003 | Per-term global | Document-level |
| Block-Max WAND (Ding & Suel) | 2011 | Per-block local | Block + document level |

## Advantages

- Reduced score computations at query time
- Scalable with corpus growth
- Guaranteed exact top-k correctness
- Compatible with [[BM25]] and [[Learning to Rank]] frameworks

## Related Concepts

- [[WAND]] — the base dynamic pruning algorithm
- [[Block-Max WAND]] — block-level extension of WAND
- [[BM25]] — the scoring function most commonly paired with these algorithms
- [[Sparse Vector Retrieval]] — broader category these algorithms belong to
- [[Learning to Rank]] — framework these algorithms integrate with

## Related Articles

- [[Faster Retrieval of Top Hits in Elasticsearch with Block-Max WAND]] — [[Adrien Grand]]; deep technical account of Block-Max WAND in Lucene 8 / Elasticsearch 7
- [[BlockMax WAND - How Weaviate Achieved 10x Faster Keyword Search]] — [[André Mourão]], [[Joon-Pil (JP) Hwang]]; Weaviate v1.29 implementation

## People

- [[Jithendrasaikilaru]] — author
