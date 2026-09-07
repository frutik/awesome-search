---
type: topic
aliases:
  - result diversification
  - diversity in search
  - search diversification
tags:
  - topic
  - diversity
  - ranking
  - e-commerce
related_concepts:
  - "[[MMR]]"
  - "[[APD]]"
  - "[[Diversity Metrics]]"
  - "[[Query Types]]"
  - "[[Faceted Search]]"
  - "[[Search Intent]]"
  - "[[NDCG]]"
  - "[[Reranking]]"
related_topics:
  - "[[E-commerce Search]]"
  - "[[Query Understanding in Practice]]"
  - "[[Search Quality Assurance]]"
articles:
  - "[[Searching for Goldilocks]]"
  - "[[Thoughts on Search Result Diversity]]"
  - "[[How Etsy Uses Thermodynamics for Search]]"
  - "[[Targeting Broad Queries in Search]]"
  - "[[Broad and Ambiguous Search Queries]]"
  - "[[Three Pillars of Search Quality - Discovery and Inspiration]]"
  - "[[Uncovering the Bigger Picture - Comprehensive Event Understanding via Diverse News Retrieval]]"
datasets:
  - "[[LocalNews]]"
  - "[[DSGlobal]]"
people:
  - "[[Daniel Tunkelang]]"
  - "[[Andreas Wagner]]"
  - "[[Yixuan Tang]]"
  - "[[Yiqun Sun]]"
  - "[[Yuanyuan Shi]]"
  - "[[Anthony K.H. Tung]]"
created: 2026-05-16
---

# Search Result Diversity

When and how to diversify search results — ensuring a ranked list covers multiple aspects of user intent rather than converging on one interpretation.

---

## Why Diversity Matters

Diversity serves two distinct purposes:

### 1. Ambiguity Hedging
The query has multiple valid interpretations:
- "jaguar" → car, animal, OS
- "apple" → fruit, company, color
- "necklace" → gold, silver, minimalist, statement, budget, luxury

When intent is uncertain, a homogeneous result list serves only one segment of users. Diversity covers the intent space.

### 2. Redundancy Reduction
Even for clear queries, near-duplicate results waste rank positions. Showing ten barely-different black t-shirts is worse than showing three variations.

---

## The Goldilocks Problem

Too little diversity: results all look the same → boring, wastes real estate
Too much diversity: results are incoherent → users can't find what they need

The Wundt Curve describes this: user satisfaction increases with diversity up to a point, then drops as the result set becomes incoherent. Finding the optimal λ is empirical.

---

## Methods

### MMR (Maximal Marginal Relevance)
Active diversification during reranking:

`score(d) = λ × rel(d, q) − (1−λ) × max_sim(d, already_selected)`

Greedy selection: pick the next item that maximizes the MMR score. λ=1 = pure relevance, λ=0 = pure diversity.

See [[MMR]] for full formula and implementation.

### Entropy-Based (Etsy's Approach)
Measure Shannon entropy over category/attribute distributions in the result set. Set an entropy target per query type. Re-rank or inject items to meet the target.

Works well for marketplace search where items have structured categories.

### Category/Subtopic Caps (Hard Diversity)
Limit N results per category: "max 2 results per domain", "max 3 results per price tier."

Simple and interpretable but requires explicit taxonomy.

### KL-Divergence
Measure divergence between the result list's topic distribution and the corpus's topic distribution. Penalize result sets that over-concentrate on one subtopic.

---

### Sentence-Level Clustering (NEWSCOPE)

Every method above diversifies over whole-item representations — a document vector, a category label, a topic distribution. That is where redundancy hides: two articles can sit far apart as documents while repeating the same three facts.

[[Uncovering the Bigger Picture - Comprehensive Event Understanding via Diverse News Retrieval|NEWSCOPE]] moves the unit of diversity down a level. Retrieve at paragraph level, then split candidates into sentences, embed each, and cluster them with OPTICS so the number of aspects need not be fixed in advance. Each cluster stands for one distinct thing being said about the event. Selection is then greedy over *uncovered clusters* rather than over pairwise distance:

