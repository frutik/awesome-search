---
title: "Exploring Vector Databases with Milvus"
source: "https://medium.com/@hsinhungw/exploring-vector-databases-with-milvus-dbf917d9ab00"
author:
  - "[[Henry]]"
published: 2024-02-06
created: 2026-06-01
description: "More"
tags:
  - "clippings"
---
This post introduces vector databases with Milvus, an open-source vector data management system to efficiently store and search large-scale and dynamic vector data. Our discussion will closely follow the [original paper](https://dl.acm.org/doi/pdf/10.1145/3448016.3457550).

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*Bd3M1Yqy2jMmLev8)

Photo by Joshua Sortino on Unsplash

## Background

There has been a growth in unstructured data and a rapid development of machine learning that can effectively transform unstructured data into vector embeddings for more efficient processing, analytics, and comparisons. Vector embeddings are a more compact and meaningful data representation that can capture patterns, relationships, and underlying structures.

However, due to their high-dimensional nature, traditional databases often struggle to manage vector embeddings efficiently. This led to the development of specialized vector databases, designed to handle this data type.

## Vector Databases

Vector databases are designed to efficiently store, search, and manage vector data. Each vector represents an object or item, such as a word, image, audio, or any other type of data. These databases typically focus on vector similarity search and allow users to find and retrieve similar objects quickly at scale. We will dive into an open-source vector database known as Milvus, to see how these databases work.

## Milvus

Milvus is an open-source vector data management system to efficiently store and search large-scale and dynamic vector data. It is built on top of [Facebook Faiss](https://github.com/facebookresearch/faiss), an open-source C++ library for vector similarity search. Milvus enhanced Faiss by making it faster, adding more features, and making it easier for people to use. We’ll dive into how it does this by looking at some of the improvements it brings to Faiss.

Here’s a look at what Milvus offers:

- **Query Types:** It supports versatile query types including vector similarity search, attribute filtering, and multi-vector query processing.
- **Dynamic Vector Data:** It efficiently handles dynamic vector data, such as insertions and deletions, via an LSM-based structure while providing consistent real-time searches with snapshot isolation.
- **Indexes:** It mainly supports quantization-based indexes, graph-based indexes, and an extensible interface to incorporate new indexes into the system easily.
- **Heterogeneous Computing:** It leverages the heterogeneous computing platform with both CPUs and GPUs to achieve high performance.
- **Distributed System:** It is a distributed data management system deployed across multiple nodes to achieve scalability and availability.
- **Application Interface:** It provides many application interfaces, including SDKs and RESTful APIs, that can be easily used by applications.

## System Design

![](https://miro.medium.com/v2/resize:fit:1352/format:webp/1*UB9_veJVj-as3oiAFePJKQ.png)

Figure 1: System Architecture. \[1\]

The system architecture of Milvus consists of three major components: **Query Engine**, **GPU Engine**, and **Storage Engine**.

- **Query Engine:** Supports efficient query processing over vector data and is optimized for modern CPUs by reducing cache misses and leveraging SIMD instructions.
- **GPU Engine:** A co-processing engine that accelerates performance with vast parallelism and supports multiple GPU devices for efficiency.
- **Storage Engine:** Ensures data durability and incorporates an LSM-based structure for dynamic data management. It runs on various file systems with a buffer pool in memory.

We will go over each component in detail.

## Query Engine

The query engine consists of three sub-components: query processing, indexing, and cache-aware and SIMD-aware optimizations. We will go over each in detail.

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*h9VB01aaHiV8ntSnxenF3g.png)

Figure 2: Query Engine. \[1\]

## Query Processing

In Milvus, a piece of data can be one or more vectors and optionally some numerical attributes (non-vector data), since it supports multi-vector query and attribute filtering. There are three primitive query types:

- **Vector Query:** Similarity search on a single query vector that returns the *k* most similar vectors.
- **Attribute Filtering:** A filtered vector similarity search on a single query vector that returns the *k* most similar vectors while adhering to the attribute constraints.
- **Multi-vector Query:** Similarity search on a multi-vector query that returns the *k* most similar multi-vectors according to an aggregation function between multiple vectors.

For the similarity search, Milvus supports the common similarity metrics such as Euclidean distance, inner product, cosine similarity, Hamming distance, and Jaccard distance, and it allows applications to explore the most effective approach for their use cases.

## Indexing

Indexing is extremely important for query performance. Milvus mainly supports quantization-based indexes and graph-based indexes. We will explain quantization-based indexes as they consume much less memory and are much faster to build than graph-based indexes. We will first talk about what vector quantization is:

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*a7vOoXeCF_gJ2j8kR7mFow.png)

