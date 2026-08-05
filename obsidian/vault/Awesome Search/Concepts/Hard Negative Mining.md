---
type: concept
title: "Hard Negative Mining"
aliases: ["hard negatives", "ANCE", "Approximate Nearest Neighbor Negative Contrastive Estimation", "negative mining"]
tags:
  - concept
  - training
  - neural-ir
  - search
related_concepts:
  - "[[Embedding Fine-tuning]]"
  - "[[Learned Sparse Retrieval]]"
  - "[[SPLADE]]"
  - "[[Embeddings]]"
created: 2026-07-27
---

# Hard Negative Mining

## Definition

**Hard negative mining** is the practice of selecting *difficult* irrelevant examples for contrastive retrieval training — documents that look relevant to the current model but are not. It exists because the naive alternative, random sampling, teaches almost nothing: as [[Evgeniya Sukhodolskaya]] puts it, *"I am querying for iPhone and I'm getting banana. They're pretty irrelevant — the model doesn't have to learn too much."*

A retrieval model learns from two signals: what is relevant (usually from labels or click logs) and what to push away. The second signal is only useful if it sits near the decision boundary.

## ANCE: The Search Engine in the Training Loop

**ANCE** (Approximate Nearest Neighbor Negative Contrastive Estimation) makes the negatives adapt to the model as it trains. Originally developed for dense retrievers, it transfers to learned sparse models:

1. Take the **current checkpoint**
2. Index the training corpus with it into a search engine ([[Qdrant Vector DB]] in the Qdrant experiments)
3. **Retrieve** for each training query — the top results are what the model currently *believes* is relevant
4. **Filter out the known-relevant ones.** What remains is, by construction, hard negatives: the model was confident and wrong
5. Train on `(query, positive, hard_negatives)` triplets, then loop

Because the negatives are re-mined against each new checkpoint, difficulty tracks the model's improving competence.

### Cost and payoff

In [[Fine-Tuning Sparse Embeddings for E-Commerce Search]] the loop was worth **5–10% on top of basic training**, and stayed cheap: sparse retrieval mines at sub-millisecond per query. Practical defaults in [[qdrant-sparse-finetune]] are 3 mining iterations, top-20 retrieval, 3 negatives per query.

## What Good Hard Negatives Look Like

A concrete e-commerce example from the [[qdrant-sparse-finetune]] smoke test — querying **"Pampers medium diapers"** surfaced:

- the right brand in the **wrong size**
- a **competitor** brand in the right size
- **adult** diapers

All three look relevant to a lexical matcher and are wrong for the shopper. This is exactly the boundary an e-commerce retriever needs to learn.

## Negatives for Synthetic Queries

When the queries themselves are generated rather than logged ([[Synthetic Query Generation]]), the same
principle applies with a shortcut: the retrieval pass that validates the query also produces the negatives.

In [[Improving Search Ranking with Few-Shot Prompting of LLMs]], each generated query is run through the
existing ranking model for [[Consistency Filtering]] anyway — keep the pair only if the source document
ranks #1. Two negatives per query are then **sampled from that same retrieved top-100**, so mining costs
nothing beyond a pass already being made. 14,156 surviving queries → 14,156 triplets with two negatives each.

The generated-query setting also softens the false-negative problem described below, but only slightly: the
source document is known to be positive by construction, so at least the intended answer is never mined
against itself.

## The False-Negative Risk

The method's structural weakness: **it assumes anything unlabeled is irrelevant.** A genuinely relevant product that was never labeled gets mined as a negative and actively trained against. In [[Evgeniya Sukhodolskaya - Fine-Tuning Sparse Neural Retrievers for E-Commerce]] this was raised in Q&A and conceded outright — the suggested mitigation is a side model acting as a relevance judge (possibly a dense one) before a candidate is accepted as a negative, at the cost of extra overhead in the loop.

The risk is worse the sparser your labels, which is the usual situation with click-log-derived training data.

## Related Concepts

- [[Contrastive Learning]] — the training objective whose outcome hard negatives dominate
- [[Staged Judging]] — how teams afford the high-coverage judgments that mining at catalogue scale requires, and that sampling cannot supply
- [[Embedding Fine-tuning]] — hard negatives are a core lever on the dense side too
- [[Learned Sparse Retrieval]] · [[SPLADE]] — where the ANCE loop was applied here
- [[Contrastive Gap]] — hard negatives as a remedy for embedding-space geometry
- [[Judgment Lists]] — the labels that determine what counts as a false negative
- [[Synthetic Query Generation]] · [[Consistency Filtering]] — mining negatives from the validation pass
- [[Cross-Encoder]] — the model trained on the resulting triplets in that pipeline

## Articles

- [[Fine-Tuning Sparse Embeddings for E-Commerce Search]] — ANCE loop implementation and measured gain
- [[Fine-Tuning Text Embeddings For Domain-Specific Search]] — hard negatives in dense triplet construction
- [[The Complete Guide to Fine-Tuning Embedding Models]] — loss functions that consume them
- [[ColBERT-Zero - To Pre-train Or Not To Pre-train ColBERT Models]] — in-batch negatives as the cheaper alternative
- [[Improving Search Ranking with Few-Shot Prompting of LLMs]] — [[Jo Kristian Bergum]]; negatives sampled from the top-100 of the consistency-check retrieval

## Videos

- [[Evgeniya Sukhodolskaya - Fine-Tuning Sparse Neural Retrievers for E-Commerce]]
