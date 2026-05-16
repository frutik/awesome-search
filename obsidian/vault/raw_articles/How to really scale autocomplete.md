---
title: "How to really scale autocomplete"
source: "https://bonsai.io/blog/how-to-really-scale-autocomplete/"
author:
published: 2025-07-18
created: 2026-05-15
description: "A straightforward guide to scaling an autocomplete solution in Elasticsearch or OpenSearch."
tags:
  - "clippings"
---
Last time, in Part 1, ["How To Really Do Autocomplete"](https://bonsai.io/blog/how-to-really-do-autocomplete), we covered a straightforward technique to build a quality autocomplete solution in pure Elasticsearch or OpenSearch. We used the significant\_terms aggregation to provide diverse and helpful suggestions of words and phrases to help guide the user while they are typing a query. In this part, we'll **scale it up** to 6 million documents, and get 500 autocompletes-per-second at 30ms latency on a cluster that most teams probably run already.

## Our adventure continues

While Part 1 worked well and offered good suggestions for small datasets, it didn't scale for phrases the way I had it configured. The sweet spot for significant\_phrases from Part 1 was for tens of thousands of docs. It turns out that as you add more and more documents and increase the variance and cardinality of the vocabulary, aggregating significant\_terms on shingles gets really slow.

I found this out because I was working on load testing a vector search cluster, and I had finished my goals for the week. I had [millions of Wikipedia documents and vectors](https://huggingface.co/datasets/Cohere/wikipedia-22-12-en-embeddings) loaded into a nice set of data nodes. I wanted to get an index time comparison for lexical ingestion without vectors anyway, so I went side questing for an afternoon and said, "let's scale autocomplete, baby!"

## Fall from grace

Sad trombone. It was slow. Not just laggy - but failures everywhere. I tried warming the index but didn't get very far. CPU started screaming and almost all the queries were timing out. However when it did run, the word suggestions were amazing.

Shortly after, I singled out `significant_phrases` aggregation as the culprit. Just plain unusable when doing an agg and include pattern at that cardinality of millions of docs. Shingles really explodes the set, and sadly it must go.

## Rebuild

I started with the completions analyzer for both titles and text. An out-of-the-box `search-as-you-type` field on titles works well and is really fast. It's still using edge\_ngrams and shingles behind the scenes, but when isolating on titles and coupled with max shingle size of 3 it performed surprisingly well.

The next to go was the `significant_phrases` aggregations. Our replacement is now just a regular `terms` agg. This works great! It's fast and honestly much better in terms of quality.

Here's how it works: we perform a match of the prefix in the completions field, and that narrows the result set down to thousands of documents from millions. With this narrow scope, the significant\_words and phrase terms aggregations are very fast, and the quality is laudable.

```json
{
  ...
  "aggs": {
    "significant_words": {
      "significant_terms": {
        "field":  "suggest_word_all",
        "min_doc_count": 1,
        "include": q+'.*'
      }
    },
    "significant_phrases": {
      "terms": {
        "field":  "suggest_phrase",
        "order":  { "_count": "desc" },
        "include": q+'.*',
        "min_doc_count": 1
      }
    }
  },
  ...
}
```

## Load Testing

To ensure we're actually able to handle load, we need to test. I use the following methodology: source a list of thousands of prefixes, and test by running those as our prefix queries at high load.

With the prefixes, we can run the load test. I used [Locust](https://locust.io/), which is really easy to setup and use with `uvx`.

### Results

#### Request Summary (requests/second)

| Name | req/s | fails | Avg | Min | Max | Med |
| --- | --- | --- | --- | --- | --- | --- |
| autocomplete | 416.02 | 0 | 25 | 17 | 275 | 25 |

#### Response Time Percentiles (milliseconds)

| Name | 50% | 75% | 95% | 99% |
| --- | --- | --- | --- | --- |
| autocomplete | 23 | 26 | 31 | 45 |

We can see a clear sub-50ms query time at p99, running ~450qps once the concurrency rampup finishes and the index is warm. This is very fast, and very production ready.

## Implementation Notes

Here are some important implementation specifics to keep it snappy:

- In most cases, you should use a separate index for autocomplete than your regular search.
- When the user is typing, don't send a request for autocomplete immediately - wait 25ms to 50ms for them to pause beforehand. This will save on requests and only suggest when the user briefly pauses to think.
- For your dataset, experiment with your match prefix query and what goes into the `completions` field.
- One area to watch is the `fielddata` property of the aggregation fields.

## Co-Occurrence Sugar

Once you've chosen a suggestion from autocomplete, drawn from a corpus of millions, there could be hundreds or thousands of results that match the selection. We can help improve discovery with some UX by showing narrow navigation paths using suggestions to help guide the user.

Some examples from the engine:

- **"elasticsearch"**: ['kibana', 'lucene', 'opensearch', 'solr', 'mongodb']
- **"large language model"**: ['chatgpt', 'gpt', 'openai', 'megatron', 'transformer']

We call this co-occurrence of terms. With a fully formed concept, co-occurrence shows which terms appear in the same passages as that concept.