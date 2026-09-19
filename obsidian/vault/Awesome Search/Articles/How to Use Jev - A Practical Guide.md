---
title: "How to Use Jev - A Practical Guide"
type: article
tags: [article, structured-output, llm, calibration, retrieval, practitioner-guide]
source: "https://dev.to/valyuai/how-to-use-jev-a-practical-guide-to-typesafes-system-one-model-g5e"
author:
  - "[[Prosper Otemuyiwa]]"
published: 2026-09-17
created: 2026-09-19
publisher: "[[Valyu AI]]"
concepts:
  - "[[System One Model]]"
  - "[[Calibrated Relevance Probability]]"
  - "[[Clean Context]]"
  - "[[Context Engineering]]"
  - "[[Query Routing]]"
  - "[[LLM Guardrails]]"
  - "[[Reranking]]"
topics:
  - "[[Reasoning Reranking]]"
companies:
  - "[[TypeSafe]]"
  - "[[Valyu AI]]"
tools:
  - "[[Jev]]"
---

# How to Use Jev - A Practical Guide

**Author:** [[Prosper Otemuyiwa]]
**Published on:** [[Valyu AI]]'s dev.to account
**Source:** https://dev.to/valyuai/how-to-use-jev-a-practical-guide-to-typesafes-system-one-model-g5e
**Published:** 2026-09-17

## Summary

A practitioner's guide to [[Jev]] covering the three question primitives, five usage patterns,
the documented failure modes, and a deliberately sceptical read of TypeSafe's benchmark. Two
things make it worth keeping despite being vendor-adjacent: it is the best single summary of
what Jev is *bad* at, and its Pattern 5 states a limit of calibrated scoring that the vendor
material does not.

**Framing to keep in view:** this is published on [[Valyu AI]]'s account, and Pattern 5 — the
search-relevant one — is built around Valyu's own retrieval API. The observation it makes is
sound and stands independently; the product placement is still product placement.

## The Three Primitives

The whole API is three question types, which the author frames as a design commitment rather
than a limitation:

| Type | Question | Returns | Bounds |
|---|---|---|---|
| **Choice** | One option from a set | `.choice`, `.probabilities`, `.confidence` | up to 255 options |
| **Score** | A position on a spectrum | `.score` (can land between levels, e.g. `1.035`), `.probabilities`, `.confidence` | 2–10 ordered levels |
| **Noul** | Yes or no, as a probability | `.noul` (0–1) | — no confidence field, because the number *is* the belief |

Two practical notes: add an explicit `other` option to a Choice so the model can decline rather
than pick the closest wrong thing; and since options cost only a few tokens each and output is
billed at zero, pass the full candidate list rather than a shortlist.

## Pattern 5: Retrieve, Then Judge

The pattern that matters for search, and the sharpest observation in the piece:

> Jev has no knowledge of the world beyond the state you hand it. It cannot look anything up.

The consequence the author draws is the part worth recording. Whatever assembles the state
decides what the model is allowed to know — so padding the state costs accuracy to context rot,
and grounding it in a weak source means the model returns *a well-calibrated judgment about bad
material*. Calibration describes confidence in a verdict; it says nothing about whether the
evidence deserved to be there.

The shape is two layers: **fetch precisely, then judge cheaply.** Retrieve wide from primary
sources, then run one Noul per passage to filter for relevance before anything expensive sees
it — the same structure as [[TypeSafe Cookbook - Re-ranking]], used as a filter rather than an
ordering. At this pricing, the filter costs less than the context window it saves. See
[[Clean Context]] and [[Context Engineering]] for the general principle.

## The Other Four Patterns

- **Speculative fan-out** — ask many questions in one call, since output tokens are free.
- **Confidence-gated routing** — branch on the returned confidence, not just the answer.
- **Composite scoring** — combine several returned numbers in code, so re-weighting is a code
  change you can A/B rather than a re-prompt.
- **The cascade** — cheap classification first, code where code suffices, a frontier model for
  the hard minority. The worked figure: roughly $6,480 instead of $30,400 per million support
  tickets, with about 800,000 answered in under half a second.

## The Failure Modes

TypeSafe publishes a "jaggedness" page listing what the model is bad at, which the author calls
unusually honest for a launch. Condensed:

- **It reads literally.** Negations, scoping words, and implied conditions land at face value.
  The tell: you explain what you *really* meant — that explanation was the missing half of the
  instruction.
