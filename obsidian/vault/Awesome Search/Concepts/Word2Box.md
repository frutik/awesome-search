---
title: "Word2Box"
aliases: ["Word2Box", "word2box"]
tags:
  - concept
  - embeddings
  - region-based-embeddings
  - box-embedding
  - nlp
---

# Word2Box

An **unsupervised** method (Dasgupta et al., ACL 2022, *Word2Box: Capturing Set-Theoretic Semantics of Words using Box Embeddings*) that learns a [[Box Embedding]] for every word directly from a text corpus — no hierarchy supervision required. It is, in effect, **[[Word2Vec]] with boxes**: the CBOW training scheme is reused, but a word is a box and similarity is the **volume of box intersection** (computed with the Gumbel-box machinery) instead of a vector dot product.

## How It Trains

1. Pick a **center word** from the corpus.
2. Collect **context words** within a **window size** around it (CBOW-style sampling, following Mikolov et al., 2013).
3. Convert center and context words to boxes; **increase the overlap** between center-box and context-boxes.
4. To avoid the degenerate "make every box huge" solution, draw **negative-sampled** words and **decrease** their overlap with the context boxes.

Overlap is the **intersection volume of [[Box Embedding|Gumbel boxes]]**, which keeps gradients well-behaved.

## Evaluation

- **Setup:** 64-dim Word2Box vs. 128-dim Word2Vec — a fair comparison on parameter count, since a box stores two corners (start + end) per dimension. ~900M words of preprocessed English, 10 epochs.
- **Word similarity:** measured by Spearman rank correlation against human-annotated pairs on benchmarks such as **SimLex-999**. Word2Box generally **surpasses Word2Vec**, with the largest gains where rare words are involved.
- **Set-theoretic / collective operations:** quantitative and qualitative tests show boxes handle **polysemy** and "strict meaning" better than point methods like Word2Vec.

## Why Boxes Beat Points Here

A point vector collapses all senses of a polysemous word into one location. A box can stretch to cover multiple senses and supports **[[Set-Theoretic Embeddings|set operations]]** — intersecting two word boxes approximates the conjunction of their meanings.

## Related Concepts
- [[Box Embedding]] — the representation Word2Box learns (Gumbel-box variant)
- [[Word2Vec]] — the CBOW/skip-gram method Word2Box mirrors
- [[Set-Theoretic Embeddings]] — semantics Word2Box is designed to capture
- [[Region-Based Representation]] — the broader family
- [[Embeddings]] — point-vector baseline

## Articles
- [[Express Words in a Box - Understanding Box Embedding from the Basics]] — [[Shun Tsukagoshi]]; ends at Word2Box

## People
- [[Shib Sankar Dasgupta]] — lead author of Word2Box (and Gumbel Box)
- [[Tomas Mikolov]] — Word2Vec / CBOW, the training scheme Word2Box reuses
