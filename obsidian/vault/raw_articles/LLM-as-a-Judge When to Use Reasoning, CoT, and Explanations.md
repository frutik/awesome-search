---
title: "LLM-as-a-Judge: When to Use Reasoning, CoT, and Explanations"
source: "https://medium.com/data-science-collective/llm-as-a-judge-when-to-use-reasoning-cot-and-explanations-964ad82ebc3d"
author:
  - "[[Aparna Dhinakaran]]"
published: 2025-08-20
created: 2026-05-15
description: "A guide on what to use where — and why"
tags:
  - "clippings"
---
## A guide on what to use where — and why

When LLMs are used as evaluators, two design choices often determine the quality and usefulness of their judgments: whether to require explanations for decisions, and whether to use explicit chain-of-thought (CoT) prompting. Both impact not only evaluation accuracy but also the diagnostic value of the outputs.

## Explanations as signals & supervision

Requesting an explanation alongside a label changes the nature of the eval output. According to several studies, the requirement reduces variance across repeated judgments and increases agreement with human annotators. Beyond accuracy metrics, explanations expose the model's decision factors, revealing everything from systematic biases to misinterpretations of the rubric or reliance on irrelevant features.

In my experience, these explanations become high-value artifacts. They support post-hoc analysis of evaluator behavior and can be used as labeled reasoning data for retraining evaluators or improving generation models.

Explanations give you three concrete things: **stability in scoring**, **visibility into decision criteria**, and **reusable supervision signals**.

## Does explanation order matter?

If you collect both a label and an explanation, the order is a design variable. One controlled comparison showed little difference in measured accuracy between the two orders. Given the probabilistic nature of LLM decoding, putting the explanation first means the score is generated in the context of the reasoning, rather than the reasoning being shaped to fit an already-produced score.

There's no strong dataset-level evidence that order drives big changes in quality, but **explanation-first is still a reasonable default**.

## What about chain-of-thought?

Some evaluation frameworks, such as G-Eval, advocate for a Chain-of-Thought (CoT) prompting approach where the prompt includes detailed step-by-step instructions for the evaluation task. Despite wide adoption, there is little evidence to favor this CoT approach over simpler prompting strategies for NLG evaluation.

Some studies show CoT prompts only improve accuracy when the task requires multiple, complex reasoning steps. For simpler or more qualitative evaluation tasks, CoT has been shown to have either neutral or negative effects on human alignment.

Some of the improvements attributed to CoT may simply be an artifact of writing better prompts. **Avoid including generic CoT-style phrases like "think step by step," which are unlikely to add value.**

## Reasoning models change the tradeoff

Modern reasoning models perform internal deliberation and are trained to produce a hidden chain of thought before answering. Benchmarks show that reasoning-optimized models outperform their base versions on a wide variety of tasks.

These accuracy gains come at the trade-off of latency and cost. Reasoning models are slower and often consume significantly more tokens, with estimates ranging from about three to twenty times the usage of their base counterparts.

With reasoning models, **explicit CoT prompting is unnecessary** — it primarily increases token usage without improving judgment quality. Even so, generating explanations remains useful.

In most evaluation settings, the added cost and latency of reasoning-enabled models are not justified. They are best reserved for tasks that require complex multi-step reasoning or domain-specific checks.

## Practical Prompting Patterns

### A) Explanation-first, then label (recommended default for NLG)

```rb
System: You are an evaluator. Use the rubric to reason briefly, then produce a final label.

Rubric (summarization quality):
- Consistency: no contradictions with the source
- Relevance: covers central points
- Fluency: easy to read
- Conciseness: avoids unnecessary detail

Task: Evaluate the summary vs. the article on the four dimensions.
Output JSON with fields {reasoning, scores:{consistency, relevance, fluency, conciseness}, overall}.

Article: <...>
Summary: <...>