---
type: concept
title: "miniCOIL"
aliases: ["mini-COIL", "miniCOIL sparse retriever"]
tags:
  - concept
  - sparse-retrieval
  - neural-ir
  - search
website: https://qdrant.tech/articles/minicoil/
related_concepts:
  - "[[BM25]]"
  - "[[Learned Sparse Retrieval]]"
  - "[[SPLADE]]"
  - "[[Sparse Vector Retrieval]]"
created: 2026-07-27
---

# miniCOIL

## Definition

**miniCOIL** is a lightweight [[Learned Sparse Retrieval]] model from [[Qdrant]], introduced by [[Evgeniya Sukhodolskaya]] in May 2025. Where [[SPLADE]] replaces lexical weights entirely with learned ones, miniCOIL **augments the [[BM25]] formula with a small semantic component** — described by its author as standing "on the shoulders of BM25".

The problem it targets: BM25 scores `bat` in "fruit bat" and "baseball bat" identically, because it sees only term statistics. Dense retrievers resolve the ambiguity but give up keyword precision.

## Mechanism

Derived from **COIL** (Contextualized Inverted Lists), which stored per-term vectors in an inverted index rather than collapsing each term's meaning to one number. COIL's practical problems were specialized indexes, domain-specific training, and subword tokenization; miniCOIL works at **word level** instead.

```
Word → contextual embedding (jina-embeddings-v2-small-en, 512d)
     → linear layer + Tanh
     → 4 dimensions per word in the sparse vector
```

- **Vocabulary:** the 30,000 most common English words, stemmed and cleaned
- **Per word:** 4 consecutive cells, one per semantic dimension
- **Scoring:** the BM25 formula extended with a *Meaning* component comparing query and document term semantics

## The Out-of-Vocabulary Fallback

miniCOIL's distinguishing property: **a word with no miniCOIL training falls back to plain BM25 scoring within the same sparse vector.**

This is the direct answer to a structural limit of SPLADE, raised in Q&A at [[Evgeniya Sukhodolskaya - Fine-Tuning Sparse Neural Retrievers for E-Commerce]] — SPLADE's output dimensions *are* its base model's vocabulary, so terms outside that vocabulary simply cannot be represented, and SPLADE has no graceful degradation path. With SPLADE you must choose a base model that already knows your tokens.

## Benchmarks

On BEIR datasets it had not been trained on, nDCG@10 vs BM25:

| Dataset | miniCOIL | BM25 |
|---|---|---|
| MS MARCO | 0.244 | 0.237 |
| NQ | 0.319 | 0.304 |
| Quora | 0.802 | 0.784 |
| FiQA-2018 | 0.257 | 0.252 |
| HotpotQA | 0.633 | **0.634** |

Wins on four of five. The gains are deliberately modest — the point is generalization without domain-specific training bias, in contrast to a fine-tuned SPLADE, which buys large in-domain gains at the cost of transfer (see [[Fine-Tuning Sparse Embeddings for E-Commerce Search]]).

## vs SPLADE

| | SPLADE | miniCOIL |
|---|---|---|
| Relationship to BM25 | Replaces the weighting | Extends the formula |
| Term expansion | Yes (synonyms) | No |
| Out-of-vocabulary | Unrepresentable | Falls back to BM25 |
| Vector size | ~100–200 non-zero of 30,522 | 4 dims per word |
| Domain adaptation | Fine-tune per catalog | Designed to generalize |

## Related Concepts

- [[BM25]] — the formula miniCOIL extends
- [[SPLADE]] — the alternative learned-sparse approach
- [[Learned Sparse Retrieval]] · [[Sparse Embeddings]] · [[Sparse Vector Retrieval]]
- [[Hybrid Search]] — miniCOIL is positioned as a BM25 replacement in the sparse leg

## People

- [[Evgeniya Sukhodolskaya]] — author
