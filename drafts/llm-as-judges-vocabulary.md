# LLM as Judges: A Vocabulary

*Nine words people use about AI relevance judges, and what each one actually claims.*

The same handful of words comes up again and again in papers and blog posts about LLM judges: agreement, self-consistency, calibration, jury, adjudication.

Each one names a different claim. "The judge agrees with humans", "the judge is consistent" and "the judge is calibrated" are each checked a different way, and a judge can pass one and fail the other two.

So here is the vocabulary as I understand it, with the evidence behind each term.

## Agreement

Agreement is how often two judges give the same answer. It is never one number, because two judges can be compared at four levels:

1. **Label**: do they put the same grade on the same query–document pair?
2. **Score**: do they give each search approach roughly the same metric value?
3. **Ranking**: do they put the approaches in the same order?
4. **Decision**: do they lead to the same call, the same winner, the same "ship it"?

These levels barely move together. Think of a tape measure that reads five centimetres short. Every plank comes out wrong, but the longest plank is still the longest. If all you need is to sort the planks, the broken tape measure works.

A Portuguese legal search study (NormasTCU, 2026) shows exactly this: Cohen's κ of 0.32–0.53 on individual labels, alongside a Kendall τ of 0.9 or more on the nDCG@10 and MRR leaderboards. The reverse also happens. Otero, Parapar and Barreiro (2025) found LLM judges producing false "significant difference" calls *at high τ*.

So when someone quotes an agreement figure, the first question is: at which level?

## Inter-judge agreement

Inter-judge agreement is agreement between two specific judges. The term only means something once you say which two:

- human vs. human: is the task objective at all?
- LLM vs. human: does the model copy *this* human?
- LLM vs. LLM: would another model have said something else?
- prompt vs. prompt
- the same model run twice
- a panel vs. a single judge

The bar is not 1.0. It is how often your own human raters agree with each other. If your annotators agree at κ 0.6, asking a model for κ 0.8 makes no sense. Typical reported figures: human–human κ above 0.5 on binary relevance, LLM–human κ around 0.3–0.5.

Two warnings. Matching one human is not the same as matching your users. And three LLMs that agree may simply share a blind spot.

## Ordinal and binary agreement

The grading scale determines which agreement statistic is valid.

**Binary** agreement is on a relevant/not-relevant scale, where every disagreement costs the same. **Ordinal** agreement is on a graded scale, such as 0–3, where confusing 0 with 3 is worse than confusing 0 with 1. Ordinal scales need weighted statistics, such as quadratic-weighted κ or ordinal Krippendorff's α.

The usual mistake is to quietly collapse graded labels into binary. Agreement goes up, and the distinctions nDCG depends on disappear.

But sometimes binary is the honest scale. In *Better Retrievers, Worse Labels* (Kochergin and Konovalov, 2026), judges rating context sufficiency on three labels reached κ of only 0.38–0.49. Collapsed to sufficient/insufficient, the same pairs reached 0.59–0.79. The judges argued about "partial" vs. "sufficient" but mostly agreed on the decision that mattered: answer or abstain.

So pick the scale that matches the decision the labels feed. And report raw agreement next to κ, because a change in label prevalence can drag κ down while the judges agree just as often in practice.

## Self-consistency

Self-consistency is agreement of a judge with itself: the same model and prompt, run more than once on the same pair.

It measures stability, not correctness. A judge can give the same wrong answer every time. Its advantage is that it needs no reference labels, which makes it useful as a cheap signal. Etsy samples its LLM annotator several times and plans to send only the inconsistent cases to humans.

## Qrels

Qrels ("query relevance") is the IR word for a judgment list: query, document, grade. They belong in this vocabulary because qrels are what an LLM judge *produces*. Every agreement number above compares two sets of them.

One trap matters more as retrieval improves. A document missing from the qrels is *unjudged*, not irrelevant. *Better Retrievers, Worse Labels* tested the shortcut "no gold document retrieved, so the evidence is insufficient" on four retrievers. Moving from the weakest to the strongest, the share of no-gold contexts that actually contained the answer rose from 28% to 72%, and the shortcut's precision fell from 0.68 to 0.10.

Better retrievers find relevant documents that nobody judged. The fix is to judge each context by what it contains, which is the job an LLM judge does.

## Learning to Adjudicate

Adjudication is how disagreements get resolved: a vote, or an expert who makes the final call. Allegro's relevance dataset, for example, used two blind annotators and an expert arbiter whenever they disagreed.