Figure 3: Quantization Example. \[1\]

### Vector Quantization

The main idea of vector quantization is to apply a quantizer to map a vector to a code word chosen from a codebook. The K-mean clustering algorithm is commonly used to construct the codebook. In Figure 3, we have 10 vectors. After applying K-mean clustering, we have three clusters. The three cluster centroids will be the code words, and the quantizer *q* will map each vector to its closest cluster centroid.

Let’s summarize vector quantization in two steps:

1. **Codebook Generation:** Uses K-mean clustering to create a codebook, which is a set of centroid vectors (code words) for each cluster.
2. **Quantization:** The quantizer will map each vector to its closest centroid vector (code word) in the codebook.

### Quantization-based Indexes

Quantization-based indexes use two quantizers: a coarse quantizer and a fine quantizer. The coarse quantizer applies K-mean clustering to cluster the vectors into K clusters. The fine quantizer encodes the vectors within each cluster. Milvus supports [different indexes](https://milvus.io/docs/index.md#floating) for different scenarios with different tradeoffs between speed, memory, and recall. For example, index IVF\_FLAT uses the original vector representation as encoding and provides high-speed query and recall, but it requires a more expensive scan within the relevant clusters.

Next, we will discuss how query processing is done with quantization-based indexes.

Query processing of a query *q* over quantization-based indexes consists of two operations:

1. Find the closest *n\_probe* clusters based on the distance between *q* and the centroid of each cluster.
2. Search within each of the *n\_probe* relevant clusters based on different fine quantizers used.

*n\_probe* is a parameter that controls the trade-off between accuracy and performance. A higher *n\_probe* increases the accuracy as it reduces the chance of missing true results, but worsens performance as it requires more search.

The key challenge in optimizing query processing over quantization-based indexes is to quickly find the top- *k* similar vectors for a given set of queries against a collection of data vectors. In short, we want to improve the two main operations: finding the relevant clusters and searching within each relevant cluster.

We will talk about how Milvus tackles this problem next.

## Query Processing Optimizations

Milvus optimizes query processing by leveraging the heterogeneous computing platform involving both CPUs and GPUs to achieve high performance. We will discuss CPU-oriented optimization, GPU-oriented optimization, and GPU & CPU co-optimization in detail.

### CPU-oriented Optimization

CPU-oriented optimization mainly consists of cache-aware optimizations and SIMD-aware optimizations.

**Cache-aware Optimizations:** This approach reuses the accessed data vectors as much as possible to minimize CPU cache misses. It assigns threads to data vectors instead of query vectors to best leverage multi-core parallelism, as the data size is usually much larger than the query size in practice.

**SIMD-aware Optimizations:** SIMD, which stands for Single Instruction, Multiple Data,refers to hardware components that perform the same operation on multiple data operands concurrently. Milvus supports a wide range of SIMD instructions and allows for automatic SIMD instruction selection during runtime.

### GPU-oriented Optimization

GPU-oriented optimization mainly consists of support for large 𝑘 query processing in the GPU kernel and support for multi-GPU devices.

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*XWbvSgd0sbGjeKnkXv8nkA.png)

Figure 4: GPU Engine. \[1\]

**Large-k Query Processing:** To support *k* larger than 1024, which was originallylimited by shared memory,Milvus executes the query in a round-by-round fashion to cumulatively produce the final results.

**Supporting Multi-GPU Devices:** Milvus supports multiple GPU devices and allows users to select any number of GPU devices during runtime instead of compilation time.

