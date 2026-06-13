---
title: "How LambdaMART works - optimizing product ranking goals"
source: "https://softwaredoug.com/blog/2021/11/28/how-lammbamart-works"
author:
  - "[[Doug Turnbull]]"
published:
created: 2026-06-13
description: "LambdaMART directly optimizes whatever search relevance ranking metric matters to your business. This article details how this neat machine learning trick works to target what matters most to your product"
tags:
  - "clippings"
---
[Learning to Rank](https://en.wikipedia.org/wiki/Learning_to_rank) optimizes search relevance using machine learning. If you bring to Learning to Rank [training data](https://softwaredoug.com/blog/2021/02/21/what-is-a-judgment-list) – documents labeled as relevant / irrelevant for queries – you’ll get out a *ranking function* optimizing search closer to what users want.

That sounds wicked cool, right? It is!

So the data nerd in you wants to jump right into the *models*. What is this, you think, some kind of deep learning thing? Clearly it must have about twenty layers of transformers and involve some BERT somewhere, right?

Slow your roll there sparky.

With Learning to Rank the *objective function* holds the product goals we must optimize for - expressed as a ranking quality metric like [DCG](https://en.wikipedia.org/wiki/Discounted_cumulative_gain), [Precision](https://en.wikipedia.org/wiki/Precision_and_recall#Precision), or something tailored to your application. Some metric measuring the ‘how well-ordered’ your applications search results are. Ultimately this holds your power to make or break your search application, far more than the chosen model.

In this article, I’ll dig into how one classic method, LambdaMART, optimizes your search product’s relevance using a pair-wise swapping techniques.

## Exploring search training data…

To explore how LambdaMART optimizes relevance ranking, I’ll be using this [notebook from OpenSource Connection’s Hello-LTR](https://github.com/softwaredoug/hello-ltr/blob/lambda-mart-in-python/notebooks/elasticsearch/tmdb/lambda-mart-in-python.ipynb) project. (It’s used quite a bit in their [Learning to Rank training](https://opensourceconnections.com/training/hello-ltr-learning-to-rank/), which I highly recommend). This dataset uses [TheMovieDB corpus](https://softwaredoug.com/blog/2021/11/28/themoviedb.org) (TMDB) - a very dev friendly movie metadata database. It has a [toy training set](http://es-learn-to-rank.labs.o19s.com/title_judgments.txt) with about 40 labeled queries, each with a few dozen movies labeled as relevant or irrelevant.

The file format is… a bit weird.

```
...
4    qid:31     # 5825    christmas vacation
1    qid:31     # 13673    christmas vacation
1    qid:31     # 77499    christmas vacation
0    qid:31     # 16342    christmas vacation
...
4    qid:38     # 10191    how to train your dragon
3    qid:38     # 82702    how to train your dragon
0    qid:38     # 70057    how to train your dragon
```

But it’s not too bad, once you realize what’s being represented here:

```
<grade 0-4> qid:<query_id> # <doc_id> <query>
```

Where

- **grade -** labels a movie as relevant or irrelevant, here on a scale of 0-4 with 4 as most relevant, 0 as absolutely irrelevant.
- **query\_id** - gives each query a unique identifier
- **doc\_id** - gives us an identifier for the document (here a movie) being labeled as relevant or irrelevant
- **query** - the actual keywords sent to the search engine

As we see, each training example lives in a group (the query id). The goal is to get the search system to learn to place the relevant results (those with labels closer to 4) higher than the irrelevant ones. We want to optimize queries, moving them closer to the ideal ranking, most importantly – *as defined by our product needs –* If we do this well for all of our groups, we’ll have done our job!

Compare this to a *point-wise* problem, like predicting stock prices, such as with the data below

```
stock, actual, prediction
AAPL, $1241.00, $1005.53
SHOP, $1520.52, $1756.96
IBM, $125.51, $100.05
...
```

Here, there’s no concept of *grouping*. Each example lives on its own. You either get close to that company’s actual price when you make predictions, or you don’t. Other classic examples include classification - either the weather is rainy, or it’s not. Either the patient has cancer, or she doesn’t.

Finally, to make these predictions, we of course need *features*: the independent variables that help us predict relevance. In the case of our [Hello LTR notebook](https://github.com/softwaredoug/hello-ltr/blob/lambda-mart-in-python/notebooks/elasticsearch/tmdb/lambda-mart-in-python.ipynb), we log two simple features. In this format, features are appended to each row, with a numerical, 1-based, index for each variable.

```
...
4    qid:31    1:9.816013    2:6.6271276 # 5825    christmas vacation
1    qid:31    1:5.820251    2:10.637934 # 13673    christmas vacation
1    qid:31    1:4.895831    2:7.5047264 # 77499    christmas vacation
0    qid:31    1:0.0    2:13.546556 # 16342    christmas vacation
...
4    qid:38    1:17.98862    2:7.62917 # 10191    how to train your dragon
3    qid:38    1:15.820302    2:18.026808 # 82702    how to train your dragon
0    qid:38    1:7.4486933    2:0.0 # 70057    how to train your dragon
...
```

Features are

- **1:** title\_bm25 - the relevance score (BM25) of the query terms in the *title* field
- **2:** overview\_bm25 - the relevance score (BM25) of the query terms in the movie *overview* field.

We can think of these features as a vector describing the query-document relationship. Of course much of work is crafting these features! But feature development isn’t our focus in this article, instead we care about unlocking the ranking optimization underlying LambdaMART. Let’s do that now:)

## LambdaMART’s ‘one neat trick’

You’ve seen that optimizing relevance ranking [differs from your garden variety machine learning problem](https://opensourceconnections.com/blog/2017/08/03/search-as-machine-learning-prob/). It’s not a point-wise problem, like predicting stock prices or the weather, rather it’s a different kind of problem all together.

Tackling a new kind of problem sounds hard, and I’m lazy 😴😴.

Can we cheat somehow and make our list-wise ranking problem more of a point-wise one? Yes! LambdaMART is one such trick for doing this.

But first, what *is* [LambdaMART](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/MSR-TR-2010-82.pdf)? We have to tackle that definition in two parts - the *MART* and the *lambda*.

*MART* refers to the structure of the model. MART means [*Multiple Additive Regression Trees*](https://stanfordphd.com/MART.html) - in other words, many decision trees literally added together. Underneath LambdaMART lives a classic machine learning technique known as [Gradient Boosting](https://machinelearningmastery.com/gentle-introduction-gradient-boosting-algorithm-machine-learning/) for combining many models into a single prediction.

But we’ll set the set the gradient boosting, MARTy, many-trees part of LambdaMART aside for this article.

Instead, for today we zero-in on the *lambda* part of the model’s name. The *lambdas* refer to what’s being predicted. Lambdas are the reformulated point-wise prediction. The output of the magic trick that let’s us remain gleefully lazy😴.

Let’s jump into how LambdaMART does this. I’ll use “DCG” to refer to the ranking metric being optimized for, but just keep in your mind, you can swap out DCG for anything - precision or YourPersonalMetric™.

Each training round of gradient boosting (each new tree added to the MART) we perform the transformation of the list-wise loss function (i.e. DCG) into a point-wise supervised learning problem (i.e. something that looks like stock prices).

We go query-by-query. We swap every document, and accumulate that swap’s impact on the query’s DCG.

In other words, for each query, we follow this algorithm:

```
1. Sort each result by grade descending, to get the ideal ordering
2. Compute DCG for this perfect ordering (ideal_dcg)
3. For each document doc_i
    1. For each document doc_j
        if j > i:
            1. Swap doc_i, doc_j in the ranking
            2. Compute a new_dcg
            3. dcg_diff = ideal_dcg - new_dcg
            4. lambdas[doc_i] +=  dcg_diff
            5. lambdas[doc_j] -=  dcg_diff
```

I’ve included the Python code for this psuedocode [in our notebook](https://github.com/softwaredoug/hello-ltr/blob/lambda-mart-in-python/notebooks/elasticsearch/tmdb/lambda-mart-in-python.ipynb) in the function `compute_swaps`.

We swap every possible pair of documents for a query exactly once to build a table of *lambdas* for each scenario. We’re playing many ‘what if’ scenarios here - what if we screwed up the ranking and something was placed out of order. How big of a deal would that be for the query’s ranking metric important to our business?

Here’s the results of the algorithm for a movie query, `matrix`. We have the original movie “The Matrix” graded a 4. Sequels to The Matrix receive a grade of 3. Other Matrix related movies get a grade of 2 or 1. The remainder of the movies are irrelevant.

Notice the `lambda` values, indicating the impact of the DCG swaps if this result was screwed up. Not unexpectedly, screwing up the most relevant document has a huge impact on DCG. The overall impact of out-of-order swaps decreases more and more as you move down the ideal ordering.

```
keywords   docId  grade     lambda            features
matrix     603      4       86.475734         [11.657399, 10.040129]
matrix     605      3       27.686695         [9.456276, 0.0]
matrix     604      3       17.644949         [9.456276, 9.392262]
matrix   55931      2        7.377625         [0.0, 10.798681]
matrix   73262      1        0.875434         [0.0, 0.0]
matrix   33068      0       -3.766147         [0.0, 0.0]
matrix    3573      0       -4.009811         [0.0, 0.0]
matrix   12254      0       -4.201164         [0.0, 0.0]
...
matrix  125607      0       -5.369701         [0.0, 0.0]
matrix   21208      0       -5.396523         [0.0, 0.0]
matrix  181886      0       -5.421927         [0.0, 0.0]
matrix   21874      0       -5.446038         [0.0, 7.8627386]
matrix    4247      0       -5.468967         [0.0, 8.114125]
matrix   10999      0       -5.490810         [0.0, 11.466951]
matrix    1857      0       -5.511654         [0.0, 9.65805]
matrix   75404      0       -5.531576         [0.0, 0.0]
```

But like I emphasized, any metric could be used! What would happen if instead of dcg we tried to optimize *precision* of the top 10?

```
keywords   docId  grade  lambda    features
matrix     603      4    2.300     [11.657399, 10.040129]
matrix     605      3    1.725            [9.456276, 0.0]
matrix     604      3    1.725       [9.456276, 9.392262]
matrix   55931      2    1.150           [0.0, 10.798681]
matrix   73262      1    0.575                 [0.0, 0.0]
matrix   33068      0    0.000                 [0.0, 0.0]
matrix    3573      0    0.000                 [0.0, 0.0]
matrix   12254      0    0.000                 [0.0, 0.0]
...
matrix  125607      0   -0.325                 [0.0, 0.0]
matrix   21208      0   -0.325                 [0.0, 0.0]
matrix  181886      0   -0.325                 [0.0, 0.0]
matrix   21874      0   -0.325           [0.0, 7.8627386]
matrix    4247      0   -0.325            [0.0, 8.114125]
matrix   10999      0   -0.325           [0.0, 11.466951]
matrix    1857      0   -0.325             [0.0, 9.65805]
matrix   75404      0   -0.325                 [0.0, 0.0]
```

The lambdas with precision metric are far less dramatic, having to do with the simpler nature of the precision metric. While DCG has a strong bias towards ordering the top results correctly, precision doesn’t. So there’s no difference between getting “The Matrix” in the first position or the fifth position.

## Train a model to predict lambdas

We next train a [decision tree regression model](http://scikit-learn.org/stable/auto_examples/tree/plot_tree_regression.html) to predict the lambdas given the features (here we switch back to optimizing DCG).

```python
from sklearn.tree import DecisionTreeRegressor
tree = DecisionTreeRegressor()
tree.fit(train_set['features'].tolist(), train_set['lambda'])
```

Placing training data back into the model, we see close to expected predictions. Here we get a prediction for a movie with a strong title bm25 and strong overview bm25 score (similar to *The Matrix* for `matrix`)

```python
>> tree.predict([[11.6, 10.08]])   
array([106.58265768])
```

Notice how the output gets close to the ‘lambdas’ we computed earlier.

Similarly, for a movie with no relevance for title / overview, we predict the negative lambda values we’d expect:

```python
>> tree.predict([[0.0, 0.0]])
array([-4.06995481])
```

We can simplify the tree to better visualize how it works. For example, here we limit `max_leaf_nodes=4`

```python
tree = DecisionTreeRegressor(max_leaf_nodes=4)
tree.fit(train_set['features'].tolist(), train_set['lambda'])
plot_tree(tree)
```

![An example decision tree](https://softwaredoug.com/assets/media/learned_decision_tree.png)

See if you can follow along this first decision tree. Here X\[0\] is the `title_bm25` score. In this simpler model, the most important feature – title matches – comes up as the biggest decider in relevance. Decision trees work this way - trying to find the biggest factor in deciding the ultimate value of the model first.

The leaf’s `value` correspond to the prediction. And following the trees, the leaves are nicely displayed here in order of title relevance. The value ranges from -3 to 71 depending on the strength of the title score.

## Relevance Ranking - And we’re off!

We have the beginnings of a ranking function. If we input a set of document features, we get back out a score we could sort on. Even cooler: this relevance score *relates to the list-wise metric we wish to optimize!*

Let me state that again, because it’s, to me, one of the best things about this algorithm. We:

1. Gathered a set of relevance labels (hopefully correctly corresponding to our applications definition of relevance!)
2. Decided on some ranking metric for our use case (here DCG, but we could choose any metric, or make one up!)
3. Then we ran the algorithm on (1) and (2) as inputs, training a model on the result!

This means we can make domain-specific decisions about (1) and (2). What metrics make sense? How do we arrive at our relevance labels/grades?

If we’re supporting primarily a research use case, like in legal research, perhaps having many relevant results in the top N matters quite a bit. Perhaps, in this case, we want to base our relevance grades based on signals related to whether the searcher actually reads the articles. However, if our search is known-item search, where we know there’s exactly one right answer, perhaps we want a ranking metric that only examines whether the user clicked the first result. We want a metric like MRR or even Precision@1.

## Iterating on the model

This just begins the story of LambdaMART. Congrats! You’ve taken your first step into a larger world!

To *really* understand LambdaMART you’ll need to step back and consider the implication of the MARTy, gradient boosting, nature of the model - how many models work together in an *ensemble* to produce an even better prediction than just one model.

Most importantly, in gradient boosting, subsequent trees don’t just predict lambdas, but instead try to compensate for the errors in this first model. In this way, each iteration of the ensemble tries to move ever closer to the optimal ranking function. But that’s a blog post for another time!

We’ll leave it here for now. If you’d like to learn more, and go beyond this article, I encourage you to look at

1. The [Jupyter notebook that goes with this article](https://github.com/softwaredoug/hello-ltr/blob/lambda-mart-in-python/notebooks/elasticsearch/tmdb/lambda-mart-in-python.ipynb) with LambdaMART recreated
2. The Ranklib source code for LambdaMART, particularly [this function](https://github.com/o19s/RankyMcRankFace/blob/master/src/ciir/umass/edu/learning/tree/LambdaMART.java#L395)
3. [AI Powered Search](http://aipoweredsearch.com/) chapters 10-12

[Cunningham’s law applies here](https://en.wikipedia.org/wiki/Ward_Cunningham#Cunningham's_Law) - so please [get in touch](https://www.linkedin.com/in/softwaredoug) if I made any mistakes here! And always, I’d love to work with you at Shopify’s search team. Here’s one of our job listings for [relevance engineers](https://jobs.smartrecruiters.com/ni/Shopify/bedf9119-9a23-4fd3-8d8a-7fcbf168eca9-senior-relevance-engineer-search-discovery)!

Special Thanks to [Felipe Besson](https://felipebesson.com/), [John Berryman](http://blog.jnbrymn.com/) and [David Fernig](https://davefernig.com/) for reviewing this post and giving substantive edits and feedback!

---

### Enjoy softwaredoug in training course form!

#### Starting May 18!

Signup here - [http://maven.com/softwaredoug/cheat-at-search](http://maven.com/softwaredoug/cheat-at-search) [![](https://softwaredoug.com/assets/media/2026/cheat-at-search-social.png) ](https://maven.com/softwaredoug/cheat-at-search)I hope you join me at [Cheat at Search with Agents](https://maven.com/softwaredoug/cheat-at-search) to learn use agents in search. build better RAG and use LLMs in query understanding.

---