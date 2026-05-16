---
title: "Vector Similarity Metrics"
aliases: ["cosine similarity", "dot product", "euclidean distance", "L2 distance", "inner product", "vector distance", "similarity function", "vector similarity"]
tags:
  - concept
  - vector-search
  - embeddings
  - foundations
---

# Vector Similarity Metrics

## Definition

Similarity (or distance) functions that measure how "close" two vectors are in embedding space. The choice of metric affects what geometry the model learns and which ANN index structures work efficiently.

## The Three Core Metrics

### Cosine Similarity

Measures the **angle** between two vectors — ignores magnitude, only cares about direction.

```
cos(A, B) = (A · B) / (|A| × |B|)
```

- Range: -1 (opposite) to 1 (identical direction)
- **0 = orthogonal (unrelated)**
- For unit vectors: cosine similarity = dot product (identical computationally)

**Use when:** vectors are not normalized; magnitude carries no meaning (e.g., TF-IDF vectors of different document lengths).

### Dot Product (Inner Product)

```
A · B = Σ(aᵢ × bᵢ)
```

- No fixed range; value depends on vector magnitudes
- For unit-norm vectors: equivalent to cosine similarity
- Rewards both **direction alignment and magnitude**

**Use when:** embeddings are trained with dot-product objectives (most modern dense retrieval models like OpenAI, E5, BGE use inner product). Dot product similarity is faster to compute than cosine (no normalization step).

> Most embedding models normalize outputs to unit length, making dot product and cosine similarity equivalent in practice.

### Euclidean Distance (L2)

```
d(A, B) = √(Σ(aᵢ - bᵢ)²)
```

- Range: 0 (identical) to ∞
- Measures straight-line distance in the vector space
- Sensitive to magnitude differences

**Use when:** vectors represent spatial coordinates, or the model was trained with L2 objectives. Common in image retrieval and KNN classification.

## Metric Comparison

| Metric | Geometry | Normalization needed | Typical use |
|---|---|---|---|
| Cosine | Angle | No (ignores magnitude) | Text search, unnormalized vectors |
| Dot product | Angle + magnitude | No (but faster with norm) | Dense retrieval, recommendation |
| Euclidean (L2) | Straight-line | Optional | Image search, spatial data |

## Which Metric Does Your Model Use?

Check the model card. Common conventions:
- **OpenAI text-embedding-3**: dot product (normalized outputs → cosine = dot)
- **sentence-transformers**: cosine similarity by default
- **FAISS Flat index**: L2 distance by default (use `IndexFlatIP` for inner product)
- **Elasticsearch dense_vector**: configurable (`cosine`, `dot_product`, `l2_norm`)

Mixing metrics — e.g., indexing with L2 but querying with cosine — produces **wrong results**.

## ANN Index Compatibility

Different [[Dense Vector Retrieval|ANN indexes]] are optimized for specific metrics:

| Index | Preferred metric |
|---|---|
| HNSW (`cosine`) | Cosine / inner product |
| FAISS `IndexFlatL2` | Euclidean L2 |
| FAISS `IndexFlatIP` | Inner product |
| `pgvector` | Configurable (`<->`, `<#>`, `<=>`) |

## Related Concepts

- [[Embeddings]] — what the vectors being compared represent
- [[Dense Embeddings]] — the type of vectors these metrics apply to
- [[Dense Vector Retrieval]] — ANN/KNN search using these metrics
- [[Bi-Encoder]] — models that produce vectors for similarity comparison
- [[Vector Quantization]] — approximating distance under compression
