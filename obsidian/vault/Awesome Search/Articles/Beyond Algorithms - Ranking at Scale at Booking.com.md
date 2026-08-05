---
type: article
title: "Beyond Algorithms: Ranking at Scale at Booking.com"
source: https://ceur-ws.org/Vol-2697/paper3_complexrec.pdf
author: ["[[Themis Mavridis]]", "[[Soraya Hausl]]", "[[Andrew Mende]]", "[[Roberto Pagano]]"]
venue: ComplexRec-ImpactRS @ RecSys 2020 (CEUR Vol-2697)
published: 2020
companies: ["[[Booking.com]]"]
concepts: ["[[Learning to Rank]]", "[[Ranking Signal Selection]]", "[[Impression Bias]]", "[[Position Bias]]", "[[Isolated Feedback Loops]]", "[[Interleaving]]", "[[Out-of-Time Validation]]", "[[Hashing Trick]]", "[[LTR Feature Engineering]]"]
topics: ["[[Two-Sided Marketplace Ranking]]", "[[E-commerce Search]]", "[[A-B Testing for Search]]"]
tags: [article, ranking, learning-to-rank, experimentation, marketplace]
created: 2026-08-05
---

# Beyond Algorithms: Ranking at Scale at Booking.com

A practitioner paper arguing that in a commercial ranking system the *choice of
algorithm* is the least of the problems. Four Booking.com authors (all contributed
equally) walk through the three areas that actually decide whether a Machine
Learned ranker delivers business value: **Modelling**, **Experimentation**, and
**Serving**. Notably, the paper reports business impact only in *relative* terms
against an anonymized "important business metric" — a deliberate disclosure choice.

## The marketplace framing

Ranking in a two-sided marketplace carries several objectives and constraints:
surfacing accommodations that suit the customer, *and* delivering consistent
exposure to accommodation providers, *and* giving partners tools to influence
visibility per their sales strategy. The paper explicitly scopes itself to the
single objective it calls "by far the most important": catering to customer
preferences. See [[Two-Sided Marketplace Ranking]].

## Signal definition

The paper's most transferable contribution. Candidate labels are judged on four
axes — relation to user satisfaction, amount of data, delay to observe, and bias:

| Positive signal | Satisfaction | Volume | Delay | Bias |
|---|---|---|---|---|
| Property click | Weak | Large | Small | Clicking ≠ satisfaction |
| Click w/ dwell > threshold | Medium | Large/Medium | Small | Browsing time ≠ satisfaction |
| Reservation | Strong | Small | Medium (days) | Missing info, e.g. later cancellation |
| Stay | Strong | Small | Large (months) | No info on stay experience |
| Stay w/ review > threshold | Strong | Very small | Large | Who chooses to review is biased |

Booking.com settled on **reservations** as the primary positive signal — strong
satisfaction link, adequate volume, modest delay. Clicks (optionally dwell-gated)
serve as *secondary* positives, teaching the model that several options can
satisfy a user even though only one gets booked.

For negatives, the **skip-above** rule: if a user clicked a listing, everything
ranked above it was examined and deliberately passed over — a large, fast set of
weak-fit data points. Sessions with no click at all are still used, to stop the
ranker over-fitting to users who click or book. See [[Ranking Signal Selection]].

## Feature representation

- **Seasonality** — encode context (day of week, month), and make performance
  features season-relative: bucket "reservations over the last 6 months" into
  daily N-percentiles rather than using the raw count.
- **Non-linearity** — solve via algorithm (Gradient Boosting) *or* via
  categorical encoding, which lets even linear models capture non-linear relations.
- **Complexity** — human-made attributes describe the space poorly: star rating
  is standard for hotels but undefined for apartments, and hotels are only part
  of the inventory. Fix: project properties into a latent space, e.g. training
  [[Word2Vec]] over sequences of user actions (impressions, clicks, bookings).
- **Locality** — either a ranker per destination/cluster, or destination as a
  feature (watch the curse of dimensionality). Neighborhoods are too sparse to
  use raw; "is this property in the destination's top-N neighborhoods" works.
- **In-session adjustment** — similarity between a candidate and the properties
  the user clicked *earlier in this same search*, used as a live feature.

## Ranking biases

Three named biases, all reinforced by the ranker's own history:

- **[[Impression Bias]]** — customers never examine properties exhaustively or
  uniformly, so a property's propensity to be seen is set by the rankers
  previously in production.
- **[[Position Bias]]** — items nearer the top are assumed "better" and get
  disproportionate clicks and reservations.
- **User bias** — heavy users generate far more training rows, skewing the ranker
  toward them when it should serve everyone equally.

The paper surveys mitigations rather than claiming one: Inverse Propensity
Weighting, query-level IPW, and modelling position trust bias as
position-dependent noise.

## Model creation and offline evaluation

Training spans billions of sessions and terabytes. Online learning enables
out-of-core incremental training with a small memory footprint; the
[[Hashing Trick]] gives variable-size feature vectors under a memory bound.
Distributed ML is available when data exceeds disk or retraining is too slow,
but the paper is candid that there is *no consensus* on the best method.

Three evaluation disciplines worth stealing:

1. **[[Out-of-Time Validation]]** — the ranker is trained on the past to serve
   the future, so validate across time (walk-forward), never by random split.
2. **Train on displayed, test on available** — training uses what users were
   shown, but *testing must include every property available at that moment* to
   simulate real inference before computing precision, recall, MRR, or [[NDCG]].
3. **Multi-scenario evaluation** — because behavioral features drive the model,
   check customer subgroups, not just global metrics: a ranker can excel for
   returning users and fail for someone who just landed.

