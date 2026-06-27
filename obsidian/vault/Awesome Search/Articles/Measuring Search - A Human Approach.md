---
title: "Measuring Search, A Human Approach"
source: "https://jamesrubinstein.medium.com/measuring-search-a-human-approach-acf54e2cf33d"
author:
  - "[[James Rubinstein]]"
published: 2020-05-18
created: 2026-05-15
access: paywalled
description: "Online (A/B testing) and offline (human-rated) search evaluation are complements, not alternatives. A/B tests tell you what users did; human judgment tells you why — and catches the corner cases logs miss."
tags:
  - clippings
  - medium
  - paywalled
  - search-evaluation
  - human-judgment
  - ab-testing
concepts:
  - Search Evaluation
  - Judgment Lists
  - A-B Testing for Search
  - Click Signals
  - NDCG
---

# Measuring Search, A Human Approach

**Source**: https://jamesrubinstein.medium.com/measuring-search-a-human-approach-acf54e2cf33d
**Author**: [[James Rubinstein]]

## Summary

The second post in [[James Rubinstein]]'s "Measuring Search" series. The core claim: there are two ways to measure search relevance — **online (log-based)** and **offline (human-rated)** — and they are *complements, not alternatives*. To really measure and improve search you need both. A/B testing is the gold standard for drawing causal inference from a change, but it only tells you *what* users did, never *why*. Human judgment supplies the missing *why*.

## Online measurement tells you "what," not "why"

A/B testing splits traffic into randomized groups, gives each a different treatment, and measures the difference in a metric of interest — effectively a controlled experiment that licenses causal inference. But online metrics are **only as good as the metric you choose**. Optimizing click-through rate, for instance, can promote engaging-but-irrelevant results rather than the most relevant ones.

The illustration: for the query *"sweater,"* a cute pug in a sweater may out-engage the actual men's sweater — more clickable, less relevant. Users **satisfice**: once they find something good enough they leave, or they get distracted. So clicks are a noisy proxy, and it's easy to fool yourself into thinking results are great when you're really just surfacing your most clickable results.

## Human judgment supplies the "why"

[[Pointwise Relevance Evaluation|Human relevance rating]] gives raters a (query, document) pair and asks how relevant the document is; those ratings become scores (see [[Judgment Lists]]). Advantages of raters over live-traffic signals:

- **Captive, focused audience** — they rate every pair shown, not just the clickable ones, and aren't swayed by the "soulful gaze of the pug."
- **They explain the *why*** — raters can articulate why something is relevant, which is what ties the human-centered and metrics-driven approaches together.

Limitations — raters are human, and only a **proxy** for the user:

- They need guidance, make mistakes, take time, and cost money.
- They don't know the actual user's task or motivation. The tradeoff: a rater *can* tell you whether *Chew v. Gates* or *Priebe v. Nelson* is the better result for **"Dog Bite"** on a case-law search engine — feedback you'd never get from logs alone.

Dismissing human rating as an unnecessary tuning step is a mistake: without it you risk tuning on the wrong metric, or to the lowest common denominator. It's a **foil** against going down the wrong path.

## Bringing them together: the launch review

Every search algorithm change should get a **launch review** — a meeting weighing the overall metrics, the A/B test results, and the human ratings together. Typical tensions:

- Human DCG (see [[NDCG]]) goes up but engagement-based DCG goes down — should we ship?
- Engagement is up across the board, but raters report we're weaker on **ambiguous queries**.

Log metrics often hide corner cases that human judges catch. The purpose of the review is to *understand the impact* of the change — is it solving the user need we thought it was? — and human evaluation is what makes that understanding possible. (Rubinstein expands this into [[The Launch Review]].)

## Related Concepts

- [[Search Evaluation]] — the online/offline framing
- [[A-B Testing for Search]] — the online half
- [[Judgment Lists]] — output of human rating
- [[Pointwise Relevance Evaluation]] — the (query, document) rating task
- [[Click Signals]] — why behavioral metrics can mislead
- [[NDCG]] — the DCG metric weighed in launch reviews

## Related Articles

- [[Statistical and Human-Centered Approaches to Search Improvement]] — the "first post" this one builds on
- [[Measuring Search - Metrics Matter]] — same series, online-metrics focus
- [[The Launch Review]] — same author, deep dive on the launch-review meeting
- [[Evaluating Search - Using Human Judgments]] — Tunkelang's complementary view

## People

- [[James Rubinstein]] — author; Search/data PM (eBay, Apple, Pinterest; Product Analytics at LexisNexis)
