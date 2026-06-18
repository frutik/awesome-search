---
title: "Zero Results"
aliases: ["no results", "zero-result queries", "null results", "empty SERP"]
tags:
  - concept
  - search-ux
  - search-quality
---

# Zero Results

## Definition

A zero-results query returns no documents to the user. It is the most unambiguous search failure — the system could not satisfy any part of the user's information need.

Zero-result rate is one of the cleanest and most actionable [[Search Evaluation]] metrics: unlike NDCG which requires judgment lists, zero results are immediately measurable from system logs.

## Causes of Zero Results

| Cause | Example | Solution |
|-------|---------|---------|
| Spelling error | "iphne" | [[Spelling Correction]] |
| Over-specific query | "nike air max 90 infrared 2024 size 10.5 wide" | [[Query Relaxation]] |
| Vocabulary mismatch | "digital money transfer" (index has "wire transfer") | [[Semantic Search]] |
| Overly strict filters | Category + Brand + Price all applied | [[Query Relaxation|Facet relaxation]] |
| New/rare products | Just-launched item not yet indexed | Indexing freshness |
| Wrong catalog scope | Cross-site query on scoped search | Scope expansion |

## Zero Results as Findability Failure

[[Andreas Wagner]]'s Three Pillars framework: zero results represent a fundamental failure of **Findability** — the first pillar of search quality. A system that cannot find items cannot serve any higher-order quality goals (relevance, discovery).

Target: <2% zero-result rate for most e-commerce and enterprise search systems.

## Recovery Strategies

### Query Relaxation
Progressively remove constraints until results appear:
1. Try full query
2. Remove least-important filters (price range, color)
3. Remove adjectives from query
4. Try individual query tokens
5. Fall back to category browse

### Spelling Correction
Detect and correct misspellings before retrieval ([[Spelling Correction]]).

### Query Rewriting / Expansion
Automatically expand or rewrite the query with synonyms or related terms:
- "fleece jacket" → also search "fleece pullover", "polar fleece top"

### Alternative Suggestions
Instead of empty page, offer:
- "Did you mean: [corrected query]?"
- "Browse [closest category]?"
- "Here are popular items in [related category]"
- "See all items in [department]"

## UX Design for Zero Results (Baymard)

Six essential elements for no-results pages:
1. Acknowledge the failure ("No results for X")
2. Spell-check and show suggestion ("Did you mean Y?")
3. Suggest alternative categories
4. Show fallback content (bestsellers, popular categories)
5. Offer to expand/relax the search
6. Provide contact/help option

What not to do: silently redirect to homepage or show completely unrelated "popular" items.

## Measuring Zero Results

```python
zero_result_rate = (
    queries_with_zero_results / total_queries
)
```

Track by:
- Query type (head vs. tail)
- Category
- Device type (mobile users have higher zero-result rates due to autocorrect failures)
- Time (new product launches temporarily spike zero results)

## Related Concepts

- [[Spelling Correction]] — primary cause of zero results
- [[Autocomplete]] — prevents zero-result queries by steering users
- [[Semantic Search]] — vocabulary mismatch → zero results solved by embeddings
- [[Faceted Search]] — over-filtering causes zero results
- [[Query Types]] — tail queries have much higher zero-result rates
- [[Search Evaluation]] — zero-result rate as a key metric

- [[Query Relaxation]] — primary recovery mechanism for zero-result queries

- [[Query Specificity]] — over-specific queries are the dominant cause of zero results in the tail


- [[Search Problem Archetypes]] — the same zero-results metric means opposite things across archetypes (wasted real estate in e-commerce vs. correct behavior under a precision mandate)

## People

- [[Daniel Tunkelang]] — zero results in e-commerce search context
