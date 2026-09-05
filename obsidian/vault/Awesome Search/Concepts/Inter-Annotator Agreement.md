---
type: concept
title: "Inter-Annotator Agreement"
aliases: ["IAA", "inter-rater agreement", "Cohen's kappa", "Krippendorff's alpha", "chance-corrected agreement", "annotator agreement"]
tags:
  - concept
  - search-evaluation
  - inter-annotator-agreement
  - statistics
created: 2026-09-04
---

# Inter-Annotator Agreement

## Definition

Inter-annotator agreement measures how often two or more judges assign the same label to the same item, corrected for the agreement you would expect by chance alone. In [[Search Evaluation]] the items are query-document pairs and the labels are relevance grades, so it is the statistic that answers "would a different assessor have graded this the same way?"

It is the label-level statistic in the hierarchy described under [[Levels of Judge Agreement]], and the level people most often quote — and most often over-read.

## The Statistics

| Statistic | What it handles | Where it misleads |
|---|---|---|
| Raw agreement / accuracy | Nothing beyond counting matches | Looks excellent when 90% of items are non-relevant |
| **Cohen's / Fleiss' κ** | Agreement beyond chance | Moves with class balance; two collections are not comparable |
| **Krippendorff's α** | Multiple annotators, missing data, any measurement scale | Same class-balance sensitivity |
| **Quadratic-weighted κ** | Ordinal grades — a 0-vs-3 error counts more than 0-vs-1 | An average hides one-sided (systematically lenient) error |
| **MAE on the grade scale** | How far off, on average | Says nothing about direction |
| Per-class precision / recall / **F1** | Which distinctions the judge can actually make | F1 has no universal chance baseline — it is not on κ's scale |

## The Landis-Koch Bands Are Not a Standard

The bands everyone quotes — fair 0.21–0.40, moderate 0.41–0.60, substantial 0.61–0.80 — come from a 1977 biometrics paper by Landis and Koch. They have nothing to do with information retrieval and were offered as a convenience. They are usable as shared vocabulary and should not be used as a gate.

## Humans Are the Baseline, Not 1.0

Relevance disagreement long predates LLM judges. Voorhees (2000) showed that different sets of human judgments change many individual labels while system comparisons largely hold; Bailey and colleagues (2008) found that *who* judges matters — the person who wrote the topic, a task expert, and a random assessor are not interchangeable, and test collections are not fully robust to swapping judges of very different expertise.

The consequence is a rule about setting bars. If your own annotators agree at κ 0.6, demanding κ 0.8 from a model is incoherent. Measure human-human agreement on your own data first; that number, not 1.0, is what to ask of a machine judge. The MT-Bench framing is the same one: GPT-4's ~80% agreement with human preferences was reported as meaningful precisely because it is "the same level of agreement between humans."

## Reporting Rules

Three rules recur across the [[LLM as Judge]] literature, and each exists because a single agreement number concealed something:

**Never post a κ without the label distribution and confusion matrix.** A judge that is lenient uniformly across the board can post a perfectly normal κ. The leniency is the part that bites — LLM judges are repeatedly found more generous than human assessors.

**Report per class, not just overall.** [[Automating Search Relevance Assessment at Scale with LLM-as-a-Judge|Allegro's RAT]] is the sharpest case: quadratic-weighted κ of 0.69 overall — genuinely good for a four-level ordinal scale — against per-class F1 of 0.94 on exact matches and 0.83 on complements, but **0.51 and 0.33** on separating "highly substitutable" from "substitutable". The overall figure was excellent on the calls nobody needed help with and hid poor discrimination on the boundary the business actually argues about. Note that the overall weighted κ and the per-class F1 are different quantities on different scales; F1 0.33 does not mean "coin flip". For a chance-corrected per-class figure, compute a one-vs-rest binary κ and label it as such.

**Don't quietly collapse graded labels to binary.** Squashing 0/1/2/3 into relevant/not manufactures agreement and discards exactly the distinctions [[NDCG]] depends on. If you do collapse, report both.

## Typical Values in Relevance Judging

Reported figures are consistently modest, and vary with collection, model, prompt, grading scale, the context given to the judge, and who the humans were:

- Human-human κ can exceed 0.5 on binary assessment; LLM-human κ typically runs 0.3–0.5 depending on the scale.
- NormasTCU (2026), Brazilian Portuguese legal search: Cohen's κ 0.32–0.53, MAE 0.46–0.66 on a 0–2 scale — while its nDCG@10 and MRR leaderboards cleared Kendall τ 0.9.
- Allegro, Polish e-commerce, quadratic-weighted κ 0.69 for a local quantized judge.

Fair-to-moderate label agreement is the normal condition, not a failure state. Better agreement happens when the task is tightly specified — Keller et al. (2026) found judges given only a short query "judge many more documents relevant and have a lower agreement" than judges given a proper topic description, and that generating the description automatically still helps.

## Related Concepts

- [[Levels of Judge Agreement]] — where label agreement sits relative to ranking and decision agreement
- [[LLM as Judge]] — the judge whose agreement is usually being measured
- [[Judgment Lists]] — the labelled artifact agreement is computed over
- [[Kendall Rank Correlation]] — the ranking-level counterpart statistic
- [[Statistical Significance in Search Evaluation]] — the decision-level counterpart
- [[NDCG]] — the metric graded labels feed
- [[Search Evaluation]] — the enclosing practice

## Related Articles

- [[Do LLM Judges Actually Agree With Us]] — [[Andrew Kornilov]]; the measurement table and the reporting rules
- [[Automating Search Relevance Assessment at Scale with LLM-as-a-Judge]] — [[Joanna Marhula]], [[Mateusz Sidor]]; the κ 0.69 / F1 0.33 per-class case
- [[Benchmarking LLM-based Relevance Judgment Methods]] — [[Negar Arabzadeh]], [[Charles L. A. Clarke]]; human-human and LLM-human κ reference points
- [[Evaluating Search - Using Human Judgments]] — human assessment as the practice being measured

## Related Topics

- [[Search Quality Assurance]] — where agreement figures get quoted in practice
- [[Relevance Program Setup]] — measuring your own annotators before setting a model's bar
