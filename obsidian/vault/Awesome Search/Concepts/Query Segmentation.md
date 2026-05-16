---
title: "Query Segmentation"
aliases: ["query parsing", "query chunking", "phrase detection in queries"]
tags:
  - concept
  - query-understanding
  - nlp
---

# Query Segmentation

## Definition

Query segmentation splits a multi-word query into meaningful segments (phrases, entities, concepts) that should be treated as atomic units rather than individual words.

Example:
- Input: `"new york times best seller list 2024"`
- Naive tokenization: `["new", "york", "times", "best", "seller", "list", "2024"]`
- Correct segmentation: `["new york times"] ["best seller list"] ["2024"]`

Without segmentation, the query would match documents about "New York" + "times" + "best" — not the newspaper's bestseller list.

## Why Segmentation Matters

Mis-segmented queries cause:
- **Over-matching**: "black board" (chalkboard) matched against "black" + "board" separately
- **Under-matching**: "Apple Watch" matched against "apple" (fruit) + "watch" (timepiece)
- **Ranking errors**: correct documents ranked lower because query phrase not preserved

## Segmentation Approaches

### Rule-Based
- Named entity recognition (NER) → entities are segments
- Dictionary lookup → known brand names, product models = segments

### Statistical (Unsupervised)
Pointwise Mutual Information (PMI) measures how often words appear together vs. independently:
```
PMI(w₁, w₂) = log P(w₁w₂) / (P(w₁) × P(w₂))
```
High PMI → likely a meaningful phrase → keep as segment.

Query log-based: if "new york times" appears 10,000 times as a query but "new york" and "times" appear separately much more, that co-occurrence signal suggests segmentation.

### Neural
Fine-tuned sequence labeling models (BERT-based) that predict segment boundaries:
```
Input: "new york times best seller list"
Labels: B  I   E   B    I    E    (B=begin, I=inside, E=end)
Output: ["new york times"] ["best seller list"]
```

## Relation to [[Query Understanding]]

Segmentation is the first step in Tunkelang's three-part [[Query Understanding]] framework:
1. **Query formulation** (includes segmentation) → parse the query
2. **Intent classification** → understand the goal
3. **Contextualization** → personalize/situate

## E-commerce Examples

| Raw Query | After Segmentation |
|-----------|-------------------|
| "red wine glasses set 6" | ["red wine glasses"] ["set"] ["6"] |
| "canon eos r5 battery" | ["canon eos r5"] ["battery"] |
| "mens running shoes nike size 11" | ["mens running shoes"] ["nike"] ["size 11"] |

## Related Concepts

- [[Query Understanding]] — segmentation is a component
- [[Search Intent]] — segmentation enables better intent classification
- [[Query Types]] — different query types need different segmentation rules
- [[Hybrid Search]] — segmented phrases matched in BM25 phrase queries

## People

- [[Daniel Tunkelang]] — query segmentation as part of QU framework
