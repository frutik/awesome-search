---
title: "Modality Gap"
aliases: ["modality gap", "cross-modal gap", "embedding space gap", "CLIP modality gap", "modal gap"]
tags:
  - concept
  - search
  - embeddings
  - multimodal
created: 2026-05-16
---

# Modality Gap

## Definition

The modality gap is the observation that in jointly trained multimodal embedding spaces (e.g., CLIP), image embeddings and text embeddings occupy **distinct, non-overlapping regions** of the embedding space — even after joint training intended to align them.

Images cluster in one cone of the hypersphere, text in another. The gap between these cones is the modality gap.

## Why It Occurs

Two contributing factors:

1. **Initialization**: Different encoder architectures (vision transformer vs. text transformer) start from different random initializations, pushing representations into different regions.
2. **[[Contrastive Gap]]**: Contrastive training (InfoNCE loss) pushes *matched* pairs together and *mismatched* pairs apart, but doesn't force both modalities to occupy the same geometric region — just to be closer to their match than to random negatives.

## Impact on Multimodal Search

In [[Multimodal Embeddings]] systems (image-text retrieval, cross-modal search):
- Cosine similarity between a text query and an image is systematically lower than same-modality similarity
- Nearest neighbor searches can be biased toward same-modality results
- Uniform thresholds for "relevant" don't work across modalities

## Mitigations

- **Temperature scaling**: rescale similarity scores per modality before combining
- **Modality-specific normalization**: normalize scores within modality before cross-modal comparison
- **Fine-tuning with cross-modal negatives**: explicitly train to close the gap
- **Modality tokens**: some models add explicit modality indicators to pull representations closer

## Related Concepts

- [[Multimodal Embeddings]] — the broader context where modality gap appears
- [[Contrastive Gap]] — related phenomenon from contrastive training dynamics
- [[Dense Embeddings]] — the vector space where the gap manifests
- [[Vector Similarity Metrics]] — gap affects cosine similarity comparisons
- [[Embedding Fine-tuning]] — one way to mitigate the gap
