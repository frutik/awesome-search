---
type: person
title: "Annabell Schäfer"
aliases: []
tags:
  - person
  - evaluation
  - llm-as-judge
  - observability
affiliation: "[[Langfuse]]"
website: https://langfuse.com/blog
created: 2026-09-19
---

# Annabell Schäfer

Writes on the [[Langfuse]] blog about LLM evaluation and observability.

---

## Contribution to This Vault

- [[Using TypeSafe's Jev for Evals]] (2026-09-18) — using [[Jev]] in place of a generative
  [[LLM as Judge|LLM-as-a-judge]] for rubric verdicts, with a worked integration that scores
  Langfuse traces and writes the result back.

The argument worth carrying into relevance judging is about rubric design rather than cost. A
judge that answers one atomic question at a time with a probability will return *low confidence*
when the criteria are vague, instead of a crisp label that conceals the vagueness — so the tool
surfaces a bad rubric rather than absorbing it. The piece is also clear-eyed about what the
approach gives up: no rationale on any individual verdict, and no ability to abstain unless the
question space includes an explicit escape hatch.

It is likewise careful with the benchmark it reports, noting that agreement with one frontier
model is not accuracy, and that an open-source judge scored two points better for marginally
more money.

## Related Concepts

- [[LLM as Judge]] · [[Staged Judging]] · [[Levels of Judge Agreement]] · [[Calibrated Relevance Probability]] · [[Search Evaluation]]

## Related Notes

- [[Langfuse]] · [[Jev]] · [[TypeSafe]]
