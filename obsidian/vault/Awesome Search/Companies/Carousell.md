---
type: company
category: end-user
industry: [e-commerce, C2C marketplace, Southeast Asia]
products: [Carousell marketplace, Spotlight (sponsored search)]
search_domain: C2C marketplace search, multilingual Southeast Asian market
use_cases: ["[[Carousell - Dense Vector Migration for Spotlight]]"]
tags: [company, end-user, e-commerce, c2c, multilingual, dense-vectors]
created: 2026-05-16
---

# Carousell

Southeast Asian C2C marketplace operating in Singapore, Malaysia, Philippines, Indonesia, and other markets. Search challenge: multilingual user base with mixed-language queries, and sponsored listing relevance (Spotlight product).

## Search Context

**Spotlight** is Carousell's paid placement product — sellers pay to appear prominently in search. The core challenge: match sponsored listings to user queries semantically, not just lexically. "Selling my old iPhone 12" should appear for query "used apple phone."

## Key Engineering Work

### Dense Vector Migration
- Migrated from pure BM25 to hybrid search with dense vectors
- Model: `paraphrase-multilingual-MiniLM-L12-v2` — essential for SE Asian mixed-language queries (English + Filipino, Bahasa, Mandarin)
- 384-dim embeddings chosen over 768-dim for storage/speed trade-off at scale
- Elasticsearch `dense_vector` field + cosine similarity

### Results
- **+23% CTR** on Spotlight listings (semantically relevant ads shown for semantic queries)
- **-18% zero-result queries** — listings found where keyword matching failed
- Multilingual model was essential: users mix English with local languages in the same query

### Key Lesson
Hybrid over pure dense: BM25 still wins for exact model/SKU searches; dense wins for categorical/semantic queries.

## Articles

- [[Migrating to Elasticsearch with Dense Vector for Carousell Spotlight]] — migration strategy, results

## Related Concepts

- [[Dense Vector Retrieval]] · [[Hybrid Search]] · [[Semantic Search]] · [[Bi-Encoder]]
