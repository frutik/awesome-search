# Can Jev Rank? Can Jev Grade? Does Jev Know When Its Grading Is Unreliable?

*Three questions that sound simple but aren't, inspired by my work on bringing Jev into Quepid.*

I've been spending quite a bit of time with Jev recently.

It started with [bringing Jev into Quepid (PR #1802)](https://github.com/o19s/quepid/pull/1802), the open-source tool for search relevance evaluation. That led to more work, including two new pull requests, [#1826](https://github.com/o19s/quepid/pull/1826) and [#1827](https://github.com/o19s/quepid/pull/1827).

Somewhere along the way, I realized that I was mixing up three rather different problems.

We often talk about whether an AI model is a *good relevance judge*. But what does that actually mean?

Does it put the best products at the top? Does it assign the same grades as a human? Can it recognize when its own judgment isn't reliable?

These abilities are related, but one doesn't guarantee the others.

And that distinction matters when we start using AI judges to evaluate — or even improve — real search systems.

## 1. Can Jev rank?

Imagine someone searches for **"red running shoes"**.

Our search engine returns four products. We ask Jev to evaluate each one and get the following hypothetical relevance probabilities:

| Product | Probability |
|---|---|
| Red Nike running shoes | 0.45 |
| Red Adidas running shoes | 0.40 |
| Blue Nike running shoes | 0.25 |
| Red leather dress shoes | 0.15 |

Let's assume this is exactly how a human relevance expert would order them.

Jev has done a perfect job of ranking these four products.

But there's something strange about the numbers.

Every probability is below 0.5.

If we apply the usual 0.5 threshold for a yes-or-no relevance decision, Jev classifies all four products as irrelevant.

How can it be a good reranker and a bad classifier at the same time?

Because **knowing which product is better isn't the same as knowing whether a product is good enough**.

A reranker primarily needs to order results correctly. It doesn't necessarily need perfectly calibrated probabilities or a useful binary decision threshold.

This is more than a theoretical curiosity.

In a recent [Elastic Search Labs experiment](https://www.elastic.co/search-labs/blog/ecommerce-search-reranking-llm-alternative-jev), Dustin Coates tested Jev as a reranker using 250 queries from Amazon's Shopping Queries Dataset.

The best reported approach improved nDCG@10 from 0.9351 to 0.9565.

That's a modest improvement over a baseline that was already very good. Still, it suggests that Jev can contribute useful ranking signals.

There's an important limitation: the benchmark compared different ways of ordering the same set of judged products. It didn't demonstrate what would happen in a complete production search pipeline, where retrieval determines which products are available to rerank in the first place.

Around the same time, Doug Turnbull explored a related idea in [Bag of Decisions](https://softwaredoug.com/blog/2026/10/08/bag-of-decisions).

I particularly like the idea of building a ranking score from several decisions rather than asking a model for one mysterious relevance number.

For example, instead of simply asking whether a product is relevant, we might ask:

- Is it the product type the shopper requested?
- Does it satisfy the important constraints?
- Is it an exact match or a reasonable alternative?

Then we combine those signals into a ranking score.

This gives us something interesting: a ranking policy that we can inspect, adjust, and experiment with.

But it also creates a new question. How should we combine those decisions, and how do we know that the resulting ranking is actually better?

For that, we need a proper ranking experiment.

## 2. Can Jev grade?

Now imagine a different task.

We're not trying to reorder search results. We're trying to evaluate them.

This is familiar territory in Quepid, where relevance judgments are used to measure search quality and compare experiments.

Suppose we use a four-point relevance scale:

- **0** — Irrelevant
- **1** — Slightly relevant
- **2** — Relevant
- **3** — Perfect match

With Jev's multiclass `Choice` output, we can get a probability for each grade.

For example:

| Grade | Probability |
|---|---|
| 0 | 2% |
| 1 | 8% |
| 2 | 75% |
| 3 | 15% |

Jev picks grade 2.

But what if a human relevance expert assigns grade 3?

It's a disagreement, although perhaps not a particularly serious one.

Now imagine Jev assigns grade 0 to a product that a human considers a perfect match.

That's much more concerning.

Simple accuracy treats both predictions as wrong, but the mistakes are very different.

There's another possibility worth considering: perhaps Jev consistently gives excellent products a grade of 2 rather than 3.

It might still rank those products correctly. But its grading would be systematically different from the human rubric.

And if we use those grades to evaluate search improvements, that difference matters.

We could end up optimizing our search engine for the judge's preferences instead of the relevance criteria we intended.

So I'd want to look beyond overall accuracy.

Where do the disagreements happen? Are they mostly between neighboring grades? Does Jev systematically avoid extreme grades? Does it struggle with particular query types?

And perhaps the most uncomfortable question: **is the model misunderstanding our grading instructions, or are our instructions simply not good enough?**

Human relevance experts don't always agree either. Sometimes a disagreement tells us more about an ambiguous rubric than about the quality of the judge.

That's why grading deserves its own evaluation, separate from ranking.

## 3. Does Jev know when its grading is unreliable?

This is the question that interests me most.

While working on the Jev integration, I started looking at something beyond the final predicted grade: the distribution of probabilities.

That led to my earlier article, [Can We Outsmart JEV? Not All Uncertainty Is the Same: Neighbour Splits vs. Scale Splits](https://www.linkedin.com/pulse/can-we-outsmart-jev-all-uncertainty-same-neighbour-splits-kornilov-zexce/).

The main observation was that two judgments can have similar confidence scores while expressing very different kinds of uncertainty.

Consider:

| Grade | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| Judgment A | 2% | 48% | 47% | 3% |
| Judgment B | 45% | 5% | 5% | 45% |

Judgment A is essentially saying:

*"I'm not sure whether this is slightly relevant or relevant."*

Judgment B is saying:

*"This is either completely irrelevant or a perfect match."*

Those are not the same problem.

The first looks like an ordinary disagreement about the boundary between two neighboring grades.

The second might suggest an ambiguous query, missing product information, confusing instructions, or a model that has misunderstood the task.

In the earlier article, I explored why collapsing these distributions into a single confidence number can hide useful information.

But that led to a bigger question.

**Just because Jev expresses uncertainty, does that mean its uncertainty is actually useful?**

A model can confidently make mistakes.

It can also be uncertain about predictions that turn out to be correct.

What we really want to know is whether confidence helps us identify judgments that are more likely to be wrong.

If it does, we can use that information to build a more efficient judging system.

If it doesn't, the confidence numbers might look impressive without being particularly helpful.

And that brings me to the experiments I'd like to run.

## Three experiments I'd like to run in Quepid

The advantage of working on an evaluation tool is that these questions don't have to remain theoretical.

We can test them against real relevance judgments.

### Experiment 1: Ranking

Take queries with human-judged products, ask Jev to score each query-product pair, and use those scores to rerank the results.

Then compare the ranking with the original search engine and other reranking approaches using nDCG@10.

There's one important detail: **we need enough human judgments to evaluate the results fairly**.

If Jev moves previously unjudged products into the top 10, we can't simply assume they're irrelevant. We'd need additional judgments or a carefully designed evaluation set.

I'd also want to compare different scoring approaches: a single relevance probability, a weighted combination of multiclass probabilities, and potentially several more specific yes-or-no decisions.

Which approach produces the best ranking?

### Experiment 2: Grading

Take the same query-product pairs and ask Jev to assign relevance grades.

Compare those grades with human judgments, paying particular attention to the nature of disagreements.

Confusing a 2 with a 3 is not the same as confusing a 0 with a 3.

We could also experiment with different grading instructions.

Perhaps a more precise rubric improves agreement. Perhaps certain categories require additional context.

The goal is to understand not only how often Jev disagrees with humans, but why.

### Experiment 3: Knowing when to ask for help

This is where things get especially interesting.

Suppose we have 10,000 query-product pairs to judge.

We could send all of them to an expensive LLM. Or we could let Jev handle the first pass and escalate only the difficult cases.

Something like:

**Jev → More capable LLM → Human judge**

But how do we decide which judgments need escalation?

We could start with a simple confidence threshold.

Take judgments with human labels, sort them by confidence, and measure agreement as we accept an increasing percentage of them.

What happens when we accept only the most confident 50%?

What about 70% or 90%?

Does agreement deteriorate predictably?

Then we could try something more sophisticated, inspired by my earlier article.

Instead of looking only at confidence, what if we consider *where the probability is distributed*?

Perhaps uncertainty between neighboring grades is less problematic than uncertainty between opposite ends of the scale.

Or perhaps that intuition turns out to be wrong.

Either result would be useful.

Finally, we could introduce a second judge and measure the trade-off between cost and quality.

For example, can Jev handle most judgments while an expensive LLM processes only the cases where Jev is least reliable?

How much does agreement with human experts improve? And how much does that improvement cost?

There's a subtle but important point here: **the best escalation strategy is not necessarily the one that escalates the most uncertain judgments according to Jev**.

It's the one that most effectively identifies cases where a second judge can actually improve the result.

Those might not be exactly the same cases.

## Maybe we don't need one perfect judge

The more I work on Jev, the less convinced I am that comparing AI judges using a single benchmark tells us enough.

One model might be excellent at reranking but only moderately good at reproducing human relevance grades.

Another might produce better grades but less useful confidence estimates.

And a relatively inexpensive judge might be particularly valuable as the first step in a larger evaluation pipeline, even if it isn't the most accurate model available.

That doesn't mean we should build complicated systems for the sake of complexity.

Maybe a single judge is good enough.

Maybe a simple confidence threshold works just as well as a sophisticated uncertainty measure.

Maybe some clever escalation strategy adds more complexity than value.

These are exactly the kinds of things I'd like to find out.

What started as adding Jev support to Quepid has gradually turned into a much broader exploration of how AI judgments should be evaluated, calibrated, and combined.

I don't have definitive answers yet.

But I think separating these questions will help us understand where Jev — and perhaps other decision-oriented models — can be most useful.

Because the most accurate judge isn't necessarily the best judge for every job.

And sometimes the most useful thing a judge can do is recognize when we should ask someone else.

---

## Further reading

- [Bringing Jev into Quepid — PR #1802](https://github.com/o19s/quepid/pull/1802)
- [Ongoing Quepid work — PR #1826](https://github.com/o19s/quepid/pull/1826) and [PR #1827](https://github.com/o19s/quepid/pull/1827)
- [Can We Outsmart JEV? Not All Uncertainty Is the Same — Andrew Kornilov](https://www.linkedin.com/pulse/can-we-outsmart-jev-all-uncertainty-same-neighbour-splits-kornilov-zexce/)
- [Using Jev as a Search Reranker — Dustin Coates, Elastic Search Labs](https://www.elastic.co/search-labs/blog/ecommerce-search-reranking-llm-alternative-jev)
- [Bag of Decisions — Doug Turnbull](https://softwaredoug.com/blog/2026/10/08/bag-of-decisions)
