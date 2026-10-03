---
type: article
title: "Diversity-Aware k-Maximum Inner Product Search Revisited"
aliases:
  - DkMIPS
  - Diversity-Aware kMIPS
  - "Balancing Relevance and Diversity in k-Maximum Inner Product Search"
  - DiversiNews
source: "https://arxiv.org/abs/2402.13858"
pdf: "https://arxiv.org/pdf/2402.13858"
repo: "https://github.com/HuangQiang/DiverseMIPS"
author:
  - "[[Qiang Huang]]"
  - "Yanhao Wang"
  - "[[Yiqun Sun]]"
  - "[[Anthony K.H. Tung]]"
published: 2024-02-21
created: 2026-10-03
venue: "arXiv preprint (cs.IR); extended as \"Balancing Relevance and Diversity in k-Maximum Inner Product Search\", The VLDB Journal 35(4), 2026"
datasets:
  - "[[NewsSpectrum]]"
concepts:
  - "[[Maximum Inner Product Search]]"
  - "[[MMR]]"
  - "[[Diversity Metrics]]"
  - "[[Vector Similarity Metrics]]"
  - "[[Brute-Force Vector Search]]"
  - "[[Approximate Nearest Neighbor Search]]"
  - "[[Dense Embeddings]]"
topics:
  - "[[Search Result Diversity]]"
tags:
  - article
  - diversity
  - vector-search
  - recommendation
  - news
  - information-retrieval
---

# Diversity-Aware k-Maximum Inner Product Search Revisited

