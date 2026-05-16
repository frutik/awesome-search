---
title: "Multilingual embedding model: hybrid search reranking"
source: "https://www.elastic.co/search-labs/blog/multilingual-embedding-model-hybrid-search-reranking"
author:
  - "[[Quynh Nguyen]]"
published: 2025-10-30
created: 2026-05-15
description: "Learn how to improve the relevancy of E5 multilingual embedding model search results using Cohere's reranker and hybrid search in Elasticsearch."
tags:
  - "clippings"
---
From vector search to powerful REST APIs, Elasticsearch offers developers the most extensive search toolkit. Dive into our sample notebooks in the [Elasticsearch Labs repo](https://github.com/elastic/elasticsearch-labs?tab=readme-ov-file) to try something new. You can also start your [free trial](https://cloud.elastic.co/registration) or run [Elasticsearch locally](https://github.com/elastic/start-local) today.

## Introduction

In the [last part of this series](https://www.elastic.co/search-labs/blog/multilingual-embedding-model-deployment-elasticsearch), we walked through deploying Elastic's pre-trained E5 model (as well as other multilingual text embedding models from Hugging Face) and dived into generating dense vector [embeddings](https://www.elastic.co/what-is/vector-embedding) from your text data using [Elasticsearch](https://elastic.co/elasticsearch) and [Kibana](https://elastic.co/kibana). In this blog, we will examine the results of these embeddings and highlight the significant advantages of leveraging a multilingual model.

Now that we have our index `coco_multilingual`, performing the search will give us documents in multiple languages, with the "en" field for us to reference:

```json
# GET coco_multilingual/_search
    {
       "_index": "coco_multilingual",
       "_id": "WAiXQJYBgf6odR9bLohZ",
       "_score": 1,
       "_source": {
         "description": "Ein Parkmeßgerät auf einer Straße mit Autos",
         "en": "A row of parked cars sitting next to parking meters.",
         "language": "de",
         "vector_description": {...}
       }
     },
     . . .
```

## Performing a search in English

Let's try to perform the search in English and see how well it does:

```json
GET coco_multi/_search
{
"size": 10,
"_source": [
  "description", "language", "en"
],
"knn": {
  "field": "vector_description.predicted_value",
  "k": 10,
  "num_candidates": 100,
  "query_vector_builder": {
    "text_embedding": {
      "model_id": ".multilingual-e5-small_linux-x86_64_search",
      "model_text": "query: kitty"
    }
  }
}
}
```

```json
{
       "_index": "coco_multi",
       "_id": "JQiXQJYBgf6odR9b6Yz0",
       "_score": 0.9334303,
       "_source": {
         "description": "Eine Katze, die in einem kleinen, gepackten Koffer sitzt.",
         "en": "A brown and white cat is in a suitcase.",
         "language": "de"
       }
     },
      {
       "_index": "coco_multi",
       "_id": "3AiXQJYBgf6odR9bFod6",
       "_score": 0.9281012,
       "_source": {
         "description": "Una bambina che tiene un gattino vicino a una recinzione blu.",
         "en": "A little girl holding a kitten next to a blue fence.",
         "language": "it"
       }
     },
     . . .
```

Here, even though the query looks deceptively simple, we are searching for the numerical embeddings of the word 'kitty' across all documents in all languages underneath the hood. And because we are performing [vector search](https://www.elastic.co/search-labs/blog/introduction-to-vector-search "Learn more about vector search"), we can semantically search for all words that might be related to 'kitty': "cat", "kitten", "feline", "gatto" (Italian), "mèo" (Vietnamese), 고양이 (Korean), 猫 (Chinese), etc. As a result, even if my query is in English, we can search for content in all other languages too. For example, searching for a kitty l `ying on something` gives back documents in Italian, Dutch, or Vietnamese, too. Talk about efficiency!

## Performing a search for content in other languages

```json
GET coco_multi/_search
{  
 "size": 100,
 "_source": [
   "description", "language", "en"
 ],
 "knn": {
   "field": "vector_description.predicted_value",
   "k": 50,
   "num_candidates": 1000,
   "query_vector_builder": {
     "text_embedding": {
       "model_id": ".multilingual-e5-small_linux-x86_64_search",
       "model_text": "query: kitty lying on something"
     }
   }
 }
}
```

```json
{
 "description": "A black kitten lays on her side beside remote controls.",
 "en": "A black kitten lays on her side beside remote controls.",
 "language": "en"
},
{
 "description": "un gattino sdraiato su un letto accanto ad alcuni telefoni ",
 "en": "A black kitten lays on her side beside remote controls.",
 "language": "it"
},
{
 "description": "eine Katze legt sich auf ein ausgestopftes Tier",
 "en": "a cat lays down on a stuffed animal",
 "language": "de"
},
{
 "description": "Một chú mèo con màu đen nằm nghiêng bên cạnh điều khiển từ xa.",
 "en": "A black kitten lays on her side beside remote controls.",
 "language": "vi"
}
. . .
```

Similarly, performing a keyword search for "cat" in Korean ("고양이") will also give back meaningful results. What's spectacular here is that we don't even have any documents in Korean in this index!

```json
GET coco_multi/_search
{
 "size": 100,
 "_source": [
   "description", "language", "en"
 ],
 "knn": {
   "field": "vector_description.predicted_value",
   "k": 50,
   "num_candidates": 1000,
   "query_vector_builder": {
     "text_embedding": {
       "model_id": ".multilingual-e5-small_linux-x86_64_search",
       "model_text": "query: 고양이"
     }
   }
 }
}
```

```json
{
      {
        "description": "eine Katze legt sich auf ein ausgestopftes Tier",
        "en": "a cat lays down on a stuffed animal",
        "language": "de"
      }
    },
    {
      {
        "description": "Một con chó và con mèo đang ngủ với nhau trên một chiếc ghế dài màu cam.",
        "en": "A dog and cat lying  together on an orange couch. ",
        "language": "vi"
      }
    },
```

This works because the embedding model represents meaning in a shared semantic space, allowing retrieval of relevant images even with a query in a different language than the indexed captions.

## Increasing relevant search results with hybrid search and reranking

We are happy that the relevant results showed up as expected. But, in the real world, say in [ecommerce](https://www.elastic.co/enterprise-search/ecommerce "Fast & scalable e-commerce search") or in [RAG](https://www.elastic.co/search-labs/blog/retrieval-augmented-generation-rag "Learn more about retrieval augmented generation (RAG)") applications that need to narrow down to the top 5-10 most applicable results, we can use a rerank model to prioritize the most relevant results.

Here, performing a query that asks "what color is the cat?" in Vietnamese will yield a lot of results, but the top 1 or 2 might not be the most relevant.

```json
GET coco_multi/_search
{
 "size": 20,
 "_source": [
   "description",
   "language",
   "en"
 ],
 "knn": {
   "field": "vector_description.predicted_value",
   "k": 20,
   "num_candidates": 1000,
   "query_vector_builder": {
     "text_embedding": {
       "model_id": ".multilingual-e5-small_linux-x86_64_search",
       "model_text": "query: con mèo màu gì?"
     }
   }
 }
}
```

The results all mention cat, or some form of color:

![](https://www.elastic.co/search-labs/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fme0ej585%2Fsearch-labs-import-testing%2F33e1e887dbbdd1066cfedc7375f5e3b46538529e-859x847.png&w=3840&q=75)

So let's improve that! Let's integrate [Cohere](https://cohere.com/blog/rerank-3pt5) 's multilingual rerank model to improve the reasoning corresponding to our question.

```json
PUT _inference/rerank/cohere_rerank
{
 "service": "cohere",
 "service_settings": {
   "api_key": "your_api_key",
   "model_id": "rerank-v3.5"
 },
 "task_settings": {
   "top_n": 10,
   "return_documents": true
 }
}

GET coco_multi/_search
{
"size": 10,
"_source": [
  "description",
  "language",
  "en"
],
"retriever": {
  "text_similarity_reranker": {
    "retriever": {
      "rrf": {
        "retrievers": [
          {
            "knn": {
              "field": "vector_description.predicted_value",
              "k": 50,
              "num_candidates": 100,
              "query_vector_builder": {
                "text_embedding": {
                  "model_id": ".multilingual-e5-small_linux-x86_64_search",
                  "model_text": "query: con mèo màu gì?" // English: What color is the cat?
                }
              }
            }
          }
        ],
        "rank_window_size": 100,
        "rank_constant": 0
      }
    },
    "field": "description",
    "inference_id": "cohere_rerank",
    "inference_text": "con mèo màu gì?"
  }
}
}
```

```json
{
      "_index": "coco_multi",
      "_id": "rQiYQJYBgf6odR9bBYyH",
      "_score": 1.5501487,
      "_source": {
        "description": "Hai cái điện thoại được đặt trên một cái chăn cạnh một con mèo con màu đen.",
        "en": "A black kitten lays on her side beside remote controls.",
        "language": "vi"
      }
    },
    {
      "_index": "coco_multi",
      "_id": "swiXQJYBgf6odR9b04uf",
      "_score": 1.5427427,
      "_source": {
        "description": "Một con mèo sọc nâu nhìn vào máy quay.", // Real translation: A brown striped cat looks at the camera 
        "en": "This cat is sitting on a porch near a tire.",
        "language": "vi"
      }
    },
```

Now, with the top results, our application can confidently answer that the kitten's color is black or brown with stripes. What's even more interesting here is that our vector search actually caught an omission in the English caption in the original dataset. It's able to find the brown striped cat even though the reference English translation missed that detail. This is the power of vector search.

## Conclusion

In this blog, we have walked through the utility of a multilingual embedding model, and how to leverage Elasticsearch to integrate the models to generate embeddings, and to effectively improve relevance and accuracy with a [hybrid search](https://www.elastic.co/search-labs/blog/hybrid-search-elasticsearch "Learn more about hybrid search") and reranker. You can [create a Cloud cluster](https://cloud.elastic.co/registration?onboarding_token=vectorsearch&cta=cloud-registration&tech=trial&plcmt=article%20content&pg=search-labs) of your own to try [multilingual semantic search using our out-of-the-box E5 model](https://www.elastic.co/docs/explore-analyze/machine-learning/nlp/ml-nlp-e5) on the language and dataset of your choice.