---
title: "Sparse embeddings: Dense vs. sparse vector & usage with ML models"
source: "https://www.elastic.co/search-labs/blog/sparse-vector-embedding"
author:
  - "[[Dai Sugimori]]"
published: 2025-02-18
created: 2026-05-16
description: "Learn about sparse vector embeddings in Elasticsearch, how they differ from dense vectors, and how to implement semantic search with them."
tags:
  - "clippings"
---
From vector search to powerful REST APIs, Elasticsearch offers developers the most extensive search toolkit. Dive into our sample notebooks in the [Elasticsearch Labs repo](https://github.com/elastic/elasticsearch-labs?tab=readme-ov-file) to try something new. You can also start your [free trial](https://cloud.elastic.co/registration) or run [Elasticsearch locally](https://github.com/elastic/start-local) today.

[Elasticsearch](https://elastic.co/elasticsearch) provides a [semantic search](https://www.elastic.co/search-labs/blog/introduction-to-vector-search "Learn more about vector search") feature that allows users to query in natural language and retrieve relevant information. To achieve this, target documents and queries must first be transformed into vector representations through an embedding process, which is handled by a trained Machine Learning (ML) model running either inside or outside Elasticsearch.

Since choosing a good machine learning model is not easy for most search users, Elastic introduced a house-made ML model called ELSER ([Elastic Learned Sparse EncodeR](https://www.elastic.co/docs/explore-analyze/machine-learning/nlp/ml-nlp-elser)). It is bundled with Elasticsearch, so they can use it out-of-the-box under a platinum license (refer to the [subscription page](https://www.elastic.co/subscriptions)). It has been a widely used model for implementing semantic search. Unlike many other models that generate "dense vectors," ELSER produces "sparse vectors," which represent [embeddings](https://www.elastic.co/what-is/vector-embedding) differently.

Although sparse vector models work in many use cases, only dense vector models could be uploaded to Elasticsearch until Elasticsearch and Eland 8.16. However, starting from version 8.17, you can now upload sparse vector models as well using Eland’s [eland\_import\_hub\_model](https://www.elastic.co/guide/en/machine-learning/current/ml-nlp-import-model.html) CLI. This means you can generate sparse vector embeddings using models from Hugging Face, not just ELSER.

In this article, I’d like to recap what sparse vectors are compared to dense ones as well as introduce how to upload them from outside for use in Elasticsearch.

## What is a sparse vector?

What is the difference between dense and sparse vectors? Let's start with dense vectors, which are more commonly used for search today.

#### Dense vectors

When text is embedded as a dense vector, it looks like this:

```sh
[
  0.13586345314979553,
  -0.6291824579238892,
  0.32779985666275024,
  0.36690405011177063,
  ...
]
```

Key characteristics of dense vectors:

- The vector has a fixed dimension.
- Each element is a numeric value (float by default).
- Every element represents some feature, but their meanings are not easily interpretable by humans.
- Most elements have nonzero values.

The ML models, especially those based on transformers, will produce geometrically similar vectors if the meanings of the input text are similar. The similarity is calculated by some different functions such as cosine, l2\_norm, etc.

For example, if we embed the words "cat" and "kitten", their vectors would be close to each other in the vector space because they share similar semantic meaning. In contrast, the vector for "car" would be farther away, as it represents a completely different concept.

Elastic has many interesting articles about vector search. Refer to them if you are keen to learn more:

- [A quick introduction to vector search - Elasticsearch Labs](https://www.elastic.co/search-labs/blog/introduction-to-vector-search)
- [Navigating an Elastic vector database - Elasticsearch Labs](https://www.elastic.co/search-labs/blog/elastic-vector-database-practical-example)
- [Vector similarity techniques and scoring - Elasticsearch Labs](https://www.elastic.co/search-labs/blog/vector-similarity-techniques-and-scoring)

#### Sparse vectors

In contrast, sparse vectors have a different structure. Instead of assigning a value to every dimension, they mostly consist of zeros, with only a few nonzero values. A sparse vector representation looks like this:

{"f1":1.2,"f2":0.3,… }

Key characteristics of sparse vectors:

- Most values in the vector are zero.
- Instead of a fixed-length array, they are often stored as key-value pairs, where only nonzero values are recorded.
- The feature which has zero value never appears in the sparse vector representation.
- The representation is more interpretable, as each key (feature) often corresponds to a meaningful term or concept.

### BM25 and sparse vector representation

[BM25](https://www.elastic.co/search-labs/blog/lexical-and-semantic-search-with-elasticsearch), a well-known ranking function for lexical search, uses a sparse vector representation of text known as a **term vector**. In this representation, each term (known as token or word) in the document is assigned a weight based on its frequency and importance within the corpus (a set of documents). This approach allows efficient retrieval by matching query terms to document terms.

### Lexical search vs. semantic search

BM25 is an example of **lexical search**, where matching is based on exact terms found in the document. It relies on a sparse vector representation derived from the vocabulary of the corpus.

On the other hand, **semantic search** goes beyond exact term matching. It uses vector embeddings to capture the meaning of words and phrases, enabling retrieval of relevant documents even if they don't contain the exact query terms.

In addition, Elasticsearch can do more. You can combine these two searches in one query as a [hybrid search](https://www.elastic.co/search-labs/blog/hybrid-search-elasticsearch "Learn more about hybrid search"). Refer to the links below to learn more about it.

- [When hybrid search truly shines - Elasticsearch Labs](https://www.elastic.co/search-labs/blog/elasticsearch-hybrid-search)
- [Hybrid search with multiple embeddings: A fun and furry search for cats! - Elasticsearch Labs](https://www.elastic.co/search-labs/blog/hybrid-search-multiple-embeddings)
- [Hybrid Search: Combined Full-Text and kNN Results - Elasticsearch Labs](https://www.elastic.co/search-labs/tutorials/search-tutorial/vector-search/hybrid-search)
- [Hybrid Search: Combined Full-Text and ELSER Results - Elasticsearch Labs](https://www.elastic.co/search-labs/tutorials/search-tutorial/semantic-search/hybrid-search)
- [Tutorial: hybrid search with semantic\_text | Elasticsearch Guide | Elastic](https://www.elastic.co/guide/en/elasticsearch/reference/current/semantic-text-hybrid-search.html)

### Dense and sparse vectors in semantic search

Semantic search can leverage both dense and sparse vectors:

- **Dense vector models** (e.g., BERT-based models) encode semantic meaning into fixed-length vectors, enabling similarity search based on vector distances.
- **Sparse vector models** (e.g., ELSER) capture semantic meaning while preserving interpretability, often leveraging term-based weights.

With Elasticsearch 8.17, you can now upload and use both dense and sparse vector models, giving you more flexibility in implementing semantic search tailored to your needs.

## Why sparse vectors?

Sparse vectors offer several advantages in Elasticsearch, making them a powerful alternative to dense vectors in certain scenarios. For example, dense vector (knn) search requires the models to be learned with a good/enough corpus of the domain that users are working with. But it is not always easy to have such a model which is suitable for your use case, and fine-tuning the model is even harder for most users. In this case, the sparse vector models will help you. Let’s learn why.

### Good for zero-shot learning

Sparse vectors, especially those generated by models like ELSER, can generalize well to new domains without requiring extensive fine-tuning. Unlike dense vector models that often need domain-specific training, sparse vectors rely on term-based representations, making them more effective for **zero-shot** retrieval—where the model can handle queries it hasn’t explicitly been trained on.

### Resource efficiency

Sparse vectors are inherently more resource-efficient than dense vectors. Since they contain mostly zeros and only store nonzero values as key-value pairs, they require less memory and storage.

## Sparse vectors in Elasticsearch

Elasticsearch initially supported sparse vector search using the `rank_features` query. However, with recent advancements, sparse vector search is now natively available through the sparse\_vector query, providing better integration with Elasticsearch’s machine learning models.

### Integration with ML models

The `sparse_vector` query is designed to work seamlessly with trained models running on Elasticsearch ML nodes. This allows users to generate sparse vector embeddings dynamically and retrieve relevant documents using efficient similarity search.

### Leveraging Lucene’s inverted index

One of the key benefits of sparse vectors in Elasticsearch is that they **leverage Lucene’s inverted index** —the same core technology that powers Elasticsearch’s fast and scalable search.

- **Resource efficiency:** Since Lucene is optimized for term-based indexing, sparse vectors benefit from efficient storage and retrieval.
- **Maturity:** Elasticsearch has a well-established and highly optimized indexing system, making sparse vector search a natural fit within its architecture.

By utilizing Lucene’s indexing capabilities, Elasticsearch ensures that sparse vector search remains **fast, scalable, and resource-efficient**, making it a strong choice for real-world search applications.

## Implementing sparse embedding with a preferred model from Hugging Face

Starting from Elasticsearch 8.17, you can use any sparse vector model from Hugging Face as long as it employs a supported tokenization method. This allows greater flexibility in implementing **semantic search** with models tailored to your specific needs.

Elasticsearch currently supports the following tokenization methods for sparse and dense vector embeddings:

- **`bert`** – For BERT-style models
- **`deberta_v2`** – For DeBERTa v2 and v3-style models
- **`mpnet`** – For MPNet-style models
- **`roberta`** – For RoBERTa-style and BART-style models
- **`xlm_roberta`** – For XLM-RoBERTa-style models
- **`bert_ja`** – For BERT-style models trained specifically for Japanese

For a full list of supported tokenization methods, refer to the official documentation:[Elasticsearch Reference: PUT Trained Models](https://www.elastic.co/guide/en/elasticsearch/reference/current/put-trained-models.html)

If the tokenization of your model is available, you can select it even if it’s not for non-English languages! Below are some examples of available sparse models on Hugging Face:

- [naver/splade-v3-distilbert](https://huggingface.co/naver/splade-v3-distilbert)
- [hotchpotch/japanese-splade-v2](https://huggingface.co/hotchpotch/japanese-splade-v2)
- [aken12/splade-japanese-v3](https://huggingface.co/aken12/splade-japanese-v3)

### Steps to use a sparse vector model from Hugging Face

We already have [a good article](https://www.elastic.co/search-labs/blog/elasticsearch-sparse-vector-query) about sparse vector search with ELSER. Most of the steps are the same, but if you’d like to use the sparse embedding model from Hugging Face, you need to upload it to Elasticsearch beforehand with Eland.

Here is the step-by-step guide to use the external sparse model on Elasticsearch for semantic search.

**1\. Find a sparse vector model**

Browse Hugging Face ([huggingface.co](https://huggingface.co/)) for a **sparse embedding model** that fits your use case. Ensure that the model uses one of the supported tokenization methods listed above.

Let’s select the “ [naver/splade-v3-distilbert](https://huggingface.co/naver/splade-v3-distilbert) ” model as an example of the sparse embedding model.

Note: Elastic’s ELSER model is heavily inspired by Naver’s SPLADE model. Visit [their website](https://europe.naverlabs.com/research/machine-learning-for-robotics/splade-models/) to learn more about SPLADE.

**2\. Upload the model to Elasticsearch**

You need to install Eland, a Python client and toolkit for DataFrames and machine learning in Elasticsearch. Note that you need Eland 8.17.0 or later for uploading sparse vector models.

```
python -m pip install eland
```

Once it is installed on your computer, use **Eland’s CLI tool** (`eland_import_hub_model`) to import the model into Elasticsearch.

```sh
eland_import_hub_model \
--url "your.elasticsearch.host" \
--es-api-key "your_api_key" \
--hub-model-id naver/splade-v3-distilbert \
--task-type text_expansion \
--start
```

Alternatively, you can do the same [with Docker](https://www.elastic.co/guide/en/elasticsearch/client/eland/current/machine-learning.html#ml-nlp-pytorch-docker) if you don’t want to install Eland locally.

```sh
docker run -it --rm docker.elastic.co/eland/eland \
eland_import_hub_model \
--url "your.elasticsearch.host" \
--es-api-key "your_api_key" \
--hub-model-id naver/splade-v3-distilbert \
--task-type text_expansion \
--start
```

The key point here is that you need to set `text_expansion` as the task type for the sparse vector embeddings, unlike `text_embedding` for the dense vector embeddings. (JFYI, there is a [discussion](https://github.com/elastic/elasticsearch/issues/119576) about the task name.)

**3\. Define index mapping with `sparse_vector`**

Create an index that has a **`sparse_vector`** field.

```sh
PUT sparse-test
{
  "mappings": {
    "properties": {
      "content_embedding": { 
        "type": "sparse_vector" 
      },
      "content": { 
        "type": "text" 
      }
    }
  }
}
```

It should be noted that the [sparse\_vector](https://www.elastic.co/guide/en/elasticsearch/reference/current/sparse-vector.html) field type was formerly known as [rank\_features](https://www.elastic.co/guide/en/elasticsearch/reference/current/rank-features.html) field type. Although there is no functional difference between them, you should use sparse\_vector field type for the clarity of its usage.

Note: Elastic recently introduced a `semantic_text` field. It is super useful and easy-to-implement semantic search. Refer to [this article](https://www.elastic.co/search-labs/blog/semantic-search-simplified-semantic-text) for the details. You can use semantic\_text field for the same purpose, but to stay focused on the embedding part, let’s use sparse\_vector field for now.

**4\. Create ingest pipeline with [inference](https://www.elastic.co/docs/explore-analyze/elastic-inference) processor**

The text information needs to be embedded into the sparse vector before it is indexed. That can be done by the ingest pipeline with the inference processor.

Create the ingest pipeline with an inference processor which refers to the model you have uploaded before.

```sh
PUT _ingest/pipeline/sparse-test-pipeline
{
  "processors": [
    {
      "inference": {
        "model_id": "naver__splade-v3-distilbert",
        "input_output": [ 
          {
            "input_field": "content",
            "output_field": "content_embedding"
          }
        ]
      }
    }
  ]
}
```

**5\. Ingest the data with the pipeline**

Ingest text data into an index with the “sparse-test-pipeline” we created so that the content will be automatically embedded into the sparse vector representation.

```sh
POST sparse-test/_doc/1?pipeline=sparse-test-pipeline
{
  "content": "Elasticsearch provides a semantic search feature that allows users to query in natural language and retrieve relevant information."
}
```

Once it is done, let’s check how it is indexed.

```sh
GET sparse-test/_doc/1
```

It will return like this:

```sh
{
  "_index": "sparse-test",
  "_id": "1",
  "_source": {
    "content": "Elasticsearch provides a semantic search feature that allows users to query in natural language and retrieve relevant information.",
    "content_embedding": {
      "software": 3.2601595,
      "web": 2.0722878,
      "browser": 1.8972412,
      "platform": 1.6211865,
      "java": 1.5984035,
      "sql": 1.5119768,
      "engine": 1.4900811,
      ...
    },
    "model_id": "naver__splade-v3-distilbert"
  }
}
```

As you can see, the input text " *Elasticsearch provides a semantic search feature that allows users to query in natural language and retrieve relevant information.*" is embedded as:

```sh
{
  "software": 3.2601595,
  "web": 2.0722878,
  "browser": 1.8972412,
  "platform": 1.6211865,
  "java": 1.5984035,
  "sql": 1.5119768,
  "engine": 1.4900811,
  ...
}
```

As you can see, the input text doesn’t directly mention most of the words listed in the response, but they look semantically related. It means, the model knows that the concepts of these words are related to the input text based on the corpus the model was trained on. Therefore, the quality of these sparse embeddings depends on the ML model you configured.

### Search with a semantic query

Now you can perform semantic search against the “sparse-test” index with sparse\_vector query. I’ve ingested some Elastic’s blog content into `sparse-test` index, so let’s test it out.

```sh
GET sparse-test/_search
{
   "query":{
      "sparse_vector":{
         "field": "content_embedding",
         "inference_id": "naver__splade-v3-distilbert",
         "query": "How to implement semantic search?"
      }
   }
}
```

The response was:

```sh
{
  "hits": {
    "hits": [
      {
        "_index": "sparse-test",
        "_id": "QYrHE5UB5umUPDxXt3YF",
        "_score": 1.9065769,
        "_source": {
          "content": "In this article, we'll learn how to connect local models to the Elasticsearch inference model using Ollama and then ask your documents questions using Playground.",
          "content_embedding": {
            "algorithms": 1.2229483,
            "modeling": 1.4566671,
            "inference": 1.4407207,
            "software": 1.3217216,
            "neural": 0.4337984,
            ...
          },
          "model_id": "naver__splade-v3-distilbert"
        }
      },
      {
        "_index": "sparse-test",
        "_id": "RorHE5UB5umUPDxXt3YF",
        "_score": 1.4432585,
        "_source": {
          "content": "One of the main challenges that developers, SREs, and DevOps professionals face is the absence of an extensive tool that provides them with visibility to their application stack. Many of the APM solutions out on the market do provide methods to monitor applications that were built on languages and frameworks (i.e., .NET, Java, Python, etc.) but fall short when it comes to C++ applications.",
          "content_embedding": {
            "code": 0.3599707,
            "software": 2.6935644,
            "developers": 0.4449697,
            "cad": 0.19158684,
            "##kit": 0.03371501,
            ...
          },
          "model_id": "naver__splade-v3-distilbert"
        }
      },
      {
        "_index": "sparse-test",
        "_id": "SorHE5UB5umUPDxXt3YF",
        "_score": 1.2041138,
        "_source": {
          "content": "Elastic and Confluent are key technology partners and we're pleased to announce new investments in that partnership. Built by the original creators of Apache Kafka®, Confluent's data streaming platform is a key component of many Enterprise ingest architectures, and it ensures that customers can guarantee delivery of critical Observability and Security data into their Elasticsearch clusters. Together, we've been working on key improvements to how our products fit together. With Elastic Agent's new Kafka output and Confluent's newly improved Elasticsearch Sink Connectors it's never been easier to seamlessly collect data from the edge, stream it through Kafka, and into an Elasticsearch cluster.",
          "content_embedding": {
            "server": 0.98200905,
            "software": 2.248463,
            "link": 0.37674126,
            "technology": 0.9098742,
            "networks": 0.8262937,
            ...
          },
          "model_id": "naver__splade-v3-distilbert"
        }
      },
      ...
    ]
  }
}
```

As you can see, the original content is embedded into the sparse vector representation, so you can easily understand how the model determines the meanings of those texts. The first result doesn’t contain most words that can be found in the query text, but still, the relevance score is high because the sparse vector representations are similar.

For better precision, you can also try hybrid search with [RRF](https://www.elastic.co/search-labs/blog/weighted-reciprocal-rank-fusion-rrf) so that you can combine lexical and semantic search within one query. Refer to the [official tutorial](https://www.elastic.co/guide/en/elasticsearch/reference/current/semantic-text-hybrid-search.html) to learn more.

## Conclusion

Sparse vectors provide a powerful and efficient way to enhance search capabilities in Elasticsearch. Unlike dense vectors, sparse vectors offer key advantages such as **better zero-shot performance** and **resource efficiency**. They integrate seamlessly with Elasticsearch’s machine learning capabilities and leverage Lucene’s **mature and optimized inverted index**, making them a practical choice for many applications.

Starting with Elasticsearch 8.17, users now have greater flexibility in choosing between **dense and sparse vector models** based on their specific needs. Whether you're looking for **interpretable representations**, **scalable search performance**, or **efficient memory usage**, sparse vectors provide a compelling option for modern search applications.

As Elasticsearch continues to evolve, sparse vector search is set to play an increasingly important role in the future of information retrieval. Now, you can take advantage of **ELSER and also other Hugging Face models** to explore new possibilities in semantic search.

#### Frequently Asked Questions

##### What is a sparse vector?

A sparse vector is a vector representation where most values are zero. It is often stored as key-value pairs, making it more interpretable and resource-efficient compared to dense vectors.

##### What is a dense vector?

A dense vector is a vector representation where most elements have nonzero values. It has a fixed dimension, and every element represents some feature, but their meanings are not easily interpretable by humans.

##### What is the difference between dense and sparse vectors?

Most dense vector elements have nonzero values. Here, every element represents some feature, but their meanings are not easily interpretable by humans. In contrast, sparse vectors mostly consist of zeros, with only a few nonzero values. The representation is more interpretable, as each key (feature) often corresponds to a meaningful term or concept.

##### What is the difference between lexical and semantic search?

In lexical search, matching is based on exact terms found in the document. On the other hand, semantic search captures the meaning of words and phrases, enabling retrieval of relevant documents even if they don't contain the exact query terms.