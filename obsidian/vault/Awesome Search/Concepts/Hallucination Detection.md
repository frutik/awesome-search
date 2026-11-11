---
type: concept
title: Hallucination Detection
aliases:
  - hallucination detection
  - hallucination measurement
  - groundedness
  - faithfulness evaluation
  - SelfCheckGPT
tags:
  - concept
  - llm
  - rag
  - evaluation
related_concepts:
  - "[[RAG]]"
  - "[[LLM as Judge]]"
  - "[[LLM Guardrails]]"
  - "[[Atomic Claim Verification]]"
created: 2026-09-05
---

# Hallucination Detection

## Definition

Determining whether a generated answer is supported by the evidence it was given. In a [[RAG]] system this is the *generation-side* quality question, distinct from the retrieval-side question that [[Search Evaluation]] and [[Vector Search Evaluation]] answer: retrieval can be perfect while the answer still invents.

## Families of Method

### 1. Self-consistency (no reference needed)

Sample the model several times and measure whether the samples agree — an invented fact varies across samples, a known one does not. [[Iulia Brezeanu]] benchmarked four variants:

| Method | Mechanism | Latency |
|---|---|---|
| Embedding cosine distance | all-MiniLM-L6-v2 over sampled outputs | **~0.002 s** (fastest) |
| SelfCheckGPT-BERTScore | RoBERTa-large (17 layers), MNLI-tuned | ~2 s (slowest) |
| SelfCheckGPT-NLI | DeBERTa-v3-large, entailment/contradiction/neutral | ~1 s |
| SelfCheckGPT-Prompt | gpt-3.5-turbo scores consistency 0.0–1.0 | ~0.5 s — **best performing** |

On the discriminating example, scores separated cleanly: a fabricated subject scored 0.52 (cosine) / 0.0 (prompt), a real one 0.93 / 0.95.

Evaluated on WikiBio — 238 Wikipedia topics, 1,908 annotated sentences (~40% major-inaccurate, 33% minor-inaccurate, 27% accurate), inter-annotator Cohen's κ = 0.595.

### 2. Reference-based groundedness (the RAG case)

Where retrieved passages exist, the question becomes narrower and easier: did the summary use *only* what it was given? Vectara's **Hallucination Evaluation Model (HEM)** scores exactly this, published as an open model with a public **Hallucination Leaderboard** ([[Shane Connelly]], November 2023):

| Model | Accuracy | Hallucination rate |
|---|---|---|
| GPT-4 | 97.0% | **3.0%** |
| GPT-3.5 | 96.5% | 3.5% |
| Llama 2 70B | 94.9% | 5.1% |
| Claude 2 | 91.5% | 8.5% |
| Mistral 7B | 90.6% | 9.4% |
| Google PaLM-Chat | 72.8% | 27.2% |

The PaLM-Chat row is instructive: it produced by far the longest summaries (221 words vs GPT-4's 81) and hallucinated most. Summary length and hallucination rate move together, because every additional sentence is another opportunity to exceed the evidence.

### 3. Claim-level verification (long-form answers)

Both families above give one score per answer. For long answers that hides where the problem is, because most answers mix supported and unsupported statements. [[Atomic Claim Verification]] splits the answer into single-fact claims and checks each against evidence:

- **FActScore** ([[FActScore - Fine-grained Atomic Evaluation of Factual Precision]]) checks each claim against a chosen knowledge source and reports the share supported. On biographies, ChatGPT scored 58.3% and search-augmented PerplexityAI 71.5%. Scores fell sharply for rarer people and for facts later in the answer, and PerplexityAI's citations did not track which sentences were correct.
- **SAFE** ([[Long-form Factuality in Large Language Models]]) has an LLM agent check each claim through several rounds of Google Search queries. It agreed with crowd annotators on 72% of facts and was right in 76% of the disagreements, at $0.19 per answer.

The SAFE authors draw a terminology line worth keeping. *Factuality* is agreement with established world knowledge, which is what search-based checking measures. *Hallucination*, in their usage, is disagreement with the model's own internal knowledge. In RAG terms, checking against the retrieved passages is groundedness, while checking against the web or a reference corpus is factuality. They are different questions, and an answer can pass one and fail the other.
## Why This Belongs in a Search Vault

It is the metric that closes the loop on RAG quality. Retrieval metrics like [[NDCG]] tell you the right passage was found; a groundedness score tells you it was actually used. Both are needed, and only together do they explain a bad answer.

Note the recursion: HEM and SelfCheckGPT-Prompt are themselves models judging models — the same dependency, with the same validation burden, discussed in [[LLM as Judge]].

## Related Concepts

- [[RAG]] · [[LLM as Judge]] · [[LLM Guardrails]] · [[Clean Context]]
- [[Search Evaluation]] · [[Vector Search Evaluation]] — the retrieval-side counterparts

- [[Atomic Claim Verification]] — claim-level, evidence-backed checking of long answers

## Related Tools

- [[RAGAS]] — packages these metrics for routine pipeline evaluation

## Articles

- [[How to Detect Hallucinations in LLMs]] — [[Iulia Brezeanu]]; the four-method benchmark
- [[Measuring Hallucinations in RAG Systems]] — [[Shane Connelly]]; HEM and the leaderboard

- [[FActScore - Fine-grained Atomic Evaluation of Factual Precision]] — [[Sewon Min]] et al.; atomic-fact precision against a knowledge source
- [[Long-form Factuality in Large Language Models]] — [[Jerry Wei]] et al.; SAFE, F1@K and [[LongFact]]
