---
title: "Presentation Bias"
aliases: ["survivorship bias in search", "display bias"]
tags:
  - concept
  - search-evaluation
  - click-data
---

# Presentation Bias

## Definition

The distortion in click-based relevance signals caused by the fact that **users can only interact with results that are actually displayed to them**. Results never shown cannot be clicked, so they never accumulate signal — regardless of their true relevance.

> "Shoppers won't purchase what search doesn't show them." — [[Doug Turnbull]]

## The Self-Reinforcing Cycle

```
System shows A, B, C (not D, E, F)
    ↓
Users click A, B, C (only option)
    ↓
System learns "A, B, C are preferred"
    ↓
D, E, F never shown → no clicks → never improve
    ↓
System becomes more entrenched
```

This is **survivorship bias** applied to search: only shown results can generate training signal.

## Distinction from [[Position Bias]]

| Concept | Cause | Scope |
|---|---|---|
| **[[Position Bias]]** | Users favour top positions regardless of quality | Within a shown result set |
| **Presentation Bias** | Users can't signal on what's not shown | Across the entire corpus |

Position bias is a specific manifestation of presentation bias. Both corrupt [[Click Signals]] and [[Relevance Feedback]].

## Mitigations

- **Result diversity** — surface long-tail items to create exposure
- **Active learning / exploration** — randomly promote underexposed items to gather signal
- **[[A-B Testing for Search]]** — controlled experiments to break the feedback loop
- **[[Judgment Lists]]** — human evaluators who see items independently of the system's choices
- **Inverse propensity scoring (IPS)** — weight clicks by 1/(probability of being shown) to debias

## Related Concepts

- [[Position Bias]] — rank-position-specific form of presentation bias
- [[Click Signals]] — the feedback mechanism that gets corrupted
- [[Relevance Feedback]] — broader context of user feedback signals
- [[Judgment Lists]] — unbiased alternative to click data
- [[Search Evaluation]] — why correcting for this bias matters
- [[Diversity Metrics]] — diversity as a mitigation strategy

## Articles

- [[What is Presentation Bias in Search]] — [[Doug Turnbull]]; highway sign metaphor; self-reinforcing cycle
- [[Query Understanding - Relevance Feedback]] — [[Daniel Tunkelang]]; implicit feedback biases
- [[What AI Engineers Should Know about Search]] — [[Doug Turnbull]]; point 7 of the primer

## People

- [[Doug Turnbull]] — coined "presentation bias" framing in search context