**Authors:** [[Qiang Huang]], Yanhao Wang, [[Yiqun Sun]], [[Anthony K.H. Tung]] (National University of Singapore; East China Normal University) · arXiv:2402.13858, February 2024 · code at [HuangQiang/DiverseMIPS](https://github.com/HuangQiang/DiverseMIPS) (C++, MIT), Python bindings at [dukesun99/PyDkMIPS](https://github.com/dukesun99/PyDkMIPS)

Extended journal version: *Balancing Relevance and Diversity in k-Maximum Inner Product Search*, The VLDB Journal 35(4), 2026, with Jun Yu added as an author — [doi:10.1007/s00778-026-00982-8](https://doi.org/10.1007/s00778-026-00982-8). The news demo built on it, **DiversiNews**, is covered [below](#diversinews-the-news-application).

## Summary

[[Maximum Inner Product Search|k-Maximum Inner Product Search]] (kMIPS) returns the *k* item vectors with the largest inner product against a query vector. It is the retrieval step of matrix-factorization recommenders, and it optimizes relevance only. The paper's opening example is a MovieLens user with interests across ten genres whose exact kMIPS top-10 collapses onto five of them: Action, Adventure, Drama, War, Western.

**DkMIPS** puts [[MMR]]'s relevance/diversity trade-off *inside* the inner-product search problem, rather than running it as a separate rerank over a retrieved list. The paper revisits an earlier formulation (Hirata et al., with the IP-Greedy heuristic) and argues that formulation was flawed in three ways:

- **Two vector spaces.** It measured relevance with matrix-factorization vectors but dissimilarity with separate Item2Vec vectors, even though both derive from the same rating matrix — extra preprocessing for no clear gain.
- **A marginal-gain function that does not match its own objective.** IP-Greedy's per-step gain recomputes the minimum pairwise distance over the whole set at every step, so the minimum distance is counted repeatedly, for possibly different pairs.
- **No approximation guarantee**, and a worst-case cost of O(ndk² log n).

## The Revised Problem

DkMIPS uses one inner-product space for both terms. A balancing factor λ ∈ [0, 1] and a scaling factor µ > 0 set the trade-off, and diversity is measured as either the **average** or the **maximum** pairwise inner product within the result set:

```
f_avg(S) = (λ/k) Σ_{p∈S} ⟨p,q⟩  −  (2µ(1−λ) / k(k−1)) Σ_{p≠p'∈S} ⟨p,p'⟩
f_max(S) = (λ/k) Σ_{p∈S} ⟨p,q⟩  −  µ(1−λ) · max_{p≠p'∈S} ⟨p,p'⟩
```

At λ = 1 this is plain kMIPS. At λ = 0 it becomes the max-mean or max-min **dispersion** problem. Because it is grounded in MMR, the problem is NP-hard, so the paper builds approximation algorithms rather than exact ones.

The two diversity measures behave differently mathematically, and that difference drives the algorithm design:

- `f_avg` is **submodular** (diminishing returns) but non-monotone — adding a near-duplicate can lower the score.
- `f_max` is neither submodular nor supermodular, so submodular-optimization guarantees do not apply to it.

## Algorithms

- **Greedy** — the MMR recipe: seed with the top inner-product item, then add the item with the largest marginal gain for *k* rounds. It has a data-dependent approximation bound under either objective, valid mainly when λ is close to 1.
- **DualGreedy** — grows **two** result sets in parallel, each step adding to whichever set gains more, and returns the better one. This is the standard trick for non-monotone submodular maximization. For `f_avg` it gives a **1/4 approximation plus an additive regularization term**. For `f_max` the guarantee is only data-dependent.

Both cost O(ndk²) as stated, which optimizations in the paper reduce to O(ndk). Both are still linear scans.

### Pruning with a Ball-Cone Tree

To avoid scanning every item each round, both algorithms sit on a **BC-Tree**, a Ball-Tree variant from earlier work by Huang and Tung. It keeps ball bounds (centre and radius) at every node, plus per-point ball and cone values (norm, and angle to the leaf centre) in the leaves. These give upper bounds on the marginal gain, so whole subtrees and individual points can be skipped. The pruned variants are **BC-Greedy** and **BC-DualGreedy**.

Construction takes O(nd log n) time and O(nd) space. On the largest dataset, LFM, at roughly 32 million items, the authors report building it within an hour at about 1.3 GB.

The paper explains why it did not use the usual [[Approximate Nearest Neighbor Search|ANN]] structures — [[LSH]], [[Vector Quantization|quantization]], [[HNSW|proximity graphs]]. The marginal gain has two terms, relevance and diversity, and that makes it hard to meet those structures' basic requirements. Diversity-aware retrieval does not drop straight into an off-the-shelf vector index.

## Evaluation (authors' own)

The setup uses ten recommendation datasets, including MovieLens, Netflix, Yelp, Google Local (California), Yahoo! Music, Taobao, two Amazon Review categories and LFM. Vectors come from 100-dimensional non-negative matrix factorization; there are 100 random user queries, k from 5 to 25 and λ from 0.1 to 0.9. Everything runs single-threaded in C++ and in memory.

Quality is judged by how well the recommended items' genre or category mix matches the user's history:

- **Coverage** — the share of the user's categories that appear in the results.
- **PCC** — the Pearson correlation between the category histograms of the results and of the user's rated items.

All of the following are the authors' own results.

- **Quality.** The new methods generally score best on both measures across λ. Exact kMIPS generally comes second and IP-Greedy generally scores worst, which the authors attribute to its objective/gain mismatch. On MovieLens at λ = 0.5, coverage is 0.682 for exact kMIPS, 0.684 for IP-Greedy and 0.765 for BC-DualGreedy-Avg.
- **DualGreedy vs Greedy.** DualGreedy beats Greedy in most cases, especially with `f_avg`, consistent with its stronger guarantee there.
- **Speed.** The linear scan and the new methods run one to two orders of magnitude faster than IP-Greedy. BC-Greedy is at least twice as fast as BC-DualGreedy, and `f_max` is faster than `f_avg` because its bounds are tighter. On MovieLens at λ = 0.1 the reported per-query times are 3.34 ms for the linear scan, 59.9 ms for IP-Greedy and 1.00 ms for BC-Greedy-Max.
- **Pruning.** It works better as λ rises: the bounds are tighter when relevance dominates. Query time grows linearly with k and near-linearly with n.
- **Item2Vec.** Adding Item2Vec vectors for the diversity term matched or underperformed the single-space version, which supports the decision to drop the second space.
- **µ.** No single value of µ is best across datasets, because vector norms differ. The authors suggest tuning it by binary search. It is a real knob that needs per-corpus calibration.

The repository for the journal version moves the evaluation beyond collaborative filtering. It covers five datasets: MovieLens-25M and Yahoo! Music for recommendation; Yahoo! News and [[NewsSpectrum]], encoded with the AnglE `UAE-Large-V1` text embedder, for retrieval; and T2I-10M, 10 million text-to-image vectors.

## DiversiNews: the news application

*DiversiNews: Enriching News Consumption with Relevant Yet Diverse News Articles Retrieval* — [[Yiqun Sun]], [[Qiang Huang]], Yanhao Wang, [[Anthony K.H. Tung]] — PVLDB 17(12): 4277–4280, 2024 (demo paper), [doi:10.14778/3685800.3685854](https://doi.org/10.14778/3685800.3685854) · code and data at [dukesun99/DiversiNews](https://github.com/dukesun99/DiversiNews) (MIT; article texts remain the publishers').

DiversiNews applies DkMIPS to the echo-chamber problem in news feeds. The query is the embedding of the article a reader is currently viewing. BC-Greedy or BC-DualGreedy then returns related articles that are relevant but spread across perspectives, with λ exposed to the user as a slider.

- **Embeddings, no fine-tuning.** Three encoders are used off the shelf: Sentence-BERT (`all-MiniLM-L12-v2`, see [[Sentence Transformers]]), AnglE (`UAE-Large-V1`), and LLaMA 2 7B, taking the last token's final hidden state. The authors' bet is that general-purpose embeddings already encode latent political perspective through writing style and word choice. No bias labels are used in training or retrieval, so the system is not tied to US left/right politics. The labels are used only for evaluation.
- **Corpus.** The corpus is [[NewsSpectrum]]: 250,000 articles linked from Reddit, balanced across the five AllSides media-bias levels.
- **Evaluation.**
  - *Relevancy* is the mean inner product with the query.
  - *Diversity* is the mean pairwise difference in outlet bias rating, on a −2 to +2 scale.
  - Baselines are exact kMIPS (the relevance ceiling) and random selection (the diversity ceiling).
  - At k = 10 the authors report that DkMIPS raises diversity while keeping relevancy similar, particularly at larger λ, with the expected trade-off as λ moves.
- **Demo.** A split-view page puts the source article beside the retrieved set. Retrieval method and encoder are switchable, and a media-bias summary chart sits alongside. Two scenarios are shown: corroborating a story through coverage from the opposite side of the spectrum, and widening the perspectives a reader sees on a polarizing story.

The bias labels describe **outlets**, matched by domain. They are not article-level ideology judgements, so "diversity" here means a spread of sources, which is only a proxy for a spread of viewpoints. The quantitative evaluation is small and descriptive; the paper is a system demonstration, not a user study.

## Why It Matters

- **Diversity as part of retrieval.** Most diversification in search is a post-hoc rerank over a top-N list ([[MMR]], [[Search Result Diversity|category caps, entropy]]), which can only diversify what the first stage already returned. DkMIPS makes diversity part of the inner-product query itself, with stated approximation guarantees. The cost is giving up ordinary ANN indexes.
- **A small, honest result.** Average pairwise similarity is submodular and so tractable with guarantees; maximum pairwise similarity is not. That is worth knowing before choosing a diversity objective for any greedy reranker.
- **A baseline for later work.** DkMIPS was a baseline in the same group's later [[Uncovering the Bigger Picture - Comprehensive Event Understanding via Diverse News Retrieval|NEWSCOPE]] paper. There it scored highest on embedding-distance diversity ([[APD]]) but behind NEWSCOPE on sentence-cluster coverage. Spreading results out in vector space and covering distinct aspects are different objectives.

## Limitations

- The core experiments are collaborative-filtering recommendation with NMF vectors, and genre or category coverage stands in for diversity. The approximation bounds assume non-negative inner products, which NMF guarantees and general text embeddings do not.
- µ has to be tuned per corpus.
- All efficiency and quality comparisons are the authors' own, against a linear scan and a single prior method (IP-Greedy).

## Related Concepts

- [[Maximum Inner Product Search]] — the base problem DkMIPS extends
- [[MMR]] — the relevance-minus-redundancy objective DkMIPS adapts
- [[Diversity Metrics]] — average vs. maximum pairwise similarity as set-level diversity measures
- [[APD]] — the average-pairwise measure on which DkMIPS led in NEWSCOPE's comparison
- [[Vector Similarity Metrics]] — inner product as the single similarity used for both terms
- [[Brute-Force Vector Search]] — the linear-scan baseline
- [[Approximate Nearest Neighbor Search]] — the index families the paper argues do not transfer directly
- [[Dense Embeddings]] — the text-embedding setting of DiversiNews

## Related Topics

- [[Search Result Diversity]]

## Related Datasets

- [[NewsSpectrum]] — released with DiversiNews

## Related Articles

- [[Uncovering the Bigger Picture - Comprehensive Event Understanding via Diverse News Retrieval]] — later work from the same group, with DkMIPS as a baseline

## People

- [[Qiang Huang]] — first author of DkMIPS; co-author of DiversiNews
- [[Yiqun Sun]] — co-author of DkMIPS; first author of DiversiNews
- [[Anthony K.H. Tung]] — co-author of both
