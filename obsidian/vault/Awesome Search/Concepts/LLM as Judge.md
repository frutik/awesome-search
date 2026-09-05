---
type: concept
title: "LLM as Judge"
aliases: ["LLM judge", "LLM-as-a-judge", "automated relevance evaluation", "LLM evaluation"]
tags:
  - concept
  - search-evaluation
  - llm
  - automation
created: 2026-05-16
---

# LLM as Judge

## Definition

Using a large language model (LLM) to evaluate the relevance of search results — as a cheaper, faster alternative to human annotators for creating [[Judgment Lists]] or running automated quality checks.

## Why LLM Judges?

Human annotation for [[Search Evaluation]] is expensive:
- Typical cost: $0.50–$5.00 per (query, document) judgment
- For 1,000 queries × 10 candidates each = $5,000–$50,000
- Turnaround time: days to weeks

LLM judgment:
- Cost: ~$0.001–$0.01 per judgment (100–1000x cheaper)
- Turnaround: minutes
- Scalable: run continuously as part of CI/CD

## How It Works

### Point-wise Scoring
Rate each (query, document) pair independently:
```python
def llm_judge_relevance(query, document, llm):
    prompt = f"""Rate the relevance of this document to the query on a scale of 0-3:
    
    Query: {query}
    Document: {document}
    
    0 = Not relevant
    1 = Marginally relevant  
    2 = Relevant
    3 = Highly relevant
    
    Return only the integer grade."""
    
    return int(llm.generate(prompt))
```

### Pairwise Comparison (Stronger Signal)
Ask the LLM which of two documents is more relevant:
```python
def llm_compare(query, doc_a, doc_b, llm):
    prompt = f"""Which document is more relevant to this query?
    Query: {query}
    Document A: {doc_a}
    Document B: {doc_b}
    Answer: A or B"""
    return llm.generate(prompt)
```
Pairwise comparison gives a stronger per-pair signal than absolute scoring — though see below: it does not follow that it gives better *system-level* rankings.

### Nugget-Based Evaluation
LLM first identifies "answer nuggets" (key facts needed to answer the query), then checks which retrieved documents contain them. This is itself a family rather than one method, and it splits two ways. **Document-agnostic** ("Exam") nuggets are derived from the query alone and turned into questions each document must answer; **document-dependent** ("AutoNuggetizer") nuggets are extracted with the documents in view. Within the latter, variants differ in which nuggets count — all of them, only the *vital* ones, or a weighted mix — and in how strictly a document must match.

## The Assessment Paradigm Is Part of the Method

The three patterns above are not interchangeable implementations of one idea. How you ask changes the labels you get, and it changes the conclusions those labels support — "use an LLM judge" names a category, not a method.

[[Negar Arabzadeh]] and [[Charles L. A. Clarke]] benchmarked the families side by side in [[Benchmarking LLM-based Relevance Judgment Methods]]. They group them three ways — traditional judgments (binary and graded, UMBRELA-style); nugget-based, in a *document-agnostic* (Exam) and a *document-dependent* (AutoNuggetizer) flavour; and pairwise preference — expanded into twelve concrete variants, run with GPT-4o over the [[TREC Deep Learning Track|TREC Deep Learning]] tracks of 2019/2020/2021 and [[ANTIQUE]]. Crucially they score each method on **two separate axes** that are usually reported as one:

1. **Agreement with human labels** — does the judge grade this query-document pair the way a human would?
2. **Agreement with human system rankings** — does a leaderboard built from the judge's labels order retrieval systems the way a human-labelled one does?

No method wins both:

- **Pairwise preferences** align best with human labels — "perhaps because they directly compare two documents".
- **Graded and binary pointwise** labels agree best with system rankings. Kendall τ on DL-19/20/21: UMBRELA 0.920 / 0.894 / 0.890 and binary 0.869 / 0.922 / 0.904, against 0.911 / 0.852 / 0.816 for preferences (human labels themselves: 0.953 / 0.956 / 0.916). Nugget variants are generally weaker here — the poorest at 0.685 — though not uniformly: Exam-Graded_max reaches 0.881 on DL-19, above binary.

Their conclusion — "methods prioritizing alignment with human labels may not inherently optimize for agreement with system rankings, and vice versa" — has a direct practical consequence. **Pick the paradigm to match the question.** Judging whether *this document* is relevant and deciding which of two *systems* is better are different tasks, and an agreement figure quoted without saying which one was measured does not mean much. Their reference points are also worth keeping in view: human-human κ can be above 0.5 on binary assessment, with LLM-human κ typically 0.3–0.5 depending on the scale.

