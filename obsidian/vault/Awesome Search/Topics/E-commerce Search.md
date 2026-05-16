---
type: topic
aliases: ["product search", "e-commerce search", "retail search"]
tags: [topic, e-commerce, product-search]
related_concepts: ["[[Query Types]]", "[[Zero Results]]", "[[Faceted Search]]", "[[Results Merchandising]]", "[[Results Boosting]]", "[[Learning to Rank]]", "[[Personalization]]"]
related_topics: ["[[Search Result Diversity]]", "[[Synonyms and Vocabulary Management]]", "[[Query Understanding in Practice]]", "[[Search Quality Assurance]]"]
articles: [
  "[[Deconstructing E-Commerce Search - The 12 Query Types]]",
  "[[Targeting Broad Queries in Search]]",
  "[[Three Pillars of Search Quality - Findability]]",
  "[[Three Pillars of Search Quality - Discovery and Inspiration]]",
  "[[How Etsy Uses Thermodynamics for Search]]",
  "[[Incremental AI Adoption for E-commerce Search]]",
  "[[Migrating to Elasticsearch with Dense Vector for Carousell Spotlight]]"
]
companies: ["[[Etsy]]", "[[Canva]]", "[[Carousell]]", "[[Zalando]]", "[[Airbnb]]"]
created: 2026-05-16
---

# E-commerce Search

Practice guide for product search — the specific challenges, patterns, and tradeoffs that distinguish e-commerce search from web or enterprise search.

---

## What Makes E-commerce Search Different

### The Catalog Is the Corpus
Unlike web search, your corpus is fully controlled. This is a superpower (you can enrich it) and a constraint (vocabulary mismatch is your problem to solve).

### Users Don't Know the Right Words
Sellers describe products their way; buyers search their way. A listing titled "Bohemian Macramé Wall Hanging" needs to surface for "boho wall art" and "woven wall decoration." Bridging this gap is the core e-commerce search problem.

### Relevance Is Multi-Dimensional
A result is "relevant" if the user can buy it, it fits their need, it's available, it's in their price range, and the seller is trustworthy. Each dimension may require separate signals.

### Business Rules Are First-Class
Margin, inventory, promoted listings, new seller support — these business concerns legitimately affect ranking. The challenge is integrating them without destroying relevance.

---

## The 12 Query Types (Baymard)

Understanding which type a query is determines how to handle it:

| Type | Example | Challenge |
|---|---|---|
| Exact product | "iPhone 15 Pro Max" | Navigational — precision matters most |
| Category | "headphones" | Diversity — show the space |
| Feature/spec | "wireless noise cancelling" | Attribute matching + ranking |
| Thematic | "minimalist desk accessories" | Semantic, no keyword overlap |
| Symptom | "my back hurts pillow" | Requires intent inference |
| Compatible product | "case for MacBook Air M2" | Structured attribute matching |
| Use-case | "shoes for marathon running" | Activity → product category |
| Inspirational | "gift ideas for dad" | Pure exploration |

Most search systems optimize for exact + category queries. Symptom, thematic, and inspirational queries are where most systems fail.

---

## The Three Pillars of Quality

### Findability
Can the user find what they're looking for?
- **Key metric**: zero-results rate
- **Main causes of failure**: vocabulary mismatch, spelling errors, missing synonyms
- **Fixes**: synonyms, spelling correction, query relaxation, dense retrieval

### Relevance / Ranking
Are the right items at the top?
- **Key metric**: NDCG, conversion rate
- **Main causes of failure**: wrong ranking signal, position bias in training data, business rules overriding relevance
- **Fixes**: LTR, implicit signals, debiasing

### Discovery
Can users find things they didn't know they were looking for?
- **Key metric**: diversity, engagement depth, session conversion
- **Main causes of failure**: winner-takes-all ranking, filter over-application
- **Fixes**: diversification, exploratory UI patterns, personalization

---

## Vocabulary Management

The most common root cause of e-commerce search failure:
- Sellers write product titles in one vocabulary; buyers search in another
- Solution stack: synonyms (known pairs) → spelling correction → query expansion → semantic/dense retrieval
- Don't jump straight to dense retrieval: synonyms and spelling correction are cheaper and more controllable

See [[Synonyms and Vocabulary Management]] and [[Spelling Correction]].

---

## Facets in E-commerce

Facets are the primary UX mechanism for navigating large product catalogs. Key decision: are facet selections **hard filters** (Boolean, zero results if nothing matches) or **soft preferences** (boost matching, don't exclude)?

- For navigational queries: hard filters are correct
- For exploratory queries: soft preferences improve discovery
- Hybrid: hard filter + "include similar items?" suggestion

See [[Faceted Search]].

---

## Broad and Head Queries

High-traffic head queries ("shoes", "necklace", "bag") span enormous intent spaces. Optimizing purely for relevance produces "winner takes all" results — the most popular subcategory dominates.

**Approach**: detect broad queries → inject diversity → ensure result set represents multiple interpretations.

See [[Search Result Diversity]].

---

## Incremental AI Adoption

Four levels from zero to conversational:
1. **Level 0**: keyword + filters only
2. **Level 1**: async AI suggestion ("did you mean: Property Type: Condo?") — zero latency risk
3. **Level 2**: AI auto-executes rewritten query — 2-3s added latency
4. **Level 3**: conversational chat interface — stateful, multi-turn

Start at Level 1. Only move up if A/B test shows improvement.

---

## Related

- [[Query Understanding in Practice]] — the pipeline that powers QU in e-commerce
- [[Search Result Diversity]] — handling broad queries
- [[Synonyms and Vocabulary Management]] — vocabulary gap solutions
- [[Results Merchandising]] — business rules layer above relevance
- [[Personalization in Search]] — user-specific ranking
