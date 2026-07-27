---
type: video
title: "Fine-Tuning Sparse Neural Retrievers for E-Commerce Is Not That Scary"
speaker: "[[Evgeniya Sukhodolskaya]]"
company: "[[Qdrant]]"
medium: talk / video
url: https://www.youtube.com/watch?v=Ft7xHtmAFlg
published: 2026-06-30
conference: "[[MICES]]"
duration: 29:55
tags:
  - video
  - sparse-retrieval
  - splade
  - fine-tuning
  - e-commerce
  - neural-ir
topics:
  - "[[E-commerce Search]]"
  - "[[Learned Sparse Retrieval]]"
concepts:
  - "[[SPLADE]]"
  - "[[Sparse Embeddings]]"
  - "[[Sparse Vector Retrieval]]"
  - "[[BM25]]"
  - "[[Hard Negative Mining]]"
  - "[[Embedding Fine-tuning]]"
  - "[[miniCOIL]]"
  - "[[Query Expansion]]"
tools:
  - "[[Qdrant Vector DB]]"
  - "[[qdrant-sparse-finetune]]"
  - "[[Sentence Transformers]]"
people:
  - "[[Evgeniya Sukhodolskaya]]"
  - "[[Thierry Damiba]]"
created: 2026-07-27
---

# Fine-Tuning Sparse Neural Retrievers for E-Commerce Is Not That Scary

📺 **Watch:** https://www.youtube.com/watch?v=Ft7xHtmAFlg

Talk by [[Evgeniya Sukhodolskaya]] (Developer Advocate, [[Qdrant]]) at [[MICES]], June 2026. The argument: [[SPLADE]] gives you semantic matching without leaving the explainable, exact-match world of lexical search — but the off-the-shelf models are trained on web search, so they need to be pointed at your catalog. The talk walks from "what is a sparse vector" to a working fine-tuning framework, deliberately pitched at practitioners who find ML fine-tuning intimidating.

The experiments described are [[Thierry Damiba]]'s, written up with full numbers in [[Fine-Tuning Sparse Embeddings for E-Commerce Search]]. **The talk itself quotes no benchmark figures** — for those, see the article note.

## Key Moments

