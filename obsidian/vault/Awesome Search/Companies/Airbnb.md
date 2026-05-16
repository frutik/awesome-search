---
type: company
industry: travel / marketplace
products:
  - Airbnb (home stays)
  - Airbnb Experiences
search_domain: accommodation and experience discovery / ranking
use_cases:
  - "[[Airbnb - ML-Powered Experiences Ranking]]"
---

# Airbnb

## Search Context

Airbnb runs two distinct search products:
- **Listing search**: finding homes and apartments to rent (the core product)
- **Experiences search**: finding local tours, classes, and activities hosted by individuals

Both are marketplace ranking problems — the goal is not just relevance but probability of booking. Airbnb has published extensively on ML-based ranking and embedding-based personalization.

## Search Challenges

- **Conversion signal as relevance**: bookings (not just clicks) are the true label — but sparse
- **Cold start for new listings/experiences**: no historical engagement data
- **Personalization at scale**: pre-computing rankings for 1M+ users daily
- **Diversity vs. precision tradeoff**: showing only the single most relevant experience category hurts discovery
- **Multi-objective**: quality, popularity, diversity, and business goals must be balanced in one model

## Tech Stack

- Gradient Boosted Decision Trees (GBDT) for core ranking
- **Category Intensity** features derived from user click history with recency decay
- Offline pre-computation of personalized rankings + online re-ranking for query-time features
- 32-dimensional **listing embeddings** trained on 800M booking sessions (word2vec-style)

## Use Cases

- [[Airbnb - ML-Powered Experiences Ranking]]

## Published Articles

- [[Machine Learning-Powered Search Ranking of Airbnb Experiences]]
- [[Listing Embeddings in Search Ranking]]
