---
title: "Autocomplete"
aliases: ["autosuggest", "search suggestions", "query suggestions", "search as you type", "typeahead"]
tags:
  - concept
  - search-ux
  - query-understanding
  - e-commerce-search
---

# Autocomplete

## Definition

Autocomplete (also: autosuggest, search suggestions, typeahead) shows predicted query completions or related queries as the user types, before they submit the full search. It reduces typing effort, helps users formulate better queries, and surfaces popular/relevant searches.

## Types of Suggestions

| Type | Source | Example |
|------|--------|---------|
| Query completion | Query log (most common continuations) | "nike r" → "nike running shoes" |
| Content-based | Index (actual titles/products) | "ipho" → "iPhone 15 Pro" |
| Trending | Recent query spikes | "black friday deals" (seasonal) |
| Personalized | User history | Previous searches |
| Category steering | Taxonomy | "shoes" → "Women's Shoes", "Men's Shoes" |

## Architecture Components

### Retrieval
How to find candidate suggestions fast for every keystroke:
- **Prefix trie** (Patricia tree): O(prefix_length) lookup
- **Inverted index**: for full-text suggestion matching
- **Fuzzy matching**: handle typos in partial queries

### Ranking
Which suggestions to show first:
- Query frequency (most popular completions)
- Query success rate (completions that led to clicks/conversions)
- User personalization signals
- Trending boost (recency × velocity)

### Filtering
Remove suggestions that should not be shown:
- Zero-result queries (avoid suggesting searches that return nothing)
- Offensive/inappropriate content
- Trademarked terms (jurisdiction-dependent)

## Corpus Building

Suggestions come from:
1. **Query log analysis**: extract common queries → filter low-frequency → rank by success
2. **Content crawl**: index actual product/document titles
3. **Editorial curation**: manually add branded/campaign terms

Quality threshold: only suggest queries with sufficient historical frequency to be statistically reliable.

## UX Design Considerations (Baymard Institute)

13 design patterns for autocomplete (Baymard's research):
- Show query suggestions AND product suggestions simultaneously (categorized)
- Highlight the typed prefix in the suggestion
- Limit to 5–8 suggestions (cognitive load)
- Include thumbnails for product suggestions
- Allow keyboard navigation
- Don't autocorrect the typed text (user intent)

## Neural/Semantic Autocomplete

Modern improvement: use embeddings to suggest semantically related queries, not just prefix matches:
- "warm winter boots" → also suggest "insulated hiking boots" (semantic expansion)
- Requires [[Semantic Search]] over query embeddings
- Grubhub's query2vec for food search suggestions

## Zero-Result Prevention

Autocomplete is a first line of defense against zero results:
- Only suggest queries known to return results
- Steer users toward retrievable formulations
- Can silently rewrite unproductive terms

## Related Concepts

- [[Query Understanding]] — autocomplete is first-touch query understanding
- [[Query Types]] — suggestion strategy differs by query type
- [[Spelling Correction]] — often combined with autocomplete
- [[Semantic Search]] — neural autocomplete
- [[Zero Results]] — autocomplete prevents zero-result queries
- [[Faceted Search]] — category steering in autocomplete

## People
## Articles

- [[How to Really Scale Autocomplete]] — bonsai.io; search_as_you_type + significant_terms; 416 RPS at 45ms p99 on 6M docs
- [[LLM-Powered Query Extraction for Autocomplete]] — [[David Albrecht]]; GPT-4.1-nano on WANDS; LLM cold-start solution for <$5


- [[Daniel Tunkelang]] — "Autocomplete" and "Autocomplete and User Experience" at queryunderstanding.com

- [[Autosuggest Retrieval Data Structures and Algorithms]]
- [[Autosuggest Ranking]]
- [[Affordances for Conversational Search]]