- **It is not a calculator.** Counting is unreliable and error grows with the size of the thing
  counted. Iterate in code, one Noul per item.
- **Dates are text, not ordered quantities.** Ordering, gaps, and window membership are all
  unreliable. Extract with a Choice, arrange in code.
- **Context rot is real.** Accuracy falls as state fills with material the question does not
  need.
- **State is not treated as hostile.** Text engineered to argue for its own classification can
  move the answer — a real threat model wherever user-controlled content enters the state.
- **Contradictory instructions and criteria confuse it.** Criteria are an extension of the
  instruction, not a separate knob.
- **It does not generate.** No text, code, or summaries.

The meta-rule, which the author rightly notes is general design advice: don't ask a model what
code can compute exactly, and don't hide several judgments inside one question.

## The Scorecard, Read Sceptically

On TypeSafe's own four-workflow evaluation: Jev **67.8%**, level with GPT-5.6 Terra (67.9%),
behind Sol (74.1%) and Opus 5 (73.1%) — at roughly 1/200th the cost and 1/50th the latency. The
comparison the author highlights is Claude Sonnet 5 scoring *exactly* 67.8% at 293× the cost per
case and 195× the latency.

The four caveats attached, which align with what the launch post itself admits:

1. **That column is not accuracy.** There is no ground truth. Labels are a consensus built by
   averaging two frontier models at high thinking, so the figure measures *agreement with those
   two models* — which is why neither appears in the results.
2. **It is self-run.** TypeSafe designed the workflows, built the harness, ran it. No
   independent reproduction.
3. **"Cannot hallucinate" is narrower than it sounds.** The model cannot return an invalid
   value; it can return the wrong valid one, and the 0% is asserted by construction rather than
   measured. The 45.5% structured-output error figure on the LLM side is a single outlier —
   most models sit between 0.58% and 13.2%.
4. **The price may move**, and cannot be shown not to be subsidised.

## Operational Details

- Model versions: `jev-latest` currently resolves to `jev-1.13.0`. **Pin the version if you tune
  thresholds**, since answers can shift under you; the response reports the versioned ID that
  answered, so log it. (The vendor's reranking cookbook used `jev-1.12`.)
- Rate limits for `jev-1.13`: 250,000 tokens/second and 1,200 requests/minute, 429 over either,
  with both SDKs retrying on `retry-after`. TypeSafe warns these are moving without notice.
- Billing is input-only, which is what makes fan-out and long option lists cheap.
- Launch context: 2026-09-15, with $40M led by DCVC.
- The piece also characterises [[Diogo Almeida]] as having **co-invented RLHF and InstructGPT** at
  OpenAI. That is this author's framing, and it is stronger than Almeida's own account in
  [[Introducing System One Models & Jev]], which says he helped build the instruction-following
  and conversational methods that became the research behind ChatGPT. The person note follows
  Almeida's wording.

## Where the Author Would and Wouldn't Use It

**Yes:** routing and triage, moderation, relevance filtering ahead of an expensive context
window, scoring or guardrailing LLM output, tagging at volumes previously uneconomic, anything
sub-second inside a request handler.

**No:** generating anything, arithmetic or date math, decisions needing a written rationale for
an auditor, one-off complex reasoning, genuinely open answer spaces.

The closing framing: this is not a cheaper LLM but a different primitive — a function call that
happens to be intelligent, returns a type, and tells you how much to trust it.

## Related Concepts

- [[System One Model]] — the model class
- [[Calibrated Relevance Probability]] — and its limit: calibration is not grounding
- [[Clean Context]] · [[Context Engineering]] — what "retrieve and filter first" is an instance of
- [[Reranking]] — the Noul-per-passage filter, used for pruning rather than ordering
- [[Query Routing]] · [[LLM Guardrails]] · [[LLM as Judge]] — the named use cases
- [[Prompt Sensitivity]] — "it reads literally" is this failure mode, sharply stated

## Related Notes

- [[Jev]] · [[TypeSafe]] — the model and vendor
- [[Valyu AI]] — the publisher, and the retrieval half of Pattern 5
- [[Introducing System One Models & Jev]] — the launch announcement this reads sceptically
- [[TypeSafe Cookbook - Re-ranking]] — the same retrieve-then-judge shape, as a reranker
- [[Hev meets Jev]] — the independent search-side evaluation