## Multi-Criteria Judgments

A different response to the same unreliability: rather than change *how* you ask, decompose *what* you are asking about. [[Naghmeh Farzi]] and [[Laura Dietz]] propose the Multi-Criteria framework in [[Criteria-Based LLM Relevance Judgments]], on the observation that an unconstrained relevance prompt yields "not only incorrect predictions but also outputs that are difficult for humans to interpret."

Four dimensions, each scored 0–3 by its own prompt:

- **Exactness** — how precisely the passage answers the query
- **Topicality** — whether the passage is about the same subject as the whole query
- **Coverage** — how much of the passage discusses the query and related topics
- **Contextual fit** — whether the passage supplies relevant background or context

The four grades are then aggregated into one 0–3 label either by a second LLM call that sees all four scores, or by summing them and mapping the total through fixed thresholds. Evaluated on [[TREC Deep Learning Track|TREC DL]] 2019/2020 and [[LLMJudge]] (built on TREC DL 2023) with LLaMA-3-8B, LLaMA-3.3-70B and FLAN-T5-large, it improved system-ranking performance over direct grading; the LLaMA-3-8B configuration placed first on Spearman correlation in the LLMJudge challenge.

The payoff is as much **interpretability** as accuracy, and that is what makes it useful day to day. A single holistic grade gives no account of itself; four criteria give a grade you can argue with, and they force the evaluation designer to say what "relevant" is supposed to mean for this collection. Much judge-human disagreement then turns out not to be model error at all — it is an unstated definition, with judge and assessor weighting exactness against coverage differently and nobody having decided which should win.

Costs are real: roughly 5.4× the runtime of direct prompting with LLaMA-3-8B (though only ~1.3× with FLAN-T5-large), and a systematic **leniency** — where judge and human diverged sharply, the judge scored the passage higher about 92% of the time.

## Vespa's LLM Judge for Retrieval

Vespa's blog post demonstrates using an LLM to evaluate first-stage retrieval quality:
1. For each query, generate an "ideal answer" with the LLM
2. Judge retrieved documents: does this document contain information needed for the ideal answer?
3. Aggregate to compute system-level NDCG approximation

