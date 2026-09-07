---
type: person
title: "Hajer Bouafif"
role: OpenSearch Solutions Architect
affiliation: "[[Amazon Web Services]]"
tags:
  - person
  - opensearch
  - personalization
  - agentic-memory
created: 2026-09-07
---

# Hajer Bouafif

OpenSearch Solutions Architect at [[Amazon Web Services]]. Works on [[Personalization]] and [[Agentic Memory]] in [[OpenSearch]], and presented the memory-based approach to search personalization at [[Berlin Buzzwords]] 2026.

Her argument is that personalization has been mis-framed as a ranking-and-feature problem. The question a personalized system should answer is not *how do we better rank these results* but **who is running this query, and why now** — and the durable answer to that lives in memory rather than in a retrained feature space. She positions memory as the agent's "source of intelligence", complementary to grounding: the catalog tells the agent what exists, the memory tells it what this particular user means.

A second recurring theme is operational discipline around agents. Her production guidance keeps LLM reasoning off the query path entirely — preferences inferred offline, profiles cached, retrieval capped at the top 5–10 facts, a small language model online, and a conventional lexical/k-NN/hybrid fallback always standing by for when the agent is slow or misbehaves.

## Talks in this vault

- [[Hajer Bouafif - Personalize Search Results with OpenSearch Agentic Memory]] — [[Berlin Buzzwords]] 2026; the offline/online pipeline split, OpenSearch's four memory types, and preference inference from [[User Behavior Insights|UBI]] clickstream

## Topics

- [[Agentic Memory]] · [[Personalization]] · [[Query Rewriting]] — memory-driven query enrichment
- [[Conversational and Agentic Search]] — the broader pattern her work sits in

## Related

- [[Amazon Web Services]] — employer
- [[OpenSearch]] — the engine her work is built on
- [[User Behavior Insights]] — the behavioural signal source she feeds into preference inference
