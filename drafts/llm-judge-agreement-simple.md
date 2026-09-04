# Do LLM Judges Actually Agree With Us? (the no-jargon version)

## The short version

People keep asking whether LLM judges "work" for search evaluation. Wrong question. They work fine for some things and fall apart for others, and the whole game is knowing which is which.

Two words first.

An **approach** is one version of a search engine — your current ranker, the new one you want to ship instead. You're always comparing a few and picking one. Some papers call this a "system"; same thing.

The **leaderboard** is what comes out the other end. Somebody grades the results, each approach gets a score, and they line up best to worst. That line-up is what you end up arguing about.

Now the thing nobody tells you up front: **there are four different things you could mean by "the judges agree," and they don't move together.**

1. **Do they put the same grade on the same result?**
2. **Do they give each approach roughly the same score?**
3. **Do they put the approaches in the same order?**
4. **Do they lead you to the same decision — same winner, same "yes this is a real difference," same ship-it call?**

You'd assume these rise and fall together. They don't. Two judges can fight over thousands of individual grades and still both say "B beats A beats C" — when a judge's mistakes land on every approach in much the same way, the scores can be wrong while the ordering survives.

Picture a tape measure that reads five centimetres short. Every plank you measure comes out wrong. But the longest plank is still the longest, and the shortest is still the shortest, so if all you needed was to put them in order, the broken tape measure did the job. That holds as long as the error is the same for every plank — which, as we'll see, is not something you get for free.

That's the whole reason people got excited about this. The judge doesn't have to be right about each result — only about which approach wins.

But a matching leaderboard hides a lot: different ideas of what "relevant" even means, blowups on specific kinds of queries, your top two approaches swapping places, differences that look real and aren't, and a quiet thumb on the scale for certain kinds of search.

So: a real tool you have to check, not a drop-in replacement for people. When someone hands you a study, ask whether they checked both the individual grades *and* the final decision, whether they used more than one model, whether they looked at the disagreements instead of averaging them into mush, and whether the conclusion holds for the kind of comparison you actually care about.

And if you're the one shipping it — skip to §6, where I try to answer the question everybody actually has: *how good is good enough?*

## 1. Who's even doing the judging?

Somebody looks at a search and a result and says how good the match is. That somebody can be the person who searched, an expert, a paid worker, an LLM you asked nicely, or some mix.

Which means "judge vs. judge" covers a bunch of different comparisons that answer different questions:

| Who vs. who | What you're really asking |
|---|---|
| Person vs. person | Is this even an objective task? Are people swappable? |
| Model vs. person | Does the model copy this particular person? |
| Model vs. a different model | Would another model have told me something else? |
| One prompt vs. another prompt | Does my answer survive me rewording the instructions? |
| Same model, run twice | Is it even consistent with itself? |
| A panel vs. one judge | Does averaging help, or just paper over the cracks? |

These are not interchangeable. Matching one person doesn't mean matching your users. Three models agreeing might just mean three models share the same blind spot. And a model that's consistently wrong is still wrong — consistency isn't correctness.

Work out which comparison you're making *before* you start quoting agreement numbers at people.

## 2. Why anyone wants this: money and time

Let's not be coy about the motivation. The main driver was never accuracy. It was that human judgment is brutally expensive and slow.

Roughly, to grade one result for one search:

| | Cost each | Turnaround |
|---|---|---|
| A person | $0.50–$5.00 | days to weeks |
| A model | about a tenth of a cent | minutes |

