---
type: concept
aliases: ["Average Pairwise Distance", "average pairwise distance"]
tags: [concept, diversity, metrics]
related: ["[[MMR]]", "[[Diversity Metrics]]", "[[Search Quality Assurance]]"]
created: 2026-05-16
---

# APD — Average Pairwise Distance

A passive diversity measurement that quantifies how dissimilar the results in a ranked list are from each other.

## Formula

$$\text{APD} = \frac{1}{\binom{n}{2}} \sum_{i < j} \text{dist}(d_i, d_j)$$

Where:
- $n$ = number of results
- $\text{dist}(d_i, d_j)$ = distance between documents $i$ and $j$
- $\binom{n}{2}$ = number of unique pairs

## Distance Functions

The choice of distance function determines what kind of diversity is measured:

| Distance type | What it captures |
|---|---|
| Edit distance (text) | Lexical diversity — different words, not just different meaning |
| Embedding cosine distance | Semantic diversity — results cover different topics/aspects |
| Category/facet distance | Structural diversity — results span different product types or domains |

## Interpretation

- APD = 0: all results are identical
- APD = 1 (max for normalized distances): all results are maximally dissimilar

APD measures the diversity **that exists** in a result set. [[MMR]] actively **creates** diversity by penalizing similar results during reranking. APD is used to evaluate; MMR is used to optimize.

## Use in Evaluation

APD is useful as a dashboard metric:
- Track APD alongside NDCG — a system can score well on relevance while surfacing near-duplicate results
- Segment by query type: exploratory queries should have higher APD than navigational queries
- Compare systems: does the new ranker increase or decrease diversity?

## Limitations

- Sensitive to the distance function choice — semantic distance and lexical distance tell different stories
- Doesn't account for position — a diverse but relevant result at position 10 vs a redundant one at position 2 are treated equally
- Does not penalize redundancy in proportion to user harm — [[MMR]] is better when you want to actively improve diversity

## Related

- [[MMR]] — active diversity optimization (APD's complementary tool)
- [[Diversity Metrics]] — broader overview of diversity approaches
- [[NDCG]] — relevance metric APD is typically used alongside
