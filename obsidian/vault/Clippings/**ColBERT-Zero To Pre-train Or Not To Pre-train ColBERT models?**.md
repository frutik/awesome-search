---
title: "**ColBERT-Zero: To Pre-train Or Not To Pre-train ColBERT models?**"
source: "https://huggingface.co/blog/lightonai/colbert-zero"
author:
  - "[[Antoine Chaffin]]"
  - "[[Luca Arnaboldi]]"
  - "[[Amélie Chatelain]]"
  - "[[Florent Krzakala]]"
published: 2026-02-19
created: 2026-05-16
description: "A Blog post by LightOn AI on Hugging Face"
tags:
  - "clippings"
---
## ColBERT-Zero: To Pre-train Or Not To Pre-train ColBERT models?

![](https://cdn-uploads.huggingface.co/production/uploads/609bbe2f4932693ca2009d6a/xn21ll7YRj0ZftBli3-T5.jpeg)

> TL;DR: State-of-the-art ColBERT models are commonly built by taking a strong dense model and bolting on a small knowledge distillation step. We show this leaves a lot of performance on the table. By performing contrastive pre-training directly in the multi-vector setting, enabled by [PyLate](https://www.lighton.ai/lighton-blogs/pylate-flexible-training-and-retrieval-for-late-interaction-models), **ColBERT-Zero outperforms GTE-ModernColBERT and its dense base model, GTE-ModernBERT despite using only public data and sets new state-of-the-art results**. We also show that performing a supervised contrastive step before distillation closes most of the gap at a fraction of the cost. Finally, we find that aligning your prompts between pre-training and fine-tuning is non-negotiable. All [models](https://huggingface.co/collections/lightonai/colbert-zero), including intermediate checkpoints for every phase and configuration, and [full training scripts](https://github.com/lightonai/pylate/tree/main/examples/train/ColBERT-zero/) are released under Apache 2.0.

> - 📦 **Models:** [HF Collection](https://huggingface.co/collections/lightonai/colbert-zero): every phase, with and without prompts, including the **SOTA on BEIR for model <150M.**
> - 💻 **Code:** [PyLate boilerplates](https://github.com/lightonai/pylate/tree/main/examples/train/ColBERT-zero/)
> - 📄 **Paper:** [ArXiv](https://arxiv.org/abs/2602.16609)

## ColBERT models deserve better training

Late interaction models, also known as ColBERT or multi-vector models, have gained popularity thanks to their [out-of-domain](https://arxiv.org/abs/2112.01488) generalization, [long-context](https://huggingface.co/lightonai/GTE-ModernColBERT-v1) handling and [reason-intensive retrieval](https://huggingface.co/lightonai/Reason-ModernColBERT) capabilities. If you're unfamiliar with how they work and why they're powerful, our [PyLate introductory blog post](https://www.lighton.ai/lighton-blogs/pylate-flexible-training-and-retrieval-for-late-interaction-models) covers the fundamentals, and our [multi-vector retrieval ecosystem overview](https://www.lighton.ai/lighton-blogs/lightons-multi-vector-retrieval-revolution-from-research-to-production) provides the broader picture.

Despite these clear advantages, they are less studied than single-vector (dense) embedding models. Currently, state-of-the-art ColBERT models such as our own [`GTE-ModernColBERT`](https://www.lighton.ai/lighton-blogs/lighton-releases-gte-moderncolbert-first-state-of-the-art-late-interaction-model-trained-on-pylate) and [`ColBERT-small`](https://huggingface.co/answerdotai/answerai-colbert-small-v1) are simply built by performing a small knowledge distillation phase on top of a strong pre-trained single-vector model. Even the very recent [`mxbai-edge-colbert-v0`](https://www.mixedbread.com/blog/edge-v0), which detailed a recipe to train strong ColBERT models from scratch, performed all the early stages in a single-vector setting and only used the multi-vector objective in the final knowledge distillation stage.

This leaves an open question: *What if we performed the early stages of the training directly in the multi-vector setting?* Is multi-vector pre-training worth the cost, or is the final knowledge distillation step enough?

## The three training phases

Training a strong retrieval model typically involves three distinct phases, each providing a different type of learning signal. Understanding them is key to following our experiments:

![](https://cdn-uploads.huggingface.co/production/uploads/609bbe2f4932693ca2009d6a/uypt45zkZC4wrP5igo-H-.png)

Illustration of the 3 training phases

**Unsupervised contrastive pre-training** does the heavy lifting. The model processes massive amounts of paired texts (query and an associated positive document) and learns to distinguish relevant from irrelevant documents using only in-batch negatives: other documents from the same batch serve as negative examples. No human labels are needed, but this is by far the most expensive phase in terms of GPU hours.

**Supervised contrastive fine-tuning** is a refinement step. It uses smaller, higher-quality datasets where hard negatives have been specifically mined: documents that are superficially similar to the query but not actually relevant. This provides a much stronger training signal than random in-batch negatives because the model needs to differentiate between the positive and close negatives.

**Knowledge distillation (KD)** transfers knowledge from a powerful but expensive model (the "teacher") to our retrieval model (the "student"). The teacher scores a set of documents for each query, and the student learns to reproduce these scores.

## Contrastive Pre-training with PyLate

One of the reasons for the lack of pre-trained ColBERT models (compared to dense ones) has been the lack of available resources to easily explore these setups. Thankfully, [PyLate](https://github.com/lightonai/pylate) offers features that make it suitable for running such large-scale pre-training.

First, the implementation of [GradCache](https://arxiv.org/abs/2101.06983) allows us to scale the per-GPU batch size arbitrarily without VRAM constraints (as standard gradient accumulation is not beneficialapplicable for contrastive learning). Second, the option of gathering samples from other GPUs in a multi-GPU setting allows us to leverage all computed representations, scaling the effective batch size without additional memory requirements.These two features combined allow us to easily reach batch sizes of ~16k, which is required for unsupervised training to get plausible in-batch hard negatives.

Also, PyLate allows us to easily track in-training evaluations using NanoBEIR, which makes sweeping hyperparameters (like learning rate and temperature) and monitoring training significantly easier.  
Finally, we use \`split\_batches\` so that each batch is composed of only one data source at a time, to prevent [shortcut learning](https://arxiv.org/abs/2402.01613).

## Scaling Pre-training of ColBERT Models

To isolate the effect of multi-vector pre-training, we needed a controlled comparison. We chose to train on the public datasets used by [**Nomic Embed**](https://arxiv.org/abs/2402.01613) for a strategic reason: Nomic has already trained a dense `ModernBERT` model on this exact data mixture, so we can compare dense vs. multi-vector training with the same data, same base model, and same pipeline. The only variable is whether the contrastive phases are performed in the dense or multi-vector setting.

We compared three training pipelines to measure the impact of each training stage on final performance:

![](https://cdn-uploads.huggingface.co/production/uploads/609bbe2f4932693ca2009d6a/dw7rcXnXECmxSgIn7pGhQ.png)

Illustration of the different setup tested, alongside their GH200 cost

We first compare the usual setup of performing only a KD step on top of the dense pre-trained model (setting (a)) and ColBERT-zero, a model where all the pre-training steps are performed as a multi-vector model (setting (c)).  
Since the unsupervised phase is by far the most expensive step, costing roughly 10x more than the supervised and KD steps combined, we also investigated if we could cut corners. We set up a comparison to see if starting from Nomic’s `modernbert-embed-unsupervised` *dense* model and performing only the supervised and distillation steps in the multi-vector setting could yield similar results at a fraction of the cost (setting (b)).

## Results

Our evaluation on the BEIR benchmark reveals that **the standard practice of treating multi-vector training as a minor fine-tuning step significantly limits model potential**. As illustrated below, our fully pre-trained ColBERT-Zero, trained exclusively on public Nomic data, achieves an nDCG@10 of 55.43, outperforming the previous state-of-the-art GTE-ModernColBERT (54.67).

This result is particularly significant given the data disparity: the dense baseline trained on Nomic data scores 52.89, while the one trained on GTE's proprietary data scores 55.33. Despite this initial 2.4-point disadvantage in data quality, the full ColBERT pre-training pipeline allows ColBERT-Zero to overcome the gap and surpass even the `gte-modernbert` base model, **setting a new state-of-the-art results on BEIR for model <150M.**

| Model | Avg | FiQA | NFCorpus | TREC-COVID | Touche | ArguAna | Quora | SCIDOCS | SciFact | NQ | ClimateFEVER | HotpotQA | DBPedia | CQADupstack | FEVER | MSMARCO |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **Baselines** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| [ModernBERT-embed-unsupervised](https://huggingface.co/nomic-ai/modernbert-embed-base-unsupervised) | 47.05 | 42.53 | 35.33 | 68.44 | 18.58 | 48.82 | 88.63 | 19.83 | 72.30 | 46.32 | 22.97 | 60.00 | 37.97 | 42.40 | 67.39 | 34.23 |
| [ModernBERT-embed-supervised](https://huggingface.co/nomic-ai/modernbert-embed-base) | 52.89 | 40.59 | 33.40 | **84.15** | 31.91 | 48.96 | **88.85** | 18.59 | 69.63 | 62.15 | 35.67 | 67.11 | 41.50 | 42.08 | 87.35 | 41.47 |
| [GTE-ModernColBERT](https://huggingface.co/lightonai/GTE-ModernColBERT-v1) | 54.67 | 45.28 | **37.93** | 83.59 | 31.23 | 48.51 | 86.61 | 19.06 | 76.34 | 61.80 | 30.62 | 77.32 | 48.03 | 41.00 | 87.44 | 45.32 |
| [gte-modernbert-base](https://huggingface.co/Alibaba-NLP/gte-modernbert-base) | 55.33 | **48.81** | 36.44 | 81.95 | 21.68 | **72.68** | 88.55 | 21.29 | **77.40** | 57.62 | **37.74** | 69.47 | 41.79 | 42.63 | **91.03** | 40.90 |
| **KD from dense supervised** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| [ModernColBERT-embed-base-kd-only](https://huggingface.co/lightonai/ModernColBERT-embed-base-kd-only) | 54.09 | 42.51 | 37.01 | 79.52 | 34.58 | 51.75 | 87.67 | 18.15 | 75.04 | 61.45 | 28.31 | 76.70 | 47.54 | 40.68 | 84.82 | 45.57 |
| **Supervised + KD from dense unsupervised** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| [ModernColBERT-embed-base-supervised](https://huggingface.co/lightonai/ModernColBERT-embed-base-supervised) | 50.72 | 40.09 | 35.56 | 71.12 | 25.53 | 44.27 | 86.96 | 18.19 | 73.78 | 58.89 | 32.95 | 71.49 | 43.23 | 42.55 | 70.51 | 45.72 |
| [ModernColBERT-embed-base](https://huggingface.co/lightonai/ModernColBERT-embed-base) | 55.12 | 41.50 | 36.51 | 77.46 | 33.77 | 52.45 | 86.26 | 18.66 | 74.90 | 62.24 | 37.27 | **80.07** | **48.27** | 41.60 | 89.71 | **46.17** |
| **ColBERT-Zero** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| [Unsupervised](https://huggingface.co/lightonai/ColBERT-Zero-unsupervised) | 51.44 | 45.38 | 36.88 | 67.82 | 22.59 | 51.53 | 87.78 | 22.30 | 76.76 | 58.80 | 24.24 | 68.29 | 43.16 | **45.76** | 81.58 | 38.78 |
| [Supervised](https://huggingface.co/lightonai/ColBERT-Zero-supervised) | 51.81 | 42.45 | 35.60 | 74.72 | 23.83 | 41.81 | 87.19 | 19.85 | 73.71 | 61.95 | 35.01 | 71.37 | 46.20 | 45.16 | 72.61 | 45.68 |
| [Distilled](https://huggingface.co/lightonai/ColBERT-Zero) | **55.43** | 42.62 | 37.28 | 78.69 | 36.13 | 53.07 | 85.24 | 19.88 | 76.50 | 61.66 | 35.72 | 79.41 | 47.48 | 41.34 | 90.59 | 45.80 |

### The standard recipe leaves performance on the table.

The KD-only approach (pipeline **(a)** on the figure above) scores 54.09, lagging behind full pre-training by 1.3 points. This confirms that a simple distillation step is insufficient for optimal multi-vector performance.

### Supervised + KD is the efficiency sweet spot.

We investigated whether the gap could be closed without the expensive unsupervised phase. By running a supervised contrastive step in the multi-vector setting before distillation (pipeline **(b)** on the figure above), we observed a gain of over 1 point, reaching 55.12 nDCG@10. This effectively closes the gap with the fully pre-trained model (55.43), offering a highly efficient alternative that skips the most computationally intensive training stage while retaining nearly all the performance benefits. This costs ~40 GH200-hours instead of ~408: roughly **10× cheaper for 99.4% of the performance**.

![](https://cdn-uploads.huggingface.co/production/uploads/609bbe2f4932693ca2009d6a/V1_hTZ0VnJHldfd3Ip-Jm.png)

BEIR average performance w.r.t GH200-hours spent on ColBERT training

### The critical role of Prompt Alignment.

Nomic's base models are pre-trained with specific asymmetric prompts (`search_query:` and `search_document:`) prepended to queries and documents. While ColBERT already has its own asymmetric mechanism through `[Q]` and `[D]` markers, we found that aligning the fine-tuning setup with these pre-training prompts is essential: stripping them during fine-tuning led to significant performance degradation. Conversely, *adding* prompts to a model that was *not* pre-trained with them also hurt performance. The takeaway is clear: **whatever prompt setup your base model was trained with, you need to preserve it downstream.**

But alignment alone doesn't explain everything. Even when comparing apples to apples, that is, full ColBERT pre-training [with prompts](https://huggingface.co/lightonai/ColBERT-Zero) vs. [without prompts](https://huggingface.co/lightonai/ColBERT-Zero-noprompts), no mismatch, we still observe a meaningful gap (54.61 vs. 55.43 nDCG@10). This suggests prompts provide an intrinsic benefit in their own rights

Why? Our leading hypothesis is that the prompt tokens act as implicit query expansion: extra slots that don't carry specific meaning but let the model store global information about the sequence. The original ColBERT model used PAD tokens for this purpose, but modern Flash Attention implementations disabled this trick since they do not produce usable embeddings for masked tokens. Explicit prompt tokens may be quietly re-enabling it. We ran ablations (detailed in the paper) to try to separate prompt content from sequence length effects, but the picture remains unclear, and our preliminary analysis seems to point to a richer interaction between these factors: an interesting avenue for future work.

**The practical takeaway: always align your prompts with the base model's pre-training setup. Misalignment is one of the easiest ways to silently lose performance.**

![](https://cdn-uploads.huggingface.co/production/uploads/609bbe2f4932693ca2009d6a/uZoRA7SwisR-svi4lPDTi.png)

Effect of adding prompts during the fine-tuning of models pre-trained with and without prompts

## Discussion

We deliberately chose the Nomic Embed data to enable a controlled comparison with existing dense models trained on the same mixture. While this grounds our findings in a well-established setup, it also means some observations may not generalize to different or stronger training configurations, an avenue we leave for future work.

For instance, we noted that prompt alignment is critical for good performance. However, when we experimented with stronger fine-tuning data ([NV-Retriever](https://arxiv.org/abs/2407.15831) on various datasets), adding prompts on top of a ColBERT model pre-trained *without* them did not degrade results the way it did with ColBERT-Zero. With stronger or longer fine-tuning, the model has enough room to adapt to an initial mismatch. So while "align your prompts" is sound default advice, it becomes less critical the heavier your downstream training is.

Likewise, the small remaining advantage of pre-training a ColBERT model, rather than relying solely on fine-tuning and KD, is likely influenced by the quality and scale of those subsequent phases. Given that knowledge distillation typically *improves* results after supervised fine-tuning, the fact that a prior contrastive phase further enhances performance suggests that these gains are less about the specific objective and more about the *scale of training*. This extra capacity allows the model more time to optimize within a multi-vector setting. Consequently, performing KD alone at a larger scale might yield similar, if not superior, results due to the higher quality of the distillation signal. The goal of this study, however, was to explore the conventional setup where training scale is inversely proportional to signal quality, reflecting the higher cost of generating high-quality labels. Thus, the results of each phase primarily highlight the impact of *scale* within those phases rather than the specific training objective itself.

## Conclusion

Our results demonstrate that the conventional approach to training ColBERT models leaves significant performance on the table. Whether through full pre-training or our efficient supervised-first recipe, treating the multi-vector objective as a first-class citizen allows public data to outperform proprietary, closed-source models and create state-of-the-art models.

For your own pipelines, the lesson is clear: adding a supervised step before distillation is a massive efficiency hack, and aligning your prompts with the base model is non-negotiable to avoid performance degradation.

For serving these models at scale, check out [NextPlaid](https://www.lighton.ai/lighton-blogs/introducing-lighton-nextplaid) and [FastPlaid](https://www.lighton.ai/lighton-blogs/fastplaid), our production-grade engines for multi-vector retrieval.

In order to enable more exploration, we release all the code and models (including intermediate ones) under Apache 2.0 license.

*Now that we showed that we can train SOTA models with non-SOTA data, what would happen if we used SOTA data? Just a little more patience...*

> - 📦 **Models:** [HF Collection](https://huggingface.co/collections/lightonai/colbert-zero): every phase, with and without prompts, including the **SOTA on BEIR for model <150M.**
> - 💻 **Code:** [PyLate boilerplates](https://github.com/lightonai/pylate/tree/main/examples/train/ColBERT-zero/)
> - 📄 **Paper:** [ArXiv](https://arxiv.org/abs/2602.16609)

### Acknowledgments

This work was supported as part of the Swiss AI Initiative by a grant from the Swiss National Supercomputing Centre (CSCS) under project `IDa120` on Alps.

We also want to thank Raphaël Sourty for the helpful discussions and reviewing the early version of this work, as well as Tom Aarsen and Oskar Hallström for their feedback on the BP!

Please also note that this work has been performed in collaboration with Ecole Polytechnique de Lausanne (EPFL) through the participation of Luca Arnaboldi and Florent Krzakala.

More from this author

## [DenseOn with the LateOn: Open State-of-the-Art Single and Multi-Vector Models](https://huggingface.co/blog/lightonai/denseon-lateon)

lightonai

38

April 21, 2026

## [LateOn-Code & ColGrep: LightOn unveils state-of-the-art code retrieval models and code search tooling](https://huggingface.co/blog/lightonai/colgrep-lateon-code)

lightonai

56

February 12, 2026