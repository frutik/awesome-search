# Duplicate note names across Concepts/ and Topics/ break 93 notes' links

**Status:** open
**Found:** 2026-08-07, while fixing the Quartz folder-page link bug (`b602e6ad8`)

## Symptom

Three published URLs 404, and every wikilink to them from anywhere in the vault
lands on the 404 page:

```
https://frutik.github.io/awesome-search/A-B-Testing-for-Search   404
https://frutik.github.io/awesome-search/Economics-of-Search      404
https://frutik.github.io/awesome-search/Search-Observability     404
```

The notes themselves are published fine at their real paths
(`/Topics/Economics-of-Search`, `/Concepts/Search-Observability`, …) — only the
links pointing at them are dead.

## Cause

Each of those three names exists as a file in **both** `Concepts/` and `Topics/`:

```
Awesome Search/Concepts/A-B Testing for Search.md      126 B
Awesome Search/Topics/A-B Testing for Search.md      9,254 B
Awesome Search/Concepts/Economics of Search.md         123 B
Awesome Search/Topics/Economics of Search.md         5,009 B
Awesome Search/Concepts/Search Observability.md      2,370 B
Awesome Search/Topics/Search Observability.md       16,244 B
```

They are the only duplicated basenames in the vault:

```sh
find "obsidian/vault/Awesome Search" -name '*.md' -exec basename {} \; | sort | uniq -d
```

Quartz is configured with `markdownLinkResolution: "shortest"`
(`quartz/quartz.config.ts:72`). Shortest resolution needs exactly one candidate
for a bare `[[Name]]`; with two it cannot pick, falls back to a root-level slug,
and emits `href` to `/A-B-Testing-for-Search`, which nothing writes. Obsidian is
unaffected — it disambiguates interactively — so the breakage is invisible while
editing and only appears on the published site.

## Blast radius

| Name | Notes linking it |
|---|---|
| A-B Testing for Search | 63 |
| Economics of Search | 16 |
| Search Observability | 14 |

Counted with `grep -rlE --include='*.md' "\[\[<name>(\]\]|\|)"`. The links are
spread across Concepts, Topics, Articles and the section MOCs, so this is not
confined to one corner of the graph.

## Notes on each case

**A-B Testing for Search** and **Economics of Search** — the `Concepts/` copies
are not real notes. They are `type: redirect` stubs left behind by a move to
`Topics/` on 2026-05-16, whose entire body is:

```markdown
> This note has moved. See [[A-B Testing for Search]] in Topics.
```

The stub's own link is ambiguous in exactly the same way, so the redirect does
not even redirect — it 404s.

**Search Observability** is a genuine duplicate: both files are substantive
notes (a concept definition and a topic page) that were written independently,
2026-06-01 and later. `Topics/Search Observability.md` lists
`related_concepts: ["[[Search Observability]]"]`, i.e. it links ambiguously to
its own name.

## Fix options

1. **Delete the two redirect stubs** (`Concepts/A-B Testing for Search.md`,
   `Concepts/Economics of Search.md`). The name becomes unique, and all 79
   inbound links resolve to the `Topics/` note with no edits anywhere else.
   Obsidian's own link resolution already sends readers to the Topics note, so
   nothing is lost.
2. **Decide what `Search Observability` is** — one note or two. If two, one must
   be renamed (e.g. the topic page to `Search Observability (Topic)`), and the
   14 inbound links plus the self-referential `related_concepts` entry updated.
   If one, merge the concept definition into the topic page and delete the
   other.

## Guard

Nothing currently catches a new duplicate basename. The `uniq -d` command above
is a one-liner that could run in `build-web.sh` next to `fix-folder-pages.py`,
or as a check in one of the vault audit skills
(`awesome-search-kg-frontmatter` already walks every note).
