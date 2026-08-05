---
type: person
title: "Jo Kristian Bergum"
aliases: ["jobergum"]
role: "Co-founder"
affiliation: "Hornet"
former_affiliation: "Vespa AI"
website: "https://hornet.dev"
tags:
  - person
  - search
created: 2026-05-15
---

# Jo Kristian Bergum

Co-founder of [[Hornet]], a retrieval infrastructure company focused on agentic AI systems. Formerly Chief Scientist at [[Vespa]] AI, where he led research on AI-powered search and retrieval, including the native ColBERT embedder and LLM-as-judge work.

## Articles in This Vault

- [[Announcing the Vespa ColBERT embedder 1|Announcing the Vespa ColBERT Embedder]]
- [[Using Approximate Nearest Neighbor Search to Find Similar Products]]
- [[E-commerce Search and Recommendation with Vespa]]
- [[Improving retrieval with LLM-as-a-judge]]
- [[This Is What Agentic Retrieval Looks Like]] — Hornet; GPT-5 query behavior analysis on BrowseComp-Plus
- [[Three mistakes when introducing embeddings and vector search]] — pre-trained models without fine-tuning, single-vector models out-of-domain, and unpriced ANN tradeoffs; source of *"an exhaustive search might be all you need"*
- [[Improving Zero-Shot Ranking with Vespa Hybrid Search]] — part one; BEIR, IR evaluation, and why in-domain scores don't predict transfer
- [[Improving Zero-Shot Ranking with Vespa Hybrid Search - part two]] — tuned BM25 + distilled 22M ColBERT hybrid; 0.481 BEIR average, 12 of 13 datasets
- [[Improving Search Ranking with Few-Shot Prompting of LLMs]] — flan-t5-xl generating synthetic training data from three labeled examples; 80.2 nDCG@10 on TREC-COVID

## Key Contributions

- Native [[ColBERT]] embedder in Vespa with 32x asymmetric compression
- Asymmetric binarization (float queries, int8 documents) for late interaction at scale
- LLM-as-judge retrieval evaluation framework (Vespa)
- Characterization of agentic query workload: long queries, web-search operators, multi-turn compounding (Hornet)
- Zero-shot hybrid ranking on [[BEIR]] — tuned BM25 fused with a distilled ColBERT reranker, with distributed min-max [[Score Normalization|normalization]] computed at the query dispatcher
- [[Synthetic Query Generation]] pipeline for domains with no labels: instruction-prompted [[FLAN-T5]], [[Consistency Filtering]], cross-encoder training — released as open notebooks and data

## Concepts

- [[ColBERT]]
- [[Late Interaction]]
- [[Dense Vector Retrieval]]
- [[Hybrid Search]]
- [[Agentic Search]]
- [[LLM as Judge]]
- [[Zero-Shot Retrieval]]
- [[Brute-Force Vector Search]]
- [[Synthetic Query Generation]]
- [[Consistency Filtering]]
- [[Score Normalization]]
- [[Cross-Encoder]]

## Case Studies

- [[Vespa - Ranking Without Labels on CORD-19]] — the three-post arc from tuned BM25 to a synthetically trained cross-encoder
