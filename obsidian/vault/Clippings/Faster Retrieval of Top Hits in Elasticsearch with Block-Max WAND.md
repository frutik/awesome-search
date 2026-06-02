---
title: "Faster Retrieval of Top Hits in Elasticsearch with Block-Max WAND"
source: "https://www.elastic.co/blog/faster-retrieval-of-top-hits-in-elasticsearch-with-block-max-wand"
author:
  - "[[Adrien Grand]]"
published: 2019-02-05
created: 2026-06-02
description: "Block-max WAND is coming to Lucene 8.0 and Elasticsearch 7.0, and it's bringing serious performance boosts. Learn about this big change and how it impacts you...."
tags:
  - "clippings"
---
## Once upon a time...

At Berlin Buzzwords in 2012, Stefan Pohl came to present [MAXSCORE](https://dl.acm.org/citation.cfm?id=220057), an algorithm introduced by H. Turtle and J. Flood in 1995 which helps optimize the retrieval of top matches of a disjunction such as "elasticsearch OR kibana". The idea is quite simple: say that you want to collect the top 10 matches, that the maximum score for the term "elasticsearch" is 3.0 and the maximum score for the term "kibana" is 5.0. Then if at some point during document collection the 10th best score which has been seen so far gets greater than 3.0 then you don't need to visit documents that only contain "elasticsearch" anymore: a document that only contains "elasticsearch" will have a score of at most 3.0 and won't be competitive. As a consequence, from the time when the minimum competitive score gets greater than 3.0, it is enough to only visit documents that contain "kibana" and only check whether they contain "elasticsearch" as well to compute their score. This idea can easily be generalized to arbitrary numbers of terms by maintaining two sets: one set of terms that is used to find candidates, and another set of terms that are only used to compute scores. Documents that only match terms in the second set couldn't get a competitive score. As more documents are collected and the minimum score that allows a document to enter the list of the top 10 matches increases, the term from first set that has the lowest maximum score moves to the set of optional terms, which in-turn speeds up query execution since the query to find candidates becomes more selective.

But Stefan didn't only describe the algorithm. A couple days before the conference, he opened a [ticket](https://issues.apache.org/jira/browse/LUCENE-4100) against Lucene, where he shared a prototype that he had built. This contribution was exciting but also challenging to integrate because we would need a way to compute the maximum score for every term in the index. In particular, scores depend on index statistics such as document frequency (total number of documents that contain a given term), so adding more documents to an index also changes the maximum score of postings in existing segments. Stefan's prototype had worked around this issue by requiring a rewrite of the index, which meant this optimization would only work for static indexes in practice. This is a limitation that we weren't happy with, but addressing it would require a lot of work. Due to lack of capacity, this issue remained stalled for 5 years.

## The end of the tunnel

Five years is a long time and many changes occurred meanwhile. One in particular would be interesting for this optimization: Lucene switched from TF-IDF to BM25 as its default scoring model. This move is important for MAXSCORE because BM25 scores are naturally bounded, which allowed us to implement this optimization without recording maximum scores in the index yet. Of course this upper bound is not as good as if we computed the maximum score for each term over all documents, but it is good enough so that work could resume on this issue. And indeed after a couple hacks to allow collectors to tell queries about the minimum score that is required for a hit to be competitive, we were able to optimize collection of the top matches on dynamic indexes. With this change, disjunctions went between 40% and 13x faster when running Lucene's benchmark suite.

Actually, this new patch didn't implement MAXSCORE like Stefan's initial patch but WAND, an algorithm introduced by A. Broder and al in 2003. WAND stands for "Weak AND" and is a bit finer grained than MAXSCORE: instead of maintaining two sets of query clauses, WAND keeps a single set but assigns weights to each clause (the maximum score in that case) and leverages the fact that the sum of the weights must be greater than a certain number to not evaluate all matches on all terms. This is the same algorithm that Lucene and Elasticsearch already used for boolean queries whose "minimum\_should\_match" is greater than 1. The algorithm is just slightly simpler in the case of `minimum_should_match` since all weights are equal to 1.

But work didn't stop there. Even though this optimization gives accurate top hits, the fact that it skips some documents means that the total hit count would no longer be computed, which would be a breaking change. Also this optimization is based on the assumption that matching more clauses may only increase the score so it is defeated if some clauses trigger negative scores.

## Further improvements

We also knew that this could be further optimized: the score upper bounds that we were using were not as good as if we would take the maximum score of every term over all documents. Yet even if we computed the actual maximum score for every term, we didn't like the fact that having a single outlier that gets a very high score would increase the maximum score and make the optimization less efficient. Upon further digging we found a [2011 paper by S. Ding and T. Suel](http://engineering.nyu.edu/~suel/papers/bmw.pdf) that introduces block-max indexes and [block-max WAND](https://issues.apache.org/jira/browse/LUCENE-8135). The underlying idea of this paper is to split postings into fixed-size blocks and to [record the maximum impact score separately for each block](https://issues.apache.org/jira/browse/LUCENE-4198), which helps mitigate issues with outliers. The impact score is the contribution to the score of per-document statistics: term frequency (number of occurrences of a term in a document) and document length. Block-max WAND is a variant of WAND that leverages the fact that each block may have a different maximum score. Block-max indexes also help speed up term queries and conjunctions by skipping blocks whose sum of maximum scores is not competitive.

We implemented this idea with a slight modification: instead of recording impact scores in the index, we record pairs of term frequency and document length. Impact scores can easily be derived from these per-document statistics, and recording those rather than impact scores has two important benefits:

- It doesn't require that the ranking function is decomposable into a per-term contribution and a per-document contribution: the optimization works with all scoring functions that Lucene provides including TF-IDF, BM25 and divergence from randomness.
- Users can still switch to a different similarity at search time, as long as it encodes document length the same way, which was already a requirement before we introduced block-max indexes.

Recording impacts in the index and implementing block-max WAND made term queries between 3x and 7x faster, conjunctions between 3% and 7x faster and disjunctions between -8% (slightly slower) and 15x faster when running Lucene's benchmark suite. A subset of these queries are tracked on [Lucene's nightly benchmarks](http://people.apache.org/~mikemccand/lucenebench/), see for instance annotation CJ on [term queries](http://people.apache.org/~mikemccand/lucenebench/Term.html) and [disjunctions](http://people.apache.org/~mikemccand/lucenebench/OrHighMed.html). Other queries such as [phrases](http://people.apache.org/~mikemccand/lucenebench/Phrase.html) and constant-scoring queries like [prefix queries](http://people.apache.org/~mikemccand/lucenebench/Prefix3.html) got speedups too, but via a completely different mechanism.

## Practical implications for Lucene and Elasticsearch

Block-max WAND will be integrated into Lucene 8.0 and Elasticsearch 7.0.

Given the serious speedups that this optimization triggers, we decided that it was ok to do two breaking changes that would allow us to expose it as a first-class citizen:

- Scores may no longer be negative.
- The total hit count is no longer always accurate

Lucene still gives the option to get accurate hit counts, but this comes with a performance penalty given that it requires to collect all matches.

Furthermore the response format was changed to reflect the fact that hit counts are no longer always accurate. Instead of being a number, `hits.total` is now going to be an object that looks like this:

```
{
  "value": 1000,
  "relation": "gte" // can only be "eq" if equal of "gte" if \`value\` is a lower bound of the hit count
}
```

It is possible to tell Elasticsearch how many hits to count via the `track_total_hits` parameter. If the actual number of hits is less than this number then the response will return the accurate hit count, and otherwise the response will set the value of `track_total_hits` as a number of hits with "gte" as a "relation", meaning that the actual hit count is actually greater than or equal to this number. The lower the value to `track_total_hits`, the faster the query.

If you include aggregations in your search requests, then this optimization won't apply: Elasticsearch still needs to visit all matches to compute aggregations. It doesn't necessarily mean that this optimization is not useful to you. For instance say you have an e-commerce website that both returns products and displays facets about the whole set of matches. By running one request to compute top products and another one for facets, the UI could start displaying hits even if facets aren't available yet.

## Conclusion

It's not every day that you get to make things several times faster. This is probably one of the most exciting changes that made it to Lucene over the last years and we are very excited that it is soon going to be released to our users.

Download the 7.0.0 preview release, take these new features for a spin, and let us know what you think. Become an [Elastic Pioneer](https://www.elastic.co/blog/elastic-pioneer-program-7-0) and you’ll also have a chance to win some cool Elastic swag.