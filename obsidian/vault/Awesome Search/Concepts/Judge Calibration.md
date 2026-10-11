---
type: concept
title: "Judge Calibration"
aliases: ["LLM Judge Calibration", "Calibrating a Relevance Judge", "Judge-Reference Calibration"]
tags: [concept, search-evaluation, llm-judge, inter-annotator-agreement]
created: 2026-10-11
---

# Judge Calibration

**Judge calibration** is measuring an AI relevance judge against a **reference** judge on a shared random sample of query–document pairs before trusting the AI judge's ratings, per collection and per prompt. The reference is usually a person but does not have to be.

This is a different sense of the word from probability calibration ([[Calibrated Relevance Probability]], [[Expected Calibration Error]]). That kind asks whether a model's stated probabilities match observed frequencies. Judge calibration asks whether *this* judge, with *this* prompt, on *this* collection, agrees with a reference you already trust.

---

## Why It Is Needed

From [[Calibrate Before You Trust]] ([[Andrew Kornilov]]):

- LLM–human agreement on individual grades is moderate ([[LLM as Judge]]).
- The direction of a judge's bias cannot be assumed in advance.
- A reworded prompt can move agreement as much as a different model ([[Prompt Sensitivity]]).

So a judge's quality is a property of model, prompt, collection and reference together. A model name alone tells you almost nothing.

## What a Calibration Reports

Agreement is reported at more than one of the [[Levels of Judge Agreement]], because they decouple:

- **Pair level:** ordinal Krippendorff's α, exact and within-one agreement, the direction the judge leans, and a confusion table by grade ([[Inter-Annotator Agreement]]).
- **Rank level:** per-query [[NDCG|nDCG@10]] computed once with each judge's grades. Reports include [[Kendall Rank Correlation|Kendall's τ]] across queries, the mean score shift, and how many queries move by at least 0.1.

A low α alongside a high τ means the judge is wrong in a consistent way that leaves orderings intact. Only seeing both reveals which situation you are in.

## Practices

- **Freeze the sample.** Prompt changes are compared on the *same* pairs. Otherwise a prompt effect cannot be told apart from a sampling effect.
- **Keep it out of production numbers.** A calibration run should never change ratings, scores or the judging queue.
- **Chain it through escalation.** In [[Staged Judging]], calibrate the expensive judge against people, then use that calibrated judge as the reference for the cheap one. Agreement between two uncalibrated models is not evidence about either.
- **Set the bar from human agreement.** The target is how often your own raters agree with each other, not perfection.
- **Treat disagreement as a hypothesis.** A reference can be wrong, especially on ambiguous pairs.

## Limits

The figures are only as good as the reference. Agreement with a random reference comes out near zero by construction: Quepid's sample data seeds its "OSC Team Member" ratings at random, so a real calibration needs a reference who actually rated the pairs.

## Implementations

- [[Quepid]] — a Judge Calibration tab proposed in [PR #1827](https://github.com/o19s/quepid/pull/1827): pairs and ranks agreement, side-by-side re-runs on the same pairs, and applying the winning settings to the judge.

## Related Concepts

- [[Levels of Judge Agreement]] · [[Inter-Annotator Agreement]] · [[Kendall Rank Correlation]]
- [[LLM as Judge]] · [[Staged Judging]] · [[Prompt Sensitivity]] · [[Prompt Optimization]]
- [[Calibrated Relevance Probability]] — the unrelated probabilistic sense of "calibration"
- [[Judgment Lists]] · [[Search Evaluation]]

## Related Articles

- [[Calibrate Before You Trust]] — [[Andrew Kornilov]]
- [[Do LLM Judges Actually Agree With Us]] — the evidence the practice rests on

## People

- [[Andrew Kornilov]]
