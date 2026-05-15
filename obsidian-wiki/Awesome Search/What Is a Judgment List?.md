---
title: "What Is a Judgment List?"
source: "https://softwaredoug.com/blog/2021/02/21/what-is-a-judgment-list"
author:
  - "[[Doug Turnbull]]"
published:
created: 2026-05-15
description: "Judgment lists prevent search whack-a-mole. They provide a safety net for search, allowing you to innovate quickly on relevance with a high degree of confidence."
tags:
  - "clippings"
---
As a search practitioner, I’ve seen eyes open up when I introduce one particular relevance topic: **judgment lists**. This topic is a great way to learn about search relevance evaluation. I’ll define judgment lists, how they’re used to evaluate search, and finally go through the many FAQs that come up whenever I introduce this idea to others.

## Judgment lists: alleviating your search manager’s stress one search at a time!

When you look at your company’s search results, you might have a reaction:) “This stinks” you think. You fire off an email to the search team, asking them to fix your query. The manager looks at your email with frustration: solving this one problem could upset the search apple cart. They worry a fix for your query could easily worsen millions of others.

Without good testing in place, relevance improvements become a perpetual game of search whack-a-mole. Fixing one issue creates three more. Because of this lack of confidence, search teams often get too conservative, uncertain about new ideas, as there’s no safety net in place to catch search relevance issues.

A judgment list provides such a safety net. A judgment list defines a document’s relevance for a query. Perhaps, for example, we have a simple grading scheme of 0 (irrelevant) or 1 (relevant). If we’re building a movie search engine, we might create the following judgment list:

```
query,      movie,                            grade
star wars, “Star Wars: A New Hope”,           1
star wars, “Return of The Jedi”,              1
star wars, “Blair Witch Project”,             0
star wars, “A Star Is Born”,                  0
star trek, “Star Trek Into Darkness”,         1
star trek, “Star Trek II: The Wrath of Khan”, 1
star trek, “Sense and Sensibility”,           0
star trek, “Forrest Gump”,                    0
...
```

Above, “Star Wars: A New Hope” is graded as 1, or ‘relevant’, for a `star wars` search. While “Blair Witch Project” is considered irrelevant. “Sense and Sensibility” is irrelevant for a search for `star trek` but “Star Trek II: The Wrath of Khan” is relevant.

With such a judgment list, we hope to turn search relevance evaluation from a subjective, “looks good to me” exercise to a more systematic evaluation practice.

To see what I mean, what if our movie search engine returns the following for the query `star wars`:

1. Blair Witch Project
2. A Star Is Born
3. Star Wars: A New Hope
4. Return Of The Jedi

Using our judgment list, we know the first two results are irrelevant and the last two relevant. We can replace the listing above with each document’s grade for `star wars`:

1. 0
2. 0
3. 1
4. 1

In other words, two irrelevant results, above two relevant ones. The ideal case, of course, would push the relevant results above the irrelevant ones, like so:

1. 1
2. 1
3. 0
4. 0

## Putting a number on relevance

How can we put a number on how good a query is doing, given a judgment list? What metric would put a low number on the first ranking `[0, 0, 1, 1]` and a higher number on the second one `[1, 1, 0, 0]`.

