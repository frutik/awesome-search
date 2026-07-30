---
title: "Hybrid Search"
aliases: ["hybrid retrieval", "sparse-dense fusion", "multi-vector search"]
type: concept
tags:
  - concept
  - search
  - retrieval
created: 2026-05-01
---

# Hybrid Search

## Definition

Hybrid search combines two or more retrieval signals — most commonly sparse (lexical/term-based) and dense (semantic/embedding-based) — to produce results that outperform either approach alone.

The intuition: sparse retrieval excels at exact keyword matching; dense retrieval excels at semantic understanding. Their failure modes are largely complementary.

[[Erik Hatcher]] ([[MongoDB]]) offers a practitioner's definition that widens the frame beyond
sparse+dense: *combining two or more search techniques to produce results better than any single
technique alone*. The operative word is **better** — which makes measurement a precondition rather
than a follow-up, and yields the series mantra **measure, tune, repeat**. On this reading "hybrid"
is a mindset of blending rather than a prescriptive recipe, and it retroactively covers the older
practice of folding behavioral signals and learned rules into a query, not just fusing two ranked
lists. See [[Survey of the Hybrid Search Landscape]].

### The rankability spectrum

Hatcher orders the available techniques by **rankability** — how readily the query-document
relationship can be given a numeric score:

| Technique | Rankability |
|---|---|
| Key/value matching (B-Tree, exact + range) | None intrinsically — binary match; proximity can be computed |
| [[Dense Vector Retrieval\|Vector search]] | Geometric distance; embedding model choice is the dominant relevancy factor |
| [[Full-Text Search\|Lexical search]] | Richest — field weights, term and document frequencies, per-clause formulas |

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
Requires score normalization (scores from different systems aren't comparable). Skipping the
normalization step is a live production failure mode, not a theoretical one — see the warning
under *Implementation in Elasticsearch* below.

### Re-ranking
Retrieve N candidates from each system → merge → re-rank with [[Cross-Encoder]].

### Learning-to-Rank Fusion
Treat each retriever's score (BM25, cosine) as an input feature to a [[LambdaMART]] / [[Learning to Rank|LTR]] model trained on click feedback — the model learns the optimal combination, and decision trees handle missing scores when a document came from only one retriever. [[Metarank]] is an open-source secondary re-ranker built for exactly this; [[Interleaving]] provides the cold-start baseline ranking used to collect the initial click data.

- See: [[Hybrid Search and Learning-to-Rank with Metarank]] — [[Vsevolod Goloviznin]] ([[Pinecone]])

## Common Implementations

### SPLADE + Bi-Encoder
- [[SPLADE]] for learned sparse retrieval (term expansion)
- [[Bi-Encoder]] (e.g., sentence-transformers) for dense semantic
- Fusion: RRF or learned combiner

### BM25 + Dense
- BM25 for lexical baseline (no ML required)
- Dense encoder for semantic lift
- Popular in production (Elasticsearch, OpenSearch)

### PostgreSQL (single datastore)
- Lexical: native [[Full-Text Search]] (`ts_rank`) or [[ParadeDB]] [[BM25]]
- Semantic: [[pgvector]] ([[HNSW]])
- Fusion: [[Reciprocal Rank Fusion|RRF]] expressed directly in SQL
- See [[Search using PostgreSQL]]

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

> [!warning] A `bool`/`should` merge sums raw scores — it does not normalize
> In a `bool` query, a document matching several `should` clauses scores the **sum** of those
> clauses. The engine does not normalize across clauses; it adds whatever each one emits. So the
> effective ranking function above is `BM25 + second_clause_score`, on whatever scales those two
> happen to occupy.
>
> The mismatch is starkest when the second clause is a bounded **`knn`** clause: BM25 is unbounded —
> it rises with term frequency, term rarity and shortness, with no ceiling — while cosine-derived
> vector scores sit in a narrow band typically well under 1. Summed, the unbounded branch can decide
> the ranking outright and the vector branch stops participating.
>
> Do not read the example above as safe merely because both clauses are term-based. [[ELSER]]
> `text_expansion` scores are sums of learned term weights and are not bounded either, and two
> unbounded scores are still not two *calibrated* scores — they need normalizing just as much, only
> with a less dramatic failure when you skip it.
>
> This fails silently: the query compiles, returns a single `_score`, and looks correct. Prefer the
> engine's purpose-built hybrid query with a normalization pipeline (see [[OpenSearch]]), or
> normalize explicitly before weighting ([[Linear Score Combination]]).
>
> Worked example and diagnostics:
> [[Hybrid Fusion Failure - BM25 Displacing Reference Documents]].

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
- [[Interleaving]] — score-free merge + cold-start baseline
- [[Learning to Rank]] / [[LambdaMART]] — learned fusion of retriever scores
- [[Metarank]] — open-source LTR re-ranker for multi-retriever fusion
- [[Full-Text Search]] — the lexical leg
- [[PostgreSQL]] / [[pgvector]] / [[ParadeDB]] — hybrid search in a single datastore

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
- See: [[Reciprocal Rank Fusion and Relative Score Fusion]] — RRF and RSF worked through with full arithmetic
- See: [[Score Normalization]] — the step that decides whether score-based fusion works at all
