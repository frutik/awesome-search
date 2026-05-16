---
title: "The influence of TF-IDF algorithms in eCommerce search"
source: "https://medium.com/empathyco/the-influence-of-tf-idf-algorithms-in-ecommerce-search-e7cb9ab8e662"
author:
  - "[[David Argüello Sánchez]]"
published: 2018-08-24
created: 2026-05-16
description: "More"
tags:
  - "clippings"
---
At a basic level, information retrieval systems work by receiving a term and returning a set of documents relevant for that term. The magic that happens inside these systems is defined by algorithms that, relying on probability and statistical measures, are responsible for deciding which documents are relevant for a term and the ranking of those documents. One of these statistical measures is TF-IDF.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*CA_n3qwSCJIOofvZEkvDHA.jpeg)

Photo by Becca McHaffie on Unsplash

**What is TF-IDF?**

TF-IDF stands for Term Frequency (TF) and Inverse Document Frequency (IDF). It is a numerical, statistical measure that can be used to determine the relevance of a term in a document or in a collection. Particularly, in information retrieval systems it is used to retrieve relevant documents for a given term.

TF-IDF infers relevance based on two principles:

- The more times a term appears in a document, the more relevant the document is for that particular term (TF).
- The rarer a term is in a field, the more relevant the document is for that particular term (IDF).

This post will focus on the impact of TF-IDF in eCommerce search, more general detail on TF-IDF and how it is calculated can be found [here](https://en.wikipedia.org/wiki/Tf-idf#Term_frequency_2).

**How is the TF-IDF algorithm used?**

TF-IDF is used in information retrieval algorithms, in combination with some other normalisation values, to infer document relevance for a given term.

Using this algorithm makes sense from two points of view. Firstly, from the TF perspective, every document containing a term can be relevant, but if a document contains a term 10 times, the probability that the document is focused on a subject related to that term is much higher. If we think about an information retrieval system built to retrieve old news from a newspaper, when a user searches for a term “car”, he would be more likely to be looking for a car article, containing sentences such as “This car…”, “It’s a car that…”, than news about a bank robbery in which there is a line saying, “the robbers escaped in a car.” In this type of search the repetition of a term increases the probability that the term is important in the document.

Secondly, taking the IDF perspective, when a field contains the term in a less common field, it is given much more information than in a common one as the relevancy is deemed higher.

Following the same example of a newspaper, for a piece of news in which the term “car” is really important, the word would probably appear in the title of the article. However, the number of times that this term appears in the title would be much lower than in the corpus. This can also be done by applying different weights to each searchable field, but this is a way of doing it out of the box.

As mentioned above, after gathering the vanilla TF-IDF scores, algorithms use the same other normalisation values such as:

- Length normalisation: This normalisation value is based on the idea that finding a term in a corpus of 10 words is much more relevant than finding it in a corpus of 100 words.
- Logarithmical normalisation: This kind of normalisation is used to soften the impact of each extra match. More matches of a term in a document is still more important, however, the impact of the second match in the scoring is lower than the first one, the impact of the third one is lower than the second one and so on.
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*nEUpCOGpGMiOBscp-H3W0Q.jpeg)

TF-IDF Score using logarithmical normalisation

There are some other normalisations that can be applied over TF or IDF values, you can check them all [here](https://en.wikipedia.org/wiki/Tf%E2%80%93idf#Term_frequency_2).

**The impact of TF-IDF in eCommerce search**

The example of a newspaper is a good way to understand how TF-IDF works, however, from a search perspective, an eCommerce catalogue is very different from a newspaper library. In eCommerce, corpuses are smaller than those of a newspaper and products are tagged or listed based on marketing purposes, not specifically for a search engine.

This means that the assumption that term repetition makes a document more relevant and that finding a term in a less common used field is more accurate, can cause some weird results that, while they might make sense from an engineering point of view, they certainly don’t from a customer perspective.

It’s also worth remarking that when a search engine is built for an eCommerce platform, it doesn’t have to retrieve only documents that contain a certain term, but ones that are relevant to that term from a commercial perspective. What that means is it needs to find products that the user is looking for and also the products that the retailer wants to sell.

**The impact of TF**

In order to show why term frequency doesn’t always imply that a document is more relevant, let’s think about a technology eCommerce platform where users can search for laptops, tablets, smartphones, tvs and their accessories… and let’s use the following context:

- The search engine contains 400 documents.
- The term that is going to be searched is “iPad.”
- In order to simplify this example, the term “iPad” is only going to be searched in the name field.
- Let’s say that there are 35 documents that contain “iPad” at least once in the name field.
- Let’s say that there are 20 “iPad” documents categorised as iPad.
- We’ll use graphs to show the scoring distribution for the first ten possible matches.
- To calculate the scoring distribution vanilla TF-IDF will be used (Product of TF and IDF without any normalisation value).

When a user searches for “iPad”, he expects to see all the iPads the store offers. However, when the search engine relies on a TF-IDF system, a common result would be to see some iPad accessories ranked higher than any of the actual iPads.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*HPyuCv3fmlN08zkDSefLPw.jpeg)

“iPad” search score distribution using TF-IDF