*Learning* to adjudicate means training the arbiter instead of hand-writing a rule. The term comes from a 2026 paper by Shu et al. that proposes CADRE. Three specialist agents look at product attributes, user intent and business rules, and a trained verifier makes the final decision. The verifier starts a debate only when the specialists disagree.

On 18,710 held-out e-commerce pairs, the verifier reached 0.8334 accuracy. That beat an oracle allowed to pick any correct specialist label (0.8051), so the verifier sometimes got right a case every specialist got wrong. The debate itself added little: about a quarter of a point over the same verifier without it.

Doug Turnbull showed a smaller version of the same idea: several "dumb" single-attribute LLM judges, with a decision tree learning how much to trust each one.

## Distilled student

A distilled student is a small, cheap model trained to copy an expensive judge, the teacher. It makes the judge affordable at full-catalogue or serving scale.

Etsy runs a three-step chain: an o3 annotator, then a teacher model, then a BERT student that adds under 10 ms. Macro F1 drops at each step: 0.72, 0.71, 0.65. CADRE distils into an mBERT student, which improved from 0.7456 to 0.7809 accuracy when it learned from the reasoning as well as the labels.

The risk is that a student copies the teacher's systematic mistakes as faithfully as its good calls, and then serves them at scale. So check the student against people, not only against the teacher.

## Calibration

Calibration has two meanings in this area, and they get confused constantly.

**Judge calibration** means measuring an AI judge against a reference you trust, usually a person, on a fixed sample of pairs, for each prompt and each collection. Report pair-level agreement (α, exact and within-one, which way the judge leans) and rank-level agreement (τ over per-query nDCG). A low α with a high τ is the tape-measure case.

**Probability calibration** means a judge that says "70% relevant" is right about 70% of the time. This is what makes thresholds meaningful. "Send everything below 0.4 to a human" only works if 0.4 really means 40%.

## Jury

A jury is a panel of judges whose verdicts are combined into one label: different models, different prompts, or narrow judges that each look at one aspect.

Two 2026 results show where juries go wrong.

**A jury of weak judges is still weak.** In *Better Retrievers, Worse Labels*, a jury of four small open models agreed with itself at Fleiss' κ of only 0.26. Yet it still reproduced the paper's main finding, the direction of the effect. Weak judges can be good enough for direction while useless for individual labels.

**Keep judges independent until you combine them.** In CADRE, letting specialists see earlier reports cut accuracy by 1.14 points, and letting them see each other while revising cut it by 1.76. The authors blame premature convergence: the judges stop contributing the different evidence that made a panel worth having.

A jury is only as independent as its members. Judges built on the same base model can be confidently wrong together, and CADRE's specialists all share one backbone. A jury agreeing with itself is self-consistency at panel level. It still has to be checked against people.

## How the words fit together

A judge, or a jury of judges, produces qrels. Self-consistency tells you it is stable. Inter-judge agreement, ordinal or binary, at a stated level, tells you whether it matches a reference. Calibration is that check done carefully before you trust it. Disagreements get adjudicated, by hand or by a learned arbiter. A distilled student then reproduces the result cheaply, along with whatever mistakes it inherited.

None of these words means "the judge is right". Each one covers a single, narrower claim.

## References

- [Better Retrievers, Worse Labels: How Incomplete Relevance Judgments Distort Abstention Evaluation in Conversational RAG — Ivan Kochergin, Vasily Konovalov (arXiv, 2026)](https://arxiv.org/abs/2610.40966)
- [Learning to Adjudicate: Verifier-Guided Multi-Agent Reasoning for E-Commerce Relevance — Shi Shu et al. (arXiv, 2026)](https://arxiv.org/abs/2611.02758)
- [Automating Search Relevance Assessment at Scale with LLM-as-a-Judge — Joanna Marhula, Mateusz Sidor, Allegro](https://blog.allegro.tech/2026/08/automating-search-relevance-llm-as-a-judge.html)
- [How Etsy Uses LLMs to Improve Search Relevance — Etsy Code as Craft](https://www.etsy.com/codeascraft/how-etsy-uses-llms-to-improve-search-relevance)
- [Classic ML to Cope with Dumb LLM Judges — Doug Turnbull](https://softwaredoug.com/blog/2025/01/21/llm-judge-decision-tree)
- [Improving retrieval with LLM-as-a-judge — Jo Kristian Bergum, Vespa](https://blog.vespa.ai/improving-retrieval-with-llm-as-a-judge/)
