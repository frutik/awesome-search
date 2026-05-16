---
title: "Query Understanding, Divided into Three Parts"
source: "https://dtunkelang.medium.com/query-understanding-divided-into-three-parts-d9cbc81a5d09"
author:
  - "[[Daniel Tunkelang]]"
published: 2018-10-02
created: 2026-05-15
description: "A framework dividing query understanding into three stages: holistic understanding, reductionist understanding, and resolution."
tags:
  - clippings
---

# Query Understanding, Divided into Three Parts

## Introduction

Drawing from Caesar's "Gallia est omnis divisa in partes tres," query understanding divides into three distinct components:

1. **Holistic understanding** — broad classification of topic and intent
2. **Reductionist understanding** — breaking the query into components and determining meanings
3. **Resolution** — transforming understood queries into executable search engine commands

---

## Part One: Holistic Understanding

Examines queries broadly without deep analysis. Key tasks:

**Language Identification** — Recognizes query language for multilingual search.

**Query Categorization** — Maps queries into a predefined taxonomy (e.g., "History of the Roman Empire").

**High-Level Intent Recognition** — Identifies searcher motivations beyond literal meaning (e.g., quotation lookup vs. biography search).

### Implementation

- Rule-based systems (regex, heuristics)
- Machine learning classifiers trained on labeled data
- Character-level embeddings (e.g., fastText) for feature vectors

---

## Part Two: Reductionist Understanding

Decomposes queries into meaningful segments and classifies them.

**Query Segmentation** — Divides queries into semantic units. Example: "roman empire poetry" → ["roman empire", "poetry"].

**Entity Recognition** — Classifies each segment by type: "roman empire" = Subject, "poetry" = Genre.

### Approaches

- Historical: Hidden Markov Models (HMM), Conditional Random Fields (CRF)
- Modern: Bidirectional LSTM-CRF models

Holistic understanding selects the appropriate reductionist model per category, simplifying each individual model and improving accuracy.

---

## Part Three: Resolution

Translates understood queries into executable search backend queries.

**Entity Mapping** — Maps recognized entities to a knowledge base (taxonomies, ontologies, faceted classifications, knowledge graphs).

**Query Assembly** — Combines mapped entities and unmatched keywords into executable queries (AND operation as baseline).

Advanced resolution features:
- Query expansion (broaden for recall)
- Query relaxation (soften constraints for low-result queries)
- Intent-based ranking model or collection selection
- Facet selection based on intent

---

## Conclusion

Implementing complete query understanding is substantial work — "query understanding can't be built in one day." The three-stage framework guides incremental prioritization and phased improvements.


## Related Concepts

- [[Query Understanding]]
- [[Query Relaxation]]
- [[Query Segmentation]]
- [[Faceted Search]]
- [[Synonyms]]

## People

- [[Daniel Tunkelang]]
