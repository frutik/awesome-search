---
name: kg-readme-writer
description: Keep README.md at the repo root (not in the Obsidian vault) in sync with the Awesome Search KG — links to the 5 latest History week files plus the full content of global_toc.md, with every wikilink converted to a vanilla markdown link. Modifies the existing file in place with targeted edits; never regenerates it from scratch. Invoke after vault changes, or on `/kg-readme-writer`.
---

# Awesome Search KG — README Writer

Maintains `README.md` in the **repository root**. This is a published artifact of the vault, not a vault note — never write it inside `obsidian/vault/`, and vault note conventions (approval, history entries, kg-reviewer) do not apply.

**Update in place, don't regenerate.** Read the existing `README.md`, compare it against the current vault state, and apply only the edits needed to bring it back in sync (Edit tool, targeted `old_string`/`new_string` replacements). Do not rewrite the whole file, and do not use scripts to rebuild it. Only if the file does not exist at all, create it once with the structure below.

## Output contract

`README.md` contains, in order:

1. `# Awesome Search — Knowledge Graph` title heading.
2. `## Latest History` — a bullet list linking the **5 most recent** `Awesome Search/History/<year>.<week>.md` files (sorted by `year.week` descending; `History Stats.md` and other non-week files excluded).
3. A `---` separator.
4. The **full content** of `Awesome Search/global_toc.md` (frontmatter stripped), with wikilinks converted.

## Link format

All links must be **vanilla markdown links** — `[text](url)` — never Obsidian `[[wikilinks]]`. Links point at the published site, `https://frutik.github.io/awesome-search/`, which serves the vault's `Awesome Search/` folder:

- Resolve a wikilink target by finding the matching `.md` file (by filename stem) under `obsidian/vault/`; path-style targets like `[[Awesome Search/Topics/Foo]]` resolve against the vault root, with the last path segment as display text.
- Build the URL from the note's path relative to `obsidian/vault/Awesome Search/`, **without the `.md` extension**, slugified the way Quartz does (the site is built with Quartz — do **not** URL-encode): in each path segment, first replace every whitespace character with `-`, then `&` → `-and-` (so `A & B` becomes `A--and--B`), then `%` → `-percent`, and delete `?` and `#`. All other characters (parentheses, apostrophes, commas, accented letters, …) stay as-is. Prefix with the site base. E.g. `[[Bayesian BM25]]` → `[Bayesian BM25](https://frutik.github.io/awesome-search/Concepts/Bayesian-BM25)`; `[[All about Information Retrieval & Search]]` → `.../All-about-Information-Retrieval--and--Search`; `[[Note|alias]]` uses `alias` as display text.
- Never emit `obsidian/vault/...` repo paths.
- Notes **outside** `Awesome Search/` (e.g. `Clippings/`, `raw_articles/`) are not published on the site: keep their display text as plain text, no link.
- If no file matches a wikilink target, keep the display text as plain text — never emit a broken link — and report the unresolved name.

## Procedure

1. Read `README.md` and the current vault state: the list of `History/<year>.<week>.md` files, and `Awesome Search/global_toc.md`.
2. **History section**: if the 5 newest week files differ from the bullets in `## Latest History`, edit just those bullet lines.
3. **TOC section**: diff the README's TOC portion (everything after the `---` separator) against the current `global_toc.md` (after mentally applying the wikilink conversion). Apply targeted edits only to the lines that changed — added notes, renamed notes, removed notes, new sections. Leave untouched lines alone.
4. Verify after editing: `grep -c '\[\[' README.md` must return 0 (no wikilinks leaked in).
5. If any wikilink target in `global_toc.md` doesn't resolve to a note file, report those names to the user — they usually indicate a renamed or missing note. Do not silently create notes to satisfy them.
6. Confirm in your summary: which history links changed, how many TOC lines were edited, and any unresolved wikilinks.
