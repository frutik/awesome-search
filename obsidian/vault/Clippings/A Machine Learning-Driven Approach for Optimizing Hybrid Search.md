---
title: "A Machine Learning-Driven Approach for Optimizing Hybrid Search"
source: "https://aipoweredsearch.com/articles/machine-learning-for-optimizing-hybrid-search/"
author:
  - "[[Trey]]"
published: 2025-07-10
created: 2026-06-18
description: "How to greatly improve your hybrid search results using machine learning to dynamically optimize hybrid search parameters for each query."
tags:
  - "clippings"
---
How to greatly improve your hybrid search results using machine learning to dynamically optimize hybrid search parameters for each query.

![Optimizing Hybrid Search](https://aipoweredsearch.com/wp-content/uploads/2025/07/AD_4nXejApaxKCc9uXOsF8PXtZ3HUegwr-ihRljBrzpRRLECt40g-HYa-UWnGgJGQNcCdfrQDBNfzoODXM31EYspY2pKx2WrRjbY5I1iCGa8PaH2VIdezNvmyrGaAXrrYeWceyG3qJbHAA.png)

Optimizing Hybrid Search

Hybrid search is the combination of lexical and vector search results. Search practitioners need to understand how to choose the different normalization and combination techniques together with the weighting parameters for their search application. We’ll discuss how to optimize hybrid search using a machine learning-driven approach to dynamically predict these parameters for each query.

Optimizing hybrid search involves a journey—from identifying the best global parameter combinations to leveraging machine learning techniques. This post summarizes key findings from our efforts, which are explored in greater detail in the OpenSearch blog post [*Optimizing Hybrid Search in OpenSearch*](https://opensearch.org/blog/hybrid-search-optimization/).

## Identifying the best global parameters for optimizing hybrid search

Hybrid Search optimization often boils down to parameter tuning. By evaluating various parameter combinations against a query set and a collection of judgments, you can calculate [search quality metrics](https://opensourceconnections.com/blog/2020/02/28/choosing-your-search-relevance-metric/) to identify the best-performing configuration quantitatively.

For simple parameter spaces, you can feasibly test all combinations. In more complex scenarios, you might focus on subsets or use optimization algorithms like Bayesian optimization. Chapter 12 of [*AI-Powered Search*](https://aipoweredsearch.com/) provides an excellent example of applying Bayesian optimization in the search domain to address presentation bias.

## Parameters for hybrid search in OpenSearch

In our OpenSearch-based exploration, we defined the following parameters and their possible values:

- *Normalization technique*: \[l2, min\_max\]
- *Combination technique*: \[arithmetic\_mean, harmonic\_mean, geometric\_mean\]
- *Lexical search weight*: \[0.0, 0.1, …, 1.0\]
- *Neural search weight*: \[1.0, 0.9, …, 0.0\]

By iterating over all combinations and evaluating metrics like DCG@10, NDCG@10, and Precision@10, we identified the best global configuration:

- *Normalization*: l2
- *Combination*: arithmetic\_mean
- *Lexical weight*: 0.4
- *Neural weight*: 0.6

## Results: Global Hybrid Search Optimization

The globally-optimized hybrid search configuration resulted in significant metric improvements:

|  | **Relative Change** | **Baseline** | **Global Parameter Optimization** |
| --- | --- | --- | --- |
| **DCG@10** | +5.4% | 8.82 | 9.30 |
| **NDCG@10** | +8.7% | 0.23 | 0.25 |
| **Precision@10** | +12.5% | 0.24 | 0.27 |

However, not all queries benefited equally, highlighting the limitations of a static global configuration. The query cbd, for example, dropped to a DCG@10 value of 0 from the baseline value of 13.8 for the baseline. The query power steering low pressure return line counts to the positive examples, showing an increase from a DCG@10 value of 7.0 to 25.3.

This led us to explore a dynamic, machine-learning-driven approach to parameter prediction.

## A machine learning-driven approach to dynamic optimization

To further enhance search result quality, we developed a model that predicts the best parameters dynamically for each query. By engineering features that capture various aspects of the query and its results, our dynamically-optimized hybrid search model outperformed the global configuration:

|  | **Relative Change** | **Global Parameter Optimization** | **Model-based Approach** |
| --- | --- | --- | --- |
| **DCG@10** | +8.9% | 9.30 | 10.13 |
| **NDCG@10** | +8.0% | 0.25 | 0.27 |
| **Precision@10** | +7.4% | 0.27 | 0.29 |

## Key features for dynamic hybrid search optimization

We categorized the features into three groups:

- *Query features*: Attributes of the user query string; number of terms, query length in characters, Inclusion of numbers and special characters.
- *Lexical search result features*: Attributes of the results that the user query retrieves when executed as a lexical search; number of results, maximum title score, sum of title scores.
- *Neural search result features*: Attributes of the results that the user query retrieves when executed as a neural search; maximum semantic score, average semantic score.

## Comparative performance

The following diagrams show the metrics from baseline (light blue), the global hybrid search optimization process (dark blue) and the dynamic hybrid search optimization process (orange).

![DCG@10 for each hybrid search optimization technique](https://aipoweredsearch.com/wp-content/uploads/2025/07/AD_4nXcRQUlTqT0vtNlugt8a76XN42c80xfBcGOUKTOX-xzacXs9JWg62p25MQ0KNkmghZQ79_YTFv67lQRlwIUptcgbmAi22gEKqPg3t7k76HxvIAVlDjStZrrh_yqcWmW4OltOEVr8MQ.png)

DCG@10 for each hybrid search optimization technique

![NDCG@10 for each hybrid search optimization technique](https://aipoweredsearch.com/wp-content/uploads/2025/07/AD_4nXejApaxKCc9uXOsF8PXtZ3HUegwr-ihRljBrzpRRLECt40g-HYa-UWnGgJGQNcCdfrQDBNfzoODXM31EYspY2pKx2WrRjbY5I1iCGa8PaH2VIdezNvmyrGaAXrrYeWceyG3qJbHAA.png)

NDCG@10 for each hybrid search optimization technique

![Precision@10 for each hybrid search optimization technique](https://aipoweredsearch.com/wp-content/uploads/2025/07/AD_4nXdMpcmttVJTBQn5JG3q_msaQa_fil0LeKcSAXdnqU0fHkF6bfzb5N9jy0lmJUyOZG5CeqYuXiS9pkKxaPTvoD2cb0paxeaRU-zWsWFxQiJ4WJZrmco4fcj9NFzeQ7OYLoa592pXRQ.png)

Precision@10 for each hybrid search optimization technique

For more information, check out the [linked blog post](https://opensearch.org/blog/hybrid-search-optimization/) that we published on the OpenSearch blog and the following video walkthrough taking you through the notebooks. The [repository](https://github.com/o19s/opensearch-hybrid-search-optimization/) was updated with minor changes in notebooks 7 and 8 for model training and evaluation after the recording, so make sure to follow along with the latest code.

![](https://www.youtube.com/watch?v=eU7Ihc61ang)

## Conclusion

By treating hybrid search optimization as a parameter optimization problem, you can achieve measurable performance improvements over your baseline through systematic experimentation. Taking this a step further with machine learning enables dynamic, query-specific optimization that surpasses global configurations.

Although this implementation was developed for OpenSearch, the methodology is transferable to other search engines supporting hybrid search.

## Additional resources

- [Optimizing hybrid search in OpenSearch](https://opensearch.org/blog/hybrid-search-optimization/)
- [Github repository with code](https://github.com/o19s/opensearch-hybrid-search-optimization/)
- [YouTube notebook walkthrough covering global and dynamic hybrid search optimization](https://youtu.be/eU7Ihc61ang)

Contact us today to understand your users’ queries better and elevate your search result quality!