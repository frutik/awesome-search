---
title: "Knowledge Graph Search"
aliases: ["knowledge graph", "entity search", "graph-based search", "federated graph search"]
tags:
  - concept
  - search
  - architecture
created: 2026-05-15
---

# Knowledge Graph Search

Search infrastructure that represents entities and their relationships as a graph, enabling structured navigation and semantic retrieval beyond keyword matching.

## Core Idea

A knowledge graph stores:
- **Entities** — people, places, things (nodes)
- **Relationships** — typed edges connecting entities
- **Properties** — attributes of entities

Search over a knowledge graph enables:
- Entity disambiguation ("Apple" the company vs. the fruit)
- Relationship traversal ("movies with actors who worked with Spielberg")
- Faceted filtering from structured data

## Making a Graph Searchable

Netflix's approach (federated graph):
1. **Graph construction** — ingest structured metadata into entity nodes
2. **Embedding entities** — represent nodes as vectors for similarity search
3. **Federated queries** — route sub-queries to appropriate graph partitions
4. **Materialized views** — pre-compute common traversals for latency

## Graph + Vector Integration

Modern systems combine:
- Vector similarity for semantic retrieval
- Graph traversal for relational filtering
- The intersection: embed graph neighborhoods, not just leaf documents

## Industry Examples

- **Netflix**: federated content graph searchable via vector embeddings
- **LinkedIn**: entity graph for people/job/company search
- **Google Knowledge Panel**: structured entity data surfacing

## Related Concepts

- [[Dense Vector Retrieval]]
- [[Semantic Search]]
- [[Faceted Search]]
- [[Retrieval Pipeline]]
- [[Personalization]]
