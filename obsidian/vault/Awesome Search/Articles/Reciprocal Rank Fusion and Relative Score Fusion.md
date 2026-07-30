---
title: "Reciprocal Rank Fusion and Relative Score Fusion: Classic Hybrid Search Techniques"
aliases: ["Hybrid Search Blueprint Part 2", "RRF and RSF"]
type: article
source: "https://medium.com/mongodb/reciprocal-rank-fusion-and-relative-score-fusion-classic-hybrid-search-techniques-3bf91008b81d"
author:
  - "[[Erik Hatcher]]"
company: ["[[MongoDB]]"]
published: 2025-11-20
created: 2026-07-30
tags:
  - article
  - hybrid-search
  - ranking
  - score-fusion
  - mongodb
  - medium
concepts:
  - Reciprocal Rank Fusion
  - Relative Score Fusion
  - Score Normalization
  - Hybrid Search
  - Linear Score Combination
  - BM25
  - Search Results Explainability
  - Dense Vector Retrieval
topics:
  - Search Platforms
---

# Reciprocal Rank Fusion and Relative Score Fusion

**[[Erik Hatcher]]** ([[MongoDB]]) works through the two classic hybrid fusion mechanisms —
[[Reciprocal Rank Fusion]] (RRF) and [[Relative Score Fusion]] (RSF) — with full arithmetic, using a
deliberately non-search toy dataset so the mechanics aren't tangled up with lexical and vector
infrastructure.

Second article in the series:
1. [[Survey of the Hybrid Search Landscape]] — the landscape and the mantra
2. This article — RRF and RSF
3. [[Hybrid Search Blueprint Series Semantic Boosting]] — [[Semantic Boosting]]

---

## The framing: fusion doesn't care where the lists came from

Fusing two differently-ordered lists of the same documents is **mathematically unconcerned with how
those lists were created** — only that they are ranked or scored. Commonly the lists come from
lexical and vector searches, but rather than entangle RRF and RSF with those details, Hatcher
demonstrates both with documents carrying two independent variables.

> Two independent variables and a fusion technique is where it's at.

The contrived dataset: **nine restaurants**, each with a `distance` from the city center and a
`rating` averaged from user reviews.

| _id | name | distance | rating |
|---|---|---|---|
| 1 | Yummi Grub | 2 | 4.1 |
| 2 | Hao Chi Food | 15 | 4.9 |
| 3 | All Daysayuno | 5 | 4.3 |
| 4 | Soup for Supper | 3 | 3.5 |
| 5 | Salada Grande | 6 | 4.2 |
| 6 | Veggie Bites | 3 | 4.0 |
| 7 | Food Fiesta | 1 | 2.5 |
| 8 | Pizza & Pie | 4 | 4.4 |
| 9 | Burger Bizaar | 3 | 4.2 |

The decision problem is intuitive: trek out to the excellent Hao Chi Food, settle for the very close
but poorly-rated Food Fiesta, or go a little further for something pretty good? "Relevance" here is
the secret sauce — a blend of proximity and rating. Even limiting the display to five of nine, there
are **15,120 possible unique lists**.

Two input pipelines are built with plain `$sort` + `$limit`: `top_closest_ranked` (ascending
distance) and `top_rated_ranked` (descending rating).

## Reciprocal Rank Fusion (RRF)

Using rank fusion, the actual distance and rating are irrelevant — **only the order matters**. For a
document at position `r(d)` in each list:

```
RRFscore(d ∈ D) = Σ  wᵢ · 1 / (60 + r(d))
                 r∈R
```

The reciprocal of the rank is multiplied by an optional weighting factor; the final score is the sum
of those weighted reciprocals. **60 is a built-in fixed value** — basic mean reciprocal rank is
simply the inverse of the rank without that addition.

```python
rrf_results = collection.aggregate([
  {'$rankFusion': {
      'input': {'pipelines': {
          'distance_pipeline': top_closest_ranked,
          'rating_pipeline': top_rated_ranked}},
      'combination': {'weights': {
          'distance_pipeline': 30,
          'rating_pipeline': 30}},
      'scoreDetails': True}},
  {'$addFields': {
      'score': {'$meta': 'score'},
      'scoreDetails': {'$meta': 'scoreDetails'}}}
])
```

