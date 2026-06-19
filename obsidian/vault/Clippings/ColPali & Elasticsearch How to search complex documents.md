---
title: "ColPali & Elasticsearch: How to search complex documents"
source: "https://www.elastic.co/search-labs/blog/elastiacsearch-colpali-document-search"
author:
  - "[[Peter Straßer]]"
published: 2025-03-16
created: 2026-06-19
description: "Learn about ColPali and explore how to use it to search through complex documents in Elasticsearch, including tables, figures, multiple columns & more."
tags:
  - "clippings"
---
Elasticsearch is packed with new features to help you build the best search solutions for your use case. Learn how to put them into action in our hands-on webinar on [building a modern Search AI experience](https://www.elastic.co/virtual-events/getting-started-semantic-search-excellence). You can also start a [free cloud trial](https://cloud.elastic.co/registration) or try Elastic on your [local machine](https://github.com/elastic/start-local) now.

When building search applications, we often need to deal with documents that have complex structures—tables, figures, multiple columns, and more. Traditionally, this meant setting up complicated retrieval pipelines including OCR (optical character recognition), layout detection, semantic chunking, and other processing steps. In 2024, the model [ColPali](https://arxiv.org/pdf/2407.01449) was introduced to address these challenges and simplify the process.

![](https://www.elastic.co/search-labs/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fme0ej585%2Fsearch-labs-import-testing%2Ff642006f1dec8a516d1949cf40abfabd2219756f-970x794.png&w=3840&q=75)

Source: https://huggingface.co/blog/manu/colpali

From [Elasticsearch](https://elastic.co/elasticsearch) version 8.18 onwards, we added support for late-interaction models such as ColPali as a tech preview feature. In this blog, we will take a look at how we can use ColPali to search through documents in Elasticsearch.

## ColPali performance

While we have [many benchmarks](https://www.elastic.co/guide/en/machine-learning/current/ml-nlp-elser.html#elser-qualitative-benchmarks) that are based on previously cleaned-up text data to compare different retrieval strategies, the authors of the ColPali paper argue that real-world data in many organizations is messy and not always available in a nice, cleaned-up format.

![Example documents from the ColPali paper](https://www.elastic.co/search-labs/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fme0ej585%2Fsearch-labs-import-testing%2Fd9b10e740bf5a055089116bee35630a8373e4436-1014x680.png&w=3840&q=75)

Example documents from the ColPali paper: https://arxiv.org/pdf/2407.01449

To better represent these scenarios, the [ViDoRe benchmark](https://huggingface.co/spaces/vidore/vidore-leaderboard) was released alongside the ColPali model. This benchmark includes a diverse set of document images from sectors such as government, healthcare, research, and more. A range of different retrieval methods, including complex retrieval pipelines or image [embedding models](https://www.elastic.co/what-is/vector-embedding), were compared with this new model.

The following table shows that ColPali performs exceptionally well on this dataset and is able to retrieve relevant information from these messy documents reliably.

![ColPali retrieval performance ](https://www.elastic.co/search-labs/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fme0ej585%2Fsearch-labs-import-testing%2Fce5361af7353005a0e34b3b21f1e22be4ace4559-1600x966.png&w=3840&q=75)

Source: https://arxiv.org/pdf/2407.01449 Table 2

## How ColPali works

As teased in the beginning, the idea of ColPali is to just embed the image instead of extracting the text via complicated pipelines. ColPali builds on the vision capabilities of the PaliGemma model and the late-interaction mechanism introduced by ColBERT.

![How ColiPali works](https://www.elastic.co/search-labs/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fme0ej585%2Fsearch-labs-import-testing%2Fd26e7f36ceaac345abd3e54a52f9715e8b40ec4a-1600x965.png&w=3840&q=75)

Source: https://arxiv.org/pdf/2407.01449 Figure 1

Let’s first take a look at how we index our documents.

Instead of converting the document into a textual format, ColPali processes documents by dividing a screenshot into small rectangles and converts each into a 128-dimensional vector. This vector represents the contextual meaning of this patch within the document. In practice, a 32x32 grid generates 1024 vectors per document.

For our query, the ColPali model creates a vector for each token.

To score documents during search, we calculate the distance between each query vector and each document vector. We keep only the highest score per query vector and sum those scores for a final document score.

![ColPali late interaction mechanism for scoring ColBERT](https://www.elastic.co/search-labs/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fme0ej585%2Fsearch-labs-import-testing%2F4926ef745a9f686ec7810213bee4d7b561f3ca3d-1600x665.png&w=3840&q=75)

Late interaction mechanism for scoring ColBERT

## ColPali interpretability

[Vector search](https://www.elastic.co/search-labs/blog/introduction-to-vector-search "Learn more about vector search") with bi-encoders struggle with the fact that the results are sometimes not very interpretable—meaning we don’t know *why* a document matched. Late interaction models are different: we know how well each document vector matches our query vectors; therefore, we can determine *where* and *why* a document matches.

![Colipali heatmap](https://www.elastic.co/search-labs/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fme0ej585%2Fsearch-labs-import-testing%2F5a8572802071717e571be5a4d7543cfc03f5c9c8-1600x1346.png&w=3840&q=75)

A heatmap of where the word “hour” matches in this document. Source: https://arxiv.org/pdf/2407.01449

## Searching with ColPali in Elasticsearch

We will be taking a subset of the ViDoRe test set to take a look at how to index documents with ColPali in Elasticsearch. The [full code examples can be found on GitHub](https://github.com/elastic/elasticsearch-labs/blob/main/supporting-blog-content/colpali/01_colpali.ipynb).

To index the document vectors, we will be defining a mapping with the new [rank\_vectors](https://www.elastic.co/guide/en/elasticsearch/reference/8.18/rank-vectors.html) field.

```python
mappings = {
    "mappings": {
        "properties": {
            "col_pali_vectors": {
                "type": "rank_vectors"
            }
        }
    }
}

INDEX_NAME = "searchlabs-colpali"
es = Elasticsearch(<ELASTIC_HOST>, api_key=<ELASTIC_API_KEY>)
es.indices.create(index=INDEX_NAME, body=mappings)

for image_path in tqdm(images, desc="Index documents"):
    vectors = create_col_pali_image_vectors(image_path)
    es_client.index(index=INDEX_NAME, id=image_path, document={"col_pali_vectors": vectors})
```

We now have an index ready to be searched full of ColPali vectors. To score our documents, we can use the new `maxSimDotProduct` function.

```python
query = "What do companies use for recruiting?"
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
                    "query_vector": create_col_pali_query_vectors(query)
                }
            }
        }
    },
    "size": 5
}

results = es.search(index=INDEX_NAME, body=es_query)
image_ids = [hit["_id"] for hit in results["hits"]["hits"]]

html = "<div style='display: flex; flex-wrap: wrap; align-items: flex-start;'>"
for image_id in image_ids:
    image_path = os.path.join(DOCUMENT_DIR, image_id)
    html += f'<img src="{image_path}" alt="{image_id}" style="max-width:300px; height:auto; margin:10px;">'
html += "</div>"

display(HTML(html))
```

![Searching with ColPali in Elasticsearch](https://www.elastic.co/search-labs/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fme0ej585%2Fsearch-labs-import-testing%2F2bfc5b9d5aaf8b89dd702ccc70f62cd47b2d165c-1600x766.png&w=3840&q=75)

Searching with ColPali in Elasticsearch

## Key takeaways on ColPali in Elasticsearch

ColPali is a powerful new model that can be used to search complex documents with high accuracy. Elasticsearch makes it easy to use as it provides a fast and scalable search solution. Since the initial release, other powerful iterations such as [ColQwen](https://huggingface.co/vidore/colqwen2-v1.0) have been released. We encourage you to try these models for your own search applications and see how they can improve your results.

Before implementing what we covered here in production environments, we highly recommend that you check out [part 2](https://www.elastic.co/search-labs/blog/scale-late-interaction-model-colpali) of this article. [Part 2](https://www.elastic.co/search-labs/blog/scale-late-interaction-model-colpali) explores advanced techniques, such as bit vectors and token pooling, which can optimize resource utilization and enable effective scaling of this solution.

#### Frequently Asked Questions

##### What is ColPali?

ColPali is a late-interaction model that simplifies the process of searching complex documents with images and tables.

##### How does ColPali works?

ColPali processes documents by dividing a screenshot into small rectangles and converting each into a 128-dimensional vector. For our query, the ColPali model creates a vector for each token. To score documents during search, the distance between each query vector and each document vector is calculated.