---
type: topic
aliases: ["career in search", "breaking into search", "search engineer career", "learning search", "search learning path"]
tags: [topic, career, learning-path, hiring, search-team]
related_concepts:
  - "[[BM25]]"
  - "[[Precision and Recall]]"
  - "[[Learning to Rank]]"
  - "[[Search Evaluation]]"
  - "[[Judgment Lists]]"
  - "[[Query Understanding]]"
  - "[[Semantic Search]]"
  - "[[Hybrid Search]]"
  - "[[Search Team]]"
related_topics:
  - "[[Hiring for Search]]"
  - "[[Managing a Search Team]]"
  - "[[Search Consultancy]]"
  - "[[Books]]"
  - "[[Events and Conferences]]"
  - "[[Courses]]"
  - "[[Search Platforms]]"
  - "[[Relevance Program Setup]]"
  - "[[Economics of Search]]"
articles: []
people:
  - "[[Daniel Tunkelang]]"
  - "[[Doug Turnbull]]"
  - "[[Trey Grainger]]"
  - "[[Charlie Hull]]"
  - "[[Jo Kristian Bergum]]"
  - "[[James Rubinstein]]"
  - "[[Giovanni Fernandez-Kincade]]"
  - "[[Atita Arora]]"
  - "[[Eugene Yan]]"
  - "[[Nikhil Dandekar]]"
companies:
  - "[[OpenSource Connections]]"
  - "[[Sease]]"
  - "[[Elastic]]"
created: 2026-06-18
---

# How to Start a Career in Search

A self-directed learning path for breaking into search and information retrieval. Search is a specialized field — generic software or ML backgrounds get you partway, but the people who thrive learn the IR fundamentals, build an *evaluation mindset*, and follow the small, generous community that publishes openly.

This note is a curated entry point into the rest of the vault. Each step links to the deeper material.

---

## The Short Plan

