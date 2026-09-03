---
type: concept
title: "Embedding Fine-tuning"
aliases: ["fine-tuning embeddings", "domain adaptation", "embedding adaptation", "custom embeddings"]
tags:
  - concept
  - embeddings
  - fine-tuning
  - machine-learning
created: 2026-05-16
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

### 1. [[Contrastive Learning]] (Most Common)
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

### 5. LoRA / PEFT
[[LoRA]] (Low-Rank Adaptation) injects small trainable matrices alongside frozen base model weights — updating ~0.1–1% of parameters while achieving comparable quality to full fine-tuning. Increasingly the standard approach for embedding fine-tuning, especially on large models (Qwen3, E5-large).
[[QLoRA]] extends LoRA with 4-bit base quantization, enabling fine-tuning on consumer hardware.
See [[PEFT]] for the full family of parameter-efficient methods.

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

## The Non-Negotiable Case

Before the cost/benefit question, there is a case where skipping fine-tuning is simply broken.
Representations taken straight from a model that has *only* been pre-trained are not useful for
any task: encoding queries and documents with vanilla [[BERT]] and ranking by cosine similarity
gives *"next to random ranking results."* [[Jo Kristian Bergum]] files this as mistake number one
in [[Three mistakes when introducing embeddings and vector search]] — pre-training optimises a
masked-language-model objective, not a ranking one, and the two do not transfer.

The corollary is mistake number two: fine-tuning on [[MS MARCO]] fixes this *for MS MARCO*, and
in-domain gains do not predict out-of-domain gains. See [[Zero-Shot Retrieval]].

## When to Fine-tune vs. General Model

Fine-tune when:
- Domain has specialized vocabulary not well-covered by general training
- You have 1,000+ labeled query-document pairs
- Retrieval quality is measurably below target on domain-specific benchmarks

Use general model when:
- Broad coverage needed
- Limited training data
- Latency/serving cost constraints (larger fine-tuned models)

## Measuring Whether It Worked

Fine-tuning is easy to do and easy to fool yourself about. Training loss falling is not evidence of retrieval improvement, and the most common source of an impressive-looking gain is query-level leakage between train and test splits. See [[Model Selection and Fine-Tuning Evaluation]] for the harness, split discipline, and checkpoint-selection traps.

## Related Concepts
- [[Contrastive Learning]] — the objective underneath most of the approaches above
- [[Embeddings]] — what embeddings are; training approaches
- [[Dense Embeddings]] — the representation type typically fine-tuned

- [[Bi-Encoder]] — architecture typically fine-tuned
- [[The Generalization Cliff]] — the gap fine-tuning closes, and the generality it costs in exchange
- [[Zero-Shot Retrieval]] — what fine-tuning is trying to buy, and where it fails to transfer
- [[Matryoshka Embeddings]] — fine-tuning strategy for flexible dimensions
- [[Task-Aware Embeddings]] — lightweight adaptation via prompts
- [[Multimodal Embeddings]] — cross-modal fine-tuning
- [[Dense Vector Retrieval]] — downstream use of fine-tuned models
- [[Asymmetric Semantic Search]] — common fine-tuning target scenario
- [[Retrieval Pipeline]] — fine-tuning can collapse multi-stage pipelines
- [[LoRA]] — dominant PEFT method for embedding fine-tuning
- [[QLoRA]] — LoRA + 4-bit quantization; consumer GPU fine-tuning
- [[PEFT]] — umbrella term; parameter-efficient fine-tuning family

## People
## Articles

- [[Fine-Tuning Qwen3 Embeddings for Product Category Classification]] — LoRA on 615M model; LSPC dataset; 0.836 macro-F1
- [[Qwen3 Embedding Series]] — 0.6B/4B/8B; #1 MTEB multilingual; MRL support; Apache 2.0


- [[Shaw Talebi]] — Fine-tuning text and multimodal embedding models
- [[Fine-Tuning an Embedding Model for Semantic Search]] — practical Sentence Transformers fine-tuning; MNR Loss; catastrophic forgetting warning
- [[Fine-Tuning Sparse Embeddings for E-Commerce Search]] — the same argument on the **sparse** side: [[SPLADE]] fine-tuned on catalog data, +27.5% nDCG@10 over BM25, with cross-domain transfer measured and found wanting
- [[Three mistakes when introducing embeddings and vector search]] — [[Jo Kristian Bergum]]; skipping fine-tuning entirely as mistake #1, and trusting it out-of-domain as mistake #2
- [[Hard Negative Mining]] — the ANCE loop, and the false-negative risk it carries
- [[The Complete Guide to Fine-Tuning Embedding Models]] — comprehensive guide: 6 dataset types, 5 loss functions (MNRL/CoSENT/Triplet/CachedMNRL/Matryoshka), evaluation metrics