`Score(p) = |uncovered clusters ∩ clusters(p)|`

with an optional relevance-weighted variant that scores each cluster by its similarity to the query before summing, plus a `λ · Sim(query, p)` term — the same relevance/diversity dial as [[MMR]], applied to aspects instead of documents.

Two consequences worth carrying to non-news domains. The selection is **interpretable**: a cluster is inspectable, so a diversity decision can be explained rather than just scored. And it is **unsupervised** — no labeled subtopics, no stance annotation, no training.

## When to Apply Diversity

| Query type | Apply diversity? | Why |
|---|---|---|
| Broad head queries ("shoes", "necklace") | Yes — strongly | Huge intent space; homogeneity wastes real estate |
| Ambiguous queries ("python", "apple") | Yes — intent coverage | Multiple distinct interpretations |
| Category queries ("winter jackets") | Yes — moderate | Covers different styles, price points |
| Navigational ("Nike Air Max 270") | No | User intent is specific; diversity adds noise |
| Exact product ("B08N5LNQCV") | No | Single correct answer |

---

## Detecting Broad/Ambiguous Queries

Classifier features:
- Query length (shorter = more likely broad)
- Query frequency (head queries tend to be broader)
- Click entropy on historical results (high click entropy → ambiguous)
- Number of distinct categories in past click sessions for this query
- Absence of specific attributes (no color, size, brand mentioned)

---

## Diversity vs. Precision Trade-off

Standard precision metrics (NDCG@k, P@k) reward near-duplicate top hits — they don't penalize redundancy. If you optimize purely for NDCG, diversity suffers.

Diversity-aware metrics:
- **α-nDCG**: penalizes redundant relevant documents at lower ranks
- **ERR-IA**: intent-aware Expected Reciprocal Rank
- **[[APD]]**: Average Pairwise Distance — passive diversity measurement
- **Positive Cluster Coverage**: fraction of the aspects present in the relevant set that the results actually surface
- **Information Density Ratio**: aspects covered per sentence returned — penalizes padding inside results

Track APD alongside NDCG to catch diversity regressions. But note what APD cannot tell you: the last two metrics are coverage-denominated, and a system can lead on aspect coverage while sitting mid-pack on average pairwise distance. Spreading results out and covering what the reader needs are separate objectives, and NEWSCOPE's results show them diverging.

---

## Relationship to Facets

Diversity and faceted search are complementary:
- **Facets**: user explicitly constrains intent — diversity becomes less important
- **No facets selected**: diversity hedges the ambiguity the user didn't resolve

Broad-query diversification is "pre-emptive faceting" — the system makes the intent-coverage decision the user didn't.

---

## Key People

- **[[Daniel Tunkelang]]** — Searching for Goldilocks (Wundt Curve, λ-MMR), Thoughts on Search Result Diversity (KL-divergence, greedy reranking)
- **[[Andreas Wagner]]** — Three Pillars framework (Discovery pillar); [[MICES]] talk on diverse result sets showing how result positioning shapes user basket composition
- **[[Yixuan Tang]]**, **[[Yiqun Sun]]**, **[[Yuanyuan Shi]]**, **[[Anthony K.H. Tung]]** — NEWSCOPE: sentence-level clustering as the diversification unit, and the coverage-based metrics that go with it

---

## Related

- [[MMR]] — primary active diversification algorithm
- [[APD]] — passive diversity measurement
- [[E-commerce Search]] — diversity is especially critical for head queries
- [[Faceted Search]] — complementary user-controlled disambiguation
- [[Diversity Metrics]] — the metric family, including the two coverage-based measures
- [[Reranking]] — where diversification is applied
- [[LocalNews]] · [[DSGlobal]] — benchmarks for measuring aspect coverage
