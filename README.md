# Awesome-search

I've been building search applications for almost ten years. Below you can find a list of (some) publications, conferences and books that inspire me. Grouped by topic.

### Topics
- [General, fun, philosophy](#general-fun-philosophy)
- [Types of search](#types-of-search)
- [Baymard's guides](#baymards-guides) 
- [Spelling correction](#spelling-correction) 
- [Synonyms](#synonyms) 
- [Suggestions](#suggestions) 
- [BERT](#bert) 
- [Spacy](#spacy) 
- [Word2Vec](#word2vec) 
- [Collocations, common phrases](#collocations-common-phrases)
- [Graphs/Taxonomies/Knowledge Graph](#graphstaxonomiesknowledge-graph) 
- [Query understanding](#query-understanding)
- [Learning to rank](#learning-to-rank)
- [Other, Search](#other-search) 
- [Other, Algorithms](#other-algorithms)
- [Tracking, profiling, GDPR, Analysis](#tracking-profiling-gdpr-analysis) 
- [Testing](#testing) 
- [Conferences](#conferences) 
- [Books](#books) 
- [Personalies and influencers](#personalies-and-influencers) 
- [Usecases](#usecases)

## General, fun, philosophy

* [Falsehoods Programmers Believe About Search](https://opensourceconnections.com/blog/2019/05/29/falsehoods-programmers-believe-about-search/)
* [Ethical Search: Designing an irresistible journey with a positive impact](https://medium.com/empathyco/fooddiscovery-2-ethical-search-designing-an-irresistible-journey-with-a-positive-impact-cc921c07a5a8)
* [Humans Search for Things not for Strings](https://www.linkedin.com/pulse/humans-search-things-strings-andreas-wagner/)
* [On Semantic Search](https://medium.com/modern-nlp/semantic-search-fuck-yeah-e371c0f639d)
* [Feedback debt: what the segway teaches search teams](https://opensourceconnections.com/blog/2020/03/19/feedback-debt/)

## Types of search

* Etsy. [Targeting Broad Queries in Search](https://codeascraft.com/2015/07/29/targeting-broad-queries-in-search/)
* [How Etsy Uses Thermodynamics to Help You Search for “Geeky”](https://codeascraft.com/2015/08/31/how-etsy-uses-thermodynamics-to-help-you-search-for-geeky/)
* Daniel Tunkelang.
[Broad and Ambiguous Search Queries](https://medium.com/@dtunkelang/broad-and-ambiguous-search-queries-1bbbe417dcc)

## Baymard's guides

* [Deconstructing E-Commerce Search: The 12 Query Types](https://baymard.com/blog/ecommerce-search-query-types)
* [Autodirect or Guide Users to Matching Category](https://baymard.com/blog/autodirect-searches-matching-category-scopes)
* [13 Design Patterns for Autocomplete Suggestions (27% Get it Wrong)]()
* [E-Commerce Search Needs to Support Users’ Non-Product Search Queries (15% Don’t)]()
* [Search UX: 6 Essential Elements for ‘No Results’ Pages]()
* [Product Thumbnails Should Dynamically Update to Match the Variation Searched For (54% Don’t)]()
* [Faceted Sorting - A New Method for Sorting Search Results]()
* [The Current State of E-Commerce Search]()
* [E-Commerce Sites Need Multiple of These 5 ‘Search Scope’ Features]()
* [E-Commerce Search Field Design and Its Implications]()
* [E-Commerce Sites Should Include Contextual Search Snippets (96% Get it Wrong)]()
* [E-Commerce Search Usability: Report & Benchmark]()

## Spelling correction

* Peter Norvig. ["How to Write a Spelling Corrector"](http://norvig.com/spell-correct.html). Classic publication. 
* Daniel Tunkelang. ["Spelling Correction"](https://queryunderstanding.com/spelling-correction-471f71b19880)
* [A simple spell checker built from word vectora](https://blog.usejournal.com/a-simple-spell-checker-built-from-word-vectors-9f28452b6f26)
* A closer look into the spell correction problem: [1](https://medium.com/@searchhub.io/a-closer-look-into-the-spell-correction-problem-part-1-a6795bbf7112), [2](https://medium.com/@searchhub.io/a-closer-look-into-the-spell-correction-problem-part-2-introducing-predict-8993ecab7226), [3](https://medium.com/@searchhub.io/a-closer-look-into-the-spell-correction-problem-part-3-the-bells-and-whistles-19697a34011b), [preDict](https://github.com/searchhub/preDict)
* [Deep Spelling](https://machinelearnings.co/deep-spelling-9ffef96a24f6)
* [Modeling Spelling Correction for Search at Etsy](https://codeascraft.com/2017/05/01/modeling-spelling-correction-for-search-at-etsy/)
* Wolf Garbe. Author of [Sympell](https://github.com/wolfgarbe/symspell). [1000x Faster Spelling Correction algorithm](https://medium.com/@wolfgarbe/1000x-faster-spelling-correction-algorithm-2012-8701fcd87a5f), [Top highlight SymSpell vs. BK-tree: 100x faster fuzzy string search & spell checking](https://towardsdatascience.com/symspell-vs-bk-tree-100x-faster-fuzzy-string-search-spell-checking-c4f10d80a078), [Fast Word Segmentation of Noisy Text](https://towardsdatascience.com/fast-word-segmentation-for-noisy-text-2c2c41f9e8da)
* [Chars2vec: character-based language model for handling real world texts with spelling errors and](https://hackernoon.com/chars2vec-character-based-language-model-for-handling-real-world-texts-with-spelling-errors-and-a3e4053a147d)
* JamSpell, spelling correction taking into account surrounding context - [library](https://github.com/bakwc/JamSpell), (in russian) [Исправляем опечатки с учётом контекста](https://habr.com/ru/post/346618/)
* [Embedding for spelling correction](https://towardsdatascience.com/embedding-for-spelling-correction-92c93f835d79)
* [A simple spell checker built from word vectors](https://blog.usejournal.com/a-simple-spell-checker-built-from-word-vectors-9f28452b6f26)
* [What are some algorithms of spelling correction that are used by search engines?](https://www.quora.com/String-Searching-Algorithms/What-are-some-algorithms-of-spelling-correction-that-are-used-by-search-engines-For-example-when-I-used-Google-to-search-Google-imeges-it-prompted-me-Did-you-mean-Google-images/answer/Wolf-Garbe)
* [Moman](https://github.com/jpbarrette/moman) - lucene/solr/elasticsearch spell correction/autocorrect is actually powered by this library.
* [Query Segmentation and Spelling Correction](https://towardsdatascience.com/query-segmentation-and-spelling-correction-483173008981)

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

## Suggestions

* Giovanni Fernandez-Kincade. 
[Bootstrapping Autosuggest](https://medium.com/related-works-inc/bootstrapping-autosuggest-c1ca3edaf1eb), [Building an Autosuggest Corpus, Part 1](https://medium.com/related-works-inc/building-an-autosuggest-corpus-part-1-3acd26056708), [Building an Autosuggest Corpus, Part 2](https://medium.com/related-works-inc/building-an-autosuggest-corpus-nlp-d21b0f25c31b), [Autosuggest Retrieval Data Structures & Algorithms](https://medium.com/related-works-inc/autosuggest-retrieval-data-structures-algorithms-3a902c74ffc8), [Autosuggest Ranking](https://medium.com/related-works-inc/autosuggest-ranking-d8a3242c2837)
* [13 Design Patterns for Autocomplete Suggestions](https://baymard.com/blog/autocomplete-design)
* [On two types of suggestions](https://web.archive.org/web/20181207194952/https://www.searchblox.com/autosuggest-search-query-based-vs-content-based)
* [Improving Search Suggestions for eCommerce](https://medium.com/empathyco/improving-search-suggestions-for-ecommerce-cb1bc2946021)
* [Autocomplete Search Best Practices to Increase Conversions](https://lucidworks.com/post/autocomplete-search-increase-conversions/)

## BERT

* [Understanding BERT and Search Relevance](https://opensourceconnections.com/blog/2019/11/05/understanding-bert-and-search-relevance/)
* [Google is improving web search with BERT – can we use it for enterprise search too?](https://www.linkedin.com/pulse/google-improving-web-search-bert-can-we-use-too-mickel-gr%C3%B6nroos/)

## Spacy

[Awesome Spacy](https://github.com/frutik/awesome-spacy) - Natural language upderstanding, content enrichment etc.

## Word2Vec

* [Word2Vec For Phrases — Learning Embeddings For More Than One Word](https://towardsdatascience.com/word2vec-for-phrases-learning-embeddings-for-more-than-one-word-727b6cf723cf)
* [Gensim Word2Vec Tutorial](http://kavita-ganesan.com/gensim-word2vec-tutorial-starter-code/#.XV-wnJMzbUL)
* [How to incorporate phrases into Word2Vec – a text mining approach](http://kavita-ganesan.com/how-to-incorporate-phrases-into-word2vec-a-text-mining-approach/#.XV-wnJMzbUL)
* [Word2Vec — a baby step in Deep Learning but a giant leap towards Natural Language Processing](https://medium.com/explore-artificial-intelligence/word2vec-a-baby-step-in-deep-learning-but-a-giant-leap-towards-natural-language-processing-40fe4e8602ba)
* [How to Develop Word Embeddings in Python with Gensim](https://machinelearningmastery.com/develop-word-embeddings-python-gensim/)

## Collocations, common phrases

* [Automatically detect common phrases – multi-word expressions / word n-grams – from a stream of sentences.]( https://radimrehurek.com/gensim/models/phrases.html)
* [The Unreasonable Effectiveness of Collocations](https://opensourceconnections.com/blog/2019/05/16/unreasonable-effectiveness-of-collocations/)

## Graphs/Taxonomies/Knowledge Graph

* [Combining WordNet and ConceptNet in Neo4j](http://tomkdickinson.co.uk/2017/05/21/combining-wordnet-and-conceptnet-in-neo4j/)
* [Dive into WordNet with NLTK](https://medium.com/parrot-prediction/dive-into-wordnet-with-nltk-b313c480e788)
* [Awesome Knowledge Graphs](https://github.com/frutik/awesome-knowledge-graphs)

## Query understanding

* Daniel Tunkelang [Query Understanding](https://queryunderstanding.com/introduction-c98740502103). 
* [Query Understanding, Divided into Three Parts](https://medium.com/@dtunkelang/query-understanding-divided-into-three-parts-d9cbc81a5d09)
* [Search for Things not for Strings](https://medium.com/@searchhub.io/humans-search-for-things-not-for-strings-5dd115d95986)

## Learning to Rank

* [How is search different than other machine learning problems?](https://opensourceconnections.com/blog/2017/08/03/search-as-machine-learning-prob/)

## Other, Search

* Baymard Institute [11 E-Commerce Search Articles](https://baymard.com/ecommerce-search/articles)
* [Why is it so hard to sort by price?](https://medium.com/@dtunkelang/why-is-it-so-hard-to-sort-by-price-2a5e63899233)
* [Faceted Sorting](https://baymard.com/blog/faceted-sorting)

## Other, Algorithms

* [Locality Sensitive Hashing](https://towardsdatascience.com/understanding-locality-sensitive-hashing-49f6d1f6134)
* [Minhash](http://ekzhu.com/datasketch/minhash.html)
* [Better than Average: Sort by Best Rating](https://www.elastic.co/blog/better-than-average-sort-by-best-rating-with-elasticsearch)
* [How Not To Sort By Average Rating](https://www.evanmiller.org/how-not-to-sort-by-average-rating.html)
* [The influence of TF-IDF algorithms in eCommerce search](https://medium.com/empathyco/the-influence-of-tf-idf-algorithms-in-ecommerce-search-e7cb9ab8e662)
* [One hot encoding](https://medium.com/fintechexplained/nlp-text-data-to-numbers-d28d32294d2e)
* [Keyword Extraction using RAKE](https://codelingo.wordpress.com/2017/05/26/keyword-extraction-using-rake/)

## Tracking, profiling, GDPR, Analysis

* [Anonymisation: managing data protection risk (code of practice)](https://ico.org.uk/media/1061/anonymisation-code.pdf)
* [The Anonymisation Decision-Making Framework](https://ukanon.net/wp-content/uploads/2015/05/The-Anonymisation-Decision-making-Framework.pdf)
* [98 personal data points that Facebook uses to target ads to you](https://www.washingtonpost.com/news/the-intersect/wp/2016/08/19/98-personal-data-points-that-facebook-uses-to-target-ads-to-you/)
* [Opportunity Analysis for Search](https://www.linkedin.com/pulse/opportunity-analysis-search-daniel-tunkelang/)

## Testing

* [A/B Testing for Search is Different](https://medium.com/@dtunkelang/a-b-testing-for-search-is-different-f6b0f6f4d0f5)
* [Discounted cumulative gain](https://en.wikipedia.org/wiki/Discounted_cumulative_gain)
* [Demystifying nDCG and ERR](https://opensourceconnections.com/blog/2019/12/09/demystifying-ndcg-and-err/)
* Evaluating Search (by Daniel Tunkelang) [Measure It](https://medium.com/@dtunkelang/evaluating-good-search-part-i-measure-it-5507b2dbf4f6), [Measuring Searcher Behavior](https://medium.com/@dtunkelang/evaluating-search-measuring-searcher-behavior-5f8347619eb0), [Using Human Judgement](https://medium.com/@dtunkelang/evaluating-search-using-human-judgement-fbb2eeba37d9)
* [When There’s No Conversion Rate](https://medium.com/@dtunkelang/when-theres-no-conversion-rate-67a372666fed)

## Conferences

* [Activate](https://www.activate-conf.com/)
* [Berlin buzzword](berlinbuzzwords.de)
* [Haystack](https://haystackconf.com/)
* [Elastic{ON}](https://www.elastic.co/elasticon/)
* [MIX-CAMP E-COMMERCE SEARCH](http://www.mices.co)

## Books

* [AI-powered search](https://www.manning.com/books/ai-powered-search)
* [Relevant Search](https://www.manning.com/books/relevant-search)
* [Deep Learning for search](https://www.manning.com/books/deep-learning-for-search)
* [Interactions with search systems](https://www.cambridge.org/core/books/interactions-with-search-systems/5B3CF5920355A8B09088F2C409FFABDC)
* [Embeddings in Natural Language Processing. Theory and Advances in Vector Representation of Meaning](http://josecamachocollados.com/book_embNLP_draft.pdf)
* [Search User Interfaces](http://www.searchuserinterfaces.com)
* [Search Patterns](https://searchpatterns.org/)

## Personalies and influencers

* [Daniel Tunkelang (he is God of Search)](https://twitter.com/dtunkelang)
* [Max Irwin](https://twitter.com/binarymax)
* [Doug Turnbull](https://twitter.com/softwaredoug)
* [Baymard’s Institute](https://baymard.com/blog)

## Usecases

* Airbnb - [Machine Learning-Powered Search Ranking of Airbnb Experiences](https://medium.com/airbnb-engineering/machine-learning-powered-search-ranking-of-airbnb-experiences-110b4b1a0789)
* Airbnb - [Listing Embeddings in Search Ranking](https://medium.com/airbnb-engineering/listing-embeddings-for-similar-listing-recommendations-and-real-time-personalization-in-search-601172f7603e)
* Skyscanner - [Learning to Rank for Flight Itinerary Search](https://hackernoon.com/learning-to-rank-for-flight-itinerary-search-8594761eb867)
* [Search at Slack](https://slack.engineering/search-at-slack-431f8c80619e)


