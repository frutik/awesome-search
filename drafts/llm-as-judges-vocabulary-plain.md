# LLM as Judges: A Vocabulary (plain version)

*Nine words people use about AI relevance judges, and what each one actually claims.*

*Last updated: 2026-11-10 21:22 CET*

Papers and blog posts about LLM judges keep using the same few words: agreement, self-consistency, calibration, jury, adjudication.

Each word means something different. "The judge agrees with humans", "the judge is consistent" and "the judge is calibrated" are three separate claims. Each one is tested in its own way, and a judge can pass one test and fail the other two.

I am actively involved in AI-as-judge work in Quepid, so I have to deal with all of this. Below is what each word means, as I understand it, with the evidence behind it.

## Agreement

Agreement is how closely two judges match each other. But "matching" can mean four different things:

1. **Label**: do they give the same grade to the same query and document?
2. **Score**: do they give each search approach about the same score?
3. **Ranking**: do they put the search approaches in the same order?
4. **Decision**: do they lead to the same choice, the same winner, the same "ship it"?

A judge can do well on one of these and badly on another. Think of a tape measure that reads five centimetres short. Every plank it measures comes out wrong, but the longest plank is still the longest. If all you need is to sort the planks, the broken tape measure is fine.

A study on Brazilian legal search (NormasTCU) found exactly this. The AI judge often disagreed with human experts on single documents, yet it put the search systems in almost the same order as the humans did. The opposite also happens. Otero, Parapar and Barreiro found AI judges that ranked systems in roughly the right order overall, but still found significant differences that human judgments did not support, and mixed up the order of the best systems.

So when someone says "the judge agrees with humans", ask: agrees on what?

## Inter-judge agreement

Inter-judge agreement is agreement between two different judges. It only means something once you say which two:

- human and human: is the task clear enough that people agree?
- AI and human: does the model match *this particular* person?
- AI and AI: would another model have answered differently?
- one prompt and another prompt
- a panel of judges and a single judge

(The same judge asked twice is a different thing: self-consistency, below.)

Don't expect perfect agreement. First check how often your own human raters agree with each other. If an AI judge agrees with your reference much more often than your people agree with each other, that is worth a closer look: what is it matching that they are not?

Two warnings. Matching one person is not the same as matching your users. And three AI models that agree with each other may simply share the same blind spot.

## Ordinal and binary agreement

How you grade affects how you should measure agreement.

**Binary** grading has two answers: relevant or not relevant. Every disagreement counts the same. **Ordinal** grading has levels, such as "not relevant, somewhat relevant, relevant, perfect". Here, mixing up "not relevant" with "perfect" is much worse than mixing up two neighbouring levels, and the measurement should count it that way.

A common mistake is to quietly turn graded labels into yes/no. Agreement looks better, but you lose the fine differences that graded search metrics rely on.

Sometimes, though, yes/no is the right choice. In *Better Retrievers, Worse Labels*, judges had to say whether a text contained enough information to answer a question: yes, partly, or no. They agreed poorly overall. On the clear yes and no cases they agreed much better. The disagreement was in the "partly" middle. Part of that improvement is simply that the hardest cases were left out, so agreement depends on which cases you include, not only on the grading scale.

So choose the grading scale that fits the decision you will make with the labels.

## Self-consistency

Self-consistency means the judge agrees with itself: the same model and the same prompt, asked more than once about the same pair.

It shows the judge is stable, not that it is correct. A judge can give the same wrong answer every time. Its advantage is that you need no human labels to check it, so it is cheap. Etsy asks its AI judge several times and is exploring using that to send only the hard cases to people.

## Qrels

"Qrels" is the search-evaluation word for a judgment list: a query, a document, and a grade. It belongs here because a judgment list is what an AI judge *produces*. Every kind of agreement above compares two such lists.

One trap gets worse as search gets better. A document that is not in the list was *never judged*. That does not make it irrelevant, even though most evaluation tools count it as irrelevant. *Better Retrievers, Worse Labels* showed this. A common shortcut says "none of the known good documents was found, so there is not enough information to answer". With weak search, the shortcut was often right. With strong search it was mostly wrong, because the search found useful documents that nobody had ever judged.

The fix is to judge each result by what it actually says. That is exactly the job an AI judge can do.

## Adjudication

Adjudication is how disagreements get settled: a vote, or an expert who makes the final call. Allegro, for example, had two people grade each pair without seeing each other's answers, and an expert decided whenever they disagreed.

*Learning* to adjudicate means training the decider instead of writing fixed rules. The idea comes from a 2026 paper by Shu et al. that proposes a system called CADRE. Three specialist AI agents look at the product details, what the shopper wants, and the business rules. A trained final judge then makes the decision, and starts a debate between the specialists only when they disagree.

