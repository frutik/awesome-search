---
type: article
title: "Replacing Judges with Juries: Evaluating LLM Generations with a Panel of Diverse Models"
source: "https://arxiv.org/abs/2404.18796"
pdf: "https://arxiv.org/pdf/2404.18796"
author:
  - "[[Pat Verga]]"
published: 2024-04-29
created: 2026-11-11
venue: "arXiv (cs.CL)"
companies:
  - "[[Cohere]]"
datasets:
  - "[[Natural Questions]]"
concepts:
  - "[[LLM Jury]]"
  - "[[LLM as Judge]]"
  - "[[Inter-Annotator Agreement]]"
  - "[[Prompt Sensitivity]]"
  - "[[Kendall Rank Correlation]]"
topics: []
tags:
  - article
  - llm-judge
  - evaluation
  - llm
---

# Replacing Judges with Juries

**Authors:** [[Pat Verga]], Sebastian Hofstätter, Sophia Althammer, Yixuan Su, Aleksandra Piktus, Arkady Arkhangorodsky, Minjie Xu, Naomi White, Patrick Lewis · [[Cohere]] · **arXiv:2404.18796** (2024)

## Summary

The default way to judge LLM output is one large model, usually GPT-4. The paper argues this is costly, introduces intra-model bias (judges recognise and prefer their own outputs), and is often unnecessary. It proposes a **Panel of LLM evaluators (PoLL)**: several smaller judges from *different model families* score each output independently, and a voting function pools their scores. See [[LLM Jury]].

## Setup

- **Panel:** Command R, Claude 3 Haiku and GPT-3.5 — three disjoint families.
- **Voting:** max voting for the QA tasks (binary correct/incorrect); average pooling for Chatbot Arena Hard, where 1–5 scores from three judges rarely give a clear majority.
- **Settings:** single-hop QA on KILT versions of [[Natural Questions]], TriviaQA and HotpotQA; multi-hop QA on Bamboogle and HotpotQA; and Chatbot Arena Hard (500 prompts, pairwise against a GPT-4 baseline). QA judging is reference-based with few-shot examples; humans from Cohere's internal annotation workforce judged whether the reference answer is semantically contained in the generation.

## Findings

- **Agreement with humans.** [[Inter-Annotator Agreement|Cohen's κ]] on single-hop QA: PoLL 0.763 / 0.906 / 0.867 on NQ / TriviaQA / HotpotQA, against GPT-4 at 0.627 / 0.841 / 0.830 — GPT-4 was one of the weaker judges here, below each individual small model on NQ.
- **System rankings.** Against the Chatbot Arena leaderboard, PoLL reached [[Kendall Rank Correlation#Kendall vs Spearman vs Pearson|Pearson]] 0.917 and [[Kendall Rank Correlation|Kendall τ]] 0.778, versus 0.817 and 0.667 for GPT-4, with the closest match at the top of the list. Both statistics compare the judge's model ranking with the human one: Pearson measures how linearly the two sets of values move together, and Kendall τ counts how many pairs of models the two rankings order the same way. τ normally comes out lower than Pearson on the same data, so the two figures are not directly comparable. [[LLM as Judges - A Vocabulary]] covers κ and τ, including the τ ≥ 0.9 convention, in its statistics primer.
- **Prompt fragility.** GPT-4's κ on NQ ranged from 0.518 (zero-shot) to 0.725 depending on prompt variant. The best variant explicitly told it not to "overthink" or reason about real-world factuality — the authors' hypothesis is that GPT-4 over-reasons and injects background knowledge into what is essentially reference matching. The same instruction badly hurt GPT-3.5. See [[Prompt Sensitivity]].
- **Bias.** On multi-hop QA, PoLL had the smallest spread of score deviation from humans (standard deviation 2.2, against 6.1 for GPT-3.5), and each model received its highest positive delta when judged by itself. On Arena Hard the GPT-4 judge ranked a GPT-4 variant 2nd where the human ranking had it 4th.
- **Cost.** The three-model panel ran at $1.25 input / $4.25 output per million tokens against $10 / $30 for GPT-4 Turbo — seven to eight times cheaper. Smaller models run in parallel are also generally faster, though latency was not measured.

## Limitations

Only three evaluation settings, few judges and few panel compositions were tested. Applicability to maths or reasoning evaluation is open, and *panel selection* — choosing which models to include — is left to future work.

## Why It Matters

The finding that changes practice is that there is no single best judge across settings, while the panel performs consistently. It turns judge diversity from a nice-to-have into the main lever: repeated calls to one judge sample that judge's bias again, while judges from different families have errors that partly cancel.

## Related Concepts

- [[LLM Jury]] — the method
- [[LLM as Judge]] — the single-judge baseline it replaces
- [[Inter-Annotator Agreement]] — Cohen's κ as the agreement measure
- [[Kendall Rank Correlation]] — system-ranking agreement
- [[Prompt Sensitivity]] — GPT-4's κ swing across prompt variants

## Related Articles

- [[Trust or Escalate - LLM Judges with Provable Guarantees for Human Agreement]] — also uses several models of different cost, but in sequence rather than in parallel
- [[LLM as Judges - A Vocabulary]] — defines "jury" alongside related judge terms

## People

- [[Pat Verga]] — first author
