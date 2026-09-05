---
type: concept
title: "Levels of Judge Agreement"
aliases: ["judge agreement levels", "label vs leaderboard agreement", "levels of agreement", "agreement hierarchy"]
tags:
  - concept
  - search-evaluation
  - llm-judge
  - inter-annotator-agreement
created: 2026-09-04
---

# Levels of Judge Agreement

## Definition

"The judges agree" is not one claim but four, and they do not move together. When comparing any two relevance judges — two humans, a human and an [[LLM as Judge|LLM]], two LLMs, two prompts, or the same model run twice — agreement can be measured at four increasingly consequential levels:

1. **Label agreement** — do they put the same grade on the same query-document pair?
2. **Score agreement** — do they give each retrieval approach roughly the same metric value?
3. **Ranking agreement** — do they put the approaches in the same order?
4. **Decision agreement** — do they lead to the same call? Same winner, same "this difference is significant", same ship-it decision.

The distinction matters because the levels are only loosely coupled: a judge can be poor at level 1 and excellent at level 3, and — the case that hurts — excellent at level 3 while unreliable at level 4.

## Why the Levels Decouple

Two judges can disagree over thousands of individual labels and still both report "B beats A beats C". The mechanism is error cancellation: if the judge's mistakes land on every approach in much the same way, the scores can all be wrong while the *ordering* survives.

[[Andrew Kornilov]]'s analogy in [[Do LLM Judges Actually Agree With Us]] is a tape measure that reads five centimetres short. Every plank comes out wrong, but the longest plank is still the longest and the shortest still the shortest — so if all you needed was to sort them, the broken instrument did the job. The condition is that the error is the same for every plank, which is not something you get for free.

This decoupling is the founding insight of reusable test collections. Voorhees (2000) showed that swapping in a different set of human judgments changes many individual labels while the comparison between systems mostly holds. It is also why LLM judges got taken seriously at all: the judge does not have to be right about each result, only about which approach wins.

## Where the Decoupling Turns Against You

A matching leaderboard is weaker evidence than it looks. The same independence that lets level 3 survive bad level-1 agreement also lets level 3 look healthy while level 4 fails.

- **False significance at high correlation.** Otero, Parapar and Barreiro (2025) found LLM judgments "unfair at ranking top-performing systems," with "an exceedingly high rate of false positives regarding statistical differences." Crucially these occur *at high Kendall τ* — so aggregate ranking correlation alone cannot validate a close head-to-head decision. See [[Statistical Significance in Search Evaluation]].
- **Overall τ hides the top.** Nobody needs a judge to separate a terrible approach from a great one. The candidates that matter are the two or three nearly tied at the top, and a global rank correlation averages over exactly that region. A top-weighted companion measure is required.
- **The metric is a third axis.** NormasTCU (2026) reported [[NDCG]]@10 and [[MRR]] leaderboards at Kendall correlations of 0.90+ while P@10 and R@10 were markedly shakier, on the same labels.

## The Diagnostic Cases

Three results pin the levels apart empirically:

| Study | Label level | Ranking level |
|---|---|---|
| NormasTCU (2026), Portuguese legal search | Cohen's κ 0.32–0.53 — fair to moderate | Kendall τ ≥ 0.9 on nDCG@10 and MRR |
| Mohtadi et al. (2025), documents vs. summaries | "systematic shifts in label distributions and biases" | "comparable stability in systems' ranking" |
| *Judging the Judges* (2025), 42 LLM label sets | judges label things "completely differently" | nearly the same leaderboard |

Passing a ranking threshold tells you nothing about label quality, and passing a label threshold tells you nothing about ranking.

## Which Level Is the Gate

The level that gates depends on what the judgments will be used for:

- **Broad ranking of a diverse field of approaches** — stable ranking and decision agreement can be enough even with mediocre label agreement. This is the Voorhees insight, still standing.
- **Labels read by humans, reused as training data, or used to diagnose specific queries** — weak label agreement is disqualifying on its own, and no amount of leaderboard correlation rescues it.
- **Choosing between two close approaches** — high aggregate correlation cannot validate this decision at all; the deciding slice has to be adjudicated by humans.

The practical instruction that follows is to measure at least the label level *and* the decision level, and to say which one an agreement figure refers to whenever quoting it. A study that reports only one has not answered the question.

## Related Concepts

- [[LLM as Judge]] — the judges whose agreement is being decomposed
- [[Inter-Annotator Agreement]] — the statistics used at the label level, and the human-human baseline
- [[Kendall Rank Correlation]] — the statistic used at the ranking level, and the τ ≥ 0.9 convention
- [[Statistical Significance in Search Evaluation]] — the decision level, where false positives appear at high τ
- [[NDCG]] — which metric the leaderboard is built on is itself a separate axis
- [[Search Evaluation]] — the enclosing practice
- [[Judgment Lists]] — the artifact produced at the label level

## Related Articles

- [[Do LLM Judges Actually Agree With Us]] — [[Andrew Kornilov]]; the four-level framing and the evidence pinning the levels apart
- [[Benchmarking LLM-based Relevance Judgment Methods]] — [[Negar Arabzadeh]], [[Charles L. A. Clarke]]; scores judgment paradigms separately on label agreement and system-ranking agreement, finding no method wins both

## People

- [[Andrew Kornilov]] — the four-level framing
