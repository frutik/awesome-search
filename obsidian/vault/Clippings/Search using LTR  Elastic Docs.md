---
title: "Search using LTR | Elastic Docs"
source: "https://www.elastic.co/docs/solutions/search/ranking/learning-to-rank-search-usage"
author:
published:
created: 2026-06-13
description: "Once your LTR model is trained and deployed in Elasticsearch, there are two ways to use it with the search API to improve your search results: As a rescorer,..."
tags:
  - "clippings"
---
## Search using LTR

Serverless

Stack

> [!note] Note
> This feature was introduced in version 8.12.0 and is only available to certain subscription levels. For more information, refer to [Elastic self-managed subscriptions](https://www.elastic.co/subscriptions).

Once your LTR model is trained and deployed in Elasticsearch, there are two ways to use it with the [search API](https://www.elastic.co/docs/solutions/search/querying-for-search) to improve your search results:

1. **As a [rescorer](#learning-to-rank-rescorer)**
2. **As a [retriever](#learning-to-rank-retriever)**

## Learning To Rank as a rescorer

To use your LTR model as a [rescorer](https://www.elastic.co/docs/reference/elasticsearch/rest-apis/rescore-search-results) in the [search API](https://www.elastic.co/docs/solutions/search/querying-for-search), follow this example:

```json
GET my-index/_search
                    {
  "query": {
    "multi_match": {
      "fields": ["title", "content"],
      "query": "the quick brown fox"
    }
  },
  "rescore": {
    "learning_to_rank": {
      "model_id": "ltr-model",
      "params": {
        "query_text": "the quick brown fox"
      }
    },
    "window_size": 100
  }
}
```

1. First pass query providing documents to be rescored.
2. The unique identifier of the trained model uploaded to Elasticsearch.
3. Named parameters to be passed to the query templates used for feature.
4. The number of documents that should be examined by the rescorer on each shard.

## Learning To Rank as a retriever

Serverless

Stack9.1+

LTR models can also be used as a [retriever](https://www.elastic.co/docs/solutions/search/retrievers-overview) in the search pipeline. You can implement this with a [rescorer retriever](https://www.elastic.co/docs/reference/elasticsearch/rest-apis/retrievers/rescorer-retriever) as shown in the following example:

```json
GET my-index/_search
                    {
  "retriever": {
    "rescorer": {
      "rescore": {
        "window_size": 100,
        "learning_to_rank": {
          "model_id": "ltr-model",
          "params": {
            "query_text": "the quick brown fox"
          }
        }
      },
      "retrievers": [
        {
          "standard": {
            "query": {
              "multi_match": {
                "fields": ["title", "content"],
                "query": "the quick brown fox"
              }
            }
          }
        }
      ]
    }
  }
}
```

1. First pass retrievers used to retrieve documents to be rescored
2. The unique identifier of the trained model uploaded to Elasticsearch.
3. Named parameters to be passed to the query templates used for feature extraction.
4. The number of documents that should be examined by the rescorer.

## Known limitations

### Rescore window size

Scores returned by LTR models are usually not comparable with the scores issued by the first pass query and can be lower than the non-rescored score. This can cause the non-rescored result document to be ranked higher than the rescored document. To prevent this, the `window_size` parameter is mandatory for LTR rescorers and should be greater than or equal to `from + size`.

When exposing pagination to users, `window_size` should remain constant as each page is progressed by passing different `from` values. Changing the `window_size` can alter the top hits causing results to confusingly shift as the user steps through pages.