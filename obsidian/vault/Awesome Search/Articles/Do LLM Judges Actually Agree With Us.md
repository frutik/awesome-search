---
type: article
title: "Do LLM Judges Actually Agree With Us?"
source: "https://www.linkedin.com/pulse/do-llm-judges-actually-agree-us-andrew-kornilov-aezfe/"
author:
  - "[[Andrew Kornilov]]"
published: 2026-09-04
created: 2026-09-04
concepts:
  - "[[LLM as Judge]]"
  - "[[Levels of Judge Agreement]]"
  - "[[Inter-Annotator Agreement]]"
  - "[[Prompt Sensitivity]]"
  - "[[Adversarial Relevance Judgment]]"
  - "[[Kendall Rank Correlation]]"
  - "[[Statistical Significance in Search Evaluation]]"
  - "[[Staged Judging]]"
  - "[[Judgment Lists]]"
  - "[[Search Evaluation]]"
  - "[[NDCG]]"
  - "[[Position Bias]]"
  - "[[Knowledge Distillation]]"
topics:
  - "[[Search Quality Assurance]]"
  - "[[Duality in Measuring Search]]"
  - "[[Relevance Program Setup]]"
  - "[[E-commerce Search]]"
companies:
  - "[[Etsy]]"
  - "[[Allegro]]"
  - "[[eBay]]"
tags:
  - article
  - llm-judge
  - search-evaluation
  - inter-annotator-agreement
  - e-commerce
  - survey
---

# Do LLM Judges Actually Agree With Us?

**[[Andrew Kornilov]]** surveys the evidence on whether [[LLM as Judge|LLM relevance judges]] agree with human assessors, and argues the question as usually posed is malformed. Judges work well for some evaluation tasks and fail badly on others; the useful move is separating which is which.

---

## The Central Claim: Agreement Has Four Levels

The organising idea is that **"the judges agree" names four different things, and they do not move together**:

1. Do they put the same label on the same result?
2. Do they give each approach roughly the same score?
3. Do they put the approaches in the same order?
4. Do they lead to the same *decision* — same winner, same significance call, same ship-it call?

Two judges can disagree over thousands of individual labels and still both produce "B beats A beats C", because judge noise lands on every approach in much the same way and cancels out in the aggregate. That cancellation is why the field got excited: the judge does not have to be right about each result, only about which approach wins.

The article's warning is that a matching leaderboard hides differing definitions of relevance, blowups on specific query types, the top two approaches swapping places, false statistical significance, and systematic preference for certain kinds of retrieval.

A terminology note runs throughout: **"approach"** is used for what the IR papers call a **"system"** — one version of a search engine being compared against another.

## Who Is Judging Whom

"Judge vs. judge" covers several distinct comparisons that answer different questions: human vs. human (is the task objective at all?), LLM vs. human (does the model copy *this* human?), LLM vs. LLM (would another model have said something else?), prompt vs. prompt, same model run twice (self-consistency), and panel vs. single judge. Matching one human is not matching users in general; three LLMs agreeing may mean three models share a blind spot; and consistency is not correctness.

## The Economics

The motivating driver was never accuracy — it was cost. A human assessor judgment runs $0.50–$5.00 and takes days to weeks; an LLM judgment runs ~$0.001–$0.01 and takes minutes. A thousand queries with ten candidates each is $5,000–$50,000 and a couple of weeks with people, versus tens of dollars and twenty minutes with a model.

But cheap per unit is not cheap. At e-commerce scale — billions of searches a year, hundreds of billions of query-product pairs — judging everything with a frontier model is impossible, so teams sample. Sampling tracks aggregate quality fine and is useless for coverage work: mining [[Hard Negative Mining|hard negatives]] across a full catalogue, or catching a regression on one tail query.

The way out is architectural, and the article follows [[Towards Scalable Relevance Engineering|Andreas Wagner]]'s account: judge *far less* first — use [[Implicit Judgments|behavioral signals]] to prune the pair space (~93% cleared), then cascade cheap quantized bi-encoder judges that settle 75–85% of the remainder, escalating only disagreements, then [[Knowledge Distillation|distill]] ~100,000 LLM judgments into a small CPU model. See [[Staged Judging]].

Two cautions attach: two weak judges sharing a base model can be confidently wrong together, so audit the auto-accepted sample and not only the escalations; and pruning inherits whatever [[Position Bias|position bias]] shaped the behavioral signal underneath it.

