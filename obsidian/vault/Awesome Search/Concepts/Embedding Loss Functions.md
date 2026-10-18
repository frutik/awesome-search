---
type: concept
title: Embedding Loss Functions
aliases:
  - embedding loss
  - embedding loss function
  - MultipleNegativesRankingLoss
  - MNRL
  - CoSENTLoss
  - CoSENT
  - CachedMultipleNegativesRankingLoss
  - CachedMNRL
  - MatryoshkaLoss
tags:
  - concept
  - embeddings
  - fine-tuning
  - loss-function
related_concepts:
  - "[[Contrastive Learning]]"
  - "[[Dataset Types for Embedding Fine-Tuning]]"
  - "[[Matryoshka Embeddings]]"
  - "[[Hard Negative Mining]]"
created: 2026-10-18
---

# Embedding Loss Functions

The loss function is the number training minimises; for an embedding model it measures how well the vector space matches the similarity the training data asserts. In practice the choice is driven by the shape of the data ([[Dataset Types for Embedding Fine-Tuning]]), and the common options are all implemented in [[Sentence Transformers]]. Most of them are forms of [[Contrastive Learning]], which covers the objectives in general; this note covers the concrete Sentence Transformers losses and when to use each.

---

## The main options

### MultipleNegativesRankingLoss (MNRL) — the default
Needs only (anchor, positive) pairs: every other example's positive in the batch serves as a negative, so a batch of 32 gives each anchor 31 negatives. [[Ritik Jain]] recommends it for about 90% of use cases — semantic search, document retrieval, FAQ matching. Its weaknesses follow from the same mechanism: it wants batches of at least 32, an in-batch "negative" can turn out to be relevant (a false negative), and random negatives are often too easy. Supplying explicit hard negatives addresses the last one ([[Hard Negative Mining]]).

### CoSENTLoss — graded scores
CoSENT ("Consistent SENTence embedding") trains on continuous similarity scores, such as STS ratings from 0 to 5, using cosine similarity in both training and inference. Graded labels carry more information than binary ones, and the author reports faster convergence and better final quality than MNRL — but it needs human-scored pairs and suits similarity and paraphrase tasks rather than retrieval.

### TripletLoss — explicit negatives
For (anchor, positive, negative): `loss = max(‖anchor − positive‖ − ‖anchor − negative‖ + margin, 0)`. The model is penalised until the negative is at least the margin further away than the positive. Simple and fully controllable, but it gives a weaker signal than MNRL and the margin must be tuned.

### CachedMultipleNegativesRankingLoss — very large batches
MNRL with gradient caching: embedding and loss are computed in two stages, each in mini-batches, so memory sized for a batch of 32 can serve far larger batches — the guide's example is 65,536. More in-batch negatives per step, at about 20% more time per step. Suited to training sets of 100k+ examples.

### MatryoshkaLoss — a modifier, not a base loss
Wraps any of the above and applies it at several truncated dimensions at once, so the trained vectors still work when cut short. The author's figure is 768 → 128 dimensions with about 99% of quality retained — six times less storage and faster comparison. It combines with the cached losses. See [[Matryoshka Embeddings]], including the debate over truncation vs. post-hoc PCA.

## Choosing

| Data you have | Loss |
|---|---|
| Positive pairs only | MNRL |
| Pairs + mined hard negatives | MNRL with negatives |
| Explicit triplets | TripletLoss or MNRL |
| Graded similarity scores | CoSENTLoss |
| 100k+ examples, more negatives wanted | CachedMNRL |
| Need smaller vectors at serving time | MatryoshkaLoss around any of the above |

## A falling loss is not a better model

Loss measures separation on the training examples, and it routinely moves without moving [[NDCG]] on real queries. Evaluate retrieval metrics at checkpoints ([[Model Selection and Fine-Tuning Evaluation]]). Ranking losses for learning-to-rank models, such as [[LambdaLoss]], are a separate family that optimises list order rather than vector geometry.

## Related Concepts
- [[Contrastive Learning]] — the objective family most of these belong to
- [[Dataset Types for Embedding Fine-Tuning]] — the data each loss consumes
- [[Hard Negative Mining]] — what makes MNRL and TripletLoss work
- [[Matryoshka Embeddings]] · [[Embedding Fine-tuning]]
- [[Hyperparameter Tuning for Embedding Fine-Tuning]] — batch size matters directly for in-batch losses
- [[LambdaLoss]]

## Tools
- [[Sentence Transformers]]

## Related Articles
- [[The Complete Guide to Fine-Tuning Embedding Models]]

## People
- [[Ritik Jain]]
