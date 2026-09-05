---
type: concept
title: "Prompt Sensitivity"
aliases: ["prompt sensitivity", "prompt brittleness", "paraphrase sensitivity", "prompt variance"]
tags:
  - concept
  - search-evaluation
  - llm-judge
  - llm
created: 2026-09-04
---

# Prompt Sensitivity

## Definition

Prompt sensitivity is the tendency of an [[LLM as Judge|LLM judge]] to produce materially different labels when the instructions are reworded, restructured, or re-asked — including rewordings that mean the same thing. It makes the prompt part of the measuring instrument rather than a cosmetic wrapper around it, which is why a reported agreement figure is uninterpretable without the exact prompt beside it.

## The Evidence

**Paraphrases move the numbers.** Thomas and colleagues, reporting Bing-scale LLM relevance labeling, state it directly: "Systematic changes to the prompts make a difference in accuracy, but so too do simple paraphrases." Not adversarial rewrites — ordinary restatements of the same instruction.

**How you ask is a method choice, not an implementation detail.** [[Negar Arabzadeh]] and [[Charles L. A. Clarke]] compared binary, graded, pairwise and two nugget-based ways of asking across TREC DL 2019–2021 and ANTIQUE (see [[Benchmarking LLM-based Relevance Judgment Methods]]). Different framings give different labels *and* support different conclusions — pairwise preferences align best with human labels, graded and binary pointwise best with human system rankings. "Use an LLM judge" names a category, not a method.

**Context in the prompt changes leniency.** Keller et al. (2026) found judges handed only a short query "judge many more documents relevant and have a lower agreement" than judges given a proper topic description — and that generating that description automatically still recovers much of the gain.

**Domain prompting folklore does not transfer.** [[Automating Search Relevance Assessment at Scale with LLM-as-a-Judge|Allegro]] found that *removing* few-shot examples improved both accuracy and inter-rater agreement, the opposite of the usual assumption. What helped instead was structured reasoning and domain-specific business logic written into the prompt. Adding category and department metadata did nothing, because product names already carried it.

**Batching is part of the prompt too.** Allegro judged whole product pages in a single request against cloud models to save cost, then found the same batching degraded local-model reliability badly enough to revert to single-item requests — quadratic-weighted κ dropping from 0.56 to 0.34–0.37 for the local variant.

**Temperature 0 is not determinism.** Re-running the same prompt against the same model gives a distribution, not a point. Repeated runs are how you estimate that spread.

## Why It Matters for Evaluation

Prompt sensitivity is one of the reasons a judge's conclusions can be unstable in ways an average agreement score never shows. It also underlies a broader worry from Faggioli et al. (2023): if a model defines relevance, and the model's definition shifts with wording, then relevance quietly becomes whatever the prompt happened to elicit.

The practical responses are the same ones that address judge variance generally:

- **Record the prompt.** Model version, access date, exact prompt text, decoding settings and document truncation all belong in the experiment record. You will not remember in four months.
- **Treat prompt-vs-prompt as its own comparison.** "Does my answer survive me rewording the instructions?" is a distinct question from "does the model match a human", and needs its own measurement.
- **Measure run-to-run variation through to the decision.** Re-run the whole judging process several times and recompute the *final metrics and decisions*, not just the labels. If the difference between two approaches is routinely reversed or swallowed by that spread, the judge cannot resolve them however good its human correlation looks. Label flip rate and a metric gap are different quantities on different scales, so the variation has to be propagated to the metric before comparing.
- **Cross model families.** Three versions of one vendor's model do not constitute three judges.

## Related Concepts

- [[LLM as Judge]] — the judge whose output moves with the prompt
- [[Levels of Judge Agreement]] — prompt-vs-prompt is one of the judge comparisons the levels apply to
- [[Inter-Annotator Agreement]] — the statistic prompt changes shift
- [[Adversarial Relevance Judgment]] — the deliberate-manipulation counterpart to accidental sensitivity
- [[Context Engineering]] — the broader practice of controlling what a model is given
- [[Search Evaluation]] — where the instability shows up as unreliable conclusions

## Related Articles

- [[Do LLM Judges Actually Agree With Us]] — [[Andrew Kornilov]]; prompt sensitivity as one of the systematic error shapes
- [[Benchmarking LLM-based Relevance Judgment Methods]] — [[Negar Arabzadeh]], [[Charles L. A. Clarke]]; the assessment paradigm as a first-class method choice
- [[Automating Search Relevance Assessment at Scale with LLM-as-a-Judge]] — [[Joanna Marhula]], [[Mateusz Sidor]]; few-shot examples hurting, batching degrading local inference
- [[LLM-as-a-Judge When to Use Reasoning CoT and Explanations]] — [[Aparna Dhinakaran]]; prompt structure choices and their mixed evidence