Key result: LLM judgments correlate well (Spearman's ρ ≈ 0.85–0.90) with human judgments for factual queries.

## "Do the Judges Agree?" Is Four Questions

The question the field is usually posed — does the LLM agree with the human — conflates four claims that do not move together: whether the two put the same **label** on the same pair, whether each retrieval approach gets the same **score**, whether the approaches come out in the same **order**, and whether the same **decision** follows (same winner, same significance call, same ship-it).

The decoupling runs both ways. Two judges can disagree over thousands of individual labels and still both produce the same leaderboard, because judge error that lands evenly on every approach cancels out of the ordering — the founding insight behind reusable test collections, and the reason LLM judges were taken seriously at all. But a matching leaderboard also survives things you would want it to catch: false statistical significance on close pairs, your top two approaches swapping, and a systematic thumb on the scale for particular kinds of retrieval.

NormasTCU (2026), on Brazilian Portuguese legal search, is the cleanest demonstration: Cohen's kappa of 0.32-0.53 on labels while nDCG@10 and MRR leaderboards cleared Kendall tau 0.9 — and P@10/R@10 were shakier still, making *which metric you chose* a third independent axis. Measure at least the label level and the decision level, and say which one any quoted agreement figure refers to. See [[Levels of Judge Agreement]].

## Setting the Bar

Two conventions circulate and neither is a law. **Kendall's tau >= 0.9** comes from Voorhees (2000) as a threshold for treating two evaluation schemes as equivalent; it is twenty-odd years old and has never been re-derived for LLM judges. **Cohen's kappa bands** (fair 0.21-0.40, moderate 0.41-0.60, substantial 0.61-0.80) come from a 1977 biometrics paper and have nothing to do with IR — vocabulary, not a gate.

Which one gates depends on the use. For broad ranking of a diverse field, stable decision agreement can be enough even with mediocre labels. Where the labels will be read by humans, reused as training data, or used to diagnose specific queries, weak label agreement is disqualifying on its own. And for choosing between two close approaches, high aggregate correlation cannot validate the decision at all — Otero's false positives occur *at* high tau — so the deciding slice needs human adjudication.

The bar itself should be set against human-human agreement on your own data rather than against 1.0. If your annotators agree at kappa 0.6, demanding kappa 0.8 from a model is incoherent. See [[Inter-Annotator Agreement]].

## Limitations

1. **Positional bias**: LLMs prefer the first document presented
2. **Length bias**: LLMs often favor longer documents
3. **Self-citation bias**: LLMs may prefer documents stylistically similar to their training data
4. **Hallucination**: LLM may recall facts not in the document and rate it highly
5. **Calibration**: absolute scores are unreliable; relative pairwise comparisons are better
6. **Cost at scale**: even cheaper than humans, still non-trivial at millions of judgments
7. **Underspecified relevance**: an unconstrained prompt never states which aspect of relevance is being graded, so some judge-human disagreement is a definition gap rather than model error
8. **Paradigm sensitivity**: the same model over the same pairs gives materially different labels depending on whether it is asked binary, graded, pairwise or nugget-style
9. **Prompt sensitivity**: not only systematic prompt changes but "simple paraphrases" move accuracy, so the exact prompt is part of the instrument — see [[Prompt Sensitivity]]
10. **Gameable**: a judge is itself a relevance-scoring model, and query-word stuffing or instructions embedded in the judged document can win a favourable grade without any gain in real relevance — see [[Adversarial Relevance Judgment]]
11. **False significance on close comparisons**: judges are "unfair at ranking top-performing systems," with a high rate of false positives on statistical differences, and this happens at high leaderboard correlation rather than instead of it

### The errors are systematic, so more labels don't fix them

The failure list above is not noise. Leniency, over-reaction to query words, prompt sensitivity, following embedded instructions, position and length preferences, and possible favouritism toward LLM-built rankers (which SynDL disputes) all have a *shape*. Collecting more labels from the same judge samples the same bias more precisely rather than averaging it away. Crossing model families, prompts and repeated runs is the response; more volume from one configuration is not.

## The Economics Problem

Limitation 6 above deserves its own treatment, because it is the constraint that decides whether an LLM judge is a research demo or a production system.

Per-judgment cost is only cheap relative to humans. At e-commerce scale — billions of annual searches, hundreds of billions of query-document pairs — judging everything with a frontier model is not expensive, it is impossible. Most teams respond by **sampling**: judge a few thousand pairs and generalize. That is adequate for tracking aggregate quality and inadequate for anything requiring coverage, such as mining [[Hard Negative Mining|hard negatives]] across a full catalogue or catching per-query regressions in the tail.

The architectural answer is [[Staged Judging]]: prune the pair space with [[Implicit Judgments|behavioral signals]], let cheap quantized judges settle the easy majority, escalate only disagreement to the LLM, and [[Knowledge Distillation|distill]] the LLM's judgments into a small production model. See [[Towards Scalable Relevance Engineering]] for a worked implementation.

Note that this is an axis **orthogonal to judge quality**. Most of the literature — and most of the articles below — optimizes how closely a judge agrees with humans. A 95%-accurate judge you cannot afford to run produces no judgments at all, which is strictly worse than a 90% judge with full catalogue coverage.

## Best Practices

- Match the **assessment paradigm to the question**: pairwise comparisons when judging individual documents, graded pointwise scoring when the output is a system-level comparison
- Run multiple LLM calls per judgment and take majority vote
- Validate on a small set of human judgments before trusting LLM judges — and say which axis you validated on, label agreement or system ranking
- Consider **decomposing relevance into named criteria** rather than asking for one holistic grade, when you need the judge's reasoning to be inspectable
- Use a capable LLM (GPT-4, Claude) — cheaper models have significantly worse calibration

## Related Concepts

- [[Pointwise Relevance Evaluation]] — score each item independently; best agreement with human *system rankings*
- [[Pairwise Relevance Evaluation]] — LHS/RHS comparison; best agreement with human *labels*
- [[Listwise Relevance Evaluation]] — rank full candidate list; most holistic
- [[Judgment Lists]] — what LLM judges help create
- [[Search Evaluation]] — where LLM judgments are used
- [[NDCG]] — metric computed from LLM-generated grades
- [[Staged Judging]] — the cost-driven architecture for judging at catalogue scale
- [[Knowledge Distillation]] — turning expensive judgments into a servable model
- [[RAG]] — LLM judge also used for RAG faithfulness/relevancy evaluation
- [[Agentic Search]] — LLM verification step is a form of LLM judgment
- [[Semantic Relevance]] — the intent-based signal LLM judges are used to scale, alongside engagement-based relevance
- [[Levels of Judge Agreement]] — label, score, ranking and decision agreement, and why they decouple
- [[Inter-Annotator Agreement]] — the label-level statistics and the human-human baseline the bar should be set against
- [[Prompt Sensitivity]] — the prompt as part of the measuring instrument
- [[Adversarial Relevance Judgment]] — gaming the judge, and the marketplace threat model
- [[Kendall Rank Correlation]] — the leaderboard-agreement statistic and the tau >= 0.9 convention
- [[Statistical Significance in Search Evaluation]] — where false positives appear on close comparisons
- [[Position Bias]] — the first-option preference in pairwise judging

## Related Datasets

- [[LLMJudge]] — a benchmark for judges rather than rankers; scores LLM labels on Cohen's κ against humans and Kendall τ against system rankings
- [[TREC Deep Learning Track]] — the graded, pooled NIST judgments LLM judges are most often validated against
- [[ANTIQUE]] — non-factoid QA, where "relevant" means convincing rather than fact-bearing

## Articles

- [[Benchmarking LLM-based Relevance Judgment Methods]] — [[Negar Arabzadeh]], [[Charles L. A. Clarke]]; benchmarks traditional (binary/graded), nugget-based and pairwise-preference judging over TREC DL and ANTIQUE; no paradigm wins both label agreement and system-ranking agreement
- [[Criteria-Based LLM Relevance Judgments]] — [[Naghmeh Farzi]], [[Laura Dietz]]; Multi-Criteria framework decomposing relevance into exactness, coverage, topicality and contextual fit for interpretability
- [[LLM-as-a-Judge When to Use Reasoning CoT and Explanations]] — [[Aparna Dhinakaran]]; explanation-first pattern; CoT has mixed evidence
- [[Using LLMs to Amplify Human Labeling and Improve Dash Search Relevance]] — [[Dmitriy Meyerzon]]; LLM calibrated on human labels → 100x scale-up; DSPy for prompt optimization; context-aware evaluation with tool use
- [[Search Quality Assurance with AI as a Judge]] — [[Tao Ruangyam]]; Zalando production pipeline; NER-clustered test queries; GPT-4o; ~$250/run for 1,500 segments × 25 results; pre-launch market validation
- [[Classic ML to Cope with Dumb LLM Judges]] — [[Doug Turnbull]]; per-attribute LLM signals as ML features → decision tree; 96.7% precision on 40% of pairs
- [[Automating Search Relevance Assessment at Scale with LLM-as-a-Judge]] — [[Joanna Marhula]], [[Mateusz Sidor]]; Allegro's RAT framework; 380K+ multilingual judgment dataset; few-shot examples hurt accuracy; migration to local Gemma judge cut inference cost 60%
- [[How Etsy Uses LLMs to Improve Search Relevance]] — [[Yuqing Zhang]], [[Congzhe Su]], [[Susan Liu]]; LLM annotator anchored to human golden labels, scaled via a three-tier [[Knowledge Distillation|distillation]] cascade into a real-time production judge
- [[Do LLM Judges Actually Agree With Us]] — [[Andrew Kornilov]]; landscape survey from Voorhees (2000) to 2026, separating four levels of agreement, and finding that in every documented industry deployment humans define the standard, the LLM scales it, and business metrics keep it honest

## People

- [[Andrew Kornilov]] — the four-level agreement framing
- [[Negar Arabzadeh]] — benchmarking judgment paradigms
- [[Charles L. A. Clarke]] — benchmarking judgment paradigms
- [[Naghmeh Farzi]] — criteria-based judgments
- [[Laura Dietz]] — criteria-based judgments
- [[Jo Kristian Bergum]] — Vespa "Improving retrieval with LLM-as-a-judge"
- [[Daniel Tunkelang]] — traditional human judgment advocate; acknowledges LLM judges
- [[Aparna Dhinakaran]]
- [[Dmitriy Meyerzon]]
- [[Tao Ruangyam]]
- [[Doug Turnbull]]
- [[Joanna Marhula]]
- [[Mateusz Sidor]]
- [[Yuqing Zhang]]
- [[Congzhe Su]]
- [[Susan Liu]]
