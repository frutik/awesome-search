---
type: person
title: "Han-chung Lee"
aliases: ["Han Lee", "leehanchung"]
tags:
  - person
  - evaluation
  - calibration
  - llm
affiliation: "Moody's"
blog: https://leehanchung.github.io/
linkedin: https://www.linkedin.com/in/hanchunglee/
created: 2026-09-21
---

# Han-chung Lee

Director of Machine Learning at Moody's, where he leads teams building custom LLMs, generative
AI applications, and search and discovery systems over financial data. He writes on machine
learning systems, evaluation and alignment, search and recommendations, and is writing
*Evaluation and Alignment: The Seminal Papers* for Manning. A Berkeley EECS graduate.

🔗 https://leehanchung.github.io/ · [LinkedIn](https://www.linkedin.com/in/hanchunglee/)

## Contribution to This Vault

- [[Jev and the Return of AI-ML Engineering|Jev and the Return of AI/ML Engineering]]
  (2026-09-21) — a structural review of [[Jev]]: take the four things the launch promises, show
  three of them are available off the shelf, and the case for the model reduces to the fourth,
  [[Reinforcement Learning for Calibrated Decisions|calibration]], which he cannot reproduce.

His angle is unusual in the [[Reception of Jev|reaction]] because he comes to the model from
evaluation and alignment rather than from product or from ranking. That shows up twice.

**He endorses the interface for the two uses this vault cares about.** Rubric and preference
modelling for [[LLM as Judge|LLM evaluation]] and alignment, and search engine
[[Reranking|reranking]] and optimization — he says the API design matches his intuition for that
shape. The endorsement is of the shape, not of the model.

**Then he attacks the differentiator with measurements.** He asks *what does it calibrate to*,
on the grounds that calibration is only defined relative to a distribution, and reports high
[[Expected Calibration Error|ECE]] across coin-toss, two-dice and three UCI datasets, worst once
the experiments leave simulated distributions. He also cites Valeriy M's 16,500 predictions
across eight datasets, with calibration failures on seven of them. He is careful to label what
the figures do not show — poor calibration is not a finding about accuracy.

The contribution nobody else in the reaction made is a question about attribution: the working
demonstrations of the model may come from **its base model rather than from RLCD**, which is the
ablation the vendor has not published.

His conclusion gives the piece its title. Reliable calibrated probabilities paired with
thresholds would be a durable advantage ([[Staged Judging]]); absent evidence of one, a capable
team should train its own model, and the evaluation stack becomes an engineering problem rather
than a purchasing decision.

## Related Concepts

- [[Calibrated Relevance Probability]] · [[Expected Calibration Error]]
- [[Reinforcement Learning for Calibrated Decisions]] · [[System One Model]]
- [[LLM as Judge]] · [[Staged Judging]] · [[Reranking]]

## Related Notes

- [[Jev]] · [[TypeSafe]]
- [[Reception of Jev]] — where this piece sits in the wider argument
- [[Praneeth Paikray]] — the other independent calibration measurement, on a real corpus
- [[Hev]] — the retrieval-side reading that came out favourable
