# Contributing to Awesome Search

Thanks for wanting to add something. Please read this first — this repo does
not work like the awesome-list it superficially resembles, and the difference
is the reason most contributions need rework.

## What this actually is

Not a curated list of links. It is a **knowledge graph**: an Obsidian vault of
some 890 interlinked Markdown notes about search and information retrieval —
525 entity notes plus the article and video source notes behind them —
published as a static site at
[frutik.github.io/awesome-search](https://frutik.github.io/awesome-search/).

An entry here is not a line in a list. It is a *note* — with typed
frontmatter, prose grounded in checkable sources, and dense mutual links to
the notes around it. The README you may have arrived from is generated output,
not the content.

## A pull request is a nomination, not a patch

This is the part that surprises people, so it is stated plainly:

**Your diff will almost certainly not be merged as written, even if we accept
your subject.** Notes are written by a maintainer-run pipeline that fetches
primary sources, derives placement from the graph's existing structure, and
generates the cross-links. The folder you chose, the section you filed under,
your frontmatter and your prose are read as *evidence of what you think the
thing is*. Sometimes they turn out to be right. They are never adopted just
because they arrived in a diff.

The practical consequence: **a well-argued issue is worth as much as a PR.** If
you would rather open an issue that says "X belongs here, here is why, here are
the primary sources," that is a completely valid contribution and it saves you
writing a note that gets rewritten.

## What clears the bar

The question asked of every proposal is: *does this fill a gap in the graph,
with substance a reader can check?*

- **Documented technical substance about search or IR.** Index structures,
  ranking approaches, evaluation methodology, query understanding, a real
  deployment with published results. A company or product qualifies through
  what it has *published* about its search work — not through existing.
- **A gap, not a fourth instance.** Something with no representative in the
  graph — an engine lineage, a distinct architectural position, a technique
  nothing else covers — is a much stronger case than another entry in a
  well-covered category.
- **Primary sources beat positioning.** A landing page, a README's own
  summary, and a pitch are marketing. The manual, the paper, the API docs, the
  engineering blog post are evidence. Link to the latter.
- **Self-published benchmarks are quarantined.** "N× faster than X" on a
  self-chosen workload with the baseline's tuning unspecified can appear in a
  note only as *the project's own claim*, attributed. If there is no
  independent replication, say so — we will check anyway.

Things that do not clear it, however good they may be: products with nothing
published about how their retrieval works, directories and link aggregators,
and anything whose case rests entirely on its own copy.

## Disclose affiliation

If you built it, work there, or are being paid to place it — **say so in the
PR or issue body.** One sentence.

Disclosure is never on its own grounds for rejection, and it is treated as a
mark in your favour. It changes how we research the subject (harder, from
primary sources only), not whether we will. Undisclosed affiliation that
becomes obvious from the diff or your account is worse for you than disclosure
ever is.

## Never edit generated files

These are overwritten by their generators. A hand-edit to any of them is lost
at the next maintenance pass, no matter how good the content:

| Path | Generated from |
|---|---|
| `README.md` | `global_toc.md` + the newest History weeks |
| `docs/` | the vault, via Quartz (`build-web.sh`) |
| `mails/<year>.<week>.html` | that week's History file |
| `drafts/html/<stem>.html` | `drafts/<stem>.md` |
| `obsidian/vault/**/global_toc.md`, `HOME.md`, `index.md` | the vault's note set |

Hand-authored, safe to edit: `obsidian/vault/**` notes, `drafts/*.md`, and the
standalone lists `PAPERS.md`, `QUOTES.md`, `TALKS.md`,
`UNDERFUNDED_SEARCH_TEAMS.md`.

## If you do write a note

Not required — see "a pull request is a nomination" above — but if you want to,
these are the conventions:

**Folders and types.** `Concepts/` (`type: concept`), `Topics/`
(`type: topic`), `People/` (`type: person`), `Companies/` (`type: company`),
`Tools/` (`type: tool`), `Conferences/` (`type: conference`), `Case Studies/`
(`type: case_study`), `Datasets/` (`type: dataset`). `Articles/` and `Videos/`
are source notes and are generated when a source is processed — don't
hand-write them.

**Frontmatter** always carries `type:` plus type-specific fields — `website:`
and `repo:` for tools, `website:` for companies, `affiliation:` for people,
`companies:`/`source:` for case studies.

**Every note links out.** All 525 entity notes currently in the vault contain
at least one `[[wikilink]]` to another note — there are no exceptions. A note
that links to nothing is an orphan and gets flagged by the audit tooling. If
you cannot find anything in the graph to link your subject to, that is usually
the graph telling you it does not fit.

**Grounding is mandatory and invisible.** Every specific claim — a number, a
date, a quote, a name, an affiliation, "X invented Y" — must trace to a
source. Nothing is written from memory. Do not leave citation scaffolding or
notes-to-self about grounding in the text; the prose should read cleanly and
simply be true.

## What happens to your PR

It is evaluated against the criteria above: the subject researched
independently from primary sources, the verified facts separated from the
unverifiable claims, and the result reported as a verdict on **the subject**,
with a separate note on how the contribution was made. You will get a straight
answer either way, including when the answer is no and why.

Please don't take a rejection of the patch as a rejection of the subject —
they are decided separately, and the first happens far more often than the
second.
