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
- **Agentic query workload** — characterizing how agents search differently from humans (long queries, web operators, multi-turn sessions)
- **Agentic context quality** — treating each retrieved chunk as a liability rather than a free addition

## People

- [[Jo Kristian Bergum]] — Co-founder; former Vespa AI Chief Scientist; agentic retrieval workload research
- [[Lester Solbakken]] — Co-founder; author of the MAD framework and defensive retrieval principles
- [[Skip Everling]] — scaling dimensions of keyword search; agentic query workload on the serving side

## Articles

- [[Mutually Assured Distraction]] — why better retrieval and better reasoning can make agentic systems less reliable
- [[This Is What Agentic Retrieval Looks Like]] — GPT-5 query behavior: 24 calls/session, 10-term median, phrase quotes in 98% of sessions
- [[The Scaling Dimensions of Keyword Search]] — [[Skip Everling]]; Block-Max WAND degrades on long agent queries; the serving-side case for a retrieval engine built for agents

## Concepts

[[Agentic Search]] · [[Agentic Retrieval]] · [[Clean Context]] · [[UDCG]] · [[Retrieval Pipeline]] · [[LLM as Judge]] · [[Search Evaluation]] · [[BM25]] · [[Query Operators]] · [[Agentic Query Workload]] · [[Block-Max WAND]]

## Topics

- [[Conversational and Agentic Search]]
- [[Current Frontier of Search]]
- [[Search Quality Assurance]]
