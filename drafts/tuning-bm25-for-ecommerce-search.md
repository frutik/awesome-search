---
type: article
title: "Tuning BM25 for E-commerce Search: Is It Worth It?"
status: draft
author:
  - "[[Andrew Kornilov]]"
tags:
  - search
  - search-evaluation
  - bm25
  - e-commerce
  - relevance-tuning
concepts:
  - BM25
  - Bayesian Optimization
  - NDCG
  - MRR
---

# Tuning BM25 for E-commerce Search: Is It Worth It?

[[BM25]] has been the default lexical ranking algorithm in [[Elasticsearch]] for a long time, and for good reason: its default parameters work surprisingly well across a wide range of datasets.

But e-commerce data is not exactly a typical document collection.

A product may have a six-word title, a brand consisting of a single token, a category hierarchy, dozens of attributes, and a description ranging from 30 words to several thousand. On top of that, merchant-provided content can contain plenty of repetition:

> running shoe, running shoes, shoe for running, women's running shoe...

So it is reasonable to ask:

**Should we tune BM25 specifically for product search?**

The short answer appears to be:

**Yes, it can make sense. But don't expect miracles.**

## What are we actually tuning?

BM25 has two main parameters that Elasticsearch exposes:

```text
k1 = 1.2
b  = 0.75
```

These are the traditional defaults.

They control two quite different things.

### `k1`: how much does repetition matter?

`k1` controls term-frequency saturation.

Imagine the query:

```text
nike running shoes
```

And two product titles:

```text
Nike Air Zoom Running Shoes
```

and:

```text
Nike Nike Running Shoes by Nike
```

The second document contains `Nike` multiple times.

BM25 gives repeated occurrences additional credit, but that credit gradually saturates. `k1` controls how quickly that happens.

Lower `k1` means:

> I mostly care whether the term is present. Repeating it doesn't tell me much more.

Higher `k1` means:

> Repeated occurrences are useful evidence that this document is particularly relevant.

That distinction becomes interesting in e-commerce because product data often contains repetition that has little semantic value.

A merchant description might contain:

```text
running shoe
running shoes
shoe for running
women's running shoe
best running shoes
```

Five occurrences of essentially the same concept don't necessarily make this a better result.

For short structured fields such as product titles, reducing the influence of term frequency can therefore make sense.

## `b`: should long fields be penalized?

`b` controls field-length normalization.

Suppose two products both contain the term `waterproof`.

One description says:

```text
Waterproof hiking jacket with detachable hood.
```

The other contains 3,000 words of manufacturer copy and mentions `waterproof` somewhere in the middle.

The occurrence in the short description is arguably stronger evidence.

BM25 accounts for this by normalizing term frequency according to field length.

At:

```text
b = 0
```

field length doesn't matter.

At:

```text
b = 1
```

length normalization has its full effect.

The default is:

```text
b = 0.75
```

That seems reasonable for prose documents.

For product data, however, it deserves some thought.

Consider these two titles:

```text
Apple iPhone 16 Pro 256GB Black
```

and:

```text
Apple iPhone 16 Pro Smartphone 256GB Black Titanium
```

Should the second product receive a noticeably lower lexical score just because its title is a little longer?

Probably not.

And there is an even bigger issue with descriptions.

One merchant may provide 50 words. Another may provide 1,500 words of excellent structured product information. Length normalization can inadvertently punish the product with better data.

## Product fields aren't all the same

This is probably the most important part of BM25 tuning for e-commerce.

There is little reason to assume that:

```text
title
brand
category
attributes
description
```

should all use exactly the same scoring behaviour.

For example, a reasonable experimental configuration might look like:

| Field | `k1` | `b` |
|---|---:|---:|
| Title | 0.8 | 0.2 |
| Brand | 0.5 | 0 |
| Category | 0.5 | 0 |
| Attributes | 0.8 | 0.2 |
| Description | 1.2 | 0.75 |

These are **not universal optimal values**. They illustrate the underlying idea.

For a brand field, term frequency is nearly meaningless.

```text
Nike
```

isn't less relevant than:

```text
Nike Nike Nike
```

Likewise, length normalization is probably not particularly useful.

For a description, both term frequency and length can carry considerably more information.

## Marketplaces are a special case

BM25 tuning may be more important in marketplaces than in tightly controlled first-party catalogs.

The reason is simple: **the content is user-published, and users may actively try to exploit the ranking model.**

If sellers can control titles, descriptions, tags, or attributes, some of them will eventually discover that repeating query terms appears to improve ranking.

You may start seeing titles like:

```text
Running Shoes Men Running Shoes Lightweight Running Sneakers Sport Shoes
```

