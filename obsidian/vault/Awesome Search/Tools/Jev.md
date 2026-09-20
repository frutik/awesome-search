---
type: tool
title: "Jev"
aliases: ["Jev model", "TypeSafe Jev", "System One model"]
tags:
  - tool
  - model
  - structured-output
  - reranking
  - llm
website: https://docs.typesafe.ai/introduction
company: "[[TypeSafe]]"
created: 2026-09-19
---

# Jev

**Jev** is [[TypeSafe]]'s flagship model, which the company describes as the first *System One
model*: a model built to make fast, structured decisions that software consumes directly,
rather than to produce text a human reads. It generates no free-form output. The caller sends a
**state** plus a set of **typed questions**, and Jev answers each one independently and in
parallel, returning typed values and probabilities.

Its relevance to search is that this shape happens to be exactly the shape of a
[[Reranking|reranker]] — a fact demonstrated empirically in [[Hev meets Jev]].

---

## Model and Training

From the launch announcement ([[Introducing System One Models & Jev]], [[Diogo Almeida]]),
Jev is built on a purpose-built stack rather than a fine-tuned chat model: a new architecture,
a parallel sampler, and a training method TypeSafe calls
[[Reinforcement Learning for Calibrated Decisions|RLCD]] — optimizing for confidence that
tracks accuracy, rather than for human preference (RLHF) or verifiable rewards (RLVR). That
training objective is the stated reason its outputs are probabilities you can threshold rather
than scores you can only sort.

Vendor-stated operating figures, none independently verified:

| | Claimed |
|---|---|
| Input cost | $0.042 / MTok |
| Output cost | free |
| End-to-end latency | 70–500 ms |
| vs. frontier LLMs | 40–200× faster on System One-shaped queries |
| Type errors | 0%, by construction — the schema fixes the output space |

Two hard limits matter in practice. Choices are supported up to **cardinality 255**; above
that, Jev uses a two-stage system that scores options independently and then makes an explicit
choice. And the request budget is **32k tokens**, which holds roughly 50 passages — the binding
constraint on rerank depth.

The "cannot hallucinate" claim is precise but narrow: a fixed schema guarantees a *valid*
value, not a *correct* one. A confidently wrong probability remains available.
## Question Types

TypeSafe's documentation defines three:

| Type | Question it answers | Output |
|---|---|---|
| **Choice** | Choose an option from a list | choice, probabilities, confidence |
| **Score** | Score the state on a rubric | score, probabilities, confidence |
| **Noul** | Is this statement true? | a value in 0–1 |

All three can be combined in one API call. Because each question is evaluated independently
against the shared state, TypeSafe's stated design properties are that adding questions barely
changes response time, and that per-question independence avoids context-rot across a long
list of judgments.

## The Noul Type

A **Noul** is Jev's true-or-false type: a statement plus explicit criteria for what makes it
true and what makes it false, answered as a probability from 0 to 1. It is the primitive that
makes Jev usable as a reranker — "is this document relevant to this query?" is a Noul, and
thirty documents are thirty Nouls against one state.

