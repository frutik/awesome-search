---
type: person
title: Doug Turnbull
aliases:
  - Turnbull
  - softwaredoug
tags:
  - person
  - search-practitioner
  - search-researcher
created: 2026-05-15
---

# Doug Turnbull

Co-founder of OpenSource Connections (OSC); currently independent (previously [[Shopify]], then [[Reddit]]); co-author of *Relevant Search* (O'Reilly). Search relevance consultant and practitioner; author of the Softwaredoug blog.

## Known For
- *Relevant Search* book (with John Berryman)
- Bayesian BM25 (BB25) — calibrated BM25 probabilities for principled hybrid fusion
- Practical Elasticsearch relevance tuning
- "What is Relevant?" — task-centered definition of relevance

## Articles
- [[What is Presentation Bias in Search]]
- [[What AI Engineers Should Know about Search]]
- [[Bayesian BM25 is Cool]]
- [[What is a Relevant Search Result]]
- [[Practical BM25 - The Effect of k1 and b]]

- [[Semantic Search Without Embeddings]]
- [[Finding the Relevance Cutoff - When to Stop Showing Search Results]]

- [[Getting Started on Search Relevance for the Understaffed Search Team]]

- [[Principal Component Analysis - an embedding shrink-ray]] — PCA for embedding compression; measured recall vs. dimensions on [[MS MARCO]]

- [[Just brute force your embeddings]] — measured NumPy scan throughput on 384-dim vectors; the case against adopting a vector database at ~1m documents

- [[Updating a Vector Database Is No Simple Thing]] — tombstoning, segmented graphs, and vendor-by-vendor comparison of how HNSW indexes handle updates/deletes

## Talks & Videos
- [[Haystack US 2022 - Bayesian Optimization of Relevance at Shopify]] — with [[Andy Toulis]]; [[Bayesian Optimization]] as a lightweight halfway point to [[Learning to Rank]], with a concrete Shopify BM25 `b`/`k1` retuning case study

## Topics
- [[Tuning BM25 for E-commerce Search]]

## Affiliations

- Independent (current)
- [[Reddit]] (former)
- [[Shopify]] (former)

## Teaching
- [[Courses]] — teaches *Cheat at Search Essentials* (free intro), co-teaches *AI-Powered Search* with [[Trey Grainger]], and teaches *Build your own vector database* (https://maven.com/softwaredoug/vectordb)

## Key Concepts
- [[BM25]]
- [[Hybrid Search]]
- [[Learning to Rank]]
- [[Search Evaluation]]
- [[Judgment Lists]]
- [[Bayesian Optimization]]

## Affiliations
- OpenSource Connections (OSC) — Doug co-founded it but has since left (later [[Shopify]], now independent); also former org of [[Max Irwin]] (now at [[Bonsai]])
- [[Can BM25 be a Probability]] — BB25 framework; calibrating BM25 as probability for principled hybrid fusion
- [[Metadata - The 3rd Kind of Retrieval]] — attribute-based retrieval as a third paradigm beyond lexical + embeddings
- [[Classic ML to Cope with Dumb LLM Judges]] — combining many dumb LLM judges via decision tree to improve precision
- [[Don't Classify, Hallucinate]] — hypothetical classifications: let a cheap LLM invent a category, resolve it into the real taxonomy by embedding similarity; see [[Query Classification]]
- [[Agentic search models]] — the case for [[Purpose-Built Agentic Search Models]] for "the last 20%"; see topic [[Frontier of Search 2026]]
