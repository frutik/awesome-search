---
type: concept
title: "LLM Guardrails"
aliases: ["guardrails", "LLM guardrails", "AI guardrails", "output guardrails", "NeMo Guardrails", "Llama Guard"]
tags:
  - concept
  - llm
  - rag
  - safety
related_concepts:
  - "[[RAG]]"
  - "[[Hallucination Detection]]"
  - "[[Query Routing]]"
created: 2026-09-05
---

# LLM Guardrails

> [!note] Different sense of "guardrail"
> This note is about constraining LLM inputs and outputs. The
> experimentation/governance sense used in [[Search Governance]] and
> [[A-B Testing for Search]] — a metric threshold that halts a rollout — is
> unrelated.

## Definition

A guardrail is, in [[James Briggs]]'s phrasing, **"a semi or fully deterministic shield"** placed around a generative model: a mechanism that validates or constrains what goes in and what comes out, without relying on the model's own judgement.

[[Eugene Yan]] lists guardrails as one of seven patterns for LLM systems — "to ensure output quality" — covering structural correctness, factuality, and safety.

## What They Are Applied To

1. **Safety and topic guidance** — filtering malicious inputs, keeping conversation on-subject
2. **Deterministic dialogue** — fixed response flows for predictable queries
3. **Retrieval control** — deciding by semantic similarity *whether* retrieval is needed at all
4. **Agent tool use** — governing when external tools or APIs may be invoked

Points 3 and 4 make guardrails a retrieval concern, not only a safety one: the decision "should this query hit the index?" is the same decision [[Query Routing]] makes.

## NeMo Guardrails and Colang

NVIDIA's NeMo Guardrails is the most documented implementation. It is programmed in **Colang**, a modelling language for dialogue with three building blocks — user message blocks, bot message blocks, and flow blocks. User utterances are encoded into semantic vector space (MiniLM by default) and matched against predefined **canonical forms**, so most routing happens by embedding similarity without an LLM call.

Supporting pieces: utterances (example phrases per canonical form), variables (`$name`), and actions (Python functions exposed via `register_action()`).

## NeMo Guardrails vs Llama Guard

[[Wenqi Glantz]] compared the two (February 2024). Llama Guard is a fine-tuned Llama 2 derivative acting as an input-output classifier with six built-in unsafe categories, extensible with custom ones. NeMo Guardrails is the broader programmable framework.

| | Result |
|---|---|
| Input-moderation accuracy (18 adversarial prompts) | **89%** for both |
| Hardware | NeMo runs on free-tier T4; Llama Guard needs A100 |

Equal accuracy at very different cost is the practical finding.

## Related Concepts

- [[RAG]] · [[Hallucination Detection]] · [[Query Routing]] · [[Agentic Search]]
- [[Search Governance]] — the *other* sense of guardrail, for contrast

## Articles

- [[NeMo Guardrails - The Missing Manual]] — [[James Briggs]]
- [[NeMo Guardrails, the Ultimate Open-Source LLM Security Toolkit]] — [[Wenqi Glantz]]
- [[Patterns for Building LLM-based Systems and Products]] — [[Eugene Yan]]
