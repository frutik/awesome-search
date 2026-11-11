---
type: article
title: "Trust or Escalate: LLM Judges with Provable Guarantees for Human Agreement"
source: "https://arxiv.org/abs/2407.18370"
pdf: "https://arxiv.org/pdf/2407.18370"
author:
  - "[[Jaehun Jung]]"
  - "[[Yejin Choi]]"
published: 2024-07-25
created: 2026-11-11
venue: "ICLR 2025"
concepts:
  - "[[Staged Judging]]"
  - "[[LLM as Judge]]"
  - "[[Judge Calibration]]"
  - "[[Expected Calibration Error]]"
  - "[[Pairwise Relevance Evaluation]]"
topics: []
tags:
  - article
  - llm-judge
  - evaluation
  - calibration
---

# Trust or Escalate: LLM Judges with Provable Guarantees for Human Agreement

**Authors:** [[Jaehun Jung]], Faeze Brahman, [[Yejin Choi]] · University of Washington, Allen Institute for AI · **arXiv:2407.18370** (2024), ICLR 2025

## Summary

LLM judges are usually chosen by habit — the strongest, most expensive model — with no guarantee of how often they agree with people. The paper makes the judge **abstain when it is not confident**, and picks the confidence threshold so that, on the cases it does decide, agreement with the human majority is at least a level the user sets, with high probability. It then chains judges of increasing cost into a cascade with the same guarantee. See [[Staged Judging]].

## Selective Evaluation

A judge returns a verdict only if its confidence is at or above a threshold λ, and abstains otherwise. The user sets a risk tolerance α (allowed disagreement) and an error level δ. On a small human-labelled calibration set, thresholds are tested from high to low (fixed-sequence testing) using an exact binomial upper bound on the disagreement rate, and the lowest threshold that keeps the bound under α is chosen. The paper proves that the resulting judge then agrees with humans at least 1 − α of the time on the cases it decides, with probability at least 1 − δ.

The guarantee holds for any reasonable confidence measure. What the confidence measure determines is **coverage** — how many cases are decided rather than abstained on.

## Simulated Annotators

Standard confidence signals turned out to be **over-confident** for pairwise preference judging, even for GPT-4-turbo: both the probability of the predicted label and a confidence the model states itself overestimate how often humans would agree.

Simulated Annotators borrows from human evaluation, where a label is trusted when several annotators agree. The judge is prompted N times, each time with K few-shot examples taken from one real annotator's preferences, and confidence is the agreement across these simulated annotators (typically K, N ≤ 5). For GPT-4 it cut [[Expected Calibration Error|expected calibration error]] by 50% and improved AUROC by 13%. It also made weaker judges' confidence estimates as reliable as GPT-4's or better, though their accuracy stayed lower. A variant that uses only majority labels, for datasets without per-annotator labels, did almost as well.

## Cascaded Selective Evaluation

Judges are ordered cheapest first — Mistral-7B, then GPT-3.5, then GPT-4 — each with its own calibrated threshold. A case goes to the next judge only when the current one is not confident, and if even the last judge is not confident the system abstains. The guarantee holds across the whole cascade, and the user does not choose which judge handles which case.

## Results

- **TL;DR summarization:** the human-agreement target was met at every level tested, including levels GPT-4 cannot reach when it judges every case. At 80% agreement, 75% of evaluations were done by Mistral-7B or GPT-3.5. Across 1,000 random splits, the method met its target in over 90% of runs, as the δ setting predicts, while baselines either failed the guarantee or gave up most coverage.
- **ChatArena:** over 80% human agreement — a level GPT-4 almost never reaches on its own — at 79.1% coverage, with 88.1% of covered cases judged by Mistral-7B or GPT-3.5 instead of GPT-4.
- **Abstentions follow difficulty:** what the judges abstained on matched what humans found subjective, not surface features such as length ratio or token overlap.

## Why It Matters

Most LLM-judge work reports how often the judge agrees with people on average. This paper changes the question to which cases a given judge can be trusted on, and answers it with a small calibration set instead of a blanket choice of the largest model. Escalating to a stronger judge, or to a person, is then something the method decides, not a default.

## Related Concepts

- [[Staged Judging]] — the cascade pattern, here with a formal guarantee
- [[Judge Calibration]] — calibrating each judge against people before trusting it
- [[Expected Calibration Error]] — how the confidence measures were compared
- [[LLM as Judge]] · [[Pairwise Relevance Evaluation]] — the pairwise preference setting

## Related Articles

- [[Replacing Judges with Juries]] — combines several cheaper judges in parallel rather than in sequence
- [[Calibrate Before You Trust]] — the practitioner's version of "calibrate each stage against a reference"

## People

- [[Jaehun Jung]] — first author
- [[Yejin Choi]] — author
