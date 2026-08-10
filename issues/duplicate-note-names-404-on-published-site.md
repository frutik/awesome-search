# Duplicate note names across Concepts/ and Topics/ break links on the published site

**Status:** closed
**Found:** 2026-08-07, while fixing the Quartz folder-page link bug (`b602e6ad8`)
**Fixed:** 2026-08-10 — all three `Concepts/` files deleted. The vault now has
zero duplicated basenames, so every bare `[[Name]]` resolves and the three URLs
below are live. See *Resolution* at the bottom.

## Symptom

Three published URLs 404, and every bare wikilink to them from anywhere in the
vault lands on the 404 page:

```
https://frutik.github.io/awesome-search/A-B-Testing-for-Search   404  (fixed)
https://frutik.github.io/awesome-search/Economics-of-Search      404  (fixed)
https://frutik.github.io/awesome-search/Search-Observability     404  (open)
```

The notes themselves are published fine at their real paths
(`/Topics/Economics-of-Search`, `/Concepts/Search-Observability`, …) — only the
links pointing at them are dead.

## Cause

Each of those three names existed as a file in **both** `Concepts/` and `Topics/`
(the two marked *deleted* were removed on 2026-08-10):

```
Awesome Search/Concepts/A-B Testing for Search.md      126 B   deleted
Awesome Search/Topics/A-B Testing for Search.md      9,254 B
Awesome Search/Concepts/Economics of Search.md         123 B   deleted
Awesome Search/Topics/Economics of Search.md         5,009 B
Awesome Search/Concepts/Search Observability.md      2,370 B   deleted
Awesome Search/Topics/Search Observability.md       16,244 B
```

`Search Observability` is now the only duplicated basename left in the vault:

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

The broken links are spread across Concepts, Topics, Articles and the section
MOCs, so this is not confined to one corner of the graph. `A-B Testing for Search`
is by far the most linked of the three; `Search Observability` the least.

Only **bare** `[[Name]]` links break. Path-qualified links
(`[[Awesome Search/Topics/Economics of Search|Economics of Search]]`, used in
places in `global_toc.md`) are unambiguous and resolve correctly.

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

1. ~~**Delete the two redirect stubs**~~ — **done 2026-08-10.**
   `Concepts/A-B Testing for Search.md` and `Concepts/Economics of Search.md`
   were deleted. Both names are now unique and every bare inbound link resolves
   to the `Topics/` note. The only other edits needed were removing the two
   path-qualified `Concepts/` entries from `global_toc.md` (and their mirror in
   `README.md`), which would otherwise have dangled. Nothing was lost — the
   stubs' only content was a redirect line that itself 404'd.
2. ~~**Decide what `Search Observability` is**~~ — **done 2026-08-10.** Resolved
   as *one note, a topic*. `Concepts/Search Observability.md` was deleted; the
   topic page already covered its definition, its three-planes table, and the
   SQA/A-B contrast in more depth, so the only thing merged across was the alias
   `production search monitoring`. The self-referential `related_concepts:
   ["[[Search Observability]]"]` entry was removed.

## Resolution

All three `Concepts/` files are gone and `uniq -d` over the vault now returns
nothing. Bare `[[Name]]` links resolve everywhere, so no link edits were needed
in the ~90 notes that reference these names.

Index files were updated to drop the deleted concepts: `global_toc.md` (Concepts
sections), `Concepts.md`, and the `README.md` mirror. The path-qualified
`[[Awesome Search/Topics/…|…]]` workaround links in `global_toc.md` were
simplified back to bare, now that the names are unambiguous.

The path-qualified `[[Awesome Search/Topics/…|…]]` links to these three names —
in `Extreme Search Systems`, `Multi-Tenancy in Search`, `Sharding`,
`Compute-Storage Disaggregation`, `Erik Hatcher`,
`Survey of the Hybrid Search Landscape` and `Vector Podcast` — were also
shortened to bare links. That was not merely cosmetic: the path-qualified form
is itself broken on the published site, which is now tracked separately in
[Path-qualified links 404 on the published site](path-qualified-links-404-on-published-site.md).

## Guard

Nothing currently catches a new duplicate basename. The `uniq -d` command above
is a one-liner that could run in `build-web.sh` next to `fix-folder-pages.py`,
or as a check in one of the vault audit skills
(`awesome-search-kg-frontmatter` already walks every note).