| Time | Topic |
|---|---|
| [02:25](https://www.youtube.com/watch?v=Ft7xHtmAFlg&t=145s) | What a sparse vector is; sparse retrieval as dot product |
| [06:20](https://www.youtube.com/watch?v=Ft7xHtmAFlg&t=380s) | SPLADE: lexical search with learned weights and term expansion |
| [09:48](https://www.youtube.com/watch?v=Ft7xHtmAFlg&t=588s) | The experiment stack and the [[Amazon ESCI Dataset]] |
| [11:46](https://www.youtube.com/watch?v=Ft7xHtmAFlg&t=706s) | Inside SPLADE: base model, MLM head, log saturation, pooling |
| [15:12](https://www.youtube.com/watch?v=Ft7xHtmAFlg&t=912s) | Two objectives: retrieve well **and** stay sparse |
| [16:16](https://www.youtube.com/watch?v=Ft7xHtmAFlg&t=976s) | The ANCE loop — a search engine inside the training loop |
| [17:04](https://www.youtube.com/watch?v=Ft7xHtmAFlg&t=1024s) | Results, forgetting, and the multi-domain model |
| [18:38](https://www.youtube.com/watch?v=Ft7xHtmAFlg&t=1118s) | Should *you* fine-tune? |
| [20:16](https://www.youtube.com/watch?v=Ft7xHtmAFlg&t=1216s) | `qdrant-sparse-finetune`: the five steps under the hood |
| [22:19](https://www.youtube.com/watch?v=Ft7xHtmAFlg&t=1339s) | Architecture config; full SPLADE vs inference-free |
| [23:13](https://www.youtube.com/watch?v=Ft7xHtmAFlg&t=1393s) | Hard-negative mining step and its resource footprint |
| [24:22](https://www.youtube.com/watch?v=Ft7xHtmAFlg&t=1462s) | Evaluation caveat: no held-out split by default |
| [24:58](https://www.youtube.com/watch?v=Ft7xHtmAFlg&t=1498s) | BigBasket smoke test |
| [25:40](https://www.youtube.com/watch?v=Ft7xHtmAFlg&t=1540s) | The hard negatives the mining actually surfaced |
| [27:57](https://www.youtube.com/watch?v=Ft7xHtmAFlg&t=1677s) | Q&A: out-of-vocabulary terms, false negatives |

---

## Sparse Retrieval, Reframed

A sparse vector has one dimension per vocabulary term; almost all are zero, and the non-zero weights encode each term's importance *for the task*. Encode query and product as sparse vectors, take the dot product, and only shared non-zero dimensions contribute — which is exactly exact-match lexical search.

This reframing is what lets a vector database do lexical retrieval. [[BM25]] becomes "a sparse vector whose weights happen to be term frequency, inverse document frequency and length normalization", scored through a classic inverted index. Sukhodolskaya's framing: *"everybody thinks Qdrant is a vector search engine so they can't do lexical search — but no, we hacked it."*

BM25's limit is that it has no notion of context. **"Apple juice" and "Apple iPhone" contain the same `apple`** — statistically identical, commercially nothing alike. The usual answer is dense retrieval, but practitioners find its fuzziness hard to trust.

### The middle ground

[[SPLADE]] keeps the exact-match, inverted-index world but replaces statistical weights with **learned** ones, and additionally **expands** the representation with synonyms. You get synonym search that is still explainable term by term — "much less fuzzy than dense search".

## Why Off-the-Shelf SPLADE Underdelivers on Catalogs

Nearly every public SPLADE checkpoint — FastEmbed, [[Sentence Transformers]], Hugging Face, cloud inference — is trained on [[MS MARCO]]: **web queries against Wikipedia passages**. The learned weights and the synonym expansions reflect that text.

The canonical demo ("Nike running shoes" → "footwear") looks fine. In practice, Sukhodolskaya notes, you inference SPLADE on real catalog text, look at the expansions, and think *"what is that?"* The model needs nudging toward your data.

## Inside SPLADE (and how it maps to config)

| Component | What it does |
|---|---|
| **Base model** | A dense encoder — supplies context, so it knows the `iPhone` in `Apple iPhone` is a phone |
| **MLM head** | Vocabulary reader and probabilistic synonym expander — trained right, "noise cancelling headphones" lights up the brands that matter for *you* |
| **Log saturation** | A learned analogue of BM25 term-frequency saturation — stops one term dominating |
| **Sparsity penalty** | Without it the model cheats: *"ML models are smart and lazy, they want to train away your requirements"* — it will return a dense vector unless penalized |
| **Pooling** | Collapses the per-token vocabulary distributions into one sparse vector |

In [[Sentence Transformers]] v5 these appear as two modules: `MLMTransformer` (base model + MLM head) and `SpladePooling` (log saturation + pooling).

### Choices made in the experiment

- **Base model: plain DistilBERT**, not an existing SPLADE checkpoint — starting from scratch to see how much domain fine-tuning is actually worth.
- **Full SPLADE, not inference-free.** The inference-free variant skips the expensive encoder pass on the query side to save latency. Sukhodolskaya recommends against it for e-commerce: **the domain is intent-heavy**, and "Apple juice" vs "Apple iPhone" are two different intents around the same token — that distinction is precisely what you lose.
- **Max pooling** — the standard.

## The ANCE Loop

To learn, the model needs positives (from your data) and negatives. Randomly sampled negatives are useless — *"I'm querying for iPhone and I'm getting banana"* teaches nothing.

Instead, plug the search engine into the training loop:

1. Take the current checkpoint
2. Index the training corpus into [[Qdrant Vector DB]] with it
3. Retrieve for each query — the top results are **what the model believes is relevant**
4. Filter out the actually-relevant ones; the rest are hard negatives, by construction
5. Feed them into the next training step and repeat

See [[Hard Negative Mining]]. The talk's most concrete illustration comes from the [[qdrant-sparse-finetune]] smoke test: querying **"Pampers medium diapers"** surfaced the same brand in the *wrong size*, a *competitor* in the right size, and *adult* diapers — all plausible-looking, all wrong.

## Specialize or Generalize

Fine-tuning on one catalog makes the model good at that catalog and worse elsewhere. The counter-move is multi-domain training (Sentence Transformers supports it), which produced a more generalist model trained across three datasets.

Sukhodolskaya's decision rule:

- **Single retailer with data** → fine-tune on your catalog
- **Marketplace / multi-retailer** → multi-domain training
- **Already happy with what you have** → *"if it works it works, don't touch it"*

## The Framework

[[qdrant-sparse-finetune]] — open source, three lines to run, five steps under the hood: parse catalog → obtain or generate queries → build the SPLADE architecture from config → train with Qdrant-based hard-negative mining → publish to Hugging Face.

Sukhodolskaya is candid that it is **"slightly shaky"**: you must name the ID column and text fields explicitly, and the built-in evaluation runs on training data — she had to hand-roll a held-out query split. *"If the numbers look too good, don't get too excited immediately."*

Her own smoke test on the BigBasket Kaggle catalog fine-tuned an **already-off-the-shelf SPLADE** and found it was performing decently unmodified — a case for leaving it alone. The evaluation was also weakened by LLM-generated queries being too literal: almost purely lexical, no synonymy, so **BM25 scored well too**. Her conclusion — work harder on the prompts, or test on real queries.

## Q&A

**Out-of-vocabulary terms.** SPLADE's output dimensions *are* the base model's vocabulary, so tokens outside it cannot be represented. Qdrant's [[miniCOIL]] handles this by falling back to a BM25 weight in the same sparse vector; SPLADE has no such mechanism, so *"you need to pick a model which knows your tokens."*

**False negatives in mining.** Asked whether mining can label a true positive as a negative: yes, acknowledged outright. A possible mitigation is a side model — perhaps a dense one — acting as judge, at the cost of extra overhead. *"It's always a trade-off."*

## Related

- Article: [[Fine-Tuning Sparse Embeddings for E-Commerce Search]] — the five-part write-up with all benchmark numbers
- Concepts: [[SPLADE]] · [[Learned Sparse Retrieval]] · [[Sparse Embeddings]] · [[Hard Negative Mining]] · [[miniCOIL]]
- Dataset: [[Amazon ESCI Dataset]] — the training data; [[MS MARCO]] — what off-the-shelf SPLADE was trained on instead
- Tools: [[qdrant-sparse-finetune]] · [[Qdrant Vector DB]] · [[Sentence Transformers]]
- Conference: [[MICES]]
- Compare: [[Fine-Tuning Text Embeddings For Domain-Specific Search]] — the same argument on the dense side
