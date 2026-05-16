---
type: company
category: end-user
industry: [e-commerce, marketplace, handmade goods]
products: [Etsy marketplace, seller search, buyer search]
search_domain: long-tail handmade/vintage e-commerce search
use_cases: ["[[Etsy - Entropy-Based Search Diversity]]", "[[Etsy - Domain-Specific Spelling Correction]]"]
tags: [company, end-user, e-commerce, diversity, spelling-correction]
created: 2026-05-16
---

# Etsy

Marketplace for handmade, vintage, and unique goods. Search is unusually challenging because Etsy's catalog uses non-standard vocabulary — sellers create their own item names and descriptions with platform-specific terminology ("cottagecore", "steampunk").

## Search Context

Etsy search must handle:
- **Long-tail vocabulary**: seller-invented terms and styles not in standard dictionaries
- **Broad/ambiguous queries**: "necklace" covers an enormous semantic space
- **Diversity imperative**: for broad queries, showing five variations of the same item is a failure

## Key Engineering Work

### Entropy-Based Diversity
- Applied Shannon entropy to measure result diversity over category/attribute distributions
- Set entropy targets per query type: broad queries → high entropy target; specific queries → low
- Thermodynamics analogy: optimal search = maximum useful entropy, not maximum relevance

### Domain-Specific Spelling Correction
- Standard spell correction would "fix" valid Etsy terms like "cottagecore"
- Used noisy-channel model with domain-specific language model trained on Etsy query logs
- Click data validates corrections: if a "correction" leads to zero clicks, it was wrong

### Broad Query Handling
- Classifies queries as broad vs. navigational
- For broad queries: diversity injection to represent multiple interpretations
- Prevented "winner takes all" domination by popular categories

## Articles

- [[How Etsy Uses Thermodynamics for Search]] — entropy-based diversity
- [[Modeling Spelling Correction for Search at Etsy]] — domain-specific spell correction
- [[Targeting Broad Queries in Search]] — broad query diversity strategy

## Related Concepts

- [[Diversity Metrics]] · [[Spelling Correction]] · [[Query Types]] · [[Query Understanding]]
