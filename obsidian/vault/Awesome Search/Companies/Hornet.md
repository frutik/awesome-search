---
type: company
website: https://hornet.dev
industry: search infrastructure
category: technology-provider
search_domain: high-precision context delivery for agentic AI systems
---

# Hornet

## What They Build

Hornet (hornet.dev) is a retrieval infrastructure company focused on **high-precision context delivery for agentic AI systems**. Their core thesis: the failure mode of agentic retrieval is not missing relevant documents but injecting convincing distractors — text that is semantically adjacent, high-confidence, and wrong.

Their work challenges the assumption that better retrieval always means better end-to-end accuracy. In agentic settings, a retriever that returns more plausible but incorrect documents actively degrades LLM reasoning.

## Focus Areas

- **Defensive retrieval** — precision over recall; dynamic-k over fixed-k; abstention as a first-class retrieval outcome
- **Distractor-aware evaluation** — UDCG metric that assigns negative utility to passages that cause incorrect answers
- **MAD (Mutually Assured Distraction)** — framework describing how independently rational improvements to retrieval and reasoning can lead to global system instability
- **Agentic context quality** — treating each retrieved chunk as a liability rather than a free addition

## People

- [[Lester Solbakken]] — Co-founder; author of the MAD framework and defensive retrieval principles

## Articles

- [[Mutually Assured Distraction]] — why better retrieval and better reasoning can make agentic systems less reliable

## Concepts

[[Agentic Search]] · [[Clean Context]] · [[UDCG]] · [[Retrieval Pipeline]] · [[LLM as Judge]] · [[Search Evaluation]]

## Topics

- [[Conversational and Agentic Search]]
- [[Search Quality Assurance]]
