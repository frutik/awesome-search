---
title: "Embedding Fine-tuning"
aliases: ["fine-tuning embeddings", "domain adaptation", "embedding adaptation", "custom embeddings"]
tags:
  - concept
  - embeddings
  - fine-tuning
  - machine-learning
---

# Embedding Fine-tuning

## Definition

Embedding fine-tuning adapts a pre-trained embedding model (trained on general web data) to perform better on a specific domain, task, or query distribution. General-purpose models like `text-embedding-ada-002` or `all-MiniLM-L6-v2` may underperform on specialized corpora (legal, medical, code, e-commerce).

## Why Fine-tune?

General embedding models are trained on broad internet text. They may:
- Miss domain-specific terminology ("apoptosis" in biology, "covenant" in legal)
- Fail at task-specific semantics (question↔answer vs. paraphrase matching)
- Underperform on short queries vs. long documents ([[Asymmetric Semantic Search]])

[[Shaw Talebi]]'s experiments show fine-tuned models consistently outperform general models on domain-specific benchmarks, often with small datasets (1,000–10,000 examples).

## Fine-tuning Approaches

### 1. Contrastive Learning (Most Common)
Train with positive pairs (query, relevant doc) and negatives:
```
Loss = -log(exp(sim(q,d+)/τ) / Σ exp(sim(q,d_i)/τ))
```
Framework: `sentence-transformers` with `MultipleNegativesRankingLoss`

### 2. Knowledge Distillation
Use a powerful [[Cross-Encoder]] as teacher → compress into [[Bi-Encoder]] student.
- Teacher scores many (query, doc) pairs
- Student learns to match teacher's scores in embedding space
- Related: [[Retrieval Pipeline]] compression

### 3. Matryoshka Fine-tuning
Train with [[Matryoshka Embeddings]] loss — embeddings remain valid at multiple truncated sizes. Useful for tiered search systems.

### 4. Task-Specific Heads
Add task-aware prefix prompts (e.g., `"Represent this question:"`) rather than full fine-tuning.
Related: [[Task-Aware Embeddings]]

## Dataset Construction

| Method | Effort | Quality |
|--------|--------|---------|
| Human annotation | High | Best |
| LLM-generated pairs | Low | Good for bootstrapping |
| BM25 hard negatives | Medium | Critical for quality |
| In-batch negatives | None | Baseline |

**Hard negatives** — documents that look relevant but aren't — are crucial for training discriminative embeddings.

## Multimodal Fine-tuning

For image+text search, fine-tune [[CLIP]]-style models:
- Align image and text embeddings in the same vector space
- Cross-modal retrieval: text query → image results (or vice versa)
- [[Shaw Talebi]] demonstrates CLIP fine-tuning for domain-specific multimodal search

## When to Fine-tune vs. General Model

Fine-tune when:
- Domain has specialized vocabulary not well-covered by general training
- You have 1,000+ labeled query-document pairs
- Retrieval quality is measurably below target on domain-specific benchmarks

Use general model when:
- Broad coverage needed
- Limited training data
- Latency/serving cost constraints (larger fine-tuned models)

## Related Concepts
- [[Embeddings]] — what embeddings are; training approaches
- [[Dense Embeddings]] — the representation type typically fine-tuned

- [[Bi-Encoder]] — architecture typically fine-tuned
- [[Matryoshka Embeddings]] — fine-tuning strategy for flexible dimensions
- [[Task-Aware Embeddings]] — lightweight adaptation via prompts
- [[Multimodal Embeddings]] — cross-modal fine-tuning
- [[Dense Vector Retrieval]] — downstream use of fine-tuned models
- [[Asymmetric Semantic Search]] — common fine-tuning target scenario
- [[Retrieval Pipeline]] — fine-tuning can collapse multi-stage pipelines

## People
## Articles

- [[Fine-Tuning Qwen3 Embeddings for Product Category Classification]] — LoRA on 615M model; LSPC dataset; 0.836 macro-F1
- [[Qwen3 Embedding Series]] — 0.6B/4B/8B; #1 MTEB multilingual; MRL support; Apache 2.0


- [[Shaw Talebi]] — Fine-tuning text and multimodal embedding models
