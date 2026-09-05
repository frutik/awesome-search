---
type: concept
title: "Adversarial Relevance Judgment"
aliases: ["judge gaming", "gaming the LLM judge", "adversarial judging", "judge manipulation", "keyword stuffing the judge"]
tags:
  - concept
  - search-evaluation
  - llm-judge
  - security
created: 2026-09-04
---

# Adversarial Relevance Judgment

## Definition

An [[LLM as Judge|LLM relevance judge]] is itself a relevance-scoring model, and anything that scores relevance can be gamed. Adversarial relevance judgment covers the ways document text can be crafted to win a favourable grade from a machine assessor without being more relevant to the user — and, relatedly, the ways an evaluation can be structurally rigged in the judge's favour.

The threat is acute wherever the people who write the item text profit from ranking: marketplaces, classifieds, affiliate catalogues, any [[E-commerce Search|e-commerce]] platform with third-party sellers.

## The Attacks

**Query-word stuffing.** Alaofi and colleagues (2025) found LLM judges "highly influenced by the presence of query words in the passages under assessment, even if the wider passage has no relevance to the query." Pack the query terms into an otherwise worthless passage and the judge grades it relevant. Their broader finding is that LLMs "are more likely to label passages as relevant compared to human judges" to begin with.

**Instructions hidden in the judged document.** The same work found some models following instructions written *inside the passage they were assessing* — prompt injection through the corpus, where the attacker controls the content but not the prompt.

**Verbosity padding.** Zheng et al.'s MT-Bench work named verbosity bias as a general judge failure mode and demonstrated it: a "repetitive list" padding attack fooled Claude-v1 and GPT-3.5 over 90% of the time, and GPT-4 8.7% of the time. Longer text reads as better text.

**Position manipulation.** Position bias — preferring whichever option was presented first — is live the moment judging is pairwise, and is cheap to exploit as well as cheap to measure. See [[Position Bias]].

**Grading your own homework.** Clarke and Dietz (2024) make the structural version of the point: if the retrieval approach and the judge share an underlying model, the evaluation is self-referential. They construct an example where an approach scores well automatically and gains nothing with real human assessors. Balog, Metzler and Qin (2025) report the empirical shape of this — "the first empirical evidence of LLM judges exhibiting significant bias towards LLM-based rankers." The point is contested: SynDL (2024), with 1,988 queries and 637,063 LLM labels, reports that their setup "does not favour language model approaches."

## Why Aggregate Agreement Will Not Catch It

The defining property of these attacks is that they are invisible at the level people report. Your average agreement score, your Cohen's κ and your leaderboard correlation can all look perfectly healthy while a subset of documents is being scored on surface form instead of substance — because the attacked items are a small, deliberately-chosen slice and the aggregate averages them away. See [[Levels of Judge Agreement]] and [[Inter-Annotator Agreement]].

The corollary is that adversarial testing is not a threshold you clear but a separate check you run. Where you do not control the content, adversarial tests come *before* any agreement threshold means anything.

## Defences

- **Put dirty tricks in the evaluation sample deliberately**: query-word stuffing, instructions embedded in text, misleading summaries, very long documents. If third parties write your item text, this is a threat model rather than paranoia.
- **Don't let judge and ranker share a base model**, or if they must, report it and validate the result against human assessors on the deciding slice.
- **Randomise or systematically swap option order** in pairwise judging, and measure the position effect rather than assuming it away.
- **Keep humans on a stratified slice**, weighted toward close calls and toward content you do not control.
- **Anchor the judge to something the attacker cannot write.** The industry pattern — human golden labels defining the standard, the LLM scaling it, business metrics keeping it honest — is partly a defence: seller-authored text cannot move a revenue metric the way it can move a text-similarity judgment.

## Open Problems

How to detect someone gaming the judge, especially when they both write the item text and profit from ranking, is listed as unresolved. So is whether [[Staged Judging|cascade-and-distill]] architectures preserve a judge's *biases* along with its accuracy — a distilled student inheriting an exploitable weakness at production scale is barely studied.

## Related Concepts

- [[LLM as Judge]] — the judge under attack
- [[Position Bias]] — one of the exploitable biases, and a contaminant of behavioral pruning
- [[Prompt Sensitivity]] — the accidental counterpart to deliberate manipulation
- [[Levels of Judge Agreement]] — why aggregate figures stay healthy through an attack
- [[Inter-Annotator Agreement]] — the statistic that fails to surface it
- [[Search Governance]] — the platform-side controls over seller-authored content
- [[Staged Judging]] — the architecture whose inherited-bias question is open

## Related Articles

- [[Do LLM Judges Actually Agree With Us]] — [[Andrew Kornilov]]; collects the attack evidence and the marketplace threat model
- [[Why Ecommerce Search Needs Governance and How It Improves Retrieval]] — governance over third-party-authored catalogue text

## Related Topics

- [[E-commerce Search]] — where sellers write the text and have money riding on ranking
- [[Search Quality Assurance]] — where adversarial tests belong in the evaluation protocol
