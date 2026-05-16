---
title: "Personalizing e-commerce search results based on purchase history in Elasticsearch"
source: "https://alexmarquardt.com/elastic/personalizing-search-in-elasticsearch-without-ml-post-processing/"
author:
  - "[[Alexander Marquardt]]"
published: 2025-09-12
created: 2026-05-15
description: "IntroductionWhether you're looking for a product in an online store, an article in a news archive, or a file in a company knowledge base, the quality of the search experience determines how quickly you find what you need. Behind the scenes, many of these systems are powered by Elasticsearch, a popular open-source search engine designed to handle large volumes of data and return relevant results in milliseconds.At its core, Elasticsearch matches user queries against text fields and ranks results using relevance scoring. But search doesn't have to stop there. That's where personalization comes in. By incorporating signals such as past purchases, browsing behavior, or recent activity, search results can be adjusted so the items most relevant to you appear higher. For example, if two people both search for "chips", one might see classic potato chips at the top, while the other sees crispy thin-cut chips, depending on their history."
tags:
  - "clippings"
---
## Introduction

Whether you're looking for a product in an online store, an article in a news archive, or a file in a company knowledge base, the quality of the search experience determines how quickly you find what you need. Behind the scenes, many of these systems are powered by **Elasticsearch**, a popular open-source search engine designed to handle large volumes of data and return relevant results in milliseconds.

At its core, Elasticsearch matches user queries against text fields and ranks results using relevance scoring. But search doesn't have to stop there. That's where **personalization** comes in. By incorporating signals such as past purchases, browsing behavior, or recent activity, search results can be adjusted so the items most relevant to *you* appear higher. For example, if two people both search for *"chips"*, one might see *classic potato chips* at the top, while the other sees *crispy thin-cut chips*, depending on their history.

Search personalization is often treated as a "phase two" re-ranking project that happens *after* search results have been retrieved, typically by adding a separate ML re-ranker. That can work, but in many stacks it introduces extra infrastructure and can slow iteration compared with a pure-query approach.

On the other hand, if you're already using Elasticsearch, you already have the building blocks for implementing personalization. With Elasticsearch you can:

- Store your product catalog (all the items you want users to search).
- Store user activity (like purchases or clicks). \*
- Run queries that combine those two data sources.

In this post, I'll show you how to build **personalization directly leveraging Elasticsearch** capabilities, without post processing ML jobs. I'll show how to leverage a user's past purchases, turn it into boosts, and apply those boosts to a search query against product inventory — so the products that a user is most likely to want to purchase (based on their history) naturally rise to the top. The full working code is available here: [alexander-marquardt/elasticsearch-personalization](https://github.com/alexander-marquardt/elasticsearch-personalization).

\* Note: In this article we assume you pre-process or pre-aggregate the purchase history to get it into an efficient format for for fast lookup, similar to the user's purchase history index presented in this article.

## Why this approach is useful

- **No extra infrastructure**: All the logic lives in Elasticsearch queries. No ML jobs.
- **Transparent**: Boosts are calculated with a simple formula (log1p(purchases) × recency decay), easy to explain and tweak.
- **Composable**: The boosts combine naturally with standard BM25 ranking.

This design pushes personalization into the query itself.

## How it works (high-level overview)

At query time we execute **two phases**:

1. **History phase** — Look up this user's purchase history to return items relevant to their query. **Compute a boost** for each relevant product that they have purchased in the past.
2. **Search phase** — Build a query that includes a function\_score query that incorporates the personalised product boosts that we just calculated, so that **items previously purchased by this user are pushed to the top** of the results. Run the user's query against the product catalog.

## The formula

We have an index that contains the purchase history for each user. Each product that a client has purchased has the following fields defined:

- **purchase\_count(p)** = number of times the user purchased product *p*
- **age\_days(p)** = days since the last purchase of *p*

A formula that can be used to convert these values into a personalised boost is:

