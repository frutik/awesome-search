---
title: "Synthetic Query Generation"
type: concept
aliases:
  - Synthetic Training Data
  - Query Generation
  - LLM-Generated Queries
  - Instruction Prompting for Query Generation
tags:
  - concept
  - synthetic-data
  - llm
  - training-data
  - zero-shot
  - retrieval
created: 2026-07-30
---

# Synthetic Query Generation

Using a generative model to invent the queries you don't have: point an LLM at each document in
your corpus and ask *"what would someone search for to find this?"* The output is a labeled
query–document pair, which is exactly what a ranking model needs and exactly what most domains
lack.

It is the practical escape from the bind described in [[Zero-Shot Retrieval]]. In-domain
fine-tuning is the biggest lever on retrieval quality, but it requires labels; nobody has labels
for their own catalogue; so almost everyone deploys models out-of-domain and accepts the loss.
Synthetic generation manufactures the missing ingredient instead of doing without it.

---

**Not the same as Doc2Query.** Doc2Query also predicts queries for documents, but consumes them at
*indexing* time — the predicted queries are appended to the document so a lexical matcher can find it,
making it a document-expansion technique. Here the generated queries are *training data* for a ranking
model and never enter the index.

## The Pipeline

```
corpus documents
   → instruction prompt + k labeled examples → synthetic queries
   → filter (see Consistency Filtering)
   → sample negatives (see Hard Negative Mining)
   → train ranking model
```

Four properties make this affordable:

- **Generation is offline.** The LLM never sits in the query path — it runs once over the corpus.
  This is what allows a billion-parameter generator to feed a model small enough to serve.
- **Only a handful of human labels are needed.** The examples in the prompt are the entire
  labeling budget.
- **Coverage can be partial.** You do not need a query for every document.
- **The output is distilled away.** What ships is a small ranking model, not the generator —
  see [[Knowledge Distillation]].

## Prompt Wording Is Load-Bearing

The most transferable finding in
[[Improving Search Ranking with Few-Shot Prompting of LLMs]] is not the architecture but a
sentence. The instruction included **"The query must be specific and detailed"**; earlier
iterations without it produced overly generic queries. One clause in the prompt separated usable
training data from unusable.

The reason is that a generic query — "coronavirus" against a corpus of coronavirus papers —
carries no discriminative signal. Every document is a plausible answer, so the pair teaches the
ranker nothing. What the instruction is really requesting is [[Query Specificity]].

## Measured Example

From [[Improving Search Ranking with Few-Shot Prompting of LLMs]] on [[TREC-COVID]]:

| Stage | Figure |
|---|---|
| Generator | flan-t5-xl, 3B parameters ([[FLAN-T5]]) |
| Human-labeled examples in prompt | **3** |
| Documents given a synthetic query | 33,099 of 171K (~19%) |
| Pairs surviving [[Consistency Filtering]] | 14,156 (43%) |
| Negatives per query | 2, sampled from the retrieved top-100 |
| Trained model | 22M-parameter [[Cross-Encoder|cross-encoder]], 2 epochs |
| Result | **80.2 nDCG@10** vs 76.0 zero-shot hybrid, 70.0 BM25 |
| Generation cost | A100 40GB, ~$1/hour, ~3,600 queries/hour |

Three labeled queries bought four nDCG points over an already-strong hybrid baseline. It also beat
[[PROMPTAGATOR]]'s reported 76.2 on the same dataset, which used a 137B generator — evidence that
generator scale is not the binding constraint once the prompt and the filter are right.

## Where the Quality Risk Sits

Generated queries are not free of problems, they just have *different* problems than click logs:

| Source of labels | Characteristic failure |
|---|---|
| Clicks / [[Implicit Judgments]] | [[Presentation Bias]]; survivorship bias — only queries that already worked are observed |
| Human judgments | Expensive, slow, inconsistent between annotators |
| Synthetic queries | Generic or trivially answerable queries; the LLM's idea of a question rather than a user's |

The last row is why a filter is mandatory rather than optional. Left unfiltered, a synthetic set
teaches a ranker to satisfy the generator's query distribution — which may be nothing like the real
one. [[Consistency Filtering]] is the standard defence.

A second caution carried over from [[Zero-Shot Retrieval]]: a model tuned on one domain's synthetic
data is a model tuned for that domain. The worked example of domain tuning cutting both ways is
[[Fine-Tuning Sparse Embeddings for E-Commerce Search]].

## Related Uses in the Vault

Query generation shows up well beyond ranker training:

- [[qdrant-sparse-finetune]] — synthetic query generation routed through `litellm` as a step in
  [[SPLADE]] fine-tuning on a product catalogue
- [[LLM-Powered Query Extraction for Autocomplete]] — [[David Albrecht]]; generated queries as the
  cold-start fix for [[Autocomplete]], where there is no query log yet
- [[Qwen3 Embedding Series]] · [[Fine-Tuning Qwen3 Embeddings for Product Category Classification]] —
  synthetic pairs as the weak-supervision pre-training stage of an embedding model
- [[Hypothetical Document Embeddings]] — the inverse operation: generate a *document* from a query
  at search time rather than a query from a document offline

## Related Concepts

- [[Consistency Filtering]] — the quality gate that makes generated data usable
- [[Zero-Shot Retrieval]] — the problem this solves; "synthetic in-domain labels" as one rung of its cost ladder
- [[Embedding Fine-tuning]] — what the generated data is consumed by
- [[Hard Negative Mining]] — the other half of a training triplet
- [[Knowledge Distillation]] — large generator to small server-side model
- [[Judgment Lists]] — what synthetic pairs substitute for
- [[LLM as Judge]] — the sibling technique: LLMs producing *relevance labels* rather than *queries*
- [[Query Specificity]] — the property a good generation prompt demands
- [[Query Expansion]] — a different use of generated text, at query time rather than training time
- [[FLAN-T5]] — an open generator with a licence that permits this

## Articles

- [[Improving Search Ranking with Few-Shot Prompting of LLMs]] — [[Jo Kristian Bergum]] ([[Vespa]]);
  the vault's primary end-to-end account, with released notebooks and data
- [[LLM-Powered Query Extraction for Autocomplete]] — [[David Albrecht]]; the autocomplete cold-start case

## People

- [[Jo Kristian Bergum]] — the TREC-COVID pipeline and released artifacts
- [[David Albrecht]] — synthetic query datasets for autocomplete cold start
