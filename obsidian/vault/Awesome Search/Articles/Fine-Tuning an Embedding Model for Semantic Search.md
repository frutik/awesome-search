---
created: 2026-06-01
type: article
title: "Fine Tuning an Embedding Model for Semantic Search"
source: "https://medium.com/@venkat.ramrao/fine-tuning-a-sentence-transformer-for-semantic-search-7c7a57f4db2f"
author: "[[Venkat Ram Rao]]"
published: 2023-12-23
tags:
  - article
  - embedding
  - fine-tuning
  - sentence-transformers
  - medium
concepts:
  - Embedding Fine-tuning
  - Semantic Search
topics:
  - Search Quality Assurance
---

# Fine Tuning an Embedding Model for Semantic Search

A practical hands-on introduction to fine-tuning embedding models for semantic search using the Sentence Transformers library. Demonstrates fine-tuning `all-MiniLM-L12-v2` on the Databricks Dolly-15k dataset using Multiple Negatives Ranking Loss, with measurable improvement on QA retrieval.

---

## Key Concepts

### Sentence Transformers
Python framework and library for accessing and training vector embedding models. Widely used for semantic similarity and RAG pipelines. Supports text, images, and other data types. Access to Hugging Face-hosted models.

### Loss Functions for Embedding Training

| Loss | When to use |
|---|---|
| **Multiple Negatives Ranking (MNR) Loss** | Positive pairs of related text (query, answer) |
| **Triplet Loss** | Anchor + positive + negative triplets |
| **Contrastive Loss** | Positive and negative pairs |

### Catastrophic Forgetting
A real risk when training with semantically similar negatives: the model can lose all ability to differentiate between texts, clustering all embeddings together. Mitigation: use clearly distinct negatives; shorter text segments tend to train better.

## Practical Experiment

- **Base model**: `sentence-transformers/all-MiniLM-L12-v2`
- **Dataset**: `databricks/databricks-dolly-15k` — closed QA subset (~1,700 question+context pairs); 70/30 train/test split
- **Loss**: MultipleNegativesRankingLoss
- **Training**: 10 epochs, free Google Colab T4 GPU, ~1,200 training examples

### Results

| Test | Before | After |
|---|---|---|
| "What color is the Sky?" → "The sky is blue" cosine sim | 0.608 | 0.692 |
| "What color is the sea?" (wrong answer) cosine sim | 0.704 | 0.634 |
| Average cosine sim (test set, correct contexts) | 0.620 | 0.694 |

The fine-tuned model substantially improved question→correct-answer similarity while reducing similarity to incorrect answers.

## Alternatives Mentioned
- **LlamaIndex**: its own embedding fine-tuning functions
- **FlagEmbeddings / BGE**: FlagEmbedding library with fine-tuning support
- **API access**: OpenAI ada, other hosted embedding APIs

---

## Related Concepts
- [[Embedding Fine-tuning]] — core subject of the article
- [[Semantic Search]] — target use case
- [[Dense Vector Retrieval]] — downstream application

## Related Articles
- [[The Complete Guide to Fine-Tuning Embedding Models]] — comprehensive companion covering all dataset types and loss functions
- [[Fine-Tuning Qwen3 Embeddings for Product Category Classification]] — more recent fine-tuning example with LoRA

## People
- [[Venkat Ram Rao]] — author
