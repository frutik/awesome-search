---
title: "When There's No Conversion Rate"
tags:
  - clippings
  - search
  - evaluation
  - medium
source: "https://medium.com/@dtunkelang/when-theres-no-conversion-rate-67a372666fed"
author: "Daniel Tunkelang"
created: 2026-05-15
concepts:
  - Search Evaluation
  - Click Signals
  - Session-Based Evaluation
---

# When There's No Conversion Rate

**Source:** https://medium.com/@dtunkelang/when-theres-no-conversion-rate-67a372666fed
**Author:** [[Daniel Tunkelang]]
**Series:** Evaluating Search (Part 4 of 4)

## Summary

What do you measure when your search product has no conversion signal? Long-document search, enterprise search, internal tools — these lack the clean purchase/signup events e-commerce relies on. This article proposes proxies.

## The Problem

Some search domains lack reliable conversion signals:
- Long-document retrieval (academic, legal, enterprise)
- Internal search tools (no external revenue event)
- Exploratory browsing (goal is discovery, not a transaction)

In these contexts, "clicks still serve as a relevance signal, but they are only a weak signal."

## Alternative Metrics

1. **Dwell time** — time on clicked result; longer = more engagement. Ambiguous for long documents (did they read it, or abandon it?)
2. **Session behavior** — query repetition, pogo-sticking, progression to new queries; absence of reformulation signals satisfaction
3. **Client-side instrumentation** — scrolling depth, in-page search usage; distinguishes browsing from actual reading
4. **Retention metrics** — do users return? Better relevance increases search usage over time

## The "Change the Problem" Insight

> "Sometimes, when you can't come up with a great solution, the better strategy is to change the problem."

If click signal is too weak, improve snippets and autocomplete to strengthen the signal before trying to measure it.

User feedback buttons don't work without giving users reciprocal value for their effort.

## Series
1. [[Evaluating Good Search - Measure It]]
2. [[Measuring Searcher Behavior]]
3. [[Evaluating Search - Using Human Judgments]]
4. **When There's No Conversion Rate** (this article)

## Related Concepts

- [[Search Evaluation]]
- [[Click Signals]]
- [[Session-Based Evaluation]]
- [[Judgment Lists]]

## People

- [[Daniel Tunkelang]]
