---
title: "Block-Max WAND"
aliases: ["BlockMax WAND", "BMW", "Block-Max Weak AND", "block-max indexes", "block-max WAND"]
tags: [concept, retrieval, sparse-retrieval, efficiency, bm25, lucene]
type: concept
---

# Block-Max WAND

## Definition

Block-Max WAND (BMW) is an enhancement of the [[WAND]] (Weak AND) algorithm that divides posting lists into fixed-size blocks, each with its own local maximum impact score. This allows more aggressive document skipping than global-upper-bound WAND — both at block level (skip whole blocks) and at disk I/O level (avoid loading irrelevant blocks entirely).

Introduced in a 2011 paper by S. Ding and T. Suel (NYU). Implemented in Lucene 8.0 / Elasticsearch 7.0 (2019) and Weaviate v1.29 (2025).

## Why It Improves on WAND

Standard [[WAND]] assigns one global upper-bound score per term — typically the IDF. This bound is set by the single highest-scoring document for that term. A single outlier inflates the bound and reduces skipping efficiency.

Block-Max WAND fixes this by storing a *per-block* max impact instead of a global one. Blocks with no high-scoring outliers get tighter bounds, enabling safe skips that WAND would miss.

## How It Works

1. Divide each posting list into fixed-size blocks (e.g., 128 docs/block)
2. Store per-block metadata: **max doc ID** and **max impact score**
3. During top-k retrieval:
   - At block level: skip blocks whose max impact is below the current k-th score (**shallow advance**)
   - Avoid loading blocks from disk entirely if they cannot contribute (**deep block skip**)
   - Within promising blocks: apply standard WAND pruning per document

## Block Structure

Each block stores:
- **doc IDs** — delta encoded + varenc compressed
- **term frequencies (tf)** — varenc compressed
- **block metadata** (separate structure): max doc ID, max impact score — used to filter blocks before decoding

## Compression

Block boundaries also enable efficient compression:
- **Delta encoding**: store differences between consecutive doc IDs (small deltas → fewer bits)
- **Varenc (variable-length encoding)**: use only the bits needed to represent the maximum value in each block

Combined, Weaviate reports **50–90% index size reduction** on standard BEIR datasets.

## Performance

| System | Metric | WAND | Block-Max WAND |
|---|---|---|---|
| Weaviate v1.29 | MS Marco p50 | 136 ms | 27 ms (-80%) |
| Weaviate v1.29 | Fever p50 | 517 ms | 33 ms (-94%) |
| Weaviate v1.29 | Docs inspected | 15–30% | 5–15% (-50%) |
| Lucene 8 / ES 7 | Term queries | baseline | 3x–7x faster |
| Lucene 8 / ES 7 | Disjunctions | baseline | up to 15x faster |

## Implementations

- **Lucene 8.0 / Elasticsearch 7.0** — [[Adrien Grand]] (Elastic), 2019. Stores (tf, doc_length) per block for scoring-function flexibility. Required breaking API changes: no negative scores, hit counts approximate by default (`track_total_hits`)
- **Weaviate v1.29** — [[André Mourão]] and [[Joon-Pil (JP) Hwang]], 2025. Technical preview. 128-doc blocks with delta encoding + varenc compression
- **Apache Solr** — via shared Lucene codebase

## Papers

- Broder et al. (2003) — original WAND algorithm — [ACM DL](https://dl.acm.org/doi/abs/10.1145/956863.956944)
- Ding & Suel (2011) — block-max indexes — [ACM DL](https://dl.acm.org/doi/10.1145/2009916.2010048), [PDF](http://engineering.nyu.edu/~suel/papers/bmw.pdf)

## Related Concepts

- [[WAND]] — parent algorithm; Block-Max WAND is a refinement
- [[BM25]] — the scoring model most commonly paired with block-max indexes
- [[Sparse Vector Retrieval]] — broader category
- [[Retrieval Pipeline]] — Block-Max WAND serves first-stage retrieval

## Related Articles

- [[BlockMax WAND - How Weaviate Achieved 10x Faster Keyword Search]]
- [[Faster Retrieval of Top Hits in Elasticsearch with Block-Max WAND]]
- [[Mirror Mirror - All About Search Suggestions]] — mentions block-max WAND in the context of `search_as_you_type`
- [[WAND and Block-Max WAND - Efficient Algorithms for Top-k Document Retrieval]] — [[Jithendrasaikilaru]]; introductory comparison of WAND and BMW with algorithm lineage from MaxScore
