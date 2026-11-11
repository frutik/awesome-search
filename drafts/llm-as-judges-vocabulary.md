# LLM as Judges: A Vocabulary

*Nine words people use about AI relevance judges, and what each one actually claims.*

*Last updated: 2026-11-10 21:22 CET*

Papers and blog posts about LLM judges keep using the same few words: agreement, self-consistency, calibration, jury, adjudication.

Each word means something different. "The judge agrees with humans", "the judge is consistent" and "the judge is calibrated" are three separate claims. Each one is tested in its own way, and a judge can pass one test and fail the other two.

I am actively involved in AI-as-judge work in Quepid, so I have to deal with all of this. Below is what each word means, as I understand it, with the evidence behind it.

## The numbers, briefly

The sections below quote a few statistics. Here is what each one means, in one or two lines.

- **Cohen's κ (kappa)**: how often two judges give the same label, after subtracting the agreement you would get by chance. 1 means perfect agreement, 0 means no better than chance. A common rough reading: 0.21–0.40 fair, 0.41–0.60 moderate, 0.61–0.80 substantial. These bands are a convention, not a pass mark.
- **Fleiss' κ**: the same idea for three or more judges at once, such as a jury.
- **Quadratic-weighted κ**: κ for graded labels. A big disagreement (0 vs. 3) costs much more than a small one (0 vs. 1).
- **Krippendorff's α (alpha)**: a close relative of κ. It works with any number of judges, missing labels and graded scales. Read it like κ.
- **Raw agreement**: the plain share of pairs where the judges gave the same label, with no chance correction.
- **Kendall's τ (tau)**: how similarly two lists are ordered. 1 means the same order, 0 means unrelated, −1 means reversed. A common convention treats τ of 0.9 or more as "the same ranking".
- **nDCG@10**: a score for one search result page that rewards putting the most relevant documents in the top 10, and near the top.
- **MRR (mean reciprocal rank)**: how high the first relevant result appears, averaged over queries. 1 means it is always first.
- **Accuracy**: the share of labels that match the reference.
- **Precision**: of the cases a rule flags, the share it gets right.
- **F1 / Macro F1**: a single score that balances catching the right cases against raising false alarms. Macro F1 averages it across all grades, so rare grades count as much as common ones.

## Agreement

Agreement is how often two judges give the same answer. It is never one number, because two judges can be compared at four levels:

1. **Label**: do they put the same grade on the same query–document pair?
2. **Score**: do they give each search approach roughly the same metric value?
3. **Ranking**: do they put the approaches in the same order?
4. **Decision**: do they lead to the same call, the same winner, the same "ship it"?

These levels can move independently. Think of a tape measure that reads five centimetres short. Every plank comes out wrong, but the longest plank is still the longest. If all you need is to sort the planks, the broken tape measure works.

A Brazilian Portuguese legal search study (NormasTCU, 2026) shows exactly this: Cohen's κ of 0.32–0.53 on individual labels, alongside a Kendall τ of 0.9 or more between the system rankings built from human and LLM labels on nDCG@10 and MRR. The reverse also happens. Otero, Parapar and Barreiro (2025) found LLM judges producing false "significant difference" calls *at high τ*, and a high overall τ hiding disagreement among the top systems.

So when someone quotes an agreement figure, the first question is: at which level?

## Inter-judge agreement

Inter-judge agreement is agreement between two distinct judges. The term only means something once you say which two:

- human vs. human: is the task objective at all?
- LLM vs. human: does the model copy *this* human?
- LLM vs. LLM: would another model have said something else?
- prompt vs. prompt
- a panel vs. a single judge

(The same judge run twice is a different thing: self-consistency, below.)

The bar is not 1.0. It is how often your own human raters agree with each other. If your annotators agree with each other at κ 0.6, a model at κ 0.8 against an adjudicated reference is not impossible, but it deserves a look: what is it matching that individual annotators don't? Typical reported figures: human–human κ can exceed 0.5 on binary relevance, LLM–human κ around 0.3–0.5.

