---
title: "We're Bringing Learning to Rank to Elasticsearch"
source: "https://opensourceconnections.com/blog/2017/02/14/elasticsearch-learning-to-rank/"
author:
  - "[[OpenSource Connections]]"
published: 2017-02-14
created: 2026-06-13
description: "We’re excited to release our Elasticsearch Learning to Rank Plugin. With learning to rank, a team trains a machine learning model to learn what users deem relevant."
tags:
  - "clippings"
---
It’s no secret that machine learning is revolutionizing many industries. This is equally true in search, where companies exhaust themselves capturing nuance through manually tuned search relevance. Mature search organizations want to get past the “good enough” of manual tuning to build smarter, self-learning search systems.

That’s why we’re excited to release our [Elasticsearch Learning to Rank Plugin](http://github.com/o19s/elasticsearch-learning-to-rank). What is learning to rank? With learning to rank, a team trains a machine learning model to learn what users deem relevant.

When implementing Learning to Rank you need to:

1. Measure what users deem relevant through analytics, to build a **judgment list** grading documents as exactly relevant, moderately relevant, not relevant, for queries
2. Hypothesize which **features** might help predict relevance such as TF\*IDF of specific field matches, recency, personalization for the searching user, etc.
3. Train a **model** that can accurately map features to a relevance score
4. Deploy the model to your **search infrastructure**, using it to rank search results in production

Don’t fool yourself: underneath each of these steps lie complex, hard technical and non-technical problems. There’s still no silver bullet. As we mention in [Relevant Search](http://manning.com/books/relevant-search), manual tuning of search results comes with many of the same challenges as a good learning to rank solution. We’ll have more to say about the many infrastructure, technical, and non-technical challenges of mature learning to rank solutions in future blog posts.

In this blog post I want to tell you about our work to integrate learning to rank within Elasticsearch. Clients ask us in nearly every [relevance consulting engagement](http://opensourceconnections.com/services/relevancy) whether or not this technology can help them. But while there’s a clear path in [Solr](https://issues.apache.org/jira/browse/SOLR-8542) thanks to Bloomberg, there hasn’t been one in Elasticsearch. Many clients want the modern affordances of Elasticsearch, but find this a crucial missing piece to selecting the technology for their search stack.

Indeed Elasticsearch’s Query DSL can rank results with tremendous power and sophistication. A skilled relevance engineer can use the query DSL to compute a broad variety of query-time features that might signal relevance. Giving quantitative answers to questions like

1. How much Is the search term mentioned in the title?
2. How long ago was the article/movie/etc published?
3. How does the document relate to user’s browsing behaviors?
4. How expensive is this product relative to a buyer’s expectations?
5. How conceptually related is the user’s search term to the subject of the article?

Many of these features aren’t static properties of the documents in the search engine. Instead they are **query dependent** – they measure some relationship between the user or their query and a document. And to readers of [Relevant Search](http://manning.com/books/relevant-search), this is what we term *signals* in that book.

So the problem becomes, how can we marry the power of machine learning with existing power of the Elasticsearch Query DSL? And that’s exactly what our plugin does: use Elasticsearch Query DSL queries as feature inputs to a machine learning model.

## How does it work? In short, (the TL; DR)

The plugin integrates [RankLib](https://sourceforge.net/p/lemur/wiki/RankLib/) and Elasticsearch. Ranklib takes as input a file with judgments and outputting a model in its own native, human-readable format. Ranklib then lets you trains models either programatically or via the command line. Once you have a model the Elasticsearch plugin contains the following

1. A custom Elasticsearch script language called **ranklib** that can accept ranklib generated models as an Elasticsearch scripts
2. An custom **ltr query** that inputs a list of Query DSL queries (the features) and a model name (what was uploaded at 1) and scores results

As learning to rank models can be expensive to implement, you almost never want to use ltr query directly. Rather you would [rescore](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-request-rescore.html) the top N results such as:

```js
{
    "query": {/*a simple base query goes here*/},
    "rescore": {
        "window_size": 100,
        "query": {
           "rescore_query": {
              "ltr": {
                  "model": {
                     "stored": "dummy"
                  },
                  "features": [{
                       "match": {
                           "title":
                        }
                   }
               ...
```

## The gritty details: behold the power of this fully functional learning to rank example!

Now beyond the TL; DR;

You can dig into a fully functioning example in the [demo](https://github.com/o19s/elasticsearch-learning-to-rank/tree/master/demo) directory of the project. It’s a canned example, using hand-created judgments of movies from TMDB. I use an Elasticsearch index with TMDB to execute queries corresponding to features, augment a judgment file with the relevance scores of those queries/features, and train a Ranklib model at the command line. I store the model in Elasticsearch, and provide a script to search using the model.

Don’t be fooled by the simplicity of this example. The reality of a real learning to rank solution is a tremendous amount of work, including studying users, processing analytics, data engineering, and feature engineering. I say that to not dissuade you, because the payoff can be worth it, just know what you’re getting into. Smaller organizations might still do better with the ROI of hand-tuned results.

### Training and loading the learning to rank model

Let’s start with the hand-created, minimal judgment list I’ve provided to show how our example trains a model.

Ranklib judgment lists come in a fairly standard format. The first column contains the judgment (0-4) for a document. The next column a query id, such as “qid:1.” The subsequent columns contain the values of the features associated with that query-document pair. On the left-hand side is the 1-based index of the feature. To the right of that number is the value for the feature. The example in the Ranklib README is:

```js
3 qid:1 1:1 2:1 3:0 4:0.2 5:0 # 1A
2 qid:1 1:0 2:0 3:1 4:0.1 5:1 # 1B
1 qid:1 1:0 2:1 3:0 4:0.4 5:0 # 1C
1 qid:1 1:0 2:0 3:1 4:0.3 5:0 # 1D
1 qid:2 1:0 2:0 3:1 4:0.2 5:0 # 2A
```

Notice also the comment (`# 1A` etc). That comment is the document identifier for this judgement. The document identifier isn’t needed by Ranklib, but it’s fairly handy to human readers. As we’ll see it’s useful for us as well when we gather features via Elasticsearch queries.

Our example starts with a minimal version of the above file (seen [here](https://github.com/o19s/elasticsearch-learning-to-rank/blob/master/demo/sample_judgments.txt)). We need to start with a trimmed-down version of the judgement file that simply has a grade, query id, and document id tuple. Like so:

```js
4    qid:1 #    7555
3    qid:1 #    1370
3    qid:1 #    1369
3    qid:1 #    1368
0    qid:1 #    136278
...
```

As above, we provide the Elasticsearch `_id` for the graded document as the comment on each line.

We need to enhance this a bit further. We must map each query id (qid:1) to an actual keyword query (“Rambo”) so we can use the keyword to generate feature values. We provide this mapping in the header which the example code will pull out:

```js
# Add your keyword strings below, the feature script will
# Use them to populate your query templates
#
# qid:1: rambo
# qid:2: rocky
# qid:3: bullwinkle
#
# https://sourceforge.net/p/lemur/wiki/RankLib%20File%20Format/
#
#
4    qid:1 #    7555
3    qid:1 #    1370
3    qid:1 #    1369
3    qid:1 #    1368
0    qid:1 #    136278...
```

To help clear up confusion, I’m going to start talking about ranklib “queries” (the `qid:1` etc) as “keywords” to differentiate from the Elasticsearch Query DSL “queries” which are Elasticsearch-specific constructs used to generate feature values.

What’s above isn’t a complete Ranklib judgement list. It’s just a minimal sample of relevance grades for given documents for a given keyword search. To be a fully-fledged training set, it needs to include the feature values shown above, the `1:0 2:1 …` included after each line in the first judgement list shown.

To generate those feature values, we also need to have proposed features that might correspond to relevance for movies. These, as we said, are Elasticsearch queries. The scores for these Elasticseach queries will finish filling out the judgement list above. In the example above, we do this using a jinja template corresponding to each feature number. For example the file [1.json.jinja](https://github.com/o19s/elasticsearch-learning-to-rank/blob/master/demo/1.json.jinja) is the following Query DSL query:

```js
{
   "query": {
       "match": {
          "title": "{{ keywords }}"
       }
   }
}
```

In other words, we’ve decided that feature 1 for our movie search system ought to be the TF\*IDF relevance score for the user’s keywords when matched against the title field. There’s also [2.jinja.json](https://github.com/o19s/elasticsearch-learning-to-rank/blob/master/demo/2.json.jinja) which performs a more complex search across multiple text fields:

```js
{
   "query": {
       "multi_match": {
          "query": "{{ keywords }}",
          "type": "cross_fields",
          "fields": ["overview", "genres.name", "title", "tagline",
 "belongs_to_collection.name", "cast.name", "directors.name"],
          "tie_breaker": 1.0
       }
   }
}
```

Part of the fun of learning to rank is hypothesizing what features might correlate with relevance. In the example, you can change features 1 and 2 to any Elasticsearch query. You can also experiment by adding additional features 3 through however many. There’s problems with too many features, as you’ll want to get enough representative training samples that cover all reasonable feature values. We’ll discuss more about training and testing learning to rank models in a future blog post.

With these two ingredients, the minimal judgment list and a set of proposed Query DSL queries/features, we need to generate a fully-fleshed out judgement list for Ranklib and load the Ranklib generated model into Elasticsearch to be used. This means:

1. Getting relevance scores for features for each keyword/document pair. Aka issuing queries to Elasticsearch to log relevance scores.
2. Outputting a full judgment file not only with grades and keyword query ids, but also with feature values from step 1 (1:
3. Running Ranklib to train the model
4. Loading the model into Elasticsearch for use at search time

The code to do this is all bundled up in [train.py](https://github.com/o19s/elasticsearch-learning-to-rank/blob/master/demo/train.py) which I encourage you to take apart. To run this, you’ll need

- [RankLib.jar](https://sourceforge.net/projects/lemur/files/lemur/RankLib-2.6/) downloaded to the scripts folder
- Python packages elasticsearch / jinja2 installed (there’s a Python requirements.txt if you’re familiar)

Then you can just run:

```js
python train.py
```

This one script runs through all the steps mentioned above. To walk you through the code:

First we load the minimal judgment list with just our document, keyword query id, grade tuples, with search keywords specified in the file’s header:

```js
judgements = judgmentsByQid(judgmentsFromFile(filename='sample_judgements.txt'))
```

We then issue bulk Elasticsearch queries to log features for each judgment (augmenting the passed in judgements).

```js
kwDocFeatures(es, index='tmdb', searchType='movie', judgements=judgements)
```

The function `kwDocFeatures` finds 1.json.jinja through N.json.jinja (the features/queries), and strategically batches Elasticsearch queries up to get a relevance score for each keyword/document tuple using Elasticsearch’s bulk search ([\_msearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-multi-search.html)) API. The code is tedious, you can see it [here](https://github.com/o19s/elasticsearch-learning-to-rank/blob/master/demo/features.py#L23).

Once we have the fully fleshed-out features, we then output the full training set (judgements plus features) into a new file (sample\_judgements\_wfeatures.txt):

```js
buildFeaturesJudgmentsFile(judgements, filename='sample_judgements_wfeatures.txt')
```

The output will correspond to a fully fleshed-out Ranklib judgement list, ala:

```js
3    qid:1    1:9.476478    2:25.821222 # 1370
3    qid:1    1:6.822593    2:23.463709 # 1369
```

Where feature 1 is the TF\*IDF score of “Rambo” searched on the title (1.json.jinja); feature 2 is the TF\*IDF score of the more complex search (2.json.jinja).

Next we train! This line runs Ranklib.jar via the command line using this saved file as judgement data

```js
trainModel(judgmentsWithFeaturesFile='sample_judgements_wfeatures.txt', modelOutput='model.txt')
```

As you can see below, this just basically runs `java -jar Ranklib.jar` training a [LambdaMART model](https://www.microsoft.com/en-us/research/publication/from-ranknet-to-lambdarank-to-lambdamart-an-overview/):

```js
def trainModel(judgmentsWithFeaturesFile, modelOutput):
    # java -jar RankLib-2.6.jar -ranker 6 -train sample_judgements_wfeatures.txt -save model.txt
    cmd = "java -jar RankLib-2.6.jar -ranker 6 -train %s -save %s" %   (judgmentsWithFeaturesFile, modelOutput)
    print("Running %s" % cmd)
    os.system(cmd)
```

We then store the model into Elasticsearch using simple Elasticsearch commands:

```js
saveModel(es, scriptName='test', modelFname='model.txt')
```

Here `saveModel`, as seen [here](https://github.com/o19s/elasticsearch-learning-to-rank/blob/master/demo/train.py#L13) just reads the file contents and POSTs it to Elasticsearch as a ranklib script to be stored.

### Searching with the learning to rank model

Once you’re done training, you’re ready to issue a search! You can see an example in search.py; it’s pretty straightforward with a simple query inside. You can run `python search.py rambo`, which will search for “rambo” using the trained model, executing the following rescoring query:

```js
{
    "query": {
        "match": {
            "_all": "rambo"
        }
    },
    "rescore": {
    "window_size": 20,
        "query": {
            "rescore_query": {
                        "ltr": {
                    "model": {
                        "stored": "test"
                    },
                    "features": [{
                        "match": {
                            "title": "rambo"
                        }
                    }, {
                        "multi_match": {
                            "query": "rambo",
                            "type": "cross_fields",
                            "tie_breaker": 1.0,
                            "fields": ["overview", "genres.name", "title", "tagline", "belongs_to_collection.name", "cast.name", "directors.name"]
                        }
                    }]
                }
            }
        }
    }
}
```

Notice we’re only reranking the top 20 results here. We could use ltr query directly. Indeed, running the model directly works pretty well. Albeit it takes a few hundred milliseconds to run over the whole collection. For a larger collection it wouldn’t be feasible. In general, it’s best to rerank a top N results due to the performance cost of learning to rank models.

And that’s the working example. Of course this is just a dumb, canned example meant to get your juices flowing. Your particular problem likely has many more moving parts. The features you choose, how you log features, train your model, and implement a baseline ranking function depends quite a bit on your domain. Much of what we write about in [Relevant Search](http://manning.com/books/relevant-search) still applies. So I guess what we’re saying is uh still buy the book;).

## What’s next! And get in touch!

In future blog posts we’ll have much more to say about learning to rank, including:

- Basics: more about what learning to rank is exactly
- Applications: Using learning to rank for search, recommendation systems, personalization and beyond
- Models: What are the prevalant models? What considerations play in selecting a model?
- Considerations: What technical and non-technical considerations come into play with Learning to Rank?

If you think you’d like to discuss how your search application can benefit from learning to rank, please [get in touch](https://opensourceconnections.com/contact/). We’re also always on the hunt for collaborators or for more folks to beat up our work in real production systems. So give it a go and send us feedback!