---
type: person
name: Stuart Cam
affiliation: Canva
role: Search & Recommendations Engineer
tags: [person, search-architecture, e-commerce]
created: 2026-05-16
---

# Stuart Cam

Search and Recommendations engineer at **Canva**. Led the architectural overhaul of Canva's search pipeline — migrating from four separate "big ball of mud" codebases to a unified componentized architecture handling ~20,000 req/s.

## Articles

- [[Canva Search Pipeline Part I]] — problem diagnosis, scale facts, requirements
- [[Canva Search Pipeline Part II]] — new architecture, design principles, impact

## Key Contributions

- Componentized pipeline design (Validation → Tokenization → Annotation → Candidate Generation → Feature Extraction → Re-ranking)
- 50ms deadline-based parallel candidate generation
- Technology-agnostic query DSL decoupled from Lucene syntax

## Related

- [[Canva]] · [[Search Architecture]] · [[Retrieval Pipeline]]
