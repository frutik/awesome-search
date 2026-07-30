---
title: "Zero-Shot Retrieval"
type: concept
aliases:
  - Zero-Shot Ranking
  - Out-of-Domain Retrieval
  - Out-of-Domain Generalization
  - Domain Transfer in Retrieval
  - Zero-Shot Generalization
tags:
  - concept
  - retrieval
  - evaluation
  - zero-shot
created: 2026-07-30
---

# Zero-Shot Retrieval

**Zero-shot retrieval** is using a retrieval model on a corpus and query distribution it was
never trained on — no in-domain labels, no fine-tuning pass. It is the normal case in practice:
almost nobody has judgment data for their own catalogue, so almost every deployed embedding
model is being asked to generalise.

## The Central Result

In-domain quality does not predict out-of-domain quality. The [[BEIR]] paper's finding, as
quoted in [[Three mistakes when introducing embeddings and vector search]]:

> We studied the effectiveness of ten different retrieval models and demonstrate that in-domain
> performance cannot predict how well an approach will generalize in a zero-shot setup. Many
> approaches that outperform BM25 in an in-domain evaluation on MS MARCO, perform poorly on the
> BEIR datasets.

The practical consequence is a rule: **never adopt an embedding model on the strength of its
[[MS MARCO]] number alone.** A model can beat [[BM25]] by a very large margin on MS MARCO and
lose to it on a corpus with slightly different documents and questions.

BM25 is the reason this stings. It has no learnable parameters, so it has nothing to overfit —
which makes it a stubbornly strong out-of-domain baseline and the honest thing to measure
against first.

## Why Single-Vector Models Transfer Worst

The sources report the *result* rather than the mechanism, so treat what follows as the usual
explanation rather than a measured finding. A [[Bi-Encoder]] compresses a whole passage into one
vector, and that bottleneck appears to force the model to decide at training time *which*
semantic distinctions are worth preserving — a decision necessarily made against the training
query distribution. Move the distribution and the discarded distinctions are plausibly the ones
you now need.

On the same reasoning, architectures that keep more representational surface should transfer
better. This is an ordering by argument, not a measured ranking:

| Approach | Why it generalises better |
|---|---|
| [[ColBERT]] / [[Late Interaction]] | Per-token vectors with MaxSim; matching decisions are deferred to query time rather than baked into one pooled vector |
| [[Learned Sparse Retrieval]] ([[SPLADE]], [[ELSER]]) | Stays in term space, so lexical overlap remains available as a fallback signal |
| [[Hybrid Search]] | Keeps BM25 in the loop precisely as insurance against dense-side domain failure |

Bergum's stated position is the first row: multi-vector representations *"generalize much
better than single-vector representations."*

Related caveat from within the vault: [[miniCOIL]]'s BM25 fallback on out-of-vocabulary terms is
the same instinct — preserve a signal that doesn't depend on having seen the domain.

## Closing the Gap

When zero-shot quality isn't good enough, the options in rough order of cost:

- **Hybrid fusion** — add BM25 back; cheapest insurance, no training.
- **Domain fine-tuning** — [[Embedding Fine-tuning]] on in-domain labels; the single biggest
  lever, and the one that requires data you may not have.
- **Synthetic in-domain labels** — generate queries for your own documents, then train.
- **[[Hard Negative Mining]]** — worth more once you are already fine-tuning in-domain.
- **[[Knowledge Distillation]]** — teach a cheap retriever to rank like an expensive
  [[Cross-Encoder]] that you could never run over the full corpus.

The warning attached to all of them: fine-tuning on one domain can *cost* you performance on
another. The vault's worked example is [[Fine-Tuning Sparse Embeddings for E-Commerce Search]],
where an [[Amazon ESCI Dataset]]-tuned SPLADE beat BM25 by 27.5% in-domain, yet lost to the
off-the-shelf model on [[Home Depot Product Search Relevance]] and collapsed on MS MARCO. A
model tuned for one catalogue is not a general model.

## How It's Measured

[[BEIR]] is the standard instrument — 9 task types across 18 zero-shot datasets, nDCG@10 by
convention, models trained elsewhere and evaluated without further tuning. Read reported
averages with the subset caveat in the [[BEIR]] note: licence-restricted datasets mean a
published "BEIR average" often covers 12–15 of them rather than the full suite.

## Related Concepts

- [[Bi-Encoder]] — the architecture most exposed to domain shift
- [[ColBERT]] · [[Late Interaction]] — better transfer via deferred matching
- [[Learned Sparse Retrieval]] · [[SPLADE]] · [[ELSER]] · [[miniCOIL]] — term-space alternatives
- [[BM25]] — the parameter-free baseline that keeps winning out-of-domain
- [[Hybrid Search]] — insurance against dense-side failure
- [[Embedding Fine-tuning]] · [[Hard Negative Mining]] · [[Knowledge Distillation]] — the gap-closing toolkit
- [[Search Evaluation]] — the parent practice

## Datasets

- [[BEIR]] — the zero-shot benchmark
- [[MS MARCO]] — the training corpus whose numbers mislead
- [[Amazon ESCI Dataset]] · [[Home Depot Product Search Relevance]] — the in-domain / out-of-domain pair in the vault's worked example

## Articles

- [[Three mistakes when introducing embeddings and vector search]] — [[Jo Kristian Bergum]];
  out-of-domain failure as one of three adoption mistakes
- [[Fine-Tuning Sparse Embeddings for E-Commerce Search]] — measured evidence that domain tuning
  cuts both ways

## People

- [[Jo Kristian Bergum]]
