---
title: Calibrate Before You Trust
type: article
tags:
  - article
  - llm-judge
  - search-evaluation
  - quepid
  - opinion
source: https://www.linkedin.com/pulse/calibrate-before-you-trust-andrew-kornilov-pgewf/
author:
  - "[[Andrew Kornilov]]"
published: 2026-10-11
created: 2026-10-11
concepts:
  - "[[Judge Calibration]]"
  - "[[Levels of Judge Agreement]]"
  - "[[LLM as Judge]]"
  - "[[Inter-Annotator Agreement]]"
  - "[[Kendall Rank Correlation]]"
  - "[[NDCG]]"
  - "[[Prompt Sensitivity]]"
  - "[[Staged Judging]]"
topics:
  - "[[Search Quality Assurance]]"
tools:
  - "[[Quepid]]"
  - "[[Jev]]"
companies:
  - "[[Etsy]]"
  - "[[Allegro]]"
  - "[[eBay]]"
---

# Calibrate Before You Trust

**Source:** https://www.linkedin.com/pulse/calibrate-before-you-trust-andrew-kornilov-pgewf/
**Author:** [[Andrew Kornilov]] · 2026-10-11
**Builds on:** [Quepid PR #1827](https://github.com/o19s/quepid/pull/1827) and [[Do LLM Judges Actually Agree With Us]]

## Summary

A short argument for **measuring an AI relevance judge before trusting it**. The occasion is a Judge Calibration tab proposed for [[Quepid]], which answers one question: if this AI judge had rated the pairs that a reference judge rated, how often would they agree, and where would they differ? The author argues that answering that question is worth more than the judge itself.

## The Argument

**An unmeasured judge is an unknown judge.** Three findings from the earlier survey are combined here. LLM–human agreement on individual grades is moderate. The direction of a judge's bias cannot be assumed. Rewording a prompt can move agreement as much as switching models ([[Prompt Sensitivity]]). The conclusion is that a judge's quality belongs to the model, the prompt, the book and the reference **together**. "We use GPT-4o as our judge" says almost nothing, so each judge must be measured per book and per prompt.

**Calibration here is not probability calibration.** It means having the AI judge rate a random sample of pairs a reference has already rated, then comparing the two ([[Judge Calibration]]). It is distinct from [[Calibrated Relevance Probability]].

**It is a chain, not one check.** With escalating judges ([[Staged Judging]]), first calibrate the expensive judge against people. That calibrated judge then becomes the reference for the cheap judge. Two models that look reasonable are not assumed to agree.

**Agreement is reported at more than one level** ([[Levels of Judge Agreement]]):
- *Pairs agreement*: ordinal Krippendorff's α, exact and within-one agreement, which way the judge leans, and a grade-by-grade confusion table that opens onto the pairs and the judge's explanations ([[Inter-Annotator Agreement]]).
- *Ranks agreement*: each query's top 10 scored with [[NDCG|nDCG@10]] once with each judge's grades. It reports [[Kendall Rank Correlation|Kendall's τ]] across queries, the average score shift, and how many queries move by 0.1 or more.

A judge can have a weak α and a high τ. That is the "wonky tape measure" again, and seeing both numbers is how you tell which kind of judge you have.

**Tuning becomes an experiment.** "Tune and run again" re-runs the judge on the **same frozen pairs** with a changed prompt (or, for [[Jev]], a different minimum confidence), compares runs side by side, and applies the winner. If a reworded prompt can move agreement as much as a different model, comparing runs on different samples tells you nothing. A calibration never changes a rating, a case score or the judging queue.

**The reference is the ceiling.** Quepid's sample data seeds its "OSC Team Member" ratings at random, so agreement with it comes out near zero, as it should. Set the bar against your own raters' agreement, not against perfection. When judge and reference disagree, "the judge got it wrong" is one hypothesis, not a conclusion.

**Why it matters.** The documented deployments at [[Etsy]], [[Allegro]] and [[eBay]] share one pattern: people set the standard, the model spreads it, and something keeps it honest. Calibration is the "keeps it honest" part, inside the tool people already use. An AI judge multiplies raters rather than replacing them.

## Related Concepts

- [[Judge Calibration]] — the practice the article argues for
- [[Levels of Judge Agreement]] — why pairs and ranks are reported separately
- [[LLM as Judge]] · [[Staged Judging]] · [[Prompt Sensitivity]]
- [[Inter-Annotator Agreement]] · [[Kendall Rank Correlation]] · [[NDCG]]
- [[Calibrated Relevance Probability]] — the *other* meaning of calibration, explicitly set aside

## Related Notes

- [[Do LLM Judges Actually Agree With Us]] — the survey this builds on
- [[Quepid]] — the tool the calibration tab is proposed for
- [[Search Quality Assurance]]

## People

- [[Andrew Kornilov]]