Offline metrics are explicitly framed as a *health check* that does not
necessarily correlate with business value.

## Experimentation: leakage

Ranking is self-learning — the model that sorts the items also shapes the data
it will be trained on. In an RCT splitting users into control and treatment:

- **Re-training leakage** — retraining mid-trial on logs pooled across both
  groups leaks customer preferences between rankers, pulling them toward similar
  recommendations and similar sorting.
- **Feature leakage** — even without retraining, time-dynamic features (e.g.
  reservations in the last day) transmit one ranker's effect into the other's inputs.

Two remedies: **freezing** data sources to pre-experiment data (cheap, but assumes
a stationary world — unacceptable when features reflect very recent performance),
or **[[Isolated Feedback Loops]]** per experiment group (clean separation, at the
cost of complexity in how the data is later used).

## Experimentation: interleaving

Concurrent ranking experiments break the independence assumption, so tests can't
simply be run in parallel. Multivariate designs and traffic-splitting into
subgroups both cost power or add complexity. Following Netflix's reported
results, Booking.com tried **team-draft [[Interleaving]]**: rather than
randomizing on the customer, results from two rankers are merged and *each
position becomes the unit of randomization*, measuring which ranker's results
users engage with more, with bootstrapping for the distribution.

Reported outcome: IL was highly sensitive to user-preference differences, with
potential for a **10–100x speedup**, allowing less traffic and more simultaneous
variants. Statistically, runtime could shrink to hours — but they still run at
least a day so results aren't decided by one timezone.

**Why it's more sensitive** — the paper's intent-segmentation argument is the
clearest explanation of interleaving's power in the vault. Segment users by intent:
low-intent users produce searches and pageviews but no bookings (noise in every
design); high-intent users book almost regardless of ranking order, so in an RCT
they *also* contribute noise, providing no evidence about ranking quality. An RCT
therefore learns only from the sliver of users who are ready to book but only if
convinced. Interleaving recovers signal from high-intent users too, since they
still pick the property that fits best — vastly increasing the number of
meaningful votes.

**Limitations, stated plainly:** a conclusive IL preference does not imply a
significant RCT effect at the usual expected effect size, and IL cannot estimate
effect size at all. So IL is a *preselection* tool between algorithms; the worst
case is advancing a suboptimal model into the RCT that follows.

## Serving

Availability must be resolved in real time across check-in/check-out, policy, and
room combinations, for searches up to a year out. Sharding parallelizes it: each
shard holds a subset of properties and a reverse index from destinations to
properties, computes availability and ranking score for its subset, and returns a
partial top-N to a coordinator that merges them into the final list. Because each
shard owns a fixed subset, availability can be precomputed and materialized for
all date/room/policy combinations. The stated tradeoff: **no shard has global
visibility into what is available.**

Feature deployment splits by lifetime — historical customer features from
key-value storage fetched on arrival; in-session and search features in memory
with an expiry; property features (static and periodically-updated performance)
via in-memory lookup tables, since passing them per request is wasteful when they
don't depend on user context. Feature-weight lookup is the remaining memory
problem, solved again with the [[Hashing Trick]]: hashing costs nanoseconds and,
with a correctly sized hash space, has negligible impact on model performance.

## Business impact

Improvements are reported as relative multiples of the first Machine Learned
model (set to 1), each measured in an RCT against control. The step changes, in
order: baseline ML model → item-to-item ranking from historical co-occurrence
→ contextual item-to-item (in-session personalization by traveller profile) →
behavioural + contextual item-to-item (e.g. reading reviews, time since last
click) → a single **full-scale Machine Learned ranker**.

The arc is the interesting part: years of incremental components, each added via
RCT, accumulated into an ensemble that eventually **plateaued**. Consolidating
every learning into one full-scale ranker that *replaced* the cooperating
components produced gains the authors describe as substantial relative to the
earlier steps.

## Notable references

- Bernardi, Mavridis & Estevez (2019), *150 Successful Machine Learning Models:
  6 Lessons Learned at Booking.com*, KDD
- Kaufman, Pitchforth & Vermeer (2017), *Democratizing online controlled
  experiments at Booking.com*, arXiv:1710.08217
- Radlinski, Kurup & Joachims (2008) — team-draft interleaving
- Agarwal et al. (2019), *Addressing Trust Bias for Unbiased Learning-to-Rank*, WWW
- Weinberger et al. (2009) — feature hashing
- [Netflix Technology Blog (2017)](https://medium.com/netflix-techblog/interleaving-in-online-experiments-at-netflix-a04ee392ec55) — the interleaving result that prompted this work

## Related Concepts

- [[Ranking Signal Selection]] — the four-axis label tradeoff
- [[Isolated Feedback Loops]] · [[Impression Bias]] · [[Out-of-Time Validation]]
- [[Interleaving]] — the online-evaluation case, deepened by this paper
- [[Position Bias]] · [[Implicit Judgments]] · [[Click Signals]]
- [[LTR Feature Engineering]] · [[Word2Vec]] · [[Hashing Trick]]

## Related Articles

- [[Machine Learning-Powered Search Ranking of Airbnb Experiences]] — same
  domain and a parallel word2vec-style listing embedding approach
- [[Listing Embeddings in Search Ranking]] — Airbnb's latent property space
- [[Learning to Rank for Flight Itinerary Search]] — travel LTR with booking as label
- [[Paper Review - Ranking at Scale at Booking.com]] — third-party review (paywalled)

## People

- [[Themis Mavridis]] · [[Soraya Hausl]] · [[Andrew Mende]] · [[Roberto Pagano]]
