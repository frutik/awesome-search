---
title: "Distilling Retrieval Pipelines to a Single Embedding Model"
source: "https://dtunkelang.medium.com/distilling-retrieval-pipelines-to-a-single-embedding-model-606f3ecf0c91"
author:
  - "[[Daniel Tunkelang]]"
published: 2026-04-20
created: 2026-05-15
description: "More"
tags:
  - "clippings"
---
*A Pretrained Bag-of-Documents Model for Product Search*

Search systems typically treat queries as text to be interpreted. That is the wrong abstraction. Instead of building multi-stage retrieval pipelines, we can train a single embedding model to do the same job.

A query is not just a string. It is a distribution over the results it should retrieve.

A query like "wireless keyboard" is not fundamentally about the words "wireless" and "keyboard". It corresponds to a set of [relevant](https://dtunkelang.medium.com/ranking-vs-relevance-ba672c79625e) products. The center captures the canonical intent, while the spread reflects how narrowly or [broadly](https://dtunkelang.medium.com/broad-and-ambiguous-search-queries-1bbbe417dcc) that [intent](https://dtunkelang.medium.com/search-queries-and-search-intent-1dec79ad155f) is defined.

This reframes [query understanding](https://queryunderstanding.com/) as predicting result distributions rather than encoding text directly. That idea is the foundation of the [bag-of-documents model](https://dtunkelang.medium.com/modeling-queries-as-bags-of-documents-b7d79d0916ab).

[Aritra Mandal](https://www.linkedin.com/in/aritram/) and I [introduced this model](https://arxiv.org/abs/2308.03869) at the [KDD 2023 workshop on e-commerce and NLP](https://www.aclweb.org/portal/content/e-commerce-nlp). In this post, I describe a pretrained version of that model, along with a simple pipeline for training it using entirely public data and local compute.

## From Queries to Result Distributions

The bag-of-documents model represents each query as a set of relevant documents — a "bag" — rather than as a sequence of tokens. Each bag has two key properties:

- A **centroid vector**, representing the canonical search intent.
- A [**specificity**](https://queryunderstanding.com/query-specificity-a6156f4043eb) **score**, defined as the mean cosine similarity between the centroid and the documents in the bag.

Broad queries produce diffuse bags with lower specificity; narrow queries produce tightly clustered bags with higher specificity.

For example:

- "laptop" → specificity ≈ 0.70
- "hp laptop" → ≈ 0.81
- "hp laptop 16gb ram" → ≈ 0.84

The goal of the model is to map query text directly to the centroid of its corresponding bag.

## Why a Pretrained Model?

In principle, any organization with query logs and relevance data could build a bag-of-documents model. In practice, many lack either the data or the infrastructure to do so.

A pretrained model lowers that barrier. It provides:

- A strong initialization for query understanding.
- A simple, adaptable training pipeline.
- A working system that runs entirely locally.

To demonstrate this, I built the full pipeline using public datasets and ran it on a 16GB MacBook Air M4.

## The Retrieval Index

The model operates over a fixed catalog of products represented in a shared embedding space.

I built a [FAISS](https://github.com/facebookresearch/faiss) index over a 6M-product subset of the [McAuley Lab Amazon Reviews 2023 dataset](https://amazon-reviews-2023.github.io/) (a 20% sample), embedding each product title using the base [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) model. This index serves two roles:

- During **bag construction**, it provides candidates for semantic retrieval.
- During **inference**, it is the target of nearest-neighbor search.

Because the fine-tuned query model shares its embedding space with the base product model, no re-indexing is required. The same FAISS index is used for both training and serving.

## Building the Bags

The critical step is constructing high-quality bags of documents for real queries. I used the 75K queries from the [Amazon Shopping Queries Dataset](https://github.com/amazon-science/esci-data) and built bags using a hybrid retrieval and filtering pipeline.

### Hybrid Retrieval

For each query, I retrieve candidates using two complementary methods:

- **Semantic retrieval**: embedding the query with a [MiniLM](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) model and retrieving nearest neighbors from a [FAISS](https://github.com/facebookresearch/faiss) index.
- **Lexical retrieval**: retrieving keyword matches using [Tantivy](https://github.com/quickwit-oss/tantivy).

Semantic and lexical retrieval produce largely disjoint results — and you need both. In practice, over a third of the final bag members come from keyword search alone, with minimal overlap between the two methods.

This reflects their complementary strengths:

- Semantic retrieval captures meaning without requiring token overlap.
- Lexical retrieval captures exact matches for brands, model numbers, and rare terms.

You need both to approximate the true intent distribution.

### Relevance Filtering

The combined candidate set is:

- Deduplicated.
- Scored using a [cross-encoder model](https://huggingface.co/LiYuan/Amazon-Cup-Cross-Encoder-Regression) that [Li Yuan](https://huggingface.co/LiYuan) trained for the Amazon Shopping Queries Dataset.
- Filtered to remove low-relevance results (those that score less than 0.3 on the cross-encoder) and truncated to the top 50.

This step is critical: bag quality determines the quality of the model.

### Bag Representation

Each bag is stored as:

- A set of document titles.
- A centroid vector.
- A specificity score.

Individual document embeddings are discarded to keep storage manageable.

## Training the Model

Once the bags are constructed, training is straightforward.

Each query becomes a training example:

- Input: query text.
- Target: centroid vector of its bag.

The model is the same all-MiniLM-L6-v2 sentence transformer model used for the product vectors, fine-tuned to minimize cosine distance between its output and the target centroid.

Training details:

- ~74K usable queries after filtering.
- 80/20 train-validation split.
- Batch size: 32.
- 15 epochs.
- Model selection based on nearest-neighbor recall on held-out queries.

The entire training run takes about an hour on a laptop.

## Distilling a Retrieval Pipeline

The key result is that the trained model internalizes the behavior of a full retrieval pipeline.

At training time, bags are constructed using:

- Hybrid retrieval.
- Cross-encoder reranking.
- Relevance filtering.

At inference time, none of that is needed. Query processing reduces to:

- Encode the query.
- Retrieve nearest neighbors from the precomputed product index.

The model distills a multi-stage retrieval pipeline into a single embedding step at query time, while retaining the same retrieval index.

## Results

I evaluated the fine-tuned model against the base MiniLM model using held-out queries and the dataset's relevance judgments. Across all metrics, the fine-tuned model behaves much more like the full retrieval pipeline it approximates.

The fine-tuned model consistently outperforms the base model:

- **Cosine similarity to centroid** improves from 0.787 to 0.914.
- **Recall@10** (overlap with centroid's top results) rises from 0.367 to 0.506.
- **ESCI precision** increases from 96.0% to 97.0%.
- **Complement retrieval rate** drops from 14.2% to 7.7% (lower is better).

Each metric captures a different aspect of performance.

Cosine similarity measures how well the model reproduces the target embedding space. The jump from 0.787 to 0.914 suggests that the model has internalized where the full retrieval pipeline would place each query.

Recall@10 evaluates whether that translates into retrieving the right products. The increase from 0.367 to 0.506 indicates that the model retrieves results much closer to those produced by the full pipeline.

ESCI precision is already near ceiling for the base model, so the gain there is modest. The more interesting result is the complement retrieval rate, which nearly halves. For queries like "iphone," retrieving cases instead of phones is a classic failure mode in product search. The bag-of-documents model reduces this error because it learns from result distributions rather than isolated examples.

## Specificity as an Emergent Property

Query specificity emerges naturally from the bag construction process.

As queries become more constrained, their bags become more internally consistent, and their centroids better defined. This provides a principled way to quantify specificity without introducing an explicit scalar feature.

## Relation to Prior Work

The bag-of-documents model can be understood as a learned, amortized form of [pseudo-relevance feedback](https://en.wikipedia.org/wiki/Relevance_feedback#Pseudo_relevance_feedback).

Traditional pseudo-relevance feedback:

- Retrieves documents.
- Uses them to refine the query.
- Repeats at inference time.

The bag-of-documents model:

- Uses retrieved documents during training.
- Learns to predict their aggregate representation.
- Eliminates the need for feedback at inference time.

It can also be viewed as a form of distillation: a complex retrieval pipeline is compressed into a single encoder.

## Resources

Everything described here is available under an MIT license:

- Model and data: [huggingface.co/datasets/dtunkelang/bag-of-documents](https://huggingface.co/datasets/dtunkelang/bag-of-documents)
- Live demo: [huggingface.co/spaces/dtunkelang/bag-of-documents-demo](https://huggingface.co/spaces/dtunkelang/bag-of-documents-demo)
- Code: [github.com/dtunkelang/bag-of-documents](https://github.com/dtunkelang/bag-of-documents)

## Next Steps

This is a starting point, not an endpoint.

Obvious directions include:

- Scaling to the full 30M-product catalog.
- Exploring stronger base models and cross-encoders.
- Evaluating against production-grade ranking systems.

More broadly, the bag-of-documents model suggests a different abstraction for search. Queries are not just text to be interpreted. They are latent distributions over results to be predicted.

## Final Note

The bag-of-documents model does not eliminate retrieval. It changes where the complexity lives. Instead of constructing result sets at query time, we learn where to retrieve from.