### GPU & CPU co-optimization

In this mode, if the GPU memory is not large enough to store all the data, the challenges are to improve data transfer I/O utilization and to use the CPU when the cost of data movement outweighs the benefit of using the GPU.

In Facebook Faiss’s original implementation, the I/O bandwidth was not fully utilized as it copies data from CPU to GPU cluster by cluster. It also executes queries on the GPU even when the CPU could be faster due to data transfer overhead.

Milvus addresses these two limitations. It improves I/O utilization by copying multiple clusters if possible on the fly. It also executes queries in a hybrid manner when needed as described below:

1. If the query batch size is larger than a threshold, then all queries are executed on the GPU as the workload is more computation-intensive.
2. Otherwise, Milvus executes the queries in a hybrid manner. The first operation of query processing (finding the relevant clusters) will be done by the GPU, and the second operation (searching within each relevant cluster) will be done by the CPU.

Now that we understand how Milvus optimizes query processing by leveraging the heterogeneous computing platform, we will dive into advanced query processing including attribute filtering and multi-vector queries.

## Advance Query Processing

### Attribute Filtering

![](https://miro.medium.com/v2/resize:fit:1124/format:webp/1*NnVecR0Pz_K_vNRnzCGYeQ.png)

Figure 5: Attribute Filtering Strategies. \[1\]

Milvus implemented four attribute filtering approaches (strategies A, B, C, D) from studies in [AnalyticDB-V](https://dl.acm.org/doi/10.14778/3415478.3415541). Strategy D is a cost-based strategy that estimates the cost of the strategy A, B, and C and picks up the one with the least cost. Milvus developed a new partition-based strategy E that is faster than strategy D. We will briefly explain each strategy:

- **Strategy A:** This strategy first uses the attribute constraint to obtain relevant vectors. The relevant vectors are then fully scanned to compare against the query vector to produce the final top- *k* results. This strategy is suitable when the attribute constraint is highly selective.
- **Strategy B:** This strategy is similar to strategy A, but after attribute filtering, instead of a full scan, normal vector query processing is done on the relevant vectors to obtain the final top- *k* results. This strategy is suitable when the attribute constraint and the vector query constraint are moderately selective.
- **Strategy C:** This strategy first applies normal vector query processing to obtain relevant vectors. The relevant vectors are then fully scanned to verify if they satisfy the attribute constraint.
- **Strategy D:** This strategy is a cost-based approach that estimates the cost of strategies A, B, and C and picks the least cost strategy.
- **Strategy E:** This is a partition-based strategy that Milvus uses. The main idea is to partition the dataset based on the frequently searched attribute and apply the cost-based approach for each partition.

This shows us how Milvus improves attribute filtering performance by developing a new partition-based strategy that utilizes and improves upon the existing approaches. We will discuss multi-vector queries next.

### Multi-Vector Queries

In Multi-vector queries, we want to find the top- *k* multi-vector according to some aggregated scoring function over the similarity function of each vector. Suppose each multi-vector contains *n* vectors and we have an aggregated scoring function *g*, a similarity function *f*, and two multi-vectors *X* and *Y.* The process for computing the similarity between *X* and *Y* is outlined below.

![](https://miro.medium.com/v2/resize:fit:1344/format:webp/1*OUqc-q_g8N2dk4yhSSTZdw.png)

Milvus develops two approaches (**vector fusion** and **iterative merging**) to efficiently find the top- *k* multi-vector for different scenarios.

**Vector Fusion:**

This approach assumes that the similarity function is decomposable, such as the inner product, which applies in most cases when the underlying data is normalized.

Let *e* be any multi-vector in the dataset, each with *n* vectors. This approach stores *e* as a concatenated vector v shown below.

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*DYSNVSS9GmFTij3rVYxVHQ.png)

Let *q* be the query multi-vector. This approach applies the aggregation function *g* to the *n* vectors of *q*, producing an aggregated query vector shown below.

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*AzUHdVmByUAms6FVnlKOkg.png)

Now, apply vector query processing to find the top- *k* multi-vector using the concatenated vectors and the aggregated query vector.

Next, we will look at the second approach, iterative merging, for when the underlying data is not normalized and the similarity function is not decomposable.

**Iterative Merging:**

This approach is built on top of Fagin’s No Random Access ([NRA](https://arxiv.org/abs/cs/0204046)) Algorithm, a general technique for top-𝑘 query processing.

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*QMxBLjKZgmNjgW52Qdcg4A.png)

Figure 6: Iterative Merging. \[1\]

Let *q* be the query multi-vector and *k* be the number of results we want. Let *k’* be a variable that starts as *k*, but keeps adapting (doubling) as the algorithm progresses. Let *D* be the dataset and *D\_i* be a collection of *v\_i* of all the multi-vectors *e*.

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*Otpb09TR20lEO3BdtmOtVg.png)

The algorithm iteratively issues a top- *k’* query processing for each *q.v\_i* on *D\_i* and puts the result in *R\_i.* Then, it executes the NRA algorithm over all the *R\_i.* If *k* results can be fully determined after applying NRA on all *R\_i*, then the algorithm can stop and return the top- *k* result. Otherwise, double *k’* and run the algorithm again until *k’* reaches a threshold.

Let’s summarize what we’ve discussed so far:

- **Query types:** The basics of vector similarity search, attribute filtering, and multi-vector query processing
- **Indexing:** Vector quantization and quantization-based indexes using coarse quantizer and fine quantizer.
- **Query processing optimization:** Leveraging the heterogeneous computing platform that involves both CPUs and GPUs to achieve high performance.
- **Advance query processing:** A partition-based strategy forattribute filtering. Vector fusion and iterative merging for multi-vector query processing

Next, we will look at the Storage Engine, particularly dynamic data management.

## Storage Engine

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*FeNKMkVu_5pShIlejWYhJg.png)

