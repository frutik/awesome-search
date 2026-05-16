---
type: person
name: Mihajlo Grbovic
affiliation: Airbnb
role: ML Engineer / Research Scientist
tags: [person, embeddings, learning-to-rank, personalization, airbnb]
created: 2026-05-16
---

# Mihajlo Grbovic

ML/Research Scientist at **Airbnb**. Led two major search ranking initiatives: listing embeddings from 800M+ click sessions, and the ML-powered Experiences ranking system that delivered ~28% cumulative booking improvement.

## Articles

- [[Listing Embeddings in Search Ranking]] — 32-dim listing embeddings from 800M sessions, EmbClickSim/EmbSkipSim features, +21% CTR
- [[Machine Learning-Powered Search Ranking of Airbnb Experiences]] — four-stage ML progression (GBDT → personalization → online scoring → business rules)

## Key Contributions

- Adapted word2vec to listing click sessions; booked listings as global context across sessions
- Market-specific negative sampling to address geographic concentration bias
- Real-time personalization features EmbClickSim and EmbSkipSim in main LTR model
- Business rules via training data weighting (no separate rules engine)

## Related

- [[Airbnb]] · [[Learning to Rank]] · [[Personalization]] · [[Embedding Fine-tuning]] · [[Dense Vector Retrieval]]
