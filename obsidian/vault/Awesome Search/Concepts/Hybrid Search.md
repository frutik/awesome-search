---
title: "Hybrid Search"
aliases: ["hybrid retrieval", "sparse-dense fusion", "multi-vector search"]
tags:
  - concept
  - search
  - retrieval
---

# Hybrid Search

## Definition

Hybrid search combines two or more retrieval signals — most commonly sparse (lexical/term-based) and dense (semantic/embedding-based) — to produce results that outperform either approach alone.

The intuition: sparse retrieval excels at exact keyword matching; dense retrieval excels at semantic understanding. Their failure modes are largely complementary.

## Why Combine?

| Retrieval Type | Strengths | Weaknesses |
|---------------|-----------|------------|
| Sparse (BM25/[[SPLADE]]) | Exact terms, proper nouns, codes | Vocabulary mismatch, no synonyms |
| Dense ([[Bi-Encoder]]) | Semantics, paraphrases, intent | Weak on rare terms, slower |
| **Hybrid** | **Best of both** | More complex, harder to tune |

## Fusion Strategies

### Reciprocal Rank Fusion (RRF)
Most common, parameter-free:
```
RRF_score(d) = Σ 1 / (k + rank_i(d))
```
where k=60 is a constant that smooths rank differences.

**Advantages**: No score normalization needed, robust, no training required.

### Linear Score Combination
```
final_score = α × sparse_score + (1 − α) × dense_score
```
Requires score normalization (scores from different systems aren't comparable).

### Re-ranking
Retrieve N candidates from each system → merge → re-rank with [[Cross-Encoder]].

## Common Implementations

### SPLADE + Bi-Encoder
- [[SPLADE]] for learned sparse retrieval (term expansion)
- [[Bi-Encoder]] (e.g., sentence-transformers) for dense semantic
- Fusion: RRF or learned combiner

### BM25 + Dense
- BM25 for lexical baseline (no ML required)
- Dense encoder for semantic lift
- Popular in production (Elasticsearch, OpenSearch)

### Vespa Hybrid
- Native [[ColBERT]] + BM25 hybrid in Vespa
- [[Jo Kristian Bergum]]'s work on ColBERT embedder

## Implementation in Elasticsearch

```python
# Two-phase: BM25 + ELSER (sparse) or BM25 + dense
GET /products/_search
{
  "query": {
    "bool": {
      "should": [
        {"match": {"text": "query"}},           # BM25
        {"text_expansion": {                     # ELSER sparse
          "ml.tokens": {"model_id": ".elser_model_1", "model_text": "query"}
        }}
      ]
    }
  }
}
```

## Wormhole Vectors as Hybrid Bridge

[[Trey Grainger]]'s [[Wormhole Vectors]] concept extends hybrid search by identifying vectors that bridge multiple retrieval spaces (sparse, dense, behavioral). A document traverses from one space to another through these "wormhole" connections.

- See also: [[Wormhole Vectors Beyond Hybrid Search in OpenSearch]] — [[Dima Kan]]'s production implementation at Aiven

## Related Concepts
- [[Dense Embeddings]] — the dense leg of hybrid search
- [[Sparse Embeddings]] — the sparse leg of hybrid search

- [[Sparse Vector Retrieval]] — one leg of hybrid
- [[Dense Vector Retrieval]] — the other leg
- [[SPLADE]] — preferred learned sparse component
- [[ELSER]] — Elastic's sparse model for hybrid
- [[Bi-Encoder]] — preferred dense component
- [[ColBERT]] — alternative dense component with late interaction
- [[Wormhole Vectors]] — advanced multi-space traversal
- [[RAG]] — downstream use of hybrid retrieval

## People

- [[Trey Grainger]] — Wormhole Vectors, multi-space traversal
- [[James Briggs]] — Hybrid SPLADE articles at Pinecone
- [[Jo Kristian Bergum]] — Vespa hybrid search, ColBERT embedder
- [[Stéphane Clinchant]] — SPLADE, sparse component

- [[Bayesian BM25 is Cool]]

- [[Bayesian BM25]]

## Semantic Boosting

[[Semantic Boosting]] is a two-phase alternative to RRF/RSF fusion: run vector search first, inject the results as boost clauses into a final lexical query. The output comes entirely from the lexical engine, so faceting, highlighting, and pagination work natively without extra merging.

- See: [[Hybrid Search Blueprint Series Semantic Boosting]] — [[Erik Hatcher]] ([[MongoDB]])
- See: [[Relative Score Fusion]] — score-normalization-based fusion, contrasted with RRF