Figure 7: Storage Engine. \[1\]

The storage engine mainly consists of data segments, a buffer pool manager, and multi-storage, which we will discuss next.

### Data Segment

Milvus supports dynamic vector data through insertions and deletions. It uses a log-structured merge-tree (LSM) structure to first store newly inserted data in memory and then flush to disk as an immutable segment once the accumulated size reaches a threshold. Smaller segments are merged into larger ones for fast sequential access. Deleted data are removed during segment merges.

### Buffer Pool Manager

Most data and indexes are kept in memory for high performance. If not, the storage engine uses a LRU-based buffer manager to cache segments.

### Multi-Storage

Milvus supports multiple file systems including local file systems, Amazon S3, and HDFS for the underlying data storage.

## System Implementation

### Asynchronous Processing

Milvus improves throughput with asynchronous processing, where write operations are consumed and indexes are built asynchronously. Milvus provides an API flush() that blocks all incoming requests until the system finishes processing all the pending operations.

### Snapshot Isolation

Milvus ensures snapshot isolation to maintain a consistent view for reads and writes since it supports dynamic data management. Every query operates on the snapshot available at the query’s start, and subsequent updates generate new snapshots without interfering with the ongoing queries.

### Distributed System

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*ZchWLNV92PP45FytcpTc7g.png)

Figure 8: Milvus Distributed System. \[1\]

Milvus is a distributed system that supports data management across multiple nodes. The overall architecture consists of three layers.

- **Coordinator layer:** The coordinator layer maintains the metadata such as sharding and load-balancing information.
- **Computing layer:** Managed by Kubernetes, this layer processes user requests. It has asingle writer to handle data insertions, deletions, and updates, and ensures atomicity with a write-ahead log (WAL). It has multiple readers to process user queries, which auto-scales based on the load. Data is sharded among the readers with consistent hashing and caches data locally to minimize frequent access to the storage layer.
- **Storage layer:** The shared storage layer utilizes Amazon S3 for its high availability.

## References

- \[1\] [Milvus: A Purpose-Built Vector Data Management System](https://doi.org/10.1145/3448016.3457550). In Proceedings of the 2021 International Conference on Management of Data (SIGMOD ‘21). Association for Computing Machinery, New York, NY, USA, 2614–2627.