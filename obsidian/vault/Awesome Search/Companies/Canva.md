---
type: company
category: end-user
industry: [design, SaaS, creative tools]
products: [Canva (design platform), template search, media search, font search]
search_domain: creative asset search (templates, photos, audio, fonts, video)
scale: ~20,000 req/s peak, 50+ unique entry points, 70% single-word queries
use_cases: ["[[Canva - Componentized Search Pipeline]]"]
people: ["[[Stuart Cam]]"]
tags: [company, end-user, design, search-architecture]
created: 2026-05-16
---

# Canva

Design platform used by 150M+ people. Search powers discovery of templates, photos, audio, fonts, and video across a massive creative asset catalog.

## Search Context

Canva's search challenge is breadth: four fundamentally different content types (templates, media, audio, fonts) originally had four separate search codebases. The team rebuilt all of them on a shared componentized architecture.

**Scale**: ~20,000 requests/second at peak. 70% of queries are single words ("cat", "dog"). 20% are two words. Single-character queries common for CJK languages.

## Key Engineering Work

- Migrated from "big ball of mud" (4 separate Solr/custom codebases) to shared pipeline architecture
- New pipeline: Validation → Tokenization → Annotation → Candidate Generation → Feature Extraction → Re-ranking
- **50ms deadline-based candidate generation**: parallel generators, return top-500 for early pages; lighter execution for deep pages
- Technology-agnostic query DSL decoupled from Lucene syntax
- Enabled ML integration for ranking and personalization across all 4 content types

## Articles

- [[Canva Search Pipeline Part I]] — problem statement, scale, requirements
- [[Canva Search Pipeline Part II]] — new architecture, design principles, impact

## Related Concepts

- [[Search Architecture]] · [[Retrieval Pipeline]] · [[Learning to Rank]] · [[Personalization]]
