---
title: "SPLADE for Sparse Vector Search Explained"
source: "https://www.pinecone.io/learn/splade/"
author: ["James Briggs"]
tags:
  - clippings
  - splade
  - sparse-search
  - pinecone
  - neural-retrieval
concepts:
  - SPLADE
  - Sparse Vector Retrieval
  - Hybrid Search
created: 2026-05-15
---

# SPLADE for Sparse Vector Search Explained

**Source**: https://www.pinecone.io/learn/splade/  
**Author**: [[James Briggs]] (Pinecone)

## Summary

[[James Briggs]] explains [[SPLADE]] from first principles — the architecture, the Log-ReLU transformation, term expansion, and practical implementation in Pinecone's sparse vector index.

## SPLADE Architecture Deep Dive

### Step 1: BERT Tokenization
Input text → BERT tokenizer → input_ids, attention_mask

### Step 2: BERT MLM Forward Pass
```python
from transformers import AutoTokenizer, AutoModelForMaskedLM

model = AutoModelForMaskedLM.from_pretrained("naver/splade-cocondenser-selfdistil")
output = model(**encoded_input)
logits = output.logits  # shape: [batch, seq_len, vocab_size=30522]
```

### Step 3: Log-ReLU Activation
Transform logits to non-negative sparse weights:
```python
# Log(1 + ReLU(x)) — keeps sparsity, creates meaningful weights
activated = torch.log(1 + torch.relu(logits))
```

Why Log-ReLU?
- **ReLU**: zeros out negative logits → sparsity
- **Log**: compresses large values → better calibrated weights

### Step 4: MaxPool over Sequence
```python
# Aggregate across all token positions: take max for each vocab term
sparse_vector = torch.max(activated, dim=1).values  # [batch, vocab_size]
```

MaxPool ensures each vocabulary term gets its highest weight across all positions — effectively capturing the most salient occurrence of each concept.

### Step 5: Sparse Representation
```python
# Convert to sparse dict
non_zero_ids = (sparse_vector > 0).nonzero()
sparse_dict = {
    tokenizer.decode([idx]): weight.item()
    for idx, weight in zip(non_zero_ids, sparse_vector[non_zero_ids])
}
```

Example output for "machine learning algorithms":
```
{
    "machine": 2.1, "learning": 2.4, "algorithm": 1.8,
    "model": 1.2, "training": 0.9, "neural": 0.7,  ← expanded terms
    "##gorithm": 0.3, "computational": 0.4, ...
}
```

Note: "neural" and "model" are **expanded terms** — not in the input but relevant.

## FLOPS Regularizer

SPLADE training includes a regularizer to control sparsity:
```
Loss = task_loss + λ × Σ(non_zero_terms) 
```

Higher λ → sparser vectors → faster retrieval, potentially lower quality.

## SPLADE Variants

| Model | Released | Notes |
|-------|---------|-------|
| SPLADE | 2021 | Original |
| SPLADE-v2 | 2022 | Improved efficiency |
| SPLADE-cocondenser | 2022 | Better recall |
| SPLADE++ | 2023 | Distillation from cross-encoder |

## Pinecone Implementation

```python
import pinecone

# Create sparse-dense index
index = pinecone.Index("hybrid-search")

# Upsert with SPLADE sparse + dense
index.upsert([{
    "id": "doc1",
    "values": dense_embedding,      # bi-encoder embedding
    "sparse_values": {              # SPLADE sparse vector
        "indices": [token_id for token_id, _ in sparse_terms],
        "values": [weight for _, weight in sparse_terms]
    },
    "metadata": {"text": document_text}
}])
```

## Related Articles

- [[Hybrid Search SPLADE Sparse Encoder]] — SPLADE in hybrid context
- [[SPLADE - Sparse Bi-Encoder BERT Model for First-Stage Ranking]] — original paper explained
- [[Elastic Learned Sparse Encoder ELSER Retrieval Performance]] — production SPLADE
- [[The Missing WHERE Clause in Vector Search]] — same author, filtering

## Related Concepts

- [[SPLADE]] — primary topic
- [[Sparse Vector Retrieval]] — category
- [[Hybrid Search]] — primary use case
- [[Dense Vector Retrieval]] — dense counterpart

## People

- [[James Briggs]] — author (Pinecone)
- [[Stéphane Clinchant]] — SPLADE creator
- [[Thibault Formal]] — SPLADE creator
