---
title: "The Scaling Dimensions of Keyword Search"
type: article
source: "https://hornet.dev/blog/the-scaling-dimensions-of-keyword-search"
author: "[[Skip Everling]]"
published: 2026-02-06
created: 2026-06-18
concepts: [Agentic Query Workload, Block-Max WAND, WAND, BM25, Sparse Vector Retrieval]
topics: [Current Frontier of Search, Conversational and Agentic Search, Search Platforms]
companies: [Hornet]
people: [Skip Everling]
tags: [article, agentic-search, bm25, block-max-wand, retrieval-efficiency]
---

# The Scaling Dimensions of Keyword Search

A [[Hornet]] benchmark study arguing that **document count is only one scaling dimension** of keyword search — query length and query structure matter just as much, and agents push all three. The headline result: [[Block-Max WAND|BM-WAND]] dynamic pruning, tuned for short human queries, can become *slower than exhaustive scoring* on the long queries agents generate.

---

## Three Scaling Dimensions

Search engine design was shaped by human behavior. The [AOL search log](https://en.wikipedia.org/wiki/AOL_search_log_release) (36M queries, 650k users) shows:

| Metric | Value |
|---|---|
| Mean query length | 2.46 terms |
| Median query length | 2 terms |
| 90th percentile | 5 terms |
| 99th percentile | 8 terms |

Nearly two-thirds of searches are two words or fewer. Agents flip this: they emit long, structured, natural-language queries — see the companion piece [[This Is What Agentic Retrieval Looks Like]].

## How Keyword Engines Got Fast

- **Inverted index** — per-term sorted docID lists, replacing linear brute-force (grep-style) scans.
- **Disjunctive (OR) query processing** — merge posting lists, accumulate scores, return top-k.
- **Dynamic pruning** — return the exact top-k *without* scoring every matching doc. Lineage: [[WAND]] (Broder et al., 2003) → built on MaxScore (Turtle & Flood, 1995) → [[Block-Max WAND]] (Ding & Suel, 2011), adopted in Lucene 8.0 (2019), powering Elasticsearch, OpenSearch, and Solr.

The hidden assumption: **queries are short.** These algorithms were tuned for a world where 90% of queries are four words or fewer.

## Where the Optimization Breaks

Benchmarks on [Tantivy](https://github.com/quickwit-oss/tantivy) 0.25 (SIMD posting lists, Block-Max WAND, BM25) over Wikipedia (1M–5M docs, 1–20 terms):

- **Random-term queries:** for 1–5 terms BM-WAND scales sub-linearly (great). But at ~7.5 terms on a 5M-doc index it crosses *over* exhaustive search. At 20 terms it takes ~58ms/query vs ~12ms exhaustive. With many terms, most docs match at least one term, so the pruning condition rarely fires and the algorithm spends more time on bookkeeping than it saves.
- **Real queries (Google [Natural Questions](https://ai.google.com/research/NaturalQuestions), avg 9 terms):** BM-WAND stays 1.5–2x faster than exhaustive across all lengths (18ms vs 36ms at 8 terms). The difference is **query term weight distribution** — real queries have a few high-IDF discriminating terms that let BM-WAND establish a high score threshold early and skip aggressively. Synthetic uniform-weight queries defeat this mechanism.

## Latency Is a Proxy for Cost

A 60ms query burns ~5x the CPU cycles of a 12ms query. At thousands of agent queries per minute, choosing the wrong algorithm is a direct cost multiplier; cost scales with both document count and term count.

## Why It Matters for Agents

- **Query length** — human median 2 terms; agent queries routinely 8–15 terms, the human 99th percentile.
- **Query volume** — a human issues dozens of queries per session; an autonomous agent testing hypotheses may issue thousands, ~100x, compounding with complexity.

The conclusion is not that dynamic pruning is broken, but that algorithms must **adapt to query characteristics** — selecting scoring strategy by query structure. This is the retrieval-engine-for-agents thesis Hornet is building toward.

---

## Related Concepts
- [[Agentic Query Workload]] — the demand-shape shift this article quantifies on the serving side
- [[Block-Max WAND]] — the pruning algorithm that degrades on long uniform-weight queries
- [[WAND]] — parent algorithm
- [[BM25]] — the scoring model being pruned

## Related Articles
- [[This Is What Agentic Retrieval Looks Like]] — companion piece on the query side (this one is the serving side)
- [[Agentic Search Models with OpenSearch and Elasticsearch]] — the multi-turn querying that generates this workload
- [[Faster Retrieval of Top Hits in Elasticsearch with Block-Max WAND]] — Lucene/Elasticsearch's BM-WAND adoption

## People
- [[Skip Everling]]

## Companies
- [[Hornet]]

## Topics
- [[Current Frontier of Search]]
- [[Conversational and Agentic Search]]
