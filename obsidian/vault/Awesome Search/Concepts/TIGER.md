---
title: "TIGER"
aliases: ["TIGER", "Transformer Index for GEnerative Recommenders", "Recommender Systems with Generative Retrieval"]
tags:
  - concept
  - generative-retrieval
  - recommendation
  - quantization
---

# TIGER

**TIGER** (*Transformer Index for GEnerative Recommenders*; Rajput et al., Google, 2023 — *"Recommender Systems with Generative Retrieval"*, [arXiv:2305.05065](https://arxiv.org/pdf/2305.05065)) applies [[Generative Retrieval]] to recommendation. It is the work that popularized [[RQ-VAE]] [[Semantic IDs]] for items, carrying the [[Differentiable Search Index|DSI]] idea from document search into recsys.

---

## How It Works

1. **Build semantic IDs** — encode each item's content into a dense embedding, then quantize it with [[RQ-VAE]] into a short sequence of codebook tokens.
2. **Sequence the session** — represent a user's interaction history as the concatenation of those item semantic IDs.
3. **Generate the next item** — a seq2seq Transformer predicts the *next item's semantic ID* token-by-token; beam search yields a ranked candidate list.

## Why It Mattered

- Demonstrated that a recommender can be a single generative model rather than a dense-retrieve-then-rank pipeline.
- Showed semantic IDs improve **cold-start** and **long-tail** recommendation, because new/rare items get content-derived codes that share prefixes with popular neighbours.
- Established the RQ-VAE-semantic-ID recipe now reused across generative retrieval and ranking (e.g. semantic IDs for ranking at YouTube, [arXiv:2306.08121](https://arxiv.org/pdf/2306.08121)).

## Related Concepts
- [[Semantic IDs]] — the identifier scheme TIGER builds on
- [[RQ-VAE]] — produces TIGER's item codes
- [[Generative Retrieval]] — the paradigm TIGER instantiates for recsys
- [[Differentiable Search Index]] — the document-retrieval precursor

## Articles
- [[Semantic IDs for Recommendation Systems]] — [[Janu Verma]]; reproduces a TIGER-style pipeline on Amazon Beauty
