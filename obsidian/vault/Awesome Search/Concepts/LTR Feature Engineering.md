---
type: concept
title: "LTR Feature Engineering"
aliases:
  - feature engineering for ranking
  - ranking features
  - LTR features
tags:
  - concept
  - ranking
  - learning-to-rank
  - feature-engineering
  - search
created: 2026-06-13
---

# LTR Feature Engineering

## Why features matter

[[Learning to Rank|LTR]] models are only as good as the signals fed into them. The model learns which features predict relevance, but it can only work with what you give it. Feature engineering is where most of the practical leverage lies — a well-chosen 20-feature set often outperforms a 200-feature model built on weak signals.

A feature is useful if it helps answer one of three questions:

1. **Is this product relevant to the query?** (query × document interaction)
2. **Does this user tend to prefer products like this?** (user × document personalization)
3. **Is this product generally successful/popular?** (document-level popularity/quality)

The most valuable features are usually interaction features between `query × product` or `user × product`, not raw product attributes alone.

---

## Feature taxonomy

### 1. Document/product features

Raw attributes of the item being ranked. Useful as inputs to interaction and personalization features; less useful on their own.

| Feature | Example value | Value alone | Best use |
|---|---|---|---|
| `brand` | Nike | Medium | → `brand_match`, `user_brand_affinity` |
| `category` | Running Shoes | Medium | → `category_match`, `user_category_affinity` |
| `gender` | Women | Medium | → `gender_match`, `user_gender_affinity` |
| `price_bucket` | 100–150 | Medium | → `user_price_affinity`, price competitiveness |
| `in_stock` | true | Useful | Directly rankable |
| `rating_bucket` | 4.5+ | Useful | Directly rankable |
| `color` | Red | Low–medium | → `color_match`, `user_color_affinity` |
| `material` | Leather | Low | → `material_match` in niche domains |
| `size` | XL | Low | Only useful if not pre-filtered (see below) |
| `weight` | 500g | Very low | Domain-specific |

**Note on size**: many pipelines filter by size *before* ranking, so every candidate is the right size — the feature then carries zero discriminating information. Only add size if your retrieval stage does not pre-filter.

---

### 2. Query × product interaction features

These are the highest-value features. They capture how well the product matches what the user typed.

| Feature | Example condition | Strength |
|---|---|---|
| `brand_match` | query = "nike shoes" AND product.brand = Nike | Very strong |
| `category_match` | query = "running shoes" AND product.category = Running Shoes | Very strong |
| `color_match` | query = "red shoes" AND product.color = Red | Strong when color appears in queries |
| `gender_match` | query = "women's running shoes" AND product.gender = Women | Strong in apparel |
| `material_match` | query = "leather boots" AND product.material = Leather | Domain-specific |
| `bm25_title` | BM25 of query against product title | Strong |
| `bm25_description` | BM25 of query against description | Medium |
| `semantic_similarity` | Cosine between query embedding and product embedding | Strong |

These features require parsing the query and comparing against product attributes — not just passing the attribute value.

---

### 3. User × product personalization features

Capture whether *this user specifically* tends to prefer items like this.

| Feature | Signal source | Strength |
|---|---|---|
| `user_brand_affinity` | User click/purchase history on brand | Very strong |
| `user_category_affinity` | User history in category | Very strong |
| `user_price_affinity` | User's historical price range | Strong |
| `user_color_affinity` | User's repeated color selections | Medium (fashion-heavy) |
| `user_material_affinity` | User's material preferences | Domain-specific |

These require user history storage and real-time lookup — typically served from a [[Feature Store]] (e.g. Redis) rather than the search index.

---

### 4. Behavioral / popularity features

Global signals about how the product performs across all users.

| Feature | Meaning | Strength |
|---|---|---|
| `ctr` | Click-through rate | Strong |
| `purchase_rate` | Conversion rate | Very strong |
| `popularity` | Raw impression/click count | Strong |
| `freshness` | Recency of product / last update | Domain-specific |

These are the easiest to add and often have a strong baseline effect. A product with high purchase rate ranks well even without personalization.

---

## Suggested minimal feature set

If starting from scratch, a practical first version:

**Document features:**
- `brand`, `category`, `gender`, `price_bucket`, `in_stock`, `rating_bucket`

**Interaction features:**
- `bm25_title`, `bm25_description`, `semantic_similarity`
- `brand_match`, `category_match`

**Behavioral features:**
- `ctr`, `purchase_rate`, `popularity`

**Personalization features (second iteration):**
- `user_brand_affinity`, `user_category_affinity`, `user_price_affinity`

This set covers the three core questions and captures most of the reachable value before introducing exotic signals.

---

## Why feature engineering is critical for LTR

- **Garbage in, garbage out** — a perfect LambdaMART model on weak features underperforms a simpler linear model on strong ones.
- **Feature orthogonality matters** — redundant features (brand + brand_with_spaces) waste model capacity; distinct signals (query_match vs user_affinity) compound.
- **Interaction features dominate** — a raw attribute like `color = Red` tells the ranker nothing. `color_match = true` (query contains "red" AND product.color = Red) is a strong signal. The model cannot learn this interaction if it only sees the raw value.
- **Behavioral signals generalize** — CTR and purchase rate work across all query types without any query parsing.
- **Personalization signals are multiplicative** — combining user affinity with query match is more powerful than either alone.

The rule of thumb: **invest in interaction features first, then personalization, then exotic product attributes**.

---

## Metarank feature types

[[Metarank]] categorizes features into:

- **item features** — static product attributes (from item metadata events)
- **user features** — aggregated behavioral signals per user
- **interaction features** — query × item or user × item combinations
- **global features** — popularity/CTR across all users

Metarank's `user_session_weight` aggregator builds user affinity profiles in real time from click events, enabling `user_brand_affinity`-style features without offline batch pipelines.

---

## Related Concepts

- [[Learning to Rank]] — the model that consumes these features
- [[LambdaMART]] — dominant algorithm; GBDTs handle non-linear feature interactions automatically
- [[Feature Store]] — infrastructure for persisting and serving features at query time
- [[Personalization]] — user × product features and affinity modeling
- [[Click Signals]] — source of behavioral features (CTR, purchase rate)
- [[Implicit Judgments]] — click data as training labels
- [[Metarank]] — open-source LTR re-ranker with built-in feature types

## Articles

- [[Hybrid Search and Learning-to-Rank with Metarank]] — [[Vsevolod Goloviznin]]; feature design for hybrid LTR
- [[Learn-to-Rank with OpenSearch and Metarank]] — [[Roman Grebennikov]]; practical feature pipeline
- [[Metarank - Personalized Ranking That Actually Reads Your Clicks]] — [[Florian Narr]]; Metarank feature configuration walkthrough
