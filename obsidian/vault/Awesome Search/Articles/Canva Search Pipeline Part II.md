---
title: "Canva Search Pipeline Part II"
tags:
  - clippings
  - search
  - architecture
  - case-study
source: "https://canvatechblog.com/search-pipeline-part-ii-3b43978607cd"
author: "Stuart Cam"
created: 2026-05-15
concepts:
  - Search Architecture
  - Retrieval Pipeline
---

# Canva Search Pipeline Part II

**Source:** https://canvatechblog.com/search-pipeline-part-ii-3b43978607cd
**Author:** [[Stuart Cam]] (Canva Search & Recommendations team)

## Summary

Describes the new componentized pipeline [[Search Architecture]] that replaced Canva's big ball of mud. Core principle: isolated, stateless, immutable pipeline phases with a shared interface.

## New Architecture: Pipeline Phases

```
Validation & Rewriting
    ↓
Tokenization (locale-specific + semantic)
    ↓
Annotation (NER, language detection, synonyms)
    ↓
Candidate Generation (OpenSearch, Solr, SageMaker — parallel)
    ↓
Feature Extraction (Redis-backed feature stores)
    ↓
Re-ranking (business rules + ML models)
```

## Key Design Principles

- **Isolated components**: no shared state between concurrent steps
- **Stateless execution**: state managed externally (Redis/DynamoDB)
- **Immutable flow**: previous steps cannot be mutated by later steps
- **Shared interface**: all pipeline types expose the same abstract interface

## ML & Performance Optimizations

- **Parallel candidate generators** with deadline-based execution
- **50ms deadline** — generate as many candidates as possible; stop at deadline
- **Pagination strategy**: overFetch top 500 results for early pages (precision priority); faster execution for deep pages (bot handling)

## Design Process

Collaborative prototyping — each engineer tackled an architecture area they cared about; consolidated outputs into initial design.

## Impact

Enabled migration of audio, font, video, and media search to shared architecture. "A shared mental model is key to limiting inaccuracies and contradictions."

## Related Concepts

- [[Search Architecture]]
- [[Retrieval Pipeline]]
- [[Learning to Rank]]
- [[Personalization]]

## People

- [[Stuart Cam]] (Canva)

## Related Articles

- [[Canva Search Pipeline Part I]]