As you can see in the graph, the most relevant results for the term “iPad” are in fact iPad cases. This is because we’ve used a simple search using just the one single field. One way to fix this kind of situation is by applying rules. For example, it’s most likely here that the products have been categorised, so boosting those belonging to the “iPad” category could resolve this as the search will then show iPads on top of the results and all the accessories after them.

The truth though, as shown in the graph below, is that the issue will still remain. While iPads have been boosted so they now have a higher scoring than related products, those ranked higher using the first approach, nevertheless the final scoring still doesn’t yet place them within the top results.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*K_GI-YPdPyfHOGsnTHaHKQ.jpeg)

“iPad” search score distribution using TF-IDF and a boost over iPad category

The reason for this is the Term Frequency. An iPad usually has a name such as “iPad Mini”, whereas an iPad case could have a name like “Black iPad mini case compatible with iPad mini 2 and iPad mini 3.” As you can see, the term “iPad” is repeated three times in the case name while the real iPad, that should be the most relevant document for this term, only contains the term once.

So, while these results may look good from a Boolean relevance perspective, all containing the term “iPad”, it doesn’t meet the user’s or retailer’s expectations when searching for an iPad.

One possible solution is disabling the TF-IDF scoring by using a Boolean model whereby the existence of the term in the field would result in a score of 1 and the absence in a score of 0. After that, any general rule applied, like the simple boost by category (as in the graph below) or using different fields with different relevancies, would lead to actual iPads taking the top results.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*__msd_b5cFDiW7e3RXgw7Q.jpeg)

“iPad” search score distribution using a boost over iPad category after disabling TF-IDF

**The Impact of IDF**

To understand the impact of IDF let’s change the platform and use a clothing example using the following context:

- The search engine contains 2,000 documents.
- The term that is going to be used is “Polo.”
- In order to simplify this example, the term “Polo” is only going to be searched in the name field and in the brand field.
- Let’s say that there are 200 documents containing the term “Polo” in both fields, we’re going to also apply a search configuration whereby the field name is weighted as two times more relevant than the brand field.
- Let’s say that there are 150 documents containing “Polo” at least once in the name field and there are 50 documents containing “Polo” at least once in the brand field.
- We’ll use graphs to show the scoring distribution for the first ten possible matches for the term “Polo.”
- To calculate the scoring distribution vanilla TF-IDF is used (Product of TF and IDF without any normalisation value).

When a user searches for “Polo”, he’s actually searching for “Polo shirts.” However, while there are polo shirts of different brands, there is a brand called “Polo Ralph Lauren” so, instead of seeing polo shirts on top of the grid, the user could see some “Polo Ralph Lauren” shirts, jackets, sweatshirts…

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*V2IYd3lvkLA4YlhqijztGA.jpeg)

“Polo” search score distribution using TF-IDF

The reason in this case is that the term “Polo” in the brand field, is much rarer than in the name field, so IDF infers that the “Polo” brand documents are the more relevant than the “Polo” name ones, even though name ones have been weighted with two times more relevancy in the scoring.

As happened with the iPad example, this looks good from a Boolean relevance perspective, since the term “Polo” is contained in all the documents and there is no guarantee that the user didn’t want to search for the brand, but it doesn’t make any sense from either the customer or retailer perspectives. As shown in the graph below, when we disable the TF-IDF, the results align more with user’s and retailer’s expectations.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*nuop4oyU4JwhX9M_rkaQnw.png)

“Polo” search score distribution after disabling TF-IDF

**Other Factors**

When a search engine is built for an eCommerce platform, actually for any business, retailers want to control each field’s relevancy for search terms based on their knowledge of their own business. This means that they want to make sure that matches are ranked based on the relevancy of the field the term matched.

In some cases, they may want name matching to be more relevant than category matching and category matching to be more relevant than description ones, or vice versa. However, as we saw with the iPad and Polo examples, when using a TF-IDF algorithm different values (TF, IDF, normalisations…) are applied to infer relevance that might cause description matches to be put on top of name matches, causing confusing results for customers.

**Conclusions**

TF-IDF is an algorithm that infers relevance based on the principles of “repetition” and “rareness.” While it’s a good relevancy algorithm and works in a lot of use cases, we’ve seen that under certain conditions it also causes some issues.

Furthermore, in the two use cases used we’ve been able to apply different rules to boost products, or to make the fields more relevant, but while these changes could work in these specific cases, there would be a lot of use cases that couldn’t be fixed manually without “breaking” the results for other search terms.

Each platform is different and has its own requirements, but through disabling TF-IDF we’ve helped [EmpathyBroker](https://www.empathybroker.com/) customers to remove several of the merchandising rules required for these edge cases.

Disabling TF-IDF is not a silver bullet, but it’s enabled [EmpathyBroker](https://www.empathybroker.com/) ’s customers to be able to remove several merchandising rules required for edge cases. However, for us this is only one part of a process to improve and optimise our search engine.

The relevance problem is much more complex and while this change has helped us to solve some term centric issues, there are other user related issues that need to be addressed. Relevancy problems are also about people! That’s why we’ve been working on our new Contextualize product that uses behavioural data to improve our ranking models, more details coming soon….