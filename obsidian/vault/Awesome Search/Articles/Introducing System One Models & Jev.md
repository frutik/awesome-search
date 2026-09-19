---
title: "Introducing System One Models & Jev"
type: article
tags: [article, structured-output, llm, calibration, model-architecture, company-news]
source: "https://typesafe.ai/blog/introducing-system-one-models-and-jev"
author:
  - "[[Diogo Almeida]]"
published: 2026-09-15
created: 2026-09-19
concepts:
  - "[[System One Model]]"
  - "[[Reinforcement Learning for Calibrated Decisions]]"
  - "[[Calibrated Relevance Probability]]"
  - "[[LLM Guardrails]]"
  - "[[Hallucination Detection]]"
  - "[[Query Routing]]"
topics:
  - "[[Reasoning Reranking]]"
companies:
  - "[[TypeSafe]]"
tools:
  - "[[Jev]]"
---

# Introducing System One Models & Jev

**Author:** [[Diogo Almeida]] (founder, [[TypeSafe]])
**Source:** https://typesafe.ai/blog/introducing-system-one-models-and-jev
**Published:** 2026-09-15

## Summary

The launch announcement for [[TypeSafe]]'s [[Jev]] and for the model class it belongs to,
[[System One Model|System One Models]] — a vendor post, and read here as one. Its framing
question is why superhuman chat has produced so little automation, and its answer is that
chat-shaped models are the wrong interface for software: they emit strings that must be parsed
and validated, and they may always go off the rails.

It matters to this vault only indirectly. Nothing here is about search. But it is the primary
source for *why* [[Jev]]'s outputs are calibrated probabilities, which is the property that made
it work as a reranker in [[Hev meets Jev]] — so the training method described below is the
mechanism behind that result.

## The Claim

A **System One Model** is presented as a new class of frontier model built to make fast,
structured decisions software consumes directly. TypeSafe says it built a new stack for this: a
new model architecture, a parallel sampler, and a training method it calls **Reinforcement
Learning for Calibrated Decisions (RLCD)** — see
[[Reinforcement Learning for Calibrated Decisions]].

The author's compact framing: think of Jev as a frontier-intelligence function call —
unstructured state in, typed probabilistic decisions out. Jev gives up string generation
entirely in exchange for structured output that, the company argues, cannot hallucinate,
because the set of possible outputs is fixed by the caller's schema before the call.

## The Comparison as TypeSafe Draws It

| | Existing LLMs | System One + Jev |
|---|---|---|
| Trained with | RLHF / RLVR | RLCD |
| Optimizes for | Human preference, or verifiable rewards | Calibrated decisions — "epistemically honest probabilities" |
| Input emphasis | Sequential messages | Structured program state |
| Output | Strings, which must be parsed and validated | Type-safe structured values with calibrated probabilities |
| Sampling | Sequential, one token at a time | Parallel, all outputs in a single query |
| Input cost | $0.20–$10 / MTok | $0.042 / MTok |
| Output cost | ~5× input tokens | Free ("too cheap to meter") |
| End-to-end latency | 3–329 s for frontier models | 70–500 ms |
| Confidence | Overconfident and inconsistent, even when asked | Always reported; calibrated and more consistent |

The stated use cases for the System One side are the ones that look like ordinary software
rather than chat: workflows as "smart if-statements" (classify, route, score, extract, branch),
map-reduce over large data, real-time applications, and verification — scoring, judging,
guardrailing, and jailbreak detection over other models' outputs. That last category is
adjacent to [[LLM as Judge]] and [[LLM Guardrails]].

## The Evidence, and What the Post Admits About It

The post separates claims it considers cheaply falsifiable — speed per call, published pricing,
and the absence of type errors — from the ones requiring interpretation. On the latter it is
notably forthcoming about its own biases, which is the part worth recording:

**Workflow evals.** TypeSafe introduces its own evaluation format: rather than scoring against
a ground-truth label, it fixes a compute graph (a "workflow" expressed in code), gives every
model the same workflow, and treats the averaged predictions of the largest external models as
reference probabilities. Jev is described as owning the Pareto frontier by almost two orders of
magnitude, and this is the source of the **193.6× faster, 444.6× cheaper** headline figures —
which the post itself calls "on the higher end of real world gains."

Its own listed caveats:

- The workflows were built by TypeSafe's model-capabilities team, so bias "could exist," though
  they are said to be outside the training distribution.
- The reference answer is the average of two external frontier models, which the post notes
  biases results toward those vendors' models.
- The competing LLMs run through TypeSafe's own wrapper constraining them to structured
  decisions — described as the most accurate way to extract decisions from an LLM, but also
  slower and more expensive than letting them answer without probabilities.
- The hallucination/type-error comparison uses third-party routing data for the LLM side, which
  may route harder queries to better models; TypeSafe's own 0% figure is **not empirical** but
  derived from the guarantee that schema matching holds by construction.
