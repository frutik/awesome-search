---
title: "Fine-Tuning Text Embeddings For Domain-Specific Search"
source: "https://shawhin.medium.com/fine-tuning-text-embeddings-f913b882b11c"
author: ["Shaw Talebi"]
tags:
  - clippings
  - embeddings
  - fine-tuning
  - domain-specific
  - search
  - medium
concepts:
  - Embedding Fine-tuning
  - Bi-Encoder
  - Dense Vector Retrieval
  - Semantic Search
created: 2026-05-15
---

# Fine-Tuning Text Embeddings For Domain-Specific Search

**Source**: https://shawhin.medium.com/fine-tuning-text-embeddings-f913b882b11c  
**Author**: [[Shaw Talebi]]

## Summary

[[Shaw Talebi]] demonstrates through a hands-on tutorial that fine-tuning a general text embedding model on domain-specific data consistently outperforms the base model, and shows how to do it with `sentence-transformers`.

## Why General Models Fail on Domains

Talebi demonstrates with a concrete example: a medical Q&A task.

Base model (`all-MiniLM-L6-v2`) on medical questions:
- Retrieves semantically similar text, but "similar" in general English ≠ "medically relevant"
- "What causes hypertension?" returns articles about "blood pressure" generally
- Misses specialized connections: "ACE inhibitors" → "renin-angiotensin system"

Fine-tuned model:
- Understands domain-specific associations
- Better calibrated similarity scores within the domain

## Dataset Construction

Key to success: **hard negatives**.

```python
# Training triplet: (query, positive, hard_negative)
# Hard negative: relevant-looking but actually not the answer

dataset = [
    {
        "query": "What causes type 2 diabetes?",
        "positive": "Insulin resistance and insufficient insulin production...",
        "negative": "Type 1 diabetes is an autoimmune condition..."  # Hard: same disease, wrong type
    },
    ...
]
```

Strategies for getting negatives:
1. **BM25 negatives**: retrieve with BM25, take false positives
2. **Random negatives**: random corpus documents (easy, less effective)
3. **In-batch negatives**: other items in the training batch (standard, adequate)

## Training with sentence-transformers

```python
from sentence_transformers import SentenceTransformer, InputExample
from sentence_transformers.losses import TripletLoss
from torch.utils.data import DataLoader

model = SentenceTransformer("all-MiniLM-L6-v2")

train_examples = [
    InputExample(texts=[q, pos, neg], label=1.0)
    for q, pos, neg in dataset
]

train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=16)
train_loss = TripletLoss(model=model)

model.fit(
    train_objectives=[(train_dataloader, train_loss)],
    epochs=3,
    warmup_steps=100
)
```

## Results

Talebi reports typical improvements:
- NDCG@10: +12–18% on domain-specific benchmark
- MRR@10: +10–15%
- Consistent improvements even with ~2,000 training examples

The improvement plateaus around 10,000–20,000 examples; more data yields diminishing returns.

## Practical Guidance

| Training Set Size | Expected Improvement | Notes |
|-----------------|---------------------|-------|
| 500 examples | +5–8% | Marginal, worth trying |
| 2,000 examples | +10–15% | Good ROI |
| 10,000 examples | +15–20% | Strong improvement |
| 50,000+ examples | +18–22% | Diminishing returns |

## When NOT to Fine-tune

- When general retrieval quality is already sufficient
- When the domain vocabulary is well-covered by general training data
- When serving infrastructure can't support a larger/custom model
- When labeled data cost exceeds retrieval quality benefit

## Related Articles

- [[Fine-tuning Multimodal Embedding Models]] — same author, image-text
- [[Introduction to Matryoshka Embedding Models]] — can combine MRL with fine-tuning
- [[How to Choose the Best Model for Semantic Search]] — model selection context

## Related Concepts

- [[Embedding Fine-tuning]] — primary topic
- [[Bi-Encoder]] — architecture being fine-tuned
- [[Dense Vector Retrieval]] — downstream use
- [[Semantic Search]] — use case
- [[Retrieval Pipeline]] — distillation as alternative

## People

- [[Shaw Talebi]] — author
