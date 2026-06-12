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


> **HNSW caveat with inner product:** Inner product does not satisfy the triangle inequality, and HNSW's graph construction assumes it. Vectors with large magnitudes are prioritised during graph traversal regardless of direction, which can silently degrade recall. Mitigate by normalising vectors before indexing (making inner product ≡ cosine) or by using IVF-based indexes that don't rely on triangle inequality.

## Normalised Vectors: The Equivalence That Matters in Production

When embeddings are L2-normalised to unit length (‖v‖ = 1), dot product and cosine similarity compute **identical rankings** — the denominator in the cosine formula becomes 1 and drops out. This is true of most modern dense retrieval models (OpenAI, E5, BGE, sentence-transformers with default pooling).

**Performance implication:** dot product skips the magnitude division, making it roughly **50% faster to compute** than cosine for the same vector dimensionality. For high-throughput search where vectors are unit-normalised, prefer dot product / inner product as the index metric.

| Condition | Dot product ≡ Cosine? | Recommendation |
|---|---|---|
| Unit-normalised vectors | Yes (identical rankings) | Use dot product for speed |
| Non-normalised, magnitude-meaningful | No | Use dot product |
| Non-normalised, magnitude irrelevant | No | Use cosine |
| Spatial / clustering workloads | N/A | Use L2 |

## Binary Metrics

For compressed or binary-quantised vectors (see [[Binary Quantization]]), standard floating-point metrics do not apply. Two alternatives:

**Hamming distance** — counts the number of differing bits between two binary vectors. Extremely fast on modern CPUs via `XOR` + `popcount`. Used with binary-quantised embeddings to get approximate similarity at ~32× memory reduction with some recall loss.

**Jaccard similarity** — intersection-over-union of the set of non-zero positions. More interpretable for sparse binary data; less common in ANN indexes but used in MinHash-based near-duplicate detection.

These metrics are niche in semantic search but essential when operating [[Binary Quantization]] or [[Vector Quantization]] schemes for memory-constrained deployments.

## Practical Decision Guide

1. **Check the model card first.** Use the metric the model was trained with — mismatching metric and training objective degrades retrieval quality, often silently.
2. **Unit-normalised outputs?** Use dot product (= cosine, but faster).
3. **Magnitude carries meaning?** Use dot product (covers both direction and scale).
4. **Spatial or clustering workload?** Use L2.
5. **Binary or heavily quantised vectors?** Use Hamming.

> Model selection has ~10× more impact on retrieval quality than metric choice. Optimise the model before tuning the metric.

## Related Concepts

- [[Embeddings]] — what the vectors being compared represent
- [[Dense Embeddings]] — the type of vectors these metrics apply to
- [[Dense Vector Retrieval]] — ANN/KNN search using these metrics
- [[Bi-Encoder]] — models that produce vectors for similarity comparison
- [[HNSW]] — the dominant ANN graph index; has a caveat with unnormalised inner product
- [[IVF]] — cluster-based ANN index; does not assume triangle inequality
- [[Vector Quantization]] — approximating distance under compression
- [[Binary Quantization]] — extreme compression requiring Hamming/Jaccard metrics
- [[Matryoshka Embeddings]] — variable-dimension embeddings; metric choice interacts with truncation
