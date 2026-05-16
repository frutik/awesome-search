---
title: "Part 1: Learning to Rank for E-Commerce Search"
source: "https://www.otto.de/jobs/en/blogs/techblog/1-learning-to-rank-for-e-commerce-search/"
author:
  - "[[Andrea Schütt]]"
published: 2021-04-21
created: 2026-05-16
description: "Enabling users to find the products they are looking for is the core job of the search team of otto.de. But not only finding the relevant articles, but also putting the most relevant products at the top of the list is one of the main challenges we are facing in our job.  In this and the following posts we will show you how we implemented Learning to Rank to improve our ranking, how we meet the ecommerce specific challenges, measure search quality and how we realized the technical implementation."
tags:
  - "clippings"
---
## What is the article about?

Enabling users to find the products they are looking for is the core job of the search team of otto.de. But not only finding the relevant articles, but also putting the most relevant products at the top of the list is one of the main challenges we are facing in our job. In this and the following posts we will show you how we implemented Learning to Rank to improve our ranking, how we meet the ecommerce specific challenges, measure search quality and how we realized the technical implementation.

## Why do we want to apply machine learning in ranking?

Since OTTO is transforming into a marketplace, the number and diversity of products on sale is increasing every day. Larger numbers result in greater complexity, particularly for the search system. This increase in complexity and the sheer volume of data at otto.de (see fig. 1) cannot be handled by traditional approaches. Instead, we are leveraging machine learning (ML) models for a data-driven approach that provides the greatest value for our customers. For our ranking, we are implementing a **Learning-to-Rank model (LTR)**. LTR helps us increase recall (given the rise in product numbers we will return an ever larger number of products per query with varying relevance to the customer) without the risk of losing precision on visible ranks.

![](https://www.otto.de/jobs/de26-wAssets/img/blogs/techblog/2021/04/weblication/wThumbnails/02.-learning-to-rank-for-e-commerce-search-7d88d9bf-924f645a@1461w.png)

## What kind of ranking model is used?

Ranking models learn abstractions of relevance dependencies for products given a certain query. Known LTR models utilize pointwise, pairwise and listwise approaches to optimize ranking (for further details see: [https://medium.com/swlh/pointwise-pairwise-and-listwise-learning-to-rank-baf0ad76203e](https://medium.com/swlh/pointwise-pairwise-and-listwise-learning-to-rank-baf0ad76203e)). We are using LambdaMART which can be considered to combine a pairwise and a listwise approach. LambdaMART calculates gradients based on a pairwise comparison of elements in the list followed by a weighting based on NDCG (a common ranking metric), combining the advantages of both approaches. As we mentioned earlier, these models have huge potential in ecommerce. There are also various sector-specific challenges to consider though, some of which we will address in the next section.

## How is the target metric defined?

A challenge we are facing due to our ecommerce setting is that we cannot generate relevance labels via crowd sourcing or similar approaches. Estimating the relevance of a product in a crowd sourcing setup differs a lot from having the intention to buy something and estimating its relevance from that perspective. We therefore need to model evaluations automatically based on customer data. How this is done exactly depends on the KPI we want to do some optimizing for.

We started out intending to optimize our model by maximizing clicks only. However, we soon discovered that other KPIs are equally if not more relevant. The availability of products, for instance, plays a big part in a customer’s buying decision just as other significant factors do. Leveraging this knowledge, many different definitions of the target metric are conceivable

- *Add to basket* or *add to wishlist* events could serve as target metric. In fact, the ultimate relevance signal is the customer ordering the product, so this could equally be defined as an optimization goal for the model. Additionally, different combinations of these KPIs should be considered relevant to identifying a good target metric.
- Thinking a bit out of the box we could also utilize other customer interaction signals such as time spent on a product details page, number of clicks invested in going through search result pages, a.s.o.

![](https://www.otto.de/jobs/de26-wAssets/img/blogs/techblog/2021/04/weblication/wThumbnails/03.-learning-to-rank-for-e-commerce-search-39d56892-924f645a@1133w.png)

## Which steps are required to get a trained model?

The model integration pipeline is shown in figure 3. We use a sampled query set to build the training data. For the queries in this set we calculate judgements (our ranking gold standard) and features per query-product pair. The features are generated in the Solr feature store. Combining judgements and features we assemble the train data used to set up our ranking model. The LambdaMART model training is done with a fork of RankLib called RankyMcRankface (see [https://github.com/o19s/RankyMcRankFace](https://github.com/o19s/RankyMcRankFace)). The model is then uploaded into the Solr model store and applied in the Solr for reranking. We can validate model performance with a test query set and our Offline Metrics Analyzer. This tool allows us to calculate NDCGs on different configurations of our search system. Thus, we are able to compare an LTR ranking with the status quo or analyze different model performances.

If you have experience in creating relevance judgements or if you have a different opinion about creating labeled data we would love to discuss this topic with you. So please contact us at JARVIS@otto.de. In the following posts we will discuss which data we used to implement LTR, how we measure search quality in our daily work and how we designed the pipeline for data collection and model training.

There is a lot to do: **Let's move together: Apply!**

[Job search](https://www.otto.de/de "Job search")

- ![Terraform Tips: Securing Infrastructure-as-Code&amp;#160;with Terratest – Part 3 
	](https://www.otto.de/jobs/de26-wAssets/img/blogs/techblog/blogauthors/weblication/wThumbnails/6c8c497d-a52f432f@889w.webp "Terraform Tips: Securing Infrastructure-as-Code&amp;#160;with Terratest – Part 3 
	")
	Nina
	0
	Data scienceDevelopmentCloud
	### Terraform Tips: Securing Infrastructure-as-Code with Terratest – Part 3
	Learn how to test Terraform modules with Terratest, detect errors early on and reliably secure IaC in CI/CD pipelines. …
	[view more](https://www.otto.de/jobs/en/blogs/techblog/terraform-tips-terratest-tests-part-3/)
- ![Team Jarvis](https://www.otto.de/jobs/de26-wAssets/img/blogs/techblog/blogauthors/weblication/wThumbnails/38c34043-a52f432f@1920w.webp "Team Jarvis")
	Team Jarvis
	0
	DevelopmentMachine learning
	### Learning to Rank is Rocket Science: How Clojure accelerates Our Machine Learning with Deep Neural Networks
	Learn how OTTO uses 🖥️ Clojure to build robust machine learning pipelines for learning to rank 🚀 and improves t…
	[view more](https://www.otto.de/jobs/en/blogs/techblog/learning-to-rank-with-clojure/)

Saved!

How interesting is this blogpost?

☆☆☆☆☆

★★★★★

We have received your feedback.