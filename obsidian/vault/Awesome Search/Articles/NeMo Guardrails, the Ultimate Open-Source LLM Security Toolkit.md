---
type: article
title: "NeMo Guardrails, the Ultimate Open-Source LLM Security Toolkit"
source: "https://towardsdatascience.com/safeguarding-llms-with-guardrails-4f5d9f57cff2"
author: ["Wenqi Glantz"]
published: 2024-02-09
tags:
  - clippings
  - llm
  - safety
  - rag
concepts:
  - LLM Guardrails
  - RAG
created: 2026-09-05
---

# NeMo Guardrails, the Ultimate Open-Source LLM Security Toolkit

**Source**: https://towardsdatascience.com/safeguarding-llms-with-guardrails-4f5d9f57cff2
**Published**: 9 February 2024 · **Author**: [[Wenqi Glantz]]

> [!note] Title differs from older citations
> This URL is often listed as *"Safeguarding LLMs with Guardrails"*. The page
> now carries the title recorded above; the slug is unchanged.

## Summary

A head-to-head of the two mainstream guardrail frameworks, with a working RAG implementation behind it.

## The Comparison

**Llama Guard** — a fine-tuned Llama 2 derivative acting as an input-output safeguard, with six built-in unsafe categories extensible with custom classifications.

**NeMo Guardrails** (NVIDIA) — the broader programmable framework: content moderation, topic steering, hallucination reduction, and response shaping.

| | Result |
|---|---|
| Input-moderation accuracy (18 security test prompts) | **89% for both** |
| Hardware | NeMo: free-tier T4 · Llama Guard: A100 |

Equal accuracy at materially different hardware cost is the operative finding.

## Implementation Stack

[[LlamaIndex]] with `RecursiveRetrieverSmallToBigPack` · Colang for rail flows · OpenAI GPT-3.5-turbo · config files `config.yml`, `prompts.yml`, `bot_flows.co`, `actions.py`

## Related Concepts

- [[LLM Guardrails]] — primary topic
- [[RAG]] · [[Hallucination Detection]] · [[Text Chunking]]

## Related Tools

- [[LlamaIndex]]

## Related People

- [[Wenqi Glantz]]
