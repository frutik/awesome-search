---
title: "Understanding the Search Query — Part II"
source: "https://medium.com/analytics-vidhya/understanding-the-search-query-part-ii-44d18892283f"
author:
  - "[[Sonu Sharma]]"
published: 2019-02-11
created: 2026-05-15
description: "Details the Crocodile Model—a BiLSTM-CRF architecture for search query tagging—and its deployment using TensorFlow Serving."
tags:
  - clippings
---

# Understanding the Search Query — Part II

## The Crocodile Model Architecture

A sequence tagging ML model with three core components:

**1. Word Representation**
- GloVe embeddings (Stanford, 300-dimensional, pre-trained, frozen)
- Character-level embeddings via BiLSTM or CNN for OOV terms (brand names, etc.)

**2. Contextual Word Representation**
- Bidirectional LSTM processes sequences to capture context
- Dense layer produces outputs matching number of semantic tags

**3. Decoding**
- Conditional Random Fields (CRF) identify optimal tag sequences using probabilistic transitions

## Model Variants

| Model | Description |
|---|---|
| LSTM-CRF | Base model |
| CharLSTM-LSTM-CRF | Adds character-level LSTM embeddings |
| CharConv-LSTM-CRF | CNN instead of LSTM for character embeddings |
| CharLSTM-LSTM-CRF + ELMo | Adds ELMo contextual embeddings |

Production selection: **CharLSTM-LSTM-CRF** (best performance).

## TensorFlow Implementation

### Data Pipeline (tf.data API)
```python
dataset = tf.data.Dataset.from_generator(
    functools.partial(generator_fn, words, tags), 
    output_shapes=shapes, output_types=types
)
dataset = dataset.shuffle(100).repeat(5)
dataset = dataset.padded_batch(2500, shapes, defaults).prefetch(2500)
```

### Architecture Details

- **Character embeddings**: 100-dim → BiLSTM (25 units each direction) → 50-dim output
- **Word embeddings**: GloVe 300-dim (frozen) + character 50-dim = 350-dim input
- **Contextual BiLSTM**: 100 units each direction → 200-dim output → dense → num_tags logits
- **CRF**: Learns tag transition scores for globally optimal predictions

### Loss & Optimization
```python
log_likelihood, _ = tf.contrib.crf.crf_log_likelihood(
    logits, correct_tags, [length_of_tags], crf_params
)
loss = tf.reduce_mean(-log_likelihood)
train_op = tf.train.AdamOptimizer().minimize(loss, global_step=...)
```

## TensorFlow Serving Deployment

Export as SavedModel, serve via Docker REST API on port 8501.

Example output for query "nut free chocolate":
```json
{"outputs": [["NV-S", "PR-S", "BQ-S"]]}
```
- **NV-S**: Nutrition attribute
- **PR-S**: Preposition  
- **BQ-S**: Base query term


## Related Concepts

- [[Query Understanding]]
- [[Query Segmentation]]
- [[Embeddings]]

## People

- [[Sonu Sharma]]
