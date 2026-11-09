---
type: topic
title: LLM as Judge Vocabulary
aliases:
  - LLM-as-a-judge vocabulary
  - LLM judge glossary
  - LLM judge terminology
related_concepts:
  - "[[LLM as Judge]]"
  - "[[Levels of Judge Agreement]]"
  - "[[Inter-Annotator Agreement]]"
  - "[[Judge Calibration]]"
  - "[[Calibrated Relevance Probability]]"
  - "[[Expected Calibration Error]]"
  - "[[Judgment Lists]]"
  - "[[Staged Judging]]"
  - "[[Knowledge Distillation]]"
  - "[[Kendall Rank Correlation]]"
  - "[[Hallucination Detection]]"
  - "[[Pairwise Relevance Evaluation]]"
  - "[[Adversarial Relevance Judgment]]"
related_topics:
  - "[[Search Quality Assurance]]"
  - "[[Model Selection and Fine-Tuning Evaluation]]"
articles:
  - "[[Do LLM Judges Actually Agree With Us]]"
  - "[[Calibrate Before You Trust]]"
  - "[[How Etsy Uses LLMs to Improve Search Relevance]]"
  - "[[Automating Search Relevance Assessment at Scale with LLM-as-a-Judge]]"
  - "[[Classic ML to Cope with Dumb LLM Judges]]"
  - "[[Benchmarking LLM-based Relevance Judgment Methods]]"
created: 2026-11-09
tags:
  - topic
  - search-evaluation
  - llm-judge
  - inter-annotator-agreement
---
tml

# LLM as Judge Vocabulary

The words used around [[LLM as Judge|LLM relevance judges]] sound interchangeable and are not. "The judge agrees", "the judge is consistent" and "the judge is calibrated" are three different claims, each checked a different way. This note is a glossary. Each entry says what the term means in relevance evaluation, what it does not mean, and which note covers it in depth.

---

## Agreement

Agreement is how often two judges give the same answer. It is never a single number, because the judges can be compared at four [[Levels of Judge Agreement|levels]] that move almost independently:

1. **Label**: same grade on the same query–document pair?
2. **Score**: about the same metric value for each approach?
3. **Ranking**: approaches in the same order?
4. **Decision**: same winner, same "this difference is significant", same call to ship?

Errors that hit every approach the same way can leave the ranking intact while every label is wrong. The tape-measure analogy in [[Do LLM Judges Actually Agree With Us]] makes this point. NormasTCU (2026) shows it in data: Cohen's κ of 0.32–0.53 on labels next to Kendall τ ≥ 0.9 on nDCG@10 and MRR leaderboards. The reverse failure also happens. Otero, Parapar and Barreiro (2025) found false positives on statistical significance *at high τ*. A quoted agreement figure should always say which level it measures.

## Inter-judge agreement

Inter-judge agreement is agreement between two specific judges. The term only means something once you say which two, and the vault's sources list six different comparisons:

- **human vs. human**: is the task objective at all?
- **LLM vs. human**: does the model copy *this* human?
- **LLM vs. LLM**: would another model have said something else?
- **prompt vs. prompt**: see [[Prompt Sensitivity]]
- **same model run twice**: self-consistency, below
- **panel vs. single judge**: see Jury, below

At the label level it is measured with the same statistics as human [[Inter-Annotator Agreement]]: Cohen's or Fleiss' κ, Krippendorff's α, and quadratic-weighted κ for graded scales. Judges are compared with Kendall's τ at the ranking level ([[Kendall Rank Correlation]]). The human–human figure on your own data sets the bar, not 1.0. If your annotators agree at κ 0.6, asking a model for κ 0.8 makes no sense. Reference points from the vault: human–human κ can exceed 0.5 on binary assessment, LLM–human κ typically runs 0.3–0.5, and GPT-4 reached about 80% agreement with human preferences on MT-Bench, which is about the rate at which humans agree with each other.

Two warnings. Matching one human is not the same as matching users in general. Three LLMs that agree may share a blind spot.

## Ordinal and binary agreement

The grading scale determines which agreement statistic is valid.

- **Binary agreement** is on a relevant/not-relevant scale. Every disagreement costs the same.
- **Ordinal agreement** is on a graded scale such as 0–3 or the [[ESCI Label Scheme]]. A 0-vs-3 disagreement is worse than a 0-vs-1, so the statistics weight distance: quadratic-weighted κ or ordinal Krippendorff's α. Exact agreement and within-one agreement are usually reported alongside.

