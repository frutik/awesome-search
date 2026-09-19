---
type: person
title: "Diogo Almeida"
aliases: ["Diogo Almeida (TypeSafe)"]
tags:
  - person
  - llm
  - structured-output
  - founder
affiliation: "[[TypeSafe]]"
website: https://typesafe.ai
created: 2026-09-19
---

# Diogo Almeida

Founder of [[TypeSafe]], the AI lab behind [[Jev]] and the
[[System One Model|System One Model]] class. Before TypeSafe he worked at OpenAI, where by his
own account he helped build the methods that made language models useful at following
instructions and conversing — work he describes as ending up as the research behind ChatGPT.

---

## Position

The question he frames as driving four years of his work: models have been superhuman at chat
for years, so where is all the automation? His answer, and TypeSafe's founding premise, is that
chat-shaped models are the wrong interface for software — strings have to be parsed and
validated, and a model free to emit anything can always go off the rails. TypeSafe spent roughly
two years in stealth building a stack around the opposite bet: a fixed output space, parallel
sampling, and training aimed at calibrated confidence rather than human preference
([[Reinforcement Learning for Calibrated Decisions]]).

TypeSafe announced Jev on 2026-09-15 with a reported $40M round led by DCVC.

A note on attribution: third-party coverage ([[How to Use Jev - A Practical Guide]]) describes
him as having co-invented RLHF and InstructGPT. His own wording in the launch post is more
measured — that he helped build the methods behind instruction-following and conversation, and
that the work ended up as the research behind ChatGPT. This note follows his own framing.

## Relevance to Search

Indirect but real. Nothing he has published is about retrieval, but the model class he
describes supplies the property that made [[Jev]] competitive as a reranker in
[[Hev meets Jev]] — a [[Calibrated Relevance Probability]] on every judgment, which no
purpose-built reranker returns.

## Articles in This Vault

- [[Introducing System One Models & Jev]] (2026-09-15) — the launch announcement for the model
  class and for Jev, including the workflow-eval methodology and the company's own list of
  caveats on its headline figures

## Related Concepts

- [[System One Model]] · [[Reinforcement Learning for Calibrated Decisions]] · [[Calibrated Relevance Probability]]

## Related Notes

- [[TypeSafe]] — the company he founded
- [[Jev]] — its first public model
