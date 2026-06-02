---
title: "BlockMax WAND: How Weaviate Achieved 10x Faster Keyword Search"
type: article
source: "https://weaviate.io/blog/blockmax-wand"
author:
  - "[[André Mourão]]"
  - "[[Joon-Pil (JP) Hwang]]"
published: 2025-02-26
created: 2026-06-02
tags: [article, retrieval, block-max-wand, weaviate, performance, compression, inverted-index]
concepts:
  - "[[Block-Max WAND]]"
  - "[[WAND]]"
  - "[[BM25]]"
  - "[[Hybrid Search]]"
  - "[[Sparse Vector Retrieval]]"
topics:
  - "[[Search Platforms]]"
company:
  - "[[Weaviate]]"
---

# BlockMax WAND: How Weaviate Achieved 10x Faster Keyword Search

**Authors:** [[André Mourão]], [[Joon-Pil (JP) Hwang]] ([[Weaviate]])
**Published:** 2025-02-26

Weaviate implemented [[Block-Max WAND]] as a technical preview in v1.29, achieving p50 query speedups of 5–10x and index size reductions of 50–90% over their existing [[WAND]]-based keyword search.

---

## Problem

As text corpora grow, keyword search latency increases relative to vector search. Even with WAND already reducing documents inspected from 100% to 15–30%, there was significant headroom for further optimization. Keyword search is a core leg of [[Hybrid Search]] for RAG and agentic AI.

## Key Concepts

### Inverted Index and Tokenization

Documents are tokenized (whitespace, lowercase, etc.) and stored in posting lists mapping term → (doc_id, tf). Exhaustive scoring requires visiting every document with at least one query term — wasteful for top-k queries that only need 10–100 results.

### WAND (existing approach)

[[WAND]] uses global per-term IDF upper bounds to skip documents that cannot beat the current k-th score. Reduces documents inspected from 100% to 15–30% on standard benchmarks.

### Block-Max WAND

[[Block-Max WAND]] (BMW) further refines this by dividing posting lists into fixed blocks (128 docs/block in Weaviate), each with local max impact metadata:

- **Shallow advances**: skip entire blocks without decoding doc IDs, using block-level max impact
- **Deep block skipping**: avoid loading blocks from disk entirely when they cannot beat the threshold
- Reduces documents inspected from 15–30% (WAND) to **5–15%** — roughly halving WAND's work

| Dataset | WAND % scored | BMW % scored | Reduction |
|---|---|---|---|
| MS Marco (8.6M docs) | 15.1% | 6.7% | -56% |
| Fever (5.4M docs) | 20.8% | 8.4% | -60% |
| Climate Fever (5.4M docs) | 29.3% | 12.2% | -58% |

## Compression

Block storage also enables aggressive compression:

**varenc (variable-length encoding):** store only the minimum bits needed to represent the max value in each block.

**Delta encoding (doc IDs):** store differences between consecutive doc IDs. Consecutive IDs in a sorted posting list are close together, producing small deltas that compress well.

Combined result: **50–90% reduction in index size** depending on data distribution.

| Dataset | WAND index | BMW index | Reduction |
|---|---|---|---|
| MS Marco (8.6M docs) | 10531 MB | 941 MB | -91% |
| Fever/Climate Fever (5.4M docs) | 9326 MB | 1175 MB | -87% |

## Query Time Results

| Dataset | WAND p50 | BMW p50 | Reduction |
|---|---|---|---|
| MS Marco (8.6M docs) | 136 ms | 27 ms | -80% |
| Fever (5.4M docs) | 517 ms | 33 ms | -94% |
| Climate Fever (5.4M docs) | 712 ms | 87 ms | -88% |

At 100M documents: scaled from 1 to 50 QPS while maintaining p50 100–200ms, p99 ≤1000ms.

## Status and Availability

Available in Weaviate **v1.29** as a **technical preview**. Requires:
- New collections (no transparent migration for existing data yet)
- Specific env vars enabled

Not recommended for production environments. Weaviate is developing a transparent migration path.

## Related Concepts

- [[Block-Max WAND]]
- [[WAND]]
- [[BM25]]
- [[Hybrid Search]]
- [[Sparse Vector Retrieval]]

## People

- [[André Mourão]]
- [[Joon-Pil (JP) Hwang]]