or descriptions containing:

```text
nike shoes nike running shoes men's nike shoes nike sneakers running nike
```

From the seller's point of view, this is rational behaviour. If repetition helps ranking, people will repeat terms.

At that point, BM25 defaults are not just a relevance choice. They become part of the incentive structure of the marketplace.

A relatively high term-frequency contribution can unintentionally reward keyword stuffing.

That is where a lower `k1`, particularly on seller-controlled short fields, becomes more interesting.

For example:

```text
title       k1=0.5–0.8
brand       k1≈0.5
category    k1≈0.5
```

means that after a term has appeared once or twice, repeating it provides little additional benefit.

This doesn't eliminate search manipulation, but it reduces one obvious incentive.

Length normalization can create another kind of game.

With a high `b`, sellers may discover that shorter, aggressively optimized titles outperform longer but more informative ones. With `b` closer to zero on titles, that particular advantage becomes weaker.

So in a marketplace, I would think about BM25 tuning not only as:

> How do I maximize NDCG?

but also as:

> What behaviour does my ranking function encourage from sellers?

That is a different problem.

If ranking rewards keyword repetition, marketplace participants will eventually optimize for keyword repetition. Once that happens, your corpus itself starts changing in response to your ranking algorithm.

In that environment, reducing the term-frequency effect on seller-controlled fields can be valuable even if the aggregate offline relevance gain looks modest.

## What does real-world experience say?

This question recently came up in the search relevance community, and the answers were remarkably consistent.

[[Doug Turnbull]] discussed exactly this kind of optimization in a [[Haystack US]] 2022 talk with [[Andy Toulis]], walking through a real deployment at [[Shopify]] ([[Haystack US 2022 - Bayesian Optimization of Relevance at Shopify]]). Rather than hand-picking `k1`/`b` values, they built [[Bayesian Optimization]] into their relevance experimentation workflow — a surrogate model that searches the parameter space using far fewer offline evaluation runs than a grid search.

Applied to the product title field, it found that the default length normalization (`b`) was over-punishing longer, more descriptive titles, and settled on a much flatter curve once the search space was properly constrained. Term-frequency saturation (`k1`) barely mattered in their setup, because Shopify's BM25 variant already used binarized term frequencies rather than raw counts — there was no saturation curve for `k1` to shape.

The more interesting lesson wasn't the final parameter values — it was how the *first* optimization run went wrong. Left unconstrained, the optimizer found a shortcut: for short, single-word queries, matching an equally short product title scored artificially well, because the *training* data itself carried presentation bias — the previous, default-BM25 engine had already been surfacing those results, so clicks skewed toward them. Only after constraining the search space and controlling for that bias did the retuned configuration show validated improvements on held-out data, including a dataset labeled independently of the old production engine.

Radu Gheorghe reported a similar experience elsewhere in the search relevance community: BM25 tuning changed things, but not enormously.

That matches what I would expect.

BM25 parameters modify the behaviour of an already reasonably good lexical scoring function. They aren't fixing fundamental retrieval problems — and, per Shopify's experience, the more valuable part of the exercise may be catching what your training data is quietly teaching your optimizer, not the final parameter values themselves.

## The juice may not be worth the squeeze

This is perhaps the best way to summarize it.

If your search currently treats:

```text
title
brand
category
description
```

as roughly equivalent text fields, tuning `k1` from `1.2` to `0.9` is unlikely to save you.

You probably have much larger gains available elsewhere.

For example:

```text
title^8
brand^6
category^4
attributes^3
description^0.5
```

versus:

```text
title^2
brand
category
description
```

can matter considerably more than tiny changes in the BM25 saturation curve.

Likewise:

- exact matches
- phrase matching
- category detection
- brand recognition
- attribute extraction
- query classification
- popularity
- availability
- business rules
- semantic retrieval
- reranking

can easily dominate the relevance impact of `k1` and `b`.

So I wouldn't make BM25 tuning the first relevance project for an e-commerce search engine.

But once you have a proper evaluation setup, the economics change.

## In 2026, testing this is cheap

Historically, parameter tuning could become an engineering project of its own.

Today, there isn't much reason for it to be.

For a single BM25 configuration, you could simply test:

```python
k1 = [0.5, 0.8, 1.2, 1.6, 2.0]
b  = [0.0, 0.25, 0.5, 0.75, 1.0]
```

That's only:

```text
5 × 5 = 25 combinations
```

Run your judged query set against all 25 and compare:

```text
NDCG@10
MRR
Recall@50
```

An LLM can write most of that experiment harness very quickly.

