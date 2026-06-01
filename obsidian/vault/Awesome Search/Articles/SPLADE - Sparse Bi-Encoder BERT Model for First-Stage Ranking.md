---
title: "SPLADE: A Sparse Bi-Encoder BERT Model for First-Stage Ranking"
source: "https://europe.naverlabs.com/blog/splade-a-sparse-bi-encoder-bert-based-model-achieves-effective-and-efficient-first-stage-ranking/"
author: ["Stéphane Clinchant", "Thibault Formal"]
tags:
  - clippings
  - splade
  - naver-labs
  - research
  - sparse-retrieval
  - company-blog
concepts:
  - SPLADE
  - Sparse Vector Retrieval
  - Retrieval Pipeline
created: 2026-05-15
---

# SPLADE: A Sparse Bi-Encoder BERT Model for First-Stage Ranking

**Source**: https://europe.naverlabs.com/blog/splade-a-sparse-bi-encoder-bert-based-model-achieves-effective-and-efficient-first-stage-ranking/  
**Authors**: [[Stéphane Clinchant]], [[Thibault Formal]] (NAVER LABS Europe)

## Summary

The original NAVER LABS blog post announcing [[SPLADE]] — the Sparse Lexical and Dense model — explaining the motivation, mechanism, and initial benchmark results showing competitive first-stage retrieval performance.

## Motivation: Beyond BM25 and Dense Retrieval

In 2021, first-stage retrieval was dominated by two approaches:
1. **BM25**: fast, lexical, no semantic understanding
2. **Dense bi-encoders** (DPR, etc.): semantic but slower, require ANN indexes

SPLADE's goal: a model that achieves **dense-model quality** while maintaining **BM25-like retrieval properties** (inverted index, FLOPS scalability).

## Key Innovation: Vocabulary Space Sparse Vectors

Rather than projecting to a fixed-size dense vector, SPLADE projects to the BERT vocabulary space:
- **30,522 dimensions** (full BERT vocabulary)
- **Sparse**: only ~100–300 non-zero dimensions per text
- **Interpretable**: each dimension corresponds to a real token

The Log-ReLU transformation and MaxPool aggregation are the technical heart:
```
z = log(1 + ReLU(MLM_output)) 
v = MaxPool(z, over_sequence_tokens)
```

## FLOPS Regularization

A key contribution: controlling sparsity through the FLOPS (Floating Point Operations per Second) regularizer during training:

```
Loss = cross-entropy(query, pos_doc, neg_docs) 
     + λ_q × FLOPS_q + λ_d × FLOPS_d
```

Where FLOPS ≈ sum of non-zero terms × their frequency in corpus.

Higher regularization → sparser vectors → faster retrieval → slight quality decrease.

## Term Expansion Example

Input: "automobile accident injury"  
SPLADE output (top terms by weight):
```
automobile: 2.1, accident: 1.9, injury: 1.8,
car: 1.4, crash: 1.3, vehicle: 1.1,    ← expanded terms
collision: 0.9, hurt: 0.8, damage: 0.7
```

The model has expanded the query to include semantically related terms it wasn't shown.

## Original Results (MS MARCO)

| Model | MRR@10 | Recall@1000 | Notes |
|-------|--------|------------|-------|
| BM25 | 0.184 | 0.853 | Baseline |
| DPR | 0.318 | 0.950 | Dense bi-encoder |
| **SPLADE** | **0.322** | **0.968** | Sparse + expansion |

SPLADE matches dense retrieval quality while using an inverted index.

## Legacy and Impact

SPLADE inspired:
- [[ELSER]] (Elastic) — production SPLADE-variant
- SPLADE-v2 (NAVER) — improved efficiency  
- SPLADE++ (NAVER) — cross-encoder distillation
- Multiple open-source SPLADE variants in sentence-transformers

## Related Articles

- [[SPLADE for Sparse Vector Search Explained]] — practitioner's guide
- [[Hybrid Search SPLADE Sparse Encoder]] — hybrid application
- [[Elastic Learned Sparse Encoder ELSER Retrieval Performance]] — production version

## Related Concepts

- [[SPLADE]] — this is the original announcement
- [[Sparse Vector Retrieval]] — category
- [[Retrieval Pipeline]] — first-stage retrieval role
- [[Hybrid Search]] — primary deployment pattern
- [[Bi-Encoder]] — same bi-encoder architecture, sparse output

## People

- [[Stéphane Clinchant]] — co-creator
- [[Thibault Formal]] — co-creator
