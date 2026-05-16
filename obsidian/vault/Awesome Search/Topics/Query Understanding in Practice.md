---
type: topic
aliases: ["query understanding pipeline", "QU in practice", "query processing"]
tags: [topic, query-understanding, nlp, pipeline]
related_concepts: ["[[Query Understanding]]", "[[Query Types]]", "[[Search Intent]]", "[[Synonyms]]", "[[Spelling Correction]]", "[[Autocomplete]]", "[[Agentic Search]]"]
related_topics: ["[[E-commerce Search]]", "[[Autocomplete and Autosuggest]]", "[[Synonyms and Vocabulary Management]]", "[[Conversational and Agentic Search]]"]
articles: [
  "[[AI for Query Understanding]]",
  "[[Food Discovery with Uber Eats - Building a Query Understanding Engine]]",
  "[[Query Understanding - Introduction]]",
  "[[Query Understanding - Divided into Three Parts]]",
  "[[Mapping Search Queries To Search Intents]]",
  "[[Semantic Search Without Embeddings]]"
]
people: ["[[Daniel Tunkelang]]"]
companies: ["[[Uber]]", "[[Grubhub]]", "[[Spotify]]"]
created: 2026-05-16
---

# Query Understanding in Practice

How to build a query understanding pipeline — the set of transformations applied to a raw user query before retrieval begins.

---

## Tunkelang's Three-Part Framework

Every query requires understanding at three levels:

1. **Tokenization and normalization** — splitting, lowercasing, stemming, language detection
2. **Query annotation** — NER (entity extraction), intent classification, attribute detection
3. **Query reformulation** — spelling correction, synonym expansion, query rewriting, relaxation

Most production QU pipelines implement these sequentially, with each step informing the next.

---

## Layer 1: Tokenization and Normalization

- **Tokenization**: split query into tokens (language-specific rules for CJK, agglutinative languages)
- **Lowercasing**: standard; exceptions for acronyms (SQL, API)
- **Stemming/lemmatization**: reduce morphological variants ("running" → "run") — be conservative; overstemming hurts precision
- **Language detection**: essential for multilingual search; gate language-specific processing

---

## Layer 2: Query Annotation

### Intent Classification
Multi-label classifier assigns query intent categories:
- Navigational ("Shake Shack downtown")
- Transactional ("buy running shoes")
- Informational ("how to clean suede shoes")
- Exploratory/inspirational ("gift ideas for dad")
- Domain-specific: dish/restaurant/cuisine/attribute (Uber Eats); exact/category/thematic/symptom (e-commerce)

Multiple labels can apply. Intent determines which retrieval strategy to use.

### Entity Extraction (NER)
Extract named entities: brand names, product models, locations, cuisines, attributes.

Domain-fine-tuned NER outperforms general models for specialized vocabulary:
- "Pad See Ew" (Thai dish) correctly identified as a single entity after fine-tuning
- Generic NER treats it as three separate tokens

### Attribute Detection
Detect structured attributes within free text:
- Price signals: "under $50", "cheap", "budget"
- Color, size, material
- Temporal: "new", "latest", "2024 model"
- Location: "near me", "downtown"

Detected attributes can populate facet filters automatically or reweight ranking signals.

---

## Layer 3: Query Reformulation

### Spelling Correction
Apply before other reformulations. Domain-specific — see [[Synonyms and Vocabulary Management]].

### Synonym Expansion
Expand with known synonyms. Apply post-intent classification to avoid wrong expansions (don't expand "Apple" to "fruit" on a tech site).

### Query Rewriting
Transform natural language into more retrievable form:
- "phone case that doesn't break when dropped" → "shockproof protective phone case drop resistant"
- LLMs are well-suited for this — zero-shot, no training data needed

### Query Relaxation
When retrieval returns too few results, progressively relax constraints:
1. Remove low-weight terms
2. Replace AND with OR
3. Expand to parent category
4. Fall back to semantic search

---

## LLMs in Query Understanding

LLMs change what's practical:

| Task | Pre-LLM approach | LLM approach |
|---|---|---|
| Intent classification | Trained classifier (training data needed) | Zero-shot prompt |
| Entity extraction | Fine-tuned NER | Structured output prompting |
| Query rewriting | Rule-based templates | Open-ended rewrite |
| Multi-turn coreference | Explicit session state | Native context window |

**Recommended hybrid**:
- Spell correction: traditional (fast, reliable)
- Common intent classes: fine-tuned classifier (fastest)
- Ambiguous/complex intent: LLM
- Conversational/multi-turn: LLM (mandatory)

**LLM limitations**: latency (50-200ms), cost at scale, consistency (use structured JSON output).

---

## Domain-Specific Challenges

### Food Search (Uber Eats)
- Cuisine ambiguity: "Thai" = Thai food OR Thai restaurant?
- Dish-category gap: "pad see ew" → "Thai food" → "noodles"
- Ingredient filters: "no gluten" = filter + ranking adjustment

### E-commerce (General)
- Symptom queries: "my back hurts pillow" → infer product category
- Vocabulary gap: seller terminology vs. buyer language
- Occasion/use-case: "wedding guest outfit" → unstructured attribute

### Enterprise Search
- Acronym disambiguation: "NRR" (Net Revenue Retention vs. Net Retention Rate?)
- Cross-reference queries: "documents about the Q3 merger" → requires temporal + entity understanding
- Access-aware interpretation: same query, different documents per user role

---

## Evaluation

Query understanding is upstream of retrieval, so QU failures show up in retrieval metrics:
- **Zero-results rate**: after QU, if the reformulated query still returns nothing, QU failed
- **Intent accuracy**: offline benchmark with labeled intent annotations
- **Downstream NDCG**: does QU change improve downstream ranking quality?

---

## Related

- [[Synonyms and Vocabulary Management]] — vocabulary layer of QU
- [[Autocomplete and Autosuggest]] — suggestions reduce the QU burden
- [[Conversational and Agentic Search]] — LLM-native QU extension
- [[E-commerce Search]] — domain application
