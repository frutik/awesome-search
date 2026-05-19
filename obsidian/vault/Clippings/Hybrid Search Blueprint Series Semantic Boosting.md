---
title: "Hybrid Search Blueprint Series: Semantic Boosting"
source: "https://medium.com/@MongoDB/hybrid-search-blueprint-series-semantic-boosting-83b0011e080d"
author:
  - "[[MongoDB]]"
published: 2026-05-14
created: 2026-05-19
description: "More"
tags:
  - "clippings"
---
> *This article was written by* [*Erik Hatcher*](https://www.linkedin.com/in/erikhatcher/)*.*

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*Q9TYaYfc3l_VYWNzRpHnVQ.png)

This is the third and final article of this hybrid search series. First, we [surveyed the (hybrid) search landscape](https://medium.com/mongodb/survey-of-the-hybrid-search-landscape-a5477115f6a8), emphasizing that “hybrid search” isn’t a specific technique but rather the broader art and science of blending results from multiple search strategies designed to return results better than each search method on its own. In the second article, we dove into two classic hybrid search techniques, [Reciprocal Rank Fusion (RRF) and Relative Score Fusion (RSF)](https://medium.com/mongodb/reciprocal-rank-fusion-and-relative-score-fusion-classic-hybrid-search-techniques-3bf91008b81d). In this article, we present a different technique we’ve named Semantic Boosting.

[Semantic boosting](https://www.mongodb.com/docs/atlas/atlas-search/tutorial/hybrid-search/?utm_campaign=devrel&utm_source=third-party-content&utm_medium=cta&utm_content=semantic_boosting&utm_term=erik.hatcher#semantic-boosting) is a two-shot retrieval approach that leverages the conceptual understanding of vector search while retaining the robust feature set of a traditional full-text lexical search. In this workflow, a system first executes a vector query to retrieve a broad pool of candidates semantically similar to the user’s query. The application then extracts the unique document identifiers and their corresponding similarity scores from these top vector results. The vector scores are incorporated into a weighting factor to adjust their overall influence before being added as explicit match and boost clauses into a final full-text, lexical query.

During this final lexical search phase, the search engine looks for exact keyword matches but actively includes and boosts the scores of any documents that also matched the initial semantic search. Because the final output is generated entirely by lexical search, developers can seamlessly apply standard text search features to these hybrid results. This allows you to facet, highlight, and page through results efficiently. This semantic boosting technique essentially forces the lexical engine to include and boost semantically relevant documents higher, producing a single, highly refined result set.

As highlighted in [this video demonstration on the topic](https://www.youtube.com/watch?v=B6stg-A9xzw), the semantic boosting approach elegantly solves complex query intents. For example, a query like “keanu reeves teenage comedy” is notoriously difficult for a pure lexical search because it doesn’t understand the abstract concept of “teenage comedy”. Conversely, a pure vector search might grasp the theme perfectly but miss the strict keyword relevance of the actor’s name.

We’ll now explore semantic boosting with a concrete example.

## Setup

The example presented here uses the sample `embedded_movies` collection, which already has the plot field pre-embedded in the `plot_embedding_voyage_3_large` field using the `voyage-3-large` model. This gets us up and running quickly without having to embed the documents, only the query.

You’ll need a Voyage AI API key to embed queries. Go create an [API Key](https://docs.voyageai.com/docs/api-key-and-installation?utm_campaign=devrel&utm_source=third-party-content&utm_medium=cta&utm_content=semantic_boosting&utm_term=erik.hatcher); it’ll be plugged into the code below.

## First, semantic/vector search

Our vector search index definition:

```c
{
  "fields": [
   {
     "type": "vector",
     "path": "plot_embedding_voyage_3_large",
     "numDimensions": 2048,
     "similarity": "dotProduct"
   }
 ]
}
```

Initially, a standard `$vectorSearch` query is executed, providing the most semantically similar documents. Only a small, reasonable number of documents are requested at this stage. If you’re paginating the results, the number displayed on the first page is a good starting point so that the initial page could consist entirely of those most semantically relevant documents if no lexical matches are better.

To query a vector index, the user’s query must first be embedded using the same (or compatible) model. Using Voyage AI’s API, a function is defined to embed a query string:

```c
from voyageai import Client

api_key = "<VOYAGE_API_KEY>"
vo = Client(api_key=api_key)

def embed_query(text):
   response = vo.embed([text], model="voyage-4-large", input_type="query",
        output_dimension=2048)
   return response.embeddings[0]
```

At query time, the query (`q`) is embedded, and a `$vectorSearch` pipeline is executed, returning only `_id` and the vector similarity `score` for each document:

```c
query_vector = embed_query(q)
vector_pipeline = [{
   "$vectorSearch": {
   "queryVector": query_vector,
   "index": "vector_index",
   "path": "plot_embedding_voyage_3_large",
   "numCandidates": 150,
   "limit": 10
   }
 },
 { "$project": { "_id": 1 }},
 { "$addFields": {"score": {"$meta": "vectorSearchScore"} }}
]

vector_results = list(collection.aggregate(vector_pipeline))
```

## Boosting the vector/semantic results

For each vector result, a corresponding lexical `$search` operator is built that matches the documents `_id` with an additional scoring factor based on the vector similarity `score`. Here’s how that works:

```c
vector_boost_clauses = []
for result in vector_results:
 vector_boost_clauses.append(
  {
    "equals": {
    "path": "_id",
    "value": result["_id"],
    "score": { "boost": { "value": result["score"] * 10 } }
   }
  }
 )
```

These `vector_boost_clauses` will be added to the final `$search`, where each of those documents is boosted by a function of the vector score. In this case, multiplying each vector score by 10 (an arbitrary decision here).

This score boosting factor is key to making vector matches fold into lexical matches appropriately for your data and queries, and will require a bit of experimentation and measuring across a variety of queries.

## Searching lexically and boosting semantically

Our `$search` index definition dynamically indexes all supported field types, with one exception. The `genres` field is defined as a `token` type, so it can be faceted. All of the movie content is in English, so to avoid English stop words (such as “a”, “and”, “of”, “the”, etc), factoring into matching and highlighting the `lucene.english` analyzer is used rather than the default (`lucene.standard`) one. Using `lucene.english` here also adds stemming, so that different suffixes of the same base word are all matched; “search” will also match “searches” and “searching”, for example.

```c
{
 "mappings": {
   "dynamic": true,
   "fields": {
     "genres": { "type": "token" }
   }
 },
 "analyzer": "lucene.english"
}
```

Now our lexical clauses are constructed, incorporating the query (`q`) string where needed. Here, both `title` and `plot` fields are queried using the `text` operator, with `title` getting a 2.0 boost factor. These specific lexical clauses are a starting point for relevancy tuning. Lexical clauses deserve your attention, adjusting the fields, weights, and search operators to provide the best results for your application. See also: [MongoDB Search Score Breakdown](https://foojay.io/today/mongodb-search-score-breakdown/)

```c
lexical_clauses = [
 {
   "text": {
   "query": q,
   "path": ["title"],
   "score": { "boost": { "value": 2 } }
  }
 },
 {
   "text": {
     "query": q,
     "path": ["plot"]
   }
 } 
]
```

The final results incorporating both the lexical clauses and the vector boost clauses, as well as keyword highlighting and genre facets, come together in this `$search` pipeline:

```c
should_clauses = lexical_clauses
should_clauses.extend(vector_boost_clauses)

search_pipeline = [{
 "$search": {
   "index": "search_index",
   "scoreDetails": True,
   "facet": {
     "operator": {
       "compound": {
         "should": should_clauses
     } 
   },
   "facets": {
     "genres": {
       "type": "string",
       "path": "genres"
     }
   }
 },
 "highlight": {
   "path": ["title","plot"]
   }
  }
 },
 { "$project": { "title": 1, "genres": 1, "plot": 1}},
 { "$addFields": {
     "score": {"$meta": "searchScore"},
     "scoreDetails": {"$meta": "searchScoreDetails"},
     "highlights": {"$meta": "searchHighlights"}
   }
 },
 { "$limit": 10 },
 {
   "$facet": {
   "docs": [
   ],
   "meta": [
     {"$replaceWith": "$$SEARCH_META"},
     {"$limit": 1}
    ]
  }
 },
 {
   "$set": {
     "meta": {
       "$arrayElemAt": ["$meta", 0]
     }
   }
 } 
]
```

There’s a fair bit going on in that pipeline, so let’s break it down:

- `$search` is querying with a `compound.should` array of clauses. If any of those clauses match, the document is a match. If the document matches one of the vector results, the boosted value is added to any lexical match scores.
- The overarching `compund` operator is wrapped within `facet` so that `genres` facets are generated.
- Highlighting is enabled on both `plot` and `title`. Matching query terms will be annotated in the projected `highlights` field.
- Score and score details are both projected here for developer diagnosis. These details aren’t meant for end-users. Score details, in particular, should be turned off in production environments, as generating those will affect search performance.
- The `$facet` stage (yes, this is overloaded terminology and unrelated to search facets) is used to pack all search results into a single output document, so that the search facets are returned alongside the matching documents.
- The final `$set` un-arrays the (single-item array) `$meta` structure that contains facets, making it simpler for a client to navigate.

## Robust results

q = “musical sibling gets out of jail and helps save an orphanage”

Search results with highlighting

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*AZ86ni-Kg1tL_nDv3kufMQ.png)

Facets

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*7GwJoys2NvDD80lsz54RXw.png)

## Signals for search

Using results from one search to match and boost results in a final pass search is not a novel technique. Many search-powered applications, well before vector search was introduced, have boosted documents based on feedback from external “signals”. The term “signal” here refers to any factors that can be associated with the content documents, such as clicks, favorites, query-to-document associations, and so on. Particularly potent in e-commerce applications, user queries will be logged, along with other user behaviors, such as clicking on a product, adding a product to the cart, or purchasing a product. Leveraging signals, search results evolve by doing exactly the same process as described here. Whether the boosts come from semantic/vector queries or from machine-learned signal feedback, it’s the same technique: using the query and its context, such as users device type, time of day, users preferences, etc., to pull in matching, boosting, and other useful tweaks to the final search phase.

What we’ve done here is a special case of signal incorporation, where the signals are semantic matches.

## Summary

Regardless of the hybrid search technique, be it this [semantic boosting](https://www.mongodb.com/docs/atlas/atlas-search/tutorial/hybrid-search/?utm_campaign=devrel&utm_source=third-party-content&utm_medium=cta&utm_content=semantic_boosting&utm_term=erik.hatcher#semantic-boosting) one, `$rankFusion`, or `$scoreFusion`, relevancy tuning is warranted.

- Search index definition and lexical clauses deserve deep attention to detail

Semantic boosting bridges this gap through the following workflow:

- Initial vector search: The application first executes a `$vectorSearch` to retrieve an initial pool of conceptually relevant documents (e.g., the top 20 results).
- Score extraction and weighting: The application extracts the unique document IDs and their vector similarity scores, often applying a weighting multiplier to determine how heavily the semantic score should influence the final outcome.
- Boosted lexical search: These weighted clauses are dynamically injected into a final `$search` pipeline as explicit boost clauses — typically appended inside a compound should array.

The primary advantage of this technique is that the final output is generated entirely by the lexical search engine. Because of this, developers can seamlessly apply standard full-text features — such as pagination, faceting, and highlighting — to hybrid results. Ultimately, semantic boosting grants developers maximum flexibility to manually manipulate and fine-tune traditional relevance models while still taking full advantage of modern semantic matching.