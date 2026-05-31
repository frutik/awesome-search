---
title: "Relevance feedback"
source: "https://en.wikipedia.org/wiki/Relevance_feedback"
author:
  - "[[Wikipedia]]"
published: 2006-07-04
created: 2026-05-31
description:
tags:
  - "clippings"
---
**Relevance feedback** is a feature of some [information retrieval](https://en.wikipedia.org/wiki/Information_retrieval "Information retrieval") and [recommender](https://en.wikipedia.org/wiki/Recommender_system "Recommender system") systems. The idea behind relevance feedback is to take the results that are initially returned from a given query, to gather user [feedback](https://en.wikipedia.org/wiki/Feedback "Feedback"), and to use information about whether or not those results are relevant to perform a new query. We can usefully distinguish between three types of feedback: explicit feedback, implicit feedback, and blind or "pseudo" feedback.

## Explicit feedback

Explicit feedback is obtained from assessors of relevance indicating the relevance of a document retrieved for a query. This type of feedback is defined as explicit only when the assessors (or other users of a system) know that the feedback provided is interpreted as [relevance](https://en.wikipedia.org/wiki/Relevance_\(information_retrieval\) "Relevance (information retrieval)") judgments.

Users may indicate relevance explicitly using a *binary* or *graded* relevance system. Binary relevance feedback indicates that a document is either relevant or irrelevant for a given query. Graded relevance feedback indicates the relevance of a document to a query on a scale using numbers, letters, or descriptions (such as "not relevant", "somewhat relevant", "relevant", or "very relevant"). Graded relevance may also take the form of a cardinal ordering of documents created by an assessor; that is, the assessor places documents of a result set in order of (usually descending) relevance. An example of this would be the [SearchWiki](https://en.wikipedia.org/wiki/SearchWiki "SearchWiki") feature implemented by [Google](https://en.wikipedia.org/wiki/Google "Google") on their search website.

The relevance feedback information needs to be interpolated with the original query to improve retrieval performance, such as the well-known [Rocchio algorithm](https://en.wikipedia.org/wiki/Rocchio_algorithm "Rocchio algorithm").

A [performance metric](https://en.wikipedia.org/wiki/Figure_of_merit "Figure of merit") which became popular around 2005 to measure the usefulness of a ranking [algorithm](https://en.wikipedia.org/wiki/Algorithm "Algorithm") based on the explicit relevance feedback is [normalized discounted cumulative gain](https://en.wikipedia.org/wiki/Discounted_cumulative_gain#Normalized_DCG "Discounted cumulative gain"). Other measures include [precision](https://en.wikipedia.org/wiki/Precision_\(information_retrieval\) "Precision (information retrieval)") at *k* and [mean average precision](https://en.wikipedia.org/wiki/Mean_average_precision#Mean_average_precision "Mean average precision").

## Implicit feedback

Implicit feedback is inferred from user behavior, such as noting which documents they do and do not select for viewing, the duration of time spent viewing a document, or page browsing or scrolling actions.[^1] [^2] There are many signals during the search process that one can use for implicit feedback and the types of information to provide in response.[^3] [^4]

The key differences of implicit relevance feedback from that of explicit include:[^5]

1. The user is not assessing relevance for the benefit of the IR system, but only satisfying their own needs and
2. The user is not necessarily informed that their behavior (selected documents) will be used as relevance feedback

An example of this is [dwell time](https://en.wikipedia.org/wiki/Dwell_time_\(information_retrieval\) "Dwell time (information retrieval)"), which is a measure of how long a user spends viewing the page linked to in a search result. It is an indicator of how well the search result met the query intent of the user, and is used as a feedback mechanism to improve search results.

## Pseudo relevance feedback

Pseudo relevance feedback, also known as blind relevance feedback, provides a method for automatic local analysis. It automates the manual part of relevance feedback, so that the user gets improved retrieval performance without an extended interaction. The method is to do normal retrieval to find an initial set of most relevant documents, to then assume that the top "k" ranked documents are relevant, and finally to do relevance feedback as before under this assumption. The procedure is:

1. Take the results returned by initial query as relevant results (only top k with k being between 10 and 50 in most experiments).
2. Select top 20-30 (indicative number) terms from these documents using for instance [tf-idf](https://en.wikipedia.org/wiki/Tf-idf "Tf-idf") weights.
3. Do [query expansion](https://en.wikipedia.org/wiki/Query_expansion "Query expansion"), add these terms to query, and then match the returned documents for this query and finally return the most relevant documents.

Some experiments such as results from the Cornell SMART system published in (Buckley et al.1995), show improvement of retrieval systems performances using pseudo-relevance feedback in the context of TREC 4 experiments.

This automatic technique mostly works. Evidence suggests that it tends to work better than global analysis.[^6] Through a query expansion, some relevant documents missed in the initial round can then be retrieved to improve the overall performance. Clearly, the effect of this method strongly relies on the quality of selected expansion terms. It has been found to improve performance in the TREC ad hoc task. But it is not without the dangers of an automatic process. For example, if the query is about copper mines and the top several documents are all about mines in Chile, then there may be query drift in the direction of documents on Chile. In addition, if the words added to the original query are unrelated to the query topic, the quality of the retrieval is likely to be degraded, especially in Web search, where web documents often cover multiple different topics. To improve the quality of expansion words in pseudo-relevance feedback, a positional relevance feedback for pseudo-relevance feedback has been proposed to select from feedback documents those words that are focused on the query topic based on positions of words in feedback documents.[^7] Specifically, the positional relevance model assigns more weights to words occurring closer to query words based on the intuition that words closer to query words are more likely to be related to the query topic.

Blind feedback automates the manual part of relevance feedback and has the advantage that assessors are not required.

## Using relevance information

Relevance information is utilized by using the contents of the relevant documents to either adjust the weights of terms in the original query, or by using those contents to add words to the query. Relevance feedback is often implemented using the [Rocchio algorithm](https://en.wikipedia.org/wiki/Rocchio_algorithm "Rocchio algorithm").

## References

[^1]: Jannach, Dietmar; Lerche, Lukas; Zanker, Markus (2018), Brusilovsky, Peter; He, Daqing (eds.), ["Recommending Based on Implicit Feedback"](https://link.springer.com/chapter/10.1007/978-3-319-90092-6_14), *Social Information Access: Systems and Technologies*, Cham: Springer International Publishing, pp. 510–569, [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.1007/978-3-319-90092-6\_14](https://doi.org/10.1007%2F978-3-319-90092-6_14), [ISBN](https://en.wikipedia.org/wiki/ISBN_\(identifier\) "ISBN (identifier)") [978-3-319-90092-6](https://en.wikipedia.org/wiki/Special:BookSources/978-3-319-90092-6 "Special:BookSources/978-3-319-90092-6"), retrieved 2025-05-20

[^2]: ["Archived copy"](https://web.archive.org/web/20040316204714/http://www.scils.rutgers.edu/etc/mongrel/kelly-belkin-SIGIR2001.pdf) (PDF). *www.scils.rutgers.edu*. Archived from [the original](http://www.scils.rutgers.edu/etc/mongrel/kelly-belkin-SIGIR2001.pdf) (PDF) on 16 March 2004. Retrieved 12 January 2022.

[^3]: Jansen, B. J. and McNeese, M. D. 2005. [Evaluating the effectiveness of and patterns of interactions with automated assistance in IR systems](https://faculty.ist.psu.edu/jjansen/academic/pubs/jansen_assistance_jasist2005.pdf). Journal of the American Society for Information Science and Technology. 56(14), 1480-1503

[^4]: Kelly, Diane, and Jaime Teevan. " [Implicit feedback for inferring user preference: a bibliography](http://vladoyak.aspone.cz/articles/Kelly%20-%20Introduction%20Implicit%20Feedback%20for%20Inferring%20User%20Preference.pdf)." ACM SIGIR Forum. Vol. 37. No. 2. ACM, 2003.

[^5]: ["Archived copy"](https://web.archive.org/web/20070611121933/http://haystack.lcs.mit.edu/papers/kelly.sigirforum03.pdf) (PDF). *haystack.lcs.mit.edu*. Archived from [the original](http://haystack.lcs.mit.edu/papers/kelly.sigirforum03.pdf) (PDF) on 11 June 2007. Retrieved 12 January 2022.

[^6]: Jinxi Xu and W. Bruce Croft, [*Query expansion using local and global document analysis*](http://portal.acm.org/citation.cfm?id=243202), in Proceedings of the 19th annual international ACM SIGIR conference on Research and development in information retrieval (SIGIR), 1996.

[^7]: Yuanhua Lv and ChengXiang Zhai, [*Positional relevance model for pseudo-relevance feedback*](http://portal.acm.org/citation.cfm?id=1835546), in Proceedings of the 33rd international ACM SIGIR conference on Research and development in information retrieval (SIGIR), 2010.