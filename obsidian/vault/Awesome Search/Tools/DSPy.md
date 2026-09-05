---
type: tool
title: "DSPy"
aliases: ["dspy", "Declarative Self-improving Python", "DSPy framework"]
website: https://dspy.ai/
repo: https://github.com/stanfordnlp/dspy
tags:
  - tool
  - llm
  - prompting
  - optimization
  - open-source
related_concepts:
  - "[[RAG]]"
  - "[[Prompt Sensitivity]]"
  - "[[Synthetic Query Generation]]"
created: 2026-09-05
---

# DSPy

DSPy — "Declarative Self-improving Python" — is a framework from Stanford NLP for *programming* rather than prompting language models. MIT licensed.

🔗 https://dspy.ai/ · https://github.com/stanfordnlp/dspy

## Core Abstractions

| Abstraction | Role |
|---|---|
| **Signatures** | Declare a task's input/output specification |
| **Modules** | Compose those signatures into systems |
| **Optimizers** | Algorithms that refine the prompts and weights behind them |

The pitch is that you specify *what* the model should do and let optimizers discover the prompt that achieves it, rather than hand-tuning strings. Applications range from simple classifiers to RAG pipelines and agent loops.

## Why It Matters Here

DSPy is the direct structural answer to [[Prompt Sensitivity]] — if retrieval and ranking quality shift with prompt phrasing, then the prompt is a parameter to be optimized rather than a constant to be authored. That reframing matters for any RAG pipeline whose generation stage is currently a hand-written template.

[[Omar Khattab]] is among the framework's authors, connecting it to the [[ColBERT]] line of retrieval work also covered here.

## Related Tools

- [[LangChain]] — the prompt-chaining approach DSPy positions against
- [[RAGAS]] — evaluation, which DSPy optimizers need a metric from

## Related Concepts

- [[RAG]] · [[Prompt Sensitivity]] · [[Synthetic Query Generation]]

## Related People

- [[Omar Khattab]]
