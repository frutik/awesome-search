# Do LLM Judges Actually Agree With Us?

## The short version

People keep asking whether LLM judges "work" for search evaluation. Wrong question. They work fine for some things and fall apart for others, and the whole game is knowing which is which.

One word first: by **"approach"** I mean one version of a search engine — your current ranker, the new one you want to ship instead. The papers all call this a **"system"**; same thing, read them as interchangeable. You're always comparing a few and picking one. The judge labels the results, each approach gets a score, they line up best to worst. That line-up is the leaderboard.

Now, the thing nobody tells you up front: **there are four different things you could mean by "the judges agree," and they don't move together.**

1. **Do they slap the same label on the same result?**
2. **Do they give each approach roughly the same score?**
3. **Do they put the approaches in the same order?**
4. **Do they lead you to the same decision — same winner, same "this is significant," same ship-it call?**

You'd assume these rise and fall together. They don't. Two judges can fight over thousands of individual labels and still both say "B beats A beats C" — the noise hits every approach about equally and cancels out. That's the whole reason people got excited: the judge doesn't have to be right about each result, only about which approach wins.

But a matching leaderboard can hide a lot: different ideas of what "relevant" means, blowups on specific query types, your top two approaches swapping places, imaginary statistical significance, and a quiet thumb on the scale for certain kinds of retrieval.

So: LLM judges are a real tool that you have to check, not a drop-in replacement for people. If someone hands you a study, look for whether they measured both the small stuff and the downstream stuff, whether they used more than one model, whether they actually looked at the disagreements instead of averaging them into mush, and whether the conclusion holds for the approaches they actually care about.

And if you're the one shipping it — skip to §6, where I try to answer the question everybody actually has: *what number is good enough?*

## 1. Who's even doing the judging?

Somebody looks at a query and a result and says how good the match is. That somebody can be:

- the person who had the question in the first place
- an expert in the domain
- a paid assessor or crowd worker
- an LLM you asked nicely
- some mix of people and models

Which means "judge vs. judge" can mean a bunch of different comparisons, and they answer different questions:

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

Let's not be coy about the motivation. Nobody adopted LLM judges because they're more accurate. They adopted them because human judgment is brutally expensive and slow.

Rough numbers for a single query-document judgment:

| | Cost each | Turnaround |
|---|---|---|
| Human assessor | $0.50–$5.00 | days to weeks |
| LLM | ~$0.001–$0.01 | minutes |

That's two to three orders of magnitude. A thousand queries with ten candidates each is $5,000–$50,000 and a couple of weeks with people, or a coffee and twenty minutes with a model. [Thomas and colleagues](https://arxiv.org/abs/2309.10621) put it plainly — models produced "better labels than third-party workers, for a fraction of the cost."

That gap is the whole reason this field exists. It's also why people are motivated to believe the agreement numbers.

**But "cheap per unit" is not the same as "cheap."** This is where a lot of teams get ambushed. At e-commerce scale — billions of searches a year, hundreds of billions of query-product pairs — judging everything with a frontier model isn't expensive, it's *impossible*. So everyone samples: judge a few thousand pairs, generalize. Which is fine for tracking aggregate quality over time, and useless for anything that needs coverage. Mining hard negatives across a full catalogue? Catching a regression on one weird query in the tail? Sampling won't find it.

The way out is architectural, and two patterns have settled in:

**Cascade your judges.** Prune the pair space with behavioral signals first. Let cheap quantized models settle the easy majority. Escalate only the pairs where the cheap judges disagree — disagreement turns out to be a decent proxy for genuine difficulty. Send just those to the expensive model. Two warnings that come with this: two weak judges can be confidently wrong *together*, especially if they share a base model, so audit a sample of what got auto-accepted, not only what got escalated. And the escalation rate is a knob that trades money against quality on exactly the hard cases you built the thing for.

**Then distill.** Turn the LLM's judgments into training data and fine-tune something small on them. [Etsy](https://www.etsy.com/codeascraft/how-etsy-uses-llms-to-improve-search-relevance) runs this: human "golden" labels anchor a big LLM teacher, the teacher scales labeling to millions of query-listing pairs, and a lightweight BERT two-tower student gets distilled out for real-time serving at under 10ms added latency. Humans define what good means, the LLM scales it, the small model serves it.

