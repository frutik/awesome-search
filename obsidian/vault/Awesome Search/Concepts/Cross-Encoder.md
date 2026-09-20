---
type: concept
title: "Cross-Encoder"
aliases: ["Cross-encoder Reranker", "Interaction Model", "Early Interaction"]
tags:
  - concept
  - search
  - neural-ir
  - reranking
created: 2026-05-16
---

# Cross-Encoder

## Definition

A **cross-encoder** processes the **query and document jointly** in a single encoder pass, producing a relevance score from their combined representation. It captures rich query-document interactions but requires encoding each pair separately — making it too slow for first-stage retrieval over large corpora.

## How It Works

```
[Query + Document] → BERT encoder → relevance score
```

The query and document are concatenated (with separator tokens) and passed through a transformer together. The `[CLS]` token embedding is projected to a scalar relevance score.

## Key Properties

| Property | Value |
|---|---|
| Query-document interaction | Full (early interaction) |
| Document pre-computation | Not possible — must encode per query-doc pair |
| Speed | Slow — O(num_candidates) at query time |
| Quality | Highest — rich interaction captures subtle relevance |

### The Score Is Ordinal, Not Calibrated

A cross-encoder's score is ordinal. Its ordering within one candidate list is meaningful; its
absolute magnitude is not. Any use that needs a *cutoff* rather than an *order* — pruning an
overfetched pool, gating a downstream [[RAG]] step, declaring
[[Zero Results|no relevant results]], comparing scores across shards or across the lexical and
vector legs of [[Hybrid Search]] — therefore requires a threshold tuned per corpus, and
re-tuned whenever the corpus, retriever, or model version changes.

This follows from how rerankers are trained and selected, not from the architecture. A
cross-encoder can end in a sigmoid and be fit with binary cross-entropy, which is a proper
scoring rule and a supported loss in [[Sentence Transformers]]; the `ms-marco` checkpoints emit
a raw value roughly in [-10, 10] that the caller may squash into [0, 1] at will. What the
squashed number is calibrated *to* is the training distribution — one positive against hard
negatives mined from a lexical top-k — whose base rate is an artifact of the sampling scheme
rather than of any corpus. Nor would anything downstream notice calibration's absence:
[[NDCG]] and [[MRR]] are invariant to monotonic score transforms, so a perfectly ordered,
arbitrarily miscalibrated model scores identically on every reranker leaderboard. The precise
claim is that a *ranking-trained* cross-encoder's score is not a probability — which covers the
checkpoints and rerank APIs in general use, but is not a limit of the architecture.

This is the gap a [[Calibrated Relevance Probability]] closes, and it is the axis on which
[[Hev meets Jev]] argues a probability-valued model such as [[Jev]] beats a cross-encoder even
when their nDCG@10 is level: on that benchmark's SciFact subset, documents scored above 0.9
were judged relevant 76% of the time, against a MiniLM-L6 logit carrying no such reading. The
other route to the property is post-hoc — Platt scaling or isotonic regression on a held-out
judged set — which works on a cross-encoder too, at the cost of exactly the per-corpus
labelling the property was meant to remove.

## Role in Multi-Stage Retrieval

Cross-encoders are typically used as **rerankers** in a two-stage pipeline:

```
Stage 1: Bi-encoder retrieves top-100 candidates (fast)
Stage 2: Cross-encoder reranks top-100 (slow, but small set)
```

This pipeline gets the speed of [[Bi-Encoder]] retrieval with the quality of cross-encoder scoring.

## Training

- Trained on query-document pairs with binary or graded relevance labels
- MS MARCO is the standard training dataset
- Can use knowledge distillation from larger cross-encoders

### Training one without labels

A cross-encoder needs query–document pairs, which is exactly what a new domain lacks. Those pairs can
be manufactured: in [[Improving Search Ranking with Few-Shot Prompting of LLMs]] a 3B [[FLAN-T5]] model
generated queries for a corpus, [[Consistency Filtering]] kept the 43% whose source document ranked #1,
and two negatives per query were sampled from the retrieved top-100. A **22M-parameter 6-layer MiniLM
cross-encoder** trained two epochs on the result reached **80.2 nDCG@10** on [[TREC-COVID]] — 4 points
above the hybrid baseline it reranked, from a labeling budget of three queries.

See [[Synthetic Query Generation]] and [[Hard Negative Mining]].

## Why It's Often the Easier Model to Operate

Quality is the usual reason given for choosing a cross-encoder over a [[Bi-Encoder]]. The operational
reason is less discussed and sometimes decisive: **swapping a cross-encoder requires no re-processing of
the document corpus.** A new bi-encoder means re-embedding and re-indexing everything, so model
versioning is a data migration; a cross-encoder is stateless, so a new version is a deployment.

This is the stated rationale in
[[Improving Search Ranking with Few-Shot Prompting of LLMs]], alongside effectiveness.

The cost — per-query inference over candidates — is managed by shrinking both the candidate set and the
text. That article capped reranking depth at **30** documents and fed the model **query-contextual
dynamic summaries** rather than full abstracts, so the sequence covers only the query-relevant span of
each document. Both levers reduce work without touching the model.

## vs. Other Architectures

| | Cross-Encoder | [[Bi-Encoder]] | [[ColBERT]] |
|---|---|---|---|
| Interaction | Early (joint) | None | Late (token-level) |
| Speed | Slow | Fast | Medium |
| Quality | Best | Good | Near cross-encoder |
| Scalability | Not scalable | Scalable | Scalable |

## Related Concepts

- [[Bi-Encoder]] — faster retrieval model it complements
- [[ColBERT]] — alternative late-interaction model bridging speed and quality
- [[Late Interaction]] — between bi-encoder (none) and cross-encoder (early) interaction
- [[Retrieval Pipeline]] — cross-encoder as Stage 2 reranker
- [[ELSER]] — distilled from a cross-encoder teacher
- [[Interaction Paradigms]] — the no/late/early spectrum; cross-encoder is the early-interaction endpoint
- [[Calibrated Relevance Probability]] — what a cross-encoder logit is not, and the operations that need it

## Articles

- [[Bi-encoder vs Cross-encoder When to Use Which One]]
- [[Improving Search Ranking with Few-Shot Prompting of LLMs]] — [[Jo Kristian Bergum]] ([[Vespa]]);
  a 22M cross-encoder trained on synthetic data, and the versioning argument for the architecture
- [[Improving Zero-Shot Ranking with Vespa Hybrid Search - part two]] — [[PROMPTAGATOR]]'s
  cross-encoder as the strongest few-shot model in that comparison (0.528 avg nDCG@10)
- [[Hev meets Jev]] — a MiniLM-L6 cross-encoder as the local baseline (0.447 mean nDCG@10), and the logit-vs-probability argument

## Case Studies

- [[Vespa - Ranking Without Labels on CORD-19]] — cross-encoder as the final stage over a 30-document shortlist
