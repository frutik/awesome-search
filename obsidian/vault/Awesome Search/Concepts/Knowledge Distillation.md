---
title: "Knowledge Distillation"
aliases: ["knowledge distillation", "model distillation", "teacher-student training", "distillation", "cross-encoder distillation", "bi-encoder distillation"]
tags:
  - concept
  - search
  - embeddings
  - ml
  - finetuning
created: 2026-05-16
---

# Knowledge Distillation

## Definition

Knowledge distillation trains a small "student" model to mimic the outputs of a larger, more powerful "teacher" model. The student learns from the teacher's soft probability distributions (not just hard labels), capturing nuance the teacher has learned.

In search, this is the primary method for building fast [[Bi-Encoder]] retrievers that approach the quality of slow [[Cross-Encoder]] rerankers.

## The Core Problem It Solves

[[Cross-Encoder]] rerankers are highly accurate but slow — they can't score millions of documents at query time. [[Bi-Encoder]] models are fast but less accurate. Distillation bridges the gap:

```
Cross-encoder (teacher)
  │  scores query-doc pairs
  ▼
Soft relevance scores (e.g., 0.87, 0.43, 0.12...)
  │  used as training signal
  ▼
Bi-encoder (student)
  │  learns to reproduce teacher's ranking
  ▼
Fast retriever with near-teacher quality
```

## Why Soft Labels Beat Hard Labels

Training on binary labels (relevant=1, not relevant=0) loses information. A cross-encoder might score three documents 0.9, 0.7, 0.3 — all "relevant" but clearly ranked. Distillation preserves this gradient, giving the student richer signal per training example.

## Distillation for Embedding Models

**Margin MSE loss**: minimize the difference between teacher's score margins and student's score margins across document pairs:

```
L = (score_teacher(q, d+) - score_teacher(q, d-)) 
  - (score_student(q, d+) - score_student(q, d-))
```

Used in SBERT, BGE, and most production-grade embedding models.

## Distillation vs. Fine-tuning

| | [[Embedding Fine-tuning]] | Knowledge Distillation |
|---|---|---|
| Training signal | Human labels / click data | Teacher model scores |
| Requires human annotation | Yes (or implicit feedback) | No (teacher generates labels) |
| Quality ceiling | Label quality | Teacher quality |
| Cost | Human labeling | Teacher inference cost |

Distillation can be combined with fine-tuning: fine-tune a cross-encoder on human labels first, then distill that teacher into a bi-encoder.

## Related Concepts

- [[Embedding Fine-tuning]] — related training approach
- [[Bi-Encoder]] — primary distillation target (student)
- [[Cross-Encoder]] — primary distillation source (teacher)
- [[Reranking]] — the task cross-encoders excel at
- [[Dense Embeddings]] — output of distilled bi-encoders
- [[BERT]] — backbone architecture for both teacher and student
