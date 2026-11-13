---
type: video
title: "Query Relaxation - a rewriting technique between search and recommendations"
speaker: "[[Rene Kriegler]]"
company: "[[OpenSource Connections]]"
medium: talk / video
url: https://www.youtube.com/watch?v=FQsX3H3I6fM
published: 2019-05-17
topics:
  - "[[E-commerce Search]]"
  - "[[Query Understanding in Practice]]"
concepts:
  - "[[Query Relaxation]]"
  - "[[Zero Results]]"
  - "[[Query Expansion]]"
  - "[[Word2Vec]]"
  - "[[Embeddings]]"
tools:
  - "[[Querqy]]"
people:
  - "[[Rene Kriegler]]"
  - "[[Charlie Hull]]"
  - "[[Daniel Tunkelang]]"
  - "[[Mihajlo Grbovic]]"
---

# Query Relaxation - a rewriting technique between search and recommendations

📺 **Watch:** https://www.youtube.com/watch?v=FQsX3H3I6fM

Talk by [[Rene Kriegler]] (introduced by [[Charlie Hull]], [[OpenSource Connections]]), 2019. Kriegler is a search & NLP relevance consultant focused on e-commerce, works mainly with Solr/Lucene, organizes the [[MICES]] e-commerce search conference in Berlin (alongside [[Berlin Buzzwords]]), and maintains [[Querqy]]. Companion note to the concept [[Query Relaxation]].

## Core Framing

[[Query Relaxation]] removes one term from a zero-result query and offers the shorter query — Google's strike-through pattern, which also lets the user re-add the removed term to stay in the conversation. The hard problem is **which term to remove?** Kriegler's central argument: it took him four months to realize query relaxation is *not* about **repairing** the query / reconstructing the exact information need — it is best understood as a **query recommendation**. The goal is to keep the user engaged on the site, not to perfectly satisfy the original intent. This places it closer to recommendations and exploratory search than to precision-oriented retrieval.

## Zero-Result Strategies (ordered by fidelity to intent)

A spectrum from "repair the query" to "recommend something related":

1. [[Query Expansion]] — synonyms / hypernyms broaden the query
2. [[Spelling Correction]] — "did you mean"
3. Searching low-quality fields (e.g. SEO-stuffed descriptions) — hurts precision, not explainable to users
4. Loosening Boolean constraints — AND→OR, `minimum-should-match` in Solr eDisMax
5. Hypernym expansion — boots → shoes
6. Related queries — beard balm → trimmer
7. General recommendations — shopping history, popular items

Strategies differ in **explainability**. Query relaxation is nicely explainable via the strike-through UX.

### Why the intuition is hard
- "iPhone 9" → remove the 9? (leaves silly matches for "9")
- "iPhone 9 Plus" → remove "Plus"? or the "9"?
- "black boots" vs "purple boots" → color salience differs; purple may matter more than boots
- "USB charger 12 volt" → every term is load-bearing

No hand-crafted rule works across all cases.

## Evaluation

- **Online:** click-through / **hit rate** (did a set of ~5 recommendations get ≥1 click), plus dwell time, exit rate, time-on-site — recommendation-style metrics, not precision@k.
- **Offline dataset:** pairs of (long query with **zero** results, shorter relaxed query **with** results). Two query sets:
  - **freq** — query frequencies: the relaxed query must be one seen before.
  - **co-oc** — original + relaxed query co-occurring in the same user **session** (sparser, harder to match).
  - A "top" split accepts only the most-frequent observed candidate when multiple exist.
  - Metrics: precision, recall, F1. In the 1-to-1 case precision = recall. **Precision here measures whether the predicted query is a "good"/observed query — not the precision of search results.**

## Algorithms Tested (roughly increasing performance)

1. **Baseline** — remove a random observed term. Mostly < 0.5.
2. **Remove shortest term** (Zipf: short tokens are ambiguous). Small gain.
3. **Remove shortest term containing a digit.** Good precision but low recall / coverage.
4. **Combine** — drop shortest digit-bearing term, else fall back to shortest term.
5. **Index term frequency** — dropping the **least-frequent** term works well: specific terms; users tend to drop the specific term and go more general.
6. **Entropy** over navigational categories — a complete failure (neither high nor low entropy helped).
7. **[[Word2Vec]] embeddings** (300-dim, trained with Gensim, CBOW) — represent original vs relaxed query, keep the most cosine-similar relaxation. Big push; usually the best after term frequency. Inspired by a blog post from [[Daniel Tunkelang]] on query relaxation with word embeddings.
8. **Query embeddings** — query-as-word, session = context (per **[[Mihajlo Grbovic]]** et al.). Only helped on the co-oc set (same-data effect); low recall from unseen queries.
9. **Multi-layer neural network** on word2vec input — up to 8 query terms × 300-dim vectors → 2 hidden layers (512, 256) with dropout + flattening → softmax over which term to drop. Categorical cross-entropy, Adam optimizer. 75k train / 25k test. Runs in **real time** via TensorFlow (Java bindings). Best so far.
10. **NN + word-shape features** — add word length, digit count, and "is there an *e* in the last two positions" (a plural-ending heuristic, originally German, that also helped in English) to each embedding. **Best result: ~0.9 precision/recall on the freq set**, high-ish on co-oc. Adding raw frequency info did not help.

## Conclusion

Query relaxation = **query recommendation**. Best approach: MLP on [[Word2Vec]] + word-shape features, extensible with further features (query embeddings, or even seller/profit interests to promote high-margin queries). Deciding *when* to relax was out of scope. As of the talk, the approach had **not** yet made it into production with two clients.

## Q&A Highlights

- **"e in last two positions"** feature = NLP word-shape trick for plural endings; based on experience.
- **Part-of-speech / product type:** product type best preserves intent, but it's hard to predict and users are willing to give it up; possibly encoded implicitly in the NN. Alternative (untried, no ontology available): use a **taxonomy/ontology** graph to find the redundant term.
- **Topic models:** could help, but skeptical for unseen query terms; would combine with another approach.
- **BERT** suggested by the audience as a successor to word2vec; Kriegler notes CBOW-vs-skip-gram is also tunable but expects more gain from added features than from swapping the embedding model.
- **Transferability beyond e-commerce:** likely for the word2vec approach; shortest-term / digit heuristics are e-commerce-specific (model numbers); the co-oc approach needs enough session data.

## Related

- Concept: [[Query Relaxation]], [[Zero Results]], [[Query Expansion]], [[Query Specificity]]
- Tool: [[Querqy]] — Kriegler's query rewriting library (its "delete terms" rule implements term-dropping relaxation)
- Grbovic et al. — query/action embeddings (see [[Mihajlo Grbovic]])
- Daniel Tunkelang's [[Query Understanding - Query Relaxation]] — the term-dropping / AND→OR framing
- [[Aron Negyesi]]'s [[Query relaxation - the forgotten hero of eCommerce search]] — recommends this talk for choosing which words to drop