- In the side-by-side demo, the query is "highly simplified" and the short input is
  acknowledged to flatter the parallel-sampling approach.

Reading this as a vendor post: the architecture claim (parallel typed sampling, no type errors)
is structural and easy to check; the speed and price figures are plausible but measured by the
vendor; the intelligence-parity claim rests on an evaluation TypeSafe designed, scored against
references TypeSafe selected.

## Demos

Two are described — a Doom-playing bot driven by structured game state as text (roughly 10
queries per second, about $7/hour), and Wikiracing, chosen to exercise high-cardinality choices
where not hallucinating a link compounds. A practical limit surfaces there: Jev supports a
cardinality up to 255, and higher-cardinality choices are handled by a two-stage system that
scores options independently and then makes an explicit choice.

## Naming

Both names are explained in the FAQ. **System One** comes from Daniel Kahneman's distinction
between fast, intuitive System 1 thinking and slow, deliberate System 2 reasoning — with the
post acknowledging that System 1 also connotes *error-prone*, and asserting the opposite for
this model class. **Jev** is named for the economist William Stanley Jevons, on the argument
that each order-of-magnitude drop in the cost of intelligence unlocks orders of magnitude more
uses — the Jevons-paradox reading of cheaper inference.

### Reception

The announcement reached the top of Hacker News on launch day
(https://news.ycombinator.com/item?id=49717558), and the technical objections raised there are
worth recording alongside the claims, since no independent evaluation existed at the time.
These are pseudonymous commenters, not verified findings — but several identify real gaps in
the post's reasoning.

**The latency comparison is apples-to-oranges.** The sharpest methodological objection: 70–500 ms
against 3–329 s is not a like-for-like measurement unless the LLM baseline is doing comparable
work. A model that skips generation entirely for a narrow structured task is faster more or less
by construction, so the ratio measures the task framing as much as the model.

**"Cannot hallucinate" is trivially true and oversold.** Not emitting text means not emitting
false statements; the model can still return a confidently wrong *valid* value. Commenters also
noted that structured output can be enforced from a conventional LLM with an appropriate harness,
which narrows the novelty considerably.

**Is this a rebranded encoder?** The most substantive framing, and the one that matters for
search: encoder models already skip generation, return a number readable as a probability, cannot
hallucinate, and run fast — a [[Cross-Encoder]] is exactly that. On this reading the genuine
novelty is not the absence of generation but that the **output space is specified per call**, at
cardinality up to 255, with no task-specific fine-tuning or labelled data. Whether that holds is
an open question the post does not address.

**"Not an LLM" is contested.** Readers of the documentation observed that the training appears to
apply RLCD to a pre-trained base model, which sits awkwardly with the FAQ's flat denial that Jev
is an LLM.

**RLCD and parallel sampling are asserted, not evidenced.** No paper, no ablation, nothing to
check.

**Out-of-distribution calibration.** One commenter's caveat generalises the calibration claim
correctly: on data unlike its training distribution the model will still return probabilities,
and those probabilities will be miscalibrated. Calibration is a property measured on a
distribution, not a guarantee that travels.

Enthusiasm ran in the other direction too, mostly from practitioners already constraining LLMs to
structured decisions in production — including one who framed it as a cheap general-purpose
ranking tool, which is the use [[Hev meets Jev]] went on to measure.
## Why It Sits in This Vault

The connection is [[Calibrated Relevance Probability]]. [[Hev meets Jev]] found that Jev
reranks about as well as purpose-built rerankers while returning a probability none of them
return; this post supplies the reason — the model is trained by
[[Reinforcement Learning for Calibrated Decisions|RLCD]] specifically to make its confidence
track its accuracy, rather than to satisfy a human rater or a verifier.

One cross-source tension is worth noting. The 70–500 ms latency envelope claimed here is
measured on the vendor's own workloads; the independent reranking run in [[Hev meets Jev]]
reported a p95 near 1.4 s for a single call carrying thirty documents, from a laptop with
network included. Both can be true — that call is far heavier than the post's examples — but
the published envelope is not what a deep rerank costs in practice.

## Related Concepts

- [[System One Model]] — the model class this post introduces
- [[Reinforcement Learning for Calibrated Decisions]] — the training method behind the calibration
- [[Calibrated Relevance Probability]] — what that calibration is worth in ranking
- [[LLM as Judge]] · [[LLM Guardrails]] · [[Hallucination Detection]] — the verification use cases named
- [[Query Routing]] — routing and classification as the archetypal "smart if-statement"
- [[Listwise Relevance Evaluation]] — the shape parallel per-item questions replace

## Related Notes

- [[Jev]] — the model
- [[TypeSafe]] — the company
- [[Diogo Almeida]] — the author and founder
- [[Hev meets Jev]] — the independent evaluation that brought this model into search
- [[hev-rerank]] — the reranker built on it
