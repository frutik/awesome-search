---
type: concept
title: "System One Model"
aliases: ["System One Models", "System 1 model", "decision model", "structured-decision model"]
tags:
  - concept
  - llm
  - structured-output
  - calibration
  - model-architecture
created: 2026-09-19
---

# System One Model

## Definition

**System One Model** is [[TypeSafe]]'s term for a class of model built to make fast, structured
decisions that software consumes directly, rather than to produce text a person reads. The
caller supplies unstructured *state* plus a schema of typed questions; the model returns typed
values with calibrated probabilities, and generates no free-form text at all.

The name is a vendor coinage, not an established category — it comes from Daniel Kahneman's
distinction between fast, intuitive System 1 thinking and slow, deliberate System 2 reasoning.
It is recorded here because the shape it describes turns out to matter for [[Reranking]], not
because the category is settled terminology.

## The Shape

The defining trade is **giving up string generation in exchange for a fixed output space**:

| | Chat-shaped LLM | System One Model |
|---|---|---|
| Output | Strings, parsed and validated downstream | Typed values, schema fixed before the call |
| Failure mode | Hallucination, type errors, refusals | Constrained to the declared output space |
| Sampling | Sequential, autoregressive | Parallel — all answers in one query |
| Confidence | Absent unless prompted, and then unreliable | Reported with every answer |
| Input emphasis | Sequential messages | Structured program state |

Because each question is scored independently against a shared state rather than generated in
sequence, adding questions costs little, and no answer conditions on the wording of another —
which sidesteps the ordering sensitivity that makes [[Listwise Relevance Evaluation]] fragile
and forces [[RankGPT]] into sliding windows.

## Why It Shows Up in Search

A reranker is a large number of independent, identically-shaped relevance judgments over a
shared query. That is precisely a System One query, which is why a model with no ranking
training at all can be pointed at the job: see [[Jev]], and the benchmark in
[[Hev meets Jev]], where the untuned approach landed alongside purpose-built rerankers on three
[[BEIR]] subsets.

The property that does *not* come free from any other reranker is the
[[Calibrated Relevance Probability|calibrated probability]] on each answer, which is a
consequence of how these models are trained — see
[[Reinforcement Learning for Calibrated Decisions]].

### Is This Just an Encoder?

The objection worth taking seriously, raised repeatedly in the launch discussion
(see [[Introducing System One Models & Jev]]), and sharper in a search context than a general
one: **encoder models already do most of this.** A [[Cross-Encoder]] skips generation, returns a
scalar readable as a relevance score, cannot hallucinate text, and runs fast. So "no generation,
returns a number, cheap" is not new — it is what the reranking stack has been built on for years.

On that reading the claimed novelty reduces to two things:

1. **The output space is specified per call.** A cross-encoder is trained for one scoring task
   and its head is fixed; here the question, its criteria, and the answer space are supplied at
   request time, at cardinality up to 255, with no task-specific fine-tuning or labelled data.
   That is a real difference in how the model is *used*, whatever the architecture.
2. **The output is calibrated by training objective** rather than by post-hoc fitting — see
   [[Reinforcement Learning for Calibrated Decisions]].

The honest position is that the first is a genuine ergonomic shift — building a cross-encoder
for a new criterion means assembling labels and training a head, and this removes that step —
while the second is asserted by its vendor and only lightly measured in public. Whether the
category is a new kind of model or a new interface onto a familiar one is not settled by the
material in this vault.

Related objection: the "not an LLM" framing is contested, since the documentation suggests the
training applies to a pre-trained base model.
## Limits

Worth holding alongside the category, from both the announcement and the independent run:

- **Bounded output space is the whole mechanism.** Anything requiring generation — explaining a
  ranking, rewriting a query, summarising a passage — is outside it.
- **Cardinality limits are real.** [[Jev]] supports choices up to cardinality 255, above which
  it falls back to a two-stage score-then-choose.
- **Request budgets bound batch size.** Jev's 32k-token budget holds roughly 50 passages, well
  under what hosted rerankers accept per call.
- **The category is one vendor's, for now.** The claims of parity-at-two-orders-of-magnitude
  rest on evaluations that vendor designed.

## Related Concepts

- [[Reinforcement Learning for Calibrated Decisions]] — the training method that produces the calibration
- [[Calibrated Relevance Probability]] — the property that matters in ranking
- [[Reranking]] — the search stage this shape fits
- [[Pointwise Relevance Evaluation]] — one independent judgment per candidate
- [[Listwise Relevance Evaluation]] · [[RankGPT]] — the order-sensitive alternative it avoids
- [[LLM as Judge]] · [[LLM Guardrails]] · [[Hallucination Detection]] — the verification uses claimed for the class
- [[Query Routing]] — classification and branching, the archetypal use case

## Related Notes

- [[Jev]] — the first model of this class
- [[TypeSafe]] — the company that coined the term
- [[Introducing System One Models & Jev]] — the announcement
- [[Hev meets Jev]] — the independent evaluation in a search setting