### The weight-30 rescaling trick

With the default 1.0 weights the computed scores are very low numbers with little visible
discernment between them. Because of the factor of 60 in the formula, a weight of **30.0 on each of
two pipelines** scales the summed score into a comfortable ~0.0–1.0 range, with each pipeline
contributing a maximum of ~0.5. A document at position 1 in *both* lists scores ~1.0.

### Results, and what they show

| rank | _id | name | distance | rating | score |
|---|---|---|---|---|---|
| 1 | 9 | Burger Bazaar | 3 | 4.2 | 0.944940 |
| 2 | 2 | Hao Chi Fan | 15 | 4.9 | 0.491803 |
| 3 | 7 | Food Fiesta | 1 | 2.5 | 0.491803 |
| 4 | 1 | Yummy Grub | 2 | 4.1 | 0.483871 |
| 5 | 8 | Pizza & Pie | 4 | 4.4 | 0.483871 |

Burger Bazaar is the **only restaurant appearing in both** the top-five closest and the top-five
rated, and its score is almost double the rest. Everything else appears in one list only and so caps
near 0.5.

The **ties are structural**: with a 30.0 weight on both pipelines, the best-rated and the closest
restaurant each sit at position 1 of their single list and therefore score identically. If tied
scores are unacceptable, use *different* weights per pipeline.

### Explainability

With `scoreDetails` enabled, the computation is exposed via `$meta` — for `_id:1`:

```json
{
  "value": 0.4838709677419355,
  "details": [
    {"inputPipelineName": "distance_pipeline", "rank": 2, "weight": 30.0, "details": []},
    {"inputPipelineName": "rating_pipeline",   "rank": "NA"}
  ]
}
```

Second position in the closest list, absent from the top-rated list: `30 × (1 / (60 + 2)) ≈ 0.48387`.
See [[Search Results Explainability]].

Besides the intricacies of each input pipeline, **only the weights need attention** to rank-fuse.

## Relative Score Fusion (RSF)

### Why rank alone loses information

The separation between items can be far more dramatic than their ranking position indicates. Ordered
by rating, the top three are 4.9, 4.4, 4.3 — a much bigger gap between first and second than between
second and third. Rank-based scoring cannot capture that.

The inverse problem also bites: two restaurants with the *same* rating still land in a ranked list
where rank fusion scores one higher than the other, purely on the arbitrary order they were listed.

### Producing scores

In vector and lexical searches a score is a natural artifact of searching. Here there is none, so
the `$score` stage places a computed value into the `$meta` score field.

Distance must be **inverted** — closer should score higher. Knowing nothing is further than 20,
distance is scaled up by five and subtracted from 100: distance 1 → 95, distance 10 → 50.

```python
top_closest_scored = [
  {'$score': {'score': {'$subtract': [100, {'$multiply': [5.0, "$distance"]}]},
              'normalization': 'none'}},
  {'$sort': {'score': {'$meta': 'score'}}},
  {'$limit': 5},
]
```

Rating is already a descending best-to-worst value, so it is used directly. Hatcher notes that all
documents are scored here — **any other filtering criteria must happen before `$score`**.

### Fusing

```python
{'$scoreFusion': {
    'input': {'pipelines': {'distance_pipeline': top_closest_scored,
                            'rating_pipeline':   top_rated_scored},
              'normalization': 'sigmoid'},
    'combination': {'weights': {'distance_pipeline': 1, 'rating_pipeline': 1},
                    'method': 'avg'},
    'scoreDetails': True}}
```

Where rank fusion offers only pipeline weighting and then sums, score fusion adds **optional
normalization of each pipeline's scores** before weighting and combining. Normalization options are
`none`, `sigmoid`, and `minMaxScaler`; combination is either averaging (the default) or a custom
expression. See [[Score Normalization]].

### Results — a different order

