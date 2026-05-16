---
title: "Patterns for Personalization in Recommendations and Search"
tags:
  - clippings
  - search
  - personalization
  - ml
source: "https://eugeneyan.com/writing/patterns-for-personalization/"
author: "Eugene Yan"
created: 2026-05-15
concepts:
  - Personalization
  - Dense Vector Retrieval
  - Learning to Rank
---

# Patterns for Personalization in Recommendations and Search

**Source:** https://eugeneyan.com/writing/patterns-for-personalization/
**Author:** [[Eugene Yan]]

## Summary

Survey of five core ML patterns for personalization, with industry examples from Airbnb, Netflix, YouTube, DoorDash, Alibaba, and others.

## The Five Patterns

### 1. Bandits
Continuously balance exploration vs. exploitation. Netflix uses contextual bandits for image personalization; DoorDash applies them to cuisine recommendations with multi-level geolocation context.

### 2. Embeddings + MLP
Map sparse features (user ID, item ID, behavioral signals) into dense vectors, pool variable-length sequences, feed through MLP. Used by TripAdvisor (experiences), YouTube (videos).

### 3. Sequential Models
Capture item order using RNNs or Transformers. Alibaba's Behavioral Sequence Transformer achieved **+4.5% CTR** over mean pooling baseline by modeling behavioral sequences.

### 4. Graph-Based
Represent users and items as nodes in weighted graphs. Uber uses graph convolutional networks for food recommendations; Alibaba uses graph intention networks.

### 5. User Embeddings
Learn direct user representations. Airbnb generates user-type embeddings for search (see [[Listing Embeddings in Search Ranking]]); Tencent builds user lookalikes for long-tail content.

## Cross-Cutting Concerns

- **Cold-start problem**: handling new users/items with limited data
- **Exploration vs. exploitation**: discovery vs. known preferences
- **Pooling strategies**: mean/sum/max compress variable behavioral sequences
- **Attention mechanisms**: weight history by relevance to current context

## Related Concepts

- [[Personalization]]
- [[Dense Vector Retrieval]]
- [[Learning to Rank]]
- [[Click Signals]]

## Related Articles

- [[Listing Embeddings in Search Ranking]]
- [[Machine Learning-Powered Search Ranking of Airbnb Experiences]]
