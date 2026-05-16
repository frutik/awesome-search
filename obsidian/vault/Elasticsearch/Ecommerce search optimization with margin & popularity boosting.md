---
title: "Ecommerce search optimization with margin & popularity boosting"
source: "https://www.elastic.co/search-labs/blog/ecommerce-search-optimization-query-governed"
author:
  - "[[Alexander Marquardt]]"
  - "[[Honza Král]]"
  - "[[Taylor Roy]]"
published: 2026-05-12
created: 2026-05-15
description: "Learn how to optimize ecommerce search using margin and popularity boosting. This blog explains how a governed control plane treats economic optimization in Elasticsearch."
tags:
  - "clippings"
---
2New to Elasticsearch? Join our [getting started with Elasticsearch](https://www.elastic.co/virtual-events/getting-started-elasticsearch) webinar. You can also start a [free cloud trial](https://cloud.elastic.co/registration) or try Elastic on your [machine](https://github.com/elastic/start-local) now.

Parts 1 through 6 of this series describe a governed control plane that classifies intent, enforces constraints, resolves conflicts, personalizes results, and routes to the appropriate retrieval strategy. This post introduces a different objective: ensuring the retailer's business priorities influence which of those relevant products rank highest, with that optimization governed per query through policies rather than applied as a static global setting.

In most [ecommerce](https://www.elastic.co/enterprise-search/ecommerce "Fast & scalable e-commerce search") deployments, economic signals, like profit margin and product popularity, are either ignored in search ranking or applied as static, global weights. A fixed margin boost might push high-margin products up across every query, which works for "chocolate" (where shoppers are open to suggestion) but backfires for "baby formula" (where shoppers want the trusted, popular brand).

The governed control plane makes it possible to treat economic optimization as a per-query decision, expressed as policy data and managed through the same admin UI as every other governance mechanism. A merchandiser can say "for chocolate queries, prioritize margin" and "for baby formula queries, prioritize popularity", without writing code, without deploying changes, and with full auditability.

For the mathematical foundation of margin and popularity boosting in [Elasticsearch](https://elastic.co/elasticsearch), including the logarithmic scaling formula and factor tuning explanation, see [Boosting e-commerce search by profit and popularity with the function score query in Elasticsearch](https://www.elastic.co/search-labs/blog/function-score-query-boosting-profit-popularity-elasticsearch).

## Two business signals: Margin and popularity

Every product document in our product catalog carries two numeric fields:

- **`margin`:** The product's profit margin as a percentage (0 to 200 in our dataset).
- **`popularity`:** A relative sales volume metric (0 to 10,000 in our dataset), such as weekly average units sold.

These fields represent two fundamentally different business objectives. *Margin optimization* pushes profit per transaction. *Popularity optimization* pushes conversion probability since products that many shoppers buy are products that the current shopper is likely to buy.

## The baseline: Global boosting with business signals

Before introducing per-query policy overrides, the system applies a default boost for both margin and popularity. These are implemented using Elasticsearch's `field_value_factor` with logarithmic scaling inside a `function_score` query as described in [Boosting e-commerce search by profit and popularity with the function score query in Elasticsearch](https://www.elastic.co/search-labs/blog/function-score-query-boosting-profit-popularity-elasticsearch).

The design has three properties worth noting:

- **Calibrated range.** Each signal's factor is calibrated so that it contributes at most approximately +1.0 to the boost multiplier at the top of its range. Combined with a baseline weight of 1, the final multiplier ranges from 1.0 (a product with zero margin and zero popularity) to approximately 3.0 (maximum margin plus maximum popularity). A product with strong business signals scores roughly 3x higher than an identical product with none, regardless of the [BM25](https://www.elastic.co/search-labs/blog/lexical-and-semantic-search-with-elasticsearch) score magnitude.
- **Logarithmic scaling.** The `ln1p` modifier grows fast at small values (rewarding incremental gains) but flattens at high values (preventing runaway scores from a single dominant product). This also makes the system resilient to data distribution changes: If the maximum popularity in a dataset shifts significantly, the boost curve stretches rather than breaking.
- **Multiplicative, not additive.** The business-signal boost is applied multiplicatively against BM25 (`boost_mode: "multiply"`) rather than added to it. BM25 scores vary dramatically across queries, so an additive boost would have inconsistent impact depending on query specificity. Multiplicative scaling guarantees a consistent percentage uplift regardless of the absolute BM25 magnitude.

## Per-query boosting overrides through policies

The default weights (1.0 for both margin and popularity) apply to every query. But the governed control plane makes it possible to override these weights on a per-query basis through the same policy engine described in [Part 3](https://www.elastic.co/search-labs/blog/ecommerce-search-governance-control-plane-architecture) and [Part 4](https://www.elastic.co/search-labs/blog/elasticsearch-percolator-search-governance).

Each policy document has two optional fields: `margin_boost_weight` and `popularity_boost_weight`. When a policy matches a query and includes weight overrides, those values flow through to the `function_score` construction, replacing the defaults.

## Why per-query control matters

Consider two queries and why they demand different economic optimization strategies.

### Margin boosting: Chocolate

A shopper searching for "chocolate" is browsing. They'll be satisfied by many chocolate-related products. The retailer's store-brand chocolate truffles at 60% margin might be just as appealing as the name-brand bar at 15% margin. Aggressive margin boosting pays for itself if the shopper doesn't care which chocolate they purchase and buys one of the margin-boosted hits.

### Chocolate results without margin boosting

To isolate the effect of per-query margin boosting, we first disable margin boosting entirely for this query (margin boost weight: 0). Without any margin signal, the ranking is driven by text relevance. In our dataset, the first hit has a margin of 10 and the next one has a margin of 84 (out of a max of 200) as follows:

![A data interface displays two chocolate products, each with pricing, nutritional details, and metadata, with a focus on the margin and popularity fields for both products.](https://www.elastic.co/search-labs/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fme0ej585%2Fsearch-labs-import-testing%2F12b36c0c2104fc30c87c993e751f469522a876b2-660x845.png&w=3840&q=75)

A data interface displays two chocolate products, each with pricing, nutritional details, and metadata, with a focus on the margin and popularity fields for both products.

### Setting a margin boost on queries for “chocolate”

A merchandiser who decides that “chocolate” queries should prioritize margin makes that change in the admin UI, tests it against representative queries, and promotes it to production. The change takes effect on the next query. No engineering ticket, no deployment, no code change. The following "chocolate" policy sets `margin_boost_weight: 3.0`, which ensures that searches for chocolate will aggressively promote high-margin items.

![A web interface titled “Edit rewrite policy” shows configuration fields for a search rewrite rule, with a focus on the Margin Boost Weight field.](https://www.elastic.co/search-labs/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fme0ej585%2Fsearch-labs-import-testing%2Fa70dcbffc8fdf04d9161b327f79008548646478c-1097x1052.png&w=3840&q=75)

A web interface titled “Edit rewrite policy” shows configuration fields for a search rewrite rule, with a focus on the Margin Boost Weight field.

### Chocolate results with margin boosting

With the above margin boost policy enabled, the higher-margin chocolates with a margin of 197 and 184 are boosted to the top of the results as follows (remember that the maximum margin in our dataset is 200):

![A data interface shows two chocolate products, with pricing, nutritional details, and metadata, with a focus on the margin and popularity fields for both products.](https://www.elastic.co/search-labs/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fme0ej585%2Fsearch-labs-import-testing%2Fd22245cbc5cd2198d1f27067718c4c8719d096fe-660x940.png&w=3840&q=75)

A data interface shows two chocolate products, with pricing, nutritional details, and metadata, with a focus on the margin and popularity fields for both products.

### Popularity boosting: Baby formula

A parent searching for baby formula is not experimenting. They want the product that other parents trust. Pushing a high-margin store-brand formula above the established brand that thousands of parents are buying would feel wrong and erode trust. Popularity is the right signal here because it functions as social proof for a high-stakes purchase.

### Baby formula results without a popularity boost

To isolate the effect of per-query popularity boosting, we first disable popularity boosting entirely for this query (`popularity_boost_weight: 0`). Without any popularity signal, the ranking is driven by text relevance. In this example, the top hit has a popularity of 50 on a scale that goes up to 10,000.

![A data interface shows two infant formula products, with pricing, product details, and metadata, with a focus on the margin and popularity fields for both products.](https://www.elastic.co/search-labs/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fme0ej585%2Fsearch-labs-import-testing%2Fe8f1121de8f5982882f6ed8cef2359b2bb76e45f-651x752.png&w=3840&q=75)

A data interface shows two infant formula products, with pricing, product details, and metadata, with a focus on the margin and popularity fields for both products.

### Setting a popularity boost on queries for “baby formula”

A "baby formula" policy sets `popularity_boost_weight: 5.0` and `margin_boost_weight: 0`; formula searches prioritize what's popular, completely ignoring margin.

![A web interface titled “Edit rewrite policy” shows configuration fields for a search rewrite rule, with a focus on the Popularity Boost Weight field.](https://www.elastic.co/search-labs/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fme0ej585%2Fsearch-labs-import-testing%2F72cdf6ac8bc24dc93d3a540a6d359a5b03145cef-1083x1042.png&w=3840&q=75)

A web interface titled “Edit rewrite policy” shows configuration fields for a search rewrite rule, with a focus on the Popularity Boost Weight field.

### Baby formula results with popularity boosting

If we enable the above rule, then the most popular baby formula (Lactogen 2 with a popularity of 9979) will be boosted to the top of the results, as shown below.

![A data interface shows two baby formula products, with pricing, product details, and metadata, with a focus on the margin and popularity fields for both products.](https://www.elastic.co/search-labs/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fme0ej585%2Fsearch-labs-import-testing%2F2ff438b375cf8bf21fc5fe27ee311afe510220df-662x732.png&w=3840&q=75)

A data interface shows two baby formula products, with pricing, product details, and metadata, with a focus on the margin and popularity fields for both products.

## Disabling business signals: Clearance

Not every query benefits from economic boosting. A shopper searching for "clearance" is looking for deals; margin and popularity are both irrelevant to that intent. A high-margin product is the opposite of what the shopper wants, and a popular product may not be on clearance at all.

A "clearance" policy sets `margin_boost_weight: 0` and `popularity_boost_weight: 0`, which disables both business signals entirely. Results are ranked on pure text relevance with no economic influence. This completes the design space: Policies can amplify either signal independently, rebalance them, or turn them off altogether.

## How overrides flow through the control plane

When the percolator returns matching policies, the control plane checks for `margin_boost_weight` and `popularity_boost_weight` fields on the highest-priority matching policy. If present, those values replace the defaults in the `RewriteState`. If no matching policy includes weight overrides, the default values (1.0 for both) are used.

The weights then flow through to the `function_score` construction when the final Elasticsearch query is assembled. The structure of the `function_score` doesn't change; only the `weight` values on the margin and popularity functions.

Weight overrides participate in the same governance model as every other policy mechanism. They’re subject to priority ordering: A Christmas campaign policy with `margin_boost_weight: 0.5` will override a product-category policy with `margin_boost_weight: 3.0` if the campaign policy has higher priority. The cascading transformation model from [Part 3](https://www.elastic.co/search-labs/blog/ecommerce-search-governance-control-plane-architecture) applies: Economic optimization parameters are just another field in the policy's execution plan.

## Interaction with other policies

Per-query weight overrides compose naturally with the constraint enforcement, conflict resolution, and personalization mechanisms described in earlier parts of this series.

Consider a search for "cheap chocolate" during a Christmas campaign, with a shopper who has a purchase history and belongs to a vegan cohort. The control plane processes this query through the full governance stack:

1. The "cheap" policy extracts the price constraint and removes "cheap" from the query.
2. The "chocolate" policy sets `margin_boost_weight: 3.0` and constrains results to chocolate categories.
3. The “Christmas campaign” policy (higher priority) overrides the category constraint with seasonal categories and adjusts the price ceiling.
4. The “vegan cohort” policy applies a soft boost to vegan-certified products.
5. The margin and popularity boosts are applied with the governed weights (margin at 3.0× from the “chocolate” policy, popularity at the default 1.0×).
6. The shopper's purchase history boosts are applied as the outermost scoring layer.

Every layer stacks multiplicatively. The economic optimization weights are governed by the same policy framework that controls category constraints, campaign overrides, and cohort-specific boosts. A merchandiser can tune all of these through the admin UI, all without code changes.

This example also illustrates where economic optimization sits in the scoring stack. The layers nest in a deliberate order: the base query (keyword or semantic match), then governance constraints (hard filters and soft boosts from [Part 3](https://www.elastic.co/search-labs/blog/ecommerce-search-governance-control-plane-architecture) and [Part 4](https://www.elastic.co/search-labs/blog/elasticsearch-percolator-search-governance)), then business-signal boosts (margin and popularity with governed weights), and then purchase history personalization ([Part 6](https://www.elastic.co/search-labs/blog/elasticsearch-personalized-search-governed-ecommerce)). Each layer wraps the previous one, and the effects compound multiplicatively. Governance controls what appears. Economic optimization influences what ranks highest from the retailer's perspective. Personalization adjusts ranking further from the shopper's perspective.

## Tuning guidance

The factor values in the baseline `function_score` are calibrated for the demo dataset's field ranges. A production deployment with substantially different ranges for margin or popularity should recalibrate the factors so that each signal contributes a consistent maximum boost. The logarithmic scaling provides built-in resilience to outliers and distribution shifts, but the factors are worth reviewing whenever the underlying data changes significantly. For the calibration methodology, see [Boosting e-commerce search by profit and popularity with the function score query in Elasticsearch](https://www.elastic.co/search-labs/blog/function-score-query-boosting-profit-popularity-elasticsearch).

## From economic optimization to agentic AI

The governed control plane now handles intent classification, constraint enforcement, conflict resolution, personalization, and economic optimization, all expressed as policy data, all managed through a business-editable admin UI, and all composable through a deterministic transformation framework.

The final post in this series asks what happens when the input to this system isn’t a search string typed by a human shopper, but an intent string extracted by an AI agent, and why the deterministic properties of the governed control plane become even more critical when the upstream decision-maker is probabilistic.

## Put governed ecommerce search into practice

The per-query economic optimization described in this post (policy-governed margin and popularity weights composing with governance constraints, personalization, and campaign overrides) was designed and built by Elastic Services Engineering as part of our repeatable ecommerce search accelerators. Contact [Elastic Professional Services](https://www.elastic.co/consulting).

## Join the discussion

Have questions about search governance, retrieval strategies, or ecommerce search architecture? Join the broader [Elastic community conversation](https://discuss.elastic.co/).