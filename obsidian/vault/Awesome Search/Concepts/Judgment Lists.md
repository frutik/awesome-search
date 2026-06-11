---
title: "Judgment Lists"
aliases: ["relevance judgments", "qrels", "annotation lists", "relevance labels", "judgment list"]
tags:
  - concept
  - search-evaluation
  - annotation
---

# Judgment Lists

## Definition

A judgment list (also called "qrels" in IR — short for "query relevance") is a dataset of (query, document, relevance_grade) triples created by human annotators. Judgment lists are the foundation of offline [[Search Evaluation]].

## Structure

```
query_id | doc_id | grade | notes
---------|--------|-------|------
q001     | d042   | 3     | "Highly relevant - directly answers query"
q001     | d117   | 1     | "Marginally relevant - tangential"
q001     | d203   | 0     | "Not relevant"
q002     | d088   | 4     | "Perfect match"
```

Grades typically follow a 0–4 scale aligned with [[NDCG]] relevance levels.

## Creating Judgment Lists

### Annotation Process
1. **Query sampling**: select representative queries ([[Sampling Strategies]])
2. **Candidate retrieval**: run query through current system(s) to get candidate documents
3. **Annotator assignment**: multiple annotators per query (compute inter-annotator agreement)
4. **Guidelines**: detailed rubric specifying what each grade means
5. **Adjudication**: resolve disagreements (voting, expert review)

### Annotation Guidelines Matter
Vague guidelines → noisy labels → misleading metrics.

Good guidelines:
- Define relevance for your specific domain (e-commerce: in-stock, correct size? news: recency matters?)
- Provide examples for each grade
- Handle ambiguous cases explicitly

### Inter-Annotator Agreement
Measure consistency with Cohen's Kappa or Krippendorff's Alpha:
- κ > 0.8: excellent agreement
- κ 0.6–0.8: good
- κ < 0.6: guidelines need revision

## Sampling Strategies

How you sample queries determines what the judgment list measures:

| Strategy | Description | Use case |
|----------|-------------|---------|
| Random | Uniform sample from query log | General coverage |
| Stratified | Sample by query type/frequency | Ensure rare queries covered |
| PPS (probability proportional to size) | Sample proportional to traffic volume | Focus on high-impact queries |
| Adversarial | Deliberately hard or edge-case queries | Stress testing |

## Pooling

For large corpora it's infeasible to judge all documents. **Pooling**: run multiple systems, collect top-K from each, judge the union.
- Documents outside the pool are treated as "unjudged" (not "irrelevant")
- Unjudged docs can bias evaluation against new systems that retrieve non-pooled docs

## Tools

- **Quepid** (OpenSource Connections): web UI for managing judgments, computing NDCG
- **LabelStudio**: general annotation platform, used for search judgments
- **TREC**: standardized qrel format (widely used in academic IR)

## LLM-Generated Judgments

An alternative to human annotation: use an LLM to rate relevance. Cheaper but less reliable for nuanced cases. See [[LLM as Judge]].

## Public Judgment List Datasets

Instead of building from scratch, teams can bootstrap evaluation using publicly released annotation datasets:

| Dataset | Domain | Label scheme | Notes |
|---|---|---|---|
| [[Amazon ESCI Dataset]] | E-commerce | 4-class (Exact/Substitute/Complement/Irrelevant) | Large-scale; multi-locale |
| [[ESCI-S Dataset]] | E-commerce | 4-class + enriched metadata | Community extension of ESCI |
| [[WANDS Dataset]] | Home goods (Wayfair) | 3-class (Exact/Partial/Irrelevant) | ~42K pairs; vertical domain |
| [[Home Depot Product Search Relevance]] | Home improvement | Continuous 1–3 | Crowdsourced; Kaggle competition |

These datasets are useful for: initial model benchmarking, transfer learning baselines, and calibrating in-house annotation guidelines against established community standards.

## Related Concepts

- [[NDCG]] — primary metric using judgment lists
- [[MRR]] — uses binary judgments from list
- [[Search Evaluation]] — how judgment lists feed into evaluation
- [[LLM as Judge]] — automated alternative
- [[Implicit Judgments]] — behavioral (click-derived) counterpart to explicit judgments
- [[Sampling Strategies]] — how queries are selected for judgment

## People

- [[Daniel Tunkelang]] — "Evaluating Search: Using Human Judgments"
- [[Doug Turnbull]] — "What Is a Judgment List?"; Quepid co-creator
- [[James Rubinstein]] — human approach to measuring search

- [[What is a Relevant Search Result]]
- [[Setting Up a Relevance Evaluation Program]]
