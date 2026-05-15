---
title: "Canva Search Pipeline Part I"
tags:
  - clippings
  - search
  - architecture
  - case-study
source: "https://canvatechblog.com/search-pipeline-part-i-faa6c543aef1"
author: "Stuart Cam"
created: 2026-05-15
concepts:
  - Search Architecture
---

# Canva Search Pipeline Part I

**Source:** https://canvatechblog.com/search-pipeline-part-i-faa6c543aef1
**Author:** Stuart Cam (Canva Search & Recommendations team)
**Published:** November 2022

## Summary

First part of Canva's search architecture overhaul. Describes the problems with their organically-grown "big ball of mud" architecture and motivates the redesign. Scale: ~20,000 requests/second at peak, 50+ unique entry points.

## The Problem: Big Ball of Mud

Organic growth produced 4 separate search systems for templates, media, audio, and fonts — each with distinct codebases. The systems passed `SolrQuery` builder objects via string manipulation, locking them into Lucene syntax and blocking integration of new technologies (dense vectors, ML ranking).

## Key Scale Facts

- **~20,000 requests/second** at peak (public content search)
- **~50 unique entry points** into search systems
- **70% of queries** are single words ("cat", "dog")
- **20% contain two words**
- Users rarely engage past position 240 in results
- Single-character queries common for CJK languages

## Requirements for New System

1. ML integration for ranking and [[Personalization]]
2. Support for both search and recommendation queries
3. Technology-agnostic query DSL (not tied to Solr syntax)
4. Enhanced debugging and observability
5. Unified architecture across 4 content types

## Team Context

~80 engineers across: ML, data science, backend, frontend, operations.

## Related Concepts

- [[Search Architecture]]
- [[Learning to Rank]]
- [[Personalization]]
- [[Retrieval Pipeline]]

## People

- Stuart Cam (Canva)

## Related Articles

- [[Canva Search Pipeline Part II]]