Search experts have developed several metrics using judgment lists to measure relevance. [Discounted Cumulative Gain](https://en.wikipedia.org/wiki/Discounted_cumulative_gain) is a popular choice. It defines a per-rank multiple (the discount) weighing the top results more than the lower ones. It then computes a gain for each position (discount \* grade). The final DCG is the sum of the gains, up to the rank depth we want to evaluate.

| Rank | Grades for ‘star wars’ | Discount (1/rank) | Gain = Discount\*Grade | Accumulated Gain |
| --- | --- | --- | --- | --- |
| 1 | 0 | 1.0 | 0 | 0.0 |
| 2 | 0 | 0.5 | 0 | 0.00 |
| 3 | 1 | 0.33 | 0.33 | 0.33 |
| 4 | 1 | 0.25 | 0.25 | 0.58 |

(Note I’m using `1/rank` discount for simplicity, most of the time the calculation is a bit more complicated - see the [wiki article](https://en.wikipedia.org/wiki/Discounted_cumulative_gain) for variants)

Compare this poor ranking with the ideal case’s DCG:

| Rank | Grades for ‘star wars’ | Discount (1/rank) | Gain = Discount\*Grade | Accumulated Gain |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1.0 | 1.0 | 1.0 |
| 2 | 1 | 0.5 | 0.5 | 1.5 |
| 3 | 0 | 0.33 | 0.0 | 1.5 |
| 4 | 0 | 0.25 | 0.0 | 1.5 |

In the ideal case, the DCG of the top 4 results (or DCG@4) is 1.5 because it has better results in more important, higher up positions. As we see, this beats the first algorithm’s DCG@4 of 0.59!

## Iterating with confidence

A judgment list gives your team permission to iterate quickly on relevance improvements. It gives you a test harness for the relevance of your search system without needing A/B or user testing. In the past I’ve called it [test-driven relevancy](https://opensourceconnections.com/blog/2013/10/14/what-is-test-driven-search-relevancy/) because it has the same effect as a unit test: it lets you tweak ranking algorithms quickly and confidently. At your laptop, you can try a new solution, run a ‘test’ (like those at [Quepid](http://quepid.com/)), examine regressions, rinse and repeat.

For example, let’s say you managed to fix the `star wars` query but all other query’s DCG declined precipitously. You instantly know not to move forward with the fix. This arms search teams with quantitative tools to solve problems, and push back on fixing one-off queries when they hurt the overall system.

Even more importantly, it gives search teams permission to innovate. With a fast, robust safety net in place, teams can venture into new, uncharted territory and try new things, without tanking their search. We’re moving to a world where applications increasingly looks like this relevance one: a relatively small algorithm controls the response of every system input. You need a way to be bold. The only way to do that is with algorithmic guardrails. A judgment list gives you that confidence.

## Frequently asked questions about judgments

Now that you’ve seen this indispensable search tool, I’ll jump into the questions that crop up most frequently when introducing judgment lists.

### Where do judgment lists come from?

Ah, this is really the million dollar question. Judgment quality and curation is a huge topic of search teams, consuming a lot of resources. I’ll mention three methods, pointing you at some external resources:

- **Explicit Judgments**: in a UX-study like environment, you recruit relevance evaluators to give direct feedback on what’s relevant and not. Tito Sierra and Tara Diedrichson gave a great overview of the complexities in using human raters [in their Haystack Talk](https://haystackconf.com/2019/human-judgement/).
- **Crowdsourced Judgments**: you crowdsource judgment creation. Some manage the process via Mechanical Turk. Third party firms like [Appen](https://appen.com/) or [Supahands](https://www.supahands.ai/) also specialize in curating search relevance evaluation data.
- **Implicit Judgments**: you use the implicit behaviors of your users (clicks, purchases, etc) to generate judgments. I’d recommend [chapter 11 of AI Powered Search](http://aipoweredsearch.com/) - coming soon. In my chapter, I cover this topic extensively in the guise of machine learning training data (one application of judgments), but the lessons apply just as well to relevance evaluation.

Each of these has its pros and cons. As you’d imagine, for example, if your search application serves domain experts, and has little user traffic, implicit judgments might not have enough behavior to find patterns. However, paying to have specialists evaluate your search results, with explicit judgments, may be perfect. A general e-commerce search system is a very different beast. Here the high volume of traffic makes implicit judgments great. The broadness of the domain may also allow the average click worker to make search evaluations.

There’s no one “ground truth” here: every judgment system gives you a different view on the problem. Even within these categorizations, there are refinements and decisions. Within implicit judgments, consider: do you just use clicks? What about purchases and conversions? What are those conversions, how often do they occur? Even within this system you could build multiple views of the relevance problem.

Thus I find it’s futile to create a single golden ‘true’ judgment list to rule them all. Instead, rely on multiple evaluation systems to get different perspectives on the problem. This is why I like the term “judgment” and not “golden set” or “ground truth”.

### Implementation choices…

As alluded to earlier, there are a number of careful implementation choices to make. Should the grades be a simple binary 0 or 1 (like above). Or categorical labels like 0,1,2,3,4? Or a probabilities (0-1)? Every domain and judgment solution will be slightly different.

For example, with explicit evaluators, you might want to give them categorical labels, with clear, objective criteria established around the meaning of the label. In a job search system, maybe you’d create a scenario to go with your query, with criteria as to how likely they’d apply be to a job in the search results listing:

> You’re an out of work tractor-trailer driver. Recently, you began searching for part time work. You issued a search for `part time` as you go through the results, please answer how much energy you would put into applying for this job?
> 
> 0 - It’s not worth ever applying for this job (least relevant)
> 
> 1 - It’s unlikely I would apply for this job
> 
> 2 - It’s about 50/50 whether I’d apply for this job
> 
> 3 - I would apply.
> 
> 4 - I would put a high level of effort here. I would instantly apply, try to call the hiring manager, and do everything I could to land this job

Other scenarios, like implicit judgments, lend themselves to probabilities. For example, building judgments from clicks, a naive system could be to use Click-Thru Rate (CTR) of documents for a query (read [AI Powered Search](http://aipoweredsearch.com/) for why raw CTR might not be a good idea). CTR, and other systems turning clickstream data, produce a relevance label between 0-1, usually best interpreted as a probability.

### How do I know if my judgments are any good?

With so many subjective decisions going into judgment list creation, how do we know they’re any good? Well there’s a couple perspectives on this:

- **A/B Test Your Judgments**: A/B testing systems are built to test any change to a user-facing system to see how they impact KPIs. You can test your judgments by building a search system that shows your judgment list’s ideal ranking for every query. If such a system performs well in an A/B testing experiment, you know you’re on the right track. You can also use your judgments aggressively in a relevance experiment as a part of the solution itself to see how well they improve search.
- **Compare to other judgment methods**: Like I said there’s not one ‘true’ judgment list. We can use different systems and look for agreement and differences. There’s statistics like [Kendall’s Tau](https://en.wikipedia.org/wiki/Kendall_rank_correlation_coefficient) that help us find correlations between judgment systems. Of course it’s not black and white, more likely we’ll learn different systems carry different insights.

Important to note too that implementation bugs, like processing clickstream data incorrectly, also plague search teams. So make sure your judgments pass the ‘smell test’. Do some subjective eyeball sleuthing of whether the relevance labels are sane to ensure bug-free calculations from the underlying data.

### Why not always just show users the judgments?

If your judgments are good, why not devise a system that always shows users the best result for each query?

Actually, it might be fine to do this. In particular “signal boosting” (see [chapter 8 of AI Powered Search](http://aipoweredsearch.com/)) is one technique for promoting documents shown to be relevant for a query (or demoting those shown to be irrelevant). But it comes with limitations:

- **It’s not generalizable**: its almost certainly the case we won’t have judgments for every query coming into our system. Even examining clicks, there will be long-tail or rare queries that won’t have great data. By not using judgment to change the core ranking, signal boosting works fine to address head queries, but doesn’t help the long tail.
- **It keeps search in a (possibly low quality) ‘bubble’**: if judgments come from user clicks, and we only show users items they clicked on, you may get stuck in a local maxima. For example, if search is already not good, and users only see and thus click mediocre results, then showing them the judgments simply keeps showing them those mediocre results. It would be better to open search up to ‘explore’ some beyond the current bubble.
- **Judgments aren’t everything**: see the FAQ below. Judgments are just one perspective on relevance. Why pin search results to just to this one point of view?

So sure, you can do this, but tread carefully. And it’s always better to make general improvements to the underlying ranking algorithm whenever possible.

### What about ungraded documents in the response?

In the movie search situation above, what would have happened if we searched for ‘star wars’ and we returned a movie we don’t have grades for, such as this scenario:

1. The Fellowship Of The Ring (grade=??)
2. A Star Is Born (grade=0)
3. Star Wars: A New Hope (grade=1)
4. Return Of The Jedi (grade=1)

How could we compute DCG if we don’t know the grade of the first result!?

This could happen, for example, if our explicit raters never were asked about the relevance of “The Fellowship Of The Ring” for Star Wars. A common solution is to assign a default value when we don’t have data. With simple 0/1 judgments, we might want to just assume irrelevance (grade=0) until proven otherwise. However in other scenarios, like probabilities, we might want to have something closer to the middle of the range to reflect our uncertainty.

### What don’t judgments capture?

No model is correct, but some models are useful. Judgments are one such model. They help capture one perspective on search quality. But consider these flaws where other tools might be better suited:

- **Personalization**: my relevance for a query is not your relevance. When I search for “Star Trek” I prefer anything made with William Shatner. You might prefer “Star Trek Voyager” content and dislike everything else. Judgments assume an objective, general relevance which is not always true. Still most search systems must work pretty well for general relevance in the case that there’s little knowledge about the user.
- **Perceived relevance vs actual relevance**: it’s not enough to return relevant results, the UI has to convince the user the result is relevant for their query. If the UI fails to show me a product image, title, or otherwise fail to inspire my confidence, we might be showing the user results that objectively solve their problem, yet still fail to inspire the user to take a follow on step like a purchase.
- **Speed**: I’ve seen that faster search systems are at least thought to be more relevant. I’ve seen teams pull out all the stops to make amazingly relevant search, only to have them fail A/B tests because the fancy relevance algorithm slows search down. You can show users a perfectly relevant set of results, but if search takes several seconds to return them, that won’t matter in the end.
- **Search is greater than the sum of its relevance grades**: judgments assume users evaluate every result in isolation, and are not influenced in their perception by adjacent items. Yet this is not true. Some users explicitly look to compare and contrast, and want a diverse result set to know what their options are. [Andreas Wagner’s MICES talk](https://www.youtube.com/watch?v=xgHf9k272nc) gives a good example of how shoes being next to each other influenced user’s perception of each item’s relevance! I blogged about [diversity vs relevance](https://opensourceconnections.com/blog/2019/09/05/diversity-vs-relevance/) as well. Relevance isn’t the only criteria to consider.

## That’s a wrap!

I hope you’ve enjoyed this deep dive! If you find this interesting, and want to work with me and my team at Shopify, [get in touch with me at LinkedIn](https://www.linkedin.com/in/softwaredoug). We have tons of data to play with to make search awesome for the world’s independent merchants!

---

### Enjoy softwaredoug in training course form!

#### Starting May 18!

Signup here - [http://maven.com/softwaredoug/cheat-at-search](http://maven.com/softwaredoug/cheat-at-search) [![](https://softwaredoug.com/assets/media/2026/cheat-at-search-social.png) ](https://maven.com/softwaredoug/cheat-at-search)I hope you join me at [Cheat at Search with Agents](https://maven.com/softwaredoug/cheat-at-search) to learn use agents in search. build better RAG and use LLMs in query understanding.

---

## Related Concepts
- [[Judgment Lists]] — the concept explained in full
- [[Search Evaluation]] — judgment lists are the foundation of offline evaluation
- [[NDCG]] — DCG / nDCG computed directly from judgment grades
- [[Click Signals]] — implicit judgment source from clickstream
- [[LLM as Judge]] — modern alternative/complement to human judgment
- [[Position Bias]] — clickstream judgments are affected by position bias
- [[A-B Testing for Search]] — judgment lists provide faster alternative to A/B tests

## People
- [[Doug Turnbull]] — author; Shopify search practitioner