## Humans Never Agreed Either

Relevance disagreement predates LLMs. Voorhees (2000) showed that swapping in a different set of human judgments changes many individual labels while the comparison between systems mostly holds — the founding insight behind reusable test collections. Bailey and colleagues (2008) qualified it: who judges matters, and test collections are *not* fully robust to swapping judges of very different expertise.

The consequence for setting a bar: the standard for an LLM is not "agrees perfectly with one human" but "lands inside the range humans already vary by, **and** doesn't change the calls you are making."

## How the Evidence Developed

- **Faggioli et al. (2023)**, *Perspectives on LLMs for Relevance Judgment*, laid out a human-machine collaboration spectrum and found the pattern that has held since: labels agree only so-so, leaderboards agree a lot. Their worry list — prompt sensitivity, model bias, evaluation eating its own tail, contamination, opacity, and relevance quietly becoming whatever the model thinks it is — remains unsolved.
- **Zheng et al. (2023), MT-Bench**, is the general LLM-as-a-judge reference point: strong judges reach over 80% agreement with human preferences, "the same level of agreement between humans." It named four failure modes that all land in search — position bias, verbosity bias (a repetitive-list padding attack fooled Claude-v1 and GPT-3.5 over 90% of the time, GPT-4 only 8.7%), self-enhancement bias, and limited reasoning.
- The article argues IR has an advantage over the general LLM-judge field: free-text answer grading often has no ground truth, so human agreement is the only check available, whereas IR can ask the downstream question *does the leaderboard come out the same*.
- **Thomas et al. (2024)** reported Bing-scale LLM labeling "as good as human labellers" and better than third-party workers — while also reporting that not just systematic prompt changes but "simple paraphrases" move accuracy.
- **UMBRELA (2024)** reproduced that assessor openly with GPT-4o across TREC Deep Learning 2019–2023, with leaderboards tracking the human ones closely.
- ***Judging the Judges* (2025)** released 42 sets of LLM labels from eight teams, enabling judge-to-judge comparison. Three findings: judge configuration changes the answer a lot; two judges can produce nearly the same leaderboard while labeling very differently; and a single average agreement number says nothing about *which direction* a judge errs.

### TREC 2024 RAG — the strongest pro-automation result

**Upadhyay et al. (2024)** ran four assessment processes over the TREC 2024 RAG Track (77 runs, 19 teams): NIST's full manual process plus three leaning on UMBRELA. On nDCG@20, nDCG@100 and Recall@100 the automated leaderboards lined up closely with the fully manual one. Two details: humans were **stricter** than the model, and human-in-the-loop assistance "does not appear to increase correlation with fully manual assessments." The caveat is what the test measures — ordering 77 wildly different runs, which is much easier than separating two nearly-tied approaches.

### Why a matching leaderboard is not the win it looks like

- **Otero, Parapar and Barreiro (2025)** found LLM judgments "unfair at ranking top-performing systems," with "an exceedingly high rate of false positives regarding statistical differences" — the judge declares your new approach a winner, with confidence, when it isn't. Directly relevant to anyone running offline A/B-style comparisons; see [[Statistical Significance in Search Evaluation]].
- **Clarke and Dietz (2024)** point out that an LLM relevance judge is itself just another relevance-scoring approach, so it can be gamed — and if retrieval and judge share a base model, you are grading your own homework.
- **Balog, Metzler and Qin (2025)** report "the first empirical evidence of LLM judges exhibiting significant bias towards LLM-based rankers," limited ability "to discern subtle system performance differences," and confirmed leniency relative to human judges.
- **SynDL (2024)** — 1,988 queries, 637,063 LLM labels — reports the opposite on the ranker-bias point: their setup "does not favour language model approaches." The article flags this as an unsettled disagreement rather than resolving it.

### Judges can be tricked

**Alaofi et al. (2025)** found LLMs "more likely to label passages as relevant compared to human judges," and "highly influenced by the presence of query words in the passages under assessment, even if the wider passage has no relevance to the query." Some models followed instructions written *inside the passage being judged*. Average agreement scores look healthy the whole time. The article flags marketplaces — where third parties write the item text and have money riding on ranking — as the acute case.

### There is no single "LLM judge"

