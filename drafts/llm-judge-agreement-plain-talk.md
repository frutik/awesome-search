# Do LLM Judges Actually Agree With Us?

## The short version

People keep asking whether LLM judges "work" for search evaluation. Wrong question. They work fine for some things and fall apart for others, and the whole game is knowing which is which.

One word first: by **"approach"** I mean one version of a search engine — your current ranker, the new one you want to ship instead. The papers all call this a **"system"**; read them as interchangeable. You're always comparing a few and picking one. The judge labels the results, each approach gets a score, they line up best to worst. That line-up is the leaderboard.

Now, the thing nobody tells you up front: **there are four different things you could mean by "the judges agree," and they don't move together.**

1. **Do they slap the same label on the same result?**
2. **Do they give each approach roughly the same score?**
3. **Do they put the approaches in the same order?**
4. **Do they lead you to the same decision — same winner, same "this is significant," same ship-it call?**

You'd assume these rise and fall together. They don't. Two judges can fight over thousands of individual labels and still both say "B beats A beats C" — the noise hits every approach about equally and cancels out. That's the whole reason people got excited: the judge doesn't have to be right about each result, only about which approach wins.

But a matching leaderboard hides a lot: different ideas of what "relevant" means, blowups on specific query types, your top two approaches swapping places, imaginary statistical significance, and a quiet thumb on the scale for certain kinds of retrieval.

So: a real tool you have to check, not a drop-in replacement for people. When someone hands you a study, look for whether they measured both the label level and the decision level, whether they used more than one model, whether they looked at the disagreements instead of averaging them into mush, and whether the conclusion holds for the approaches they actually care about.

And if you're the one shipping it — skip to §6, where I try to answer the question everybody actually has: *what number is good enough?*

## 1. Who's even doing the judging?

Somebody looks at a query and a result and says how good the match is. That somebody can be the person who had the question, a domain expert, a paid assessor or crowd worker, an LLM you asked nicely, or some mix. Which means "judge vs. judge" covers a bunch of different comparisons, answering different questions:

| Who vs. who | What you're really asking |
|---|---|
| Human vs. human | Is this task even objective? Are people swappable? |
| LLM vs. human | Does the model copy this particular human? |
| LLM vs. LLM | Would a different model have told me something else? |
| Prompt vs. prompt | Does my answer survive me rewording the instructions? |
| Same model, run twice | Is it even consistent with itself? |
| Panel vs. one judge | Does averaging help, or just paper over the cracks? |

These are not interchangeable. Matching one human doesn't mean matching users in general. Three LLMs agreeing might just mean three models share the same blind spot. And a model that's consistently wrong is still wrong — consistency isn't correctness.

Figure out which comparison you're making *before* you start quoting agreement scores at people.

## 2. Why anyone wants this: money and time

Let's not be coy about the motivation. The main driver was never accuracy. It was that human judgment is brutally expensive and slow.

Rough numbers for a single query-document judgment:

| | Cost each | Turnaround |
|---|---|---|
| Human assessor | $0.50–$5.00 | days to weeks |
| LLM | ~$0.001–$0.01 | minutes |