| rank | _id | name | distance | rating | computed_distance_score | score |
|---|---|---|---|---|---|---|
| 1 | 9 | Burger Bazaar | 3 | 4.2 | 85.0 | 0.992613 |
| 2 | 1 | Yummy Grub | 2 | 4.1 | 90.0 | 0.500000 |
| 3 | 4 | Soup for Supper | 3 | 3.5 | 85.0 | 0.500000 |
| 4 | 6 | Veggie Bites | 3 | 4.0 | 85.0 | 0.500000 |
| 5 | 7 | Food Fiesta | 1 | 2.5 | 95.0 | 0.500000 |
| 6 | 2 | Hao Chi Fan | 15 | 4.9 | 25.0 | 0.496304 |

The ordering differs from the rank-fused result — illustrating that consecutively ranked items may
have a wide gap between them, or be exactly the same, in ways a ranked list conceals.

### Where the numbers come from

`scoreDetails` for `_id:9`:

```json
{
  "value": 0.9926129841533635,
  "normalization": "sigmoid",
  "combination": {"method": "average"},
  "details": [
    {"inputPipelineName": "distance_pipeline", "inputPipelineRawScore": 85.0,
     "weight": 1.0, "value": 1.0},
    {"inputPipelineName": "rating_pipeline", "inputPipelineRawScore": 4.2,
     "weight": 1.0, "value": 0.9852259683067269}
  ]
}
```

Hatcher's warning follows directly: with score fusion it is **crucial to understand the range of
scores from each pipeline** and how best to combine them. Distance scores span 0.0–100.0 here while
rating scores span 0.0–5.0 — vastly different scales. Sigmoid maps the distance score of 85.0 to
1.0 and the rating of 4.2 to ~0.985, and those are then averaged.

### When the scores are real search scores

Lexical `$search` and `$vectorSearch` already provide a score, so `$score` would not be used:

- **`$vectorSearch`** scores are already in the 0.0–1.0 range, higher scores representing closer
  distances — the inverse of actual distance, the same manual inversion done above.
- **Lexical `$search`** is "a completely different scoring story." Scores derive from term and
  document frequencies via [[BM25]] plus potentially other custom scoring factors, and there is **no
  defined limit or range** they fit into. Normalizing lexical scores is likely to be warranted.

## Fusion challenges

Which technique? Which parameters? These depend on your data and desired results. Hatcher's stated
invariant: regardless of technique, **each search pipeline should put the best documents first and
descend by relevancy order**, by whatever measure that entails. The numbers in the equations come
from the ranking of the lists (RRF), the scores of the documents (RSF), the weights assigned to each
list, and the normalization technique.

His hardest rhetorical question: **should the pipeline and parameters vary by query?** Some queries
are strongly lexical (part numbers, identifiers, brand names); others get their best results from
semantic similarity (natural language, multi-modal). These fusion techniques are designed to blend
all search techniques used, but the scores, weights and settings are yours to control — and what's
right in one context may not work in another. Hence the repeated mantra: **measure, tune, repeat**.

## Takeaway

Fusing by **rank** is the easiest way to get started: the order of results from each technique is all
that matters, and each result is implicitly better than the one following it. Fusing by **score**
means one result could be vastly better than the next, or exactly equal, and those gap variances are
reflected in the end result.

Example data and pipelines are published as a notebook in MongoDB's GenAI-Showcase.

## Related Concepts

- [[Reciprocal Rank Fusion]] — the rank-based mechanism, worked in full here
- [[Relative Score Fusion]] — the score-based mechanism, worked in full here
- [[Score Normalization]] — `none` / `sigmoid` / `minMaxScaler`, and why scale mismatch matters
- [[Hybrid Search]] — the family both belong to
- [[Linear Score Combination]] — the closely related weighted-score approach
- [[BM25]] — the unbounded lexical scoring that motivates normalization
- [[Dense Vector Retrieval]] — already emits 0.0–1.0 scores, unlike lexical
- [[Semantic Boosting]] — the series' alternative that avoids list merging entirely
- [[Search Results Explainability]] — `scoreDetails` exposes the full computation

## Related Articles

- [[Survey of the Hybrid Search Landscape]] — part 1 of this series
- [[Hybrid Search Blueprint Series Semantic Boosting]] — part 3 of this series
- [[RRF is Not Enough]] — argues rank-only fusion discards too much signal
- [[Hybrid Fusion Failure - BM25 Displacing Reference Documents]] — what skipping normalization costs

## People

- [[Erik Hatcher]]

## Companies

- [[MongoDB]]
