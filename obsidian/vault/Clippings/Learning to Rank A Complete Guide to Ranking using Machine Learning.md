---
title: "Learning to Rank: A Complete Guide to Ranking using Machine Learning"
source: "https://towardsdatascience.com/learning-to-rank-a-complete-guide-to-ranking-using-machine-learning-4c9688d370d4/"
author:
  - "[[Francesco Casalegno]]"
published: 2022-02-28
created: 2026-06-16
description: "Sorting items by relevance is crucial for information retrieval and recommender systems."
tags:
  - "clippings"
---
![Photo by Nick Fewings on Unsplash](https://towardsdatascience.com/wp-content/uploads/2022/02/1B2oK2SifPRPRE4nFSA5FMA-scaled.jpeg)

Photo by Nick Fewings on Unsplash

## Ranking: What and Why?

In this post, by " **ranking** " we mean **sorting documents by relevance** to find contents of interest **with respect to a query**. This is a fundamental problem of **[Information Retrieval](https://en.wikipedia.org/wiki/Information_retrieval)**, but this task also arises in many other applications:

1. **[Search Engines](https://en.wikipedia.org/wiki/Search_engine)** – Given a user profile (location, age, sex, …) a textual query, sort web pages results by relevance.
2. **[Recommender Systems](https://en.wikipedia.org/wiki/Recommender_system)** – Given a user profile and purchase history, sort the other items to find new potentially interesting products for the user.
3. **[Travel Agencies](https://en.wikipedia.org/wiki/Travel_agency)** – Given a user profile and filters (check-in/check-out dates, number and age of travelers, …), sort available rooms by relevance.
![Ranking applications: 1) search engines; 2) recommender systems; 3) travel agencies. (Image by author)](https://towardsdatascience.com/wp-content/uploads/2022/02/1v4MqXSXWyjCcjpdW9tD3Og.png)

Ranking applications: 1) search engines; 2) recommender systems; 3) travel agencies. (Image by author)

Ranking models typically work by predicting a **relevance score *s = f* (*x*)** for each input ***x* = (*q, d*)** where ***q*** **is a** **query** and ***d*** **is a document**. Once we have the relevance of each document, we can sort (i.e. rank) the documents according to those scores.

