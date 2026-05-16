---
title: "Query Segmentation"
source: "https://queryunderstanding.com/query-segmentation-2cf860ade503"
author:
  - "[[Daniel Tunkelang]]"
published: 2018-09-01
created: 2026-05-15
description: "How search systems identify meaningful phrase boundaries within multi-word queries to improve understanding and matching — part of the Query Understanding series."
tags:
  - clippings
---

# Query Segmentation

Part of the **Query Understanding** series by [[Daniel Tunkelang]].

## Overview

Query segmentation identifies how multi-word queries should be grouped into meaningful phrases (segments). The segmentation affects how query terms are matched against the index.

## Why It Matters

"**red dress shoes**" has two valid segmentations:
- ["red dress", "shoes"] — red dresses + shoes? Ambiguous
- ["red", "dress shoes"] — dress shoes that are red ✓

Getting this wrong leads to poor retrieval.

## Approaches

**Statistical / unsupervised**
- Mutual Information (MI) between adjacent terms
- n-gram frequency in query logs
- Higher-frequency bigrams are more likely to be segments
- Unsupervised Query Segmentation Using Query Logs (Microsoft Research)

**Supervised**
- Train a sequence labeling model (CRF, BiLSTM-CRF) on labeled data
- Features: n-gram frequency, PMI, word embeddings

**Neural**
- BERT-based models can segment based on contextual understanding

## Key Insights

- Segment boundaries determined by statistical cohesion of word pairs
- Domain knowledge critical: "New York" always one segment, "summer dress" context-dependent
- Segmentation informs downstream entity recognition

## Applications

- Phrase queries in search (exact phrase matching)
- Compound entity detection ("Harry Potter", "New Balance 990")
- Synonym and rewrite rules applied at segment level

> Note: Article content behind Medium paywall — accessible at source URL with Medium account.


## Related Concepts

- [[Query Understanding]]
- [[Query Segmentation]]

## People

- [[Daniel Tunkelang]]
