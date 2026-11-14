---
type: video
title: "Using alternative queries to mitigate zero results"
speaker: ["[[Rene Kriegler]]", "[[Jean Silva]]"]
company: "[[Wallapop]]"
medium: talk / video
url: https://www.youtube.com/watch?v=inVktiefRl0
published: 2023-10-12
conference: "[[Haystack EU]]"
topics:
  - "[[E-commerce Search]]"
  - "[[Query Understanding in Practice]]"
concepts:
  - "[[Query Relaxation]]"
  - "[[Zero Results]]"
  - "[[Query Rewriting]]"
  - "[[Spelling Correction]]"
  - "[[Embeddings]]"
tools:
  - "[[Solr]]"
people:
  - "[[Rene Kriegler]]"
  - "[[Jean Silva]]"
created: 2026-11-14
---

# Using alternative queries to mitigate zero results

📺 **Watch:** https://www.youtube.com/watch?v=inVktiefRl0

> [!info] Follow-up talk
> This talk continues [[Rene Kriegler - Query Relaxation]], Kriegler's 2019 talk. The same term-drop algorithms, evaluation setup and query pairs (`iPhone`, `Audi A4`, `purple shoes`, `USB charger 12V`) come back here. Read that note for the original algorithm comparison; this one covers what changed in 2023.

[[Haystack EU]] 2023 talk (published by [[OpenSource Connections]]) by [[Rene Kriegler]] and [[Jean Silva]], a search engineer at [[Wallapop]]. It revisits Kriegler's 2019 talk [[Rene Kriegler - Query Relaxation]] with 2023 tools — fine-tuned language models — and then shows the deliberately simple version Wallapop put into production to cut [[Zero Results]] on its marketplace.

---

## Key Moments

