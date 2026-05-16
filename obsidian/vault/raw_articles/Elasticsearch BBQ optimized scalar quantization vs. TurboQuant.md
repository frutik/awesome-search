---
title: "Elasticsearch BBQ: optimized scalar quantization vs. TurboQuant"
source: "https://www.elastic.co/search-labs/blog/elasticsearch-bbq-osq-vs-turbo"
author:
  - "[[Thomas Veasey]]"
published: 2026-04-09
created: 2026-05-15
description: "OSQ's symmetric kernels run 10–40× faster than TurboQuant on CPU, with better ranking accuracy on real embeddings. Here's what the benchmarks show."
tags:
  - "clippings"
---
From vector search to powerful REST APIs, Elasticsearch offers developers the most extensive search toolkit. Dive into our sample notebooks in the [Elasticsearch Labs repo](https://github.com/elastic/elasticsearch-labs?tab=readme-ov-file) to try something new. You can also start your [free trial](https://cloud.elastic.co/registration) or run [Elasticsearch locally](https://github.com/elastic/start-local) today.

In CPU [vector search](https://www.elastic.co/search-labs/blog/introduction-to-vector-search "Learn more about vector search"), [Elasticsearch](https://elastic.co/elasticsearch) 's [Optimized Scalar Quantization (OSQ)](https://www.elastic.co/search-labs/blog/scalar-quantization-optimization) (the algorithm behind [Better Binary Quantization (BBQ)](https://www.elastic.co/search-labs/blog/optimized-scalar-quantization-elasticsearch)) [beats](https://www.elastic.co/beats) [TurboQuant](https://research.google/blog/turboquant-redefining-ai-efficiency-with-extreme-compression/) where production systems care most: throughput, ranking accuracy, and storage efficiency. In our tests on Apple M2 Max, OSQ's symmetric kernels are 10-40x faster, and on shifted [embeddings](https://www.elastic.co/what-is/vector-embedding) its 1-bit document encoding beats TurboQuant at 4 bits on ranking accuracy while using far less storage. TurboQuant still wins on raw reconstruction MSE, but that advantage comes mostly from the Hadamard rotation and does not translate into better CPU search behavior.

#### A brief quantization primer

Vector search indexes often store millions or billions of embedding vectors, each hundreds or thousands of floats wide. Scalar [quantization](https://www.elastic.co/search-labs/blog/better-binary-quantization-lucene-elasticsearch) compresses each float coordinate independently to a small integer, typically 1, 2, or 4 bits, reducing storage by 8-32× and enabling fast integer-arithmetic scoring.  
Why does per-coordinate quantization work at all? Because the expected squared error decomposes as a sum of independent per-coordinate terms: $\mathbb{E}[\|x - q(x)\|^2] = \sum_i \mathbb{E}[(x_i - q_i(x_i))^2]$, by linearity of expectation. Each coordinate can be quantized independently regardless of the joint distribution. The remaining question is how to make each per-coordinate quantizer *good*.

#### BBQ and Optimized Scalar Quantization

[Better Binary Quantization (BBQ)](https://www.elastic.co/search-labs/blog/optimized-scalar-quantization-elasticsearch), and its underlying algorithm [Optimized Scalar Quantization (OSQ)](https://www.elastic.co/search-labs/blog/scalar-quantization-optimization), have been part of Elasticsearch for multiple releases. OSQ is an evolution of several techniques to make scalar quantization more accurate, specifically for vector search.

Each vector's components are mapped to a uniform grid over an interval $[a, b]$. The interval is initialized from the vector's statistics (assuming approximately normal residuals), using the [exact same optimization objective](https://www.elastic.co/search-labs/blog/scalar-quantization-optimization#initializing-the-quantization-interval) as TurboQuant but with an additional constraint on centroid positions. They are then refined by coordinate descent to minimize an anisotropic loss $L = (1-\lambda)(x \cdot e)^2/\|x\|^2 + \lambda\|e\|^2$, where $e$ is the quantization error vector. With the production default $\lambda = 0.1$, this deliberately sacrifices some MSE to concentrate accuracy along the query direction. This is the direction that matters for ranking.

Before quantization, the segment (or cluster in the case of Inverted Vector File (IVF) indices) centroid $c$ is subtracted from every vector. This removes the dominant shared component that would otherwise waste the quantizer's dynamic range. Both the symmetric and asymmetric dot-product paths also center the query using the same segment centroid, so the only quantized inner product is between centered residuals. The correction terms, $\langle c, x \rangle$ for each vector and $\|c\|^2$, depend on only a single vector each, and can be precomputed exactly. Centering therefore adds no per-pair cost.

Documents are quantized at 1-bit (32× compression), queries at 4-bit (cheap since there are only a handful per search). The storage constraint binds on documents, not queries, so spending more bits on the query side recovers float-query accuracy while keeping per-document footprint minimal.

A block-diagonal [orthogonal](https://en.wikipedia.org/wiki/Orthogonal_matrix) preconditioner equalizes coordinate variances and normalizes their distribution before quantization. This is the same goal as a full [Hadamard rotation](https://en.wikipedia.org/wiki/Hadamard_transform) used by TurboQuant, but with no power-of-2 padding overhead.

Because the grid is uniform, quantized dot products decompose into integer dot products with scalar corrections. This enables NEON/SVE and SSE/AVX popcount and multiply-accumulate pipelines: bit-plane decomposition for 1-bit and 2-bit, nibble multiply for 4-bit, and a [RaBitQ-style](https://www.elastic.co/search-labs/studio/content/posts;d8336fba-c31a-42fe-8c27-0178f7779203%2Ctemplate%3Dpost) mixed 4×1 kernel that decomposes to four 1-bit kernels.

#### TurboQuant

[TurboQuant](https://arxiv.org/pdf/2504.19874) (Google, ICLR 2026) takes a slightly different path to the same starting observation: that concentrated, predictable per-coordinate distributions are easy to quantize well.

Rather than adapting the quantizer per vector, TurboQuant normalizes the vector and applies a shared randomized Hadamard rotation to the entire dataset. This general sort of idea was first proposed and formalized by [RaBitQ](https://arxiv.org/pdf/2405.12497), which showed that the random rotation yields worst-case bounds over the data, holding for any fixed unit vector, for their quantization scheme. The idea of implementing via a Hadamard rotation was suggested by [Weaviate for rotational quantization](https://weaviate.io/blog/8-bit-rotational-quantization). After normalization and rotation, each coordinate's distribution almost always converges to $\mathcal{N}(0, 1/d)$ in high dimensions, regardless of the original data. TurboQuant builds on this foundation: with the distribution pinned down, it solves for the optimal [Lloyd-Max](https://en.wikipedia.org/wiki/Lloyd%27s_algorithm) scalar quantizer, a 1-D $k$ -means problem on the known density. The resulting non-uniform centroids bunch up where the density is highest (near zero) and spread out in the tails. This achievies provably near-optimal MSE: within ~2.7× of the information-theoretic lower bound in general, and as tight as 1.45× at 1-bit.

For inner products, MSE-optimal quantizers introduce a multiplicative bias (which is most severe at 1-bit: $2/\pi \approx 0.64$). TurboQuant corrects this with a two-stage design ($Q_\text{prod}$): spend $b-1$ bits on the MSE quantizer, then use the remaining 1 bit for a [Quantized Johnson-Lindenstrauss](https://arxiv.org/pdf/2406.03482) (QJL) sketch of the residual, yielding a provably unbiased inner-product estimator.

The paper's nearest-neighbour experiments were conducted on GPU (NVIDIA A100), where the lookup-table access pattern maps naturally onto shared memory.

#### The key design divergence: integer arithmetic vs. lookup tables

The difference between uniform and non-uniform centroids may seem minor, but it creates a large computational gap.

OSQ's uniform grid means each quantized coordinate is an integer whose arithmetic meaning is preserved. The dot product of two quantized vectors decomposes into an integer dot product, directly exploitable by SIMD: `vpdpbusd` on x86, multiply-accumulate and `vcnt` (popcount) on ARM NEON. The pipeline is branch-free and the data access pattern is sequential.

TurboQuant's non-uniform centroids break this. Each coordinate pair requires looking up a centroid value from a shared codebook, and the access pattern is data-dependent with each index selecting a different table entry. On NEON, which lacks a float gather instruction, this means scalar loads to build each vector register before the Fused Multiply-Add (FMA). Precomputing per-coordinate product tables ($d \times 2^b$ entries, amortized over all documents) doesn't help either: the FMA is relatively cheap on modern cores, so the bottleneck remains the data-dependent gather, not the arithmetic. Our benchmarks confirm this: precomputed ADC tables are no faster (and sometimes slower due to the larger working set) than inline centroid lookup.

#### Conclusion

TurboQuant is a theoretically elegant construction that builds directly on the OSQ formulation. The provable MSE bound, the unbiased inner-product estimator, and the clean data-oblivious design are real contributions. For applications requiring calibrated scores (not just rankings), or running on GPU hardware where gather operations are cheap, TurboQuant's architecture is well-motivated.

But for CPU-based vector search, the setting where Elasticsearch and most operational systems execute queries, the empirical picture is clear across all three axes:

**MSE:** TurboQuant's advantage comes from the Hadamard rotation, not the Lloyd-Max centroids. OSQ with the same rotation matches TurboQuant at 1–2 bits and comes within 1.1× at 3–4 bits. OSQ's sparse preconditioner already provides this benefit without padding overhead.

**Dot-product accuracy:** After removing ranking-irrelevant multiplicative bias, OSQ has 1.2–1.4× lower ranking noise than TQ @1-bit at small angles on zero-mean data. On shifted data, centering amplifies the advantage further: OSQ at 1-bit beats TurboQuant at 4-bit on ranking accuracy at less than 1/5 the storage.

**Throughput:** 10–40× faster symmetric scoring, with the mixed 4-1 kernel at 14 ns/doc versus TurboQuant's 293 ns/doc using NEON intrinsics. This reflects a fundamental architectural divide between integer arithmetic and lookup-table gather, not a constant factor that disappears with batching.

The uniform grid, far from being a compromise, turns out to be the right trade: it sacrifices a theoretical MSE margin that almost vanishes under equivalent rotation, and in return unlocks the integer-arithmetic pipeline that makes sub-millisecond search at scale practical.