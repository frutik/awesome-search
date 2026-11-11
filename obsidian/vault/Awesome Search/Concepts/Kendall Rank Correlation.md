---
type: concept
title: Kendall Rank Correlation
aliases:
  - Kendall's Tau
  - Kendall's tau
  - tau
  - KRR
  - rank correlation coefficient
  - Spearman's rho
  - Spearman correlation
  - Pearson correlation
  - Pearson's r
tags:
  - concept
  - search-evaluation
  - metrics
  - ranking
created: 2026-08-28
---

# Kendall Rank Correlation

## Definition

Kendall rank correlation (Kendall's tau) measures how similar two orderings of the same set of items are. It compares every pair of items and checks whether the pair is ordered the same way in both rankings (**concordant**) or the opposite way (**discordant**):

```
tau = (concordant pairs - discordant pairs) / (n choose 2)
```

Equivalently, when there are no tied ranks, tau can be computed by counting **inversions** — pairs that are out of order between the two rankings — relative to the maximum possible number of pairs:

```
tau = 1 - (4 * inversions) / (n * (n - 1))
```

**Range**: -1 to +1.
- **+1** — the two orderings are identical.
- **0** — no relationship between the orderings.
- **-1** — the second ordering is the complete reverse of the first.

Common implementations: Apache Commons Math's `KendallsCorrelation` (Java), `scipy.stats.kendalltau` (Python).

## What It Measures vs. What It Doesn't

Kendall's tau compares two *orderings* against each other — it says nothing on its own about which ordering is *better*. It requires no ground-truth relevance labels, unlike [[NDCG]] or [[MAP]], which score a ranking against [[Judgment Lists]]. This makes it useful as a diagnostic for **how much an ordering changed**, but unsuited to answering **whether the change was an improvement** — that question still needs a relevance-grounded metric (NDCG, MAP) or an online signal (CTR, conversion).

## Use in Reranking Diagnostics

A low `krr` (e.g. 0.15) means the reranker substantially reshuffled the candidates relative to their input order. For a working LTR reranker this is the expected and desired outcome: `krr` near +1.0 would mean the model is echoing the input order back with little change, i.e. adding no ranking value. A near-zero or negative `krr` on its own is not a quality signal — it only confirms that reranking did something; whether that something helped users still requires NDCG/MAP against judgments, or online CTR/conversion metrics.

## The tau >= 0.9 Convention

Kendall's tau is the standard statistic for **leaderboard agreement** — asking whether two evaluation schemes, such as human assessors and an [[LLM as Judge|LLM judge]], order a field of retrieval systems the same way. The threshold usually quoted comes from Voorhees (2000), who proposed treating two evaluation schemes correlating at 0.9 or above as equivalent, partly on the grounds that you cannot really be more precise than that. Below roughly 0.8 you are seeing genuine reordering rather than neighbours swapping.

Two things are worth keeping in view about that number. It is *a convention*, twenty-odd years old, and it has not been re-derived for LLM judges. And it is a threshold on a single level of agreement — clearing it says nothing about whether the underlying labels are any good. NormasTCU (2026) cleared tau >= 0.9 on nDCG@10 and MRR while its labels sat at Cohen's kappa 0.32-0.53. See [[Levels of Judge Agreement]].

### Overall tau hides the region you care about

An aggregate tau averages over the whole field, and most of that field is easy: nobody needs a judge to separate a terrible system from a great one. The systems that matter are the two or three nearly tied at the top, and their pairwise ordering contributes a handful of pairs to a statistic computed over all of them.

Two results make this concrete. The TREC Podcast reassessment (2026) found human-vs-LLM tau of 0.81-0.84 on the 2020 track with the top systems holding, but 0.60-0.72 on 2021, where the ordering became "much more volatile... including the *top* ranking systems" — same models, same method, one year apart. And Otero, Parapar and Barreiro (2025) found LLM judgments produce false positives on statistical significance *at high tau*, meaning a healthy overall correlation cannot validate a close head-to-head call.

The practical rule is to report a **top-weighted companion measure** alongside overall tau, and to adjudicate the deciding slice with humans rather than trusting the aggregate.

## Kendall vs Spearman vs Pearson

Papers that validate a judge often report two or three correlation coefficients side by side. They answer different questions and are not interchangeable.

| | Compares | Sensitive to | Typical use here |
|---|---|---|---|
| **Pearson's r** | the raw values: does one score rise linearly as the other does? | outliers and non-linear relationships between scores | agreement of score magnitudes, e.g. a judge's metric value per system against the human one |
| **Spearman's ρ** | ranks only: Pearson computed on the rank positions | large rank displacements, which it weights by squared distance | system-ranking agreement, often in judge challenges |
| **Kendall's τ** | ranks only: the share of item pairs ordered the same way | each discordant pair equally, however far apart | system-ranking agreement in IR, and the τ ≥ 0.9 convention |

Three practical consequences:

- **Rank coefficients ignore scale; Pearson does not.** A judge that is consistently stricter than humans can preserve the order of systems perfectly (τ = 1) while its scores sit far from the human ones. Conversely, two rankings can be identical while Pearson is below 1 because the scores are not linearly related.
- **On the same data, τ usually comes out lower than ρ or r**, because it counts pairwise disagreements rather than squared distances. Both judge papers here show this. [[Replacing Judges with Juries]] reports Pearson 0.917 against Kendall τ 0.778 for the same jury-versus-Chatbot-Arena comparison, and [[Criteria-Based LLM Relevance Judgments]] reports Spearman 0.9919 against τ 0.9483 on [[LLMJudge]]. Compare a coefficient only with the same coefficient, and hold only τ to the τ ≥ 0.9 bar.
- **Kendall's pair-counting matches how IR decisions are made.** The question is usually "does the judge put system A above system B the way humans do?". τ counts exactly that, which is one reason it became the leaderboard-agreement convention. Like the others, it weights a swap at the bottom of the list the same as one at the top. See *Overall tau hides the region you care about* above, and [[Rank-Biased Overlap]] for a top-weighted alternative.
## Use in Comparing Judgment Lists

Kendall's tau is also used to compare *judgment systems* against each other — measuring how much two different methods for producing [[Judgment Lists]] (e.g. human-rated vs. click-derived) agree on relative document ordering, as one way of sanity-checking whether a judgment list is trustworthy. See [[What Is a Judgment List?]].

## Related Concepts

- [[NDCG]] — relevance-grounded ranking quality metric; contrast with tau, which requires no relevance labels
- [[MAP]] — binary-relevance ranking metric; same contrast as NDCG
- [[Learning to Rank]] — the family of models whose reranking behavior tau can be used to diagnose
- [[Reranking]] — the stage whose input/output order shift tau measures
- [[Judgment Lists]] — judgment-comparison use case for tau
- [[Levels of Judge Agreement]] — tau measures the ranking level; label and decision agreement are separate
- [[LLM as Judge]] — the judges whose leaderboard agreement tau is most often used to certify
- [[Inter-Annotator Agreement]] — the label-level counterpart statistic
- [[Statistical Significance in Search Evaluation]] — why high tau does not license a close-call decision
- [[Search Evaluation]] — broader evaluation framework

- [[Rank-Biased Overlap]] — a top-weighted way to compare two orderings

## Tools

- [[Metarank]] — logs Kendall rank correlation (`krr`) as an operational diagnostic on every rerank request

## Articles

- [[What Is a Judgment List?]] — cites Kendall's Tau as a way to find correlation/agreement between different judgment systems
- [[Do LLM Judges Actually Agree With Us]] — [[Andrew Kornilov]]; the tau >= 0.9 convention, its provenance, and why overall tau hides the top of the leaderboard

- [[Replacing Judges with Juries]] — reports Pearson and Kendall τ for the same leaderboard comparison
- [[Criteria-Based LLM Relevance Judgments]] — reports Spearman and Kendall τ on LLMJudge