**Arabzadeh and Clarke (2025)** compared binary, graded, pairwise and two nugget-based ways of asking across TREC DL 2019–2021 and ANTIQUE: how you ask changes the answer, so "use an LLM judge" names a category, not a method (see [[Benchmarking LLM-based Relevance Judgment Methods]]). **Farzi and Dietz (2025)** decompose relevance into exactness, coverage, topicality and contextual fit, producing better leaderboards and inspectable grades — and showing that some disagreement is not model error but an unstated definition of relevance (see [[Criteria-Based LLM Relevance Judgments]]).

### Outside the English passage bubble, 2025–2026

- **Mohtadi et al. (2025)** judged full documents against LLM-written summaries: "comparable stability in systems' ranking," but "systematic shifts in label distributions and biases that vary by model and dataset."
- **The TREC Podcast reassessment (2026)** — five LLMs, 18,284 query-segment pairs, 91,420 labels — found human-vs-LLM leaderboard agreement (Kendall's τ) of 0.81–0.84 on the 2020 track with top approaches holding, dropping to 0.60–0.72 on 2021 with ordering "much more volatile… including the *top* ranking systems." Same models, same method, one year apart. On the 22 most-disagreed cases (deliberately selected, not sampled), three IR experts sided with the LLMs (Krippendorff's α 0.71–0.86) and showed *negative* agreement with the original assessor (α −0.55 to −0.77). That establishes the answer key can be wrong and is contestable on exactly the cases where a judge looks like it is failing — not that keys are broadly wrong.
- **Keller et al. (2026)** found judges given only a short query "judge many more documents relevant and have a lower agreement" than judges given a topic description — and that generating that description automatically still helps.
- **NormasTCU (2026)**, Brazilian Portuguese legal search over 14,469 documents, reached only fair-to-moderate human agreement (Cohen's κ 0.32–0.53, MAE 0.46–0.66 on a 0–2 scale) while nDCG@10 and MRR leaderboards hit Kendall correlations of 0.90+ and P@10/R@10 were shakier — the cleanest demonstration that label agreement, ranking agreement, and *which metric you chose* are three separate things.

## Product Search: the Shape Transfers, the Failure Moves

For [[E-commerce Search|e-commerce]], relevance stops being topicality. The useful grading is substitutability — the [[Amazon ESCI Dataset|ESCI]] (Exact / Substitute / Complement / Irrelevant) shape — which is a judgment about shopping intent rather than about text, and it relocates the hard boundary.

That relocated boundary is where judges fall over. [[Automating Search Relevance Assessment at Scale with LLM-as-a-Judge|Allegro's RAT]] is the best-documented case: a 380K+ multilingual judgment dataset from 30 experts across 13 departments and four languages, dual blind annotation with expert arbitration. Their local quantized judge reached quadratic-weighted Cohen's κ of 0.69 on Polish — genuinely good for a four-level ordinal scale — with per-class F1 around 0.94 on exact matches and 0.83 on complements, against **0.51 and 0.33** on separating "highly substitutable" from "substitutable."

The article is careful about how to read that pair of numbers: an overall weighted κ and a per-class F1 are different quantities on different scales, and F1 has no universal chance baseline, so 0.33 does not mean "coin flip." What it means is poor discrimination on the boundary the merchandising team actually argues about, while the judge is excellent on the calls nobody needed help with — and an overall κ of 0.69 would never have revealed it.

Prompting folklore also fails to transfer: Allegro found that *removing* few-shot examples improved both accuracy and inter-rater agreement, while structured reasoning and domain-specific business logic in the prompt helped, and category/department metadata did nothing because product names already carried it.

Commerce relevance is additionally time-varying and business-defined. [[How Etsy Uses LLMs to Improve Search Relevance|Etsy]] maintains an evolving labeling guideline because relevance drifts with culture — "face masks" meant costume masks before 2020 and protective masks after. There is no stable ground truth to converge on, and the judge is frozen at its training cutoff.

The pattern across documented commercial deployments is that the LLM is never the final judge: Etsy anchors it with human golden labels and distills it into a servable model, Allegro built the 380K human dataset first and used it to validate, and eBay binds the judge to "a meticulous evaluation framework grounded in business metrics." **Humans define the standard, the LLM scales it, business metrics keep it honest** — a more modest claim than "LLM judges match humans," and a more useful one.

## What to Measure

The article gives a nine-level measurement table — raw labels, chance-corrected agreement, graded labels, per-class breakdown, judge-vs-judge ordering, same-judge repeatability, approach scores, leaderboard order, and actual decisions — each with the statistic to compute and the way it lies to you. Three rules fall out:

- **Don't quietly collapse graded labels to binary.** Squashing 0/1/2/3 into relevant/not manufactures agreement and discards the distinctions [[NDCG]] depends on.
- **Never post a κ without the label distribution and confusion matrix.** A uniformly lenient judge can have a perfectly normal κ, and the leniency is what bites.
- **Leaderboard correlation needs a top-weighted companion.** Overall τ hides the region you care about — the two or three nearly-tied candidates.

## What Number Is Good Enough

Two conventions circulate. **[[Kendall Rank Correlation|Kendall's τ]] ≥ 0.9** comes from Voorhees, who proposed treating two evaluation schemes correlating at 0.9+ as equivalent, partly because you cannot really be more precise than that; below ~0.8 you are seeing genuine reordering. It is a convention, twenty-odd years old, never re-derived for LLM judges. **Cohen's κ bands** (fair 0.21–0.40, moderate 0.41–0.60, substantial 0.61–0.80) come from a 1977 biometrics paper by Landis and Koch, have nothing to do with IR, and are vocabulary rather than a gate.

Which one gates depends on the decision. NormasTCU cleared τ ≥ 0.9 while sitting at κ 0.32–0.53: passing the ranking threshold said nothing about label quality and vice versa. If you only need a broad ranking of approaches, stable decision agreement can suffice with mediocre label agreement — the Voorhees insight, still standing. If labels will be read by humans, reused as training data, or used to diagnose specific queries, weak label agreement is disqualifying on its own and no leaderboard correlation rescues it.

The article then offers a decision-dependent rubric (flagged as the author's synthesis, not a citable result), whose sharpest row is **choosing between two close approaches: high aggregate correlation alone cannot validate that decision**, because Otero's false positives occur *at high τ* — adjudicate the deciding slice with humans.

Three practical rules are offered as worth more than any threshold:

1. **Report per class, not just overall** — publish the confusion matrix and per-class precision/recall/F1 beside any headline number; if you want a chance-corrected per-class figure, compute one-vs-rest binary κ and say so.
2. **Measure your pipeline's run-to-run variation first** — rerun the whole judging process and recompute the *final metrics and decisions*, not just the labels. If the gap between two approaches is routinely reversed or swallowed by that spread, the judge cannot distinguish them however good the human correlation looks. This is not the same as label self-disagreement: an 8% label flip rate and a 0.015 nDCG gap are different quantities, so the variation has to be propagated through to the metric.
3. **Set the bar against human-human agreement on your own data, not against 1.0** — if your annotators agree at κ 0.6, demanding κ 0.8 from a model is incoherent.

## How to Run It

Don't crown one model as The Judge. Use three or more different model families (three versions of one vendor's model does not count); run each judgment more than once, since temperature 0 is not determinism; keep several humans on a stratified slice; and record model version, access date, exact prompt, decoding settings and truncation.

Stratify the sample by query type, difficulty, ambiguity, domain, result length and original grade; load up on close calls rather than obvious cases; pull results from different *kinds* of retrieval approach; include adversarial items (query-word stuffing, instructions hidden in text, misleading summaries, very long documents); and swap option order systematically in pairwise judging.

Report all three layers — items (label distributions, confusion matrices, weighted agreement, error direction, per-class breakdown), systems (score bias, leaderboard correlation, top-weighted agreement, leader movement), and decisions (winner, pairwise significance, effect direction, whether the gap matters). Then have someone review disagreements blind, not to declare a winner but to *sort* them: ambiguous topic, missing context, human error, model error, different reading of the scale, gamed content, or two defensible ideas of what relevant means. Each needs a different fix.

## Open Questions

What happens to an evaluation when the judge model is deprecated and swapped; which disagreements actually change a decision, and how to model agreement when several answers are legitimate; how to catch someone gaming the judge when they write the item text and profit from ranking; when humans should judge everything versus review disagreements versus audit a sample versus just write the criteria; whether cascade-and-distill preserves the judge's *biases* along with its accuracy (barely studied, and the ~93%/75–85% cascade figures are one team's unreplicated production numbers); and how to evaluate against a target that moves with season, culture and stock while the judge's training data does not.

## Seven Things That Look Solid

1. **Label agreement is never great** — fair-to-moderate is normal, moving with collection, model, prompt, scale, context and assessors. Tight task specification helps.
2. **Leaderboards hold up better than labels** — item-level errors cancel or hit every approach equally, but that is a result about one level, one metric, one collection.
3. **It breaks exactly where you need it most** — sorting 77 messy runs is fine; separating two close strong approaches is not. Exact-vs-garbage is fine; substitute-vs-slightly-worse-substitute is weak.
4. **The errors have a shape** — too generous, over-reacting to query words, prompt-sensitive, following embedded instructions, position and length preferences, possibly favouring approaches like themselves (SynDL disputes this). Because it is systematic, **more labels from the same judge do not wash it out**.
5. **The humans aren't a gold standard either** — when the LLM disagrees with the key, "the LLM screwed up" is a hypothesis, not the conclusion.
6. **Model-vs-model is under-studied** — most papers fix human judgments as truth; few cross model families, prompts and repeated runs to ask whether the conclusion would have changed with a different judge.
7. **In documented industry deployments, nobody replaced the humans** — the academic question is whether the model can replace the assessor; the deployed answer is that it multiplies them.

The closing reframe: stop asking *does the LLM agree with the human*, and start asking *if I swap the judge, the prompt, or just run it again — which of my conclusions survive, and which move?* That is answerable, and it treats disagreement as information about your evaluation.

---

## Related Concepts

- [[LLM as Judge]] — the practice the whole article assesses
- [[Levels of Judge Agreement]] — the four-level label/score/ranking/decision hierarchy this article organises itself around
- [[Inter-Annotator Agreement]] — κ, weighted κ, Krippendorff's α, and the human-human baseline the bar should be set against
- [[Prompt Sensitivity]] — paraphrasing the prompt moves the numbers
- [[Adversarial Relevance Judgment]] — keyword stuffing and instructions hidden inside judged documents
- [[Kendall Rank Correlation]] — the leaderboard-agreement statistic and the τ ≥ 0.9 convention
- [[Statistical Significance in Search Evaluation]] — where the false-positive result bites
- [[Staged Judging]] — the prune-cascade-distill answer to judging economics
- [[Judgment Lists]] — what judges produce
- [[NDCG]] — the metric leaderboard agreement is usually computed on
- [[Position Bias]] — one of the four MT-Bench failure modes, and a contaminant of behavioral pruning
- [[Knowledge Distillation]] — how Etsy and Wagner turn expensive judgments into servable models

## Related Topics

- [[Search Quality Assurance]] — the practice this is evaluation infrastructure for
- [[Duality in Measuring Search]] — human judgment and behavioral signal as complements, not substitutes
- [[Relevance Program Setup]] — the decision-dependent rubric is a program-design question
- [[E-commerce Search]] — where relevance becomes substitutability and the judge's failure moves

## Related Articles

- [[Automating Search Relevance Assessment at Scale with LLM-as-a-Judge]] — [[Joanna Marhula]], [[Mateusz Sidor]]; Allegro RAT, the κ 0.69 / F1 0.33 case study central to this article
- [[How Etsy Uses LLMs to Improve Search Relevance]] — golden labels → LLM teacher → distilled student
- [[Towards Scalable Relevance Engineering]] — [[Andreas Wagner]]; the judge-economics argument this article builds §2 on
- [[Benchmarking LLM-based Relevance Judgment Methods]] — [[Negar Arabzadeh]], [[Charles L. A. Clarke]]; "how you ask changes the answer"
- [[Criteria-Based LLM Relevance Judgments]] — [[Naghmeh Farzi]], [[Laura Dietz]]; decomposed relevance and the unstated-definition diagnosis
- [[Classic ML to Cope with Dumb LLM Judges]] — [[Doug Turnbull]]; a complementary response to judge unreliability
- [[Search Quality Assurance with AI as a Judge]] — [[Tao Ruangyam]]; Zalando's production judge pipeline

## Companies

- [[Etsy]] — golden labels anchoring an LLM teacher, distilled to a servable student
- [[Allegro]] — 380K multilingual judgment dataset; per-class breakdown of judge weakness
- [[eBay]] — LLM judge bound to business metrics as a proxy for seller judgment

## People

- [[Andrew Kornilov]] — author
- [[Andreas Wagner]] — judge economics: prune, cascade, distill
