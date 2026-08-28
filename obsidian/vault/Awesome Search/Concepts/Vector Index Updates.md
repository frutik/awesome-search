---
type: concept
title: "Vector Index Updates"
aliases: ["updating a vector database", "HNSW tombstoning", "vector index mutability"]
tags:
  - concept
  - vector-search
  - hnsw
  - ann
created: 2026-08-28
---

# Vector Index Updates

## The Problem

Most [[Vector Search Evaluation|vector search benchmarks]] test only indexing and querying against a static corpus, but production indices "constantly turnover" as data is added, changed, and removed — [[Doug Turnbull]] gives job search and social media as examples where this matters. Updating a vector is usually implemented as an upsert — "a delete-then-insertion" — but deleting a node from an [[HNSW]] graph outright risks leaving navigational gaps, since other nodes' paths may route through it.

## Tombstoning

Rather than restructuring the graph immediately on delete, systems mark the deleted item as a **tombstone**: it stays in the graph and keeps its edges intact for navigation, but is excluded from search results. This defers the cost of graph repair.

## Segmentation and Write-Ahead Logs

Some engines, following a Lucene-style design, avoid mutating a single live graph at all: new insertions first queue in a write-ahead log, then commit into fresh graph segments at configurable intervals, so multiple graph segments coexist and are searched together.

## Vendor Approaches Compared

| Engine | Update strategy |
|---|---|
| [[Vespa]] | Single graph, updated concurrently in place |
| [[Weaviate]] | Tombstoning, no parallel segments |
| Lucene | Write-ahead log + segmented graphs, committed periodically |
| [[Qdrant]] | Mutable insert structure kept separate from the read-optimized graph |
| [[Milvus Vector DB\|Milvus]] | Mutable insert structure kept separate from the read-optimized graph |

## Implication for Benchmarking

Because update strategy varies so much by implementation, [[Doug Turnbull]]'s recommendation is explicit: "Never just insert data and replay thousands of queries." A benchmark that only measures static bulk-load-then-query performance misses how an engine behaves under continuous churn. He recommends shadow-testing against real production traffic patterns and engaging directly with vendor communities to understand each engine's update tradeoffs, rather than trusting simplified static benchmarks.

## Related Concepts

- [[HNSW]] — the graph index structure whose mutability this concept covers
- [[Vector Search Evaluation]] — benchmarking practices this complicates
- [[Vector Search Tradeoffs]] — broader tradeoff space HNSW update behavior sits within

## Companies

- [[Vespa]] · [[Weaviate]] · [[Qdrant]]

## Tools

- [[Milvus Vector DB]]

## Articles

- [[Updating a Vector Database Is No Simple Thing]] — [[Doug Turnbull]]; source for this note

## People

- [[Doug Turnbull]]
