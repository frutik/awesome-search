---
title: "Word2Vec"
aliases: ["Word2Vec", "word2vec", "CBOW", "skip-gram", "continuous bag of words"]
tags:
  - concept
  - embeddings
  - nlp
  - representation-learning
---

# Word2Vec

The foundational point-[[Embeddings|embedding]] method (Mikolov et al., 2013) that learns a dense vector per word from raw text, such that words appearing in similar contexts land near each other. Two training architectures:

- **CBOW (Continuous Bag of Words)** — predict a center word from its surrounding context words.
- **Skip-gram** — predict the context words from the center word.

Both use **negative sampling** for efficient training. Word2Vec popularized the observation that embedding *algebra* encodes meaning: `king − man + woman ≈ queen`.

## Why It Recurs Here

Word2Vec is the point-vector baseline that [[Region-Based Representation|region representations]] aim to improve on, and its CBOW training scheme is reused directly by **[[Word2Box]]** — which swaps the dot-product similarity for [[Box Embedding|box]] intersection volume. Its skip-gram/negative-sampling recipe also underpins many search systems' learned embeddings (e.g. Query2Vec, Airbnb/Vinted listing embeddings).

## Related Concepts
- [[Embeddings]] — parent concept
- [[Dense Embeddings]] — modern descendants (neural bi-encoders)
- [[Word2Box]] — Word2Vec's CBOW scheme applied to boxes
- [[Box Embedding]] — region method that replaces point vectors
- [[Synonyms]] — Word2Vec neighborhood mining for synonym discovery

## People
- [[Tomas Mikolov]] — lead author of Word2Vec