A Noul value is **not** a confidence score, and
[[JEV vs LLM - Your Software Doesn't Want a Conversation It Wants a Decision|Sajith K]] flags
the conflation as a threshold-wrecking trap. A Noul of 0.999 says the probability the statement
is true is 99.9%; a Noul of 0.5 is a genuine coin-flip, not "medium urgency". Confidence is a
separate quantity, derived from how peaked the output distribution is, and the Choice and Score
types return it as its own field where a Noul returns only the value. A pipeline that gates on
a Noul is thresholding a probability of truth; one that gates on `confidence` is thresholding
the model's certainty about its own answer. They are not interchangeable.

## Known Failure Modes

TypeSafe publishes a "jaggedness" page listing what the model is bad at; the clearest summary
in this vault is [[How to Use Jev - A Practical Guide]]. Condensed, because several of these
bear directly on using it as a relevance judge:

- **It reads literally.** Negations, scoping words, and implied conditions are taken at face
  value — so a relevance question phrased loosely gets answered loosely (cf.
  [[Prompt Sensitivity]]).
- **Context rot is real.** Accuracy falls as the state fills with material the question does not
  need. Retrieve and filter before sending, not after ([[Clean Context]]).
- **State is not treated as hostile.** Text engineered to argue for its own classification can
  move the answer — a live concern when the "state" is documents from an open corpus.
- **It cannot count, and dates are text.** Anything arithmetic or ordinal belongs in code.
- **Contradictory instructions and criteria degrade it.** Criteria extend the instruction rather
  than acting as a separate knob.
- **It does not generate**, so it cannot explain a ranking ([[Search Results Explainability]]).

The meta-rule from those docs generalises past this model: don't ask a model what code can
compute exactly, and don't hide several judgments inside one question.
## Versions and Limits

- `jev-latest` resolved to `jev-1.13.0` as of the guide above; the vendor's own reranking
  cookbook ran `jev-1.12`. **Pin the version if you tune thresholds** — answers shift across
  releases, and the response reports the versioned ID that answered.
- Rate limits for `jev-1.13`: 250,000 tokens/second and 1,200 requests/minute, `429` over
  either. TypeSafe warns these move without notice.
- Billing is input-only, which is what makes long option lists and fan-out cheap.
- **The request budget is documented inconsistently.** [[Using TypeSafe's Jev for Evals]] reports the models page giving 64k per request and 32k for state plus the longest question, while OpenRouter lists 32K; [[Hev meets Jev]] worked to a 32k budget holding roughly 50 passages. The 32k state figure is the one the published rerank depths are consistent with — but verify against current docs before designing around it.
- Access is waitlisted, but the model is also served through OpenRouter and the Vercel AI Gateway.
- **It cannot abstain.** A forced binary with no `unknown` option makes it pick the least wrong answer rather than decline — an escape hatch has to be an explicit option in the question.
- **A third reading of the budget.** [[JEV vs LLM - Your Software Doesn't Want a Conversation It Wants a Decision]] states it as ~32,000 tokens *shared between state and questions*, alongside the 255 Choice cardinality cap — consistent with the 32k state figure above, and with text-structured state only (no images). That piece also notes what is not published at all: p95/p99 latency, calibration-under-distribution-shift data, and any SLA.
## Use as a Reranker

[[Hev meets Jev]] benchmarks this directly. The state is the query plus a top-30 shortlist
keyed `D00`–`D29`; one Noul is asked per document key; the ranking is the sort by probability.
Two call shapes are possible — **batch** (thirty Nouls in one call) and **single** (one
(query, document) pair per call).

On three [[BEIR]] subsets with a [[BM25]] top-30 shortlist and no corpus-specific tuning, the
batch shape reached **0.501 mean nDCG@10** against 0.504 for Voyage rerank-3, 0.486 for Cohere
rerank-v3.5, and 0.404 for the unreranked BM25 order — at $0.54 per 1,000 queries. The tradeoff
is the tail: p95 near 1.4 s for one call over thirty documents, where the purpose-built
rerankers stay under half a second.

What the same run identifies as the actual differentiator is not the ranking quality but the
[[Calibrated Relevance Probability|calibration]]: on SciFact, documents scored above 0.9 were
judged relevant 76% of the time and those below 0.1, half a percent — a number a
[[Cross-Encoder]] logit does not provide.

Two practical constraints reported there: Jev's 32k-token request budget holds roughly 50
passages, so rerank depth is bounded well below what hosted rerankers accept per call; and Jev
is **hosted only**, so documents leave the caller's environment.

### The Vendor's Own Reranking Walkthrough

[[TypeSafe Cookbook - Re-ranking]] runs the same idea on [[CLERC]] legal case retrieval with
model `jev-1.12`, using the **single** shape — one call per (query, candidate) pair, 1,200 calls
across 40 queries. On a [[BM25]] top-30 shortlist that contained the correct passage for every
query, reranking moved top-1 accuracy from 5% to 18% and top-10 from 38% to 62%, at $0.0645 for
the whole run.

Two things that walkthrough makes concrete. Cost scales with **passage length**, not just
candidate count — its court-opinion passages averaged roughly 1,280 input tokens per call,
working out to about $1.61 per 1,000 queries against $0.87 for the same shape on BEIR. And the
one-question-per-pair structure is described there as expository: a production caller would ask
several questions about the same pair in one call, which is the pattern the parallel-questions
cookbook covers.

## Related Concepts

- [[Reranking]] — the use case this note documents
- [[Calibrated Relevance Probability]] — the property Jev's output has and cross-encoder logits lack
- [[Pointwise Relevance Evaluation]] — one judgment per (query, document) pair
- [[Cross-Encoder]] — the incumbent reranker architecture it is compared against
- [[LLM as Judge]] — the adjacent pattern of prompting a general model for relevance
- [[Query Routing]] · [[Search Intent]] — the classification tasks the same call shape covers

## Related Notes

- [[TypeSafe]] — the company
- [[hev-rerank]] — the open-source wrapper that packages the reranker use
- [[Hev meets Jev]] — the benchmark
- [[BEIR]] — the evaluation suite used
- [[Reasoning Reranking]] — the topic
- [[Using TypeSafe's Jev for Evals]] — as a judge rather than a ranker, via [[Langfuse]]
- [[How to Use Jev - A Practical Guide]] — the primitives, patterns and failure modes in full
- [[TypeSafe Cookbook - Re-ranking]] — the vendor's reranking walkthrough on [[CLERC]]
- [[Jevals]] — an open-source eval framework using it as a confidence-gated judge
- [[Jev - The Most Interesting Model Released This Year]] — [[Sai Yashwanth]]; the agent-loop case for keeping the uncertainty
- [[Reception of Jev]] — what named practitioners said about it, pro and con
- [[JEV vs LLM - Your Software Doesn't Want a Conversation It Wants a Decision]] — [[Sajith K]]; the price claim checked, and the decision-layer-not-substitute conclusion