The common mistake is to quietly collapse graded labels to binary. Turning 0/1/2/3 into relevant/not makes the agreement number look better. It also throws away the distinctions [[NDCG]] depends on. If you collapse, report both figures. You can go the other way too: for a chance-corrected number per class on an ordinal scale, compute one-vs-rest binary κ and label it as such.

[[Automating Search Relevance Assessment at Scale with LLM-as-a-Judge|Allegro's RAT]] shows why one ordinal figure is not enough. Its locally hosted quantized judge reached a quadratic-weighted κ of 0.69 on Polish, which is good for a four-level scale. Per-class F1 was 0.94 on exact matches but only 0.51 and 0.33 on separating "highly substitutable" from "substitutable", the boundary the business cares about.

The gap can run the other way too. In [Better Retrievers, Worse Labels](https://arxiv.org/abs/2610.40966) (Kochergin and Konovalov, 2026), three-label Cohen's κ on context sufficiency was 0.44 for Phi-4 vs. Qwen3-14B, 0.38 for Phi-4 vs. a blind audit, and 0.49 for Qwen3-14B vs. the audit. Collapsed to binary sufficient/insufficient, the same pairs reached 0.74, 0.59 and 0.79. The judges mostly disagreed about "partial" vs. "sufficient" and mostly agreed on the decision that mattered: answer or abstain. Here the binary figure is the useful one, because it matches the operational decision. Choose the scale that matches the decision the labels feed. The authors also recommend reporting raw agreement (0.64–0.70 here) next to κ, because a shift in label prevalence can push κ down even when operational agreement stays the same.

## Self-consistency

Self-consistency means agreement of a judge with itself: the same model and prompt run more than once on the same pair. It measures stability, not correctness. A judge can give the same wrong answer every time. It needs no reference labels, which is why [[Hallucination Detection]] uses it as a reference-free check.

In practice it is used in two ways:

- **Sampling technique.** [[Etsy]]'s o3 annotator uses self-consistency sampling over several reasoning paths.
- **Routing signal.** Etsy plans to send only the pairs where the LLM is inconsistent to humans. This is the same idea as escalating on disagreement in [[Staged Judging]], applied to one judge instead of several ([[How Etsy Uses LLMs to Improve Search Relevance]]).

## Qrels

Qrels ("query relevance") is the IR name for a [[Judgment Lists|judgment list]]: a set of (query, document, relevance grade) triples, stored in TREC's standard format. The term belongs in this glossary because the qrels are what an LLM judge *produces*. Every agreement figure above compares two sets of qrels.

The idea of reusable test collections also depends on it. Voorhees (2000) showed that swapping in a different set of human qrels changes many individual labels while the comparison between systems mostly holds. LLM-generated qrels are taken seriously for the same reason. Datasets such as [[MS MARCO]], [[BEIR]] and [[TREC-COVID]] ship their judgments as qrels.

**Qrels are incomplete.** A document that is not in the qrels is *unjudged*, not irrelevant. Treating the two as the same thing gets worse as retrievers improve. [Better Retrievers, Worse Labels](https://arxiv.org/abs/2610.40966) tested a common shortcut in conversational RAG: treating "no gold document retrieved" as "not enough evidence to answer". The setup was RETECO's RECOR track, with four retrievers ranging from nDCG@10 0.183 to 0.591. Moving from the weakest retriever to the strongest:

- the share of no-gold contexts that actually contained the answer rose from 28% to 72%
- the shortcut's precision fell from 0.68 to 0.10 (0.70 to 0.21 under the blind audit)
- a Qwen3-4B reader answered 62–67% of these "false misses" correctly, against 23–30% of genuinely insufficient contexts

The shortcut understated answerability AUROC by up to 0.19. On the strongest retriever it put every reader near chance, while labels based on the context's content did not. MTRAG, whose judgments come from human annotators, showed the same decline (0.72 → 0.50). The fix is to judge each retrieved context by what it contains rather than by whether it appears in the qrels. That is exactly the job an LLM judge does.

## Learning to Adjudicate

Adjudication is the step in building a judgment list that resolves disagreement between judges, by voting or by expert review. Allegro's dataset used dual blind annotation, with an expert arbitrating whenever the two annotators disagreed.

**Learning to adjudicate** means *training* the resolver instead of hand-writing a rule such as majority vote. The term is the title of [Learning to Adjudicate: Verifier-Guided Multi-Agent Reasoning for E-Commerce Relevance](https://arxiv.org/abs/2611.02758) (Shu et al., 2026), which proposes **CADRE**:

- **Specialists.** Three expert agents look at product attributes, user intent and business rules. They share a frozen Qwen3-14B backbone but work in separate contexts.
- **Verifier.** A separately trained Qwen3-14B verifier weighs their evidence and decides the label. It is trained with multi-turn GRPO and replays past trajectories that reached the correct label.
- **Selective debate.** The verifier starts a debate only when the experts' first labels disagree.
- **Data.** 97,707 multilingual query–product pairs with seven relevance/mismatch classes, 18,710 of them held out for testing.

| Method | Accuracy | Macro-F1 |
|---|---|---|
| Single Qwen3-14B, trained with context | 0.7961 | 0.6402 |
| Verifier, no debate | 0.8311 | 0.7729 |
| CADRE, selective debate | 0.8334 | 0.7766 |

The learned verifier also beat an oracle allowed to pick any correct expert label (0.8334 vs. 0.8051), so it sometimes got right a case that every expert got wrong. Debate added little: 0.23 points of accuracy over the same verifier without debate. Whether that is worth the extra inference cost should be measured case by case. The paper reports accuracy and F1 against human labels only, with no κ, human agreement, calibration or ranking stability.

A smaller version of the same idea is in [[Classic ML to Cope with Dumb LLM Judges]]. [[Doug Turnbull]] treats the verdicts of several narrow single-attribute LLM judges as features and trains a scikit-learn decision tree to predict human pairwise preference on [[Wayfair]]'s WANDS. Both have the same limit: an adjudicator is only as good as the labels it is fitted to. [[Adapting Jev to Your Domain with GEPA]] is a warning that unchecked labels teach a corpus's annotation habits rather than the truth.

## Distilled student

A distilled student is a small, cheap model trained to copy an expensive judge (the teacher). [[Knowledge Distillation]] makes the teacher's behaviour affordable at serving or full-catalogue scale.

[[Etsy]]'s three-tier cascade is the clearest worked case: an o3 LLM annotator, then a teacher model, then a BERT-based two-tower student that adds less than 10 ms at serving time. All three were scored on the same golden set, with macro F1 of 0.72 / 0.71 / 0.65. In [[Staged Judging]] the student is the last step, and it means the next cycle needs fewer escalations.

The open risk: a student can reproduce the teacher's systematic errors as faithfully as its correct calls, and then serve them at production scale. Nothing in a distillation cascade detects that ([[Adversarial Relevance Judgment]]). Check the student against human labels, not only against the teacher.

CADRE uses the same pattern, with a multi-agent system as the teacher. A distilled mBERT student rose from 0.7456 to 0.7809 accuracy when it was trained on the experts' and verifier's reasoning as well as the labels. In a seven-day online test it gained 1.69% RPM and 0.76% CTR (relative), plus 0.3 points of human-assessed relevance satisfaction ([Learning to Adjudicate](https://arxiv.org/abs/2611.02758)).

## Calibration

Calibration has two meanings in this area, and they are easy to confuse.

- **[[Judge Calibration]]**: before trusting a judge, measure it against a reference judge (usually a person) on a fixed random sample of pairs, separately for each collection and prompt. Report agreement at both the pair level (ordinal α, exact and within-one agreement, which way the judge leans, a confusion table) and the rank level (τ over per-query nDCG@10, plus how far the scores shift). A low α with a high τ is the tape-measure case. In a cascade, calibrate the expensive judge against people, then use it as the reference for the cheap judge. Agreement between two models, neither of which has been checked, says nothing about either. See [[Calibrate Before You Trust]].
- **Probability calibration**: whether a judge's stated confidence matches how often it turns out right ([[Calibrated Relevance Probability]], [[Expected Calibration Error]], [[Brier Score]]). This is what makes escalation cut-offs meaningful. "Route everything below 0.4 to a human" only works if 0.4 really means 40%.

## Jury

A jury is a panel of several judges whose verdicts are combined into one label. The panel can be different models, different prompts, or narrow judges that each look at one aspect. It is the "panel vs. single judge" comparison from the inter-judge list.

Juries show up in three forms in the vault:

- **Ensemble of cheap judges.** In [[Staged Judging]], when the cheap judges agree confidently their verdict is accepted, and when they split the pair escalates. Disagreement inside the jury serves as a measure of difficulty.
- **Learned weighting.** [[Classic ML to Cope with Dumb LLM Judges]] and CADRE replace the vote with a trained combiner (see Learning to Adjudicate).
- **Different ways of asking.** [[Benchmarking LLM-based Relevance Judgment Methods]] compares binary, graded, [[Pairwise Relevance Evaluation|pairwise]] and nugget-based judgments, and finds that the choice changes the answer.

Two 2026 preprints show what goes wrong:

- **A jury of weak judges is still weak.** In [Better Retrievers, Worse Labels](https://arxiv.org/abs/2610.40966), a jury of Qwen3-4B, Phi-4-mini, SmolLM3-3B and Granite-3.3-8B agreed with itself at Fleiss' κ of only 0.26. Each member agreed with the audit at κ 0.18–0.25. The jury still reproduced the paper's main finding, that the shortcut degrades as retrievers improve. Weak judges can be good enough for the direction of a result while useless for individual labels ([[Levels of Judge Agreement]]).
- **Keep judges independent until you combine them.** In CADRE ([Learning to Adjudicate](https://arxiv.org/abs/2611.02758)), letting experts see earlier reports cut accuracy by 1.14 points, and letting them see each other while revising cut it by 1.76. A third debate round added only 0.05. The authors blame premature convergence, which removes the complementary evidence that made the panel worth having.

A jury is only as independent as its members. Judges that share a base model or training data can be confidently wrong together. CADRE's experts all run on one backbone, so their diversity is in perspective, not in model family. A jury's agreement with itself is self-consistency at the panel level. It does not show correctness, and the jury still needs [[Judge Calibration|calibrating]] against people. Better Retrievers, Worse Labels shows the pattern: two primary judges from different model families, plus a blind audit by a third family, two independent audit runs that agreed on 97% of items, and adjudication. Its authors still note that the audit is a model, not fresh human review.

## How the Terms Fit Together

A judge, or a jury of judges, produces **qrels**. **Self-consistency** checks that the judge is stable. **Inter-judge agreement**, ordinal or binary and reported at each level, checks whether it matches a reference. **Calibration** is that check done carefully, per prompt and collection, before the judge is trusted. Disagreements are **adjudicated**, by hand or by a learned combiner. A **distilled student** then reproduces the result cheaply, along with any errors it inherited.

## Related Concepts

- [[LLM as Judge]] · [[Levels of Judge Agreement]] · [[Inter-Annotator Agreement]] · [[Kendall Rank Correlation]]
- [[Judge Calibration]] · [[Calibrated Relevance Probability]] · [[Expected Calibration Error]] · [[Brier Score]]
- [[Judgment Lists]] · [[ESCI Label Scheme]] · [[Pairwise Relevance Evaluation]]
- [[Staged Judging]] · [[Knowledge Distillation]] · [[Adversarial Relevance Judgment]] · [[Prompt Sensitivity]]
- [[Hallucination Detection]] · [[NDCG]]
- [[Macro and Micro Averaging]] — macro vs micro F1 when scoring a judge against golden labels

## Related Topics

- [[Search Quality Assurance]] · [[Model Selection and Fine-Tuning Evaluation]]

## Related Articles

- [[Do LLM Judges Actually Agree With Us]] — [[Andrew Kornilov]]; the agreement levels and the who-judges-whom comparisons
- [[Calibrate Before You Trust]] — [[Andrew Kornilov]]; judge calibration in practice
- [[How Etsy Uses LLMs to Improve Search Relevance]] — self-consistency sampling and the annotator → teacher → student cascade
- [[Automating Search Relevance Assessment at Scale with LLM-as-a-Judge]] — [[Joanna Marhula]], [[Mateusz Sidor]]; ordinal κ against per-class F1, and expert arbitration
- [[Classic ML to Cope with Dumb LLM Judges]] — [[Doug Turnbull]]; a jury of narrow judges with a learned adjudicator
- [[Benchmarking LLM-based Relevance Judgment Methods]] — [[Negar Arabzadeh]], [[Charles L. A. Clarke]]; binary, graded, pairwise and nugget-based judging compared

- [Better Retrievers, Worse Labels: How Incomplete Relevance Judgments Distort Abstention Evaluation in Conversational RAG](https://arxiv.org/abs/2610.40966) — Ivan Kochergin, Vasily Konovalov (arXiv preprint, 2026); ordinal vs. binary κ, a small-model jury, and qrels that degrade as retrievers improve
- [Learning to Adjudicate: Verifier-Guided Multi-Agent Reasoning for E-Commerce Relevance](https://arxiv.org/abs/2611.02758) — Shi Shu et al. (arXiv preprint, 2026); CADRE, a learned verifier over specialist judges, and the cost of letting judges see each other

## People

- [[Andrew Kornilov]] · [[Doug Turnbull]] · [[Joanna Marhula]] · [[Mateusz Sidor]] · [[Negar Arabzadeh]] · [[Charles L. A. Clarke]]
