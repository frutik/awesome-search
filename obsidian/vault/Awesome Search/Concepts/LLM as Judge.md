---
type: concept
title: "LLM as Judge"
aliases: ["LLM judge", "LLM-as-a-judge", "automated relevance evaluation", "LLM evaluation"]
tags:
  - concept
  - search-evaluation
  - llm
  - automation
created: 2026-05-16
---

# LLM as Judge

## Definition

Using a large language model (LLM) to evaluate the relevance of search results — as a cheaper, faster alternative to human annotators for creating [[Judgment Lists]] or running automated quality checks.

## Why LLM Judges?

Human annotation for [[Search Evaluation]] is expensive:
- Typical cost: $0.50–$5.00 per (query, document) judgment
- For 1,000 queries × 10 candidates each = $5,000–$50,000
- Turnaround time: days to weeks

LLM judgment:
- Cost: ~$0.001–$0.01 per judgment (100–1000x cheaper)
- Turnaround: minutes
- Scalable: run continuously as part of CI/CD

## How It Works

### Point-wise Scoring
Rate each (query, document) pair independently:
```python
def llm_judge_relevance(query, document, llm):
    prompt = f"""Rate the relevance of this document to the query on a scale of 0-3:
    
    Query: {query}
    Document: {document}
    
    0 = Not relevant
    1 = Marginally relevant  
    2 = Relevant
    3 = Highly relevant
    
    Return only the integer grade."""
    
    return int(llm.generate(prompt))
```

### Pairwise Comparison (Stronger Signal)
Ask the LLM which of two documents is more relevant:
```python
def llm_compare(query, doc_a, doc_b, llm):
    prompt = f"""Which document is more relevant to this query?
    Query: {query}
    Document A: {doc_a}
    Document B: {doc_b}
    Answer: A or B"""
    return llm.generate(prompt)
```
Pairwise comparison is generally more reliable than absolute scoring.

### Nugget-Based Evaluation
LLM first identifies "answer nuggets" (key facts needed to answer the query), then checks which retrieved documents contain them.

## Vespa's LLM Judge for Retrieval

Vespa's blog post demonstrates using an LLM to evaluate first-stage retrieval quality:
1. For each query, generate an "ideal answer" with the LLM
2. Judge retrieved documents: does this document contain information needed for the ideal answer?
3. Aggregate to compute system-level NDCG approximation

Key result: LLM judgments correlate well (Spearman's ρ ≈ 0.85–0.90) with human judgments for factual queries.

## Limitations

1. **Positional bias**: LLMs prefer the first document presented
2. **Length bias**: LLMs often favor longer documents
3. **Self-citation bias**: LLMs may prefer documents stylistically similar to their training data
4. **Hallucination**: LLM may recall facts not in the document and rate it highly
5. **Calibration**: absolute scores are unreliable; relative pairwise comparisons are better
6. **Cost at scale**: even cheaper than humans, still non-trivial at millions of judgments

## The Economics Problem

Limitation 6 above deserves its own treatment, because it is the constraint that decides whether an LLM judge is a research demo or a production system.

Per-judgment cost is only cheap relative to humans. At e-commerce scale — billions of annual searches, hundreds of billions of query-document pairs — judging everything with a frontier model is not expensive, it is impossible. Most teams respond by **sampling**: judge a few thousand pairs and generalize. That is adequate for tracking aggregate quality and inadequate for anything requiring coverage, such as mining [[Hard Negative Mining|hard negatives]] across a full catalogue or catching per-query regressions in the tail.

The architectural answer is [[Staged Judging]]: prune the pair space with [[Implicit Judgments|behavioral signals]], let cheap quantized judges settle the easy majority, escalate only disagreement to the LLM, and [[Knowledge Distillation|distill]] the LLM's judgments into a small production model. See [[Towards Scalable Relevance Engineering]] for a worked implementation.

Note that this is an axis **orthogonal to judge quality**. Most of the literature — and most of the articles below — optimizes how closely a judge agrees with humans. A 95%-accurate judge you cannot afford to run produces no judgments at all, which is strictly worse than a 90% judge with full catalogue coverage.

## Best Practices

- Use **pairwise** comparisons, not point-wise scoring
- Run multiple LLM calls per judgment and take majority vote
- Validate on a small set of human judgments before trusting LLM judges
- Use a capable LLM (GPT-4, Claude) — cheaper models have significantly worse calibration

## Related Concepts

- [[Pointwise Relevance Evaluation]] — score each item independently; simplest LLM judge pattern
- [[Pairwise Relevance Evaluation]] — LHS/RHS comparison; stronger signal than pointwise
- [[Listwise Relevance Evaluation]] — rank full candidate list; most holistic
- [[Judgment Lists]] — what LLM judges help create
- [[Search Evaluation]] — where LLM judgments are used
- [[NDCG]] — metric computed from LLM-generated grades
- [[RAG]] — LLM judge also used for RAG faithfulness/relevancy evaluation
- [[Agentic Search]] — LLM verification step is a form of LLM judgment
- [[Semantic Relevance]] — the intent-based signal LLM judges are used to scale, alongside engagement-based relevance

## People
## Articles

- [[LLM-as-a-Judge When to Use Reasoning CoT and Explanations]] — [[Aparna Dhinakaran]]; explanation-first pattern; CoT has mixed evidence


- [[Jo Kristian Bergum]] — Vespa "Improving retrieval with LLM-as-a-judge"
- [[Daniel Tunkelang]] — traditional human judgment advocate; acknowledges LLM judges


## Articles

- [[Using LLMs to Amplify Human Labeling and Improve Dash Search Relevance]] — [[Dmitriy Meyerzon]]; LLM calibrated on human labels → 100x scale-up; DSPy for prompt optimization; context-aware evaluation with tool use
- [[Search Quality Assurance with AI as a Judge]] — [[Tao Ruangyam]]; Zalando production pipeline; NER-clustered test queries; GPT-4o; ~$250/run for 1,500 segments × 25 results; pre-launch market validation
- [[Classic ML to Cope with Dumb LLM Judges]] — [[Doug Turnbull]]; per-attribute LLM signals as ML features → decision tree; 96.7% precision on 40% of pairs
- [[Automating Search Relevance Assessment at Scale with LLM-as-a-Judge]] — [[Joanna Marhula]], [[Mateusz Sidor]]; Allegro's RAT framework; 380K+ multilingual judgment dataset; few-shot examples hurt accuracy; migration to local Gemma judge cut inference cost 60%
- [[How Etsy Uses LLMs to Improve Search Relevance]] — [[Yuqing Zhang]], [[Congzhe Su]], [[Susan Liu]]; LLM annotator anchored to human golden labels, scaled via a three-tier [[Knowledge Distillation|distillation]] cascade into a real-time production judge

## People

- [[Dmitriy Meyerzon]]
- [[Tao Ruangyam]]
- [[Doug Turnbull]]
- [[Joanna Marhula]]
- [[Mateusz Sidor]]
- [[Yuqing Zhang]]
- [[Congzhe Su]]
- [[Susan Liu]]
