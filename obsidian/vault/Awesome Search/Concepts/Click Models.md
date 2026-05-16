---
title: "Click Models"
aliases: ["click models", "click model", "user behavior model", "position bias model", "cascade model", "DBN", "dependent click model", "UBM", "user browsing model", "examination hypothesis"]
tags:
  - concept
  - search
  - evaluation
  - ranking
  - behavioral
created: 2026-05-16
---

# Click Models

## Definition

Click models are probabilistic models that explain observed user click patterns as a function of document relevance *and* presentation biases (especially [[Position Bias]]). They de-bias click logs to extract true relevance signals for [[Learning to Rank]] and evaluation.

Raw clicks are a noisy relevance proxy — users click on position 1 far more than position 10, regardless of relevance. Click models separate "was this clicked because it's relevant?" from "was this clicked because it was at the top?"

## The Examination Hypothesis

The foundation of most click models:

```
P(click | doc d at position i) = P(examine | position i) × P(relevant | doc d)
```

A user clicks a result only if they both (a) examine it and (b) find it relevant. Examination probability decreases with position — this is [[Position Bias]].

## Common Models

### Cascade Model
Users scan results top-to-bottom and click the first relevant result, then stop. Simple but unrealistic — users do look beyond the first relevant result.

### DBN (Dependent Click Model)
Extends cascade: after clicking, the user may be satisfied and stop, or continue scanning. Models the probability of satisfaction given a click.
- Parameters: attractiveness (relevance proxy) and satisfaction per document

### UBM (User Browsing Model)
Examination probability depends on both position *and* the position of the last click. More realistic for multi-click sessions.

### PBM (Position-Based Model)
Simplest de-biasing model: examination probability depends only on position (not on prior clicks). Position bias is estimated from randomized result serving or result interleaving experiments.

## Using Click Models in Practice

1. **Training data de-biasing**: weight click labels by inverse examination probability before using for [[Learning to Rank]] training
2. **Relevance estimation**: use click model posteriors as soft relevance labels (instead of raw clicks)
3. **Online evaluation**: infer implicit judgments from sessions without explicit ratings
4. **A/B test analysis**: control for position effects when comparing rankers

Click models connect to [[Session-Based Evaluation]] — they model the full session, not individual clicks.

## Related Concepts

- [[Click Signals]] — the raw data click models operate on
- [[Position Bias]] — the primary bias click models correct for
- [[Learning to Rank]] — downstream consumer of de-biased click signals
- [[Session-Based Evaluation]] — session-level framing of user behavior
- [[Search Evaluation]] — click models enable implicit offline evaluation
- [[Judgment Lists]] — click model outputs can substitute for manual judgments
