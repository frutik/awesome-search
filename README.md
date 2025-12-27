# Awesome Search

<p align="center"> <a href="https://savelife.in.ua/en/about-foundation-en/" target="_blank">Support Ukrainian fight for the freedom</a> 
  
[RUSSIAN WARSHIP, GO F*CK YOURSELF](https://en.wikipedia.org/wiki/Russian_warship,_go_fuck_yourself!)

I've been building e-commerce search applications for more than ten years. Below is a list of some publications, conferences, and books that have inspired me, grouped by topic. If an item fits into multiple topics, it appears in multiple sections.

:star: Star us on GitHub — it helps!

Also check my other collections [awesome e-commerce](https://github.com/frutik/awesome-e-commerce), [awesome knowledge graphs](https://github.com/frutik/awesome-knowledge-graphs), [awesome cloud apps](https://github.com/frutik/awesome-cloud-apps) 

*Topics*

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Unsorted](#unsorted)
- [General, fun, philosophy](#general-fun-philosophy)
- [Types of search](#types-of-search)
  - [Classic/Lexical Search](#classiclexical-search)
  - [Vectors/Semantic search](#vectorssemantic-search)
    - [Symmetric and Asymmetric semantic search](#symmetric-and-asymmetric-semantic-search)
    - [Embeddings](#embeddings)
    - [Vector retrieval](#vector-retrieval)
    - [Handling high-dimension embeddings](#handling-high-dimension-embeddings)
    - [Finetuning models](#finetuning-models)
  - [Hybrid search](#hybrid-search)
    - [Reciprocal rank fusion (RRF)](#reciprocal-rank-fusion-rrf)
    - [Linear Score Combination](#linear-score-combination)
  - [Multimodal search](#multimodal-search)
    - [Multimodality Problems](#multimodality-problems)
- [Search Quality Assurance](#search-quality-assurance)
  - [How to select queries](#how-to-select-queries)
    - [Random sampling](#random-sampling)
    - [Stratified sampling](#stratified-sampling)
    - [Probability-proportional-to-size sampling](#probability-proportional-to-size-sampling)
  - [Metrics](#metrics)
    - [Focused on ranking quality](#focused-on-ranking-quality)
    - [Focused on diversity of results](#focused-on-diversity-of-results)
    - [Focused on interactions](#focused-on-interactions)
  - [Offline measuring](#offline-measuring)
    - [Judgements](#judgements)
  - [Online measuring](#online-measuring)
- [Areas of application](#areas-of-application)
  - [Enterprise search](#enterprise-search)
  - [e-Commerce search](#e-commerce-search)
  - [Conversational search](#conversational-search)
- [Search Results](#search-results)
  - [Retrieval](#retrieval)
    - [Relevance](#relevance)
  - [Ranking](#ranking)
    - [Multi-stage ranking](#multi-stage-ranking)
    - [Learning to Rank](#learning-to-rank)
  - [Bias](#bias)
  - [Diversification](#diversification)
    - [MMR](#mmr)
  - [Personalisation](#personalisation)
  - [Zero search results](#zero-search-results)
- [Search UX](#search-ux)
  - [Baymard Institute](#baymard-institute)
  - [Nielsen Norman Group](#nielsen-norman-group)
  - [Enterprise Knowledge LLC](#enterprise-knowledge-llc)
  - [Facets](#facets)
    - [Accidental Taxonomist](#accidental-taxonomist)
  - [Other](#other)
- [Spelling correction](#spelling-correction)
- [Synonyms](#synonyms)
- [Stopwords](#stopwords)
- [Suggestions](#suggestions)
- [Graphs/Taxonomies/Knowledge Graph](#graphstaxonomiesknowledge-graph)
  - [Integrating Search and Knowledge Graphs (by Enterprise Knowledge)](#integrating-search-and-knowledge-graphs-by-enterprise-knowledge)
- [Query expansion](#query-expansion)
- [Query understanding](#query-understanding)
  - [Search Intent](#search-intent)
  - [Query segmentation](#query-segmentation)
- [Algorithms](#algorithms)
  - [BERT](#bert)
  - [ColBERT](#colbert)
  - [Collocations, common phrases](#collocations-common-phrases)
  - [Other Algorithms](#other-algorithms)
    - [Hashing](#hashing)
    - [Sorting by average ratings](#sorting-by-average-ratings)
    - [Keywords extraction](#keywords-extraction)
- [Tracking, profiling, GDPR, Analysis](#tracking-profiling-gdpr-analysis)
  - [Tools, platforms, helpers for search tracking](#tools-platforms-helpers-for-search-tracking)
  - [Resources](#resources)
- [Experiments](#experiments)
  - [A/B testing, MABs](#ab-testing-mabs)
- [Testing, metrics, KPIs](#testing-metrics-kpis)
  - [KPIs](#kpis)
  - [Evaluating Search (by Daniel Tunkelang)](#evaluating-search-by-daniel-tunkelang)
  - [Measuring Search (by James Rubinstein)](#measuring-search-by-james-rubinstein)
  - [Three Pillars of Search Relevancy (by Andreas Wagner)](#three-pillars-of-search-relevancy-by-andreas-wagner)
- [Architecture](#architecture)
- [Education and networking](#education-and-networking)
  - [Conferences](#conferences)
  - [Trainings and courses](#trainings-and-courses)
  - [Books](#books)
  - [Blogs and Portals](#blogs-and-portals)
  - [Papers](#papers)
- [Management, Search Team](#management-search-team)
  - [Job Interviews](#job-interviews)
  - [Engineering](#engineering)
- [Blogposts series](#blogposts-series)
  - [Search Optimization 101 (by Charlie Hull)](#search-optimization-101-by-charlie-hull)
  - [Query Understanding (by Daniel Tunkelang)](#query-understanding-by-daniel-tunkelang)
  - [Grid Dynamics](#grid-dynamics)
  - [Considering Search: Search Topics (by Derek Sisson)](#considering-search-search-topics-by-derek-sisson)
- [Industry players](#industry-players)
  - [Personalies and influencers](#personalies-and-influencers)
  - [Search Engines](#search-engines)
  - [Products and services](#products-and-services)
  - [Consulting companies](#consulting-companies)
- [Case studies](#case-studies)
  - [General search](#general-search)
  - [E-commerce](#e-commerce)
  - [Multisided markets](#multisided-markets)
- [Videos](#videos)
  - [Channels](#channels)
  - [Featured](#featured)
- [Datasets](#datasets)
- [Tools](#tools)
  - [Spacy](#spacy)
  - [Word2Vec](#word2vec)
  - [Libs](#libs)
  - [Other](#other-1)
- [Other awesome stuff](#other-awesome-stuff)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Unsorted

- [sandbox Jun 2021](https://github.com/frutik/awesome-search/issues/19)
- [sandbox May 2021](https://github.com/frutik/awesome-search/issues/18)
- [sandbox April 2021](https://github.com/frutik/awesome-search/issues/17)
- [sandbox Dec 2020](https://github.com/frutik/awesome-search/issues/10)
- [sandbox Jan 2020](https://github.com/frutik/awesome-search/issues/1)

## General, fun, philosophy

* [Falsehoods Programmers Believe About Search](https://opensourceconnections.com/blog/2019/05/29/falsehoods-programmers-believe-about-search/)
* [Ethical Search: Designing an irresistible journey with a positive impact](https://medium.com/empathyco/fooddiscovery-2-ethical-search-designing-an-irresistible-journey-with-a-positive-impact-cc921c07a5a8)
* [On Semantic Search](https://medium.com/modern-nlp/semantic-search-fuck-yeah-e371c0f639d)
* [Feedback debt: what the segway teaches search teams](https://opensourceconnections.com/blog/2020/03/19/feedback-debt/)
* [Supporting the Searcher’s Journey: When and How](https://medium.com/@dtunkelang/supporting-the-searchers-journey-when-and-how-568e9b68fe02)
* [Shopping is Hard, Let’s go Searching!](https://medium.com/@dtunkelang/shopping-is-hard-lets-go-searching-f61f3d5764d3)
* [An Introduction to Search Quality](https://opensourceconnections.com/blog/2018/11/19/an-introduction-to-search-quality/)
* [On-Site Search Design Patterns for E-Commerce: Schema Structure, Data Driven Ranking & More](https://project-a.github.io/on-site-search-design-patterns-for-e-commerce/)
* [In Search of Recall](https://www.linkedin.com/pulse/search-recall-daniel-tunkelang/)
* [Balance Your Search Budget!](https://www.linkedin.com/pulse/balance-your-search-budget-daniel-tunkelang/)

## Types of search

* [Evolution of Search Technology: A Look Ahead](https://medium.com/@Ratnaparkhi/how-the-search-technology-is-evolving-88607f5efb9e)

### Classic/Lexical Search

* Etsy. [Targeting Broad Queries in Search](https://codeascraft.com/2015/07/29/targeting-broad-queries-in-search/)
* [How Etsy Uses Thermodynamics to Help You Search for “Geeky”](https://codeascraft.com/2015/08/31/how-etsy-uses-thermodynamics-to-help-you-search-for-geeky/)
* [Broad and Ambiguous Search Queries](https://medium.com/@dtunkelang/broad-and-ambiguous-search-queries-1bbbe417dcc)
* [Deconstructing E-Commerce Search: The 12 Query Types](https://baymard.com/blog/ecommerce-search-query-types)

### Vectors/Semantic search

* [Migrating to Elasticsearch with dense vector for Carousell Spotlight search engine](https://medium.com/carousell-insider/migrating-to-elasticsearch-with-dense-vector-for-carousell-spotlight-search-engine-e328b16155fc)
* [From zero to semantic search embedding model](https://blog.metarank.ai/from-zero-to-semantic-search-embedding-model-592e16d94b61)
* [Guidelines to choose an index](https://github.com/facebookresearch/faiss/wiki/Guidelines-to-choose-an-index)
* [Pinecone Series](#pinecone-series)
  * [Nearest Neighbor Indexes for Similarity Search](https://www.pinecone.io/learn/series/faiss/vector-indexes/)
  * [The Missing WHERE Clause in Vector Search](https://www.pinecone.io/learn/vector-search-filtering/)
* [Innovating Search Experience with Amazon OpenSearch and Amazon Bedrock](https://bigdataboutique.com/blog/innovating-search-experience-with-amazon-opensearch-and-amazon-bedrock-d045bc)

#### Symmetric and Asymmetric semantic search

  * [Symmetric vs. Asymmetric Semantic Search](https://www.sbert.net/examples/applications/semantic-search/README.html#symmetric-vs-asymmetric-semantic-search)

#### Embeddings
##### Types

* [Bi-encoder vs Cross encoder?When to use which one?](https://medium.com/@sujathamudadla1213/bi-encoder-vs-cross-encoder-when-to-use-which-one-4a20edbe6d37)
* [What is ColBERT and Late Interaction and Why They Matter in Search?](https://jina.ai/news/what-is-colbert-and-late-interaction-and-why-they-matter-in-search/)



#### Vector retrieval

* [Choosing the best model for semantic search](https://www.meilisearch.com/blog/choosing-the-best-model-for-semantic-search)

##### Query/Document tokens interaction

###### No interactions - Two towers / Bi-encoders

###### Early interactions - Cross-encoders

###### Late interactions - ColBERT

- [Announcing the Vespa ColBERT embedder](https://blog.vespa.ai/announcing-colbert-embedder-in-vespa/)
- [What is ColBERT and Late Interaction and Why They Matter in Search?](https://jina.ai/news/what-is-colbert-and-late-interaction-and-why-they-matter-in-search/)

##### Dense Vectors

###### Size of input and Chunking

- [Chunking Strategies for LLM Applications](https://www.pinecone.io/learn/chunking-strategies/)
- [Evaluating the Ideal Chunk Size for a RAG System using LlamaIndex](https://blog.llamaindex.ai/evaluating-the-ideal-chunk-size-for-a-rag-system-using-llamaindex-6207e5d3fec5)
- [How to Chunk Text Data — A Comparative Analysis](https://towardsdatascience.com/how-to-chunk-text-data-a-comparative-analysis-3858c4a0997a)

####### Positional chunking

####### Semantic chunking

####### Hypothetical Document Embeddings

* [HyDE](https://docs.haystack.deepset.ai/docs/hypothetical-document-embeddings-hyde)

###### Matryoshka embeddings

* [Matryoshka embeddings: faster OpenAI vector search using Adaptive Retrieval](https://supabase.com/blog/matryoshka-embeddings)
* [Introduction to Matryoshka Embedding Models](https://huggingface.co/blog/matryoshka)
* [Matryoshka representations. A guide to faster semantic search](https://ujjwalm29.medium.com/matryoshka-representation-learning-a-guide-to-faster-semantic-search-1c9025543530)

###### Context-aware embeddings

* [Improve your RAG applications by moving to Task-aware Embeddings](https://medium.com/@gal.peretz/improve-your-rag-applications-by-moving-to-task-aware-embeddings-09ebee62616f)
* [How Context-Aware Embeddings Are Transforming Enterprise Search](https://medium.com/@sonakshi.sp/smarter-knowledge-retrieval-how-context-aware-embeddings-are-transforming-enterprise-search-802c29c4b9b5)

##### Sparse Vectors

###### SPLADE

* [Hybrid Search: SPLADE (Sparse Encoder)](https://medium.com/@sowmiyajaganathan/hybrid-search-splade-sparse-encoder-neural-retrieval-models-d092e5f46913)
* [SPLADE for Sparse Vector Search Explained](https://www.pinecone.io/learn/splade/)
* [Improving information retrieval in the Elastic Stack. Introducing Elastic Learned Sparse Encoder, our new retrieval model](https://www.elastic.co/search-labs/blog/elastic-learned-sparse-encoder-elser-retrieval-performance)
* [No tracking until you click to share
SPLADE – a sparse bi-encoder BERT-based model achieves effective and efficient first-stage ranking](https://europe.naverlabs.com/blog/splade-a-sparse-bi-encoder-bert-based-model-achieves-effective-and-efficient-first-stage-ranking/)



#### Handling high-dimension embeddings

##### Dimensionality reduction

###### PCA

###### t-SNE

##### Quantization

###### Scalar quantization

###### Binary quantization

###### Product quantization

###### Rotational quantization

#### Finetuning models

* [Fine-Tuning Text Embeddings For Domain-Specific Search](https://shawhin.medium.com/fine-tuning-text-embeddings-f913b882b11c)
* [Fine-tuning Multimodal Embedding Models](https://medium.com/towards-data-science/fine-tuning-multimodal-embedding-models-bf007b1c5da5)
* [Is Fine-Tuning an Embedding Model Worth it?](https://pub.towardsai.net/is-fine-tuning-an-embedding-model-worth-it-9d5fe6875c32)


### Hybrid search

* [Hybrid search > sum of its parts?](https://pretalx.com/bbuzz22/talk/YEHRTE/)
* [On Hybrid Search](https://qdrant.tech/articles/hybrid-search/#)
* [Hybrid search with Re-ranking](https://medium.com/@sowmiyajaganathan/hybrid-search-with-re-ranking-ff120c8a426d)

#### Reciprocal rank fusion (RRF)

* [Hybrid search with Re-ranking](https://medium.com/@sowmiyajaganathan/hybrid-search-with-re-ranking-ff120c8a426d)
* [Reciprocal rank fusion](https://www.elastic.co/guide/en/elasticsearch/reference/current/rrf.html)

#### Linear Score Combination

* [Linear retriever](https://www.elastic.co/docs/reference/elasticsearch/rest-apis/retrievers/linear-retriever?utm_source=chatgpt.com)

### Multimodal search

* [Muves: Multimodal & multilingual vector search w/ Hardware Acceleration](https://www.youtube.com/watch?v=9OS8cMf2rwY)
* [Model Selection for Multimodal Search](https://docs.marqo.ai/2.6/Cookbook/model_selection/multimodal_search/#convnext-models)

#### Multimodality Problems

##### Modality Gap

- [Accept the modality gap: An exploration in the hyperbolic space](https://www.amazon.science/publications/accept-the-modality-gap-an-exploration-in-the-hyperbolic-space)

##### Contrastive Gap

- [Characterizing and Addressing the Contrastive Gap](https://arxiv.org/abs/2405.18570)

## Search Quality Assurance

### How to select queries

#### Random sampling

- [Simple random sample](https://en.wikipedia.org/wiki/Simple_random_sample)

#### Stratified sampling

- [Stratified sampling](https://en.wikipedia.org/wiki/Stratified_sampling)
- [The 8 Most Common Search Query Types ](https://baymard.com/blog/ecommerce-search-query-types)

#### Probability-proportional-to-size sampling

- [How to succeed with explicit relevance evaluation using Probability-Proportional-to-Size sampling](https://opensourceconnections.com/blog/2022/10/13/how-to-succeed-with-explicit-relevance-evaluation-using-probability-proportional-to-size-sampling/)

### Metrics

* [Choosing your search relevance evaluation metric](https://opensourceconnections.com/blog/2020/02/28/choosing-your-search-relevance-metric/)
* [Visualizing search metrics](https://nathanday.shinyapps.io/rank-algo-app/)
* [Choosing your search relevance evaluation metric](https://opensourceconnections.com/blog/2020/02/28/choosing-your-search-relevance-metric/)
* [Measuring Search: Metrics Matter](https://jamesrubinstein.medium.com/measuring-search-metrics-matter-de124c2f6f8c)

#### Focused on ranking quality

* [Discounted cumulative gain](https://en.wikipedia.org/wiki/Discounted_cumulative_gain)
* [Flavors of NDCG - normalized to what!?](https://softwaredoug.com/blog/2024/05/22/flavors-of-ndcg)
* [Mean reciprocal rank](https://en.wikipedia.org/wiki/Mean_reciprocal_rank)
* [P@k](https://en.wikipedia.org/wiki/Evaluation_measures_(information_retrieval)#Precision_at_K)
* [Demystifying nDCG and ERR](https://opensourceconnections.com/blog/2019/12/09/demystifying-ndcg-and-err/)
* https://en.wikipedia.org/wiki/Precision_and_recall
* https://en.wikipedia.org/wiki/F1_score

#### Focused on diversity of results

* [Diving into Diversity Metrics: Elevate Your Recommender Systems in a Snap!](https://shunya-vichaar.medium.com/diving-into-diversity-metrics-elevate-your-recommender-systems-in-a-snap-57637de380e1)

##### MMR

* [How to Calculate MMR?](https://www.analyticsvidhya.com/blog/2024/07/hit-rate-mrr-and-mmr-metrics/#h-how-to-calculate-mmr)
* [Maximal Marginal Relevance to Re-rank results in Unsupervised KeyPhrase Extraction](https://medium.com/tech-that-works/maximal-marginal-relevance-to-rerank-results-in-unsupervised-keyphrase-extraction-22d95015c7c5)

##### Average Pairwise Distance, APD

- edit distance
- semantic distance

##### Entropy

- [How to measure Diversity of Search Results](https://docs.google.com/presentation/d/1uz15rpxcUipvJMSfXc8_DpEnqtrH9PPx6UmF_dbdG-o/edit?slide=id.p#slide=id.p)

#### Focused on interactions

##### Zero results

##### Zero clicks



### Offline measuring

* [How to Implement a Normalized Discounted Cumulative Gain (NDCG) Ranking Quality Scorer in Quepid](https://opensourceconnections.com/blog/2018/02/26/ndcg-scorer-in-quepid/)
* [Compute Mean Reciprocal Rank (MRR) using Pandas](https://softwaredoug.com/blog/2021/04/21/compute-mrr-using-pandas.html)

#### Judgements

##### HUman judgements

* [What Is a Judgment List?](https://softwaredoug.com/blog/2021/02/21/what-is-a-judgment-list)
* [Evaluating Search: Using Human Judgments](https://dtunkelang.medium.com/evaluating-search-using-human-judgement-fbb2eeba37d9)
* [Measuring Search, A Human Approach](https://jamesrubinstein.medium.com/measuring-search-a-human-approach-acf54e2cf33d)
  
##### Implicite judgements

add something on clicks streams

##### Using LLM as judge

* [Improving retrieval with LLM-as-a-judge](https://blog.vespa.ai/improving-retrieval-with-llm-as-a-judge/)
* [LLMs-as-Judges: A Comprehensive Survey on LLM-based Evaluation Methods](https://arxiv.org/abs/2412.05579)

### Online measuring

* [How we Compute NDCG in Daraz. E-Commerce](https://medium.com/@hassam.chundrigar520/how-we-compute-ndcg-in-daraz-e-commerce-9a103b444c9f)

## Areas of application

### Enterprise search

* [GenAI Can Improve Enterprise Search, But Remains a Work In Progress](https://www.reworked.co/knowledge-findability/genai-can-improve-enterprise-search-but-remains-a-work-in-progress/)

### e-Commerce search

* [The influence of TF-IDF algorithms in eCommerce search](https://medium.com/empathyco/the-influence-of-tf-idf-algorithms-in-ecommerce-search-e7cb9ab8e662)

### Conversational search

* [Search as a Conversation](https://queryunderstanding.com/search-as-a-conversation-bafa7cd0c9a5)
* [Affordances for Conversational Search](https://dtunkelang.medium.com/affordances-for-conversational-search-2cc543eae83d)
* [Query Understanding and Chatbots](https://queryunderstanding.com/query-understanding-and-chatbots-5fa0c154f)

## Search Results

### Retrieval

#### Relevance

* [Humans Search for Things not for Strings](https://www.linkedin.com/pulse/humans-search-things-strings-andreas-wagner/)
* [What is a ‘Relevant’ Search Result?](https://opensourceconnections.com/blog/2019/12/11/what-is-a-relevant-search-result/)
* [How to Achieve Ecommerce Search Relevance](https://blog.searchhub.io/how-to-achieve-ecommerce-search-relevance?cn-reloaded=1&cn-reloaded=1)
* [Setting up a relevance evaluation program](https://medium.com/@jamesrubinstein/setting-up-a-relevance-evaluation-program-c955d32fba0e)

##### Relevance Algorithms

* [Understanding the BM25 full text search algorithm](https://emschwartz.me/understanding-the-bm25-full-text-search-algorithm/)
* Practical BM25: [How Shards Affect Relevance Scoring in Elasticsearch](https://www.elastic.co/blog/practical-bm25-part-1-how-shards-affect-relevance-scoring-in-elasticsearch), [The BM25 Algorithm and its Variables](https://www.elastic.co/blog/practical-bm25-part-2-the-bm25-algorithm-and-its-variables)
* [The influence of TF-IDF algorithms in eCommerce search](https://medium.com/empathyco/the-influence-of-tf-idf-algorithms-in-ecommerce-search-e7cb9ab8e662)
* [BM25 The Next Generation of Lucene Relevance](https://opensourceconnections.com/blog/2015/10/16/bm25-the-next-generation-of-lucene-relevation/)
* [Lucene Similarities (BM25, DFR, DFI, IB, LM) Explained](https://sematext.com/blog/search-relevance-solr-elasticsearch-similarity/)


### Ranking

#### Multi-stage ranking

* [Multi stage ranking](https://medium.com/better-ml/multi-stage-ranking-e0dacd81ac4)
* [Cross-Encoders, ColBERT, and LLM-Based Re-Rankers](https://medium.com/@aimichael/cross-encoders-colbert-and-llm-based-re-rankers-a-practical-guide-a23570d88548)

##### Reranking

* [Drowning in Documents: Consequences of Scaling Reranker Inference](https://arxiv.org/pdf/2411.11767)

#### Learning to Rank

* [How is search different than other machine learning problems?](https://opensourceconnections.com/blog/2017/08/03/search-as-machine-learning-prob/)
* [Reinforcement learning assisted search ranking](https://medium.com/sajari/reinforcement-learning-assisted-search-ranking-a594cdc36c29)
* [E-commerce Search Re-Ranking as a Reinforcement Learning Problem](https://towardsdatascience.com/e-commerce-search-re-ranking-as-a-reinforcement-learning-problem-a9d1561edbd0)
* [When to use a machine learned vs. score-based search ranker](https://towardsdatascience.com/when-to-use-a-machine-learned-vs-score-based-search-ranker-aa8762cd9aa9)
* [What is Learning To Rank?](https://opensourceconnections.com/blog/2017/02/24/what-is-learning-to-rank/)
* [Using AI and Machine Learning to Overcome Position Bias within Adobe Stock Search](https://medium.com/adobetech/evaluating-addressing-position-bias-in-adobe-stock-search-9807b11ee268)
* [Train and Test Sets Split for Evaluating Learning To Rank Models](https://sease.io/2022/07/how-to-split-your-dataset-into-train-and-test-sets-for-evaluating-learning-to-rank-models.html)
* [How LambdaMART works - optimizing product ranking goals](https://softwaredoug.com/blog/2021/11/28/how-lammbamart-works.html)

##### Click models for search

* [Click models](https://github.com/filipecasal/knowledge-repo/blob/master/click_models.md)
* [Click Modeling for eCommerce](https://tech.ebayinc.com/engineering/click-modeling-for-ecommerce/)
* [Using Behavioral Data to Improve Search](https://tech.ebayinc.com/engineering/using-behavioral-data-to-improve-search/)

### Bias
  
* [What is Presentation Bias in search?](https://softwaredoug.com/blog/2022/07/16/what-is-presentation-bias-in-search.html)
* [Dealing with Position Bias in Recommendations and Search](https://www.kdnuggets.com/2023/03/dealing-position-bias-recommendations-search.html)
  
### Diversification

* [Search Result Diversification using Causal Language Models](https://arxiv.org/pdf/2108.04026.pdf)
* [Learning to Diversify for E-commerce Search with Multi-Armed Bandit](http://ceur-ws.org/Vol-2410/paper18.pdf)
* [Search Quality for Discovery & Inspiration](https://blog.searchhub.io/three-pillars-of-search-quality-in-ecommerce-part-2-discovery-inspiration)
* [How to measure Diversity of Search Results](https://2021.berlinbuzzwords.de/session/how-measure-diversity-search-results)
* [Searching for Goldilocks](https://dtunkelang.medium.com/searching-for-goldilocks-12cb21c7d036)
* [Broad and Ambiguous Search Queries - Recognizing When Search Results Need Diversification](https://dtunkelang.medium.com/broad-and-ambiguous-search-queries-1bbbe417dcc)
* [Thoughts on Search Result Diversity](https://dtunkelang.medium.com/thoughts-on-search-result-diversity-1df54cb5bf4a)

#### MMR

* [How to Calculate MMR?](https://www.analyticsvidhya.com/blog/2024/07/hit-rate-mrr-and-mmr-metrics/#h-how-to-calculate-mmr)
* [Maximal Marginal Relevance to Re-rank results in Unsupervised KeyPhrase Extraction](https://medium.com/tech-that-works/maximal-marginal-relevance-to-rerank-results-in-unsupervised-keyphrase-extraction-22d95015c7c5)

### Personalisation

* [Patterns for Personalization in Recommendations and Search](https://eugeneyan.com/writing/patterns-for-personalization/)
* Daniel Tunkelang [Personalization](https://queryunderstanding.com/personalization-3ed715e05ef)
* Airbnb - [Real-time personalization in search](https://medium.com/airbnb-engineering/listing-embeddings-for-similar-listing-recommendations-and-real-time-personalization-in-search-601172f7603e)
* [98 personal data points that facebook uses to target ads to you](https://www.washingtonpost.com/news/the-intersect/wp/2016/08/19/98-personal-data-points-that-facebook-uses-to-target-ads-to-you/)
* [Architecture of real world recommendation systems](https://fennel.ai/blog/real-world-recommendation-system/)
* [Feature engineering for personalized search](https://fennel.ai/blog/feature-engineering-for-personalized-search/)

### Zero search results

* [Strategies for using alternative queries to mitigate zero results and their application to online marketplaces](https://haystackconf.com/files/slides/haystackEU2023/Jean_Ren%C3%A9_Strategies_for_using_alternative_queries_to_mitigate_zero_results.pdf)
* [Semantic Equivalence of e-Commerce Queries](https://dtunkelang.medium.com/semantic-equivalence-of-e-commerce-queries-78630e5fab5d)


## Search UX

### Baymard Institute

* [Deconstructing E-Commerce Search: The 12 Query Types](https://baymard.com/blog/ecommerce-search-query-types)
* [Autodirect or Guide Users to Matching Category](https://baymard.com/blog/autodirect-searches-matching-category-scopes)
* [13 Design Patterns for Autocomplete Suggestions (27% Get it Wrong)](https://baymard.com/blog/autocomplete-design)
* [E-Commerce Search Needs to Support Users’ Non-Product Search Queries (15% Don’t)](https://baymard.com/blog/support-non-product-search)
* [Search UX: 6 Essential Elements for ‘No Results’ Pages](https://baymard.com/blog/no-results-page)
* [Product Thumbnails Should Dynamically Update to Match the Variation Searched For (54% Don’t)](https://baymard.com/blog/color-and-variation-searches)
* [Faceted Sorting - A New Method for Sorting Search Results](https://baymard.com/blog/faceted-sorting)
* [The Current State of E-Commerce Search](https://baymard.com/blog/external-article-state-of-ecommerce-search)
* [E-Commerce Sites Need Multiple of These 5 ‘Search Scope’ Features](https://baymard.com/blog/search-scope)
* [E-Commerce Search Field Design and Its Implications](https://baymard.com/blog/search-field-design)
* [E-Commerce Sites Should Include Contextual Search Snippets (96% Get it Wrong)](https://baymard.com/blog/search-snippets)
* [E-Commerce Search Usability: Report & Benchmark](https://baymard.com/blog/ecommerce-search-report-and-benchmark)
* [Six ‘COVID-19’ Related E-Commerce UX Improvements to Make](https://baymard.com/blog/covid-19-ux-improvements)

### Nielsen Norman Group

* [The Love-at-First-Sight Gaze Pattern on Search-Results Pages](https://www.nngroup.com/articles/love-at-first-sight-pattern/)
* [Good Abandonment on Search Results Pages](https://www.nngroup.com/articles/good-abandonment/)
* [Complex Search-Results Pages Change Search Behavior: The Pinball Pattern](https://www.nngroup.com/articles/pinball-pattern-search-behavior/)
* [Site Search Suggestions](https://www.nngroup.com/articles/site-search-suggestions/)
* [Search-Log Analysis: The Most Overlooked Opportunity in Web UX Research](https://www.nngroup.com/articles/search-log-analysis/)
* [Scoped Search: Dangerous, but Sometimes Useful](https://www.nngroup.com/articles/scoped-search/)
* [3 Guidelines for Search Engine "No Results" Pages](https://www.nngroup.com/articles/search-no-results-serp/)

### Enterprise Knowledge LLC

* [Optimizing Your Search Experience: A Human-Centered Approach to Search Design](https://enterprise-knowledge.com/optimizing-your-search-experience-a-human-centered-approach-to-search-design/)

### Facets

* [Facets of Faceted Search](https://medium.com/@dtunkelang/facets-of-faceted-search-38c3e1043592)
* [Coffee, Coffee, Coffee!](https://medium.com/@dtunkelang/coffee-coffee-coffee-de3121b797d1)
* [Faceted Search](https://queryunderstanding.com/faceted-search-7d053cc4fada) (start here!)
* [How to implement faceted search the right way](https://medium.com/empathyco/how-to-implement-faceted-search-the-right-way-4bfba2bd2adc)
* [Metadata and Faceted Search](https://medium.com/searchblox/metadata-and-faceted-search-62ec6e4de353)
* [Metacrap: Putting the torch to seven straw-men of the meta-utopia](https://people.well.com/user/doctorow/metacrap.htm)
* [7 Filtering Implementations That Make Macy’s Best-in-Class](https://baymard.com/blog/macys-filtering-experience)
* [Facet Search: The Most Comprehensive Guide. Best Practices, Design Patterns, Hidden Caveats, And Workarounds](https://hybrismart.com/2019/02/13/facet-search-the-most-comprehensible-guide-best-practices-design-patterns/#d5)
* [Facets: Constraints or Preferences?](https://dtunkelang.medium.com/facets-constraints-or-preferences-8b8689903652)
* [Facets, But Which Ones?](https://dtunkelang.medium.com/facets-but-which-ones-6589416ed4db)


#### Accidental Taxonomist

* [How Many Facets Should a Taxonomy Have](http://accidental-taxonomist.blogspot.com/2020/07/how-many-facets-in-taxonomy.html)
* [When a Taxonomy Should not be Hierarchical](https://accidental-taxonomist.blogspot.com/2020/06/when-taxonomy-should-not-be-hierarchical.html)
* [Customizing Taxonomy Facets](http://accidental-taxonomist.blogspot.com/2020/10/customizing-taxonomy-facets.html)

### Other

* [Learning from Friction to Improve the Search Experience](https://medium.com/@dtunkelang/learning-from-friction-to-improve-the-search-experience-8937c71ec97a)
* [Why is it so hard to sort by price?](https://medium.com/@dtunkelang/why-is-it-so-hard-to-sort-by-price-2a5e63899233)
* [Faceted Sorting](https://baymard.com/blog/faceted-sorting)
* [Google kills Instant Search](https://www.904labs.com/en/blog-google-kills-instant-search.html)

## Spelling correction

* Peter Norvig. ["How to Write a Spelling Corrector"](http://norvig.com/spell-correct.html). Classic publication.
* Daniel Tunkelang. ["Spelling Correction"](https://queryunderstanding.com/spelling-correction-471f71b19880)
* [A simple spell checker built from word vectors](https://blog.usejournal.com/a-simple-spell-checker-built-from-word-vectors-9f28452b6f26)
* A closer look into the spell correction problem: [1](https://medium.com/@searchhub.io/a-closer-look-into-the-spell-correction-problem-part-1-a6795bbf7112), [2](https://medium.com/@searchhub.io/a-closer-look-into-the-spell-correction-problem-part-2-introducing-predict-8993ecab7226), [3](https://medium.com/@searchhub.io/a-closer-look-into-the-spell-correction-problem-part-3-the-bells-and-whistles-19697a34011b), [preDict](https://github.com/searchhub/preDict)
* [Deep Spelling](https://machinelearnings.co/deep-spelling-9ffef96a24f6)
* [Modeling Spelling Correction for Search at Etsy](https://codeascraft.com/2017/05/01/modeling-spelling-correction-for-search-at-etsy/)
* Wolf Garbe. Author of [Sympell](https://github.com/wolfgarbe/symspell). [1000x Faster Spelling Correction algorithm](https://medium.com/@wolfgarbe/1000x-faster-spelling-correction-algorithm-2012-8701fcd87a5f), [Top highlight SymSpell vs. BK-tree: 100x faster fuzzy string search & spell checking](https://towardsdatascience.com/symspell-vs-bk-tree-100x-faster-fuzzy-string-search-spell-checking-c4f10d80a078), [Fast Word Segmentation of Noisy Text](https://towardsdatascience.com/fast-word-segmentation-for-noisy-text-2c2c41f9e8da)
* [Chars2vec: character-based language model for handling real world texts with spelling errors and](https://hackernoon.com/chars2vec-character-based-language-model-for-handling-real-world-texts-with-spelling-errors-and-a3e4053a147d)
* JamSpell, spelling correction taking into account surrounding context - [library](https://github.com/bakwc/JamSpell), (in russian) [Исправляем опечатки с учётом контекста](https://habr.com/ru/post/346618/)
* [Embedding for spelling correction](https://towardsdatascience.com/embedding-for-spelling-correction-92c93f835d79)
* [A simple spell checker built from word vectors](https://blog.usejournal.com/a-simple-spell-checker-built-from-word-vectors-9f28452b6f26)
* [What are some algorithms of spelling correction that are used by search engines?](https://www.quora.com/String-Searching-Algorithms/What-are-some-algorithms-of-spelling-correction-that-are-used-by-search-engines-For-example-when-I-used-Google-to-search-Google-imeges-it-prompted-me-Did-you-mean-Google-images/answer/Wolf-Garbe)
* [Moman](https://github.com/jpbarrette/moman) - lucene/solr/elasticsearch spell correction/autocorrect is (was?) actually powered by this library.
* [Query Segmentation and Spelling Correction](https://towardsdatascience.com/query-segmentation-and-spelling-correction-483173008981)
* [Applying Context Aware Spell Checking in Spark NLP](https://medium.com/spark-nlp/applying-context-aware-spell-checking-in-spark-nlp-3c29c46963bc)
* [Autocorrect in Google, Amazon and Pinterest and how to write your own one](https://towardsdatascience.com/autocorrect-in-google-amazon-and-pinterest-and-how-to-write-your-own-one-6d23bc927c81)

## Synonyms

* [Boosting the power of Elasticsearch with synonyms](https://www.elastic.co/blog/boosting-the-power-of-elasticsearch-with-synonyms)
* [Real Talk About Synonyms and Search](https://medium.com/@dtunkelang/real-talk-about-synonyms-and-search-bb5cf41a8741)
* [Synonyms in Solr I — The good, the bad and the ugly](https://medium.com/empathyco/synonyms-in-solr-i-the-good-the-bad-and-the-ugly-efe8e437a940)
* [Synonyms and Antonyms from WordNet](https://medium.com/@tameremil/synonyms-and-antonyms-from-wordnet-778f6274fb09)
* [Synonyms and Antonyms in Python](https://towardsdatascience.com/synonyms-and-antonyms-in-python-a865a5e14ce8)
* [Dive into WordNet with NLTK](https://medium.com/parrot-prediction/dive-into-wordnet-with-nltk-b313c480e788)
* [Creating Better Searches Through Automatic Synonym Detection](https://lucidworks.com/post/search-automatic-synonym-detection/)
* [Multiword synonyms in search using Querqy](https://sharing.luminis.eu/blog/multiword-synonyms-in-search-using-querqy/)
* [How to Build a Smart Synonyms Model](https://blog.kensho.com/how-to-build-a-smart-synonyms-model-1d525971a4ee)
* [The importance of Synonyms in eCommerce Search](https://blog.searchhub.io/the-importance-of-synonyms-in-ecommerce-search)

## Stopwords

- [Do all-stopword queries matter?](https://observer.wunderwood.org/2007/05/31/do-all-stopword-queries-matter/)

## Suggestions

Synonyms: autocomplete, search as you type, suggestions

* Giovanni Fernandez-Kincade.
[Bootstrapping Autosuggest](https://medium.com/related-works-inc/bootstrapping-autosuggest-c1ca3edaf1eb), [Building an Autosuggest Corpus, Part 1](https://medium.com/related-works-inc/building-an-autosuggest-corpus-part-1-3acd26056708), [Building an Autosuggest Corpus, Part 2](https://medium.com/related-works-inc/building-an-autosuggest-corpus-nlp-d21b0f25c31b), [Autosuggest Retrieval Data Structures & Algorithms](https://medium.com/related-works-inc/autosuggest-retrieval-data-structures-algorithms-3a902c74ffc8), [Autosuggest Ranking](https://medium.com/related-works-inc/autosuggest-ranking-d8a3242c2837)
* [On two types of suggestions](https://web.archive.org/web/20181207194952/https://www.searchblox.com/autosuggest-search-query-based-vs-content-based)
* [Improving Search Suggestions for eCommerce](https://medium.com/empathyco/improving-search-suggestions-for-ecommerce-cb1bc2946021)
* [Autocomplete Search Best Practices to Increase Conversions](https://lucidworks.com/post/autocomplete-search-increase-conversions/)
* [Why we’ve developed the searchhub smartSuggest module and why it might matter to you](https://www.linkedin.com/pulse/why-weve-developed-searchhub-smartsuggest-module-might-andreas-wagner/)
* Nielsen Norman Group: [Site Search Suggestions](https://www.nngroup.com/articles/site-search-suggestions/)
* [13 Design Patterns for Autocomplete Suggestions](https://baymard.com/blog/autocomplete-design)
* [Autocomplete](https://queryunderstanding.com/autocomplete-69ed81bba245)
* [Autocomplete and User Experience](https://queryunderstanding.com/autocomplete-and-user-experience-421df6ab3000)
* [IMPLEMENTING A LINKEDIN LIKE SEARCH AS YOU TYPE WITH ELASTICSEARCH](https://spinscale.de/posts/2020-05-29-implementing-a-linkedin-like-search-as-you-type-with-elasticsearch.html)
* [Smart autocomplete best practices: improve search relevance and sales](https://blog.griddynamics.com/smart-autocomplete-best-practices/)
* OLX: [Building Corpus for AutoSuggest (Part 1)](https://tech.olx.com/building-corpus-for-autosuggest-part-1-4f63512b1ea1), [AutoSuggest Retrieval & Ranking (Part 2)](https://tech.olx.com/autosuggest-retrieval-ranking-part-2-14a8f50fef34)
* [Autocomplete, Live Search Suggestions, and Autocorrection: Best Practice Design Patterns](https://hybrismart.com/2019/01/08/autocomplete-live-search-suggestions-autocorrection-best-practice-design-patterns/)
* [Mirror, Mirror, What Am I Typing Next? All About Search Suggestions](https://spinscale.de/posts/2023-01-18-mirror-mirror-what-am-i-typing-next.html)
* [How we built the lightning fast autosuggest for otto.de](https://www.youtube.com/watch?v=02GLXE5EAGw)

## Graphs/Taxonomies/Knowledge Graph

* [Knowledge graphs applied in the retail industry](https://towardsdatascience.com/knowledge-graphs-applied-in-the-retail-industry-ecac4e7baf8)

  Knowledge graphs are becoming increasingly popular in tech. We explore how they can be used in the retail industry to enrich data, widen search results and add value to a retail company.  

* [Awesome Knowledge Graphs](https://github.com/frutik/awesome-knowledge-graphs)

### Integrating Search and Knowledge Graphs (by Enterprise Knowledge)

* [Part 1: Displaying Relationships](https://enterprise-knowledge.com/integrating-search-and-knowledge-graphs-series-part-1-displaying-relationships/)
* [Search query expansion with query embeddings](https://bytes.grubhub.com/search-query-embeddings-using-query2vec-f5931df27d79)


## Query expansion

- [Fundamentals of query rewriting (part 1): introduction to query expansion](https://opensourceconnections.com/blog/2021/10/19/fundamentals-of-query-rewriting-part-1-introduction-to-query-expansion/?utm_source=dlvr.it&utm_medium=linkedin)

## Query understanding

* Daniel Tunkelang [Query Understanding](https://queryunderstanding.com/introduction-c98740502103).
* [Query Understanding, Divided into Three Parts](https://medium.com/@dtunkelang/query-understanding-divided-into-three-parts-d9cbc81a5d09)
* [Search for Things not for Strings](https://blog.searchhub.io/humans-search-for-things-not-for-strings-2?cn-reloaded=1)
* Understanding the Search Query. [Part 1](https://towardsdatascience.com/understanding-the-search-query-part-i-632d1b323b50), [Part 2](https://medium.com/analytics-vidhya/understanding-the-search-query-part-ii-44d18892283f), [Part 3](https://medium.com/@sonusharma.mnnit/understanding-the-search-query-part-iii-a0c5637a639)
* [Food Discovery with Uber Eats: Building a Query Understanding Engine](https://eng.uber.com/uber-eats-query-understanding/)
* [AI for Query Understanding](https://www.linkedin.com/pulse/ai-query-understanding-daniel-tunkelang)

### Search Intent

* [Mapping Search Queries To Search Intents](https://medium.com/@dtunkelang/search-queries-and-search-intent-1dec79ad155f)
* [Search: Intent, Not Inventory](https://medium.com/@dtunkelang/search-intent-not-inventory-289386f28a21)

### Query segmentation

* Paper [Unsupervised Query Segmentation Using only Query Logs ](https://www.microsoft.com/en-us/research/wp-content/uploads/2011/01/pp0295-mishra.pdf)
* Paper [Towards Semantic Query Segmentation](https://arxiv.org/pdf/1707.07835.pdf)

## Algorithms

### BERT

* [Understanding BERT and Search Relevance](https://opensourceconnections.com/blog/2019/11/05/understanding-bert-and-search-relevance/)
* [Google is improving web search with BERT – can we use it for enterprise search too?](https://www.linkedin.com/pulse/google-improving-web-search-bert-can-we-use-too-mickel-gr%C3%B6nroos/)

### ColBERT

* [Pretrained Transformer Language Models for Search - part 3](https://blog.vespa.ai/pretrained-transformer-language-models-for-search-part-3/#)

### Collocations, common phrases

* [Automatically detect common phrases – multi-word expressions / word n-grams – from a stream of sentences.]( https://radimrehurek.com/gensim/models/phrases.html)
* [The Unreasonable Effectiveness of Collocations](https://opensourceconnections.com/blog/2019/05/16/unreasonable-effectiveness-of-collocations/)

### Other Algorithms

* [One hot encoding](https://medium.com/fintechexplained/nlp-text-data-to-numbers-d28d32294d2e)
* [Writing a full-text search engine using Bloom filters](https://www.stavros.io/posts/bloom-filter-search-engine/)

#### Hashing

* [Locality Sensitive Hashing](https://towardsdatascience.com/understanding-locality-sensitive-hashing-49f6d1f6134)
* [Locality Sensitive Hashing (LSH): The Practical and Illustrated Guide](https://www.pinecone.io/learn/locality-sensitive-hashing/)
* [Minhash](http://ekzhu.com/datasketch/minhash.html)

#### Sorting by average ratings

* [Better than Average: Sort by Best Rating](https://www.elastic.co/blog/better-than-average-sort-by-best-rating-with-elasticsearch)
* [How Not To Sort By Average Rating](https://www.evanmiller.org/how-not-to-sort-by-average-rating.html)

#### Keywords extraction

* [Keyword Extraction using RAKE](https://codelingo.wordpress.com/2017/05/26/keyword-extraction-using-rake/)
* [Yet Another Keyword Extractor (Yake)](https://github.com/LIAAD/yake)
* [Keyword Extraction with BERT](https://towardsdatascience.com/keyword-extraction-with-bert-724efca412e)

## Tracking, profiling, GDPR, Analysis

### Tools, platforms, helpers for search tracking

* [OpenSearch User Behavior Insights](https://github.com/opensearch-project/user-behavior-insights)
* [Site Search tracking with Google Analytics 4](https://opensourceconnections.com/blog/2023/04/06/site-search-tracking-with-google-analytics-4/)
* [Snowplow](https://snowplow.io/)
* [search-colletor](https://github.com/searchhub/search-collector)
* [OpenTelemetry with search additions](https://gist.github.com/binarymax/16ef2ed12d0aa446a6240c5fbb95e2c3)
* [Pulse Query Analytics](https://pulse.support/)
* [Tracking who's hot and who's not presents an algorithmic challenge](https://www.americanscientist.org/article/the-britney-spears-problem)

### Resources

* [Anonymisation: managing data protection risk (code of practice)](https://ico.org.uk/media/1061/anonymisation-code.pdf)
* [The Anonymisation Decision-Making Framework](https://ukanon.net/wp-content/uploads/2015/05/The-Anonymisation-Decision-making-Framework.pdf)
* [98 personal data points that facebook uses to target ads to you](https://www.washingtonpost.com/news/the-intersect/wp/2016/08/19/98-personal-data-points-that-facebook-uses-to-target-ads-to-you/)
* [Opportunity Analysis for Search](https://www.linkedin.com/pulse/opportunity-analysis-search-daniel-tunkelang/)
* [A Face Is Exposed for AOL Searcher No. 4417749](https://www.nytimes.com/2006/08/09/technology/09aol.html)
* [AOL search data leak](https://en.wikipedia.org/wiki/AOL_search_data_leak)
* [Personal data](https://en.wikipedia.org/wiki/Personal_data)

## Experiments

* [Common Pitfalls of Search Experimentation](https://www.searchhub.io/common-pitfalls-of-search-experimentation/)
* [Improving Search @scale with efficient query experimentation](https://youtu.be/5p9Ss2vn7t4?si=42TBiIpwO5IxO1SZ)

### A/B testing, MABs

* [A/B Testing for Search is Different](https://medium.com/@dtunkelang/a-b-testing-for-search-is-different-f6b0f6f4d0f5)
* [A/B Testing Search: thinking like a scientist](https://medium.com/@jamesrubinstein/a-b-testing-search-thinking-like-a-scientist-1cc34b88392e)

## Testing, metrics, KPIs

### KPIs

* [5 Right Ways to Measure How Search Is Performing](https://opensourceconnections.com/blog/2020/05/11/5-right-ways-to-measure-search/)
* E-commerce Site-Search KPIs. [Part 1 – Customers](https://opensourceconnections.com/blog/2020/08/28/e-commerce-site-search-kpis/), [Part 2 – Products](https://opensourceconnections.com/blog/2020/09/10/e-commerce-site-search-kpis-part-2/), [Part 3 - Queries](https://opensourceconnections.com/blog/2020/09/24/e-commerce-site-search-kpis-part-3-queries/)
* [Learning from Friction to Improve the Search Experience](https://medium.com/@dtunkelang/learning-from-friction-to-improve-the-search-experience-8937c71ec97a)
* [Behind the Wizardry of a Seamless Search Experience](https://enterprise-knowledge.com/if-i-only-had-an-enterprise-search-brain-behind-the-wizardry-of-a-seamless-search-experience/)
* [Analyzing online search relevance metrics with the Elastic Stack](https://www.elastic.co/blog/analyzing-online-search-relevance-metrics-with-the-elastic-stack)
* [How to Gain Insight From Search Analytics](https://www.searchblox.com/how-to-gain-insight-from-search-analytics/)

### Evaluating Search (by Daniel Tunkelang)

* [Measure It](https://medium.com/@dtunkelang/evaluating-good-search-part-i-measure-it-5507b2dbf4f6)
* [Measuring Searcher Behavior](https://medium.com/@dtunkelang/evaluating-search-measuring-searcher-behavior-5f8347619eb0)
* [Using Human Judgement](https://medium.com/@dtunkelang/evaluating-search-using-human-judgement-fbb2eeba37d9)
* [When There’s No Conversion Rate](https://medium.com/@dtunkelang/when-theres-no-conversion-rate-67a372666fed)

### Measuring Search (by James Rubinstein)

* [Statistical and human-centered approaches to search engine improvement](https://medium.com/@jamesrubinstein/statistical-and-human-centered-approaches-to-search-engine-improvement-52af0e98f38f)
* [A Human Approach](https://medium.com/@jamesrubinstein/measuring-search-a-human-approach-acf54e2cf33d)
* [Setting up a relevance evaluation program](https://medium.com/@jamesrubinstein/setting-up-a-relevance-evaluation-program-c955d32fba0e)
* [Metrics Matter](https://medium.com/@jamesrubinstein/measuring-search-metrics-matter-de124c2f6f8c)
* [A/B Testing Search: thinking like a scientist](https://medium.com/@jamesrubinstein/a-b-testing-search-thinking-like-a-scientist-1cc34b88392e)
* [Query Triage: The Secret Weapon for Search Relevance](https://medium.com/@jamesrubinstein/query-triage-the-secret-weapon-for-search-relevance-1a02cdd297ed)
* [The Launch Review: bringing it all together…](https://medium.com/@jamesrubinstein/the-launch-review-bringing-it-all-together-2f7e4cfbf86e)

### Three Pillars of Search Relevancy (by Andreas Wagner)

* [Part 1: Findability](https://blog.searchhub.io/three-pillars-of-search-quality-in-ecommerce-part-1-findability)
* [part 2: Search Quality For Discovery & Inspiration](https://blog.searchhub.io/three-pillars-of-search-quality-in-ecommerce-part-2-discovery-inspiration)

## Architecture

* [The Art Of Abstraction – Revisiting Webshop Architecture](https://blog.searchhub.io/the-art-of-abstraction-revisting-webshop-architecture)
* Canva - Search Pipeline
  * [Part One](https://canvatechblog.com/search-pipeline-part-i-faa6c543aef1) outline of the challenges faced
  * [Part Two](https://canvatechblog.com/search-pipeline-part-ii-3b43978607cd) new search arcthitecture
* [Event-Driven Architecture for Efficient Search Indexing](https://sasarun.medium.com/event-driven-architecture-for-efficient-search-indexing-f7af27192e98)

## Education and networking

### Conferences

* [Activate](https://www.activate-conf.com/)
* [Berlin buzzword](berlinbuzzwords.de)
* [Haystack](https://haystackconf.com/)
* [Elastic{ON}](https://www.elastic.co/elasticon/)
* [MIX-CAMP E-COMMERCE SEARCH](http://www.mices.co)
* [SIGIR eCommerce](https://sigir-ecom.github.io/index.html)
  - [2019](https://sigir-ecom.github.io/ecom2019/index.html)
  - [2018](https://sigir-ecom.github.io/ecom2018/index.html)
  - [2017](http://sigir-ecom.weebly.com/)

### Trainings and courses

* [Cheat at Search with LLMs. Doug Turnbull](http://maven.com/softwaredoug/cheat-at-search) Next: July 2025
* [Relevant Search Masterclass by Doug Turnbull](http://maven.com/softwaredoug/relevant-search) Next: July 2025
* OpenSource Connections
  - [Elasticsearch "Think Like a Relevance Engineer"](https://opensourceconnections.com/training/elasticsearch-think-like-a-relevance-engineer-tlre/)
  - [Solr "Think Like a Relevance Engingeer"](https://opensourceconnections.com/training/solr-think-like-a-relevance-engineer-tlre/)
  - [Beyond Search Relevance: Understanding and Measuring Search Result Quality](https://opensourceconnections.com/training/beyond-search-relevance-understanding-and-measuring-search-result-quality/)
  - [Hello LTR](https://opensourceconnections.com/training/hello-ltr-learning-to-rank/)
* [Sease's trainings](https://sease.io/training)
* [Search Fundamentals. Daniel Tunkelang, Grant Ingersoll](https://corise.com/course/search-fundamentals) Next: Feb 6, 2023  
* [Search with Machine Learning. Daniel Tunkelang, Grant Ingersoll](https://corise.com/course/search-with-machine-learning)  Next: Feb 27, 2023  
* [Search for Product Managers. Daniel Tunkelang](https://corise.com/course/search-for-product-managers) Next: Apr 3, 2023 
* [Sematext's Solr, Elasticsearch, and OpenSearch trainings](https://sematext.com/training/)

  Fall 2023

* https://dtunkelang.medium.com/upcoming-search-classes-this-fall-58f877fe00ad

### Books

* [AI-powered search](https://www.manning.com/books/ai-powered-search)
* [Relevant Search](https://www.manning.com/books/relevant-search)
* [Deep Learning for search](https://www.manning.com/books/deep-learning-for-search)
* [Interactions with search systems](https://www.cambridge.org/core/books/interactions-with-search-systems/5B3CF5920355A8B09088F2C409FFABDC)
* [Embeddings in Natural Language Processing. Theory and Advances in Vector Representation of Meaning](http://josecamachocollados.com/book_embNLP_draft.pdf)
* [Search User Interfaces](http://www.searchuserinterfaces.com)
* [Search Patterns](https://searchpatterns.org/)
* [Search Analytics for Your Site: Conversations with Your Customers](https://www.amazon.com/Search-Analytics-Your-Site-Conversations/dp/1933820209)
* [Click Models for Web Search](https://www.amazon.com/Synthesis-Lectures-Information-Concepts-Retrieval/dp/1627056475/)
* [Optimization Algorithms](https://www.manning.com/books/optimization-algorithms)
* [Query Understanding for Search Engines](https://link.springer.com/book/10.1007/978-3-030-58334-7)

### Blogs and Portals

* [Searchnews](http://searchnews.org/)
  
  
### Papers

* [List of papers](PAPERS.md)

## Management, Search Team

* [Search is a Team Sport](https://medium.com/search-in-21st-century/search-is-a-team-sport-400eecdfe736)
* [Thoughts about Managing Search Teams](https://medium.com/@dtunkelang/thoughts-about-managing-search-teams-f8d2f54fbed7)
* [On Search Leadership](https://dtunkelang.medium.com/on-search-leadership-815b36c15df1)
* [Building an Effective Search Team: the key to great search & relevancy](https://opensourceconnections.com/blog/2020/05/14/building-an-effective-search-team-the-key-to-great-search-relevancy/)
* [Query Triage: The Secret Weapon for Search Relevance](https://medium.com/@jamesrubinstein/query-triage-the-secret-weapon-for-search-relevance-1a02cdd297ed)
* [The Launch Review: bringing it all together ](https://medium.com/@jamesrubinstein/the-launch-review-bringing-it-all-together-2f7e4cfbf86e)
* [The Role of Search Product Owners](https://enterprise-knowledge.com/the-role-of-search-product-owners/)
* [Search Product Management: The Most Misunderstood Role in Search?](https://jamesrubinstein.medium.com/search-product-management-the-most-misunderstood-role-in-search-2b7569058638)
* [Search relevance for understaffed teams](https://softwaredoug.com/blog/2023/05/29/guide-for-search-teams.html)

### Job Interviews

* [Interview Questions for Search Relevance Engineers, Data Scientists, and Product Managers](https://medium.com/@dtunkelang/interview-questions-for-search-relevance-engineers-and-product-managers-7a1b6b8cacea)
* [Data Science Interviews: Ranking and search](https://github.com/alexeygrigorev/data-science-interviews/blob/master/theory.md#ranking-andsearch)
  
### Engineering

* [Technical debt in search](https://twitter.com/gsingers/status/1655286486692970497?t=7HVu0Kc2vXT5NPHH_bB2uA&s=19)

## Blogposts series

### Search Optimization 101 (by Charlie Hull)

* [How do I know that my search is broken?](https://blog.supahands.com/2020/07/08/how-do-i-know-that-my-search-is-broken/)
* [What does it mean if my search is ‘broken’?](https://blog.supahands.com/2020/07/20/search-optimization-101-what-does-it-mean-if-my-search-is-broken/)
* [How do you fix a broken search?](https://blog.supahands.com/2020/08/04/search-optimization-101-how-do-you-fix-a-broken-search/)
* [Reducing business risk by optimizing search
](https://blog.supahands.com/2020/09/02/reducing-business-risks-by-optimizing-search/)

### Query Understanding (by Daniel Tunkelang)
   Better search through query understanding.

* [An Introduction](https://queryunderstanding.com/introduction-c98740502103)
* [Language Identification](https://queryunderstanding.com/language-identification-c1d2a072eda)
* [Character Filtering](https://queryunderstanding.com/character-filtering-76ede1cf1a97)
* [Tokenization](https://queryunderstanding.com/tokenization-c8cdd6aef7ff)
* [Spelling Correction](https://queryunderstanding.com/spelling-correction-471f71b19880)
* [Stemming and Lemmatization](https://queryunderstanding.com/stemming-and-lemmatization-6c086742fe45)
* [Query Rewriting: An Overview](https://queryunderstanding.com/query-rewriting-an-overview-d7916eb94b83)
* [Query Expansion](https://queryunderstanding.com/query-expansion-2d68d47cf9c8)
* [Query Relaxation](https://queryunderstanding.com/query-relaxation-342bc37ad425)
* [Query Segmentation](https://queryunderstanding.com/query-segmentation-2cf860ade503)
* [Query Scoping](https://queryunderstanding.com/query-scoping-ed61b5ec8753)
* [Entity Recognition](https://queryunderstanding.com/entity-recognition-763cae840a20)
* [Taxonomies and Ontologies](https://queryunderstanding.com/taxonomies-and-ontologies-8e4812a79cb2)
* [Autocomplete](https://queryunderstanding.com/autocomplete-69ed81bba245)
* [Autocomplete and User Experience](https://queryunderstanding.com/autocomplete-and-user-experience-421df6ab3000)
* [Contextual Query Understanding: An Overview](https://queryunderstanding.com/contextual-query-understanding-65c78d792dd8)
* [Session Context](https://queryunderstanding.com/session-context-4af0a355c94a)
* [Location as Context](https://queryunderstanding.com/geographical-context-77ce4c773dc7)
* [Seasonality](https://queryunderstanding.com/seasonality-5eef79d8bf1c)
* [Personalization](https://queryunderstanding.com/personalization-3ed715e05ef)
* [Search as a Conversation](https://queryunderstanding.com/search-as-a-conversation-bafa7cd0c9a5)
* [Clarification Dialogues](https://queryunderstanding.com/clarification-dialogues-69420432f451)
* [Relevance Feedback](https://queryunderstanding.com/relevance-feedback-c6999529b92c)
* [Faceted Search](https://queryunderstanding.com/faceted-search-7d053cc4fada)
* [Search Results Presentation](https://queryunderstanding.com/search-results-presentation-7d6c6c384ec1)
* [Search Result Snippets](https://queryunderstanding.com/search-result-snippets-e8c447950219)
* [Search Results Clustering](https://queryunderstanding.com/search-results-clustering-b2fa64c6c809)
* [Question Answering](https://queryunderstanding.com/question-answering-94984185c203)
* [Query Understanding and Voice Interfaces](https://queryunderstanding.com/query-understanding-and-voice-interfaces-6cd60d063fca)
* [Query Understanding and Chatbots](https://queryunderstanding.com/query-understanding-and-chatbots-5fa0c154f)

### Grid Dynamics

* [Not your father’s search engine: a brief history of retail search](https://blog.griddynamics.com/not-your-fathers-search-engine-a-brief-history-of-retail-search/)
* [Semantic vector search: the new frontier in product discovery](https://blog.griddynamics.com/semantic-vector-search-the-new-frontier-in-product-discovery/)
* [Boosting product discovery with semantic search](https://blog.griddynamics.com/boosting-product-discovery-with-semantic-search/)
* [Semantic query parsing blueprint](https://blog.griddynamics.com/semantic-query-parsing-blueprint/)

### Considering Search: Search Topics (by Derek Sisson)

* [Intro](https://www.philosophe.com/archived_content/search_topics/search_topics.html)
* [Assumptions About Search](https://www.philosophe.com/archived_content/search_topics/search_assumptions.html)
* [Assumptions About User Search Behavior](https://www.philosophe.com/archived_content/search_topics/user_behavior.html)
* [Types of Information Collections](https://www.philosophe.com/archived_content/search_topics/collections.html)
* [A Structural Look at Search](https://www.philosophe.com/archived_content/search_topics/structure.html)
* [Users and the Task of Information Retrieval](https://www.philosophe.com/archived_content/search_topics/search_tasks.html)
* [Testing Search](https://www.philosophe.com/archived_content/search_topics/search_tests.html)
* [Useful Search Links and References](https://www.philosophe.com/archived_content/search_topics/search_links.html)

## Industry players

### Personalies and influencers

* [Daniel Tunkelang (he is God of Search)](https://medium.com/@dtunkelang)
* [Max Irwin](https://twitter.com/binarymax)
* [Doug Turnbull](https://twitter.com/softwaredoug)
* [Baymard’s Institute](https://baymard.com/blog)

### Search Engines

* Google
* Bing
* Yandex
* Amazon
* eBay

### Products and services

* [Algolia](https://www.algolia.com/)
* [Vespa] (https://vespa.ai/)
* [Elasticsearch](https://github.com/elastic/elasticsearch) - Distributed search & analytics engine
* [ParadeDB](https://github.com/paradedb/paradedb) - Modern Elasticsearch alternative built on Postgres. Built for real-time, update-heavy workloads.
* [Solr](https://solr.apache.org/) - Solr is the blazing-fast, open source, multi-modal search platform built on the full-text vector, and geospatial search capabilities of Apache Lucene
* [Fess Enterprise Search Server](https://github.com/codelibs/fess)
* [Typesense](https://github.com/typesense/typesense) - an opensource alternative to Algolia.
* [TopK](https://topk.io/) - combines AI-powered query understanding with adaptive ranking to provide the most relevant results in your domain.
* [SearchHub.io](https://www.searchhub.io/)
* [Datafari](https://www.datafari.com/en/index.html) - an open source enterprise search solution. 
* [Qdrant](https://qdrant.tech/) - an open source vector database.
* [Awakari](https://awakari.com) - Real-Time search from unlimited sources like RSS, Fediverse, Telegram. Text keyword matching conditions, numeric conditions, condition groups. Reverse search index based.
* [Meilisearch](https://www.github.com/meilisearch/meilisearch) - Open source search API that supports full-text, vector, geospatial & faceted search.

### Consulting companies

* [BigData Boutique](https://bigdataboutique.com/services/elasticsearch-consulting)
* [OpenSource Connections](https://www.opensourceconnections.com)
* https://sease.io/
* [Sematext](https://sematext.com/)

## Case studies

* Airbnb - [Machine Learning-Powered Search Ranking of Airbnb Experiences](https://medium.com/airbnb-engineering/machine-learning-powered-search-ranking-of-airbnb-experiences-110b4b1a0789)
* Airbnb - [Listing Embeddings in Search Ranking](https://medium.com/airbnb-engineering/listing-embeddings-for-similar-listing-recommendations-and-real-time-personalization-in-search-601172f7603e)
* Algolia - [The Architecture Of Algolia’s Distributed Search Network](http://highscalability.com/blog/2015/3/9/the-architecture-of-algolias-distributed-search-network.html)
* Meituan - Exploration and practice of BERT in the core ranking of Meituan search (🇨🇳 [BERT在美团搜索核心排序的探索和实践](https://tech.meituan.com/2020/07/09/bert-in-meituan-search.html))
* Netflix - How Netflix Content Engineering makes a federated graph searchable ([Part 1](https://netflixtechblog.com/how-netflix-content-engineering-makes-a-federated-graph-searchable-5c0c1c7d7eaf), [Part 2](https://netflixtechblog.com/how-netflix-content-engineering-makes-a-federated-graph-searchable-part-2-49348511c06c))
* Netflix - [Elasticsearch Indexing Strategy in Asset Management Platform (AMP)](https://netflixtechblog.medium.com/elasticsearch-indexing-strategy-in-asset-management-platform-amp-99332231e541)
* Skyscanner - [Learning to Rank for Flight Itinerary Search](https://hackernoon.com/learning-to-rank-for-flight-itinerary-search-8594761eb867)
* Slack - [Search at Slack](https://slack.engineering/search-at-slack-431f8c80619e)
* Twitter - [Stability and scalability for search](https://blog.twitter.com/engineering/en_us/topics/infrastructure/2022/stability-and-scalability-for-search)
* [Amazon SEO Explained: How to Rank Your Products #1 in Amazon Search Results in 2020](https://crazylister.com/blog/amazon-seo-ultimate-guide/)
* [Building a Better Search Engine for Semantic Scholar](https://medium.com/ai2-blog/building-a-better-search-engine-for-semantic-scholar-ea23a0b661e7)

### General search

* [How Bing Ranks Search Results: Core Algorithm & Blue Links](https://www.searchenginejournal.com/how-bing-ranks-search-results/357804/)
* [How Google Search Ranking Works – Darwinism in Search](https://www.searchenginejournal.com/how-google-search-ranking-works/307591/)


### E-commerce

* [Searchandising](https://searchanise.io/blog/searchandising/)

### Multisided markets

* [Discover How Cassini (The eBay Search Engine) Works and Rank](https://crazylister.com/blog/ebay-search-engine-cassini/)


## Videos
[Apache Solr Short Tips](https://www.youtube.com/watch?v=YFoPWgja89o&list=PLT_fd32OFYpe7xXxUYtV8upGcZtgPY3cU)

### Channels

* [Lucid Thoughts](https://www.youtube.com/c/LucidThoughts)
* [Lucidworks](https://www.youtube.com/user/LucidWorksSearch)
* [MIx-Camp E-commerce Search](https://www.youtube.com/channel/UCCxvMykUdtFFc1O_tIr9oxA)
* [OpenSource Connections](https://www.youtube.com/channel/UCiuXt-f2Faan4Es37nADUdQ)
* [SIGIR eCom](https://www.youtube.com/channel/UCd6PyC_9zrxgA7vmT05Mx4Q)

### Featured

* [Relevant Facets](https://www.youtube.com/watch?v=W8DJYfAKKLA)

## Datasets
  
* [Shopping Queries Dataset: A Large-Scale ESCI Benchmark for Improving Product Search](https://github.com/amazon-science/esci-data/tree/main)
* [ESCI-S: extended metadata for Amazon ESCI dataset](https://github.com/shuttie/esci-s)  
* [Home Depot Product Search Relevance](https://www.kaggle.com/competitions/home-depot-product-search-relevance/data)
* [WANDS - Wayfair ANnotation Dataset](https://github.com/wayfair/WANDS)  
  
## Tools
  
### Spacy

[Awesome Spacy](https://github.com/frutik/awesome-spacy) - Natural language upderstanding, content enrichment etc.

### Word2Vec

* [Word2Vec For Phrases — Learning Embeddings For More Than One Word](https://towardsdatascience.com/word2vec-for-phrases-learning-embeddings-for-more-than-one-word-727b6cf723cf)
* [Gensim Word2Vec Tutorial](http://kavita-ganesan.com/gensim-word2vec-tutorial-starter-code/#.XV-wnJMzbUL)
* [How to incorporate phrases into Word2Vec – a text mining approach](http://kavita-ganesan.com/how-to-incorporate-phrases-into-word2vec-a-text-mining-approach/#.XV-wnJMzbUL)
* [Word2Vec — a baby step in Deep Learning but a giant leap towards Natural Language Processing](https://medium.com/explore-artificial-intelligence/word2vec-a-baby-step-in-deep-learning-but-a-giant-leap-towards-natural-language-processing-40fe4e8602ba)
* [How to Develop Word Embeddings in Python with Gensim](https://machinelearningmastery.com/develop-word-embeddings-python-gensim/)

### Libs

* [Query Segmenter](https://github.com/soumyaxyz/query-segmenter)
* [Tantivy](https://github.com/quickwit-oss/tantivy) - Tantivy is a full-text search engine library inspired by Apache Lucene and written in Rust
* https://github.com/zentity-io/zentity
* https://github.com/mammothb/symspellpy
* https://github.com/searchhub/search-collector
* [Kiri](https://github.com/kiri-ai/kiri) - State-of-the-art semantic search made easy.
* [Haystack](https://github.com/deepset-ai/haystack) - End-to-end Python framework for building natural language search interfaces to data.
* https://github.com/castorini/docTTTTTquery

### Other

* [Chorus](https://github.com/querqy/chorus), [Smui](https://github.com/querqy/smui), [Querqy](https://github.com/querqy/querqy)
* [Quepid](https://github.com/o19s/quepid)
* [Rated Ranking Evaluator](https://github.com/SeaseLtd/rated-ranking-evaluator)
* [Jina AI](https://github.com/jina-ai/jina) - A neural search framework

## Other awesome stuff

* [Awesome Knowledge Graphs](https://github.com/frutik/awesome-knowledge-graphs)
* [Awesome time series](https://github.com/frutik/awesome-timeseries)
* [Awesome Spacy](https://github.com/frutik/awesome-spacy)
* [Query-Understanding](https://github.com/sanazb/Query-Understanding)
* [Click models](https://github.com/filipecasal/knowledge-repo/blob/master/click_models.md)

OLD TOC (to review)



- [General, fun, philosophy](#general-fun-philosophy)
- [Types of search](#types-of-search)
  - [Classic/Lexical search](#classic-lexical-search)
  - [Vectors/Semantic search](#vectorssemantic-search)
    -  [Embeddings](#embeddings)
        - [Types of vectors](#types-of-vectors)
          - [Dense vectors](#dense-vectors)
            - [Size of input and Chunking](#size-of-input-and-chunking)
              - [Positional chunking](#positional-chunking)
              - [Semantic chunking](#semantic-chunking)
            - [Matryoshka embeddings](#matryoshka-embeddings)
          - [Sparse vectors](#sparse-vectors)
            - [SPLADE](#splade)  
        - [Vector retrieval](#vector-retrieval)
          - Main architectures
          - [Query/Document tokens interaction]()
            - [No interactions - Two towers / Bi-encoders](#two-towers--bi-encoders)
            - [Early interactions - Cross-encoders](#early-interactions---cross-encoders)
            - [Late interactions - ColBERT](#late-interactions--colbert)
        - [Handling high-dimension embeddings](#handling-high-dimension-embeddings)
          - [Dimensionality reduction](#dimensionality-reduction)
          - [Quantization](#quantization)
            - [Scalar quantization](#scalar-quantization)
            - [Binary quantization](#binary-quantization)
            - [Product quantization](#product-quantization)
            - [Rotational quantization](#rotational-quantization)
        - [Finetuning models](#finetuning-models)
    - [Symmetric and Asymmetric semantic search](#symmetric-and-asymmetric-semantic-search)
  - [Hybrid search](#hybrid-search)
    - [Reciprocal rank fusion - RRF](#reciprocal-rank-fusion-rrf)
    - [Linear Score Combination](#linear-score-combination)
  - [Multimodal search](#multimodal-search)
    - [Multimodality Problems](#multimodality-problems)
      - [Modality Gap](#modality-gap)
      - [Contrastive Gap](#contrastive-gap)  
  - [Federated search](#federated-search)
- [Search Quality Assurance](#search-quality-assurance)
  - [How to select queries](#how-to-select-queries)
    - [Random sampling](#random-sampling)
    - [Stratified sampling](#stratified-sampling)
    - [Probability-proportional-to-size sampling](#probability-proportional-to-size-sampling)
  - [Metrics](#metrics)
    - [Focused on ranking quality](#focused-on-ranking-quality)
    - [Focused on diversity of results](#focused-on-diversity-of-results)
  - [Offline quality measuring](#offline-quality-measuring)
    - [Judgements](#judgements)
      - Explicite judgements, [HUman judgements](#human-judgements)
      - [Implicite judgements](#implicite-judgements)
      - [Using LLM as judge](#using-llm-as-judge)
  - [Online quality measuring](#online-quality-measuring)
- [Areas of application](#also-types-of-search)
  - [Enterprise search](#enterprise-search)
  - [e-Commerce search](#e-commerce-search)
  - [Conversational search](#conversational-search)
  - [Geo-Spatial Search]()
  - [Medical and Healthcare Search]()
  - [Social Media and User-Generated Content Search]()
  - [Question Answering Systems]()
  - [Personal Information Management]()
- [Search Results](#search-results)
  - [Retrieval](#retrieval)
    - [Relevance](#relevance)
      - [Relevance Algorithms](#relevance-algorithms)
  - [Ranking](#ranking)
    - [Multi stage ranking](#multi-stage-ranking)
      - [Reranking](£reranking)  
    - [Learning to Rank](#learning-to-rank)
      - [Click models for search](#click-models-for-search)
  - [Bias](#bias)
  - [Diversification](#diversification)
    - [MMR](#mmr)  
  - [Personalisation](#personalisation)
  - [Zero search results](#zero-search-results)
- [Search UX](#search-ux)
  - [Baymard Institute](#baymard-institute)
  - [Nielsen Norman Group](#nielsen-norman-group)
  - [Enterprise Knowledge LLC](#enterprise-knowledge-llc)
  - [Facets](#facets)
    - [Accidental Taxonomist](#accidental-taxonomist)
  - [Other](#other)
- [Spelling correction](#spelling-correction)
- [Suggestions](#suggestions)
- [Synonyms](#synonyms)
- [Stopwords](#stopwords)
- [Graphs/Taxonomies/Knowledge Graph](#graphstaxonomiesknowledge-graph)
  - Integrating Search and Knowledge Graphs (by Enterprise Knowledge)
- [Query expansion](#query-expansion)
- [Query understanding](#query-understanding)
  - [Search Intent](#search-intent)
  - [Query segmentation](#query-segmentation)
- [Algorithms](#algorithms)
  - [BERT](#bert)
  - [ColBERT](#colbert)
  - [Collocations, common phrases](#collocations-common-phrases)
  - [Other Algorithms](#other-algorithms)
- [Tracking, profiling, GDPR, Analysis](#tracking-profiling-gdpr-analysis)
- [Experiments](#experiments)
  - A/B testing, MABs
- Evaluating search
  - MRR
  - [Testing, metrics, KPIs](#testing-metrics-kpis)
    - KPIs
  - Evaluating Search (by Daniel Tunkelang)
  - Measuring Search (by James Rubinstein)
  - Three Pillars of Search Relevancy (by Andreas Wagner)
- [Architecture](#architecture)  
- [Vectors search](#vectors-search)
- [Education and networking](#education-and-networking)
  - [Conferences](#conferences)
  - [Trainings and courses](#trainings-and-courses)
  - [Books](#books)
  - [Blogs and Portals, News](#blogs-and-portals)
  - [Papers](#papers)
- [Management, Search Team](#management-search-team)
  - [Job Interviews](#job-interviews)
  - [Engineering](#engineering)
- [Industry players](#industry-players)
  - Personalies and influencers
  - Search Engines
  - Products and services
  - Consulting companies
- [Blogposts series](#blogposts-series)
  - Search Optimization 101 (by Charlie Hull)
  - Query Understanding (by Daniel Tunkelang)
  - Grid Dynamics
  - Considering Search: Search Topics (by Derek Sisson)
- [Videos](#videos)
  - Channels
  - Featured
- [Case studies](#case-studies)
  - [General search](#general-search)
  - [Multisided markets](#multisided-markets)
  - [E-commerce](#e-commerce) 
- [Datasets](#datasets)
- [Tools](#tools)

