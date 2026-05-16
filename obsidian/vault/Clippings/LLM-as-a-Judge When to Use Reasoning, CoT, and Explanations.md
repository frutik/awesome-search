---
title: "LLM-as-a-Judge: When to Use Reasoning, CoT, and Explanations"
source: "https://medium.com/data-science-collective/llm-as-a-judge-when-to-use-reasoning-cot-and-explanations-964ad82ebc3d"
author:
  - "[[Aparna Dhinakaran]]"
published: 2025-08-20
created: 2026-05-16
description: "A guide on what to use where — and why"
tags:
  - "clippings"
---
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*I9SFp_UJ4MmwrpydkyHOLg.png)

Image by author

## A guide on what to use where — and why

*My thanks to* [*Elizabeth Hutton*](https://www.linkedin.com/in/elizabeth-hutton/) *and* [*Sri Chavali*](https://www.linkedin.com/in/srilakshmi-chavali/]) *for their contributions to this piece*

When LLMs are used as evaluators, two design choices often determine the quality and usefulness of their judgments: whether to require explanations for decisions, and whether to use explicit chain-of-thought (CoT) prompting. Both impact not only evaluation accuracy but also the diagnostic value of the outputs.

## Explanations as signals & supervision

Requesting an explanation alongside a label changes the nature of the eval output. According to [several](https://doi.org/10.48550/arXiv.2310.05657) [studies](https://doi.org/10.48550/arXiv.2306.05685), the requirement reduces variance across repeated judgments and increases agreement with human annotators. Beyond accuracy metrics, explanations expose the model’s decision factors, revealing everything from systematic biases to misinterpretations of the rubric or reliance on irrelevant features.

In my experience, these explanations become high-value artifacts. They support post-hoc analysis of evaluator behavior and can be used as labeled reasoning data for retraining evaluators or improving generation models. For example, an explanation might reveal that a judge is systematically penalizing long answers for verbosity, a pattern that would be hidden in the raw scores.

In short, explanations give you three concrete things: stability in scoring, visibility into decision criteria, and reusable supervision signals. Without them, judgments are opaque and harder to debug or improve.

More on each below.

1. *Human agreement and stability:* Strong models already correlate well with human preferences in open‑ended evaluation, and structured prompts that elicit brief reasoning and criteria often push correlations higher.
2. *Diagnostics you can act on:* Explanations surface the features a judge is rewarding or penalizing. That makes it easier to spot known LLM-judge pathologies such as position bias, verbosity bias, and self‑preference bias, then apply mitigations like position swapping or calibration.
3. *Reusable supervision:* Short, criterion‑tethered explanations can be mined to refine prompts or fine‑tune specialized evaluators. [Recent surveys](https://doi.org/10.48550/arXiv.2506.13639) and consistency studies emphasize that evaluator reliability depends as much on prompt structure and criterion granularity as on the base model

Once you decide to include explanations, the next choice is typically sequencing: should the model explain before producing the label, or the other way around?

## Does explanation order matter?

If you collect both a label and an explanation, the order is a design variable. One [controlled comparison](https://arxiv.org/abs/2310.05657) showed little difference in measured accuracy between the two orders. Given the probabilistic nature of LLM decoding, putting the explanation first means the score is generated in the context of the reasoning, rather than the reasoning being shaped to fit an already-produced score.

Some teams use function or tool calling to capture explanations and labels as structured fields. This removes parsing issues, but it is still unclear whether applying the same evaluation templates through a tool definition produces distributions of results that match free-text prompting. Early observations suggest the difference is small, though systematic studies are limited. There’s no strong dataset-level evidence that order drives big changes in quality, but explanation-first is still a reasonable default. It lines up with how we expect the model to generate more consistent, grounded outputs, and it’s easy to standardize across evaluation runs.

There’s no strong dataset-level evidence that order drives big changes in quality, but explanation-first is still a reasonable default. It lines up with how we expect the model to generate more consistent, grounded outputs, and it’s easy to standardize across evaluation runs.

## What about chain-of-thought?

Some evaluation frameworks, [such as G-Eval](https://arxiv.org/abs/2303.16634), advocate for a Chain-of-Thought (CoT) prompting approach where, in addition to evaluation criteria, the prompt includes detailed step-by-step instructions for the evaluation task. Despite wide adoption, there is little evidence to favor this CoT approach over simpler prompting strategies for NLG evaluation. In fact, research into the effectiveness of CoT prompting is [largely mixed](https://arxiv.org/abs/2508.01191).

Some studies show CoT prompts only improve accuracy when the task requires multiple, complex reasoning steps. In the medical domain, [one study](https://doi.org/10.1016/j.compbiomed.2025.110614) comparing CoT-based prompts to simpler approaches reported higher factual accuracy in a question-answering context. If the job involves multi-step factual checks such as cross-referencing several claims against a source, or reasoning across linked evaluation criteria, explicit reasoning steps may be worth a try. For example, CoT may be helpful for evaluating agent tool calling, where the judgement requires reasoning over the context, a list of available tools, and the tool parameters.

For simpler or more qualitative evaluation tasks, CoT has been shown to have either neutral or negative effects on human alignment. The additional structure can also increase prompt complexity and cost, which matters in large-scale evaluations.

Some of the improvements attributed to CoT may simply be an artifact of writing better prompts. For that reason, we recommend investing the time to write clear, detailed instructions. Avoid including generic CoT-style phrases like “think step by step,” which are unlikely to add value.

## Reasoning models change the tradeoff

Modern reasoning models perform internal deliberation and are trained to produce a hidden chain of thought before answering. In OpenAI models, this internal reasoning is not accessible, while Anthropic provides an option to view extended reasoning traces through their API. Benchmarks [show](https://arxiv.org/html/2505.10543v2) that reasoning-optimized models outperform their base versions on a wide variety of tasks such as multi-hop QA, code generation, and structured problem solving.

These accuracy gains come at the trade-off of latency and cost. Reasoning models are slower and often consume significantly more tokens, with estimates ranging from about three to twenty times the usage of their base counterparts. In our own notebook runs, this overhead was clear in both latency and cost, which makes selective use important for large-scale evaluations.

With reasoning models, explicit CoT prompting is unnecessary — it primarily increases token usage without improving judgment quality. Even so, generating explanations remains useful. Whether the model is reasoning internally or producing CoT in the prompt, explanations are valuable artifacts for auditing decisions, detecting bias, and refining evaluation setups. For that reason, we recommend requesting explanations as part of the output regardless of model type.

In most evaluation settings, the added cost and latency of reasoning-enabled models are not justified. They are best reserved for tasks that require complex multi-step reasoning or domain-specific checks. In other cases, non-reasoning models with well-designed prompts and explanations provide a more efficient balance of accuracy and scalability.

## Practical Prompting Patterns

There are a few patterns that can be used to design eval templates:

1. Explanation-first, then label;
2. Plain label only; and
3. Structured COT plan.

### A) Explanation‑first, then label (recommended default for NLG)

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

Assistant: First provide a 2–4 sentence reasoning tied to the rubric. Then output the JSON.
```

### B) Plain label only (useful for throughput baselines or A/B smoke tests)

```rb
System: You are an evaluator. Read the article and summary. Return only a JSON object:
{scores:{consistency, relevance, fluency, conciseness}, overall}
```

### C) Structured CoT plan (only when a checklist is truly helpful)

```rb
System: Draft a 3–5 step evaluation plan specific to this example (checks to run, evidence to collect).
Then execute the plan and return {plan, reasoning, scores:{...}, overall}.
```

Use **(C)** sparingly and measure whether the added tokens improve agreement on your task. G‑Eval’s ablation suggests this can help on some dimensions, not all.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*zsEmOQ_ARrNLDu3M2kGwZw.jpeg)

Diagram by author

## Summary

Explanations can improve alignment with human judgments and make [LLM evaluation](https://arize.com/llm-evaluation/) more transparent. Ordering the explanation before the label makes it easier to review the reasoning separately, and in most NLG tasks, explicit CoT adds little beyond what a well-structured prompt already provides — especially with reasoning-optimized models. That said, CoT can be worth testing in evaluations that require multi-step factual checks or dependent criteria.

The choice to include explanations or reasoning traces is just one of many factors in designing an [effective LLM judge](https://arize.com/llm-as-a-judge/). Prompt clarity, score definitions, model parameter tuning, and bias mitigation strategies all have a measurable impact on reliability. This post focused on explanations and CoT and [prompts for LLM judges](https://arize.com/blog/evidence-based-prompting-strategies-for-llm-as-a-judge-explanations-and-chain-of-thought/); in future work, we’ll dig into other techniques for building robust, scalable evaluation setups. As always, having robust [LLM evaluation platforms](https://arize.com/llm-evaluation-platforms-top-frameworks) in place to help in testing and experimentation can help.

[**Check out this notebook**](https://github.com/Arize-ai/arize/blob/main/tutorials/python/cookbooks/phoenix_evals_examples/CoT_explanations_simple_vs_complex_evals.ipynb) **testing reasoning vs non-reasoning models on complex and simple LLM-as-a-Judge evaluations.**