![](https://alexmarquardt.com/elastic/personalizing-search-in-elasticsearch-without-ml-post-processing/images/image-1.png)

### Constants

We choose the following constant values, which work for our example but should be re-evaluated depending on your desired outcome:

- **BASE\_BOOST** = 1.0
- **SCALE** = 3.5
- **HALF\_LIFE\_DAYS** = 60

In the above formula, BASE\_BOOST = 1 guarantees we never reduce the raw BM25 score—worst case we leave it unchanged.

A SCALE of 3.5 (which is added to the BASE\_BOOST of 1) ensures that the boost (multiplier) remains between 1 and 4.5. If this is too much or too little, you can modify the SCALE to decrease or increase the resulting boost values.

Likewise, the impact of recent vs. old purchases can be controlled by the HALF\_LIFE\_DAYS value.

### Explanation of the formula

#### 1\. Log frequency term

ln(1 + purchase\_count) dampens the effect of repeat purchases. For example:

- 1 → ln(2) ≈ 0.69
- 10 → ln(11) ≈ 2.40
- 100 → ln(101) ≈ 4.62

This ensures *diminishing returns*: frequent purchases matter more, but not linearly.

#### 2\. Recency term

exp( -ln(2) × age\_days / HALF\_LIFE\_DAYS )

applies exponential decay, halving the weight every 60 days.

- 0 days → factor = 1.0
- 60 days → factor = 0.5
- 120 days → factor = 0.25

#### 3\. Normalization (max\_raw)

Dividing by max\_raw ensures that the strongest historical signal normalizes to **1.0**, and other items scale proportionally.

Without this normalization, users with very different purchase patterns would get **very different boost ranges**:

- A heavy buyer (hundreds of purchases) could generate raw weights much larger than a light buyer (a few purchases).
- That would make boosts inconsistent across users, and in extreme cases a single heavy purchase could dominate all results.

By dividing by **max\_raw** (the maximum raw weight observed in this user's history for the current query), we ensure:

- The strongest historical signal always normalizes to **1.0**.
- All other signals scale proportionally between 0.0 and 1.0.
- Every user's boosts are mapped into the same range, regardless of shopping habits.

## Example implementation

The code available at [alexander-marquardt/elasticsearch-personalization](https://github.com/alexander-marquardt/elasticsearch-personalization), makes use of the following two indices:

- **demo\_products** — the product catalog (product\_id, description) - example at: [example\_products.ndjs](https://github.com/alexander-marquardt/elasticsearch-personalization/blob/main/data/example_products.ndjs)
- **user\_purchases** — purchase history (user\_id, product\_id, purchase\_count, last\_purchase\_ts) - example at: [user\_purchases\_bulk.ndjs](https://github.com/alexander-marquardt/elasticsearch-personalization/blob/main/data/user_purchases_bulk.ndjs)

## Sample output

Here's what the script produces when different users search for **"chips"**.

Each run has two parts:

- **PHASE 1** - the image below shows an example purchase history (which prior purchases match this intent) for user\_101, along with the computed boosts.

![](https://alexmarquardt.com/elastic/personalizing-search-in-elasticsearch-without-ml-post-processing/images/image-6.png)

- **PHASE 2** execute a query to get the final personalized ranking of products in which the ranking for each product has had the user-specific boost from Phase 1 applied.

The actual query that is executed looks as follows:

![](https://alexmarquardt.com/elastic/personalizing-search-in-elasticsearch-without-ml-post-processing/images/image-10.png)

And the output that results from this query would be:

![](https://alexmarquardt.com/elastic/personalizing-search-in-elasticsearch-without-ml-post-processing/images/image-7.png)

- **Compare to user\_202**:

Notice how the above ordering of products has been impacted by the purchase history of user\_101, while the following results are ordered differently, based on the purchase history of user\_202:

![](https://alexmarquardt.com/elastic/personalizing-search-in-elasticsearch-without-ml-post-processing/images/image-8.png)

![](https://alexmarquardt.com/elastic/personalizing-search-in-elasticsearch-without-ml-post-processing/images/image-9.png)

## How to try it yourself

Clone the repo, make sure you have Elasticsearch running locally and without authentication. Load some sample user purchase histories, and some sample products, by using the BULK POSTs that are given in:

- [example\_products.ndjs](https://github.com/alexander-marquardt/elasticsearch-personalization/blob/main/data/example_products.ndjs)
- [user\_purchases\_bulk.ndjs](https://github.com/alexander-marquardt/elasticsearch-personalization/blob/main/data/user_purchases_bulk.ndjs)

Then you can run the script:

```
git clone https://github.com/alexander-marquardt/elasticsearch-personalization.git
cd elasticsearch-personalization
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Load the sample data into your Elasticsearch cluster
# (see data/ folder or use _bulk requests)

python personalized-search.py
```

This will print personalized results like those shown above.

## Conclusion

Personalization doesn't need complex ML jobs. With just two indices and a bit of query logic, you can personalize search results.

- Phase 1 builds a per-user boost profile from history.
- Phase 2 applies those boosts in the search query.

Full code and data: [alexander-marquardt/elasticsearch-personalization](https://github.com/alexander-marquardt/elasticsearch-personalization?utm_source=chatgpt.com)

## Acknowledgement

Thanks to Honza Kral for the idea and inspiration for this approach.