Latency splits into two completely different problems, by the way, and people conflate them constantly. **Offline evaluation** is a batch job — you don't care if it takes six hours overnight. **Production relevance filtering** has a single-digit-millisecond budget and a frontier LLM is simply not in the running. The judge and the production model are different animals; the judge's job is to teach the production model, not to be it.

One nice concrete data point on the economics from [Allegro](https://blog.allegro.tech/2026/08/automating-search-relevance-llm-as-a-judge.html): moving their batch judging workload from a cloud model to a locally-hosted 4-bit quantized 26B Gemma variant cut inference cost 60% and got them ~16 query-product pairs per second, 2.5× the throughput of a 12B version. And a wrinkle worth knowing — batching a whole product page into one request saves money on cloud models but *degrades* local-model reliability, so they had to revert local inference to single-item requests. The cost optimizations aren't free and they aren't portable.

## 3. Humans never agreed either

Worth remembering: judges disagreeing is not some new LLM problem. IR people have known relevance is squishy for decades.

[Voorhees showed this back in 2000](https://www.nist.gov/publications/variations-relevance-judgments-and-measurement-retrieval-effectiveness) — swap in a different set of human judgments and lots of individual labels change, but the comparison between approaches mostly holds up. That's the founding insight of the whole reusable-test-collection idea: everyone doesn't have to agree on everything, as long as the comparison between approaches survives.

It only goes so far, though. [Bailey and co. asked whether judges are actually swappable](https://www.microsoft.com/en-us/research/publication/relevance-assessment-are-judges-exchangeable-and-does-it-matter/) and found that it matters a lot who's judging — the person who wrote the topic, a task expert, and a random assessor are not the same thing. Their conclusion: test collections are *not* fully robust to swapping judges when those judges differ a lot in expertise.

Keep this as your baseline. The bar for an LLM isn't "agrees perfectly with one human." It's "lands inside the range humans already vary by, **and** doesn't change the calls you're making."

## 4. How we got here

### 4.1 First look, 2023

[Faggioli and a big crew wrote *Perspectives on Large Language Models for Relevance Judgment*](https://arxiv.org/abs/2304.09161) and laid out a spectrum — from "humans judge, model helps a bit" all the way to "model does the whole thing." Their pilot turned up the pattern that's defined everything since: labels agree only so-so, leaderboards agree a lot.

They also listed the worries. Prompt sensitivity. Model bias. Evaluation eating its own tail. Contaminated data. Black boxes. And the sneaky one — that if a model defines relevance, relevance quietly becomes whatever the model thinks it is. None of those are solved yet.

### 4.2 Meanwhile, the rest of the world was doing this too

Worth a detour, because IR isn't the only field that pointed an LLM at a grading task, and the general LLM-as-a-judge crowd found the same things a bit earlier and gave them better names.

[Zheng et al.'s MT-Bench and Chatbot Arena paper](https://arxiv.org/abs/2306.05685) is the reference point. Their headline: strong judges like GPT-4 "can match both controlled and crowdsourced human preferences well, achieving over 80% agreement, the same level of agreement between humans." Sound familiar? Same shape as the IR result — good enough at the aggregate level, and benchmarked against how much humans disagree rather than against perfection.

They also named four failure modes that everyone now cites:

- **Position bias** — preferring whichever option you showed first.
- **Verbosity bias** — preferring the longer answer. They tested this with a "repetitive list" attack, padding an answer with redundant content. Claude-v1 and GPT-3.5 fell for it over 90% of the time. GPT-4 only 8.7%.
- **Self-enhancement bias** — preferring your own model's output.
- **Limited reasoning** — judges are weak at grading things that need actual reasoning, like math.

Now map those onto search. **Position bias** is a live problem the moment you do pairwise relevance judging, which is one of the main methods people use. **Verbosity bias** is a first cousin of the keyword-stuffing vulnerability we'll get to in §4.7 — both are the judge reacting to surface form instead of substance. **Self-enhancement** is exactly the self-preference finding that shows up in IR later. Same failure modes, different clothes.

But here's the thing IR should feel smug about: the general LLM-judge world grades free-text answers where there's often no ground truth at all, so "does the judge agree with humans" is the *only* check available. IR has something better — decades of test collections and a downstream question you can actually ask, namely *does the leaderboard come out the same*. That leaderboard check is the reason this whole article can distinguish four levels of agreement instead of one. Don't give it up.

### 4.3 Better models, better prompts, 2023–2024

[Thomas and colleagues](https://arxiv.org/abs/2309.10621) wrote up what happened when Bing did relevance labeling with LLMs at scale. Their line: accuracy "as good as human labellers," and better than third-party workers when you check against what actual searchers preferred.

Read the whole thing though, because they also say this: "Systematic changes to the prompts make a difference in accuracy, but so too do simple paraphrases." Reword your prompt in a way that means the same thing, get a different answer. Sit with that for a second.

[UMBRELA](https://arxiv.org/abs/2406.06519) then rebuilt that kind of assessor in the open with GPT-4o. Ran it across TREC Deep Learning 2019 through 2023, and the leaderboards it produced tracked the human ones closely. That's what turned this from scattered results into something people could actually reproduce and compare.

### 4.4 Everybody piles in, 2024–2025

The [LLMJudge challenge](https://arxiv.org/abs/2408.08896) at the LLM4Eval workshop (SIGIR 2024) asked the obvious follow-ups out loud: which models, which prompts, does fine-tuning an open model close the gap, is the synthetic data biased, is there leakage?

Then came [*Judging the Judges*](https://arxiv.org/abs/2502.13908), which released 42 sets of LLM-generated labels for TREC 2023 Deep Learning from eight teams around the world. This one's underrated. Almost everything before it compared one favorite model against one fixed human answer key. Now you can compare judges *to each other* across a real spread of models and pipelines.

Three things fell out:

- how you set up the judge changes the answer, a lot
- two judges can produce nearly the same leaderboard while labeling things completely differently
- one average agreement number tells you nothing about *which direction* a judge is wrong in

### 4.5 The big one: TREC 2024 RAG

[Upadhyay and team](https://arxiv.org/abs/2411.08275) ran four different assessment processes over the TREC 2024 RAG Track — NIST's full manual process plus three that lean on UMBRELA to varying degrees. 77 runs, 19 teams. On nDCG@20, nDCG@100 and Recall@100, the automated stuff produced leaderboards that lined up closely with the fully manual one.

Two details worth carrying around. Humans were **stricter** than the model. And bolting humans onto the LLM pipelines didn't help — the paper's words: LLM assistance "does not appear to increase correlation with fully manual assessments, suggesting that costs associated with human-in-the-loop processes do not bring obvious tangible benefits."

Strongest pro-automation result out there. But notice what it's testing: ordering 77 wildly different runs. That's a much easier job than telling apart two approaches that are nearly tied.

### 4.6 Why a matching leaderboard isn't the win you think

Here's where it gets uncomfortable.

[Otero, Parapar and Barreiro](https://arxiv.org/abs/2411.13212) zoomed in on the approaches at the top and on pairwise statistical calls. Their finding, straight from the abstract: LLM judgments are "unfair at ranking top-performing systems," and there's "an exceedingly high rate of false positives regarding statistical differences." Translation: the judge will tell you your new approach won, with confidence, when it didn't. If you're running A/B-style offline comparisons, this is the sentence that should keep you up.

[Clarke and Dietz](https://arxiv.org/abs/2412.17156) make a point that's obvious once said: an LLM relevance judge is basically just another relevance-scoring approach. So it can be gamed, and if your retrieval approach and your judge share the same underlying model, you're grading your own homework. They build an example where an approach scores great automatically and gains nothing with real humans.

[Balog, Metzler and Qin](https://arxiv.org/abs/2503.19092) found "the first empirical evidence of LLM judges exhibiting significant bias towards LLM-based rankers" — the judge likes retrieval approaches that are built like it is. They also hit "limitations in LLM judges' ability to discern subtle system performance differences," and confirm the leniency thing: LLM judges "are more lenient in their relevance assessments than human judges."

Worth flagging an honest disagreement here, because it hasn't settled. [SynDL](https://arxiv.org/abs/2408.16312) — a synthetic collection with 1,988 queries and 637,063 LLM labels — reports the opposite on that first point: their setup "does not favour language model approaches." So does the judge play favorites? Depends whose experiment you read. Don't let anyone tell you this one's closed.

### 4.7 Judges can be tricked

[Alaofi and co.](https://arxiv.org/abs/2501.17969) is my favorite paper here, partly for the title. They found LLMs "are more likely to label passages as relevant compared to human judges," and — the good bit — that they're "highly influenced by the presence of query words in the passages under assessment, even if the wider passage has no relevance to the query."

So: stuff the query words into a garbage passage, the judge calls it relevant. Some models even followed instructions written *inside the passage they were judging*. Your average agreement score will look perfectly healthy while this is happening.

If you run a marketplace where third parties write the item text and have money riding on ranking, reread that paragraph.

### 4.8 There's no single "LLM judge"

[Arabzadeh and Clarke](https://arxiv.org/abs/2504.12558) compared five ways of asking — binary, graded, pairwise, and two flavors of nugget-based — across TREC DL 2019–2021 and ANTIQUE, with GPT-4o and Llama. The point: *how you ask* changes the answer. "Use an LLM judge" isn't a method, it's a category.

[Farzi and Dietz](https://arxiv.org/abs/2507.09488) go further and break relevance into pieces — exactness, coverage, topicality, contextual fit — and grade each. Better leaderboards and, more useful day to day, you can actually see *why* something got the grade. Some disagreement isn't the judge being dumb; it's you never having said what you meant by relevant.

### 4.9 Now leave the English passage bubble, 2025–2026

Everything above is mostly English web passages. Turns out the conclusions don't just come along for the ride.

- [Mohtadi and colleagues](https://arxiv.org/abs/2512.05334) judged full documents vs. LLM-written summaries of them. Summary-based judging gets "comparable stability in systems' ranking" — but with "systematic shifts in label distributions and biases that vary by model and dataset." Same leaderboard, different labels, again.
- [The TREC Podcast reassessment](https://arxiv.org/abs/2601.05603) is the one to read. Five LLMs, 18,284 query-segment pairs, 91,420 labels total. On the 2020 track, human-vs-LLM leaderboard agreement (Kendall's τ) ran 0.81–0.84 and the top approaches held. On 2021 it dropped to 0.60–0.72 and the ordering got, in their words, "much more volatile… including the *top* ranking systems." **Same models, same method, same task — one year apart.** Then they took 22 cases where LLMs and the original assessor disagreed most and had three IR experts look. The experts sided with the LLMs (Krippendorff's α 0.71–0.86) and *negatively* with the original TREC assessor (−0.55 to −0.77). Read that twice. Sometimes the answer key is the thing that's wrong. The paper also finds the usual over-rating, plus a possible soft spot for lexical approaches.
- [Keller and team](https://arxiv.org/abs/2604.04140) found that judges handed nothing but a short query "judge many more documents relevant and have a lower agreement" than judges given a proper topic with a description and narrative. Best part: writing that description *automatically* still helps. Cheap fix, real gain.
- [NormasTCU](https://arxiv.org/abs/2608.27746) does Brazilian Portuguese legal search — 14,469 documents. Three models, two prompting styles, and agreement with humans was only fair-to-moderate (Cohen's κ 0.32–0.53, mean absolute error 0.46–0.66 on a 0–2 scale). And yet nDCG@10 and MRR leaderboards still hit Kendall correlations of 0.90 or better. P@10 and R@10 were shakier. Cleanest demo you'll find that label agreement, ranking agreement, and *which metric you picked* are three separate things.

### 4.10 What about products? Because that's where the money is

Almost all the academic evidence above is TREC passages, podcast transcripts and legal documents. If you work on e-commerce search, the honest answer to "does this transfer" is: *the shape transfers, the failure location moves.* Here's what the product-search evidence actually shows.

**Relevance isn't topicality any more.** In web search a passage is on-topic or it isn't. In product search the useful grading is about substitutability — the [ESCI scale](https://arxiv.org/abs/2206.06588) (Exact / Substitute / Complement / Irrelevant) is the common shape. That's a different cognitive task, and it moves the hard boundary. It's not "relevant vs. not." It's "is this a substitute or a complement," which is a judgment about shopping intent, not about text.

**And that's exactly where the judges fall over.** Allegro's RAT framework is the best-documented case: a 380K+ multilingual judgment dataset built by 30 experts across 13 departments and four languages (Polish, Czech, Slovak, Hungarian), dual blind annotation with expert arbitration. Their local quantized judge hit a quadratic-weighted Cohen's κ of 0.69 on Polish — genuinely good. But break it down by class and the story changes completely: F1 of 0.94 on exact matches and 0.83 on complements, and then **0.51 and 0.33** on separating "highly substitutable" from "substitutable."

Sit with that spread. The judge is excellent at the calls you didn't need help with and close to a coin flip on the distinction your merchandising team actually argues about. That's finding 3 from §7 — *it breaks where the decisions are hardest* — showing up in the most commercially relevant place possible. An overall κ of 0.69 would never have told you.

**Prompting folklore doesn't survive contact with the domain either.** Allegro found that removing few-shot examples *improved* both accuracy and inter-rater agreement — the opposite of what everyone assumes. What helped instead was structured reasoning and domain-specific business logic written into the prompt. Adding category and department metadata did nothing, because product names already carried it.

**Relevance in commerce is time-varying and business-defined.** Etsy makes this concrete: they maintain an evolving labeling guideline because relevance drifts with culture. "Face masks" meant costume masks before 2020 and protective masks after. There's no stable ground truth to converge on — the target moves, and your judge is frozen at its training cutoff.

**The published academic work leans practical.** [Mehrdad et al.](https://arxiv.org/abs/2406.00247) work over a multi-million query-item pair dataset with the stated goal of "relevance annotations on par with the human relevance evaluators." [eBay's keyphrase work](https://arxiv.org/abs/2505.04209) uses an LLM judge as a scalable proxy for seller judgment to train relevance filters, and their framing is the one to steal: it works *provided* you bind it to "a meticulous evaluation framework grounded in business metrics." [LREF](https://arxiv.org/abs/2503.09223) is another LLM-based relevance framework built for e-commerce.

Notice what industry does that the academic papers mostly don't: nobody in commerce treats the LLM as the final judge. Etsy anchors it with human golden labels and distills it into a servable model. Allegro built a 380K human dataset *first* and used it to validate. eBay ties the whole thing back to revenue. The pattern is **humans define the standard, the LLM scales it, business metrics keep it honest** — which is a considerably more modest claim than "LLM judges match humans," and a considerably more useful one.

## 5. What to actually measure

There's no one number. Pick a few that match what you're using the judge for.

| Level | The question | What to compute | Where it lies to you |
|---|---|---|---|
| Raw labels | Same grade, same item? | Accuracy, raw agreement | Looks great when 90% of things are non-relevant |
| Chance-corrected | Agreement beyond luck | Cohen's / Fleiss' κ, Krippendorff's α | Moves around with class balance |
| Graded labels | How far off, and which way? | Weighted κ, ordinal α, MAE, confusion matrix | An average hides one-sided errors |
| Judge vs. judge | Same ordering of items? | Spearman, Kendall | Correlation isn't agreement — one judge can sit a whole grade higher |
| Same judge twice | Is it stable? | Test-retest, label entropy, variance | Stable ≠ right |
| Approach scores | Same score for my approach? | Correlation, calibration plots, score bias | Great correlation with every score inflated |
| Leaderboard | Same order? | Kendall's τ, top-weighted measures | Overall τ hides your top two swapping |
| Actual decisions | Same call? | Win/loss/tie agreement, significance confusion matrix, Type I/II errors | Needs enough topics and a real test protocol |

Three rules that fall out of that table:

**Don't quietly collapse graded labels to binary.** Or if you do, report both. Squashing 0/1/2/3 into relevant/not manufactures agreement and throws away exactly the distinctions nDCG cares about.

**Never post a κ without the label distribution and confusion matrix next to it.** A judge that's lenient across the board can have a perfectly normal κ. The leniency is the thing that'll bite you.

**Leaderboard correlation needs a top-weighted companion.** Nobody cares whether the judge can tell a terrible approach from a great one. You care about the three candidates that are nearly tied. Look there.

## 6. So what number is good enough?

This is the question everybody actually has and almost no paper answers. Here's the honest attempt.

### The two conventions people quote at you

**Kendall's τ ≥ 0.9.** This comes from Voorhees, who proposed that two evaluation schemes correlating at 0.9 or above should be treated as equivalent — partly on the grounds that you can't really be more precise than that. Below about 0.8 you're seeing genuine reordering, not just neighbours swapping. It's a sensible convention and it's been the field's default for twenty-odd years. It is *a convention*, not a law of nature, and nobody has re-derived it for LLM judges.

**Cohen's κ bands.** Fair 0.21–0.40, moderate 0.41–0.60, substantial 0.61–0.80. These come from a 1977 biometrics paper (Landis and Koch), have nothing to do with IR, and were basically made up as a convenience. People cite them as though they mean something. Use them as vocabulary, not as a gate.

### Why neither one is enough on its own

NormasTCU is the perfect cautionary tale. Their leaderboards cleared the τ ≥ 0.9 bar. Their labels sat at κ 0.32–0.53 — "fair to moderate," which is to say not good. **Passing the ranking threshold told them nothing about whether the labels were any good**, and passing the label threshold would have told them nothing about the ranking. These are separate gates and you need both.

Meanwhile Podcast 2021 came in at τ 0.60–0.72, which is well under 0.8 — squarely in "these schemes have different emphases" territory. Same method that scored 0.81–0.84 the year before.

### A rubric that actually depends on the decision

*This part is my synthesis, not something you can cite — but it follows from the evidence above.* The right threshold depends entirely on what the number is guarding:

| What you're using it for | Bar to clear | Why |
|---|---|---|
| Tracking quality over time, broad regression detection | τ ≥ 0.9 on your headline metric, κ ≥ 0.4, label distribution sanity-checked | Errors are stable across runs; you're watching the delta, not the level |
| Ranking a diverse field of candidate approaches | Same, plus top-weighted agreement | Overall τ hides exactly the region you care about |
| Choosing between two close approaches / declaring a winner | **No threshold saves you here** | Otero's false positives happen *at high τ*. Adjudicate the deciding slice with humans |
| Generating training labels | Per-class κ on the specific boundary you care about | Allegro: overall κ 0.69, but 0.33 on the class distinction that mattered |
| Judging content you don't control | Add adversarial tests before any threshold | Alaofi: keyword stuffing passes a healthy-looking judge |

### Three practical rules worth more than any threshold

**Report agreement per class, not just overall.** The Allegro spread — 0.94 on the easy class, 0.33 on the hard one, 0.69 overall — is the whole argument. Overall numbers average your best case with your worst and hand you something that describes neither.

**Measure your judge's self-disagreement first.** Run the same judgments twice. Whatever rate the judge disagrees with *itself* at is your noise floor. **Any difference between two approaches smaller than the judge's own self-disagreement is not measurable with that judge**, no matter how good the correlation with humans looks. Most teams never check this. It takes one afternoon and it tells you the resolution of your instrument.

**Set the bar against human-human agreement on your own data, not against 1.0.** MT-Bench's framing is the right one: GPT-4's ~80% agreement was reported as meaningful precisely because that's "the same level of agreement between humans." If your own annotators agree at κ 0.6, demanding κ 0.8 from a model is incoherent. Measure your humans first, then you know what to ask for.

## 7. So what do we actually know?

### 1. Label agreement is never great

Even good models don't reproduce human labels exactly. It moves with the collection, the model, the prompt, the grading scale, how much context you gave, and who the humans were. Fair-to-moderate is normal. Better happens when the task is tightly specified.

### 2. Leaderboards hold up better than labels

Same as the old human-vs-human finding. Item-level errors cancel out, or hit every approach equally, and the ordering survives. UMBRELA, TREC RAG, SynDL and NormasTCU all show this. Real result. Just remember it's a result about *one level, one metric, one collection* — not proof that judges are interchangeable.

### 3. It breaks exactly where you need it most

Sorting a messy pile of 77 runs: fine. Telling apart two strong approaches that are close: not fine. Separating exact matches from garbage: fine. Separating a substitute from a slightly-worse substitute: coin flip. Your overall number can look terrific while the winner flips and your significance tests fire off false positives. The easy case works and the case you actually have is the hard one.

### 4. The errors have a shape

They're not noise. They're patterns: too generous, over-reacting to query words in the text, twitchy about prompt wording, following instructions embedded in documents, preferring whatever came first in a pairwise comparison, preferring longer text, maybe favoring approaches that look like themselves (though SynDL disputes that one). Because it's systematic, **collecting more labels from the same judge does not wash it out.** You have to change something.

### 5. The humans aren't a gold standard either

The Podcast study is the proof. Three experts looked at the worst disagreements and sided with the machines against the original assessor — with a *negative* correlation to that assessor. So when your LLM disagrees with the answer key, "the LLM screwed up" is one hypothesis, not the conclusion. Sometimes the key is wrong. Sometimes the item is genuinely ambiguous.

### 6. Nobody's really studied model-vs-model

Almost every paper nails human judgments to the wall as truth and asks which LLM gets closest. Far fewer properly cross several model families, several prompts, and repeated runs, then ask the real question: *would my conclusion have changed if I'd picked a different judge?* The Judging the Judges collection and the Podcast study are the first solid steps.

### 7. In industry, nobody actually replaces the humans

Read what Etsy, Allegro and eBay built rather than what the headlines say. Every one of them uses humans to define the standard, the LLM to scale it, and business metrics to keep the whole thing honest. The academic question is "can the model replace the assessor." The deployed answer is "no, it multiplies them," and that's not a consolation prize — it's the actual value.

## 8. How to run this properly

Don't crown one model as The Judge. Cross it.

**Your judges**

- At least three different model families. Three versions of the same vendor's model doesn't count.
- Run each judgment more than once. Temperature 0 is not determinism — and this is how you get your noise floor from §6.
- Keep humans in it, several of them, on a stratified slice. You need human-human agreement to know what to ask of the model.
- Write down the model version, the access date, the exact prompt, decoding settings, and how you truncated documents. You will not remember in four months.

**Your sample**

- Stratify: query type, difficulty, ambiguity, domain, result length, original grade.
- Load up on the close calls. Obviously-relevant and obviously-garbage teach you nothing — and they're where your headline accuracy comes from.
- Pull results from different *kinds* of retrieval approaches, or you're only measuring agreement on one family.
- Throw in some dirty tricks: query-word stuffing, instructions hidden in the text, misleading summaries, very long documents. If you have third-party sellers writing your item text, this isn't paranoia, it's a threat model.
- If you swap the order of options in pairwise judging, do it systematically. Position bias is real and cheap to measure.

**Your analysis** — report all three layers, not just the flattering one:

1. **Items:** label distributions, confusion matrices, weighted agreement, direction of error, **and per-class breakdowns**.
2. **Systems:** score bias, leaderboard correlation, top-weighted agreement, how far the leaders moved.
3. **Decisions:** who won, pairwise significance, effect direction, whether the gap is big enough to care about.

Then take the disagreements and have someone review them blind. Not to declare a winner — to *sort* them. Ambiguous topic? Missing context? Human error? Model error? Different reading of the scale? Gamed content? Or two genuinely defensible ideas of what relevant means? Those need different fixes.

## 9. Still open

- What happens to your evaluation when the judge model gets deprecated and you swap in a new one?
- Is a small panel of different judges better at flagging "we're not sure about this one" than one strong judge?
- Which disagreements actually change a decision? Most probably don't.
- How do you even model agreement when there are several legitimate answers?
- Can spelling out the criteria improve agreement without pinning relevance down too narrowly?
- How do you catch someone gaming the judge — especially when they write the item text and profit from ranking?
- When should humans judge everything, versus review disagreements, versus audit a sample, versus just write the criteria?
- How do you keep a benchmark honest when everyone can optimize against a public automatic judge?
- Does the cascade-and-distill pattern preserve the judge's *biases* along with its accuracy? Nobody's really checked what a distilled student inherits.
- How do you evaluate against a target that moves — commerce relevance shifts with season, culture and stock, and your judge's training data doesn't?

## 10. Where that leaves you

Middle ground, and it's not a cop-out.

LLM judges are genuinely useful right now: scaling up assessment, extending pools, fast exploratory evaluation, auditing your existing human labels (the Podcast paper shows they'll find real mistakes). On several collections they reproduce broad leaderboards remarkably well, for a rounding error of the cost. That cost gap is the entire reason anyone is doing this, and it's real.

But agreement is conditional. A strong correlation does not buy you interchangeable labels, fair treatment of your best approaches, trustworthy significance tests, or protection from someone gaming the thing. And the closer you get to the decision you actually care about — this approach or that one, this substitute or that one — the less the reassuring aggregate numbers apply.

So stop asking:

> Does the LLM agree with the human?

Start asking:

> If I swap the judge, the prompt, or just run it again — which of my conclusions survive, and which ones move?

That's a question you can actually answer. And it treats disagreement as information about your evaluation, which is what it is.

## Worth reading

| Paper | Why |
|---|---|
| [Voorhees (2000)](https://www.nist.gov/publications/variations-relevance-judgments-and-measurement-retrieval-effectiveness) | Humans disagreed first; comparisons between approaches mostly survived it. Origin of the τ ≥ 0.9 convention |
| [Bailey et al. (2008)](https://www.microsoft.com/en-us/research/publication/relevance-assessment-are-judges-exchangeable-and-does-it-matter/) | Expertise matters; judges aren't swappable |
| [Faggioli et al. (2023)](https://arxiv.org/abs/2304.09161) | The collaboration spectrum, and the worry list nobody's cleared |
| [Zheng et al. (2023)](https://arxiv.org/abs/2306.05685) | MT-Bench: >80% agreement, and the names for position/verbosity/self-enhancement bias |
| [Thomas et al. (2024)](https://arxiv.org/abs/2309.10621) | It works at Bing scale — and paraphrasing your prompt moves the numbers |
| [UMBRELA (2024)](https://arxiv.org/abs/2406.06519) | Open reproduction, validated across five TREC years |
| [LLMJudge (2024)](https://arxiv.org/abs/2408.08896) | The shared challenge that got everyone comparing |
| [SynDL (2024)](https://arxiv.org/abs/2408.16312) | Huge synthetic collection — and says judges *don't* favor LM approaches |
| [Mehrdad et al. (2024)](https://arxiv.org/abs/2406.00247) | Product search relevance judgment at multi-million pair scale |
| [Upadhyay et al. (2024)](https://arxiv.org/abs/2411.08275) | 77 runs, 19 teams; humans stricter, human-in-the-loop didn't pay |
| [Otero et al. (2025)](https://arxiv.org/abs/2411.13212) | Unfair at the top, and inventing significance |
| [Clarke & Dietz](https://arxiv.org/abs/2412.17156) | Your judge is a ranker too, so it can be gamed |
| [Judging the Judges (2025)](https://arxiv.org/abs/2502.13908) | 42 judgment sets, so you can finally compare judges to judges |
| [Balog et al. (2025)](https://arxiv.org/abs/2503.19092) | Judges favor LLM rankers, miss small gaps, grade generously |
| [LREF (2025)](https://arxiv.org/abs/2503.09223) | LLM relevance framework built for e-commerce |
| [Arabzadeh & Clarke (2025)](https://arxiv.org/abs/2504.12558) | There is no single "LLM judge" — how you ask changes the answer |
| [eBay keyphrase judgments (2025)](https://arxiv.org/abs/2505.04209) | LLM judge as proxy for seller judgment, tied to business metrics |
| [Farzi & Dietz (2025)](https://arxiv.org/abs/2507.09488) | Break relevance into criteria and you can see the reasoning |
| [Alaofi et al. (2025)](https://arxiv.org/abs/2501.17969) | Keyword stuffing and hidden instructions fool the judge |
| [Mohtadi et al. (2025)](https://arxiv.org/abs/2512.05334) | Judging summaries: same leaderboard, different labels |
| [Podcast reassessment (2026)](https://arxiv.org/abs/2601.05603) | Two adjacent years, very different agreement — and the answer key was wrong |
| [Keller et al. (2026)](https://arxiv.org/abs/2604.04140) | Give the judge a real topic description; agreement goes up |
| [NormasTCU (2026)](https://arxiv.org/abs/2608.27746) | Portuguese legal search: weak labels, strong rankings, metric-dependent |
| [Etsy Code as Craft](https://www.etsy.com/codeascraft/how-etsy-uses-llms-to-improve-search-relevance) | Golden labels → LLM teacher → distilled student under 10ms |
| [Allegro RAT](https://blog.allegro.tech/2026/08/automating-search-relevance-llm-as-a-judge.html) | 380K multilingual judgments; κ 0.69 overall, 0.33 where it counted |
