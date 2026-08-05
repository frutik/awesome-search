---
type: concept
title: "Contrastive Learning"
aliases: ["contrastive loss", "contrastive training", "InfoNCE", "triplet loss", "in-batch negatives"]
tags:
  - concept
  - embeddings
  - machine-learning
  - fine-tuning
  - training
created: 2026-08-05
---

# Contrastive Learning

## Definition

Contrastive learning is the training objective underneath essentially every modern [[Embeddings|embedding]] model. Rather than predicting a label, the model is taught a **geometry**: pull semantically related things together in vector space, push unrelated things apart.

The training signal is a comparison, not an absolute target. A single training example is a *(query, positive, negative)* triple — or a query with one positive and many negatives — and the loss rewards the model for scoring the positive higher than the negatives. This is why embedding models are trained on pairs and triples rather than on labelled documents.

## The Common Objectives

- **Triplet loss** — anchor, positive, negative, with a margin. The model is penalized until the positive is closer than the negative by at least that margin. Simple, and largely superseded.
- **InfoNCE / multiple-negatives ranking loss** — the current default. Treats the batch as a classification problem: given a query and N candidates (one positive, N−1 negatives), maximize the probability assigned to the positive. Uses **in-batch negatives** — every other example's positive serves as a negative for yours, which makes it very cheap to get many negatives per step.
- **Cosine similarity loss** — regression against a graded similarity score, used when you have graded rather than binary labels.

## Why Negatives Are Everything

The single most important practical fact: **the model learns exactly the distinctions its negatives force it to make.**

In-batch negatives are cheap but random, and random negatives are almost always trivially easy — teaching a product search model to separate "running shoes" from "dishwasher" is teaching it something it already knew. Training loss drops satisfyingly and retrieval quality barely moves.

Real gains come from [[Hard Negative Mining]]: negatives that the *current* model already ranks highly but that are actually wrong. These sit near the decision boundary and carry real information. This is why negative mining, not architecture or learning rate, dominates fine-tuning outcomes — and why negatives should be re-mined as the model improves, since yesterday's hard negatives become today's easy ones.

There is a failure mode on the other side too: **false negatives**. Mine aggressively enough and you start collecting documents that are actually relevant but unlabelled, then explicitly train the model to rank them lower. Graded judgments and a relevance threshold on mined negatives guard against this.

## Consequences for Practice

- **Loss is not quality.** Contrastive loss measures separation on your training triples. It routinely decouples from [[NDCG]] on real queries. Evaluate retrieval metrics at checkpoints instead — see [[Model Selection and Fine-Tuning Evaluation]].
- **The data shape is the design.** Deciding what counts as a positive (a click? a purchase? a human label?) defines what "relevant" means to the resulting model, more than any hyperparameter. See [[Implicit Judgments]].
- **[[Bi-Encoder]] geometry is the constraint.** Contrastive training produces a space where similarity is a dot product. That is what makes retrieval fast, and also what limits it — the reasoning failures exposed by [[BRIGHT]] are a property of this objective, not a bug in a particular model.

## Related Concepts

- [[Hard Negative Mining]] — the lever that determines outcomes
- [[Embedding Fine-tuning]] — the practice this objective powers
- [[Bi-Encoder]] · [[Cross-Encoder]] — architectures trained this way
- [[Knowledge Distillation]] — the alternative signal source: learn from a stronger model's scores rather than from labels
- [[Embeddings]] · [[Dense Embeddings]]

## Related Topics

- [[Model Selection and Fine-Tuning Evaluation]] — measuring whether it worked
- [[Embedding Models Compared]]

## Articles

- [[The Complete Guide to Fine-Tuning Embedding Models]]
- [[Fine-Tuning Text Embeddings For Domain-Specific Search]]
- [[Fine-Tuning Sparse Embeddings for E-Commerce Search]]
- [[Fine-Tuning an Embedding Model for Semantic Search]]
