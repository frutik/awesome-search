---
title: "Why ecommerce search needs governance & how it improves retrieval"
source: "https://www.elastic.co/search-labs/blog/ecommerce-search-governance-improve-retrieval"
author:
  - "[[Alexander Marquardt]]"
  - "[[Honza Král]]"
  - "[[Taylor Roy]]"
published: 2026-04-08
created: 2026-05-16
description: "Learn why ecommerce search falls short without governance and how a control layer ensures predictable and intent-driven results, thus improving retrieval."
tags:
  - "clippings"
---
New to Elasticsearch? Join our [getting started with Elasticsearch](https://www.elastic.co/virtual-events/getting-started-elasticsearch) webinar. You can also start a [free cloud trial](https://cloud.elastic.co/registration) or try Elastic on your [machine](https://github.com/elastic/start-local) now.

[Ecommerce](https://www.elastic.co/enterprise-search/ecommerce "Fast & scalable e-commerce search") retailers need to handle various fundamentally different query types within the same system. A shopper searching for “oranges” expects the fruit, not products containing the word “orange”, such as orange juice or orange marmalade, and not semantically related citrus products. A shopper searching for a “gift for grandpa who has a sweet tooth” needs semantic discovery, not literal keyword matching.

*Lexical retrieval* (text matching), *semantic retrieval* (matching concepts), and *hybrid retrieval* (combining lexical and semantic signals) don’t solve these issues on their own. Lexical retrieval may return anything containing the word “oranges”, while pure semantic retrieval on a high-intent query like “oranges” may broaden toward related items, such as lemons or grapefruits. Hybrid retrieval blends these lexical and semantic signals, but it still doesn’t determine if this query should be treated as navigational, which constraints should be enforced, or which business policies should apply. The gap isn’t the retrieval technology itself; it’s the absence of a governance layer that understands what kind of query this is and what constraints should be enforced before retrieval begins.

In this blog, we explore ecommerce search governance, why it matters, and how a control layer ensures predictable, accurate retrieval.

## What governance means in ecommerce search

*Governance*, in this context, means introducing a decision layer between the user's query and the retrieval engine. This layer performs the following functions:

- Classifies query intent: Is this navigation ("oranges") or discovery ("gift for grandpa")?
- Applies business constraints: What category boundaries, eligibility rules, availability constraints, or merchandising policies apply?
- Routes to the appropriate strategy: Should this use lexical retrieval, semantic retrieval, or hybrid?

A governance layer determines which retrieval approach should be used for each query, which constraints must be enforced, and which business policies should apply before retrieval begins. It’s important not to conflate governance with hybrid retrieval: hybrid is one retrieval strategy that combines lexical and semantic signals, while governance is the upstream decision layer that determines whether lexical, semantic, or hybrid should be used.

## The status quo: The application layer "spaghetti" implementation

Currently, many retailers attempt to solve this by adding logic directly into the application layer. This often results in *spaghetti code*, that is, thousands of lines of hard-coded if-then statements, regex, and complex search templates.

![Comparison of hard‑coded application logic and Elasticsearch, showing how Elasticsearch simplifies ranking and retrieval without complex if‑then rules.](https://www.elastic.co/search-labs/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fme0ej585%2Fsearch-labs-import-testing%2Ff532b099ee103458e15563a711dae92952f8df02-1024x765.png&w=3840&q=75)

Comparison of hard‑coded application logic and Elasticsearch, showing how Elasticsearch simplifies ranking and retrieval without complex if‑then rules.

This approach can provide desired search results as shown above; however, it creates significant operational friction:

- **Engineering dependency:** Business users and merchandisers cannot modify search behavior without engineering tickets and long deployment cycles that often span several weeks.
- **Fragmentation:** Search logic becomes scattered between application code and search templates, and is difficult to explain or audit, making it risky to evolve.

Even when teams recognize the need for routing, the debate often focuses on the wrong question: which retrieval method to pick.

## The false choice: Lexical vs. semantic vs. hybrid

Search teams often frame the challenge as a retrieval strategy choice: lexical/ [BM25](https://www.elastic.co/search-labs/blog/lexical-and-semantic-search-with-elasticsearch) versus semantic/vectors versus hybrid. That framing is understandable (retrieval methods matter), but it misses the most common failure mode in real deployments, which is that using a single retrieval approach for all queries will give suboptimal results.

Commerce search is a mix of fundamentally different intents:

- **Deterministic, high-intent navigation** ( "oranges", “milk”, “chocolate without peanuts”, “cheap olive oil”).
- **Exploratory discovery** ("jacket for hiking in the mountains", "gift for a 12-year-old who likes robotics").
- **Operational constraints** (availability, size, price, color).
- **Merchandising and campaigns** (boost, bury, seasonal campaigns).

When the system routes all of these through the same retrieval strategy, the results are often systematically wrong in predictable ways because the operating model lacks governance. When teams don't recognize this as a governance gap, they respond with the only lever they have: more tuning.

## Why "relevance tuning" can become cyclical

Without a routing layer, “relevance” often turns into a never-ending backlog:

- Why is this query showing accessories above the core product?
- Why did this head query suddenly start surfacing related items?
- Why did results change after we added synonyms, adjusted analyzers, or enabled hybrid?
- Why does the business team need an engineering release to fix a single query?

Teams respond with more tuning: more synonyms, more boosts, more [reranking](https://www.elastic.co/search-labs/blog/elastic-semantic-reranker-part-1) experiments, more exceptions in application code. This can work for a while, but it often produces brittle behavior because the system still lacks an explicit decision layer for determining query type and enforcing the right constraints before retrieval.

## The anatomy of ecommerce intent: Head and tail

In this section, we use “head” and “tail” as practical shorthand for common navigational and exploratory query patterns in ecommerce. In the real world, many queries contain aspects of both:

### Head queries (deterministic intent)

These are direct, navigational queries where the user knows exactly what they want:

- Single-item intent ("oranges", "milk", "bread").
- Exact brands or product families ("iPhone 15 Pro", "Diet Coke").
- SKUs, model numbers, sizes ("ABC123", "air max 270").

For these queries, lexical retrieval can handle token correspondence (matching words), but the business also expects to respect constraints, return predictable rankings, and have controllable outcomes. A merchandiser needs to ensure that a query resolves within the correct category boundaries, respects eligibility, and surfaces specific business priorities.

Governance is required to enforce the intended resolution. For example, “oranges” should map to the produce category, not to orange juice, orange marmalade, or orange soda.

### Tail queries (exploratory discovery)

These are descriptive, intent-rich queries where shoppers are exploring:

- "Gift for grandpa who has a sweet tooth"
- "Jacket for hiking in the mountains"
- "Shoes for standing all day"

Lexical retrieval often struggles here. Semantic retrieval excels because it can connect the query concept to the product, even when wording does not match. But semantic retrieval alone is rarely sufficient either. Real queries often require constraints to be enforced, regardless of which retrieval method is used.

## Constraints are orthogonal to retrieval method

Applying constraints to semantic retrieval doesn’t mean [*hybrid search*](https://www.elastic.co/search-labs/blog/hybrid-search-elasticsearch "Learn more about hybrid search"). These are orthogonal concepts. Constraints, such as filters and boosts in [Elasticsearch](https://elastic.co/elasticsearch), can be applied to any lexical, semantic, or hybrid retrieval. The challenge is deciding how the query should be interpreted, which constraints must be enforced, and which retrieval strategy should be used.

Below are some examples of queries that combine retrieval with hard constraints:

- **Oranges:** Lexical retrieval for “oranges” plus a category constraint, such as “Fruits” or “Produce”, eliminating orange marmalade, orange juice, and orange soda.
- **Fruits high in vitamin C under $4:** Semantic retrieval for nutritional intent plus constraints limiting results to the fruit category and products under $4.
- **Comfortable shoes for work:** Semantic retrieval for contextual intent plus a category constraint limiting results to shoes.

These queries can't be handled by a single approach:

- **Pure lexical retrieval** is often insufficient here because phrases like “high in vitamin C” or “comfortable” may not exist as clean, structured attributes. They may need to be inferred from product descriptions, reviews, or specifications.
- **Pure semantic retrieval** is also not always sufficient because, without explicit constraints, a query like “fruits high in vitamin C” might broaden toward vitamin supplements, fruit-flavored drinks, or high-vitamin vegetables outside the intended category and price range.

A governance layer determines whether a query needs lexical retrieval, semantic understanding, constraint enforcement, or some combination of these. Without this layer, ecommerce teams may end up:

- **Over-constraining:** Using lexical retrieval for semantic requests (for example, "gift for grandpa").
- **Under-constraining:** Using semantic queries for high-intent head queries (for example, “oranges”).

The governance challenge is to build a system that can make the right judgment call for each class of query.

## What happens without governance

The most common failure mode is straightforward: Teams take the raw user query and pass it directly into a single retrieval strategy (lexical, semantic, or hybrid), without an intermediate governance layer.

### Lexical retrieval misses intended resolution

When a user searches for “oranges”, a lexical retrieval strategy may return anything containing that token: orange juice, orange marmalade, or orange soda. The system matched the term correctly, but without governance it may not resolve the intended shopping context (the fruit).

![ Illustration showing how a single query for “oranges” returns different related results, such as marmalade, fresh oranges, and orange soda.](https://www.elastic.co/search-labs/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fme0ej585%2Fsearch-labs-import-testing%2F99abc7a46f9c56a26a68d0a089d7ab830b9b5568-1560x814.png&w=3840&q=75)

Illustration showing how a single query for “oranges” returns different related results, such as marmalade, fresh oranges, and orange soda.

### Semantic retrieval broadens beyond intended constraints

When a user searches for “oranges”, a semantic system may retrieve conceptually related items across nearby product concepts. The system may correctly understand the broader domain (fruit or produce), but without explicit governance it can still over-broaden beyond the user’s intended constraint (specifically oranges).

![Diagram showing how a query for “oranges” routes to different fruit categories, including apples, oranges, and mixed fruit.](https://www.elastic.co/search-labs/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fme0ej585%2Fsearch-labs-import-testing%2Fc9de86363ecbed499fe48259f47b3c5b2c26bc43-1568x796.png&w=3840&q=75)

Diagram showing how a query for “oranges” routes to different fruit categories, including apples, oranges, and mixed fruit.

### The gap is governance

What’s required is an upstream decision layer that determines query intent and enforces the right constraints before retrieval begins. This fixes issues such as the following:

- Similar or related items appearing alongside what the user actually wanted.
- Blurred category boundaries ("beverages" versus. "produce").
- Inability to implement seasonal boosts or campaigns.
- Unpredictable and unexplainable results.

## Intent understanding and routing: The necessary control plane

A governed search system introduces a lightweight control plane in front of retrieval (prior to executing a query in Elasticsearch). The control will be discussed in detail in parts [3](https://www.elastic.co/search-labs/blog/ecommerce-search-governance-control-plane-architecture) and [4](https://www.elastic.co/search-labs/blog/elasticsearch-percolator-search-governance) of this blog series; for now, we just discuss what it can do but not how it works:

![Diagram showing how different queries route through a control plane to BM25 or semantic search results.](https://www.elastic.co/search-labs/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fme0ej585%2Fsearch-labs-import-testing%2F88c3d0f9731a128d73a765dcdffed897308110a6-2680x766.png&w=3840&q=75)

Diagram showing how different queries route through a control plane to BM25 or semantic search results.

A control plane can detect intent, apply business policies, and ensure the appropriate retrieval strategy as follows:

**1\. Detect intent signals**

- Is this query likely navigation versus discovery?
- Is it a known head query (milk, bread, bananas)?
- Is there a known product, brand, or category interpretation (for example, “oranges” should resolve to produce).
- Is the query an SKU-like pattern?
- Does the query fall under an active campaign or seasonal policy (for example, during Christmas, boost turkey-related results)?
- Does the query imply constraints (category, attributes, exclusions, price/size/color)?

**2\. Apply governance and business policies**

- Enforce deterministic constraints first (category/attribute/negation/availability).
- Apply active merchandising policies (boost/bury/pin/override).
- Resolve conflicts with precedence rules (for example, campaign overrides versus global policies).

**3\. Route to the appropriate retrieval strategy**

- Lexical (fast, deterministic) for navigational/high-intent head queries.
- Semantic retrieval for true discovery queries.
- Hybrid where combined lexical and semantic signals add value under explicit business constraints.

In practice, the output of the control plane is not simply “use hybrid” or “use semantic.” It’s a governed retrieval plan: an interpretation of the shopper’s intent, the constraints and policies that should apply, and the retrieval strategy that should be executed. A few simple examples make this concrete:

| Shopper query | Governed interpretation | Example retrieval plan |
| --- | --- | --- |
| “chocolate without peanuts” | Product-oriented query with a hard exclusion constraint | Lexical retrieval for chocolate plus an exclusion filter for products containing peanuts |
| “cheap olive oil” | Product/category query with a price constraint | Lexical retrieval for olive oil plus a price filter capped at the retailer’s threshold for cheap |
| “fruit high in vitamin C under $4” | Discovery query requiring semantic understanding plus hard constraints | Semantic retrieval for nutritional intent, constrained to the fruit category and filtered to products priced under $4 |

A control plane selects the right policy and retrieval strategy for each query consistently, predictably, and at scale. This makes advanced retrieval methods more predictable in production because intent-aligned constraints are enforced first and routing decisions are explicit rather than implicit.

## How this relates to other approaches

Some teams use improved [embedding models](https://www.elastic.co/what-is/vector-embedding) to better capture product semantics, which can materially improve semantic retrieval quality. Others use reranking approaches, such as [Learning To Rank (LTR)](https://www.elastic.co/docs/solutions/search/ranking/learning-to-rank-ltr), to optimize result ordering based on engagement or business signals after retrieval. Both are valuable and often complementary. Better embeddings improve similarity matching. Reranking improves ordering among retrieved candidates.

Governance addresses a different layer of the problem: It sits upstream of retrieval. It decides which retrieval strategy to use (for example, lexical, semantic, or hybrid), what deterministic constraints are required, and which queries should combine multiple business policies.

## What a governed control plane enables

Once a governance layer is in place, the operating model changes fundamentally. Revenue-critical queries become predictable. Business teams can update search behavior without waiting on engineering release cycles. And advanced retrieval methods, like semantic and hybrid, can be adopted incrementally, behind routing and guardrails, instead of as a global on/off switch.

The [next post](https://www.elastic.co/search-labs/blog/ecommerce-search-governance-zero-deploy) in this series explores what that operating model looks like in practice and why it may matter as much as the retrieval technology underneath it.

If a merchandiser has to open a Jira ticket and wait for a deploy to fix a revenue-critical query, the bottleneck isn't the engine; it's the operating model. Modern ecommerce search needs a way to translate business intent into controlled, auditable search behavior quickly and safely, while still using advanced retrieval where it adds measurable value.

## What’s next in this series

The patterns explored in this series operate upstream of retrieval: translating business intent into the right query strategy before query generation begins. In the [next post](https://www.elastic.co/search-labs/blog/ecommerce-search-governance-zero-deploy), we shift from the technical problem to the operational one: what happens when business teams can change search behavior without an engineering deployment, and why governance makes that safe.

## Put governed ecommerce search into practice

Engineering bottlenecks, brittle application-layer logic, and unpredictable search results are problems that Elastic Services can help you solve in enterprise ecommerce services engagements. The governed control plane architecture described in this series was built by Elastic Services Engineering.

If your team is spending engineering cycles translating merchandising requests into code changes, or if your [search relevance](https://www.elastic.co/search-labs/blog/search-relevance-tuning-in-semantic-search "Learn more about search relevance tuning in semantic search") backlog never seems to shrink, we can help you assess your current architecture and build a path to governed, business-editable search. Contact [Elastic Services](https://www.elastic.co/consulting).

## Join the discussion

Have questions about search governance, retrieval strategies, or ecommerce search architecture? Join the broader [Elastic community conversation](https://discuss.elastic.co/).