1. **[Read the topics](#1-read-the-topics)** — start with practice-oriented guides, not theory
2. **[Move to the concepts](#2-move-to-the-concepts)** — learn the IR fundamentals that underpin everything
3. **[Follow the people and companies](#3-follow-people-and-companies)** — the field is small and publishes in the open
4. **[Read the books](#4-read-the-books)** — a handful of canonical texts, several free
5. **[Take a course](#5-take-a-course-even-a-free-one)** — even a free one builds structure
6. **[Attend the conferences](#6-attend-the-conferences)** — practitioner events are where you meet the community
7. **[Explore the tools](#7-explore-the-tools)** — get your hands dirty with real engines
8. **[Get active in the community](#8-get-active-in-the-community)** — don't just lurk; participate
9. **[Understand the roles](#roles-in-search)** — know which job you're actually aiming for

> The single trait every search hire is screened for is an **evaluation mindset**: the instinct to measure whether a change actually improved things. See [[Hiring for Search]]. Build this habit from day one and you are ahead of most candidates.

---

## 1. Read the Topics

The [[Awesome Search/Topics|Topics]] folder is the fastest on-ramp — these are "how to *do* something in search" guides written for practitioners. A suggested reading order:

- [[Search Problem Archetypes]] — recognize the recurring shapes of search problems
- [[E-commerce Search]] — the most common commercial application, and a great worked example
- [[Query Understanding in Practice]] — the pipeline that turns a raw query into intent
- [[Search Quality Assurance]] — how you know whether search is any good
- [[A-B Testing for Search]] — measuring change in production
- [[Relevance Program Setup]] — the methodology that ties it all together
- [[Search UX]] — search is a product problem, not only a technical one

Then branch into whatever vertical interests you: [[Enterprise Search]], [[Multilingual Search]], [[Conversational and Agentic Search]], [[Personalization in Search]].

---

## 2. Move to the Concepts

Once a topic raises a term you don't know, follow it into [[Awesome Search/Concepts|Concepts]]. Don't try to read all 130+ — learn this foundation first, in roughly this order:

**Retrieval & scoring**
- [[BM25]] — the lexical baseline you must understand cold
- [[Full-Text Search]] · [[Precision and Recall]] — the vocabulary of every interview
- [[Semantic Search]] · [[Dense Vector Retrieval]] · [[Embeddings]]
- [[Hybrid Search]] · [[Reciprocal Rank Fusion]] — how lexical and vector retrieval combine

**Ranking**
- [[Learning to Rank]] · [[LTR Feature Engineering]] · [[Reranking]]
- [[Position Bias]] · [[Click Signals]] — why naive use of clicks misleads

**Evaluation** (the part most candidates are weakest on)
- [[Search Evaluation]] · [[Judgment Lists]] · [[NDCG]] · [[MRR]] · [[MAP]]
- [[Implicit Judgments]] · [[LLM as Judge]]

**Query understanding**
- [[Query Understanding]] · [[Query Types]] · [[Search Intent]]
- [[Synonyms]] · [[Spelling Correction]] · [[Query Expansion]] · [[Zero Results]]

If you only memorize one thing for interviews: be able to explain [[BM25]], the difference in [[Precision and Recall]], and how you would *measure* whether a ranking change helped ([[NDCG]] + [[Judgment Lists]]).

---

## 3. Follow People and Companies

Search has a small, unusually open community. Following the right people gives you a free, continuous curriculum.

**Educators & writers to follow first**
- [[Daniel Tunkelang]] — canonical writing on relevance, query understanding, and search teams
- [[Doug Turnbull]] — *Relevant Search* author, relevance methodology, prolific blogger
- [[Trey Grainger]] — *AI-Powered Search* author, neural/semantic search
- [[Charlie Hull]] — vendor-neutral strategy, Haystack organizer, community builder
- [[Jo Kristian Bergum]] — deep, practical retrieval and ranking writing ([[Vespa]])
- [[James Rubinstein]] — search evaluation and metrics
- [[Giovanni Fernandez-Kincade]] · [[Atita Arora]] · [[Nikhil Dandekar]] · [[Eugene Yan]] — applied search & ML

See the full roster in [[Awesome Search/People|People]].

**Companies whose engineering blogs are worth tracking**
- Consultancies that publish openly: [[OpenSource Connections]], [[Sease]], [[The Search Juggler]]
- Platform vendors: [[Elastic]], [[Vespa]], [[Algolia]], [[Weaviate]], [[Qdrant]], [[Cohere]]
- End-user teams with strong case studies: [[Etsy]], [[Airbnb]], [[Uber]], [[Spotify]], [[Zalando]], [[Reddit]]

The [[Awesome Search/Case Studies|Case Studies]] are how these companies actually solved real problems — read them like field reports.

---

## 4. Read the Books

The full annotated list is in [[Books]]. To start:

- **Free, foundational:** *Introduction to Information Retrieval* (Manning, Raghavan, Schütze) — the standard text, free online
- **Most practical first read:** *Relevant Search* ([[Doug Turnbull]], Berryman) — mental models for relevance tuning
- **Modern / neural:** *AI-Powered Search* ([[Trey Grainger]] et al.) — semantic and neural search in practice

Read *Relevant Search* for intuition, *Introduction to IR* for rigor, *AI-Powered Search* for where the field is now.

---

## 5. Take a Course (Even a Free One)

A structured course gives you scaffolding the blog-and-book path lacks. Full annotated list: [[Courses]]. Strong options, many free:

- **Cheat at Search Essentials** ([[Doug Turnbull]]) — free, beginner-friendly intro to retrieval; the ideal first structured exposure. See [[Courses]]
- **AI-Powered Search: Modern Retrieval for Humans & Agents** ([[Trey Grainger]] & [[Doug Turnbull]]) — paid 4-week cohort, the applied next step; cohort version of the *AI-Powered Search* book
- **Stanford CS276 / CMU 11-642 Search Engines** — university IR course materials are freely available online
- **Coursera — *Text Retrieval and Search Engines*** (UIUC, ChengXiang Zhai) — auditable for free
- **OpenSource Connections — *Think Like a Relevance Engineer (TLRE)*** — the practitioner-standard relevance training ([[OpenSource Connections]])
- **Vector-DB academies** — free, hands-on intros from [[Weaviate]], [[Qdrant]], and [[Pinecone]]
- **DeepLearning.AI short courses** — short, free modules on embeddings, RAG, and retrieval

Pair any course with a small project (see [next section](#7-explore-the-tools)) — the course teaches concepts, the project builds the evaluation instinct interviewers test for.

---

## 6. Attend the Conferences

Conferences are where you meet the community and see the current state of the art. Full guide: [[Events and Conferences]].

**Best for someone starting out (practitioner-focused):**
- **Haystack** — the open-source search relevance conference; the most welcoming entry point
- **Berlin Buzzwords** — strong open-source search engineering track
- **MICES** — dedicated e-commerce search
- **Activate** · **Elastic{ON}** — vendor ecosystems

**Academic (for depth / research roles):** SIGIR, ECIR, TREC, WSDM, CIKM.

You don't have to travel — many talks are posted free on YouTube, and there are active Slack/meetup communities (London Search & AI Meetup, Relevance Slack). Watching last year's Haystack talks is a free crash course.

---

## 7. Explore the Tools

Theory sticks only when you build. Stand up a real engine, index a dataset, write some queries, and — crucially — measure your results. The [[Awesome Search/Tools|Tools]] folder covers the landscape; compare options in [[Search Platforms]].

**Get hands-on with:**
- A search engine: [[Elasticsearch]] or [[OpenSearch]] (compare in [[Elasticsearch vs OpenSearch]]); or [[Vespa]] for ranking depth
- A vector database: [[Qdrant Vector DB]], [[Weaviate Vector DB]], or [[Milvus Vector DB]]
- Evaluation tooling: [[Quepid]] — build [[Judgment Lists]] and measure relevance like the pros do
- Query tuning: [[Querqy]] for rules-based query rewriting
- LTR: [[RankLib]] with [[XGBoost]] / [[LightGBM]] / [[CatBoost]] models
- Even your existing database: [[Search using PostgreSQL]] with [[pgvector]] is a low-friction starting point

**A good first project:** index a public dataset (products, Wikipedia, papers), build a small [[Judgment Lists|judgment list]], measure [[NDCG]] for a baseline [[BM25]] query, then try to beat it with synonyms, then with [[Hybrid Search]]. That single project demonstrates retrieval, ranking, *and* evaluation — exactly the [[Hiring for Search|take-home relevance task]] many teams use to hire.

---

## 8. Get Active in the Community

Following people (step 3) is passive; *participating* is what actually builds a network, surfaces job leads, and accelerates learning. Search is small and welcoming enough that newcomers who ask good questions get noticed.

### Relevance Slack — the central hub
The **Relevance Slack** community, created and run by [[OpenSource Connections]], is the single best place to be active. Practitioners share tips across Solr, Elasticsearch, [[Learning to Rank]], vector search, and product management — and post jobs.

🔗 Join: https://opensourceconnections.com/slack

Notable channels:
- `#jobs` — search-specific job opportunities (a real hiring channel, not a board)
- `#jobs-eu` — Europe-focused search roles
- `#blogs-papers-books` — curated resource sharing
- `#es-learn-to-rank` — [[Elasticsearch Learning to Rank]] discussion
- `#quepid` — questions about [[Quepid]]

**Where to actually find a search job:** the `#jobs` and `#jobs-eu` channels in Relevance Slack are the field's de-facto job board — niche search/relevance roles get posted here that never reach LinkedIn. Lurk them, but also be active in the topic channels first: many openings are filled by referral from people who've seen you ask good questions.

**Norms:** vendor pitches are discouraged; the tone is polite and supportive, oriented toward weighing the pros and cons of technical options. Background: ["Building the Search Community with Relevance Slack"](https://opensourceconnections.com/blog/2021/07/06/building-the-search-community-with-relevance-slack/).

### Ways to actually participate
- **Answer questions** in Slack on things you've just learned — teaching cements knowledge and builds reputation
- **Write in public** — blog your first-project results ([from step 7](#7-explore-the-tools)); a single honest "I measured [[BM25]] vs [[Hybrid Search]] and here's what happened" post is more credible than a résumé line
- **Show up at meetups** — London Search & AI Meetup and local equivalents; talks from [[Events and Conferences]] often have associated communities
- **Contribute to open source** — issues and docs for [[Quepid]], [[Querqy]], [[Elasticsearch]], or a vector DB are low-barrier entry points
- **Go to [conferences](#6-attend-the-conferences)** and talk to people — [[Charlie Hull]], [[Doug Turnbull]] and other organizers are notably approachable

> Building in public + being genuinely helpful in Slack is, for many people, how the first search job actually arrives — through the `#jobs` channel or a referral, not a cold application.

---

## Roles in Search

Know which job you are aiming for — the skills overlap but the emphasis differs. Full breakdown, skills, and "what separates good from great" in [[Hiring for Search]].

| Role | Owns | Core skills to build | Best starting background |
|---|---|---|---|
| **Relevance / Search Engineer** | The bridge from IR to production | [[BM25]], [[Learning to Rank]], [[Query Understanding]], engine internals, [[Search Evaluation]] | Backend / software engineering |
| **ML Engineer (Ranking/Retrieval)** | The model layer | [[LTR Feature Engineering]], embeddings, [[Reranking]], vector search, [[Click Models]] | ML / data engineering |
| **Search Data Scientist** | The measurement layer | [[A-B Testing for Search]], [[Position Bias]], query-log analysis | Statistics / data science |
| **Search Product Manager** | Strategy & roadmap | Technical literacy, measurement orientation, stakeholder translation | Technical PM |
| **Relevance Annotator / Judgment Analyst** | [[Judgment Lists]] & eval ground truth | Calibration, annotation guidelines, domain knowledge | Domain expertise; a common entry point |
| **Search Consultant** | Diagnosis & advisory across clients | All of the above + communication | Experienced practitioners — see [[Search Consultancy]] |

**Easiest entry points** for someone breaking in: starting as a backend engineer on a team that owns search, a judgment/annotation role that grows into relevance engineering, or an ML role adjacent to ranking. The annotator and data-science paths are often underrated doors into the field.

---

## Related

- [[Hiring for Search]] — what teams screen for (read this to reverse-engineer how to prepare)
- [[Managing a Search Team]] — where these roles sit once you're in
- [[Search Consultancy]] — the independent / advisory path
- [[Economics of Search]] — why search teams exist and how they're justified
- [[Books]] · [[Courses]] · [[Events and Conferences]] · [[Search Platforms]] — the companion reference lists
