---
type: concept
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

## Distilling a Generative LLM Instead of a Ranker

The teacher does not have to be a ranking model. In
[[Improving Search Ranking with Few-Shot Prompting of LLMs]] a **3B generative model** ([[FLAN-T5]] xl)
is the teacher and a **22M [[Cross-Encoder|cross-encoder]]** the student — but the transfer runs through
generated *data* rather than through soft scores:

```
3B instruction-tuned LLM
  │  generates a query per document (offline, once over the corpus)
  ▼
synthetic query–document pairs
  │  filtered by round-trip retrievability (Consistency Filtering)
  ▼
22M cross-encoder trained on the survivors
```

Why this counts as distillation: nothing of the 3B model ships, and its knowledge — what a plausible
question about this document looks like — ends up in a model ~136× smaller. The mechanism differs from
soft-label distillation in one useful way: **the teacher runs once over the corpus rather than once per
training example**, so a model too expensive to sit in a training loop is affordable here. Measured cost:
~3,600 queries/hour on one A100 at ~$1/hour.

See [[Synthetic Query Generation]].

## Distilling a Judge Rather Than a Retriever

A third target, distinct from both the ranker and the generative teacher above: the **evaluator**.

[[LLM as Judge|LLM judges]] produce high-quality relevance labels and cannot be run at catalogue scale. Treating their judgments as training data — on the order of 100,000 examples — is enough to fine-tune a small embedding model into a serviceable judge with sub-20ms CPU inference, cheap enough to run continuously rather than in periodic offline batches. See [[Towards Scalable Relevance Engineering]] and [[Staged Judging]].

The economics differ from ranker distillation in a useful way. A distilled retriever must be *better* than the alternatives to justify itself; a distilled judge only has to be good enough to handle the easy majority, because hard cases still escalate to the teacher. That tolerance for imperfection is what makes the cascade work, and it means the usual quality-loss objection to distillation carries less weight here.

[[How Etsy Uses LLMs to Improve Search Relevance]] runs this pattern as an explicit three-tier cascade rather than a single teacher/student pair: an o3-based LLM annotator (anchored to human golden labels) trains a Qwen 3 VL 4B teacher via supervised fine-tuning, which in turn trains a lightweight BERT-based two-tower student for sub-10ms production inference. Measured Macro F1 degrades tier by tier — 0.72 (annotator) → 0.71 (teacher) → 0.65 (student) — a visible, quantified version of the quality loss the cascade is designed to tolerate.

## Compression Costs More Out-of-Domain

A caveat that in-domain benchmarks hide. [[Improving Zero-Shot Ranking with Vespa Hybrid Search - part two]]
reports that a distilled 22M [[ColBERT]] underperformed full-sized variants, and states that compression and
distillation show a **greater impact zero-shot than in-domain**. That model scored 0.363 average nDCG@10
across 13 [[BEIR]] datasets against BM25's 0.453.

The implication for evaluation: measuring a student against its teacher on the training distribution
understates the loss. If the student will be deployed on a domain neither model was trained on, that is where
the comparison has to be made. See [[Zero-Shot Retrieval]].

## Related Concepts

- [[Embedding Fine-tuning]] — related training approach
- [[Bi-Encoder]] — primary distillation target (student)
- [[Cross-Encoder]] — primary distillation source (teacher)
- [[Reranking]] — the task cross-encoders excel at
- [[Dense Embeddings]] — output of distilled bi-encoders
- [[BERT]] — backbone architecture for both teacher and student
- [[Synthetic Query Generation]] — distillation via generated data rather than soft scores
- [[Consistency Filtering]] — the quality gate on that generated data
- [[FLAN-T5]] — an open generative teacher
- [[Zero-Shot Retrieval]] — where the student's losses actually show up
- [[ELSER]] — the vault's worked ensemble-teacher example (MiniLM + MonoT5-3B → 100M student)
- [[Staged Judging]] — distilling the evaluator instead of the retriever
- [[Contrastive Learning]] — the objective distillation replaces or supplements
- [[Semantic Relevance]] — the signal Etsy's three-tier cascade distills

## Articles

- [[Improving Search Ranking with Few-Shot Prompting of LLMs]] — [[Jo Kristian Bergum]] ([[Vespa]]);
  3B generative teacher → 22M cross-encoder, via synthetic data
- [[Improving Zero-Shot Ranking with Vespa Hybrid Search - part two]] — the out-of-domain cost of
  compressing a multi-vector model
- [[Distilling Retrieval Pipelines to a Single Embedding Model]] — distilling a whole pipeline rather
  than a single teacher
- [[How Etsy Uses LLMs to Improve Search Relevance]] — explicit three-tier LLM annotator → teacher → student
  cascade for real-time semantic relevance