| Time | Section |
|---|---|
| [00:00](https://www.youtube.com/watch?v=inVktiefRl0&t=0s) | Introduction to the problem |
| [04:47](https://www.youtube.com/watch?v=inVktiefRl0&t=287s) | Strategies for zero results |
| [09:15](https://www.youtube.com/watch?v=inVktiefRl0&t=555s) | Query relaxation techniques |
| [14:40](https://www.youtube.com/watch?v=inVktiefRl0&t=880s) | Evaluation and modeling |
| [24:56](https://www.youtube.com/watch?v=inVktiefRl0&t=1496s) | Token replacement methods |
| [30:35](https://www.youtube.com/watch?v=inVktiefRl0&t=1835s) | Practical implementation (Wallapop) |
| [38:02](https://www.youtube.com/watch?v=inVktiefRl0&t=2282s) | Conclusion and outlook |
| [40:01](https://www.youtube.com/watch?v=inVktiefRl0&t=2401s) | Q&A |

## The Wallapop setting

[[Wallapop]] is a classified-ads marketplace in Spain, Italy and Portugal with more than 70 million users. Listings are user-generated, so misspellings are common, and a locality filter adds another constraint. The team prioritises precision. It had already shipped the usual zero-result fixes: a Spanish stemmer contributed to Lucene, synonyms and hyponyms, [[Spelling Correction]], a wider geographic radius for some queries, and looser Boolean constraints. Vector search ([[Semantic Search]]) was judged a medium-term investment, partly because embedding a large, fast-churning inventory of listings is costly. That left alternative queries as the next lever.

## Two ways to build an alternative query

- **[[Query Relaxation]]**: drop one term (`iPhone 14 mini` → `iPhone mini`). The UI can show which term was dropped, so the result is explainable and the user can edit the query.
- **Token replacement**: swap one token for a sibling (`Audi A1` → `Audi A2`). This can stay more specific than relaxation, but it still won't match the exact intent.

The hard part of relaxation is still *which term to drop*. `Audi A4` might keep either token, depending on whether the site is all cars (A4 is also a paper size). `purple shoes` might be better relaxed to `purple`. In `USB charger 12V`, every term carries meaning.

## Relaxation experiments (Spanish data)

Evaluation uses pairs of a long query (zero or few results) and a shorter sub-query that has results, each labelled with the index of the dropped term. Accuracy is measured against the labels.

- **Drop the shortest non-alphabetical term**: accuracy 0.52 but recall 0.05, because few queries contain such a term.
- **Drop the least frequent term** (index term statistics): 0.79. Kriegler says this is the usual choice for teams without ML.
- **Sentence embeddings from a MiniLM model**: compare the original query with each candidate and keep the most similar one. Recall improves because unseen queries can be embedded, which the older query-as-word embeddings couldn't do. Accuracy was not high.
- **The 2019 winner, an MLP over word embeddings plus word-shape features**: 0.98. Kriegler explains the jump from 2019: back then he had sorted query terms alphabetically to pool analytics, which threw away token order. Fixing that, and the switch to Spanish, lifted the score.
- **A fine-tuned RoBERTa classifier** that predicts the drop position straight from the raw query reaches the same level after four epochs, with no pre-trained word embeddings. At that ceiling the model has learned the dataset, so further gains need better data, such as session-based pairs.

## Token replacement with a fill-mask model

A fill-mask model, fine-tuned on 400,000 queries (two to three hours on CPU), generates the replacement. The pipeline: predict the position with the best relaxation model, mask it, generate candidates, then filter by string similarity so that model numbers map to model numbers (for `Audi A1`, prefer `A2` over unrelated tokens). The results were mixed. Model-number swaps looked good, but some swaps changed the meaning, for example cheap cars → camping cars. Kriegler treats it as inspiration: one possible use is relaxing a query and boosting results that match a generated alternative. It was not measured systematically.

## What Wallapop shipped

They started with the simplest option, **drop the least-frequent term**, so they could get online feedback quickly and avoid running a complex ML model in production. The known weakness: the rarest term can be the most important one.

Building the offline dataset:
1. From about 30 days of logs, take queries with at least two tokens that returned results, and queries that returned zero results.
2. Normalise them with a minimal analysis chain (lowercasing, token and character cleanup).
3. For each long query, generate every leave-one-out candidate (`iPhone 14 plus` → `iPhone 14`, `iPhone plus`, `14 plus`). Count how often each candidate appears in the logs and keep the plausible ones. Save as TSV.
4. Get each token's document frequency from [[Solr]] (via the terms component), store it as JSON, and predict the drop as the lowest-frequency token. Variants to try include removing stop words or duplicated tokens first.

Offline accuracy was **about 80%**. An A/B test was about to start, with guardrails on the metrics the business doesn't want to hurt. Purchases were the likely main measure.

## Q&A highlights

- **Search passes**: run a precise pass first (Wallapop uses minimum-should-match at 100%), then [[Spelling Correction]], then looser Boolean matching. Kriegler would like relaxation to replace minimum-should-match eventually, because that is hard to explain to users. In practice he has seen teams cut zero-result queries by roughly **20–25%**.
- **Metric**: beyond business metrics, track **exit rate** after a zero-result query. The goal is to keep the user engaged, since a rewritten query (spelling correction aside) can't fully match the intent.
- **When to relax**: should relaxation also run when there are only a few poor results, not just zero? Kriegler calls the ideal result count an open question that needs testing, and suggests starting with true zero-result cases or a clearly labelled "you might also be interested in" block.
- **Position matters**: trailing modifiers such as a location can be essential, and which positions can be dropped depends on the language.
- **Numeric relaxation** (model year, price budget) should be learned from how users change their own queries within a session.
- **Datasets**: no public dataset is needed. Any query log yields (long query, sub-query) pairs.
- **Showing several alternatives with result counts** was suggested as a way to collect training data. Kriegler cautions that presentation creates bias.

## Related

- Earlier talk: [[Rene Kriegler - Query Relaxation]] (2019), with the original algorithm comparison
- Concepts: [[Query Relaxation]] · [[Zero Results]] · [[Query Rewriting]] · [[Spelling Correction]] · [[Embeddings]]
- [[Query relaxation - the forgotten hero of eCommerce search]] · [[Query Understanding - Query Relaxation]]
- Topics: [[E-commerce Search]] · [[Query Understanding in Practice]]
- Venue: [[Haystack EU]]