That's hundreds to thousands of times cheaper. A thousand searches with ten results each costs $5,000–$50,000 and a couple of weeks with people, or about ten dollars and twenty minutes with a model. [Microsoft's Bing team](https://arxiv.org/abs/2309.10621) put it plainly — models produced "better labels than third-party workers, for a fraction of the cost."

That gap is the whole reason this field exists. It's also why people are motivated to believe the agreement numbers.

**But "cheap per item" is not the same as "cheap."** At shopping-site scale — billions of searches a year, hundreds of billions of search-and-product pairs — grading everything with a top-end model isn't expensive, it's *impossible*. So everyone takes a sample: grade a few thousand, assume the rest look the same. Fine for watching quality drift over time. Useless when you need coverage — hunting down every bad result in a catalogue, or catching one weird query that broke. A sample won't find those.

The way out is to change the shape of the job, and [Andreas Wagner](https://www.linkedin.com/pulse/towards-scalable-relevance-engineering-andreas-wagner-s3akf/) has the clearest worked version of it. His company sits on upwards of 10 billion searches a year, so this was something they had to solve rather than describe. Three steps.

**Step one: grade far less.** The biggest saving isn't a cheaper model, it's not grading at all. Watch what shoppers actually do, and most pairs sort themselves into a priority order. Results people already click and buy go to the back of the queue — not because behaviour proves they're good (what gets clicked is shaped by where it ranked, by price, brand and by what happened to be in stock), but because they're the least likely place your problems are hiding. The ones nobody touches are your suspects, and they're the ones worth spending money on first. Wagner reports that this alone clears about 93% of the work. No choice of model gets you anywhere near that.

**Step two: cheap judges first, expensive judge last.** Small compressed models — the kind that run on an ordinary CPU for almost nothing — handle 75–85% of what's left. Only the cases where the cheap models *disagree with each other* go up to the expensive model. Disagreement turns out to be a decent signal that a case is genuinely hard.

Two warnings that come with this. Two weak judges can be confidently wrong *together*, especially if they're built on the same underlying model, so spot-check a sample of what got waved through, not just what got escalated. And the whole thing rests on shopper behaviour being trustworthy — if people only clicked the top result because it was the top result, that bias is baked into the 93% you decided never to look at.

**Step three: teach a small model to do it.** Take the expensive model's answers and use them as training material for a cheap one. Etsy runs this: people write the "golden" examples, a big model copies their standard across millions of pairs, and a small fast model is trained on the result and shipped into the live site, adding under 10 milliseconds. Wagner does the same thing one level up, on the judge itself — about 100,000 expensive judgments trained a small model down to under 20 milliseconds on a plain CPU, cheap enough to just leave running.

The pattern in all of it: **people define what good means, the big model spreads that definition across everything, the small model does the day job.** The judge's role is to teach the model you ship, not to be it.

One more real-world number, from the Polish shopping site [Allegro](https://blog.allegro.tech/2026/08/automating-search-relevance-llm-as-a-judge.html): moving from a cloud model to a compressed one running on their own hardware cut costs 60%. But a trick that saves money in the cloud — stuffing a whole page of products into one request — made the local model noticeably less reliable, and they went back to one product at a time. The cost savings are real, and they don't transfer between setups.

## 3. People never agreed either

Judges disagreeing is not some new LLM problem. Search people have known relevance is squishy for decades.

[Work going back to 2000](https://www.nist.gov/publications/variations-relevance-judgments-and-measurement-retrieval-effectiveness) showed it: swap in a different set of human graders and plenty of individual grades change — but the *comparison* between approaches mostly survives. That's the founding insight of the whole field. Everyone doesn't have to agree on everything, as long as the winner stays the winner.

It only goes so far. [A follow-up asked whether graders are really swappable](https://www.microsoft.com/en-us/research/publication/relevance-assessment-are-judges-exchangeable-and-does-it-matter/) and found it matters a lot who's doing it. The person who wrote the question, someone who knows the subject, and a random hired hand are not the same thing.

Keep this as your baseline. The bar for a model isn't "agrees perfectly with one person." It's **"disagrees no more than your own people disagree with each other, and doesn't change the calls you're making."**

## 4. How we got here

### 4.1 First look, 2023

The first serious [survey](https://arxiv.org/abs/2304.09161) laid out a spectrum, from "people grade, the model helps a bit" to "the model does the whole thing." Their trial run turned up the pattern that's defined everything since: **individual grades agree only so-so, leaderboards agree a lot.**

They also listed the worries — the model being sensitive to how you word the prompt, the model's own biases, evaluation eating its own tail, and the sneaky one: if a model gets to define relevance, relevance quietly becomes whatever the model thinks it is. None of those are solved.

### 4.2 The rest of the world was doing this too

Search isn't the only field that pointed a model at a grading job. The general "use an LLM to grade things" crowd got there earlier. Their [reference result](https://arxiv.org/abs/2306.05685): strong models agree with people more than 80% of the time — which happens to be about how often people agree with each other.

They also named four ways a model judge goes wrong, and all four show up in search:

- **It prefers whatever came first.** Show it two options and the order alone moves its answer.
- **It prefers longer text.** Padding an answer with a repetitive list fooled some models more than 90% of the time.
- **It prefers its own work.** A model rates output from its own family more kindly.
- **It can't reason well enough** for the genuinely hard cases.

But here's the thing search people should feel smug about. The general crowd grades free-text answers where there's often no right answer at all, so "does the judge agree with people" is the *only* check they have. Search has something better: a downstream question you can actually ask — **does the leaderboard come out the same?** That's why this article can talk about four levels of agreement instead of one. Don't give that up.

### 4.3 It takes off, 2023–2025

[Bing did relevance grading with models at scale](https://arxiv.org/abs/2309.10621) and reported accuracy as good as human graders, and better than hired workers when checked against what real searchers preferred.

Read the whole thing though, because they also say this: reword your prompt in a way that means exactly the same thing, and you get a different answer. Sit with that for a second.

Then the field got reproducible. [One project](https://arxiv.org/abs/2406.06519) rebuilt a model grader in the open and showed its leaderboards tracked the human ones closely across five years of a public benchmark. [Another](https://arxiv.org/abs/2502.13908) released 42 sets of model-generated grades from eight different teams, so for the first time you could compare judges *to each other* instead of each against one fixed answer key.

Three things fell out of that: how you set the judge up changes the answer a lot; two judges can produce nearly the same leaderboard while grading individual results completely differently; and a single average agreement number tells you nothing about *which direction* a judge is wrong in.

### 4.4 The strongest pro-automation result

[The biggest test so far](https://arxiv.org/abs/2411.08275) ran four different grading processes over the same benchmark — the full careful human process, plus three that leaned on a model to varying degrees. 77 different search approaches, 19 teams. The automated leaderboards lined up closely with the fully human one.

Two details worth carrying around. **People were stricter than the model.** And bolting a human review step onto the model pipeline didn't help — the extra cost bought no measurable improvement.

That's the strongest result out there for automating this. But notice what it's testing: sorting 77 wildly different approaches. Much easier than telling apart two that are nearly tied.

### 4.5 Why a matching leaderboard isn't the win you think

Here's where it gets uncomfortable.

[One study](https://arxiv.org/abs/2411.13212) zoomed in on just the top few approaches, and on the moment you declare a difference real. Their finding, straight from the paper: model judges are "unfair at ranking top-performing systems," with "an exceedingly high rate of false positives regarding statistical differences."

In plain terms: **the judge will tell you your new approach won, with confidence, when it didn't.** If you run offline A/B comparisons, that's the sentence that should keep you up.

[Another paper](https://arxiv.org/abs/2412.17156) makes a point that's obvious once said: a model judge is itself just another thing scoring relevance. So it can be gamed — and if your search engine and your judge run on the same underlying model, you're grading your own homework. They built an example that scores brilliantly with the model and gains nothing with real people.

[A third](https://arxiv.org/abs/2503.19092) found model judges genuinely do favour search approaches built like themselves, struggle to see small differences between approaches, and grade more generously than people do.

Worth flagging an honest disagreement, because it hasn't settled: [one large study](https://arxiv.org/abs/2408.16312) — nearly 2,000 queries and 637,000 grades — found the opposite on that favouritism point. Does the judge play favourites? Depends whose experiment you read.

### 4.6 Judges can be tricked

[This one](https://arxiv.org/abs/2501.17969) is the one to remember. Models call things relevant more readily than people do — and they're heavily swayed by the search words simply *appearing* in the text, even when the text has nothing to do with the search.

Stuff the search words into a garbage page and the judge calls it relevant. Some models even followed instructions written *inside the text they were supposed to be grading*. And your average agreement score will look perfectly healthy the whole time this is happening.

If you run a marketplace where third parties write the product descriptions and have money riding on ranking, read that paragraph again.

### 4.7 There's no single "LLM judge"

[Compare the ways of asking](https://arxiv.org/abs/2504.12558) — yes/no, a 0-to-3 scale, "which of these two is better," and a couple of others — and *how you ask changes the answer.* "Use an LLM judge" isn't a method. It's a category.

And [breaking relevance into parts](https://arxiv.org/abs/2507.09488) — is it exactly right, does it cover the whole question, is it on topic, does it fit the context — and grading each part separately gives better leaderboards *and* lets you see why something got the grade it did. Some disagreement isn't the judge being stupid. It's you never having said what you meant by "relevant."

### 4.8 Leave the English-web bubble, 2025–2026

Everything above is mostly English web pages. The conclusions don't automatically come along for the ride.

- Grading full documents versus model-written summaries of them gave [comparable leaderboards, but systematically different individual grades](https://arxiv.org/abs/2512.05334). Same ranking, different grades, again.
- [The podcast study](https://arxiv.org/abs/2601.05603) is the one to read. Five models, over 18,000 pairs, more than 91,000 grades. On one year's data the models matched the human leaderboard well and the top approaches held steady. On the *next year's* data the match dropped sharply and the ordering got, in their words, "much more volatile — including the *top* ranking systems." **Same models, same method, same task, one year apart.**

  Then they did something clever. They took the 22 cases where the models and the original human grader disagreed *most*, and had three experts look. **The experts sided with the models** — and disagreed with the original human grader worse than random chance would predict. That doesn't mean the answer key is broadly wrong. It means the answer key *can* be wrong, and is arguable, on exactly the cases where a model looks like it's failing.
- Judges given nothing but a short search query [call far more things relevant and agree less](https://arxiv.org/abs/2604.04140) than judges given a proper description of what the searcher wanted. Writing that description *automatically* still helps. Cheap fix, real gain.
- [Brazilian legal search](https://arxiv.org/abs/2608.27746), 14,469 documents: agreement on individual grades was mediocre. And yet the leaderboards still matched almost perfectly — on two scoring formulas, while two others were shakier. Cleanest demonstration you'll find that grade agreement, ranking agreement, and *which formula you picked* are three separate things.

### 4.9 What about shopping sites? Because that's where the money is

Almost all the evidence above is web pages, podcasts and legal documents. If you work on shopping search, the honest answer to "does this transfer" is: **the shape transfers, the failure moves somewhere else.**

**Relevance isn't "is it about this" any more.** On the web, a page is on-topic or it isn't. In a shop, the real question is *would this do instead?* The common scale is four levels: it's exactly the thing, it's a fair substitute, it goes with it, it's junk. That's a completely different mental task — it's about what the shopper wanted, not about what the words say.

**And that's exactly where the judges fall over.** Allegro is the best-documented case: 380,000 human judgments, built by 30 experts across 13 departments and four languages, each item graded blind by two people with an expert settling ties. Against that, their local model judge scored well overall.

Break it down by category, though, and the picture changes completely. It's excellent at spotting exact matches and things-that-go-with. It's **poor at separating a great substitute from an okay one** — which is precisely the call the merchandising team argues about every week. Brilliant at the easy stuff nobody needed help with, weak at the one distinction that mattered. The overall score would never have told you.

**Prompting folklore doesn't survive contact with the domain either.** Allegro found that *removing* worked examples from the prompt made things better — the opposite of what everyone assumes. What helped instead was telling the model how to reason step by step, and writing the actual business rules into the prompt. Adding product category information did nothing, because the product names already carried it.

**And relevance in shopping moves.** Etsy keeps rewriting its grading guidelines because meaning drifts: "face masks" meant costume masks before 2020 and medical masks after. There is no fixed truth to converge on. The target moves, and your judge's knowledge stopped on the day it was trained.

Notice what industry does that the research papers mostly don't: **in the best-documented real deployments, the model is never the final judge.** Etsy anchors it with human examples and trains a small model off it. Allegro built the 380,000-item human dataset *first*, then used it to check the model. eBay ties the whole thing back to revenue — the judge is a stand-in for seller judgment only as long as it's pinned to business numbers.

The pattern is: **people set the standard, the model spreads it, the money keeps it honest.** That's a smaller claim than "model judges match people," and a much more useful one.

## 5. What to actually measure

There's no one number. Pick a few that match what you're using the judge for.

| What you're checking | The question | Where it lies to you |
|---|---|---|
| Individual grades | Same grade on the same result? | Looks brilliant when 90% of things are obviously junk — the judge gets credit for the easy calls |
| Grades, corrected for luck | How much better than guessing? | Moves around depending on how many relevant results are in your sample |
| How far off, and which way | Off by one, or off by three? Too generous or too harsh? | An average hides a judge that's wrong in one direction every time |
| Broken down by grade | Which distinctions can it actually make? | This is the one everyone skips, and it's the one that catches the Allegro problem |
| Is it stable? | Run it twice — same answer? | Stable isn't the same as right |
| Your approach's score | Same score for my approach? | The scores can all be inflated and still move together perfectly |
| The leaderboard | Same order? | An overall match hides your top two swapping places |
| The actual decision | Same winner? Same ship-it call? | Needs enough queries and a real test to mean anything |

Three rules fall out of that.

**Don't quietly squash a 0-to-3 scale down to "relevant / not relevant."** Or if you do, report both. Squashing manufactures agreement and throws away exactly the distinctions your scoring formula cares about.

**Never quote an agreement score on its own.** Always publish the breakdown next to it — how many of each grade, and what got confused with what. A judge that's too generous across the board can post a perfectly normal-looking score. The generosity is the thing that'll bite you.

**Leaderboard agreement needs a top-of-the-table companion.** Nobody cares whether the judge can tell a terrible approach from a great one. You care about the three candidates that are nearly tied. Look there.

## 6. So how good is good enough?

The question everybody actually has, and almost no paper answers. Here's the honest attempt.

### The two rules of thumb people quote at you

**For leaderboards: 0.9 out of 1.** Two ways of grading that agree at 0.9 or above on the final ordering get treated as equivalent — partly on the honest grounds that you can't really be more precise than that. Below about 0.8 you're seeing genuine reshuffling, not just neighbours swapping. It's been the field's default for twenty-odd years. It is a *convention*, not a law of nature, and nobody has re-checked it for model judges.

**For individual grades: the "fair / moderate / substantial" bands.** These come from a 1977 medical statistics paper, have nothing to do with search, and were invented as a convenience. Use them as vocabulary, not as a gate.

### Which one is the gate depends on the decision

The Brazilian legal study is the cautionary tale. Their leaderboards cleared the 0.9 bar comfortably. Their individual grades were mediocre. **Passing the ranking bar told them nothing about whether the grades were any good, and passing a grade bar would have told them nothing about the ranking.**

So measure both, then decide which one is the gate based on what you're doing with it:

- If you just want a broad ranking of approaches, decent decision agreement is enough even with mediocre grades. That's the old insight, still standing.
- But if the grades will be read by people, reused as training data, or used to debug specific queries, **weak grade agreement kills it on its own**, and no amount of leaderboard agreement rescues it.

And remember the podcast study: the same method scored above the bar one year and well below it the next.

### A rough guide, based on what you're doing

*My own synthesis, not something you can cite — but it follows from the evidence above.*

| What you're using it for | Bar to clear | Why |
|---|---|---|
| Watching quality over time, catching big regressions | Strong leaderboard agreement, decent grade agreement, and eyeball the grade distribution | The judge's mistakes are consistent run to run; you're watching the change, not the level |
| Picking from a wide field of candidates | Same, plus check the top of the table separately | The overall number hides exactly the region you care about |
| **Choosing between two close approaches** | **High overall agreement cannot validate this on its own — validate that specific decision, with targeted human grades** | The false-alarm problem happens *at high agreement*. Have people settle the deciding cases |
| Generating training data | The breakdown by grade, on the specific distinction you care about | Allegro: fine overall, poor on the one call that mattered |
| Judging text you don't control | Run the dirty tricks first, before any threshold | Keyword stuffing sails past a healthy-looking judge |

### Three practical rules worth more than any threshold

**Report the breakdown, not just the overall number.** Publish what got confused with what, grade by grade, next to whatever single figure you quote. The Allegro result is the whole argument for this.

**Measure your own pipeline's wobble first.** Run the entire grading process several times over and recompute the *final numbers and the final decision*, not just the grades. How much they move is your instrument's margin of error. If the gap between two approaches keeps getting swallowed by that wobble, the judge cannot tell them apart — no matter how well it agrees with people.

Careful: this is not the same as "how often the judge changes its mind about a single grade." A judge that flips 8% of its grades and a quality gap of 0.015 are numbers on completely different scales. You have to push the wobble all the way through to the final score before comparing. Most teams never check. It takes one afternoon and it tells you the resolution of your instrument.

**Set the bar against your own people, not against perfection.** The 80%-agreement result everyone quotes was reported as meaningful *precisely because* that's how much people agree with each other. If your own graders only agree 60% of the time, demanding 80% from a model is incoherent. Measure your people first, then you know what to ask for.

## 7. How to run this properly

Don't crown one model as The Judge. Cross-check it.

**Your judges**

- Ideally three or more models from genuinely different makers. Three versions of the same vendor's model doesn't count.
- Run each grading more than once. "Temperature zero" is not the same as deterministic — and this is how you get your wobble measurement from §6.
- Keep people in it, several of them, on a carefully chosen slice. You need to know how much your people disagree to know what to ask of the model.
- Write down the model version, the date, the exact prompt, the settings, and how you cut long documents down. You will not remember in four months.

**Your sample**

- Cover the range deliberately: different kinds of query, easy and hard, clear and ambiguous, short and long results.
- **Load up on the close calls.** Obviously-perfect and obviously-garbage results teach you nothing — and they're where your flattering headline accuracy comes from.
- Pull results from genuinely different *kinds* of search approach, or you're only measuring agreement on one family.
- Throw in dirty tricks on purpose: search words stuffed into junk text, instructions hidden inside the text, misleading summaries, very long documents. If third parties write your product descriptions, this isn't paranoia, it's a threat model.
- If you're showing the judge two options at a time, swap the order systematically. The judge prefers whatever came first, and that's cheap to measure.

**Your analysis** — report all three layers, not just the flattering one.

- **Individual results:** the grade distribution, what got confused with what, which direction the errors run, and the breakdown by grade.
- **Approaches:** whether scores are inflated, whether the leaderboard matches, and how far the leaders moved.
- **Decisions:** who won, whether the difference is real, and whether the gap is big enough to care about.

Then take the disagreements and have someone go through them blind. Not to declare a winner — to *sort* them. Ambiguous query? Missing context? Human slip? Model slip? Different reading of the scale? Gamed content? Or two genuinely defensible ideas of what "relevant" means? Those need completely different fixes.

## 8. Still open

- What happens to your evaluation when the judge model gets retired and you swap in a new one?
- Which disagreements actually change a decision? Most probably don't. And how do you even measure agreement when several answers are legitimately correct?
- How do you catch someone gaming the judge — especially when they write the product text and profit from ranking?
- When should people grade everything, versus review the disagreements, versus spot-check a sample, versus just write the rules and step back?
- Does the prune-cascade-and-train-a-small-model approach pass along the judge's *biases* along with its accuracy? Nobody's really checked what the small model inherits. And the numbers behind it (93% pruned, 75–85% settled cheaply) come from one company's production system, reported by the person who built it. Nobody has reproduced them elsewhere.
- How do you evaluate against a target that keeps moving? Shopping relevance shifts with the season, the culture and what's in stock. Your judge's knowledge is frozen.

## 9. Where that leaves you

Pulling it together, seven things look solid enough to build on.

1. **Agreement on individual grades is never great.** Mediocre is normal. It moves with the data, the model, the prompt, the scale, the context you gave, and who your people were. It gets better when the task is tightly specified.
2. **Leaderboards hold up better than grades.** The judge's mistakes usually land on every approach about equally, so the running order comes out right even when the individual grades are wrong — the wonky tape measure again. But that's a result about *one level, one formula, one dataset*, not proof that judges are interchangeable.
3. **It breaks exactly where you need it most.** Sorting a messy pile of 77 approaches: fine. Telling apart two strong ones that are close: not fine. Separating an exact match from junk: fine. Separating a good substitute from a slightly worse one: weak. Your headline number can look terrific while the winner flips and your "this difference is real" tests fire off false alarms.
4. **The mistakes have a shape.** Too generous. Over-reacting to search words appearing in the text. Twitchy about how the prompt is worded. Following instructions hidden inside documents. Preferring whatever came first. Preferring longer text. Possibly favouring approaches that look like itself, though that one's disputed. And these aren't random slips — the judge makes the *same* mistake every time. **So collecting more grades from the same judge doesn't fix it.** A tape measure that reads short doesn't get more accurate because you measured more planks with it.
5. **Your people aren't a gold standard either.** When the model disagrees with your answer key, "the model screwed up" is one hypothesis, not the conclusion. Sometimes the key is arguable. Sometimes the case is genuinely ambiguous.
6. **Model-versus-model is badly under-studied.** Most papers nail human grades to the wall as truth and ask which model gets closest. Very few cross several model families, several prompts, and repeated runs, then ask the real question: *would my conclusion have changed if I'd picked a different judge?*
7. **In the documented deployments covered here, nobody replaced the people.** Etsy, Allegro and eBay all use people to define the standard, the model to spread it, and business numbers to keep it honest. The research question is "can the model replace the grader." The deployed answer is **"no — it multiplies them."** That's not a consolation prize. That's the actual value.

So the honest position is a middle one, and it isn't a cop-out. Model judges are genuinely useful right now: scaling up grading, extending your coverage, fast exploratory checks, auditing the human grades you already have. On several datasets they reproduce broad leaderboards remarkably well, for a rounding error of the cost.

But the agreement comes with conditions. A strong overall number does not buy you interchangeable grades, fair treatment of your best approaches, trustworthy "this difference is real" tests, or protection from someone gaming the thing. And the closer you get to the decision you actually care about — this approach or that one, this substitute or that one — the less the reassuring aggregate numbers apply.

So stop asking:

> Does the model agree with the human?

Start asking:

> If I swap the judge, change the prompt, or just run it again — which of my conclusions survive, and which ones move?

That's a question you can actually answer. And it treats disagreement as information about your evaluation, which is exactly what it is.

## Worth reading

If you only read three: the [trickery paper](https://arxiv.org/abs/2501.17969), the [top-of-the-table false alarms paper](https://arxiv.org/abs/2411.13212), and [Allegro's write-up](https://blog.allegro.tech/2026/08/automating-search-relevance-llm-as-a-judge.html).

**The foundations**

- [People disagreed first (2000)](https://www.nist.gov/publications/variations-relevance-judgments-and-measurement-retrieval-effectiveness) — and the comparisons survived it anyway. Where the 0.9 rule of thumb comes from.
- [Graders aren't swappable (2008)](https://www.microsoft.com/en-us/research/publication/relevance-assessment-are-judges-exchangeable-and-does-it-matter/) — expertise changes the answer.
- [The 80% result (2023)](https://arxiv.org/abs/2306.05685) — and the names for the four ways a model judge goes wrong.

**The case for**

- [It works at Bing scale (2024)](https://arxiv.org/abs/2309.10621) — and rewording your prompt moves the numbers.
- [Open reproduction (2024)](https://arxiv.org/abs/2406.06519) — checked across five years of benchmark data.
- [77 approaches, 19 teams (2024)](https://arxiv.org/abs/2411.08275) — people were stricter, and adding a human review step didn't pay.

**The case for caution**

- [Unfair at the top, inventing differences (2025)](https://arxiv.org/abs/2411.13212) — the one that should worry you.
- [Keyword stuffing and hidden instructions fool it (2025)](https://arxiv.org/abs/2501.17969) — the one that should worry your security team.
- [Judges favour models like themselves (2025)](https://arxiv.org/abs/2503.19092) — though [another study disagrees](https://arxiv.org/abs/2408.16312).
- [Two adjacent years, very different results (2026)](https://arxiv.org/abs/2601.05603) — and the answer key can be wrong.
- [Weak grades, strong rankings (2026)](https://arxiv.org/abs/2608.27746) — Portuguese legal search.

**From the trenches**

- [Andreas Wagner on making it affordable](https://www.linkedin.com/pulse/towards-scalable-relevance-engineering-andreas-wagner-s3akf/) — prune 93% with shopper behaviour, cheap judges for the rest, then train a small model on what the expensive one taught you.
- [Etsy](https://www.etsy.com/codeascraft/how-etsy-uses-llms-to-improve-search-relevance) — human examples, big model teacher, small model shipped in under 10 milliseconds.
- [Allegro](https://blog.allegro.tech/2026/08/automating-search-relevance-llm-as-a-judge.html) — 380,000 human judgments, good overall, poor exactly where it mattered.
- [eBay](https://arxiv.org/abs/2505.04209) — tie the judge to business metrics or it drifts.
