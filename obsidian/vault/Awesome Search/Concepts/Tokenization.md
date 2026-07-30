---
title: "Tokenization"
aliases: ["tokenizer", "tokenizers", "analyzer", "text analysis", "subword tokenization", "WordPiece", "BPE", "SentencePiece"]
type: concept
tags:
  - concept
  - lexical-search
  - query-understanding
  - neural-ir
  - multilingual
created: 2026-07-30
---

# Tokenization

Splitting raw text into the discrete units a system actually operates on. It is the first
irreversible decision in almost every retrieval pipeline: nothing downstream can match, weight or
embed a distinction that tokenization has already thrown away.

---

## Two senses of the word

Like [[Pooling]], "tokenizer" names two different things that share a name and are easy to conflate.

| | **Analyzer tokenization** | **Model tokenization** |
|---|---|---|
| Produces | Index terms | Token IDs for an encoder |
| Vocabulary | Open — whatever the corpus contains | Fixed at pre-training (~30K for BERT) |
| Consumed by | [[Full-Text Search\|Inverted index]], [[BM25]] | Transformer encoders |
| Configurable? | Yes, per field, at index time | No — baked into the model |
| Typical schemes | standard, whitespace, edge-ngram, path-hierarchy, CJK | WordPiece, BPE, SentencePiece |
| Failure mode | Recall loss from mismatched analysis | [[Out-of-Vocabulary]] terms |

The two coexist in a [[Hybrid Search]] system: the lexical leg analyzes, the dense and learned-sparse
legs use the model's own tokenizer, and they do **not** agree on what a token is.

## Analyzer tokenization

In Lucene-based engines the tokenizer is one stage in an **analysis chain** — char filters →
tokenizer → token filters (lowercase, stemming, [[Stopwords|stopwords]], [[Synonyms|synonyms]]).
[[PostgreSQL]] splits the same job across differently-named objects, where the **parser** plays the
tokenizer's role and dictionaries play the token filters'; see [[Search using PostgreSQL]] for the
full mapping.

Tokenizer choice is a design decision per field, not a global default:

- **Standard / whitespace** — the baseline for ordinary prose.
- **Edge-ngram** — emits prefixes so a query can match mid-word; the mechanism behind fast
  as-you-type [[Autocomplete]] (`min_gram`/`max_gram` trade memory for latency).
- **Path-hierarchy** — emits every ancestor path of a hierarchical value. [[Doug Turnbull]] uses this
  to make taxonomy similarity work in a plain BM25 index, letting IDF score leaf nodes above root
  nodes; see [[Semantic Search Without Embeddings]].
- **UAX URL-email** — keeps URLs and addresses intact rather than shattering them on punctuation.
  See [[Bonsai - Designing Search for a Relational Database]] for per-field analyzers in production.

### The consistency invariant

**Query-time and index-time tokenization must agree.** A mismatch does not error — it silently
returns fewer results, because the query produces terms the index never contained. This is the
failure mode [[Daniel Tunkelang]] singles out in [[Query Understanding - Tokenization]], and it is
what makes tokenization changes to a live index expensive: altering the analyzer means reindexing.

### What it decides

- **Hyphens and punctuation** — whether `t-shirt` is one token or two, and whether a user typing
  `tshirt` finds either.
- **Part numbers, SKUs, measurements** — domain tokens that should survive intact. A spurious dash
  shouldn't block a user who clearly knows what they want.
- **Compounds** — languages that concatenate (German, Dutch, Finnish) need decompounding or the
  whole compound is one unmatchable term.
- **Script** — Latin, CJK, Arabic and Devanagari need genuinely different tokenizers; CJK has no
  whitespace to split on at all. See [[Multilingual Search]].
- **Phrases** — tokenizing `New York` into two tokens makes `New` match unrelated documents; see
  [[Collocations]] and [[Query Segmentation]].

## Model tokenization

Neural models carry their own tokenizer, fixed at pre-training. Rather than emitting whole words,
modern schemes are **subword**: an unfamiliar word is decomposed into smaller known fragments
instead of being discarded, which is how a fixed ~30K vocabulary covers open-ended text.

This has a consequence that matters well beyond preprocessing: **the model's vocabulary is a hard
boundary on what it can represent.** [[SPLADE]]'s output dimensions literally *are* its base model's
vocabulary, so tokens outside it have nowhere to go. [[miniCOIL]] was designed at **word level**
specifically to avoid the subword tokenization that made its COIL predecessor impractical. See
[[Out-of-Vocabulary]] for how retrieval models cope.

Subword boundaries also leak into scoring. [[ColBERT]] matches over WordPiece tokens, so its
per-token vectors are per-*fragment* vectors, and [[Token Pooling]] compresses those fragments.

## Why it's worth caring about

[[Doug Turnbull]]'s primer puts it bluntly — *"Tokenization matters a lot. Not just in lexical
search, but embeddings too."* It is also, in practice, one of the first things to check when a query
mysteriously returns nothing: mis-tokenization, a missing synonym and a bad feature weight all look
identical from the outside. See [[What AI Engineers Should Know about Search]] and
[[Hiring for Search]], which uses exactly this diagnostic as an interview signal.

## Related Concepts

- [[Full-Text Search]] — analysis is one of its three core machinery pieces
- [[Out-of-Vocabulary]] — the failure mode of fixed model vocabularies
- [[BM25]] — scores whatever terms tokenization produced
- [[Stopwords]] · [[Synonyms]] · [[Spelling Correction]] — the token filters that follow
- [[Query Segmentation]] — deciding which adjacent tokens form one unit
- [[Collocations]] — phrases that tokenization should not split
- [[Query Understanding]] — tokenization is layer 1 of the pipeline
- [[SPLADE]] · [[miniCOIL]] — learned sparse models, bounded by their tokenizer's vocabulary
- [[ColBERT]] · [[Token Pooling]] — per-token vectors are per-subword vectors
- [[Text Chunking]] — the document-level analogue: splitting into passages, not terms
- [[Autocomplete]] — edge-ngram tokenization is the enabling trick

## Related Topics

- [[Multilingual Search]] — script and compounding make tokenization the hardest layer
- [[Query Understanding in Practice]] — "Layer 1: Tokenization and Normalization"
- [[Search using PostgreSQL]] — parser/dictionary vs tokenizer/token-filter mapping

## Articles

- [[Query Understanding - Tokenization]] — [[Daniel Tunkelang]]; the consistency requirement
- [[Semantic Search Without Embeddings]] — [[Doug Turnbull]]; hierarchical tokenizer + BM25
- [[What AI Engineers Should Know about Search]] — why it matters for embeddings too
- [[How to Really Do Autocomplete]] — edge-ngram tokenizer in a production suggest design