Two warnings. Matching one human is not the same as matching your users. And three LLMs that agree may simply share a blind spot.

## Ordinal and binary agreement

The grading scale determines which agreement statistic is valid.

**Binary** agreement is on a relevant/not-relevant scale, where every disagreement costs the same. **Ordinal** agreement is on a graded scale, such as 0–3, where confusing 0 with 3 is worse than confusing 0 with 1. Ordinal scales need weighted statistics, such as quadratic-weighted κ or ordinal Krippendorff's α.

The usual mistake is to quietly collapse graded labels into binary. Agreement goes up, and the distinctions nDCG depends on disappear.

But sometimes binary is the honest scale. In *Better Retrievers, Worse Labels* (Kochergin and Konovalov, 2026), judges rating context sufficiency on three labels reached κ of only 0.38–0.49. Restricted to yes/no cases, with "partial" dropped, the same pairs reached 0.59–0.79. The judges mostly agreed on the clear answer-or-abstain calls; the disagreement sat in the partial middle. Part of that jump is simply that the hardest cases left the sample, so agreement depends on which cases you include as well as on the scale.

So pick the scale that matches the decision the labels feed. And report raw agreement next to κ, because a change in label prevalence can drag κ down while the judges agree just as often in practice.

## Self-consistency

Self-consistency is agreement of a judge with itself: the same model and prompt, run more than once on the same pair.

It measures stability, not correctness. A judge can give the same wrong answer every time. Its advantage is that it needs no reference labels, which makes it useful as a cheap signal. Etsy samples its LLM annotator several times and is exploring using that consistency to send only the hard cases to humans.

## Qrels

Qrels (query relevance judgments) is the IR word for a judgment list: query, document, grade. They belong in this vocabulary because qrels are what an LLM judge *produces*. Every agreement number above compares two sets of them.

One trap matters more as retrieval improves. A document missing from the qrels is *unjudged*, not irrelevant, even though most evaluation tools score it as non-relevant by convention. *Better Retrievers, Worse Labels* tested the shortcut "no gold document retrieved, so the evidence is insufficient" on four retrievers. Moving from the weakest to the strongest, the share of no-gold contexts that actually contained the answer rose from 28% to 72%, and the shortcut's precision fell from 0.68 to 0.10.

Better retrievers find relevant documents that nobody judged. The fix is to judge each context by what it contains, which is the job an LLM judge does.

## Adjudication

Adjudication is how disagreements get resolved: a vote, or an expert who makes the final call. Allegro's relevance dataset, for example, used two blind annotators and an expert arbiter whenever they disagreed.

*Learning* to adjudicate means training the arbiter instead of hand-writing a rule. The term comes from a 2026 paper by Shu et al. that proposes CADRE. Three specialist agents look at product attributes, user intent and business rules, and a trained verifier makes the final decision. The verifier starts a debate only when the specialists disagree.

On 18,710 held-out e-commerce pairs, the verifier reached 0.8334 accuracy. That beat an oracle allowed to pick any correct specialist label (0.8051), so the verifier sometimes got right a case every specialist got wrong. The debate itself added little: about a quarter of a point over the same verifier without it.

Doug Turnbull showed a smaller version of the same idea: several "dumb" single-attribute LLM judges, with a decision tree learning how much to trust each one.

## Distilled student

A distilled student is a small, cheap model trained to copy an expensive judge, the teacher. It makes the judge affordable at full-catalogue or serving scale.

Etsy runs a three-step chain: an o3 annotator, then a teacher model, then a BERT student that adds under 10 ms. Macro F1 drops at each step: 0.72, 0.71, 0.65. CADRE distils into an mBERT student, which improved from 0.7456 to 0.7809 accuracy when it learned from the reasoning as well as the labels.

The risk is that a student copies the teacher's systematic mistakes as faithfully as its good calls, and then serves them at scale. So check the student against people, not only against the teacher.

