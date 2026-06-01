---
title: "Listing Embeddings in Search Ranking"
tags:
  - clippings
  - search
  - embeddings
  - personalization
  - case-study
  - medium
source: "https://medium.com/airbnb-engineering/listing-embeddings-for-similar-listing-recommendations-and-real-time-personalization-in-search-601172f7603e"
author: "Mihajlo Grbovic, Haibin Cheng, Qing Zhang, Lynn Yang, Phillippe Siclait, Matt Jones"
created: 2026-05-15
concepts:
  - Dense Vector Retrieval
  - Personalization
  - Embedding Fine-tuning
---

# Listing Embeddings in Search Ranking

**Source:** https://medium.com/airbnb-engineering/listing-embeddings-for-similar-listing-recommendations-and-real-time-personalization-in-search-601172f7603e
**Authors:** [[Mihajlo Grbovic]], Haibin Cheng, Qing Zhang, Lynn Yang, Phillippe Siclait, Matt Jones

## Summary

Airbnb trained 32-dimensional listing embeddings from 800M+ search click sessions to enable real-time [[Personalization]] in search ranking. The embeddings implicitly encode location, price, listing type, architecture, and aesthetic qualities.

## Training Approach

Adapted word2vec negative sampling to listing click sessions:
- Session = uninterrupted sequence of clicked listing IDs (30+ minute gap = new session)
- 4.5M active listings
- 800M+ click sessions
- **Key modification**: booked listings treated as global context across all sessions
- Market-specific negative sampling to address geographic concentration bias

## Model Architecture

- 32-dimensional dense vectors per listing
- Captures "location, price, listing type, architecture" implicitly from user behavior

## Integration with Search Ranking

Two real-time similarity features fed into the main ML ranking model:

- **EmbClickSim**: cosine similarity between candidate listing and user's recently clicked listings
- **EmbSkipSim**: cosine similarity between candidate and listings user explicitly skipped

## Results

- Similar Listings carousel: **+21% CTR**, **+4.9% more bookings discovered**
- Real-time personalization in search ranking: launched successfully (2017)

## Related Concepts

- [[Dense Vector Retrieval]]
- [[Personalization]]
- [[Embedding Fine-tuning]]
- [[Learning to Rank]]
- [[Click Signals]]

## Related Articles

- [[Machine Learning-Powered Search Ranking of Airbnb Experiences]]
- [[Fine-Tuning Text Embeddings For Domain-Specific Search]]
