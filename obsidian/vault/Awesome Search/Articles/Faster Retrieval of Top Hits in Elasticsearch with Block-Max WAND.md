---
title: "Faster Retrieval of Top Hits in Elasticsearch with Block-Max WAND"
type: article
source: "https://www.elastic.co/blog/faster-retrieval-of-top-hits-in-elasticsearch-with-block-max-wand"
author:
  - "[[Adrien Grand]]"
published: 2019-02-05
created: 2026-06-02
tags: [article, retrieval, block-max-wand, elasticsearch, lucene, performance]
concepts:
  - "[[Block-Max WAND]]"
  - "[[WAND]]"
  - "[[BM25]]"
  - "[[Sparse Vector Retrieval]]"
topics:
  - "[[Search Platforms]]"
company:
  - "[[Elastic]]"
---

# Faster Retrieval of Top Hits in Elasticsearch with Block-Max WAND

**Author:** [[Adrien Grand]] ([[Elastic]])
**Published:** 2019-02-05

[[Block-Max WAND]] was introduced into Lucene 8.0 and Elasticsearch 7.0 by [[Adrien Grand]], delivering 3x–15x speedups for top-k retrieval. The post traces the algorithm's lineage from MAXSCORE (1995) through WAND (2003) to block-max indexes (2011).

---

## Background: MAXSCORE to WAND

**MAXSCORE** (H. Turtle & J. Flood, 1995) was presented by Stefan Pohl at Berlin Buzzwords 2012. It splits query terms into two sets: *essential* (find candidates) and *non-essential* (only used for scoring). As the minimum competitive score rises, low-max-score terms move from essential to non-essential, reducing the document space to search.

Stefan opened a Lucene JIRA ticket with a prototype. The main challenge: computing per-term max scores on dynamic (non-static) indexes requires rewriting segments on every new document. This blocked integration for **5 years**.

**WAND** (Broder et al., 2003) became feasible when Lucene switched to [[BM25]] as its default, because BM25 scores are naturally bounded. Rather than two sets, WAND maintains one set with per-term weights (max scores) and skips documents where the sum of weights falls below the threshold. More granular than MAXSCORE.

Initial WAND implementation gave **40%–13x speedup** for disjunctions on Lucene benchmarks.

## Block-Max WAND

WAND's limitation: a single high-scoring outlier document inflates the global max score for a term, reducing skipping efficiency. A 2011 paper by S. Ding and T. Suel (NYU) introduced block-max indexes and [[Block-Max WAND]]: split postings into fixed-size blocks, record the max impact score *per block*.

**Elastic's implementation** stores (tf, document_length) per block rather than raw impact scores. Benefits:
- Works with any scoring function using per-document statistics: TF-IDF, BM25, divergence from randomness
- Users can switch similarity at search time without reindexing (as long as document length encoding is the same)

**Benchmark results** (Lucene benchmark suite):
- Term queries: **3x–7x faster**
- Conjunctions: **3%–7x faster**
- Disjunctions: **-8% to 15x faster** (slight regression in some cases)

See [Lucene nightly benchmarks](http://people.apache.org/~mikemccand/lucenebench/) annotation CJ for term queries and disjunctions.

## API Changes in Elasticsearch 7.0

Block-Max WAND required two breaking API changes:

1. **Scores may no longer be negative** — required for upper-bound pruning to be safe
2. **Total hit count no longer always accurate** — `hits.total` changed from an integer to:
   ```json
   { "value": 1000, "relation": "gte" }
   ```

The `track_total_hits` parameter controls accuracy vs. speed trade-off: lower value → faster query. Lucene still supports accurate counts on request, at a performance cost (must visit all matches).

**Aggregations are not affected** by this optimization — they must visit all matches regardless.

## Related Concepts

- [[Block-Max WAND]] — the algorithm introduced
- [[WAND]] — predecessor algorithm
- [[BM25]] — scoring model that enabled WAND on dynamic indexes
- [[Sparse Vector Retrieval]] — broader category
- [[Retrieval Pipeline]]

## People

- [[Adrien Grand]]
