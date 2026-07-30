---
title: "Out-of-Vocabulary"
aliases: ["OOV", "out of vocabulary", "out-of-vocabulary terms", "unknown tokens", "UNK"]
type: concept
tags:
  - concept
  - neural-ir
  - sparse-retrieval
  - lexical-search
  - retrieval
created: 2026-07-30
---

# Out-of-Vocabulary

A term the system cannot represent because it falls outside a **fixed vocabulary** fixed before the
term was ever seen. OOV is where the open-endedness of language collides with the closed vocabulary
a neural model was pre-trained with — and it is the axis on which several retrieval models in this
vault are differentiated from one another.

---

## Why lexical search barely has this problem

An inverted index's vocabulary **is the corpus**. Index a document containing a brand new part
number and that part number becomes searchable; no retraining, no vocabulary decision. [[BM25]] will
score any term that appears, and a rare term gets a *high* IDF rather than no representation at all.

Lexical retrieval still has *rare-term* problems — a term seen once or twice gives little to estimate
from, and IDF computed on a tiny sample is noisy. But those are problems of **estimation**, not of
representability: the term is in the index either way. This robustness is a large part of why the
lexical leg keeps earning its place in [[Hybrid Search]].

## Why neural retrieval has it acutely

A transformer's tokenizer carries a vocabulary fixed at pre-training (~30K WordPieces for vanilla
English BERT). Everything the model can express is built from those pieces. See [[Tokenization]].

**Subword decomposition softens this, but does not remove it.** An unfamiliar word is normally split
into known fragments rather than discarded, which is precisely why a 30K vocabulary can cover
open-ended text — a true `[UNK]` is the residual case, for input that cannot be decomposed at all
(unseen scripts, exotic characters). The simplified telling that unknown words "collapse to `UNK`"
is common, and directionally right about the consequence, but the mechanism is usually fragmentation
rather than erasure.

The practical problem is subtler than erasure, and worse than it sounds: **decomposition is not
understanding.** A novel brand name split into three familiar fragments yields three fragments the
model has no learned meaning for in that combination. You get a representation, just not a useful
one.

## Where it bites hardest

- **E-commerce** — SKUs, part numbers, model codes, and brand names, which are exactly the queries
  users are most confident about and least tolerant of failure on
- **Specialist domains** — medical, legal and industrial vocabulary absent from web-scale pre-training
- **Emergent terms** — new products, slang, events postdating the model
- **[[Multilingual Search]]** — vocabulary budget is split across scripts, so per-language coverage thins

## The SPLADE / miniCOIL contrast

This is the vault's recurring worked example of OOV as a *design* constraint rather than a nuisance.

[[SPLADE]]'s output dimensions **are** its base model's vocabulary. A term outside it is not merely
poorly weighted, it is unrepresentable, and there is no fallback path — you must choose a base model
that already knows your tokens. See its *Vocabulary limits* section.

[[miniCOIL]] was built around the opposite choice: **a word with no miniCOIL training falls back to
plain [[BM25]] scoring within the same sparse vector.** It also works at word level rather than
subword level, deliberately avoiding the subword tokenization that made its COIL predecessor
impractical.

| | [[SPLADE]] | [[miniCOIL]] |
|---|---|---|
| Out-of-vocabulary term | Unrepresentable | Falls back to BM25 |
| Relationship to BM25 | Replaces the weighting | Extends the formula |
| Domain adaptation | Fine-tune per catalog | Designed to generalize |

The tradeoff is real in both directions: fine-tuned SPLADE buys large in-domain gains at the cost of
transfer, which is the finding in [[Fine-Tuning Sparse Embeddings for E-Commerce Search]].

## Mitigations

1. **Pick a base model that already knows your tokens** — the only fix when the architecture offers
   no fallback.
2. **Keep a lexical leg.** [[Hybrid Search]] means an OOV term still retrieves through [[BM25]] even
   when the neural leg is blind to it. The complementarity is not just semantic-vs-exact; it is also
   closed-vocabulary-vs-open.
3. **Choose an architecture with graceful degradation** — miniCOIL's BM25 fallback.
4. **Fine-tune or extend the vocabulary** for a domain, accepting the transfer cost.
5. **Fix it upstream.** Many apparent OOV terms are misspellings or variants of in-vocabulary ones;
   see [[Spelling Correction]] and [[Synonyms]].

This connects to [[Zero-Shot Retrieval]], where the same instinct appears in general form: preserve a
signal that does not depend on having seen the domain.

## Related Concepts

- [[Tokenization]] — the fixed vocabulary that defines the boundary
- [[BM25]] — open-vocabulary by construction; the usual fallback
- [[SPLADE]] — no fallback path; the constraint at its sharpest
- [[miniCOIL]] — BM25 fallback as an explicit design goal
- [[Learned Sparse Retrieval]] — the family where the tradeoff plays out
- [[Sparse Embeddings]] — contrasts the two on exactly this axis
- [[Hybrid Search]] — keeping an open-vocabulary leg is itself a mitigation
- [[Zero-Shot Retrieval]] — generalizing to domains never seen in training
- [[Spelling Correction]] · [[Synonyms]] — resolve pseudo-OOV before retrieval

## Articles

- [[Three mistakes when introducing embeddings and vector search]] — vocabulary limits of vanilla BERT
- [[Fine-Tuning Sparse Embeddings for E-Commerce Search]] — in-domain gains vs transfer

## Videos

- [[Evgeniya Sukhodolskaya - Fine-Tuning Sparse Neural Retrievers for E-Commerce]] — the Q&A where SPLADE's vocabulary limit is raised directly

## People

- [[Evgeniya Sukhodolskaya]] — miniCOIL and its OOV fallback
