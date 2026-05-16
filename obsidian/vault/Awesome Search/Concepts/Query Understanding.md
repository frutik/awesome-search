---
title: "Query Understanding"
aliases: ["query analysis", "query interpretation", "QU", "query processing"]
tags:
  - concept
  - query-understanding
  - search
  - nlp
---

# Query Understanding

## Definition

Query understanding is the process of analyzing a user's search query to determine what they actually want — their intent, the entities they're referencing, the context of their search, and how to best translate their natural-language input into a retrieval strategy.

[[Daniel Tunkelang]] defines it as "the bridge between natural language and the formal query language of the retrieval system."

## Three Components (Tunkelang's Framework)

Tunkelang divides query understanding into three parts:

### 1. Query Formulation Analysis
What did the user type, and how should it be parsed?
- **Spelling correction**: "iphne" → "iphone"
- **Tokenization**: splitting compound terms
- **Stemming/lemmatization**: "running shoes" → stem "run"
- **[[Query Segmentation]]**: "new york times" → ["new york", "times"] vs. ["new", "york", "times"]

### 2. Query Intent Classification
What is the user trying to accomplish?
- **[[Search Intent]]**: navigational, informational, transactional
- **Domain classification**: is this a medical, legal, or general query?
- **Ambiguity detection**: "python" → programming language vs. snake

### 3. Query Contextualization  
What additional context modifies the query's meaning?
- **Personalization**: user's previous behavior, preferences
- **Location**: "restaurants near me"
- **Session context**: previous queries in this session
- **Temporal**: "latest iphone" means different things over time

## Why Query Understanding Matters

Search systems optimized only for retrieval fail when:
- Query misspelled (lexical retrieval gets nothing)
- Query too broad/ambiguous (wrong intent served)
- Query uses shorthand or slang the index doesn't contain
- Query is a compound concept the system doesn't decompose

Good query understanding multiplies the value of any retrieval system.

## Methods

| Technique | Component | Approach |
|-----------|-----------|---------|
| Spelling correction | Formulation | Edit distance, language model |
| NER | Formulation | BERT-based sequence labeling |
| Intent classification | Intent | Fine-tuned classifier |
| Query expansion | Intent | Thesaurus, embedding neighbors |
| Rewriting | All three | Seq2seq model, T5 |

## AI/LLM for Query Understanding

[[Daniel Tunkelang]]'s "AI for Query Understanding" argues that LLMs fundamentally change query understanding:
- LLMs can perform all three components in one pass
- Few-shot prompting enables rapid adaptation to new domains
- Conversational context is natively handled

## Relation to [[Agentic Search]]

In [[Agentic Search]], the agent performs query understanding in a loop:
1. Understand initial query
2. Execute retrieval
3. Re-understand query given retrieved evidence
4. Reformulate and re-retrieve

This makes query understanding dynamic rather than a static preprocessing step.

## Related Concepts

- [[Search Intent]] — component of QU
- [[Query Segmentation]] — component of QU
- [[Query Types]] — taxonomy of user queries
- [[Agentic Search]] — dynamic query understanding
- [[Semantic Search]] — benefits from good query understanding
- [[Bag-of-Documents Model]] — probabilistic framing of query intent

- [[Query Relaxation]] — loosening constraints when results are too few

## People
## Articles

- [[Semantic Search Without Embeddings]] — [[Doug Turnbull]]; taxonomy-based; hierarchical tokenizer + BM25; LLMs for classification
- [[Superintelligent Retrieval Agent SIRA]] — LLM-enriched BM25; corpus enrichment + query expansion; beats agentic RAG on BEIR
- [[Incremental AI Adoption for E-commerce Search]] — 4 levels from traditional to conversational AI


- [[Daniel Tunkelang]] — primary authority; queryunderstanding.com; extensive series

- [[Semantic Equivalence of e-Commerce Queries]]
- [[Affordances for Conversational Search]]
- [[Search Query Expansion with Query Embeddings]]
