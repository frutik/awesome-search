---
title: "Compositional Embeddings"
aliases: ["compositional embeddings", "compositional representation", "compositionality"]
tags:
  - concept
  - embeddings
  - representation-learning
---

# Compositional Embeddings

Embedding approaches in which the representation of a complex object is **built by combining the representations of its parts** under well-defined operations, rather than learned as an opaque whole. The goal is *compositionality*: if you know the embedding of "red" and of "car", you should be able to derive a meaningful representation of "red car".

Compositionality is hard for plain point [[Dense Embeddings|dense vectors]] — averaging or adding vectors is a crude proxy and loses structure. [[Region-Based Representation|Region representations]] are a natural fit:

- **[[Box Embedding|Boxes]]** compose via **set operations** — the intersection of two boxes approximates the conjunction of their concepts, giving a principled "AND".
- This makes box/[[Set-Theoretic Embeddings|set-theoretic]] embeddings a concrete substrate for compositional meaning (conjunction, containment).

> Note: this concept is broader than the box-embedding article that seeds it here; the link is conceptual — boxes are one well-behaved way to make embeddings compositional.

## Related Concepts
- [[Set-Theoretic Embeddings]] — composition via set operations
- [[Box Embedding]] — boxes compose through intersection
- [[Region-Based Representation]] — regions support composition; points struggle
- [[Embeddings]] — point baseline where composition is only approximate


## Articles
- [[Answering Compositional Queries with Set-Theoretic Embeddings]] — [[Shib Sankar Dasgupta]] et al.; box embeddings compose item–attribute relations via set operations to answer [[Compositional Queries|AND/OR/NOT queries]]