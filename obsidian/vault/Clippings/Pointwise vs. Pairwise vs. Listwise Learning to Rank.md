---
title: "Pointwise vs. Pairwise vs. Listwise Learning to Rank"
source: "https://medium.com/@nikhilbd/pointwise-vs-pairwise-vs-listwise-learning-to-rank-80a8fe8fadfd"
author:
  - "[[Nikhil Dandekar]]"
published: 2016-09-29
created: 2026-06-16
description: "1.1K"
tags:
  - "clippings"
---
![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*4c2AyEeylx-OjXLQZcOWGg.png)

At a high level, pointwise, pairwise and listwise approaches differ in how many documents you consider at a time in your loss function when training your model.

### Pointwise approaches

Pointwise approaches look at a **single document** at a time in the loss function. They essentially take a single document and train a classifier / regressor on it to predict how relevant it is for the current query. The final ranking is achieved by simply sorting the result list by these document scores. For pointwise approaches, the score for each document is independent of the other documents that are in the result list for the query.

All the standard regression and classification algorithms can be directly used for pointwise learning to rank.

### Pairwise approaches

Pairwise approaches look at a **pair of documents** at a time in the loss function. Given a pair of documents, they try and come up with the optimal ordering for that pair and compare it to the ground truth. The goal for the ranker is to minimize the number of inversions in ranking i.e. cases where the pair of results are in the wrong order relative to the ground truth.

Pairwise approaches work better in practice than pointwise approaches because predicting relative order is closer to the nature of ranking than predicting class label or relevance score. Some of the most popular Learning to Rank algorithms like ==RankNet, LambdaRank and LambdaMART \[1\] \[2\] are pairwise approaches.==

### Listwise approaches

Listwise approaches directly look at the entire **list of documents** and try to come up with the optimal ordering for it. There are 2 main sub-techniques for doing listwise Learning to Rank:

1. Direct optimization of IR measures such as NDCG. E.g. SoftRank \[3\], AdaRank \[4\]
2. Minimize a loss function that is defined based on understanding the unique properties of the kind of ranking you are trying to achieve. E.g. ListNet \[5\], ListMLE \[6\]

Listwise approaches can get fairly complex compared to pointwise or pairwise approaches.

Here are some good resources in case you want to learn more about this:

- [Learning to Rank for Information Retrieval](http://www2009.org/pdf/T7A-LEARNING%20TO%20RANK%20TUTORIAL.pdf)
- [A Short Introduction to Learning to Rank](http://times.cs.uiuc.edu/course/598f14/l2r.pdf)

## Footnotes

[\[1\]](https://www.quora.com/What-are-the-differences-between-pointwise-pairwise-and-listwise-approaches-to-Learning-to-Rank/answer/Nikhil-Dandekar#cite-eGYzS) [From RankNet to LambdaRank to LambdaMART: An Overview — Microsoft Research](https://www.microsoft.com/en-us/research/publication/from-ranknet-to-lambdarank-to-lambdamart-an-overview/)

[\[2\]](https://www.quora.com/What-are-the-differences-between-pointwise-pairwise-and-listwise-approaches-to-Learning-to-Rank/answer/Nikhil-Dandekar#cite-HCtoU) [What is the intuitive explanation of Learning to Rank and algorithms like RankNet, LambdaRank and LambdaMART?](https://www.quora.com/What-is-the-intuitive-explanation-of-Learning-to-Rank-and-algorithms-like-RankNet-LambdaRank-and-LambdaMART/answer/Nikhil-Dandekar)

[\[3\]](https://www.quora.com/What-are-the-differences-between-pointwise-pairwise-and-listwise-approaches-to-Learning-to-Rank/answer/Nikhil-Dandekar#cite-nospd) [SoftRank: Optimising Non-Smooth Rank Metrics — Microsoft Research](https://www.microsoft.com/en-us/research/publication/softrank-optimising-non-smooth-rank-metrics/)

[\[4\]](https://www.quora.com/What-are-the-differences-between-pointwise-pairwise-and-listwise-approaches-to-Learning-to-Rank/answer/Nikhil-Dandekar#cite-FKcpw) [AdaRank on Letor](http://research.microsoft.com/en-us/um/beijing/projects/letor/Baselines/AdaRank.html)

[\[5\]](https://www.quora.com/What-are-the-differences-between-pointwise-pairwise-and-listwise-approaches-to-Learning-to-Rank/answer/Nikhil-Dandekar#cite-ldEdU) [Learning to Rank: From Pairwise Approach to Listwise Approach — Microsoft Research](https://www.microsoft.com/en-us/research/publication/learning-to-rank-from-pairwise-approach-to-listwise-approach/)

\[6\] [Position-Aware ListMLE: A Sequential Learning Process for Ranking](http://auai.org/uai2014/proceedings/individuals/164.pdf)