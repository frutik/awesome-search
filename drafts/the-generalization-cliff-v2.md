# The Generalization Cliff

When a general-purpose embedding model tops a public leaderboard, that tells you very little about how it will do on your data. The gap between "good on MTEB" and "good on your queries" is not a gentle slope, it is a cliff. Below I show how far models fall (BRIGHT), why it happens (benchmark contamination), and what fixes it (domain fine-tuning, which has a cliff of its own).

## The collapse in one number

[[BRIGHT]] shows it most clearly. A model that scores 59.0 nDCG@10 on [[MTEB]] scores 18.3 on BRIGHT. BRIGHT's queries come from StackExchange, LeetCode, and math competitions, and the relevant document connects to the query only through inference, such as a shared theorem or an analogous algorithm. The two rarely share vocabulary or sit close together semantically. Dense [[Embeddings|embedding]] models, whatever else they do well, don't reason about relevance in several steps. Semantic similarity is all a [[Bi-Encoder]] can express, and once the link between query and document stops being lexical or topical, similarity is a poor stand-in for "this document helps answer this question."

## Ordinary queries hit it too

BRIGHT is the extreme case. The same drop appears on everyday in-domain retrieval where no reasoning is needed. [[Model Selection and Fine-Tuning Evaluation]] makes the point that [[MTEB]] and [[BEIR]] measure general-domain performance and are heavily optimized against, so a model's leaderboard position reflects how well it fits the benchmark about as much as how good it is. The board leader routinely loses to a mid-ranked model on in-domain data. A model can be excellent at general text similarity and mediocre on your catalog or your legal corpus at the same time; those are different skills, and public benchmarks don't separate them.

## Why: contamination, and an incentive that moves

[[RTEB]] names the mechanism: public benchmarks reward memorization. When the corpus, queries, and labels are all public, they leak into training data, and a model that has effectively seen the test posts a score that falls apart on new data. RTEB splits its datasets into an open half and a private half held by the maintainers, which makes the gap measurable. If a model scores well on the open datasets and drops sharply on the private ones, it has been trained on the test.

RTEB's governance history is the more interesting part. In 2026 the private column was temporarily removed after concerns that vendors with access to the private data had a structural advantage. Keeping a test set secret moves the incentive problem somewhere else. Someone has to hold the secret, and if that party also competes, the benchmark trades contamination for a conflict of interest.

[[BEIR]] made an earlier version of this critique by training models on one corpus (usually [[MS MARCO]]) and evaluating them zero-shot on eighteen unrelated ones. Its most durable finding, that [[BM25]] is a stubbornly strong zero-shot baseline, fits the same picture: BM25 learned nothing from training data, so it has no learned generalization to lose.

## Fine-tuning closes most of the gap

The direct response is domain [[Embedding Fine-tuning|fine-tuning]], and two worked examples show how much it recovers.

[[Fine-Tuning Text Embeddings For Domain-Specific Search|Shaw Talebi's tutorial]] uses a medical Q&A task. Asked "What causes hypertension?", a general `all-MiniLM-L6-v2` model retrieves articles about blood pressure in general, which are similar in everyday English but not medically relevant, and misses the specialized connection from ACE inhibitors to the renin-angiotensin system. Fine-tuning on domain triplets with [[Hard Negative Mining|hard negatives]] closes much of that gap. The reported NDCG@10 gains are 12 to 18%, with diminishing returns past roughly 10,000 to 20,000 examples.

[[Fine-Tuning Sparse Embeddings for E-Commerce Search|Thierry Damiba's SPLADE series]] gives numbers for sparse retrieval. Off-the-shelf [[SPLADE]], trained on MS MARCO web search, beats [[BM25]] on an e-commerce catalog by only 7.2% nDCG@10. Fine-tuned on catalog data, the same architecture beats it by 27.5%, nearly four times the improvement, from domain adaptation alone and with no change to the architecture.

## Fine-tuning has a cliff of its own

What fine-tuning produces is a domain model, and Damiba's series is explicit about the cost. Tested on other catalogs, the SPLADE model fine-tuned on ESCI loses to the off-the-shelf baseline on Home Depot data (0.384 vs 0.391 nDCG@10), so training on one retailer's catalog doesn't automatically carry over to a neighboring one. On general web queries (MS MARCO) the fine-tuned model falls well below BM25. That is catastrophic forgetting: Amazon-specific vocabulary overwrote general language ability. Blending several catalogs in multi-domain training gives up some peak in-domain performance in exchange for consistency across them, so it picks a different point on the tradeoff instead of escaping it. After fine-tuning, the cliff sits between your domain and someone else's, where before it sat between general data and yours.

## What to do about it

[[Retrieval Benchmarks and Leaderboards]] and [[Model Selection and Fine-Tuning Evaluation]] arrive at the same rule: use MTEB and BEIR to build a shortlist, and make the final pick on your own relevance judgments. Where a leaderboard reports both open and private scores, a drop between them is stronger evidence of overfitting than absolute position.

If you have domain data, fine-tune. The recovery is large, and it comes from hard negatives rather than from architecture changes. Expect the result to get worse outside that domain, and choose single-domain or multi-domain training depending on whether you serve one catalog or several.

## Related

- [[Retrieval Benchmarks and Leaderboards]]: the wider set of benchmarks and how each one deals with contamination
- [[Model Selection and Fine-Tuning Evaluation]]: how to evaluate on your own data instead of trusting a leaderboard
- [[Embedding Models Compared]]: the models this applies to
- [[BRIGHT]] · [[RTEB]] · [[BEIR]] · [[MTEB]]: the benchmarks behind each claim above
- [[Fine-Tuning Text Embeddings For Domain-Specific Search]] · [[Fine-Tuning Sparse Embeddings for E-Commerce Search]]: the fine-tuning results, with numbers