![Ranking models rely on a scoring function. (Image by author)](https://towardsdatascience.com/wp-content/uploads/2022/02/1gX8d-0eerlTHEAv716QC8Q.png)

Ranking models rely on a scoring function. (Image by author)

The scoring model can be implemented using various approaches.

- **[Vector Space Models](https://en.wikipedia.org/wiki/Vector_space_model)** – Compute a vector embedding (e.g. using [Tf-Idf](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) or [BERT](https://arxiv.org/abs/1908.10084)) for each query and document, and then compute the relevance score ***f* (*x*) *\= f* (*q, d*)** as the cosine similarity between the vectors embeddings of ***q*** and ***d***.
- **[Learning to Rank](https://en.wikipedia.org/wiki/Learning_to_rank)** – The scoring model is a Machine Learning model that learns to predict a score ***s*** given an input ***x* = (*q, d*)** during a training phase where some sort of ranking loss is minimized.

In this article we focus on the latter approach, and we show how to implement **Machine Learning models for Learning to Rank**.

## Ranking Evaluation Metrics

Before analyzing various ML models for Learning to Rank, we need to define which metrics are used to evaluate ranking models. These metrics are computed on the **predicted documents ranking**, i.e. the **\_k-\_th top retrieved document** is the *k* -th document with highest predicted score ***s***.

### Mean Average Precision (MAP)

![MAP - Mean Average Precision. (Image by author)](https://towardsdatascience.com/wp-content/uploads/2022/02/1I_Ab19M4GKj2PrtJaZ_Nuw.png)

MAP – Mean Average Precision. (Image by author)

[Mean Average Precision](https://en.wikipedia.org/wiki/Evaluation_measures_\(information_retrieval\)#Mean_average_precision) is used for tasks with **binary relevance**, i.e. when the true score *y* of a document *d* can be only **0 (*non relevant*) or 1 (*relevant*)**.

For a given query *q* and corresponding documents *D* = **\_{\_d₁, …, \_d\_ₙ}, we check how many of the top** k retrieved documents are relevant **(y=1) or no *t* (y=0)., in order to compu **te precisi** o *n* Pₖ a **nd reca** l *l* Rₖ. F *or k* =** 1…n we get differe *nt* Pₖ \_\_ \_an\_d Rₖ values that define **the precision-recall** curve: the area under this curve is **the Average Precision** (AP).

Finally, by computing the average of AP values for a set of *m* queries, we obtain the **Mean Average Precision (MAP)**.

### Discounted Cumulative Gain (DCG)

![DCG - Discounted Cumulative Gain. (Image by author)](https://towardsdatascience.com/wp-content/uploads/2022/02/1a8eRGOleBZYqehb-SNLCZw.png)

DCG – Discounted Cumulative Gain. (Image by author)

[Discounted Cumulative Gain](https://en.wikipedia.org/wiki/Discounted_cumulative_gain) is used for tasks with **graded relevance**, i.e. when the true score *y* of a document *d* is a discrete value in a scale measuring the relevance w.r.t. a query *q*. A typical scale is **0 (*bad*), 1 (*fair*), 2 (*good*), 3 (*excellent*), 4 (*perfect*)**.

For a given query *q* and corresponding documents *D* = **\_{\_d₁, …, \_d\_ₙ}, we consider the the** k-th top retrieved document. Th **e gai** n *Gₖ* = \_2^y\_ₖ – 1 measures how useful is this document (we want documents with high relevance!), while th **e discoun** t *Dₖ* = 1/lo *g* (k+1) penalizes documents that are retrieved with a lower rank (we want relevant documents in the top ranks!).

The sum of the **discounted gain** terms G\_ₖ\_D *ₖ* for *k =* 1… *n* is the **Discounted Cumulative Gain (DCG)**. To make sure that this score is bound between 0 and 1, we can divide the measured DCG by the ideal score IDCG obtained if we ranked documents by the true value *yₖ*. This gives us the **Normalized Discounted Cumulative Gain (NDCG)**, where NDCG = DCG/IDCG.

Finally, as for MAP, we usually compute the average of DCG or NDCG values for a set of *m* queries to obtain a mean value.

## Machine Learning Models for Learning to Rank

To build a Machine Learning model for ranking, we need to define **inputs**, **outputs** and **loss function**.

- **Input** – For a query ***q*** we have ***n*** documents ***D* = \_{\_** d₁, …, \_ **d** \_ₙ **}** to be ranked by relevance. The elements **\_x *ᵢ =* (\_q, \_d\_ᵢ)** are the inputs to our model.
- **Output** – For a query-document input *xᵢ* = (*q*, *dᵢ*), we assume there exists a true **relevance score *yᵢ***. Our model outputs a **predicted score** ***sᵢ = f* (*xᵢ*)***.*

All Learning to Rank models use a base Machine Learning model (e.g. [Decision Tree](https://en.wikipedia.org/wiki/Decision_tree_learning) or [Neural Network](https://en.wikipedia.org/wiki/Artificial_neural_network)) to compute *s* = *f* (*x*). The choice of the **loss function** is the distinctive element for Learning to Rank models. In general, we have **3 approaches**, depending on how the loss is computed.

1. **Pointwise Methods** – The total loss is computed as the sum of loss terms defined on **each document *dᵢ*** (hence ***pointwise***) as the distance between the predicted score ***sᵢ*** and the ground truth ***yᵢ***, for \_i=\_1… *n*. By doing this, we transform our task into a **regression problem,** where we train a model to predict *y.*
2. **Pairwise Methods** – The total loss is computed as the sum of loss terms defined on **each pair of documents \_dᵢ, dⱼ** *(hence* **pairwise** \_), for \_i, j=\_1… *n*. The objective on which the model is trained is to predict whether ***yᵢ > yⱼ*** or not, i.e. which of two documents is more relevant. By doing this, we transform our task into a **binary classification problem**.
3. **Listwise Methods** – The loss is directly computed on the whole list of documents (hence ***listwise***) with corresponding predicted ranks. In this way, ranking metrics can be more directly incorporated into the loss.
![Machine Learning approaches to Learning to Rank: pointwise, pairwise, listwise. (Image by author)](https://towardsdatascience.com/wp-content/uploads/2022/02/1s3CQuNRWcQNkQKd8Met-MA.png)

Machine Learning approaches to Learning to Rank: pointwise, pairwise, listwise. (Image by author)

### Pointwise Methods

The pointwise approach is the simplest to implement, and it was the first one to be proposed for Learning to Rank tasks. The loss directly measures the distance between ground true score ***yᵢ*** and predicted ***sᵢ*** so we treat this task by effectively solving a regression problem. As an example, **[Subset Ranking](https://link.springer.com/chapter/10.1007/11776420_44)** uses a [Mean Square Error (MSE)](https://en.wikipedia.org/wiki/Mean_squared_error) loss.

![MSE loss for pointwise methods as in Subset Ranking. (Image by author)](https://towardsdatascience.com/wp-content/uploads/2022/02/1h8zgsEZCktLerxfkY51bQA.png)

MSE loss for pointwise methods as in Subset Ranking. (Image by author)

### Pairwise Methods

The main issue with pointwise models is that true relevance scores are needed to train the model. But in many scenarios training data is available only with **partial information,** e.g. we only know which document in a list of documents was chosen by a user (and therefore is *more relevant*), but we don’t know exactly *how relevant* is any of these documents!

For this reason, pairwise methods don’t work with absolute relevance. Instead, they work with **relative preference**: given two documents, we want to predict if the first is more relevant than the second. This way we solve a **binary classification task** where we only need the ground truth *yᵢⱼ* (\_=\_1 if *yᵢ > yⱼ*, 0 otherwise) and we map from the model outputs to probabilities using a [logistic function](https://en.wikipedia.org/wiki/Logistic_function): *sᵢⱼ* = σ(*sᵢ – sⱼ*). This approach was first used by **[RankNet](https://icml.cc/Conferences/2015/wp-content/uploads/2015/06/icml_ranking.pdf)**, which used a [Binary Cross Entropy (BCE)](https://en.wikipedia.org/wiki/Cross_entropy) loss.

![BCE loss for pairwise methods as in RankNet. (Image by author)](https://towardsdatascience.com/wp-content/uploads/2022/02/1OnqFlRq7aYN8szI52jS0MA.png)

BCE loss for pairwise methods as in RankNet. (Image by author)

RankNet is an improvement over pointwise methods, but all documents are still given the same importance during training, while we would want to give **more importance to documents in higher ranks** (as the DCG metric does with the discount terms).

Unfortunately, rank information is available only after sorting, and sorting is non differentiable. However, to run [Gradient Descent](https://en.wikipedia.org/wiki/Gradient_descent) optimization we don’t need a loss function, we only need its gradient! **[LambdaRank](https://www.microsoft.com/en-us/research/publication/learning-to-rank-with-non-smooth-cost-functions/)** defines the gradients of an implicit loss function so that documents with high rank have much bigger gradients:

![Gradients of an implicit loss function as in LambdaRank. (Image by author)](https://towardsdatascience.com/wp-content/uploads/2022/02/1BFTD0koJ-AbNNQd2TOd92w.png)

Gradients of an implicit loss function as in LambdaRank. (Image by author)

Having gradients is also enough to build a [Gradient Boosting](https://en.wikipedia.org/wiki/Gradient_boosting) model. This is the idea that **[LambdaMART](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/MSR-TR-2010-82.pdf)** used, yielding even better results than with LambdaRank.

### Listwise Methods

Pointwise and pairwise approaches transform the ranking problem into a surrogate regression or classification task. Listwise methods, in contrast, solve the problem more **directly by maximizing the evaluation metric**.

Intuitively, this approach **should give the best results**, as information about ranking is fully exploited and the NDCG is directly optimized. But the obvious problem with setting **Loss = 1 – NDCG** is that the rank information needed to compute the discounts Dₖ is only available after **\*\* sortin** g **documents based on predicted scores, and** sortin **g** is non-differentiabl\*\*e. How can we solve this?

A **first approach** is to use an iterative method where **ranking metrics are used to re-weight** instances at each iteration. This is the approach used by **[LambdaRank](https://www.microsoft.com/en-us/research/publication/learning-to-rank-with-non-smooth-cost-functions/)** and **[LambdaMART](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/MSR-TR-2010-82.pdf)**, which are indeed between the pairwise and the listwise approach.

A **second approach** is to approximate the objective to make it differentiable, which is the idea behind **[SoftRank](https://www.researchgate.net/publication/221520227_SoftRank_optimizing_non-smooth_rank_metrics)**. Instead of predicting a deterministic score *s* = *f* (*x*), we predict a **smoothened probabilistic score** *s~* 𝒩(f\_(*x*)\_, σ *²*). The r **anks k \_** a *re non-continuous functions of p\*\*redicted scores s*,\_ **but thanks to the smoothening we can compute p** robability distributions for the ranks **of each document. Finally, we optimize S** oftNDCG,\*\* the expected NDCG over this rank distribution, which is a smooth function.

![Uncertainty in scores produce a smooth loss in SoftRank. (Image by author)](https://towardsdatascience.com/wp-content/uploads/2022/02/1MqY4bnrcmOVhHKBg5LsBCA.png)

Uncertainty in scores produce a smooth loss in SoftRank. (Image by author)

A **third approach** is consider that each ranked list corresponds to a permutation, and define a **loss over space of permutations**. In **[ListNet](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-2007-40.pdf)**, given a list of scores *s* we define the probability of any permutation using the **[Plackett-Luce model](https://en.wikipedia.org/wiki/Discrete_choice#J._Exploded_logit)**. **\*\* Then, our loss is easily computed as the** Binary Cross-Entropy distance **between true and predicted** probability distributions over the space of permutations\*\*.

![Probability of various permutation using Plackett-Luce model in ListNet. (Image by author)](https://towardsdatascience.com/wp-content/uploads/2022/02/1ulNdD-rW6OF0x46sPg5jqw.png)

Probability of various permutation using Plackett-Luce model in ListNet. (Image by author)

Finally, the **[LambdaLoss](https://research.google/pubs/pub47258.pdf)** paper introduced a new perspective on this problem, and created a **generalized framework** to define new listwise loss functions and achieve **state-of-the-art accuracy**. The main idea is to frame the problem in a rigorous and general way, as a **[mixture model](https://en.wikipedia.org/wiki/Mixture_model)** where the ranked list *π* is treated as a hidden variable. Then, the loss is defined as the negative log likelihood of such model.

![LambdaLoss loss function. (Image by author)](https://towardsdatascience.com/wp-content/uploads/2022/02/1zj5QvE_HkcKrkOrr96Mq4w.png)

LambdaLoss loss function. (Image by author)

The authors of the LambdaLoss framework proved two essential results.

1. All other listwise methods (RankNet, LambdaRank, SoftRank, ListNet, …) are **special configurations** of this general framework. Indeed, their losses are obtained by accurately choosing the **likelihood** ***p* (*y | s, π*)** and the **ranked list distribution *p* (*π | s*)**.
2. This framework allows us to define metric-driven loss functions directly connected to the ranking metrics that we want to optimize. This allows to **significantly improve the state-of-the-art on Learningt to Rank tasks.**

## Conclusions

Ranking problem are found everywhere, from information retrieval to recommender systems and travel booking. Evaluation metrics like MAP and NDCG take into account both rank and relevance of retrieved documents, and therefore are difficult to optimize directly.

Learning to Rank methods use Machine Learning models to predicting the relevance score of a document, and are divided into 3 classes: pointwise, pairwise, listwise. On most ranking problems, listwise methods like LambdaRank and the generalized framework LambdaLoss achieve state-of-the-art.