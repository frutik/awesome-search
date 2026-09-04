# The Generalization Cliff

A general-purpose embedding model that tops a public leaderboard is not, on that evidence, a model that will work on your data. The gap between "good on MTEB" and "good on your queries" is not a gentle slope — it is a cliff, and we have both the sharpest number and the mechanism behind it.

---

## The Collapse, In One Number

[[BRIGHT]] is the cleanest demonstration: a model scoring 59.0 nDCG@10 on [[MTEB]] scores **18.3** on BRIGHT. That is not a modest degradation, it is a collapse. BRIGHT's queries come from StackExchange, LeetCode, and math competitions, and the relevant document is connected to the query only by inference — a shared theorem, an analogous algorithm — never by shared vocabulary or obvious semantic proximity. Whatever dense [[Embeddings|embedding]] models are good at, it is not multi-step reasoning about relevance. Semantic similarity, which is all a [[Bi-Encoder]] can express, turns out to be a poor proxy for "this document helps answer this question" once the connection to the query stops being lexical or topical.

## It's Not Just Reasoning-Intensive Queries

BRIGHT is the extreme case, but the same cliff shows up on ordinary in-domain retrieval, without any reasoning required. As [[Model Selection and Fine-Tuning Evaluation]] puts it: [[MTEB]] and [[BEIR]] measure general-domain performance and are heavily optimized against, so leaderboard position reflects benchmark fit as much as model quality. It is routine — not exceptional — for the board leader to lose to a mid-ranked model on in-domain data. A model can be excellent at "general text similarity" and mediocre at "this catalog" or "this legal corpus" simultaneously, because those are different skills that public benchmarks do not separate.

## Why: Contamination and a Relocated Incentive

[[RTEB]] names the mechanism directly: public benchmarks reward memorization. When corpus, queries, and labels are all public, they leak into training data, and a model that has effectively seen the test posts a score that does not survive contact with new data. RTEB's answer — splitting datasets into an open half and a maintainer-held private half — makes the gap measurable: a model that scores well on the open datasets and drops sharply on the private ones has been trained on the test. But RTEB's own governance history is the more interesting lesson: in 2026 the private column was temporarily removed after concerns that vendors with access to the private data held a structural advantage. Keeping a test set secret does not eliminate the incentive problem, it relocates it — someone has to hold the secret, and if that party also competes, the benchmark inherits a new conflict of interest in place of the old contamination one.

[[BEIR]] established the earlier generation of this same critique: models trained on one corpus (usually [[MS MARCO]]) evaluated zero-shot on eighteen unrelated ones. Its most durable finding — that [[BM25]] is a stubbornly strong zero-shot baseline — is itself evidence for the cliff: a method with no learned generalization to fail has nothing to fall off.

## The Fix Closes Most of the Gap

Domain [[Embedding Fine-tuning|fine-tuning]] is the direct response, and there are two worked examples showing how large the recovery is.

[[Fine-Tuning Text Embeddings For Domain-Specific Search|Shaw Talebi's tutorial]] frames the failure concretely with a medical Q&A task: a general `all-MiniLM-L6-v2` model asked "What causes hypertension?" retrieves articles about blood pressure generally — "similar" in general English, not "medically relevant" — and misses the specialized connection from ACE inhibitors to the renin-angiotensin system. Fine-tuning on domain triplets with [[Hard Negative Mining|hard negatives]] closes much of that gap: reported NDCG@10 gains of +12–18%, with diminishing returns past roughly 10,000–20,000 examples.

[[Fine-Tuning Sparse Embeddings for E-Commerce Search|Thierry Damiba's SPLADE series]] puts numbers on the same story for sparse retrieval: off-the-shelf [[SPLADE]], trained on MS MARCO web search, beats [[BM25]] on an e-commerce catalog by only +7.2% nDCG@10. Fine-tuned on catalog data, the same architecture reaches **+27.5%** — nearly four times the improvement, from domain adaptation alone, with no architecture change.

## The Fix Has Its Own Cliff

Domain fine-tuning does not produce a general model that also happens to be good at your domain — it produces a domain model, and Damiba's series is explicit about the cost. Tested across catalogs, the ESCI-fine-tuned SPLADE model actually *loses* to the off-the-shelf baseline on Home Depot data (0.384 vs 0.391 nDCG@10) — fine-tuning on one retailer's catalog does not automatically transfer to a neighboring one. On general web queries (MS MARCO), the fine-tuned model falls well below BM25: catastrophic forgetting, with Amazon-specific vocabulary overwriting general language ability. Multi-domain training (blending several catalogs) trades peak in-domain performance for consistency across them, rather than escaping the tradeoff. The generalization cliff does not disappear when you fine-tune; it just moves — from "general model, your domain" to "your domain, someone else's domain."

## The Practical Response

- **Use public benchmarks to build a shortlist, not to decide.** [[Retrieval Benchmarks and Leaderboards]] and [[Model Selection and Fine-Tuning Evaluation]] both land on the same rule: shortlist on MTEB/BEIR, pick on your own judgments.
- **Treat an open-vs-private leaderboard drop as diagnostic**, where one is available — it is stronger evidence of overfitting than absolute position.
- **If you have domain data, fine-tune** — the recovery is large and comes from hard negatives, not architecture changes.
- **Know what you're trading away.** A model fine-tuned for one domain should be expected to lose generality elsewhere; choose single-domain vs multi-domain training based on whether you serve one catalog or several.

---

## Related

- [[Retrieval Benchmarks and Leaderboards]] — the wider benchmark landscape and how each one attacks contamination
- [[Model Selection and Fine-Tuning Evaluation]] — how to evaluate on your own data instead of trusting a leaderboard
- [[Embedding Models Compared]] — the candidates this cliff applies to
- [[BRIGHT]] · [[RTEB]] · [[BEIR]] · [[MTEB]] — the benchmarks behind each claim above
- [[Fine-Tuning Text Embeddings For Domain-Specific Search]] · [[Fine-Tuning Sparse Embeddings for E-Commerce Search]] — the fix, with numbers
