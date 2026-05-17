---
title: "Paper page - Beyond Semantic Similarity: Rethinking Retrieval for Agentic Search via Direct Corpus Interaction"
source: "https://huggingface.co/papers/2605.05242"
author:
published: 2026-05-08
created: 2026-05-16
description: "Join the discussion on this paper page"
tags:
  - "clippings"
---
arxiv:2605.05242

## Beyond Semantic Similarity: Rethinking Retrieval for Agentic Search via Direct Corpus Interaction

[#2 Paper of the day](https://huggingface.co/papers/date/2026-05-08)[TIGER-Lab](https://huggingface.co/TIGER-Lab)

Authors:

## Abstract

Direct corpus interaction enables more effective agentic search by allowing agents to query raw text directly, outperforming traditional retrieval methods in complex tasks.

AI-generated summary

Modern [retrieval systems](https://huggingface.co/papers?q=retrieval%20systems), whether lexical or semantic, expose a corpus through a fixed similarity interface that compresses access into a single top-k retrieval step before reasoning. This abstraction is efficient, but for [agentic search](https://huggingface.co/papers?q=agentic%20search), it becomes a bottleneck: exact lexical constraints, sparse clue conjunctions, local context checks, and multi-step hypothesis refinement are difficult to implement by calling a conventional off-the-shelf retriever, and evidence filtered out early cannot be recovered by stronger downstream reasoning. Agentic tasks further exacerbate this limitation because they require agents to orchestrate multiple steps, including discovering intermediate entities, combining weak clues, and revising the plan after observing partial evidence. To tackle the limitation, we study [direct corpus interaction](https://huggingface.co/papers?q=direct%20corpus%20interaction) (DCI), where an agent searches the raw corpus directly with general-purpose [terminal tools](https://huggingface.co/papers?q=terminal%20tools) (e.g., grep, file reads, shell commands, lightweight scripts), without any embedding model, vector index, or retrieval API. This approach requires no offline indexing and adapts naturally to evolving local corpora. Across [IR benchmarks](https://huggingface.co/papers?q=IR%20benchmarks) and end-to-end [agentic search](https://huggingface.co/papers?q=agentic%20search) tasks, this simple setup substantially outperforms strong sparse, dense, and [reranking](https://huggingface.co/papers?q=reranking) baselines on several BRIGHT and [BEIR datasets](https://huggingface.co/papers?q=BEIR%20datasets), and attains strong accuracy on [BrowseComp-Plus](https://huggingface.co/papers?q=BrowseComp-Plus) and [multi-hop QA](https://huggingface.co/papers?q=multi-hop%20QA) without relying on any conventional semantic retriever. Our results indicate that as language agents become stronger, retrieval quality depends not only on reasoning ability but also on the resolution of the interface through which the model interacts with the corpus, with which DCI opens a broader interface-design space for [agentic search](https://huggingface.co/papers?q=agentic%20search).

### Community

[ZhuofengLi](https://huggingface.co/ZhuofengLi)

Paper author Paper submitter [8 days ago](#69fdc99302e7eee8a3b6bc2a)

🔥 **The best retriever for agentic search … is no retriever. Introducing Direct Corpus Interaction (DCI)**.

🚀 We replaced the entire agentic search pipeline — embedding model, vector index, top-k retrieval — with only `grep` and `bash`. 🔧

💡The Magic:  
The agent **searches the raw corpus directly** — `grep`, `find`, `bash`, shell pipelines — exactly like a coding agent navigating a codebase. No preprocess. No embedding model. No vector index. No offline indexing.

📊The Results:  
DCI outperforms top baselines across 13 benchmarks, with average gains of:  
🔍 Agentic Search (BrowseComp-Plus): **+11.0%**  
🧠 Multi-hop QA: **+30.7%**  
📈 IR Ranking: **+21.5%**

💡 Insights:  
Beyond accuracy, we conduct a series of controlled ablation studies to pinpoint the sources of DCI’s gains in Section 4. Specifically, we examine trajectory-level search patterns (RQ2), evidence utilization (RQ3), corpus scale (RQ4), context management (RQ5), and tool usage (RQ6).

Try it yourself!  
👨💻 GitHub: [https://github.com/DCI-Agent/DCI-Agent-Lite](https://github.com/DCI-Agent/DCI-Agent-Lite)  
🚀 Demo: [https://huggingface.co/spaces/DCI-Agent/demo](https://huggingface.co/spaces/DCI-Agent/demo)  
🔎 Eval logs: [https://huggingface.co/datasets/DCI-Agent/eval-logs](https://huggingface.co/datasets/DCI-Agent/eval-logs)

[avahal](https://huggingface.co/avahal)

[8 days ago](#69fdd41aba2f0e62a57df482)

Interesting breakdown of this paper on arXivLens: [https://arxivlens.com/PaperView/Details/beyond-semantic-similarity-rethinking-retrieval-for-agentic-search-via-direct-corpus-interaction-2755-8403a410](https://arxivlens.com/PaperView/Details/beyond-semantic-similarity-rethinking-retrieval-for-agentic-search-via-direct-corpus-interaction-2755-8403a410)  
Covers the executive summary, detailed methodology, and practical applications.

[librarian-bot](https://huggingface.co/librarian-bot)

[8 days ago](#69fe910d4335dfcef1d593ab)

This is an automated message from the [Librarian Bot](https://huggingface.co/librarian-bots). I found the following papers similar to this paper.

The following papers were recommended by the Semantic Scholar API

- [A Reference Architecture for Agentic Hybrid Retrieval in Dataset Search](https://huggingface.co/papers/2604.16394) (2026)
- [Coding Agents are Effective Long-Context Processors](https://huggingface.co/papers/2603.20432) (2026)
- [Reproducing Complex Set-Compositional Information Retrieval](https://huggingface.co/papers/2605.03824) (2026)
- [FitText: Evolving Agent Tool Ecologies via Memetic Retrieval](https://huggingface.co/papers/2605.02411) (2026)
- [TaSR-RAG: Taxonomy-guided Structured Reasoning for Retrieval-Augmented Generation](https://huggingface.co/papers/2603.09341) (2026)
- [CoSearch: Joint Training of Reasoning and Document Ranking via Reinforcement Learning for Agentic Search](https://huggingface.co/papers/2604.17555) (2026)
- [Transforming External Knowledge into Triplets for Enhanced Retrieval in RAG of LLMs](https://huggingface.co/papers/2604.12610) (2026)

Please give a thumbs up to this comment if you found it helpful!

If you want recommendations for any Paper on Hugging Face checkout [this](https://huggingface.co/spaces/librarian-bots/recommend_similar_papers) Space

You can directly ask Librarian Bot for paper recommendations by tagging it in a comment: `@librarian-bot  recommend`

## Models citing this paper 0

No model linking this paper

Cite arxiv.org/abs/2605.05242 in a model README.md to link it from this page.

## Datasets citing this paper 0

No dataset linking this paper

Cite arxiv.org/abs/2605.05242 in a dataset README.md to link it from this page.