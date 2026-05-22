---
title: "Search Intent"
aliases: ["query intent", "user intent", "search intent classification", "informational", "navigational", "transactional"]
tags:
  - concept
  - query-understanding
  - search
---

# Search Intent

## Definition

Search intent describes what a user is actually trying to accomplish with a query — distinct from what words they typed. Understanding intent allows search systems to serve the user's underlying need rather than just matching keywords.

## Classic Taxonomy (Broder 2002)

### Navigational Intent
User wants to go to a specific website or page.
- "Facebook login"
- "New York Times homepage"
- Best served by: direct link, no ranked list needed

### Informational Intent
User wants to learn something.
- "How does photosynthesis work?"
- "symptoms of appendicitis"
- Best served by: comprehensive, authoritative content

### Transactional Intent
User wants to do something — often buy, download, or sign up.
- "buy Nike running shoes"
- "download Spotify"
- Best served by: product pages, conversion-optimized results

## Extended Taxonomy for E-commerce

| Intent | Query Example | Signal | Optimal Response |
|--------|--------------|--------|-----------------|
| Navigational | "my orders" | Exact brand/URL | Direct page |
| Informational | "how to clean leather shoes" | Question words | Guide/article |
| Transactional | "buy red sneakers size 10" | Buy/purchase words | Product listing |
| Comparative | "Nike vs Adidas running shoes" | vs, compare | Comparison page |
| Discovery | "cool summer outfits" | Vague, exploratory | Curated collection |

## Intent Classification

Modern intent classifiers use fine-tuned BERT/RoBERTa:
```python
from transformers import pipeline

classifier = pipeline("text-classification", 
                       model="domain/intent-classifier")
result = classifier("buy cheap running shoes")
# → {"label": "transactional", "score": 0.94}
```

Features that signal intent:
- **Question words** (what, how, why) → informational
- **Action verbs** (buy, download, sign up) → transactional
- **Brand names without product** → navigational
- **Adjectives + category** → discovery/exploratory

## Intent-Retrieval Alignment

Different intents need different retrieval strategies:

| Intent | Retrieval Strategy |
|--------|--------------------|
| Navigational | Exact match / URL lookup |
| Informational | [[Semantic Search]] / [[RAG]] |
| Transactional | Structured data + [[Hybrid Search]] |
| Discovery | [[Diversity Metrics]] + personalization |

## Ambiguous Queries

Many queries are intent-ambiguous:
- "python": programming vs. snake
- "mercury": planet, element, car, Roman god, Freddie Mercury

For ambiguous queries, [[Diversity Metrics]] / MMR ensures coverage of multiple intents.

## Relation to [[Agentic Search]]

In [[Agentic Search]], the agent must infer intent to choose the right retrieval strategy:
- Informational → comprehensive RAG
- Transactional → structured search + ranking
- Comparative → multi-source retrieval + synthesis

## Related Concepts

- [[Query Understanding]] — intent is a component of QU
- [[Query Types]] — more granular taxonomy
- [[Diversity Metrics]] — for ambiguous intent
- [[Agentic Search]] — intent-aware retrieval planning
- [[Bag-of-Documents Model]] — probabilistic intent framing

- [[Intent Drift]] — how the right answer for a query shifts over time

## People

- [[Daniel Tunkelang]] — "Mapping Search Queries To Search Intents", "Search: Intent, Not Inventory"
