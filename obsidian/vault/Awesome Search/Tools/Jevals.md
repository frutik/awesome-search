---
type: tool
title: "Jevals"
aliases: ["jevals"]
tags:
  - tool
  - evaluation
  - llm-as-judge
  - calibration
  - open-source
repo: https://github.com/theyashwanthsai/jevals
license: MIT
created: 2026-09-19
---

# Jevals

**Jevals** is an open-source evaluation framework for LLM and agent outputs, graded by [[Jev]]
rather than by a generative judge. Every result comes back with a confidence number attached,
which the framework uses for gating: set a bar, accept what clears it, and escalate only the
unclear cases to something more expensive.

Its own description is explicit that it is a **research preview, not meant for production yet**.
MIT licensed. Released by [[Sai Yashwanth]] alongside
[[Jev - The Most Interesting Model Released This Year]].

Repository: https://github.com/theyashwanthsai/jevals

---

## How It Works

The framework never calls your model. You run your LLM or agent independently, hand the
generated outputs to Jevals, and it grades them against checks you define in code — so it is a
judging layer over recorded outputs, not a harness.

Checks come in the three shapes the underlying model supports:

| Check | Question | Returns |
|---|---|---|
| `noul` | A yes/no criterion | confidence 0–1 |
| `score` | A multi-level rubric | a position on the scale |
| `choice` | Categorical classification | one of the named options |

Checks are organised into a `Suite`, cases are added with their inputs and outputs, and `run()`
evaluates them in parallel.

## Why the Confidence Matters

The argument the project makes for itself is an economic one that mirrors [[Staged Judging]]:
because grading every case is cheap, you can judge the **whole** set rather than sampling it,
and spend the expensive judge only on the ambiguous remainder. Sampling exists because
generative judging is costly; remove the cost and the sample is unnecessary.

The contrast drawn with a conventional [[LLM as Judge]] is worth recording. A generative judge
emits a token standing for its verdict and then writes a justification for the verdict it has
already chosen — so the output is a label plus a post-hoc rationalisation, with no honest signal
of how close the call was. A [[Calibrated Relevance Probability|calibrated probability]] supplies
that signal directly.

## Stated Limitations

From the project itself:

- Questions must avoid mathematical comparison and date/number logic — the underlying model's
  documented weakness.
- Answers fluctuate by roughly ±0.01 between identical runs, which matters if a threshold sits
  near a boundary.
- Prompt-injection attempts have limited effect but are not prevented, so judged content from
  an untrusted source remains a threat surface.

## Relevance to Search

Not a search tool. It is indexed here because relevance judging and eval scoring are the same
operation, and this is the clearest small implementation of confidence-gated judging in this
vault — the pattern a [[Judgment Lists|judgment list]] pipeline would use to grade a full query
set cheaply and route only the ambiguous pairs to a human.

## Related Concepts

- [[LLM as Judge]] — what this replaces for the verdict step
- [[Staged Judging]] — the cheap-first, escalate-the-rest architecture
- [[Calibrated Relevance Probability]] — the property the gating depends on
- [[Search Evaluation]] · [[Judgment Lists]] — the search-side equivalents
- [[Levels of Judge Agreement]] — the caution on treating judge agreement as accuracy

## Related Notes

- [[Jev]] · [[TypeSafe]] — the grading model and its vendor
- [[Sai Yashwanth]] — the author
- [[Jev - The Most Interesting Model Released This Year]] — the post that released it
- [[Using TypeSafe's Jev for Evals]] · [[Langfuse]] — the same pattern inside an observability platform