Radu described this nicely as essentially **autoresearch restricted to a tiny parameter space**.

There are also tools specifically designed around relevance optimization. [[Max Irwin]] pointed out Quaerite, an older search relevance evaluation toolkit that can be applied to this kind of parameter optimization.

And if you're already using [[Quepid]], you have most of the important infrastructure anyway: queries, judgments and metrics.

## Don't optimize only the global metric

There is one trap here.

Suppose:

```text
k1=0.8
b=0.2
```

improves [[NDCG]]@10 from:

```text
0.612 → 0.615
```

It is tempting to conclude:

> Basically nothing happened.

But break the queries down into groups:

```text
exact product
brand
brand + category
category
attribute + category
long-tail
natural language
```

and you might discover:

```text
Exact product       +4.2%
Brand + category    +1.8%
Category            -1.1%
Long-tail            +0.3%
```

Now you have learned something useful about how your ranking behaves.

That knowledge can be more valuable than the 0.3% movement in the aggregate metric.

For marketplaces, I would add another evaluation bucket:

```text
keyword-stuffed seller content
```

because a configuration that looks equivalent on clean relevance judgments may behave very differently once sellers start trying to game it.

## Elasticsearch makes the experiment straightforward

[[Elasticsearch]] allows custom BM25 similarities to be configured and assigned to individual fields.

For example:

```json
{
  "settings": {
    "similarity": {
      "bm25_title": {
        "type": "BM25",
        "k1": 0.8,
        "b": 0.2
      },
      "bm25_description": {
        "type": "BM25",
        "k1": 1.2,
        "b": 0.75
      }
    }
  },
  "mappings": {
    "properties": {
      "title": {
        "type": "text",
        "similarity": "bm25_title"
      },
      "description": {
        "type": "text",
        "similarity": "bm25_description"
      }
    }
  }
}
```

And changing these parameters has essentially no meaningful query-performance penalty: Elasticsearch still performs the same inverted-index lookup and BM25 scoring. You're mostly changing constants inside the scoring calculation.

The cost is therefore predominantly **experimentation and evaluation**, not runtime performance.

## Where I would start

Rather than immediately search for an "optimal" value, I'd start with three deliberately different configurations.

### Baseline

```text
title        k1=1.2  b=0.75
category     k1=1.2  b=0.75
attributes   k1=1.2  b=0.75
description  k1=1.2  b=0.75
```

### Moderate

```text
title        k1=0.8  b=0.2
category     k1=0.5  b=0
attributes   k1=0.8  b=0.2
description  k1=1.2  b=0.75
```

### Aggressive

```text
title        k1=1.0  b=0
category     k1=0.5  b=0
attributes   k1=1.0  b=0
description  k1=1.0  b=0.5
```

Run them through the same judged queries.

If nothing interesting happens, stop.

That's actually a useful result.

If one direction consistently wins, then start a finer grid search or [[Bayesian Optimization]] around that area.

For a marketplace, I would also test adversarial versions of product content: duplicated query terms, unnaturally short titles, repeated brand names, and descriptions padded with common search phrases.

## So, is BM25 tuning worth it?

My conclusion after looking at the mechanics and comparing them with practitioners' experience is:

**It is worth experimenting with, but probably not worth obsessing over.**

For e-commerce specifically, there is a plausible reason to deviate from BM25 defaults.

Short structured fields behave differently from documents. Repeated terms in a title often provide little additional evidence. Field length in product titles, categories and attributes may not mean much at all. Descriptions, meanwhile, deserve different treatment.

For marketplaces, there is an additional reason: **ranking algorithms create incentives**.

If repeating keywords gives sellers an advantage, some sellers will repeat keywords. Reducing the term-frequency contribution on seller-controlled fields can therefore be useful even when the pure relevance improvement is small.

But the community experience seems fairly consistent: don't expect a spectacular business-metric improvement.

The defaults are already pretty good.

The interesting change is that **the cost of finding out has collapsed**.

If you already have judgments and an evaluation pipeline, don't spend three weeks arguing whether `b=0.2` theoretically makes more sense than `b=0.75`.

Have an agent generate the experiment.

Run 25 combinations overnight.

And ask the data.

---

## Related Concepts
- [[BM25]] · [[Bayesian Optimization]] · [[NDCG]] · [[MRR]]

## Related Videos
- [[Haystack US 2022 - Bayesian Optimization of Relevance at Shopify]]

## People
- [[Doug Turnbull]] · [[Andy Toulis]] · [[Max Irwin]]

## Companies
- [[Shopify]]

## Tools
- [[Elasticsearch]] · [[Quepid]]
