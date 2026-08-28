---
type: article
title: "Updating a Vector Database Is No Simple Thing"
source: "https://softwaredoug.com/blog/2026/08/18/update-graph-vector-db.html"
author:
  - "[[Doug Turnbull]]"
published: 2026-08-18
created: 2026-08-28
concepts:
  - "[[HNSW]]"
  - "[[Vector Index Updates]]"
topics: []
companies:
  - "[[Vespa]]"
  - "[[Weaviate]]"
  - "[[Qdrant]]"
tags:
  - article
  - vector-search
  - hnsw
  - company-blog
---

# Updating a Vector Database Is No Simple Thing

[[Doug Turnbull]] argues that vector search benchmarks typically oversimplify the problem by testing only indexing and querying against static data — in real applications like job search or social media, indices "constantly turnover" as records are added, changed, and removed.

## The Core Problem: Updating a Graph Index

[[HNSW]] indexes are graphs connecting similar vectors to enable navigational search. Most implementations treat a vector update as an upsert — Turnbull describes it as "an upsert: a delete-then-insertion." Deleting a node outright would risk leaving gaps in graph connectivity, so systems instead **tombstone** — marking an item deleted while keeping its graph edges intact for navigation — rather than restructuring the graph immediately.

## Segmentation and Write-Ahead Logs

Some databases, following a Lucene-style design, keep multiple graph segments simultaneously: new insertions first queue in a write-ahead log, then commit into fresh graph segments at configurable intervals, rather than mutating one graph directly.

## How Vendors Differ

The article compares implementation choices across engines:
- [[Vespa]] maintains a single graph that is concurrently updated in place.
- [[Weaviate]] uses tombstoning without maintaining parallel segments.
- Lucene, [[Qdrant]], and [[Milvus Vector DB|Milvus]] use a mutable insert structure kept separate from the read-optimized graph.

## Recommendation: Don't Trust Static Benchmarks

Turnbull's central caution: "Never just insert data and replay thousands of queries." Because update behavior varies so much by implementation, he recommends shadow-testing against real production traffic patterns, engaging directly with vendor communities, and understanding the tradeoffs of each engine's update strategy rather than relying on benchmarks that only measure static indexing and querying.

## Related Concepts

- [[HNSW]] — the graph index structure whose update behavior is the article's subject
- [[Vector Index Updates]] — tombstoning, segmentation, and vendor comparison synthesized from this article

## Companies

- [[Vespa]] · [[Weaviate]] · [[Qdrant]]

## Tools

- [[Milvus Vector DB]]

## People

- [[Doug Turnbull]]
