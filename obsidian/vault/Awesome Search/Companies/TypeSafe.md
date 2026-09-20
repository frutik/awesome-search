---
type: company
title: "TypeSafe"
aliases: ["TypeSafe AI", "typesafe.ai"]
tags:
  - company
  - ai-infrastructure
  - structured-output
website: https://typesafe.ai
created: 2026-09-19
---

# TypeSafe

**TypeSafe** is an AI company building what it calls *AI primitives* — modular, composable
decision components intended to be reliable and fast enough for software to consume directly.
Its flagship model is [[Jev]], which the company positions as the first **System One model**:
a model that makes fast, structured decisions and returns typed values and probability
distributions for code, rather than text for a person.

The framing is a deliberate contrast with general chat models. A System One model generates no
free-form text, no code, and no written rationale; the possible outputs are fixed by the
caller's schema before the call is made.

Website: https://typesafe.ai · Documentation: https://docs.typesafe.ai/introduction

---

## Company

Founded by [[Diogo Almeida]], previously at OpenAI, where he describes having helped build the
instruction-following and conversational methods behind ChatGPT. TypeSafe spent roughly two
years in stealth before announcing [[Jev]] and the
[[System One Model|System One Model]] class in September 2026
([[Introducing System One Models & Jev]]).

The founding premise is that chat-shaped models are the wrong interface for software: strings
must be parsed and validated, and a model free to emit anything can always go off the rails. The
company's bet is the inverse — a fixed output space, parallel sampling, and training for
calibrated confidence ([[Reinforcement Learning for Calibrated Decisions]]) rather than human
preference.

Both names come from the FAQ in that announcement: *System One* from Daniel Kahneman's fast,
intuitive System 1 thinking, and *Jev* from the economist William Stanley Jevons — the argument
being that each order-of-magnitude drop in the cost of intelligence unlocks orders of magnitude
more uses.

Jev launched on 2026-09-15 alongside a reported $40M round led by DCVC, per
[[How to Use Jev - A Practical Guide]].

### Reading the Company's Claims

TypeSafe's headline figures (193.6× faster, 444.6× cheaper) come from **workflow evals**, an
evaluation format it designed: a fixed compute graph given to every model, scored not against
ground-truth labels but against the averaged predictions of large external models as reference
probabilities. The announcement is unusually explicit about the resulting biases — the workflows
were built by its own model-capabilities team, the reference models bias the comparison toward
those vendors, the competing LLMs run through TypeSafe's own wrapper, and its own 0%
type-error figure is derived by construction rather than measured.

That candour is worth crediting, but the structure stands: the architecture claims are checkable,
while the intelligence-parity claim rests on a benchmark the vendor designed and scored.
## Relevance to Search

TypeSafe is not a search company and does not market [[Jev]] as a reranker. It appears in this
vault because the model's call shape — a shared state plus many independent typed questions
answered in parallel with probabilities — turns out to fit [[Reranking]] closely enough to
compete with purpose-built rerankers without any reranker training.

[[Hev meets Jev]] is the benchmark that makes this case: on three [[BEIR]] subsets, an untuned
Noul-per-document prompt landed at 0.501 mean nDCG@10, against 0.504 for
[[Voyage AI|Voyage]] rerank-3 and 0.486 for [[Cohere]] rerank-v3.5. The conclusion drawn there
is less about TypeSafe than about the category: a general decision model with no ranking
training now sits in the same quality and price bracket as the reranking specialists, and adds
a [[Calibrated Relevance Probability|calibrated probability]] none of them return.

Two caveats recorded in the same source: Jev is hosted only, so documents leave the caller's
environment, and its 32k-token request budget bounds rerank depth at roughly 50 passages.

## Related Notes

- [[Jev]] — the model, and the question types (Choice, Score, Noul)
- [[hev-rerank]] — third-party wrapper using Jev as a reranker
- [[Hev meets Jev]] — the benchmark against purpose-built rerankers
- [[Voyage AI]] · [[Cohere]] · [[Mixedbread]] — the reranker vendors compared against
- [[TypeSafe Cookbook - Re-ranking]] — its own reranking walkthrough, on [[CLERC]] legal retrieval
- [[Introducing System One Models & Jev]] — the launch announcement
- [[Diogo Almeida]] — founder
- [[How to Use Jev - A Practical Guide]] — [[Prosper Otemuyiwa]]; primitives, patterns, and a sceptical read of the benchmark
- [[Using TypeSafe's Jev for Evals]] — [[Annabell Schäfer]]; the model as a rubric judge, via [[Langfuse]]
- [[Adapting Jev to Your Domain with GEPA]] — [[Praneeth Paikray]]; the latency and calibration claims measured from outside

## Related Concepts

- [[Reranking]] · [[Calibrated Relevance Probability]] · [[Cross-Encoder]]

## Related Topics

- [[Reasoning Reranking]]

## How the Pricing Claim Reads Under Audit

The launch's sharpest number is a 238x lower input price than Claude Fable 5.1.
[[JEV vs LLM - Your Software Doesn't Want a Conversation It Wants a Decision|Sajith K]] checked
it — $10.00 against $0.042 per million input tokens — and found the arithmetic exactly right,
while pointing out that the comparator is a frontier model at the top of the price curve rather
than the model anyone would actually use for classification work. Against Claude Haiku 4.5 at
$1.00 per million, the gap is roughly 24x. Still a large margin, and still not the headline
number. His verdict on the launch as a whole is that the speed, the cost and the novelty of the
category are real, while the marketing runs about ten times ahead of the evidence — something he
credits the company with half-admitting.

See [[Reception of Jev]].
## How the Latency and Calibration Claims Read Under Measurement

Two vendor figures have since been measured from outside, in
[[Adapting Jev to Your Domain with GEPA]].

**Latency.** TypeSafe's stated end-to-end range is 70–500 ms. [[Praneeth Paikray]] observed a
client-side median of **14.69 s** (p95 15.62 s) over 505 requests, and **19.59 s** (p95 24.37 s)
over 1,260 evaluations at up to 24 concurrent — with 12.35 s on a serial smoke test, so
concurrency is not the explanation. He is explicit that he cannot separate model inference from
transport and queueing, which makes this a reading of the hosted service in September 2026 rather
than of the model. It is still one to two orders of magnitude from the published range, and the
company publishes no p95/p99 figures or SLA against which to reconcile it.

**Calibration.** The launch rests on probabilities you can threshold, trained for by
[[Reinforcement Learning for Calibrated Decisions|RLCD]]. Measured at the default prompt on one
classification task, [[Jev]] returned a 10-bin [[Expected Calibration Error|ECE]] of 0.173
against 0.052 for a TF-IDF baseline, and log loss of 1.849 against 0.335 — with `confidence`
returning exactly 1.0 on half the test set, ten of those answers wrong. The fair qualification is
that optimizing the prompt cut ECE to 0.069, so the figure indicts the default instruction at
least as much as the training method. The company has still published neither a reliability curve
nor an ablation isolating RLCD.

**Cost.** This one checks out. Input billing at $0.042/MTok produced totals of $0.00898 and
$0.03067 for the two experiments, exactly as advertised.
