---
title: "Using TypeSafe's Jev for Evals"
type: article
tags: [article, evaluation, llm-as-judge, calibration, observability, structured-output]
source: "https://langfuse.com/blog/2026-09-18-using-typesafes-jev-for-evals"
author:
  - "[[Annabell Schäfer]]"
published: 2026-09-18
created: 2026-09-19
publisher: "[[Langfuse]]"
concepts:
  - "[[LLM as Judge]]"
  - "[[Calibrated Relevance Probability]]"
  - "[[Staged Judging]]"
  - "[[Judgment Lists]]"
  - "[[Levels of Judge Agreement]]"
  - "[[System One Model]]"
  - "[[Clean Context]]"
topics:
  - "[[Search Quality Assurance]]"
companies:
  - "[[TypeSafe]]"
tools:
  - "[[Jev]]"
  - "[[Langfuse]]"
---

# Using TypeSafe's Jev for Evals

**Author:** [[Annabell Schäfer]]
**Published on:** [[Langfuse]]'s blog
**Source:** https://langfuse.com/blog/2026-09-18-using-typesafes-jev-for-evals
**Published:** 2026-09-18

## Summary

Uses [[Jev]] as an [[LLM as Judge|LLM-as-a-judge]] replacement for rubric verdicts, with a
worked integration that scores [[Langfuse]] traces. The interesting claim is not the cost
saving but a design one: because the model returns a probability and refuses to hide several
judgments in one question, **it forces the rubric to be written properly** — and tells you when
it hasn't been.

Most relevant here as a judging note rather than a ranking one. Relevance judgment is the same
shape as eval scoring, and the failure modes transfer directly.

## The Argument

For years, yes/no verdicts were extracted from generative models via structured outputs and
JSON schemas — paying generation prices for a binary. A model built for the decision instead of
adapted to it changes the economics of judging at volume. The trade is that it returns no
reasoning at all.

The three question types, framed for evals:

| Type | In an eval harness | Returns |
|---|---|---|
| **Choice** | Failure-mode classification | one of up to 255 options, per-option probabilities, confidence |
| **Score** | A rubric with ordered levels (up to 10) | probability-weighted value, full distribution, confidence |
| **Noul** | A binary verdict | probability it is true — **no separate confidence field** |

A practical gotcha the author flags: since a Noul carries no `confidence`, code that reads
`answer.confidence` uniformly will break on binaries. The probability *is* the belief.

## Why the Shape Improves Rubrics

Every question is evaluated **in parallel and in isolation** against the same state. Adding a
fourth question, or a fourteenth, barely changes response time, costs only that question's
tokens, and — the part that matters for judging — **cannot degrade the answers to the others**.
Speculative asking becomes viable: ask everything, discard what you don't need.

TypeSafe's docs insist each question be **atomic**, which the author notes matches standard
guidance on writing good evaluators. The consequence is the article's best point:

> Jev forces you to think in distinct categories and yes/no decisions to define what good
> means. If you do not, the answer comes back with low confidence.

A vague rubric does not silently produce confident nonsense; it produces a low-confidence
answer, which is a signal you can act on. Compare the usual [[LLM as Judge]] failure, where an
underspecified prompt yields a crisp-looking label with no indication that the criteria were
mush.

The worked example — detecting whether a chat user is disagreeing with an assistant — contrasts
a conventional judge prompt against a structured question carrying an explicit scope, an
`inspect` target, and *both* true and false criteria enumerated with inclusion lists. Writing
the false criteria explicitly is the part conventional prompts usually skip.

## Three Paths Instead of Two

Because the answer is a probability rather than a label, the threshold belongs to the
application, and the verdict can fan out three ways rather than two:

1. **Act** on high confidence.
2. **Send the middle band to a human.**
3. **Drop or flag** the rest.

This is [[Staged Judging]] expressed as a cutoff on a calibrated number, and it is the same
manoeuvre a [[Calibrated Relevance Probability]] enables at the rerank stage — prune the
confident negatives, escalate the ambiguous middle.

## Early Benchmark Results

Reported as early third-party results, not settled findings. Good Start Labs graded **6,003
rubric checks** with Jev and five LLMs on identical instructions, measuring agreement with
Claude Fable 5.1's verdict:

| Judge | Agreement with Fable 5.1 | Cost per million graded answers |
|---|---|---|
| Jev | 91.5% | $160 |
| DeepSeek V4.1 Flash | 93.5% | $260 |
| GPT-5.6 Luna | — | $400 |
| Gemini 3.8 Flash | — | $1,600 |
| Claude Fable 5.1 | (reference) | $33,000 |

The open-source comparison is the honest one the author highlights: DeepSeek was two points
better for $100 more. Note also that "agreement with one frontier model" is not accuracy — the
same methodological caveat that applies to TypeSafe's own workflow evals, and the reason
[[Levels of Judge Agreement]] exists as a concept.

The conclusion drawn is modest and sound: some decisions — routing, classification, eval
verdicts — do not need the frontier.

## Where It Falls Short as a Judge

The three that bite specifically when judging:

- **It cannot abstain.** A forced binary with no `unknown` or `needs_review` option makes the
  model pick the least wrong answer rather than decline. You must design the escape hatch
  yourself, especially before the judge is calibrated.
- **No rationale, when you need one.** Fine for designing the rubric, bad for the individual
  case — a badly scored trace comes back with no explanation, so you debug by re-reading your
  own criteria. Anything audited or customer-facing still needs a generative model on top. (Cf.
  [[Search Results Explainability]].)
- **Context rot, with an unclear limit.** The docs state plainly that the model suffers from it,
  which is awkward when agent traces are long and mostly irrelevant. The author also finds the
  documented budget inconsistent — the models page giving 64k per request and 32k for state plus
  the longest question, while OpenRouter lists 32K — and advises verifying before designing
  around it.

## Integration

Access is waitlisted, but the model is also available through OpenRouter and the Vercel AI
Gateway. The Langfuse recipe: pull observations via the API, score them with Jev, and write the
result back as a score, carrying the probability distribution in the score comment. The example
**pins the model version** (`jev-1.13.0`) precisely because the verdict applies a fixed
threshold — a version bump would move answers under a constant cutoff.

## Related Concepts

- [[LLM as Judge]] — the practice this replaces for rubric verdicts
- [[Calibrated Relevance Probability]] — the probability-not-label property, and its use as a threshold
- [[Staged Judging]] — the three-band escalation pattern
- [[Levels of Judge Agreement]] — why "agrees with a frontier model 91.5%" is not accuracy
- [[Judgment Lists]] · [[Search Evaluation]] — where relevance judging meets this
- [[Inter-Annotator Agreement]] — the human analogue of the agreement metric used here
- [[Clean Context]] · [[Context Engineering]] — the context-rot mitigation
- [[Search Results Explainability]] — what a non-generative judge cannot give you
- [[System One Model]] — the model class

## Related Notes

- [[Langfuse]] — the observability platform and publisher
- [[Jev]] · [[TypeSafe]] — the model and vendor
- [[How to Use Jev - A Practical Guide]] — overlapping failure-mode coverage
- [[TypeSafe Cookbook - Re-ranking]] — the same primitive used for ranking instead of judging
- [[Hev meets Jev]] — the independent search-side evaluation