I wrote about training one myself in *Teaching a Small Model to Judge Like Amazon*.

## Calibration

Calibration has two meanings in this area, and they get confused constantly.

**Judge calibration** means measuring an AI judge against a reference you trust, usually a person, on a fixed sample of pairs, for each prompt and each collection, then adjusting the prompt, rubric or model where it falls short. Report pair-level agreement (Krippendorff's α, exact and within-one, which way the judge leans) and system-ranking agreement (Kendall τ between the system rankings produced by human and judge labels). A low α with a high τ is the tape-measure case.

**Probability calibration** means a judge that says "70% relevant" is right about 70% of the time. A threshold like "send everything below 0.4 to a human" can work without it, as long as low scores really do pick out more errors. That is discrimination, and it should be measured. Calibration is what lets you read 0.4 as a genuine 40%.

## Jury

A jury is a panel of judges whose verdicts are combined into one label: different models, different prompts, or narrow judges that each look at one aspect.

Two 2026 results show where juries go wrong.

**A jury of weak judges is still weak.** In *Better Retrievers, Worse Labels*, a jury of four small open models agreed with itself at Fleiss' κ of only 0.26. Yet it still reproduced the paper's main finding, the direction of the effect. Weak judges can be good enough for direction while useless for individual labels.

**Keep judges independent until you combine them.** In CADRE, letting specialists see earlier reports cut accuracy by 1.14 points, and letting them see each other while revising cut it by 1.76. The authors blame premature convergence: the judges stop contributing the different evidence that made a panel worth having.

A jury is only as independent as its members. Judges built on the same base model can be confidently wrong together, and CADRE's specialists all share one backbone. Jury members agreeing with each other is inter-judge agreement; the same jury giving the same verdict on a rerun is self-consistency at panel level. Neither replaces a check against people.

## How the words fit together

A judge, or a jury of judges, produces qrels. Self-consistency tells you it is stable. Inter-judge agreement, ordinal or binary, at a stated level, tells you whether it matches a reference. Calibration is that check done carefully before you trust it. Disagreements get adjudicated, by hand or by a learned arbiter. A distilled student then reproduces the result cheaply, along with whatever mistakes it inherited.

None of these words means "the judge is right". Each one covers a single, narrower claim.

## References

- [NormasTCU — A Brazilian Portuguese IR Dataset and an Evaluation of LLM-as-a-Judge for Relevance Assessment (arXiv, 2026)](https://arxiv.org/abs/2608.27746)
- [Limitations of Automatic Relevance Assessments with Large Language Models for Fair and Reliable Retrieval Evaluation — David Otero, Javier Parapar, Álvaro Barreiro (SIGIR 2025)](https://arxiv.org/abs/2411.13212)
- [Better Retrievers, Worse Labels: How Incomplete Relevance Judgments Distort Abstention Evaluation in Conversational RAG — Ivan Kochergin, Vasily Konovalov (arXiv, 2026)](https://arxiv.org/abs/2610.40966)
- [Learning to Adjudicate: Verifier-Guided Multi-Agent Reasoning for E-Commerce Relevance — Shi Shu et al. (arXiv, 2026)](https://arxiv.org/abs/2611.02758)
- [Automating Search Relevance Assessment at Scale with LLM-as-a-Judge — Joanna Marhula, Mateusz Sidor, Allegro](https://blog.allegro.tech/2026/08/automating-search-relevance-llm-as-a-judge.html)
- [How Etsy Uses LLMs to Improve Search Relevance — Etsy Code as Craft](https://www.etsy.com/codeascraft/how-etsy-uses-llms-to-improve-search-relevance)
- [Teaching a Small Model to Judge Like Amazon — Andrew Kornilov (Medium)](https://medium.com/@frutik/teaching-a-small-model-to-judge-like-amazon-94e69829e6b4)
- [Classic ML to Cope with Dumb LLM Judges — Doug Turnbull](https://softwaredoug.com/blog/2025/01/21/llm-judge-decision-tree)
