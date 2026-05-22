---
title: "Late interaction models: How to scale & optimize in Elasticsearch"
source: "https://www.elastic.co/search-labs/blog/late-interaction-model-colpali-scale?utm_source=chatgpt.com"
author:
  - "[[Peter Straßer]]"
  - "[[Benjamin Trent]]"
published: 2025-03-16
created: 2026-05-21
description: "Explore techniques to scale late interaction models like ColPali for large-scale vector search in Elasticsearch."
tags:
  - "clippings"
---
Elasticsearch is packed with new features to help you build the best search solutions for your use case. Learn how to put them into action in our hands-on webinar on [building a modern Search AI experience](https://www.elastic.co/virtual-events/getting-started-semantic-search-excellence). You can also start a [free cloud trial](https://cloud.elastic.co/registration) or try Elastic on your [local machine](https://github.com/elastic/start-local) now.

In our [previous blog on ColPali](https://www.elastic.co/search-labs/blog/elastiacsearch-colpali-document-search), we explored how to create visual search applications with [Elasticsearch](https://elastic.co/elasticsearch). We primarily focused on the value that models such as ColPali bring to our applications, but they come with performance drawbacks compared to [vector search](https://www.elastic.co/search-labs/blog/introduction-to-vector-search "Learn more about vector search") with bi-encoders such as E5.

Building on the examples from [part 1](https://www.elastic.co/search-labs/blog/elastiacsearch-colpali-document-search), this blog explores how to use different techniques and Elasticsearch's powerful vector search toolkit in order to make late interaction vectors ready for large-scale production workloads.

The full code examples can be found on [GitHub.](https://github.com/elastic/elasticsearch-labs/tree/main/supporting-blog-content/colpali)

## Challenges of late interaction models

ColPali creates over 1000 vectors per page for the documents in our index.

This results in two challenges when working with late interaction vectors:

1. Disk space: Saving all these vectors on disks will incur a serious amount of storage usage, which will be expensive at scale.
2. Computation: When ranking our documents with the `maxSimDotProduct()` comparison, we need to compare all of these vectors for each of our documents with the N vectors of our query.

Let’s look at some techniques for addressing these issues.

## Techniques to optimize late interaction models

### Bit vectors

In order to reduce disk space, we can compress the images into bit vectors. We can use a simple Python function to transform our multi-vectors into bit vectors:

```python
def to_bit_vectors(embeddings: list) -> list:
    return [
        np.packbits(np.where(np.array(embedding) > 0, 1, 0))
        .astype(np.int8)
        .tobytes()
        .hex()
        for embedding in embeddings
    ]
```

The function's core concept is straightforward: values above 0 become 1, and values below 0 become 0. This results in an array of 0s and 1s, which we then transform into a hexadecimal string representing our bit vector.

For our index mapping, we set the `element_type` parameter to `bit`:

```python
mappings = {
    "mappings": {
        "properties": {
            "col_pali_vectors": {
                "type": "rank_vectors",
                "element_type": "bit"
            }
        }
    }
}

es.indices.create(index=INDEX_NAME, body=mappings)
```

After having written all of our new bit vectors to our index, we can rank our bit vectors using the following code:

```python
query = "What do companies use for recruiting?"
query_vector = to_bit_vectors(create_col_pali_query_vectors(query))
es_query = {
    "_source": False,
    "query": {
        "script_score": {
            "query": {
                "match_all": {}
            },
            "script": {
                "source": "maxSimInvHamming(params.query_vector, 'col_pali_vectors')",
                "params": {
                    "query_vector": query_vector
                }
            }
        }
    },
    "size": 5
}
```

![](https://www.elastic.co/search-labs/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fme0ej585%2Fsearch-labs-import-testing%2F51b989446e4099745971e1eac27d147a78d13e0a-1600x480.png&w=3840&q=75)

Trading off a bit of accuracy, this allows us to use hamming distance (`maxSimInvHamming(...)`), which is able to leverage optimizations such as bit-masks, SIMD, etc. Learn more about [bit vectors and hamming distance in our blog](https://www.elastic.co/search-labs/blog/bit-vectors-in-elasticsearch).

Alternatively, we can not convert our query vector to bit vectors and search with the full-fidelity late interaction vector:

```python
query = "What do companies use for recruiting?"
query_vector = create_col_pali_query_vectors(query)
es_query = {
    "_source": False,
    "query": {
        "script_score": {
            "query": {
                "match_all": {}
            },
            "script": {
                "source": "maxSimDotProduct(params.query_vector, 'col_pali_vectors')",
                "params": {
                    "query_vector": query_vector
                }
            }
        }
    },
    "size": 5
}
```

![Results of using bit vectors to optimize late interaction models](https://www.elastic.co/search-labs/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fme0ej585%2Fsearch-labs-import-testing%2F89f3c795c6dc44b2f7d46801320288316b47e1b2-1600x488.png&w=3840&q=75)

Results of using bit vectors to optimize late interaction models

This will compare our vectors using an asymmetric similarity function.

Let’s think about a regular hamming distance between two bit vectors. Suppose we have a document vector *D:*

And a query vector *Q:*

Simple binary [quantization](https://www.elastic.co/search-labs/blog/better-binary-quantization-lucene-elasticsearch) will transform vectors *D* into `10101101` and *Q* into `11111011`. To find the hamming distance, we need direct bit math—it's extremely fast. In this case, the hamming distance is `01010110`, which has a bit count of 4. So, scoring then becomes the inverse of that hamming distance. Remember, more similar vectors have a SMALLER hamming distance, so inverting it allows for more similar vectors to be scored higher. Specifically here, the score would be 1/4 = `0.25`.

However, note how we lose the magnitude of each dimension. A `1` is a `1`. So, for *Q*, the difference between `0.01` and `0.79` disappears. Since we are simply quantizing according to `>0`, we can do a small trick where the Q vector isn’t quantized. This doesn’t allow for the extremely fast bitwise math, but it does keep the storage cost low as D is still quantized.

![](https://www.elastic.co/search-labs/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fme0ej585%2Fsearch-labs-import-testing%2F508e8498ba969534d2a0131d431c75735fc27cb9-1399x611.png&w=3840&q=75)

In short, this retains the information provided in *Q*, thus increasing the distance estimation quality and keeping the storage low.

Using bit vectors allows us to save significantly on disk space and computational load at query time. But there is more that we can do.

### Average vectors

To scale our search across hundreds of thousands of documents, even the performance benefits that bit vectors give us will not be enough. In order to scale to these types of workloads, we will want to leverage Elasticsearch’s HNSW index structure for vector search.

ColPali generates around a thousand vectors per document, which is too many to add to our HNSW graph. Therefore, we need to reduce the number of vectors. To do this, we can create a single representation of the document's meaning by taking the average of all the document vectors produced by ColPali when we embed our image.

![Average vector over all late interaction vectors](https://www.elastic.co/search-labs/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fme0ej585%2Fsearch-labs-import-testing%2F7c3b4dffb70bd95f67deb35f8c01e73c5286c2ab-1476x1102.png&w=3840&q=75)

We simply take the average vector over all late interaction vectors.

As of now, this is not possible within Elastic itself, and we will need to preprocess the vectors before ingesting them in Elasticsearch.

We can do this with Logstash or Ingest pipelines, but here we will use a simple Python function:

```python
def to_avg_vector(vectors):
    vectors_array = np.array(vectors)
    
    avg_vector = np.mean(vectors_array, axis=0)
    
    norm = np.linalg.norm(avg_vector)
    if norm > 0:
        normalized_avg_vector = avg_vector / norm
    else:
        normalized_avg_vector = avg_vector

    return normalized_avg_vector.tolist()
```

We are also normalizing the vector so that we can use the dot product similarity.

After transforming all of our ColPali vectors to average vectors, we can index them into our dense\_vector field:

```python
mappings = {
    "mappings": {
        "properties": {
            "avg_vector": {
                "type": "dense_vector",
                "dims": 128,
                "index": True,
                "similarity": "dot_product"
            },
            "col_pali_vectors": {
                "type": "rank_vectors",
                "element_type": "bit"
            }
        }
    }
}

es.indices.create(index=INDEX_NAME, body=mappings)
```

We have to consider that this will increase total disk usage since we are saving more information along with our late interaction vectors. Additionally, we will use extra RAM to hold the HNSW graph, allowing us to scale the search over billions of vectors. To reduce the usage of RAM, we can make use of our popular [BBQ feature](https://www.elastic.co/search-labs/blog/optimized-scalar-quantization-elasticsearch). In turn, we get fast search results over massive data sets that would otherwise not be possible.

Now, we simply search with the knn query to find our most relevant documents.

```python
query = "What do companies use for recruiting?"
query_vector = to_avg_vector(create_col_pali_query_vectors(query))
es_query = {
    "_source": False,
    "knn": {
        "field": "avg_vector",
        "query_vector": query_vector,
        "k": 10,
        "num_candidates": 100
    },
    "size": 5
}
```

![](https://www.elastic.co/search-labs/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fme0ej585%2Fsearch-labs-import-testing%2Fa500f9907020f032c3b1c7a48ed8c759dc2a1dd4-1600x498.png&w=3840&q=75)

The previously best match has unfortunately fallen to rank 3.

To fix this problem, we can do a multi-stage retrieval. In our first stage, we are using the knn query to search for the best candidates for our query over millions of documents. In the second stage, we are only [reranking](https://www.elastic.co/search-labs/blog/elastic-semantic-reranker-part-1) the top k (here: 10) with the higher fidelity of the ColPali late interaction vectors.

```python
query = "What do companies use for recruiting?"
col_pali_vector = create_col_pali_query_vectors(query)
avg_vector = to_avg_vector(col_pali_vector)
es_query = {
  "_source": False,
  "retriever": {
    "rescorer": {
      "retriever": {
        "knn": {
          "field": "avg_vector",
          "query_vector": avg_vector,
          "k": 10,
          "num_candidates": 100
        }
      },
      "rescore": {
        "window_size": 10,
        "query": {
          "rescore_query": {
            "script_score": {
              "query": {
                "match_all": {}
              },
              "script": {
                "source": "maxSimDotProduct(params.query_vector, 'col_pali_vectors')",
                "params": {
                  "query_vector": col_pali_vector
                }
              }
            }
          }
        }
      }
    }
  },
  "size": 5
}
```

![Results of using average vectors for optimizing late interaction models](https://www.elastic.co/search-labs/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fme0ej585%2Fsearch-labs-import-testing%2F797f490860af87fcf29f34668a5c4511419c6fd0-1600x501.png&w=3840&q=75)

Results of using average vectors for optimizing late interaction models

Here, we are using the in 8.18 introduced [rescore retriever](https://www.elastic.co/guide/en/elasticsearch/reference/8.18/retriever.html#rescorer-retriever) to rerank our results. After rescoring we see that our best match is again in first position.

Note: In a production application, we can use a much higher k than 10 as the max sim function is still comparatively performant.

### Token pooling

Token pooling reduces the sequence length of multi-vector [embeddings](https://www.elastic.co/what-is/vector-embedding) by pooling redundant information, such as white background patches. This technique decreases the number of embeddings while preserving most of the page's signal.

![Token pooling to optimize late interaction models](https://www.elastic.co/search-labs/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fme0ej585%2Fsearch-labs-import-testing%2F09eae0b768f4b450e555d7e53e57561bd52de2c0-1412x1056.png&w=3840&q=75)

We are clustering semantically similar vectors to achieve less vectors overall.

Token pooling works by grouping similar token embeddings within a document into clusters using a clustering algorithm. Then, the mean of the vectors in each cluster is calculated to create a single, aggregated representation. This aggregated vector replaces the original tokens in the group, reducing the total number of vectors without significant loss of document signal.

The ColPali paper proposes an initial pool factor value of 3 for most datasets, which maintains 97.8% of the original performance while reducing the total number of vectors by 66.7%.

![Pool factor for optimizing late interaction models](https://www.elastic.co/search-labs/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fme0ej585%2Fsearch-labs-import-testing%2F343cc9eaf54af8c7a125d4115838f3c7d5659de0-1600x1007.png&w=3840&q=75)

Source: https://arxiv.org/pdf/2407.01449

But we need to be careful: The "Shift" dataset, which contains very dense, text-heavy documents with little white space, declines rapidly in performance as pool factors increase.

To create the pooled vectors, we can use the colpali\_engine library:

```python
from colpali_engine.compression.token_pooling import HierarchicalTokenPooler

pooler = HierarchicalTokenPooler(pool_factor=3) # test on your data for a good pool_factor

def pool_vectors(embedding: list) -> list:
    tensor = torch.tensor(embedding).unsqueeze(0)
    pooled = pooler.pool_embeddings(tensor)
    return pooled.squeeze(0).tolist()
```

We now have a vector that was reduced by about 66.7% in its dimensions. We index it as usual and we are able to search on it with our `maxSimDotProduct()` function.

![Late interaction models results](https://www.elastic.co/search-labs/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fme0ej585%2Fsearch-labs-import-testing%2F2412c5db7d79a590b96d42fe01f140c42f010612-1600x481.png&w=3840&q=75)

Late interaction models results

We are able to get good search results at the expense of some slight accuracy in the results.

Hint: With a higher pool\_factor (100-200), you can also have a middle ground between the average vector solution and the one we discussed here. With around 5-10 vectors per document, it becomes viable to index them in a nested field to leverage the HNSW index.

## Coss-encoder vs. late-interaction vs. bi-encoder

With what we have learned so far, where does this place late interaction models, such as ColPali or ColBERT, when we compare them to other AI retrieval techniques?

While the max sim function is cheaper compared to cross-encoders, it still requires many more comparisons and computation than vector search with bi-encoders, where we are just comparing two vectors for each query-document pair.

![Coss-encoder vs. late-interaction models vs. bi-encoder](https://www.elastic.co/search-labs/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fme0ej585%2Fsearch-labs-import-testing%2F75e1fc9e601aa7a6e88f137565c1919166c7a71c-1480x458.png&w=3840&q=75)

Coss-encoder vs. late-interaction models vs. bi-encoder

Because of this, our recommendation for late-interaction models is to generally only use them for reranking the top k search results. We also capture this in the name of the field type: rank\_vectors.

But what about the cross encoder? Are late interaction models better because they are cheaper to execute at query time? As is often the case, the answer is: it depends. Cross encoders generally produce higher quality results, but they require a lot of compute because the query document pairs need to do a full pass through the transformer model. They also benefit from the fact that they do not require any indexing of vectors and can operate in a stateless manner. This results in:

- Less disk space used
- A simpler system
- Higher quality of search results
- Higher latency, and therefore not being able to rerank as deep

On the other hand, late Interaction models can offload some of this computation at index them, making the query cheaper. The price we pay is having to index the vectors, which makes our indexing pipelines more complex and also requires more disk space to save these vectors.

Specifically in the case of ColPali, the analysis of information from images is very expensive as they contain a lot of data. In this case, the tradeoff shifts in favor of using a late interaction model such as ColPali because evaluating this information at query time would be too resource-intensive/slow.

For a late interaction model such as ColBERT, which works on text data like most cross-encoders (e.g., elastic-rerank-v1), the decision might lean more toward using the cross-encoder to benefit from the disk savings and simplicity.

We encourage you to weigh those pros and cons for your use case and experiment with the different tools that Elasticsearch provides you to build the best search applications.

## Conclusion

In this blog, we explored various techniques to optimize late interaction models like ColPali for large-scale vector search in Elasticsearch. While late interaction models provide a strong balance between retrieval efficiency and ranking quality, they also introduce challenges related to storage and computation.

To address these challenges, we looked at:

- **Bit vectors** to significantly reduce disk space while leveraging efficient similarity computations like hamming distance or asymmetric max similarity.
- **Average vectors** to compress multiple embeddings into a single dense representation, enabling efficient retrieval with HNSW indexing.
- **Token pooling** to intelligently merge redundant embeddings while maintaining semantic integrity, reducing computational overhead at query time.

Elasticsearch provides a powerful toolkit to customize and optimize search applications based on your needs. Whether you prioritize retrieval speed, ranking quality, or storage efficiency, these tools and techniques allow you to balance performance and quality as you need for your real-world applications.