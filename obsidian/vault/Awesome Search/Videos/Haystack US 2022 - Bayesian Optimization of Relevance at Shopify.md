---
type: video
title: "Bayesian Optimization of Relevance at Shopify"
speaker:
  - "[[Doug Turnbull]]"
  - "[[Andy Toulis]]"
company: "[[Shopify]]"
event: "[[Haystack US]] 2022"
medium: talk / video
url: https://www.youtube.com/watch?v=YXw3fyeXgdc
published: 2022-06-22
concepts:
  - "[[Bayesian Optimization]]"
  - "[[BM25]]"
  - "[[NDCG]]"
tools:
  - "[[Elasticsearch]]"
people:
  - "[[Doug Turnbull]]"
  - "[[Andy Toulis]]"
created: 2026-08-21
---

# Bayesian Optimization of Relevance at Shopify

📺 **Watch:** https://www.youtube.com/watch?v=YXw3fyeXgdc

Haystack US 2022 talk (Charlottesville) by [[Doug Turnbull]] (then Senior Staff Engineer at [[Shopify]]) and [[Andy Toulis]] (data scientist on Shopify's relevance team, who had helped build search on the Shop app the previous year). Doug frames [[Bayesian Optimization]] as a lightweight halfway point between hand-tuned boosts and full [[Learning to Rank]]: it optimizes the *existing* ranking function's parameters — [[BM25]] `k1`/`b`, field boosts, minimum-should-match, fuzziness — without new training infrastructure, using a surrogate model over past (parameter-set, [[NDCG]]) observations instead of an expensive grid search.

## The Shopify Case Study (Andy Toulis)

Andy describes a narrow, concrete experiment: tuning the query strategy for the **product title field** at Shopify — BM25's `b` and `k1` (shared across stemmed/unstemmed variants), plus boosts on match vs. match-phrase clauses.

- **`b` (length normalization)**: the default BM25 `b` was punishing longer, more descriptive product titles — a short title like "seller moon ring" could already sit near the maximum match score purely from its length, regardless of relevance.
- **`k1` (term-frequency saturation)**: turned out to matter little in this setup, because Shopify's variant of BM25 used *binarized* term frequencies rather than raw counts — there were no repeated-term saturation curves for `k1` to shape. Lesson: if a parameter clearly won't be influential, it's reasonable to just fix it rather than let the optimizer search over it.

**First run — a loophole, not a win.** The optimizer returned a very high `b`. Investigating instead of trusting it blindly, Andy and Doug found two problems: (1) the optimizer had found a shortcut — for a one-word query like "shirt" against thousands of products, just matching the exact-length title wins on the (contaminated) training signal, so the optimizer exploited it; (2) the training data itself carried **presentation bias** — the prior search engine ran default BM25, so clicks were biased toward whatever it already surfaced. Two takeaways: optimizers exploit any loophole in the data, and the training signal must be checked for bias before trusting what it teaches.

**Second run — constrained and validated.** They constrained `b` to a narrow range (0.1–0.4) and re-ran. The winning region: a much flatter length-normalization curve (long titles no longer punished) and a shift of weight toward phrase matching. Rather than taking the single best-scoring configuration, they looked at the distribution of near-best configurations to sanity-check which parameters were actually doing work — confirming `k1` (`k`) was contributing little (as expected, given binarized term frequencies), while the phrase-match boost consistently clustered near its upper bound.

**Result:** on held-out data — including an independently, manually-labeled dataset not derived from the old production engine — the retuned configuration showed clear improvements. Andy frames Bayesian parameter optimization as a way to rebalance an already-reasonable ranking strategy without the infrastructure cost of full Learning to Rank.

## Doug's Framing (Q&A)

Bayesian optimization constrains search to the *existing* ranking function's parameter space, unlike Learning to Rank (e.g. LambdaMART, deep models), which learns an arbitrary functional form. That makes it simpler infrastructure and a semi-manual, human-in-the-loop process — informing tuning decisions rather than fully automating them — and a reasonable starting point before committing to LTR. Training data for the offline evaluation came from a standard dynamic Bayesian network click model, since the app being optimized didn't yet have real usage data of its own.

## Related Concepts
- [[Bayesian Optimization]]
- [[BM25]] — the `k1`/`b` parameters being tuned
- [[Learning to Rank]] — the more infrastructure-heavy alternative this sits "halfway" toward
- [[NDCG]] — the offline metric used to score candidate configurations

## Related Articles
- [[Bayesian BM25 is Cool]] — a different (score-calibration) use of Bayesian methods on BM25 by [[Doug Turnbull]]

## People
- [[Doug Turnbull]] · [[Andy Toulis]]

## Companies
- [[Shopify]] · [[OpenSource Connections]] (host)
