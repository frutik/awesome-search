---
title: "Elasticsearch personalized search in ecommerce: Improve relevance"
source: "https://www.elastic.co/search-labs/blog/elasticsearch-personalized-search-governed-ecommerce"
author:
  - "[[Part of the series]]"
published: 2026-05-11
created: 2026-05-16
description: "Learn how to create a personalized search experience in Elasticsearch without breaking governance. This post explains strategies for improving relevance."
tags:
  - "clippings"
---
New to Elasticsearch? Join our [getting started with Elasticsearch](https://www.elastic.co/virtual-events/getting-started-elasticsearch) webinar. You can also start a [free cloud trial](https://cloud.elastic.co/registration) or try Elastic on your [machine](https://github.com/elastic/start-local) now.

[Parts 1 through 5](https://www.elastic.co/search-labs/blog/series/governed-search-patterns) of this series describe a governed control plane that classifies intent, enforces constraints, resolves policy conflicts, and routes to the appropriate retrieval strategy, all before the product catalog is queried. Every mechanism described so far treats all shoppers identically. A search for "chocolate" produces the same governed result set, whether the shopper is a vegan, a parent buying for a child's birthday, or a halal-observant consumer.

This post introduces two personalization mechanisms that extend the governed control plane without changing its architecture. Both mechanisms stack multiplicatively with the governance layer from Parts 1 through 5: Policies still fire, constraints are still enforced, conflicts are still resolved, and personalization signals are composed into the same governed query, ensuring that the results [Elasticsearch](https://elastic.co/elasticsearch) returns are already personalized.

The first mechanism boosts products the individual shopper has purchased before. The second activates cohort-specific policies based on the shopper's profile. Together, they demonstrate that personalization is not a separate system bolted alongside search or applied as post-retrieval processing; it’s a natural extension of the policy-driven control plane.

For a deep dive into the mathematics of the personalization techniques used in this post, see [Personalizing search in Elasticsearch without ML post-processing](https://alexmarquardt.com/elastic/personalizing-search-in-elasticsearch-without-ml-post-processing/) and [Cohort-aware ranking in Elasticsearch](https://www.elastic.co/search-labs/blog/ecommerce-search-relevance-cohort-aware-ranking-elasticsearch).

To see a live demonstration of how purchase history can be used to boost search results for returning customers, watch the video: [Explainable Personalization: Boosting Search with Purchase History](https://www.youtube.com/watch?v=TGf_pOWHA5M).

## Individual purchase history boosting

The simplest form of personalization is also one of the most effective: If a shopper has bought a product before, boost it when they search for something related. A shopper who regularly buys a particular brand of chocolate chip cookies should see those cookies ranked higher when they search for "cookies", not because a model predicted a preference, but because there’s direct behavioral evidence.

### How it works

When a search request includes a user identifier, as would be the case for a user that has an open session, the control plane runs two Elasticsearch queries in parallel using a thread pool:

1. The percolator query against the policy index (the same governance lookup described in Parts 3 and 4).
2. A purchase history query against a `user_purchases` index, filtered to the specific user by `term(user_id)` and then matching the current search string against that user's product titles.

These run concurrently (neither waits for the other), so the personalization lookup adds no meaningful latency to the governance pipeline.

The purchase history query uses [Elasticsearch's text analysis](https://www.elastic.co/docs/manage-data/data-store/text-analysis) (stemming, tokenization) when matching the current search string against stored product titles. This means a search for "cookies" will match a past purchase of "brownie cookies" through standard text analysis, without requiring exact string matching.

### Computing boost weights

Not all past purchases deserve the same boost. The weight accounts for two intuitive factors: how often the shopper bought the product, and how recently. A product purchased 15 times last week is a much stronger signal than a product purchased once six months ago. The weighting uses logarithmic scaling on frequency (so a single heavily purchased item doesn't overwhelm everything else) and exponential decay on recency (so older purchases fade naturally over time).

For the mathematical details of the boost formula, see [Personalizing search in Elasticsearch without ML post-processing](https://alexmarquardt.com/elastic/personalizing-search-in-elasticsearch-without-ml-post-processing/).

### How it becomes a query

The purchase history boosts are composed into the query as the outermost scoring layer, wrapping the governance policy filters and boosts from Parts 3 and 4 and any [business-signal boosts, such as margin and popularity](https://www.elastic.co/search-labs/blog/function-score-query-boosting-profit-popularity-elasticsearch) (which we’ll explore in Part 7). This means a product that’s removed by a governance policy won’t reappear because of a purchase history boost. *Governance* controls the result set; *personalization* adjusts ordering within it. Products without any purchase history are not penalized. Their governed ranking is preserved, though products with relevant purchase history will rank above them, all else being equal.

![A flowchart shows how a user’s search for “oranges” moves through an application server, a control plane, purchase history and policy lookups, and then a product catalog index to return orange product results.](https://www.elastic.co/search-labs/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fme0ej585%2Fsearch-labs-import-testing%2F80f0285bd80935703d39b7a4e1fd6094d71af0aa-545x273.jpg&w=3840&q=75)

A flowchart shows how a user’s search for “oranges” moves through an application server, a control plane, purchase history and policy lookups, and then a product catalog index to return orange product results.

### Why query Elasticsearch on every search?

The purchase history is queried from Elasticsearch on every search rather than cached in the application layer. This is a deliberate design choice. Because the query matches the current search string against product titles using Elasticsearch's text analysis pipeline, the system benefits from the same stemming, tokenization, and language handling that powers the product search itself. A cached in-memory lookup would require reimplementing that analysis or accepting cruder matching.

To see why this ordering matters, consider a shopper who previously purchased orange juice and now searches for "oranges”. The purchase history query matches "orange juice" against the search term "oranges" through text analysis and computes a boost for that product. But the governance layer has already constrained "oranges" to the produce category, filtering out orange juice entirely. The purchase history boost for orange juice is present in the query, but it has no effect because there’s no matching document in the governed result set for it to act on. The shopper sees fresh oranges, ranked by relevance and personalization. The governance guardrail holds.

The performance cost is minimal: The purchase history index is small (a user's purchase history is typically dozens to hundreds of documents, not millions), and the query runs in parallel with the percolator lookup, so it doesn't extend the critical path.

### Example query for “spring water” without user history

If a non-logged-in user or a user that has never purchased “spring water” searches, they might see results similar to the following:

![A webpage displays search results for “spring water”, showing a search bar, category and brand filters, and three product listings with details such as brand, composition, and price.](https://www.elastic.co/search-labs/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fme0ej585%2Fsearch-labs-import-testing%2F1d03558c8f6492a0999e1ac4f1d22680c8f3a6ce-1130x1028.png&w=3840&q=75)

A webpage displays search results for “spring water”, showing a search bar, category and brand filters, and three product listings with details such as brand, composition, and price.

### Example user purchase history

On the other hand, a user called Carol has a shopping history that contains the following products:

![A digital interface titled “Purchasing Profile” shows a shopper named Carol with two cohorts and a list of recently purchased items, including quantities, last purchase dates, and time since each purchase.](https://www.elastic.co/search-labs/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fme0ej585%2Fsearch-labs-import-testing%2F31c1fb789efc6cef673984e9711d571efce8ed27-661x523.png&w=3840&q=75)

A digital interface titled “Purchasing Profile” shows a shopper named Carol with two cohorts and a list of recently purchased items, including quantities, last purchase dates, and time since each purchase.

### Example search for “spring water” with the above purchase history

If Carol searches for “spring water”, she’ll see personalized results that reflect what she has purchased in the past. Looking at the purchase history above, she purchased “Carbonated Spring Water” (the green bottle) above, about 40 times, and most recently two days ago. If she searches for “spring water”, then that product is boosted up, as we know that she likes it. Notice that in the non-personalized results, the Rubicon spring water was the first hit instead.

![A web page shows search results for “spring water”, listing product details, prices, and filter categories for beverages and brands.](https://www.elastic.co/search-labs/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fme0ej585%2Fsearch-labs-import-testing%2F6fce63ff051e345a79fef934cd6e71ba113ae585-1159x1062.png&w=3840&q=75)

A web page shows search results for “spring water”, listing product details, prices, and filter categories for beverages and brands.

## Cohort-aware policy activation

Individual purchase history works well for returning customers with established behavior. But many shoppers are new, anonymous, or browsing outside their usual patterns. For these shoppers, cohort membership provides a different kind of personalization, one based on who the shopper is, not what they've done.

A vegan shopper searching for "chocolate" should see vegan chocolate ranked higher. A halal-observant shopper searching for "snacks" should see halal-certified options prominently. A health-conscious shopper searching for "yogurt" should see probiotic options boosted.

### Cohorts as policies, not product tags

Products already carry their normal attributes, including fields like `dietary_restrictions: ["vegan"]` or `dietary_restrictions: ["halal"]`. The question is where the logic lives that connects a shopper's cohort to those product attributes.

The naive approach would be to hard-code that mapping in the application layer or in the search template: If the user is vegan, add a boost on `dietary_restrictions: "vegan"`. But this is the same application-layer spaghetti described in [Part 1](https://www.elastic.co/search-labs/blog/ecommerce-search-governance-improve-retrieval), and it creates the same operational friction: Adding a new cohort or changing what a cohort means requires a code change.

The governed control plane keeps the cohort logic in the policy engine instead. A cohort policy bridges two things: a shopper's cohort membership (for example, “vegan”) and a product attribute (for example, `dietary_restrictions: “vegan”`). The policy defines the connection: When a shopper in the vegan cohort searches, boost products where `dietary_restrictions` includes “vegan”.

![](https://www.elastic.co/search-labs/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fme0ej585%2Fsearch-labs-import-testing%2F2b6fe359774bbea059aaf93f3fa4a03eb31233ea-544x290.jpg&w=3840&q=75)

Because cohort logic lives in the policy engine rather than application code, this means:

- Adding a new cohort can be done by creating a new policy; no product reindexing required.
- Cohort policies use the full rule engine: They can add filters, apply soft boosts, expand synonyms, change retrieval strategy, or any other action a policy can take.
- Cohort behavior is managed through the same admin UI as all other policies: A merchandiser can create, test, and promote cohort policies through the Author → Test → Promote workflow described in [Part 2](https://www.elastic.co/search-labs/blog/ecommerce-search-governance-zero-deploy).

### Example vegan cohort policy

A merchandiser creates a cohort policy with the following characteristics:

- **Cohorts:** `["vegan"]`.
- **Match criteria:** Matches any query (or a specific product category).

**Action:** Soft boost on `dietary_restrictions: "vegan"` with a boost weight of 2.

![A web interface titled “Edit rewrite policy” shows fields for policy ID, title, description cohort selection, rule query options, rule type, filter settings, and more, with a focus on the cohort containing “vegan” and one on the value "vegan”.](https://www.elastic.co/search-labs/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fme0ej585%2Fsearch-labs-import-testing%2Ffc58bbd97c0dd1fa3ce757394ca117d0789c52f6-1080x1018.png&w=3840&q=75)

A web interface titled “Edit rewrite policy” shows fields for policy ID, title, description cohort selection, rule query options, rule type, filter settings, and more, with a focus on the cohort containing “vegan” and one on the value "vegan”.

### How cohort activation works

Each policy document has a `cohorts` field. Universal policies that apply to all shoppers regardless of cohort can leave this field blank, and these will internally be assigned a value of `"_all"` by the control plane. Cohort-specific policies store their target cohort names, such as `["vegan", "kosher", “sweet_tooth”]`.

When a search request includes a user profile, the control plane constructs a simple `terms` filter for the percolator query:

```json
{ "terms": { "cohorts": ["_all", "vegan", "health_conscious"] } }
```

This single filter includes all universal policies plus the user's cohort-specific policies. The `_all` sentinel makes this a clean inclusion filter: No `must_not` or `exists` queries are needed to handle the case where a policy has no cohort restriction.

The percolator then evaluates policy matches as usual. The only difference is that the candidate policy set has been narrowed to those relevant to this shopper's cohorts. Everything downstream (cascading transformations, per-field conflict resolution, consumed phrase tracking) operates identically to the non-personalized flow described in Parts 3 and 4.

### Non-vegan (standard) user results when searching for “chocolate”

When a non-vegan user searches for chocolate, there’s no vegan cohort boost applied to their results. They would often see non-vegan chocolates in the top hits, as follows:

![A web page shows search results for “chocolate”, with category and brand filters on the left and three chocolate product listings with descriptions, prices, and specifications.](https://www.elastic.co/search-labs/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fme0ej585%2Fsearch-labs-import-testing%2F5bade79944ef294e2cb835cfd6e3231392e8fbd0-1159x1104.png&w=3840&q=75)

A web page shows search results for “chocolate”, with category and brand filters on the left and three chocolate product listings with descriptions, prices, and specifications.

### Vegan cohort policy results when searching for “chocolate”

When a vegan-cohort shopper searches for "chocolate", this policy is included in the percolator candidate set. It matches, and the control plane applies a soft boost to vegan-certified chocolates. The boost is multiplicative: Vegan chocolates rank higher, but non-vegan chocolates are not fully excluded because the above filter is defined as a *soft boost*, which we described in detail in Part 3 of this series.

![A web page shows search results for “chocolate”, with category and brand filters on the left and three chocolate product listings with descriptions, prices, and specifications, with a focus on the circled vegan labels.](https://www.elastic.co/search-labs/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fme0ej585%2Fsearch-labs-import-testing%2Ffc6f7ec6a9de30f3a6d8f32bb9ee7ec457dea458-1138x1255.png&w=3840&q=75)

A web page shows search results for “chocolate”, with category and brand filters on the left and three chocolate product listings with descriptions, prices, and specifications, with a focus on the circled vegan labels.

However, if the shopper explicitly searches for "Hershey milk chocolate", the vegan boost still applies but may be outweighed by the stronger text relevance of Hershey milk chocolate products.

![A web page shows search results for “Hershey milk chocolate”, with category and brand filters on the left and three Hershey’s chocolate product listings, with detailed descriptions, prices, and nutritional information.](https://www.elastic.co/search-labs/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fme0ej585%2Fsearch-labs-import-testing%2Ff47bb8bfa58106f897c4c6c143494f4367355528-1136x1142.png&w=3840&q=75)

A web page shows search results for “Hershey milk chocolate”, with category and brand filters on the left and three Hershey’s chocolate product listings, with detailed descriptions, prices, and nutritional information.

A shopper outside the vegan cohort searching for the same query never sees the “vegan cohort” policy; it’s not in their candidate set. The governance layer is identical; only the active policy set differs.

### Cohorts with purchase history

A vegan shopper with extensive purchase history gets vegan-cohort-specific policy activation as well as purchase history boosts. For new or anonymous shoppers, implied cohort membership alone provides meaningful personalization without requiring any behavioral data (for example, perhaps an anonymous user has only searched for vegan products, and so we classify them as a member of the vegan cohort). A shopper who self-identifies as halal-observant during account creation immediately receives halal-tailored results on their first search.

![A flow diagram shows how a search for “oranges” moves through an application server, a control plane, history and policy lookups, and then a product index to return orange products.](https://www.elastic.co/search-labs/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fme0ej585%2Fsearch-labs-import-testing%2F81af35a533a567d99324860c8e69cf9752533c8f-545x301.jpg&w=3840&q=75)

A flow diagram shows how a search for “oranges” moves through an application server, a control plane, history and policy lookups, and then a product index to return orange products.

## How personalization layers compose

The nesting order of `function_score` layers matters. From innermost to outermost:

1. **Base query:** The keyword or semantic match with named queries (`fulltext_match`, `title_phrase_match`).
2. **Governance policy layer:** Hard filters as `bool.filter` clauses, soft boosts as `function_score` functions (Parts 3 and 4).
3. **Business-signal boosts:** Margin and popularity boosting (which we’ll explore in Part 7).
4. **Purchase history boosts:** The outermost `function_score` layer.

This ordering ensures that governance controls the result set (what appears), business signals adjust ranking within that set (what appears first from the retailer's perspective), and purchase history adjusts ranking further based on individual behavior (what appears first from the shopper's perspective). Each layer wraps the previous one multiplicatively, so the effects compound rather than conflict.

## What this means operationally

Personalization through the governed control plane preserves every operational property described in Parts 1 and 2:

- **Zero-deploy changes.** Cohort policies are created, tested, and promoted through the admin UI. Adding a new dietary cohort or adjusting a boost weight requires no code changes and no engineering involvement.
- **Auditability.** Every cohort policy is a discrete, versioned document. When a merchandiser asks, "Why are vegan products ranking higher for this user?", the answer is a specific policy with a specific priority, visible in the debug panel alongside every other policy that fired for that query.
- **Conflict resolution.** Cohort policies participate in the same per-field conflict resolution described in Part 3. If a cohort policy's category boost conflicts with a campaign policy's category override, the conflict is resolved deterministically by the same priority and strategy framework, no special handling needed.
- **Measurability.** Because cohort policies are discrete and individually toggleable, their impact on conversion, click-through, and add-to-cart rates can be measured independently, just like any other policy in the system.

## What's next in this series

The next post explores another dimension of the governed control plane: how margin and popularity boosting can be tuned per query through policies, turning economic optimization into a governance decision rather than a static configuration.

See Part 7: Query-governed economic optimization: Per-query margin and popularity boosting

## Put governed ecommerce search into practice

The personalization patterns described in this post (individual purchase history boosting and cohort-aware policy activation) were designed and built by Elastic Services Engineering as part of our repeatable [ecommerce](https://www.elastic.co/enterprise-search/ecommerce "Fast & scalable e-commerce search") search accelerator. Both mechanisms integrate with the governed control plane architecture described throughout this series. Contact [Elastic Professional Services](https://www.elastic.co/consulting).

## Join the discussion

Have questions about search governance, retrieval strategies, or ecommerce search architecture? Join the broader [Elastic community conversation](https://discuss.elastic.co/).