Two to three orders of magnitude. A thousand queries with ten candidates each is $5,000–$50,000 and a couple of weeks with people, or tens of dollars and twenty minutes with a model. [Thomas and colleagues](https://arxiv.org/abs/2309.10621) put it plainly — models produced "better labels than third-party workers, for a fraction of the cost." That gap is the whole reason this field exists. It's also why people are motivated to believe the agreement numbers.

**But "cheap per unit" is not the same as "cheap."** At e-commerce scale — billions of searches a year, hundreds of billions of query-product pairs — judging everything with a frontier model isn't expensive, it's *impossible*. So everyone samples: judge a few thousand pairs, generalize. Fine for tracking aggregate quality over time, useless for anything needing coverage. Mining hard negatives across a full catalogue, or catching a regression on one weird tail query — sampling won't find it.

The way out is architectural, and [[Towards Scalable Relevance Engineering|Andreas Wagner]] has the clearest worked version of it — [[searchHub]] sits on upwards of 10 billion searches a year, so this was something they had to solve rather than describe. The first move isn't a cheaper model, it's **judging far less**. Behavioral signals split the pair space before anything runs: results already performing well are the lowest-priority candidates for explicit grading — not confirmed positives, since clicks and purchases are shaped by position, price, brand and availability — while the underperformers are your candidate hard negatives and the ones worth spending on first. Wagner reports that pruning alone clears ~93% of the problem space. No model choice buys you that.

**Then cascade your judges.** Quantized bi-encoders — INT8 `multilingual-e5-large`, `bge-m3` — settle 75–85% of what's left at CPU speed, and only the pairs where they disagree escalate to the full LLM, since disagreement is a decent proxy for genuine difficulty. Two warnings. Two weak judges can be confidently wrong *together*, especially sharing a base model, so audit a sample of what got auto-accepted, not only what got escalated. And the pruning is only as good as the behavioral signal underneath it — if position bias shaped the clicks, it shaped the 93% you then never looked at.

**Then distill.** [[How Etsy Uses LLMs to Improve Search Relevance|Etsy]] runs this: human "golden" labels anchor a big LLM teacher, the teacher scales labeling to millions of query-listing pairs, and a lightweight BERT two-tower student gets distilled out for serving at under 10ms added latency. Humans define what good means, the LLM scales it, the small model serves it — the judge's job is to teach the production model, not to be it. Wagner closes the same loop one level up, on the judge itself: ~100,000 LLM judgments fine-tune a small embedding model down to sub-20ms CPU inference, so the next cycle needs fewer escalations than the last.

One concrete data point from [Allegro](https://blog.allegro.tech/2026/08/automating-search-relevance-llm-as-a-judge.html): moving batch judging from a cloud model to a locally-hosted 4-bit quantized 26B Gemma variant cut inference cost 60% at ~16 query-product pairs per second. But batching a whole product page into one request, which saves money on cloud models, *degraded* local-model reliability badly enough that they reverted to single-item requests. The cost optimizations aren't free and they aren't portable.

## 3. Humans never agreed either

Judges disagreeing is not a new LLM problem. IR people have known relevance is squishy for decades.

[Voorhees showed this back in 2000](https://www.nist.gov/publications/variations-relevance-judgments-and-measurement-retrieval-effectiveness) — swap in a different set of human judgments and lots of individual labels change, but the comparison between approaches mostly holds up. That's the founding insight of the reusable-test-collection idea: everyone doesn't have to agree on everything, as long as the comparison survives.

It only goes so far. [Bailey and co. asked whether judges are actually swappable](https://www.microsoft.com/en-us/research/publication/relevance-assessment-are-judges-exchangeable-and-does-it-matter/) and found it matters a lot who's judging — the person who wrote the topic, a task expert, and a random assessor are not the same thing. Their conclusion: test collections are *not* fully robust to swapping judges who differ a lot in expertise.

Keep this as your baseline. The bar for an LLM isn't "agrees perfectly with one human." It's "lands inside the range humans already vary by, **and** doesn't change the calls you're making."

## 4. How we got here

### 4.1 First look, 2023

[Faggioli and a big crew wrote *Perspectives on Large Language Models for Relevance Judgment*](https://arxiv.org/abs/2304.09161) and laid out a spectrum, from "humans judge, model helps a bit" to "model does the whole thing." Their pilot turned up the pattern that's defined everything since: labels agree only so-so, leaderboards agree a lot.

They also listed the worries — prompt sensitivity, model bias, evaluation eating its own tail, contaminated data, black boxes, and the sneaky one: if a model defines relevance, relevance quietly becomes whatever the model thinks it is. None of those are solved.

### 4.2 Meanwhile, the rest of the world was doing this too

IR isn't the only field that pointed an LLM at a grading task, and the general LLM-as-a-judge crowd got there earlier with better names. [Zheng et al.'s MT-Bench paper](https://arxiv.org/abs/2306.05685) is the reference point: strong judges like GPT-4 "can match both controlled and crowdsourced human preferences well, achieving over 80% agreement, the same level of agreement between humans." Same shape as the IR result — good enough in aggregate, benchmarked against how much humans disagree rather than against perfection.

They named four failure modes everyone now cites: **position bias** (preferring whichever option came first), **verbosity bias** (their "repetitive list" padding attack fooled Claude-v1 and GPT-3.5 over 90% of the time, GPT-4 only 8.7%), **self-enhancement bias**, and **limited reasoning**. All four land in search. Position bias is live the moment you do pairwise judging; verbosity bias is a first cousin of the keyword-stuffing vulnerability in §4.6 — both are the judge reacting to surface form instead of substance.

But here's the thing IR should feel smug about. The general LLM-judge world grades free-text answers where there's often no ground truth at all, so "does the judge agree with humans" is the *only* check available. IR has something better: a downstream question you can actually ask, namely *does the leaderboard come out the same*. That check is why this article can distinguish four levels of agreement instead of one. Don't give it up.

### 4.3 It takes off, 2023–2025

[Thomas and colleagues](https://arxiv.org/abs/2309.10621) wrote up what happened when Bing did relevance labeling with LLMs at scale: accuracy "as good as human labellers," and better than third-party workers when checked against what actual searchers preferred. Read the whole thing though, because they also say this: "Systematic changes to the prompts make a difference in accuracy, but so too do simple paraphrases." Reword your prompt in a way that means the same thing, get a different answer. Sit with that for a second.

[UMBRELA](https://arxiv.org/abs/2406.06519) rebuilt that kind of assessor in the open with GPT-4o across TREC Deep Learning 2019–2023, and its leaderboards tracked the human ones closely — which turned scattered results into something reproducible. Then [*Judging the Judges*](https://arxiv.org/abs/2502.13908) released 42 sets of LLM-generated labels from eight teams, so you could finally compare judges *to each other* instead of each against one fixed human answer key. Three things fell out: how you set up the judge changes the answer a lot; two judges can produce nearly the same leaderboard while labeling things completely differently; and one average agreement number tells you nothing about *which direction* a judge is wrong in.

### 4.4 The big one: TREC 2024 RAG

[Upadhyay and team](https://arxiv.org/abs/2411.08275) ran four assessment processes over the TREC 2024 RAG Track — NIST's full manual process plus three leaning on UMBRELA to varying degrees. 77 runs, 19 teams. On nDCG@20, nDCG@100 and Recall@100, the automated leaderboards lined up closely with the fully manual one.

Two details worth carrying around. Humans were **stricter** than the model. And bolting humans onto the LLM pipelines didn't help — LLM assistance "does not appear to increase correlation with fully manual assessments, suggesting that costs associated with human-in-the-loop processes do not bring obvious tangible benefits."

Strongest pro-automation result out there. But notice what it's testing: ordering 77 wildly different runs. Much easier than telling apart two approaches that are nearly tied.

### 4.5 Why a matching leaderboard isn't the win you think

Here's where it gets uncomfortable.

[Otero, Parapar and Barreiro](https://arxiv.org/abs/2411.13212) zoomed in on the approaches at the top and on pairwise statistical calls. Straight from the abstract: LLM judgments are "unfair at ranking top-performing systems," with "an exceedingly high rate of false positives regarding statistical differences." Translation: the judge will tell you your new approach won, with confidence, when it didn't. If you run A/B-style offline comparisons, that's the sentence that should keep you up.

[Clarke and Dietz](https://arxiv.org/abs/2412.17156) make a point that's obvious once said: an LLM relevance judge is just another relevance-scoring approach. So it can be gamed, and if your retrieval approach and your judge share the same underlying model, you're grading your own homework. They build an example where an approach scores great automatically and gains nothing with real humans.

[Balog, Metzler and Qin](https://arxiv.org/abs/2503.19092) found "the first empirical evidence of LLM judges exhibiting significant bias towards LLM-based rankers" — the judge likes retrieval approaches built like it is. They also hit "limitations in LLM judges' ability to discern subtle system performance differences," and confirm the leniency: LLM judges "are more lenient in their relevance assessments than human judges."

Worth flagging an honest disagreement, because it hasn't settled. [SynDL](https://arxiv.org/abs/2408.16312) — 1,988 queries, 637,063 LLM labels — reports the opposite on that first point: their setup "does not favour language model approaches." Does the judge play favorites? Depends whose experiment you read.

### 4.6 Judges can be tricked

[Alaofi and co.](https://arxiv.org/abs/2501.17969) found LLMs "are more likely to label passages as relevant compared to human judges," and — the good bit — that they're "highly influenced by the presence of query words in the passages under assessment, even if the wider passage has no relevance to the query."

Stuff the query words into a garbage passage, the judge calls it relevant. Some models even followed instructions written *inside the passage they were judging*. Your average agreement score will look perfectly healthy while this is happening.

If you run a marketplace where third parties write the item text and have money riding on ranking, reread that paragraph.

### 4.7 There's no single "LLM judge"

[Arabzadeh and Clarke](https://arxiv.org/abs/2504.12558) compared five ways of asking — binary, graded, pairwise, and two flavors of nugget-based — across TREC DL 2019–2021 and ANTIQUE. *How you ask* changes the answer. "Use an LLM judge" isn't a method, it's a category.

[Farzi and Dietz](https://arxiv.org/abs/2507.09488) break relevance into pieces — exactness, coverage, topicality, contextual fit — and grade each. Better leaderboards, and you can see *why* something got the grade. Some disagreement isn't the judge being dumb; it's you never having said what you meant by relevant.

### 4.8 Now leave the English passage bubble, 2025–2026

Everything above is mostly English web passages. The conclusions don't just come along for the ride.

- [Mohtadi and colleagues](https://arxiv.org/abs/2512.05334) judged full documents vs. LLM-written summaries of them: "comparable stability in systems' ranking," but "systematic shifts in label distributions and biases that vary by model and dataset." Same leaderboard, different labels, again.
- [The TREC Podcast reassessment](https://arxiv.org/abs/2601.05603) is the one to read. Five LLMs, 18,284 query-segment pairs, 91,420 labels. On the 2020 track, human-vs-LLM leaderboard agreement (Kendall's τ) ran 0.81–0.84 and the top approaches held. On 2021 it dropped to 0.60–0.72 and the ordering got, in their words, "much more volatile… including the *top* ranking systems." **Same models, same method, same task — one year apart.** They then took the 22 cases where LLMs and the original assessor disagreed *most* — deliberately selected, not a random sample — and had three IR experts look. The experts sided with the LLMs (Krippendorff's α 0.71–0.86) and showed *negative agreement* with the original assessor (α −0.55 to −0.77, i.e. worse than chance). That doesn't establish the answer key is broadly wrong. It establishes the key can be wrong, and is contestable, on exactly the cases where a judge looks like it's failing.
- [Keller and team](https://arxiv.org/abs/2604.04140) found judges handed nothing but a short query "judge many more documents relevant and have a lower agreement" than judges given a proper topic description. Writing that description *automatically* still helps — cheap fix, real gain.
- [NormasTCU](https://arxiv.org/abs/2608.27746) does Brazilian Portuguese legal search over 14,469 documents. Agreement with humans was only fair-to-moderate (Cohen's κ 0.32–0.53, MAE 0.46–0.66 on a 0–2 scale). And yet nDCG@10 and MRR leaderboards still hit Kendall correlations of 0.90 or better, while P@10 and R@10 were shakier. Cleanest demo you'll find that label agreement, ranking agreement, and *which metric you picked* are three separate things.

### 4.9 What about products? Because that's where the money is

Almost all the evidence above is TREC passages, podcast transcripts and legal documents. If you work on e-commerce search, the honest answer to "does this transfer" is: *the shape transfers, the failure location moves.*

**Relevance isn't topicality any more.** In web search a passage is on-topic or it isn't. In product search the useful grading is about substitutability — the [ESCI scale](https://arxiv.org/abs/2206.06588) (Exact / Substitute / Complement / Irrelevant) is the common shape. That's a different cognitive task, and it moves the hard boundary. Not "relevant vs. not," but "is this a substitute or a complement" — a judgment about shopping intent, not about text.

**And that's exactly where the judges fall over.** Allegro's RAT framework is the best-documented case: a 380K+ multilingual judgment dataset built by 30 experts across 13 departments and four languages, dual blind annotation with expert arbitration. Their local quantized judge reached a quadratic-weighted Cohen's κ of 0.69 on Polish — genuinely good for a four-level ordinal scale. Break it down by class, though, and you get F1 around 0.94 on exact matches and 0.83 on complements, against **0.51 and 0.33** on separating "highly substitutable" from "substitutable."

Careful with those two sets of numbers: an overall weighted κ and a per-class F1 are different quantities on different scales, and F1 has no universal chance baseline — 0.33 does *not* mean "coin flip." What it means is poor discrimination on the boundary the merchandising team actually argues about, while the judge is excellent on the calls nobody needed help with. An overall κ of 0.69 would never have told you.

**Prompting folklore doesn't survive contact with the domain either.** Allegro found that removing few-shot examples *improved* both accuracy and inter-rater agreement — the opposite of what everyone assumes. What helped instead was structured reasoning and domain-specific business logic written into the prompt. Adding category and department metadata did nothing, because product names already carried it.

**Relevance in commerce is time-varying and business-defined.** Etsy maintains an evolving labeling guideline because relevance drifts with culture: "face masks" meant costume masks before 2020 and protective masks after. There's no stable ground truth to converge on — the target moves, and your judge is frozen at its training cutoff.

Notice what industry does that the academic papers mostly don't: in the best-documented commercial deployments, the LLM is not the final judge. Etsy anchors it with human golden labels and distills it into a servable model. Allegro built a 380K human dataset *first* and used it to validate. [eBay](https://arxiv.org/abs/2505.04209) ties the whole thing back to revenue, and their framing is the one to steal — an LLM judge works as a proxy for seller judgment *provided* you bind it to "a meticulous evaluation framework grounded in business metrics." The pattern is **humans define the standard, the LLM scales it, business metrics keep it honest** — a more modest claim than "LLM judges match humans," and a more useful one.

## 5. What to actually measure

There's no one number. Pick a few that match what you're using the judge for.

| Level | The question | What to compute | Where it lies to you |
|---|---|---|---|
| Raw labels | Same grade, same item? | Accuracy, raw agreement | Looks great when 90% of things are non-relevant |
| Chance-corrected | Agreement beyond luck | Cohen's / Fleiss' κ, Krippendorff's α | Moves around with class balance |
| Graded labels | How far off, and which way? | Weighted κ, ordinal α, MAE | An average hides one-sided errors |
| Per class | Which distinctions can it make? | Confusion matrix, per-class precision / recall / F1 | F1 has no chance baseline — don't read it as accuracy |
| Judge vs. judge | Same ordering of items? | Spearman, Kendall | Correlation isn't agreement — one judge can sit a whole grade higher |
| Same judge twice | Is it stable? | Test-retest, label entropy, variance | Stable ≠ right |
| Approach scores | Same score for my approach? | Correlation, calibration plots, score bias | Great correlation with every score inflated |
| Leaderboard | Same order? | Kendall's τ, top-weighted measures | Overall τ hides your top two swapping |
| Actual decisions | Same call? | Win/loss/tie agreement, significance confusion matrix, Type I/II errors | Needs enough topics and a real test protocol |

Three rules fall out of that table.

**Don't quietly collapse graded labels to binary.** Or if you do, report both. Squashing 0/1/2/3 into relevant/not manufactures agreement and throws away exactly the distinctions nDCG cares about.

**Never post a κ without the label distribution and confusion matrix next to it.** A judge that's lenient across the board can have a perfectly normal κ. The leniency is the thing that'll bite you.

**Leaderboard correlation needs a top-weighted companion.** Nobody cares whether the judge can tell a terrible approach from a great one. You care about the three candidates that are nearly tied. Look there.

## 6. So what number is good enough?

The question everybody actually has, and almost no paper answers. Here's the honest attempt.

### The two conventions people quote at you

**Kendall's τ ≥ 0.9.** From Voorhees, who proposed that two evaluation schemes correlating at 0.9 or above be treated as equivalent — partly on the grounds that you can't really be more precise than that. Below about 0.8 you're seeing genuine reordering, not just neighbours swapping. Sensible convention, the field's default for twenty-odd years. It is *a convention*, not a law of nature, and nobody has re-derived it for LLM judges.

**Cohen's κ bands.** Fair 0.21–0.40, moderate 0.41–0.60, substantial 0.61–0.80. These come from a 1977 biometrics paper (Landis and Koch), have nothing to do with IR, and were made up as a convenience. Use them as vocabulary, not as a gate.

### Which one is the gate depends on the decision

NormasTCU is the cautionary tale. Their leaderboards cleared τ ≥ 0.9. Their labels sat at κ 0.32–0.53 — "fair to moderate," which is to say not good. Passing the ranking threshold told them nothing about whether the labels were any good, and passing a label threshold would have told them nothing about the ranking.

So measure both, then decide which is the gate based on how the judgments will be used. If all you want is a broad ranking of approaches, stable decision agreement can be enough even with mediocre label agreement — that's the Voorhees insight, still standing. But if the labels will be read by humans, reused as training data, or used to diagnose specific queries, weak label agreement is disqualifying on its own, and no amount of leaderboard correlation rescues it.

Meanwhile Podcast 2021 came in at τ 0.60–0.72, well under 0.8 — squarely in "these schemes have different emphases" territory. Same method that scored 0.81–0.84 the year before.

### A rubric that depends on the decision

*My synthesis, not something you can cite — but it follows from the evidence above.*

| What you're using it for | Bar to clear | Why |
|---|---|---|
| Tracking quality over time, broad regression detection | τ ≥ 0.9 on your headline metric, κ ≥ 0.4, label distribution sanity-checked | Errors are stable across runs; you're watching the delta, not the level |
| Ranking a diverse field of candidate approaches | Same, plus top-weighted agreement | Overall τ hides exactly the region you care about |
| Choosing between two close approaches / declaring a winner | **High aggregate correlation alone cannot validate this decision** | Otero's false positives happen *at high τ*. Adjudicate the deciding slice with humans |
| Generating training labels | Confusion matrix plus per-class precision / recall / F1 on the boundary you care about | Allegro: overall κ 0.69, F1 0.33 on the distinction that mattered |
| Judging content you don't control | Add adversarial tests before any threshold | Alaofi: keyword stuffing passes a healthy-looking judge |

### Three practical rules worth more than any threshold

**Report per class, not just overall.** Publish the confusion matrix and per-class precision, recall and F1 next to whatever single number you quote. The Allegro spread is the whole argument. If you want a chance-corrected per-class figure, compute a one-vs-rest binary κ and say explicitly that's what it is — don't line per-class F1 up against an overall κ as though they were the same scale.

**Measure your pipeline's run-to-run variation first.** Run the whole judging process several times and recompute the *final metrics and decisions*, not just the labels. The spread across those repeated evaluations estimates your pipeline's stochastic uncertainty. If the difference between two approaches is routinely reversed or swallowed by that spread, the judge cannot reliably distinguish them, however good the correlation with humans looks. This is not the same as the judge's label self-disagreement rate — an 8% label flip rate and a 0.015 nDCG gap are different quantities on different scales, so you have to propagate the variation through to the metric before comparing. Most teams never check. It takes one afternoon and tells you the resolution of your instrument.

**Set the bar against human-human agreement on your own data, not against 1.0.** MT-Bench's framing is right: GPT-4's ~80% agreement was reported as meaningful precisely because that's "the same level of agreement between humans." If your own annotators agree at κ 0.6, demanding κ 0.8 from a model is incoherent. Measure your humans first, then you know what to ask for.

## 7. How to run this properly

Don't crown one model as The Judge. Cross it.

**Your judges**

- Ideally three or more different model families. Three versions of one vendor's model doesn't count.
- Run each judgment more than once. Temperature 0 is not determinism — and this is how you get the run-to-run variation from §6.
- Keep humans in it, several of them, on a stratified slice. You need human-human agreement to know what to ask of the model.
- Write down the model version, access date, exact prompt, decoding settings, and how you truncated documents. You will not remember in four months.

**Your sample**

- Stratify: query type, difficulty, ambiguity, domain, result length, original grade.
- Load up on the close calls. Obviously-relevant and obviously-garbage teach you nothing — and they're where your headline accuracy comes from.
- Pull results from different *kinds* of retrieval approaches, or you're only measuring agreement on one family.
- Throw in dirty tricks: query-word stuffing, instructions hidden in the text, misleading summaries, very long documents. If third-party sellers write your item text, this isn't paranoia, it's a threat model.
- If you swap the order of options in pairwise judging, do it systematically. Position bias is real and cheap to measure.

**Your analysis** — report all three layers, not just the flattering one. **Items:** label distributions, confusion matrices, weighted agreement, direction of error, and per-class breakdowns. **Systems:** score bias, leaderboard correlation, top-weighted agreement, how far the leaders moved. **Decisions:** who won, pairwise significance, effect direction, whether the gap is big enough to care about.

Then take the disagreements and have someone review them blind. Not to declare a winner — to *sort* them. Ambiguous topic? Missing context? Human error? Model error? Different reading of the scale? Gamed content? Or two genuinely defensible ideas of what relevant means? Those need different fixes.

## 8. Still open

- What happens to your evaluation when the judge model gets deprecated and you swap in a new one?
- Which disagreements actually change a decision? Most probably don't. And how do you model agreement when there are several legitimate answers?
- How do you catch someone gaming the judge — especially when they write the item text and profit from ranking?
- When should humans judge everything, versus review disagreements, versus audit a sample, versus just write the criteria?
- Does cascade-and-distill preserve the judge's *biases* along with its accuracy? What a distilled student inherits is barely studied — and the cascade numbers above (~93% pruned, 75–85% auto-settled) are one team's production figures, reported by the author, with nobody having replicated them elsewhere.
- How do you evaluate against a target that moves — commerce relevance shifts with season, culture and stock, and your judge's training data doesn't?

## 9. Where that leaves you

Pulling the evidence together, seven things look solid enough to build on:

1. **Label agreement is never great.** Fair-to-moderate is normal, moving with the collection, the model, the prompt, the grading scale, the context you gave, and who the humans were. Better happens when the task is tightly specified.
2. **Leaderboards hold up better than labels.** Item-level errors cancel out or hit every approach equally, and the ordering survives — but that's a result about *one level, one metric, one collection*, not proof that judges are interchangeable.
3. **It breaks exactly where you need it most.** Sorting a messy pile of 77 runs: fine. Telling apart two strong approaches that are close: not fine. Separating exact matches from garbage: fine. Separating a substitute from a slightly-worse substitute: weak. Your overall number can look terrific while the winner flips and your significance tests fire off false positives.
4. **The errors have a shape.** Too generous, over-reacting to query words, twitchy about prompt wording, following instructions embedded in documents, preferring whatever came first, preferring longer text, possibly favoring approaches that look like themselves (SynDL disputes that one). Because it's systematic, **collecting more labels from the same judge does not wash it out.**
5. **The humans aren't a gold standard either.** When your LLM disagrees with the answer key, "the LLM screwed up" is one hypothesis, not the conclusion. Sometimes the key is contestable; sometimes the item is genuinely ambiguous.
6. **Model-vs-model is under-studied.** Most papers nail human judgments to the wall as truth and ask which LLM gets closest. Comparatively few cross several model families, several prompts, and repeated runs, then ask the real question: *would my conclusion have changed if I'd picked a different judge?*
7. **In the documented industry deployments, nobody replaced the humans.** Etsy, Allegro and eBay all use humans to define the standard, the LLM to scale it, and business metrics to keep it honest. The academic question is "can the model replace the assessor." The deployed answer is "no, it multiplies them" — not a consolation prize, the actual value.

So the honest position is a middle one, and it's not a cop-out. LLM judges are genuinely useful right now: scaling up assessment, extending pools, fast exploratory evaluation, auditing your existing human labels. On several collections they reproduce broad leaderboards remarkably well, for a rounding error of the cost.

But agreement is conditional. A strong correlation does not buy you interchangeable labels, fair treatment of your best approaches, trustworthy significance tests, or protection from someone gaming the thing. And the closer you get to the decision you actually care about — this approach or that one, this substitute or that one — the less the reassuring aggregate numbers apply.

So stop asking:

> Does the LLM agree with the human?

Start asking:

> If I swap the judge, the prompt, or just run it again — which of my conclusions survive, and which ones move?

That's a question you can actually answer. And it treats disagreement as information about your evaluation, which is what it is.

## Worth reading

| Paper | Why |
|---|---|
| [Voorhees (2000)](https://www.nist.gov/publications/variations-relevance-judgments-and-measurement-retrieval-effectiveness) | Humans disagreed first; comparisons survived it. Origin of the τ ≥ 0.9 convention |
| [Bailey et al. (2008)](https://www.microsoft.com/en-us/research/publication/relevance-assessment-are-judges-exchangeable-and-does-it-matter/) | Expertise matters; judges aren't swappable |
| [Zheng et al. (2023)](https://arxiv.org/abs/2306.05685) | MT-Bench: >80% agreement, and the names for position/verbosity/self-enhancement bias |
| [Thomas et al. (2024)](https://arxiv.org/abs/2309.10621) | It works at Bing scale — and paraphrasing your prompt moves the numbers |
| [UMBRELA (2024)](https://arxiv.org/abs/2406.06519) | Open reproduction, validated across five TREC years |
| [Upadhyay et al. (2024)](https://arxiv.org/abs/2411.08275) | 77 runs, 19 teams; humans stricter, human-in-the-loop didn't pay |
| [Otero et al. (2025)](https://arxiv.org/abs/2411.13212) | Unfair at the top, and inventing significance |
| [Judging the Judges (2025)](https://arxiv.org/abs/2502.13908) | 42 judgment sets, so you can compare judges to judges |
| [Balog et al. (2025)](https://arxiv.org/abs/2503.19092) | Judges favor LLM rankers, miss small gaps, grade generously |
| [Alaofi et al. (2025)](https://arxiv.org/abs/2501.17969) | Keyword stuffing and hidden instructions fool the judge |
| [Podcast reassessment (2026)](https://arxiv.org/abs/2601.05603) | Two adjacent years, very different agreement — and the answer key can be wrong |
| [NormasTCU (2026)](https://arxiv.org/abs/2608.27746) | Portuguese legal search: weak labels, strong rankings, metric-dependent |
| [[How Etsy Uses LLMs to Improve Search Relevance\|Etsy Code as Craft]] | Golden labels → LLM teacher → distilled student under 10ms |
| [Allegro RAT](https://blog.allegro.tech/2026/08/automating-search-relevance-llm-as-a-judge.html) | 380K multilingual judgments; κ 0.69 overall, F1 0.33 where it counted |
| [[Towards Scalable Relevance Engineering\|Andreas Wagner]] | Judge *economics* rather than judge quality: prune 93%, cascade the rest, distill what's left |

Also useful, more specialised: [Faggioli et al. (2023)](https://arxiv.org/abs/2304.09161) (the collaboration spectrum and the worry list), [LLMJudge (2024)](https://arxiv.org/abs/2408.08896), [SynDL (2024)](https://arxiv.org/abs/2408.16312) (says judges *don't* favor LM approaches), [Clarke & Dietz (2024)](https://arxiv.org/abs/2412.17156) (your judge is a ranker too), [Arabzadeh & Clarke (2025)](https://arxiv.org/abs/2504.12558) (how you ask changes the answer), [Mehrdad et al. (2024)](https://arxiv.org/abs/2406.00247) and [LREF (2025)](https://arxiv.org/abs/2503.09223) (product-search frameworks), [eBay keyphrase judgments (2025)](https://arxiv.org/abs/2505.04209), [Farzi & Dietz (2025)](https://arxiv.org/abs/2507.09488), [Mohtadi et al. (2025)](https://arxiv.org/abs/2512.05334) and [Keller et al. (2026)](https://arxiv.org/abs/2604.04140).