The trained final judge was more accurate than any single specialist. It sometimes got cases right that every specialist got wrong. The debate itself helped very little.

Doug Turnbull showed a smaller version of the same idea: several simple AI judges, each checking one thing, with a basic machine-learning model learning how much to trust each of them.

## Distilled student

A distilled student is a small, cheap model trained to copy a big, expensive judge (the teacher). It makes judging affordable for a whole catalogue or for live search.

Etsy uses a chain of three: a big AI model labels data, a teacher model learns from it, and a small, fast student model learns from the teacher. Each step is a little less accurate than the one before. CADRE's student became more accurate when its training included the reasoning as well as the labels.

The risk is that the student copies the teacher's mistakes as faithfully as its good answers, and then repeats them at large scale. So check the student against people, not only against the teacher.

I wrote about training one myself in *Teaching a Small Model to Judge Like Amazon*.

## Calibration

"Calibration" has two meanings here, and people mix them up all the time.

**Judge calibration** means checking an AI judge against people you trust, on a fixed set of examples, for each prompt and each collection, and then fixing the prompt, the grading rules or the model where it goes wrong. Check both whether it gives the same labels as the people and whether it puts search systems in the same order. Good order with poor labels is the tape-measure case.

**Probability calibration** means that when the judge says "70% sure", it is right about 70% of the time. A rule like "send anything the judge is unsure about to a person" can work even without this, as long as low confidence really does point to more mistakes. Check that. Calibration is what lets you take the judge's confidence number at face value.

## Jury

A jury is a group of judges whose answers are combined into one: different models, different prompts, or simple judges that each look at one thing.

Two 2026 papers show where juries go wrong.

**A jury of weak judges is still weak.** In *Better Retrievers, Worse Labels*, a jury of four small AI models often disagreed among themselves. Even so, together they still reached the paper's main conclusion. Weak judges can be good enough to show the general direction, while being unreliable on any single label.

**Keep judges independent until you combine them.** In CADRE, letting the specialists see each other's answers made the final result worse. The judges started to copy each other and stopped bringing the different views that made a group worth having.

A jury is only as independent as its members. Judges built on the same base model can be wrong in the same way at the same time, and CADRE's specialists all share one base model. Jury members agreeing with each other is inter-judge agreement. The same jury giving the same answer when asked again is self-consistency. Neither replaces a check against people.

## How the words fit together

A judge, or a jury of judges, produces a judgment list. Self-consistency tells you the judge is stable. Agreement tells you whether it matches a reference, once you say on what and on which grading scale. Calibration is that check done carefully before you trust the judge. Disagreements are settled, by people or by a trained decider. A distilled student then copies the result cheaply, along with any mistakes it inherited.

None of these words means "the judge is right". Each one covers a single, narrower claim.

## References

- [NormasTCU — A Brazilian Portuguese IR Dataset and an Evaluation of LLM-as-a-Judge for Relevance Assessment (arXiv, 2026)](https://arxiv.org/abs/2608.27746)
- [Limitations of Automatic Relevance Assessments with Large Language Models for Fair and Reliable Retrieval Evaluation — David Otero, Javier Parapar, Álvaro Barreiro (SIGIR 2025)](https://arxiv.org/abs/2411.13212)
- [Better Retrievers, Worse Labels: How Incomplete Relevance Judgments Distort Abstention Evaluation in Conversational RAG — Ivan Kochergin, Vasily Konovalov (arXiv, 2026)](https://arxiv.org/abs/2610.40966)
- [Learning to Adjudicate: Verifier-Guided Multi-Agent Reasoning for E-Commerce Relevance — Shi Shu et al. (arXiv, 2026)](https://arxiv.org/abs/2611.02758)
- [Automating Search Relevance Assessment at Scale with LLM-as-a-Judge — Joanna Marhula, Mateusz Sidor, Allegro](https://blog.allegro.tech/2026/08/automating-search-relevance-llm-as-a-judge.html)
- [How Etsy Uses LLMs to Improve Search Relevance — Etsy Code as Craft](https://www.etsy.com/codeascraft/how-etsy-uses-llms-to-improve-search-relevance)
- [Teaching a Small Model to Judge Like Amazon — Andrew Kornilov (Medium)](https://medium.com/@frutik/teaching-a-small-model-to-judge-like-amazon-94e69829e6b4)
- [Classic ML to Cope with Dumb LLM Judges — Doug Turnbull](https://softwaredoug.com/blog/2025/01/21/llm-judge-decision-tree)
