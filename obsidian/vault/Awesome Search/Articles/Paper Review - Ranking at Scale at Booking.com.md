---
type: article
title: "Paper Review — Ranking at Scale at Booking.com"
source: https://medium.com/@joparga3/paper-review-ranking-at-scale-at-booking-com-47978fa6d08d
author: "[[Jose Parreño]]"
published: 2024-02-01
publisher: Medium
paywall: true
companies: ["[[Booking.com]]", "[[Skyscanner]]"]
concepts: ["[[Ranking Signal Selection]]", "[[Isolated Feedback Loops]]", "[[Learning to Rank]]"]
topics: ["[[Two-Sided Marketplace Ranking]]"]
tags: [article, ranking, paper-review, paywalled]
created: 2026-08-05
---

# Paper Review — Ranking at Scale at Booking.com

> [!warning] Paywall
> Full text unavailable — this is a Medium member-only post. Summary based on
> publicly visible content only.
> Original article: https://medium.com/@joparga3/paper-review-ranking-at-scale-at-booking-com-47978fa6d08d

> [!tip] Read the primary source instead
> This post reviews an **open-access** paper. The full text of that paper is
> freely available, and the vault covers it in depth at
> [[Beyond Algorithms - Ranking at Scale at Booking.com]].

[[Jose Parreño]], a Sr. Data Science Manager at [[Skyscanner]], reviews the 2020
Booking.com paper *Beyond algorithms: Ranking at scale at Booking.com*. He
describes it as "a gold mine of how to start with any ranking project," arguing
its value is not limited to organisations operating at Booking.com's scale.

## Scope of the review

The visible portion establishes that the review covers two of the paper's
dimensions:

**Modelling**
- Defining target variables
- Feature engineering
- Biases in ranking
- Offline model evaluation

**Experimentation**
- Leakage

## The one substantive visible claim

Parreño's framing point is that **defining a target variable is difficult** in
ranking and recommendation, and that this is the foundational obstacle rather
than a preliminary detail — "Without a target variable, you simply cannot run
build a ML model." The body cuts off at that sentence, before the explanation of
*why* it is difficult.

This matches the emphasis of the underlying paper, whose signal-definition
section weighs candidate labels on satisfaction, volume, delay, and bias — see
[[Ranking Signal Selection]].

## Related Articles

- [[Beyond Algorithms - Ranking at Scale at Booking.com]] — the paper under review, covered in full

## People

- [[Jose Parreño]]
