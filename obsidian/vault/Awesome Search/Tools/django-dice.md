---
title: django-dice
type: tool
aliases: ["preferences-engine", "frutik/django-dice"]
tags:
  - tool
  - context-engineering
  - agentic-memory
  - personalization
  - e-commerce
  - python
  - django
website: https://github.com/frutik/django-dice
repo: https://github.com/frutik/django-dice
created: 2026-09-07
---

# django-dice

A Python/Django implementation of the [[DICE]] design — an LLM-driven engine that infers user preferences from conversation and injects them back into later turns. Written by [[Andrew Kornilov]]; packaged as `preferences-engine`.

- Repo: https://github.com/frutik/django-dice

---

## Why It Exists

[[Embabel DICE]], the reference implementation, is Kotlin/Spring and ships no Python SDK. This port follows the same design in a Django application, aimed squarely at **e-commerce preference inference** rather than general knowledge-graph construction.

The README's framing is a shop assistant who remembers you across visits: they already know the store's ontology (brands, categories, price ranges, colours), they write notes to your customer file after each visit, and they skim the most recent and most certain of those notes before greeting you — so you get *"still looking for something for your husband?"* instead of *"what are you looking for today?"*

## Memory Scoping

The four [[DICE]] memory types map onto two storage scopes, which is where the taxonomy stops being a label and starts doing work:

| Types | Written to | Lifetime |
|---|---|---|
| semantic · procedural · episodic | `global_writable`, `conversation_id = NULL` | Survives all future conversations |
| working | `conversation_writable`, tied to the current `conversation_id` | Disappears when the conversation ends |

## Inline vs Background Extraction

Two triggers for preference extraction, with an explicit latency trade:

| Strategy | Mechanism | Latency | When new preferences apply |
|---|---|---|---|
| **Inline** | Extraction awaited before the answer is generated | Slower turn — two extra LLM calls block the response | Immediately; the current message can shape this turn's answer |
| **Background** | Dispatched as a Celery task after the response returns | Fast turn — extraction runs out of band | Next turn or later |

The guidance: inline when freshness matters (a user declares a budget mid-session and the next response must respect it), background when latency matters and a one-turn lag is acceptable. This is the same offline/online split that [[Agentic Memory for Search Personalization]] argues for, exposed as a per-deployment switch rather than fixed.

## Configuration

Provider-agnostic across OpenAI, Anthropic and AWS Bedrock via `PREFERENCE_ENGINE_PROVIDER`, with `PREFERENCE_ENGINE_OPENAI_BASE_URL` allowing any OpenAI-compatible server (Ollama is documented). Extraction depends on structured JSON output, and the README warns that smaller models follow schemas less reliably.

## Roadmap

Two directions are stated, both notable for search:

- **Beyond chat as a signal.** Extending preference inference to implicit behaviour — applied filters and item clicks — which is the same signal [[User Behavior Insights|UBI]] standardises for search systems.
- **User-visible preferences.** An API letting users inspect what has been inferred about them and selectively disable individual preferences, or turn inference off entirely. Few memory systems described elsewhere offer this.

## Related Tools

- [[Agents That Extract and Use Preferences from Conversations]] — the article this port cites as its reference alongside the Kotlin source
- [[Embabel DICE]] — the Kotlin/Spring reference implementation this follows

## Related Concepts

- [[DICE]] · [[Agentic Memory]] · [[Personalization]] · [[Context Engineering]]

## Related Topics

- [[Agentic Memory for Search Personalization]] · [[E-commerce Search]]

## People

- [[Andrew Kornilov]] — author
