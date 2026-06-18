---
type: topic
aliases: ["search hiring", "hiring search engineers", "search team roles"]
tags: [topic, hiring, team, search-team]
related_concepts: ["[[Search Relevance]]", "[[Learning to Rank]]"]
related_topics: ["[[Managing a Search Team]]", "[[Economics of Search]]"]
articles: [
  "[[Thoughts about Managing Search Teams]]",
  "[[On Search Leadership]]",
  "[[Search Product Management - The Most Misunderstood Role]]"
]
people: ["[[Daniel Tunkelang]]"]
created: 2026-05-16
---

# Hiring for Search

Roles, skills, and evaluation criteria for building a search team. Search is a specialized enough domain that generic engineering hiring criteria miss what matters.

---

## Roles on a Search Team

### Relevance Engineer / Search Engineer
The core role. Owns the bridge between IR fundamentals and production systems.

**Key skills:**
- Information retrieval foundations: BM25, inverted indexes, TF-IDF, precision/recall
- Ranking system design: two-stage retrieval, LTR pipeline, feature engineering
- Query analysis: query understanding, tokenization, synonym handling
- Evaluation: building and running offline eval; interpreting NDCG, MAP, MRR
- Search engine internals: Elasticsearch / Solr / Vespa / OpenSearch configuration and tuning

**What separates good from great:** ability to form a hypothesis about why a query fails, design a measurement to test it, and implement the fix — without breaking unrelated queries.

---

### ML Engineer (Ranking / Retrieval)
Owns the model layer: learning-to-rank models, embedding models, re-rankers.

**Key skills:**
- Feature engineering for ranking (query-document features, user context features)
- Training pipelines: offline data prep, label collection, train/eval splits
- Model serving: latency-conscious inference, ONNX export, model distillation
- Vector search: embedding models, HNSW, quantization
- Implicit feedback: click models, position bias correction, counterfactual learning

**What separates good from great:** understanding of the full data flywheel — how model decisions affect user behavior, which affects training data, which affects the next model.

---

### Search Data Scientist
Owns the measurement layer.

**Key skills:**
- Experiment design: power analysis, randomization, statistical significance
- Click modeling: position bias correction, interleaving analysis
- Query log analysis: identifying patterns in head/torso/tail query distribution
- Business metric definition: tying search changes to revenue, retention, task completion

**What separates good from great:** skepticism about easy wins; ability to detect when an A/B "win" is a measurement artifact rather than a real improvement.

---

### Search Product Manager
The rarest and hardest to hire.

**Key skills:**
- Technical depth: can read a ranking formula, understand precision/recall tradeoffs, interpret eval results
- Measurement orientation: treats every change as an experiment; comfortable saying "we don't know yet"
- Stakeholder translation: can explain why a relevance regression is a business problem to execs
- Roadmap strategy: balances quick wins (head query fixes) with compound investments (infrastructure, models)

**What separates good from great:** ability to resist the pressure to ship features without measurement.

---


### UX Researcher
Owns qualitative signal: user intent studies, usability testing, task analysis.

Provides the ground truth that quantitative metrics can't — *why* users behave the way they do. Not always considered a "search role" but fills the gap when metrics look fine and users are still complaining.

**When you need one**: entering a new domain where intent patterns are unknown, or when engagement metrics and satisfaction surveys diverge.

---

### Relevance Annotator / Judgment Analyst
Produces and maintains [[Judgment Lists]] — human-labeled relevance assessments that power offline evaluation.

Often treated as a commodity task, but annotation quality directly determines the quality of your eval harness. Annotators with domain knowledge are a compounding asset; bad annotations make your offline eval misleading.

**Key skill**: calibration — consistent, explainable ratings across a large query set. Annotation guidelines matter more than raw annotator quality.

## What to Look For in Candidates

### Evaluation Mindset
The single most important trait across all search roles. Candidates who have never thought about how to measure whether their changes worked are a red flag regardless of technical depth.

Interview signal: "Walk me through how you would know if a ranking change improved user experience."

### IR Fundamentals
Surprisingly rare even among experienced engineers. Many candidates have worked with search systems without understanding why they work.

Interview signal: "Explain BM25 and why it works better than raw term frequency for ranking." Or: "What's the difference between recall and precision, and when do you optimize for each?"

### Debugging Instinct
Search failures are often subtle. A good search engineer can look at a failing query and reason about why — was it a tokenization issue, a missing synonym, a feature weight, a training data artifact?

Interview signal: present a real failing query from your system (anonymized if needed) and ask them to walk through their debugging process.

### Scale Awareness
Solutions that work on 10k documents fail differently than at 100M. Candidates should have intuition about the scaling properties of the systems they propose.

---

## Common Hiring Mistakes

**Hiring generic software engineers and expecting them to learn search.** IR is a specialized field. The ramp time for someone with no background is 6-12 months before they're net positive on relevance work.

**Prioritizing ML credentials over IR fundamentals.** A PhD in ML who has never thought about recall or precision will spend months rebuilding intuition that an experienced relevance engineer already has.

**Not testing for evaluation mindset.** Engineers who haven't worked with eval harnesses will default to eyeballing queries, which doesn't scale.

**Undervaluing domain expertise.** For vertical search (medical, legal, e-commerce), domain knowledge is a multiplier on technical skill. A relevance engineer who understands product catalogs will outperform a better engineer who doesn't.

**Skipping the search PM hire.** Teams that have no search PM default to engineering-driven roadmaps, which tend toward infrastructure at the expense of user-facing quality.

---

## Seniority and Sequencing

For a team building from scratch, suggested hiring order:

1. **Senior relevance engineer** — sets evaluation culture, architectural decisions, standards
2. **Search PM** — without this, the team will lack strategic direction
3. **ML engineer** — once you have an eval harness and a baseline, you can iterate on models
4. **Data scientist** — once you have enough traffic to run experiments
5. **Junior engineers** — after you have enough structure to onboard and mentor

Hiring data scientists before you have an eval harness is premature — there's nothing for them to measure.

---

## Interview Process Recommendations

- **Take-home relevance task**: give a small document corpus, a set of queries, and ask them to improve rankings with any approach they choose. Evaluate methodology, not just output.
- **System design**: "Design a search system for [your domain] from scratch — what are the components and tradeoffs?"
- **Failure case walkthrough**: review a real or synthetic failing query together and ask for reasoning
- **Metrics discussion**: "What metric would you use to evaluate this change, and why?"

---

## Related

- [[Managing a Search Team]] — how to structure the team once hired
- [[Economics of Search]] — headcount is a major cost driver
- [[Daniel Tunkelang]] — canonical writing on search team composition and leadership
- [[How to Start a Career in Search]] — the candidate's-eye view: how to prepare for these roles
