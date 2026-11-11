---
type: concept
title: "LLM Jury"
aliases: ["PoLL", "Panel of LLM evaluators", "LLM panel", "jury of judges", "multi-judge evaluation"]
tags:
  - concept
  - llm-judge
  - evaluation
related_concepts:
  - "[[LLM as Judge]]"
  - "[[Staged Judging]]"
  - "[[Inter-Annotator Agreement]]"
created: 2026-11-11
---

# LLM Jury

Instead of one large [[LLM as Judge|LLM judge]], several judges — ideally from different model families — score the same output independently, and a voting function combines their scores into one verdict. It is the model-side version of a standard practice in human relevance assessment: pooling several annotators so that individual bias and error average out.

---

## How It Works

Each judge on the panel scores the output exactly as a single judge would — pointwise, against a reference, or pairwise — and the scores are pooled:

- **Max voting** for binary verdicts (correct / incorrect).
- **Average pooling** for graded scores, where a small panel often has no clear majority.

The panel is chosen for **diversity, not size**. Judges that share a model family share its systematic errors, so adding them adds cost but little information.

## Evidence

[[Pat Verga]] and colleagues at [[Cohere]] named the method **PoLL** in [[Replacing Judges with Juries]]. A panel of Command R, Claude 3 Haiku and GPT-3.5 was tested against GPT-4 as a single judge, across single-hop QA, multi-hop QA and Chatbot Arena Hard:

- **Higher agreement with humans.** Cohen's κ of 0.763 / 0.906 / 0.867 on KILT [[Natural Questions]] / TriviaQA / HotpotQA, against 0.627 / 0.841 / 0.830 for GPT-4.
- **Better system rankings.** Kendall τ 0.778 against the Chatbot Arena leaderboard, versus 0.667 for GPT-4.
- **Less self-preference.** On the multi-hop QA sets, each evaluated model got its largest positive deviation from human scores when it judged itself. On Arena Hard, the GPT-4 judge ranked a GPT-4 variant second where the human ranking placed it fourth. Pooling across families gave the smallest spread of deviation from human scores.
- **Seven to eight times cheaper** than GPT-4 Turbo, and generally faster, since small models run in parallel.

The paper also found that no single judge was best in every setting, while the panel did well in all of them.

## Why Diversity Rather Than Repetition

Calling one judge several times and taking a majority vote reduces **sampling noise**: it helps when the judge sometimes gets a case right and sometimes not. It does nothing about **systematic error**. If the judge reasons the same wrong way on every call, every call returns the same wrong verdict. A jury of different models targets that systematic error. This is the response [[LLM as Judge]] recommends for its shaped, systematic failure modes: vary the model family, not just the number of calls.

## Caveats

- **A jury agreeing with itself is not accuracy.** Agreement among panel members is inter-judge agreement, and the same panel agreeing on a rerun is self-consistency. Neither replaces checking against human labels. See [[LLM as Judges - A Vocabulary]] and [[Judge Calibration]].
- **Panel selection is unsolved.** PoLL tested one composition, so which models to include, and how many, remains open.
- **Tested on a narrow range of tasks.** The evidence covers QA correctness and chat preference. How well it carries over to maths, reasoning, or graded search relevance has not been shown.

## Related Concepts

- [[LLM as Judge]] — the single-judge setup a jury replaces
- [[Staged Judging]] — the other way to combine cheap and expensive judges: in sequence, escalating on low confidence, rather than in parallel
- [[Inter-Annotator Agreement]] — the human-side practice of pooling annotators, and the κ used to evaluate panels
- [[Judge Calibration]] — validating the combined verdict against people
- [[Prompt Sensitivity]] — single large judges can swing widely across prompt variants
- [[Atomic Claim Verification]] — another way of breaking up a judgment, by splitting the claim instead of multiplying the judges

## Related Articles

- [[Replacing Judges with Juries]] — the PoLL paper
- [[LLM as Judges - A Vocabulary]] — "jury" among the core judge-evaluation terms, with evidence that small juries can agree poorly with each other yet still reproduce a paper's main finding
- [[Trust or Escalate - LLM Judges with Provable Guarantees for Human Agreement]] — several judges of different cost, arranged as a cascade

## People

- [[Pat Verga]]
