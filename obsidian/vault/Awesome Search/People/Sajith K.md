---
type: person
title: "Sajith K"
aliases: []
tags:
  - person
  - llm
  - structured-output
  - evaluation
created: 2026-09-20
---

# Sajith K

Writes on AI engineering in *Artificial Intelligence in Plain English*.

---

## Contribution to This Vault

- [[JEV vs LLM - Your Software Doesn't Want a Conversation It Wants a Decision]] (2026-09) — an
  audit of [[Jev]]'s launch claims: the docs, the benchmarks, and what he calls the pile-on from
  the sceptics, sorted into "what's real, what's marketing, and when you'd actually reach for
  it."

The piece earns its place for doing arithmetic nobody else in the
[[Reception of Jev|reaction]] did. He confirms TypeSafe's 238x price claim is exactly correct
against Claude Fable 5.1 — and then points out that the realistic incumbent for classification
work is Claude Haiku 4.5, against which the same math gives ~24x. He grants that ~24x is still a
real business case; the objection is that 238x is the number in the headline.

Two other things are worth carrying. He separates a Noul value from a confidence score — a Noul
of 0.5 is a genuine coin-flip rather than medium urgency, and confidence is a distinct quantity
derived from how peaked the distribution is, so conflating the two breaks thresholds silently.
And he ends by dismantling his own title: every use case the vendor leads with puts the model
*beside* an LLM rather than in place of one, making it a decision layer around a generation
layer.

His summary is the fairest assessment written about the launch in either direction — the speed,
the cost and the novelty of the category are real, and the marketing runs about ten times ahead
of the evidence, which the vendor half-admits.

## Related Concepts

- [[System One Model]] · [[Calibrated Relevance Probability]] · [[Staged Judging]]

## Related Notes

- [[Jev]] · [[TypeSafe]]
- [[Reception of Jev]] — where this piece sits in the wider reaction
