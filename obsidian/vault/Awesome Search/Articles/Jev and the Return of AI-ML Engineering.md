---
title: "Jev and the Return of AI/ML Engineering"
type: article
tags: [article, llm, calibration, evaluation, structured-output, opinion]
source: "https://www.linkedin.com/pulse/jev-return-aiml-engineering-han-chung-lee-jqydc/"
author:
  - "[[Han-chung Lee]]"
published: 2026-09-21
created: 2026-09-21
concepts:
  - "[[System One Model]]"
  - "[[Reinforcement Learning for Calibrated Decisions]]"
  - "[[Calibrated Relevance Probability]]"
  - "[[Expected Calibration Error]]"
  - "[[LLM as Judge]]"
  - "[[Reranking]]"
topics:
  - "[[Reception of Jev]]"
companies:
  - "[[TypeSafe]]"
tools:
  - "[[Jev]]"
---

# Jev and the Return of AI/ML Engineering

**Author:** [[Han-chung Lee]]
**Source:** https://www.linkedin.com/pulse/jev-return-aiml-engineering-han-chung-lee-jqydc/
**Published:** 2026-09-21 · LinkedIn

## Summary

A short, hostile-but-specific review of [[Jev]] from someone who runs evaluation and alignment
work for a living. The argument is structural rather than dismissive: take the four things the
launch promises, show that three of them are already available off the shelf, and the whole case
for the model rests on the fourth — [[Reinforcement Learning for Calibrated Decisions|calibration]]
— which is the one he cannot reproduce.

The conclusion is the title. If the differentiator does not hold, the fast path is not a vendor
API but building the model yourself, which is what he means by the return of AI/ML engineering.

## Taking the Four Promises Apart

Lee lists what the launch offers as calibrated decisions, structured outputs, low latency and
low cost, and argues the last three are replicable with existing models.

- **Latency and cost.** Small open-weight models land in the same envelope. He cites two
  reimplementations: a Jev-compatible API built by Eric Zhang on Qwen-3.6-35b-a3b with SGLang,
  and one by Matt Mastracci on DiffusionGemma with vLLM, reporting latency comparable to Jev on
  a DGX Spark. His generalisation is the useful part: **for small prefills, the latency and cost
  gap between autoregressive and non-autoregressive models is negligible.** A reranking call is a
  small prefill.
- **Structured outputs.** Trained into autoregressive models since the function-calling work of
  2023. Jev's three types return JSON with an answer, a probability and a confidence per
  question, which he compares to Delip Rao's AutoRubrics abstraction, due at COLM 2026.
- **The category name is marketing.** On Kahneman's own terms every fast model is System 1 —
  the range runs from plain linear regression through Transformers — so the label names a speed,
  not a class. This sharpens the objection already recorded under [[System One Model]]: the
  problem is not only that encoders do most of this, but that the term admits them.

## Where He Agrees, and It Is the Search Case

Coming from evaluation and alignment rather than product, Lee names as the most useful
application exactly the two this vault cares about: **a rubric or preference model for LLM
evaluation and alignment, and search engine reranking and optimization** — and says Jev's API
design agrees with his intuition for that shape. The endorsement is of the interface, not of the
model behind it, which is the same split [[Doug Turnbull]] arrived at from the
[[Pairwise Relevance Evaluation|pairwise]] side.

## The Calibration Objection

His central question is *what does it calibrate to?* Calibration is a property relative to a
distribution, so a blanket claim has no referent — the point already flagged under
[[Calibrated Relevance Probability]] as the out-of-distribution problem, put as an argument
against the claim being meaningful rather than against the number.

Then two measurements:

- **Valeriy M** ran 16,500 predictions across eight datasets and found calibration failures on
  seven of the eight.
- **Lee's own runs** — coin toss, two dice, and three separate UCI datasets — report high
  [[Expected Calibration Error|ECE]], with the effect most pronounced once the experiments leave
  simulated distributions for real ones.

He publishes two figures, forecast error and a reliability plot against the diagonal, and labels
the first with the caveat most people omit: *this does not establish predictive value.* Poor
calibration is not the same finding as poor accuracy, and he keeps them separate.

## Base Model or RLCD?

The sharpest contribution is a question nobody in the [[Reception of Jev|reaction]] had asked.
Lee grants the working demonstrations — Pedram's Poker Arena, Shengyao Zhuang using it as a
re-ranker, Peter Wang playing Warcraft 3 — and then suspects those capabilities come from
**Jev's base model rather than from RLCD calibration**. On the Warcraft demo he is unimpressed by
the unit behaviour, which he reads as near-random rather than deliberate.

This is the ablation the vendor has not published, reframed: the demos prove the model is
capable, not that the training method is what made it so. Nothing in this vault separates the
two.

## Why It Matters

The closing move is not anti-Jev. Reliable calibrated probabilities paired with thresholds would
be a durable advantage, which is precisely the [[Staged Judging]] argument. His position is that
this advantage is not yet observable in Jev, and that in its absence a capable team should train
its own model — the evaluation stack becoming an engineering problem again rather than a
purchasing decision.

## Caveats

- **Short opinion post**, written the same week as the other reactions. The experiments are
  described, not written up: no bin count for the ECE figures, no per-dataset numbers, no code.
- **Valeriy M's 7-of-8 result is cited, not reproduced here**, and the underlying write-up is
  not linked from the post.
- **Toy distributions dominate.** Coin tosses and dice have a known *q*, which is what makes
  them a clean calibration test and also what makes them unlike a relevance judgment.

## Related Concepts

- [[System One Model]] — the category he argues is a speed, not a class
- [[Reinforcement Learning for Calibrated Decisions]] — the claim he cannot reproduce
- [[Calibrated Relevance Probability]] — "calibrated to what?", as an argument
- [[Expected Calibration Error]] — the metric he reports
- [[LLM as Judge]] · [[Staged Judging]] — the use he endorses
- [[Reranking]] — the other use he endorses
- [[Pairwise Relevance Evaluation]] — the adjacent judging frame

## Related Notes

- [[Jev]] · [[TypeSafe]] — the model and vendor
- [[Reception of Jev]] — where this piece sits in the wider argument
- [[Adapting Jev to Your Domain with GEPA]] — the other independent ECE measurement, on a real corpus
- [[Hev meets Jev]] — the bucket-level calibration reading that came out favourable
- [[JEV vs LLM - Your Software Doesn't Want a Conversation It Wants a Decision]] — the other audit of the launch claims
- [[Introducing System One Models & Jev]] — the announcement being answered
