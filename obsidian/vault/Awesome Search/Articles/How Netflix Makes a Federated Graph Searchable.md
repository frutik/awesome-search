---
title: "How Netflix Content Engineering Makes a Federated Graph Searchable"
tags:
  - clippings
  - search
  - case-study
  - knowledge-graph
  - architecture
source: "https://netflixtechblog.com/how-netflix-content-engineering-makes-a-federated-graph-searchable-5c0c1c7d7eaf"
author: "Netflix Technology Blog"
created: 2026-05-15
concepts:
  - Knowledge Graph Search
  - Dense Vector Retrieval
  - Search Architecture
---

# How Netflix Content Engineering Makes a Federated Graph Searchable

**Source:** [Part 1](https://netflixtechblog.com/how-netflix-content-engineering-makes-a-federated-graph-searchable-5c0c1c7d7eaf) | [Part 2](https://netflixtechblog.com/how-netflix-content-engineering-makes-a-federated-graph-searchable-part-2-49348511c06c)
**Author:** Netflix Content Engineering team

## Summary

Two-part series on how Netflix makes their federated content knowledge graph searchable. Covers the challenges of searching across a distributed graph of entities (movies, shows, people, studios) and the architecture that supports it.

## Core Problem

Netflix's content catalog is represented as a federated graph — a distributed system where different teams own different entity types (titles, talent, studios, rights). Making this searchable requires:
1. Aggregating entities across graph partitions
2. Representing relationships, not just leaf documents
3. Supporting both keyword and semantic queries over structured entity data

## Key Architecture Concepts

### Graph as Search Index
- Entities (movies, shows, people, studios) become indexed documents
- Relationships (actor → movie, director → studio) enriched as document features
- Graph traversals materialized as pre-computed search signals

### Federated Query Routing
- Sub-queries routed to appropriate graph partition owners
- Results merged at the search orchestration layer

### Vector Embeddings for Entities
- Entity embeddings capture semantic relationships from graph neighborhood
- Enable similarity search across entity types ("movies similar to X")

## Two-Part Series

- **Part 1**: Challenges and motivation — why traditional search fails for federated graphs
- **Part 2**: New architecture — embedding entities, federated query execution, search indexing

## Related Concepts

- [[Knowledge Graph Search]]
- [[Dense Vector Retrieval]]
- [[Search Architecture]]
- [[Retrieval Pipeline]]
- [[Personalization]]

## Related Articles

- [[Canva Search Pipeline Part I]]
- [[Search at Slack]]
