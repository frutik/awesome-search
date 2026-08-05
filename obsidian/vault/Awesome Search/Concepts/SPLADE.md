---
type: concept
title: "SPLADE"
aliases: ["Sparse Lexical and Dense Expansion", "SParse Lexical AnD Expansion"]
tags:
  - concept
  - search
  - sparse-retrieval
  - neural-ir
created: 2026-05-16
---

# SPLADE

## Definition

**SPLADE** (**Sp**arse **L**exical **a**n**d** **E**xpansion / **SP**arse **L**exical **A**n**D** **E**xpansion) is a neural sparse retrieval model that creates **learned sparse embeddings** via BERT's Masked Language Model (MLM) head. It combines semantic understanding from transformers with the efficiency of inverted-index retrieval.

Developed by [[Thibault Formal]], [[Stéphane Clinchant]], and Benjamin Piwowarski at NAVER LABS Europe.

## Core Mechanism

```
Input text → BERT → MLM head → 30,522-dim vocabulary distribution per token
→ Log-ReLU activation
→ Max-pool across tokens
→ Sparse vector (≈100-200 non-zero entries out of 30,522)
```

For each token in the input, the MLM head predicts probability over the entire vocabulary — enabling **term expansion** (predicting relevant terms not in the original text) and **compression** (suppressing uninformative terms).

**Example:** For document about binary numbers, SPLADE:
- Expands: adds "computing", "digit" (semantically related)  
- Compresses: removes conjunctions and articles
- Result: 23-term sparse vector from a 60-term passage

## Key Technical Components

**Log saturation:** Prevents single terms from dominating scores.

**FLOPS regularizer:** Penalizes computation cost to encourage sparsity, acts as implicit stop-word removal.

## Versions

| Version | Innovation |
|---|---|
| SPLADE v1 | Original: both query & document expansion |
| SPLADE v2 | Max [[Pooling|pooling]] over the vocabulary axis; document-only expansion (faster queries) |
| SPLADE-V3 (2024) | Updated models; Hugging Face release |

## vs. BM25 and Dense Retrieval

| | BM25 | SPLADE | Dense ([[Bi-Encoder]]) |
|---|---|---|---|
| Vocabulary | Fixed (term frequency) | Expanded (learned) | None (continuous) |
| Semantics | None | Good (via BERT) | Excellent |
| Speed | Very fast | Fast (inverted index) | Fast (ANN) |
| Interpretability | High | High (vocabulary terms) | Low |
| Domain adaptation | Manual | Learned | Learned |

## Domain Fine-Tuning

Public SPLADE checkpoints are trained on [[MS MARCO]] — **web queries against Wikipedia passages**. In e-commerce that mismatch shows up directly in the learned term weights and synonym expansions, which reflect encyclopedic text rather than a product catalog.

Fine-tuning on catalog data measurably closes the gap. In [[Fine-Tuning Sparse Embeddings for E-Commerce Search]], training from `distilbert-base-uncased` on the [[Amazon ESCI Dataset]] gave nDCG@10 **0.389 vs 0.305 for BM25 (+27.5%)**, where off-the-shelf SPLADE reached only 0.326 (+7.2%). What changed: brand names gained weight, generic words like "good" lost it, and domain vocabulary such as "refurbished" became meaningful.

The cost is generality. The ESCI-tuned model **lost to off-the-shelf SPLADE on Home Depot data** (0.384 vs 0.391) and fell far below BM25 on MS MARCO (0.751 vs 0.915). Multi-domain training recovers cross-catalog consistency at the price of peak in-domain accuracy.

### Full vs inference-free SPLADE

The inference-free variant skips the encoder pass on the query side to save latency. [[Evgeniya Sukhodolskaya]] argues against it for e-commerce: the domain is **intent-heavy**, and "Apple juice" vs "Apple iPhone" are two distinct intents around the same token — precisely the distinction the query encoder provides.

### Vocabulary limits

SPLADE's output dimensions *are* the base model's vocabulary, so [[Out-of-Vocabulary|out-of-vocabulary]] terms cannot be represented and there is no fallback path — you must pick a base model that already knows your tokens. [[miniCOIL]] addresses this directly by reverting to a BM25 weight for untrained words.

Tooling: [[Sentence Transformers]] v5 (`MLMTransformer` + `SpladePooling`, `SpladeLoss`) and [[qdrant-sparse-finetune]].

## Advantages Over Dense Retrieval

- No [[Vector Search]] infrastructure needed — works with standard inverted indexes
- Interpretable representations (vocabulary-dimension vectors)
- Strong zero-shot performance
- Easier integration into existing [[Hybrid Search]] pipelines

## Related Concepts
- [[Embeddings]] — parent concept
- [[Sparse Embeddings]] — SPLADE is a learned sparse embedding model

- [[Sparse Vector Retrieval]] — SPLADE is the leading learned sparse model
- [[ELSER]] — Elastic's SPLADE-based model
- [[miniCOIL]] — alternative learned-sparse design that extends BM25 instead of replacing it
- [[Hard Negative Mining]] — the ANCE loop used to fine-tune it
- [[Embedding Fine-tuning]] — the dense-side analogue
- [[Hybrid Search]] — SPLADE complements dense retrieval
- [[Cross-Encoder]] — used as teacher model for SPLADE distillation

## Articles

- [[SPLADE for Sparse Vector Search Explained]] — [[James Briggs]]
- [[Hybrid Search SPLADE Sparse Encoder]] — Sowmiya Jaganathan
- [[SPLADE - sparse bi-encoder BERT model for first-stage ranking 1]] — [[Stéphane Clinchant]], [[Thibault Formal]]
- [[Elastic Learned Sparse Encoder ELSER Retrieval Performance]] (ELSER as SPLADE variant)
- [[Fine-Tuning Sparse Embeddings for E-Commerce Search]] — [[Thierry Damiba]]; domain fine-tuning with full benchmarks

## Videos

- [[Evgeniya Sukhodolskaya - Fine-Tuning Sparse Neural Retrievers for E-Commerce]] — [[MICES]] 2026

## People

- [[Thibault Formal]]
- [[Stéphane Clinchant]]
- [[Evgeniya Sukhodolskaya]] · [[Thierry Damiba]] — e-commerce fine-tuning
