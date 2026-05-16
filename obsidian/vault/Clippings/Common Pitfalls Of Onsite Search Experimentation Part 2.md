---
title: "Common Pitfalls Of Onsite Search Experimentation Part 2"
source: "https://www.searchhub.io/en/common-pitfalls-of-onsite-search-experimentation-part-2/"
author:
  - "[[Siegfried Schüle]]"
published: 2023-11-23
created: 2026-05-16
description: "If your business case involves only single-item baskets and 90% of your orders consist of only one article, you can skip this post. All others: welcome to another trap in search experimentation!"
tags:
  - "clippings"
---
In one of our latest blog posts, my colleague Andreas highlighted how **session-based segmentation** in A/B-tests might lead to wrong conclusions. I highly recommend you [**read his post**](https://www.searchhub.io/common-pitfalls-of-search-experimentation/) before continuing. In this blog post, I’ll show how **session-based analysis** in A/B-tests will destroy your precious work when optimizing site search.

> **tl;dr:** If your business case involves only single-item baskets and 90% of your orders consist of only one article, you can skip this post. All others: welcome to another trap in search experimentation!

## Measuring the Unmeasurable

Let’s say you and your team put significant effort into optimizing your product rankings for search result pages (SERP). Most of the formerly problematic SERPs now look much better and seem to reflect the requirements of your business more than before. However, if your key performance indicator for success is “increase shop revenue through onsite search”, you’d be short-changing yourself and jeopardizing your business’s bottom-line. Let me explain.

First of all, it’s a good thing that you understand how crucial it is, to test changes in the fundamentals of your onsite search algorithm. I mean, it’s clear that these changes influence lots of search results, which you would never even think about. Let alone be able to judge personally. And proving the quality of your work might also influence your personal bonus. That’s why you do an A/B-test before rolling out such changes to your whole audience. You do that, right? Right???

Well, after a while, you check the results in your A/B-test or analytics tool. Following standard best practices not only of Google Analytics but also many (if not all) web analytics tools, the result might look like this:

![A/B test results present a possible new ranking model.](https://www.searchhub.io/wp-content/uploads/2023/03/AB_Test_Ambiguous_Results-2048x416.webp)

(report showing ambiguous results: Although AddToBasket-ratio increased significantly, no significant increase in overall conversion rate was measured, while revenue decreased slightly).

What will your management’s decision be based on this result? Will they crack open a bottle of champagne in your honor, as you obviously have found a great option to increase revenue? Will they grant you a long – promised bonus? Most likely not, unfortunately. A glass of water will suffice, and you should be thankful for not being fired. After all, you shrank the revenue.

## The problem: You didn’t test what you intended to test.

What you wanted to test: how each search result page performs with your new ranking algorithm compared to previous rankings.

What you actually tested: All carts and orders of all users who happened to perform at least one site search during their visit.

Imagine you were able to show your management a detailed view of all search-related sessions, with specific explanations of each position in the basket that was really driven by search requests. Which products were not bought because they could not be found? Which other products were bought but not search related?

Maybe similar to this example here:

![a table to illustrate differences in A/B test significance.](https://www.searchhub.io/wp-content/uploads/2023/03/AB_Test_Ambiguous_Results_2.webp)

(detailed view of search related sessions showing improved search performance when measured directly)

Chances are high that someone will tap on your shoulder stating: “We see very nice improvements to our customer journeys where search is involved. You did an awesome job optimizing the search.”

### So what happened here?

A vast majority of visits will not start with a customer thinking: “Such a nice day. I’d finally like to use the search box in myfavoriteshop.com”. Instead, they will reach your site via organic or paid links or click on a link in your newsletter promoting some interesting stuff – well, you know all the sources where they come from, that’s potatoes for your analytics tool.

In many cases, the first product to be put into the basket is more or less easy going. But now they start to think: “I’ll have to pay €5 for shipping, what else could I order to make it worth it?” Not only does search become interesting at this point, but your business begins creating opportunities. Larger order – higher margin, as your transaction costs sink. A well-running search engine might make the key difference here. **But, do not attribute the revenue of the first cart position to the search engine**, as it had nothing to do with it!

If your analytics or A/B-testing tool shows some report starting with “visits with site search”, a red alert should go off in your head. This is a clear indication that the report mixes up a lot of stuff unrelated to your changes.

### Why is this a problem?

Search is important for your e-commerce site’s success. Because statistics love large numbers. It’s true, search provides large numbers, but order numbers are much smaller. Let me give you a simplified, but nevertheless valid example: Let’s assume your search has improved by 10%. Naturally, this should also be visible as a 10% increase in orders overall:

![A/B Test results - control vs. variant.](https://www.searchhub.io/wp-content/uploads/2023/11/Search_Performance_Uplift_Significance_Measurement-2048x626.webp)

Now we can ask statistic tools if this is significant. (You might want to start with here ). The result may come as a surprise.

[![There is no significant difference in success across the two groups tested.](https://www.searchhub.io/wp-content/uploads/2023/03/Search_Rate_of_Success_No_Difference.webp)](https://www.searchhub.io/wp-content/uploads/2023/03/Search_Rate_of_Success_No_Difference.webp)

[![Sample 2 success is more robust.](https://www.searchhub.io/wp-content/uploads/2023/11/Search_Rate_of_Success_1.webp)](https://www.searchhub.io/wp-content/uploads/2023/11/Search_Rate_of_Success_1.webp)

What? It affects my orders the same as my search overall (10% or 45 more orders), but it’s not significant? That’s because statistics want to provide a rather failsafe result. The lower the numbers and the smaller the relation between success (an order) and trials (each user), the harder the proof for an increase.

So chances are high that your A/B-test tool will consider the result as “insignificant” when trying to find the signal in the generic data. If you are Amazon or Google, this is not a problem you need to bother with – your numbers are large enough. Everyone else is obliged to dive deeper into the data.

## How do we do this at searchHub?

Over the past years, we have built a powerful framework to track search related events. Our searchCollector can be easily integrated into any e-commerce site. Without tracking any personal data, but very high consent ratios, we can collect traffic from most of your customers. We precisely track the customer journey from the search bar to the basket, also identifying when this journey is interrupted and a new, non-search-related micro-journey begins:

[![A/B Test results helpful for determining ideal product position.](https://www.searchhub.io/wp-content/uploads/2023/11/Search_KPI_Capture-2048x1098.webp)](https://www.searchhub.io/wp-content/uploads/2023/11/Search_KPI_Capture.webp)

This allows us to capture search-related KPIs in the most precise way. Not only can this be used for your daily search management work, but also for fine-grain A/B testing. By eliminating erroneous effects like non-search-related basket positions, we show exactly and with high statistical accuracy, how changes in your search algorithm, search engine or even search configuration perform.

## OK, understood - what can I do?

**First:** Make sure you’re precisely measuring the stuff you want to be measured.

**Second:** Don’t rely on summarized numbers, when you know that they include customer decisions that you cannot influence.

**Third:** Remember that in a random setup, 5% of all A/B tests will prove a significant difference. That’s what alpha=0.05 in your testing tool or A/B-test report means.