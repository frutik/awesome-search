#!/usr/bin/env python3
"""Fast filesystem-based quality audit for the Awesome Search Obsidian vault.

Reads every note once and computes, in a single pass:
  - frontmatter completeness violations (by folder / type)
  - orphan notes (zero inbound and outbound wikilinks)
  - hub ranking (inbound link counts) + Topics/ coverage mismatches
  - connected components (disconnected cluster detection)
  - duplicate articles/videos (same `source`/`url` frontmatter field
    processed into two separate notes)
  - unresolved wikilinks (targets that don't resolve to any note),
    with path-style links (Awesome Search/..., raw_articles/...) broken
    out separately from plain-title gaps

Wikilink parsing handles the backslash-pipe escape Obsidian requires for
aliased links inside markdown tables (target, backslash, pipe, alias,
closing brackets) — an earlier version of this script mis-parsed that
escape as a "broken link", which it isn't.

This is a deliberate exception to the "MCP-only, never raw filesystem
tools" rule the other kg-* skills follow: at ~800+ notes, reading every
file through MCP round-trips is too slow for a periodic health check.
Nothing here writes to the vault — it is read-only analysis. Any fixes
identified from its output should be applied via the Obsidian MCP server
(or the relevant kg-* skill), not by editing files this script touched.

Usage:
    python3 kg_audit.py [--vault PATH] [--output PATH]

Defaults: vault = "<repo_root>/obsidian/vault/Awesome Search" (derived from
this script's location), output = "<repo_root>/.scratchpad/kg_audit_result.json".
"""
import re
import json
import argparse
from pathlib import Path
from collections import defaultdict

FOLDERS = ["Articles", "Videos", "Concepts", "Topics", "People", "Companies",
           "Tools", "Conferences", "Case Studies", "Datasets"]

FRONTMATTER_RE = re.compile(r'^---\n(.*?)\n---\n', re.DOTALL)
WIKILINK_RE = re.compile(r'\[\[(.*?)\]\]')
SOURCE_FIELD_RE = re.compile(r'^(?:source|url)\s*:\s*"?([^"\n]+)"?\s*$', re.MULTILINE)


def extract_wikilink_targets(body):
    """Parse [[Target]] / [[Target|Alias]] / [[Target#Heading]], including the
    \\| escape Obsidian requires for aliased links inside markdown tables."""
    targets = set()
    for inner in WIKILINK_RE.findall(body):
        target = inner.replace("\\|", "|").split("|", 1)[0].split("#", 1)[0].strip()
        if target:
            targets.add(target)
    return targets

REQUIRED_BASE = ["type", "tags", "created"]
REQUIRED_BY_TYPE = {
    "article": ["source", "author", "concepts"],
    "video": ["speaker", "url", "concepts"],
    "concept": [],
    "topic": ["related_concepts"],
    "person": [],
    "company": ["website"],
    "tool": ["website_or_repo"],
    "conference": ["website", "organizer"],
    "case_study": ["companies", "related_concepts", "source"],
    "dataset": ["website_or_repo", "related_concepts"],
}
FOLDER_TO_TYPE = {
    "Articles": "article", "Videos": "video", "Concepts": "concept", "Topics": "topic",
    "People": "person", "Companies": "company", "Tools": "tool", "Conferences": "conference",
    "Case Studies": "case_study", "Datasets": "dataset",
}


def parse_frontmatter(text):
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None, text
    fm_text = m.group(1)
    body = text[m.end():]
    fields = {}
    cur_key = None
    for line in fm_text.split("\n"):
        if re.match(r'^\S[^:]*:', line):
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip()
            fields[key] = val
            cur_key = key
        elif line.strip().startswith("-") and cur_key:
            fields.setdefault(cur_key + "__list", [])
            fields[cur_key + "__list"].append(line.strip()[1:].strip())
    return fields, body


def load_notes(vault):
    notes = {}
    for folder in FOLDERS:
        d = vault / folder
        if not d.exists():
            continue
        for f in sorted(d.glob("*.md")):
            title = f.stem
            text = f.read_text(encoding="utf-8", errors="replace")
            fm, body = parse_frontmatter(text)
            links = extract_wikilink_targets(body)
            fm_match = FRONTMATTER_RE.match(text)
            src_match = SOURCE_FIELD_RE.search(fm_match.group(1)) if fm_match else None
            notes[title] = {
                "path": str(f.relative_to(vault)),
                "folder": folder,
                "fm": fm or {},
                "has_fm": fm is not None,
                "body_len": len(body.strip()),
                "links_out": links,
                "source_field": src_match.group(1).strip() if src_match else None,
            }
    return notes


def audit_frontmatter(notes):
    violations = defaultdict(list)
    for title, n in notes.items():
        fm = n["fm"]
        missing = []
        if not n["has_fm"]:
            missing.append("NO_FRONTMATTER_BLOCK")
        else:
            for field in REQUIRED_BASE:
                if field not in fm and (field + "__list") not in fm:
                    missing.append(field)
            expected_type = FOLDER_TO_TYPE[n["folder"]]
            for field in REQUIRED_BY_TYPE.get(expected_type, []):
                if field == "website_or_repo":
                    if not any(k in fm for k in ("website", "repo")):
                        missing.append("website/repo")
                elif field not in fm and (field + "__list") not in fm:
                    missing.append(field)
            got_type = fm.get("type", "").strip("'\"")
            if got_type != expected_type:
                missing.append(f"type_mismatch(got={got_type!r},expected={expected_type})")
        if missing:
            violations[n["folder"]].append((title, missing))
    return violations


def build_link_graph(notes):
    title_lookup = {t.lower(): t for t in notes}
    inbound = defaultdict(set)
    unresolved = defaultdict(set)
    adj = defaultdict(set)
    for title, n in notes.items():
        for link in n["links_out"]:
            target = title_lookup.get(link.lower())
            if target:
                inbound[target].add(title)
                adj[title].add(target)
                adj[target].add(title)
            else:
                unresolved[title].add(link)
    return title_lookup, inbound, unresolved, adj


def find_orphans(notes, inbound):
    orphans = defaultdict(list)
    for title, n in notes.items():
        if not n["links_out"] and not inbound.get(title):
            orphans[n["folder"]].append(title)
    return orphans


def rank_hubs(notes, inbound, top_n=30):
    ranked = sorted(notes.keys(), key=lambda t: len(inbound.get(t, [])), reverse=True)[:top_n]
    return [(t, notes[t]["folder"], len(inbound.get(t, []))) for t in ranked]


def find_components(notes, adj):
    visited = set()
    components = []
    for title in notes:
        if title in visited:
            continue
        stack = [title]
        comp = set()
        while stack:
            cur = stack.pop()
            if cur in comp:
                continue
            comp.add(cur)
            stack.extend(adj.get(cur, set()) - comp)
        visited |= comp
        components.append(comp)
    components.sort(key=len, reverse=True)
    return components


def external_link_count(notes, title_lookup, comp):
    cnt = 0
    for title in comp:
        for link in notes[title]["links_out"]:
            target = title_lookup.get(link.lower())
            if target and target not in comp:
                cnt += 1
    return cnt


def find_duplicate_sources(notes):
    """Group Articles/Videos by normalized source/url frontmatter field."""
    by_source = defaultdict(list)
    for title, n in notes.items():
        if n["folder"] not in ("Articles", "Videos"):
            continue
        src = n["source_field"]
        if src:
            by_source[src].append(title)
    return {src: titles for src, titles in by_source.items() if len(titles) > 1}


def audit_derived_readme(vault, repo_root):
    """Check that the repo-root README.md is in sync with the vault.

    README.md is a *derived* artifact: its "## Latest Changes" bullets mirror
    the 5 newest History/<year>.<week>.md files, and everything after the
    first `---` separator mirrors global_toc.md with wikilinks converted to
    site links. Any batch that touches either source invalidates it, so the
    drift is silent and cumulative -- this check makes it loud.

    Returns a dict; empty "issues" means in sync.
    """
    readme = repo_root / "README.md"
    issues = []
    if not readme.exists():
        return {"issues": ["README.md missing at repo root"], "expected_weeks": [], "linked_weeks": []}
    text = readme.read_text(encoding="utf-8")

    week_re = re.compile(r"^(\d{4})\.(\d+)\.md$")
    weeks = []
    hist = vault / "History"
    if hist.is_dir():
        for f in hist.iterdir():
            m = week_re.match(f.name)
            if m:
                weeks.append((int(m.group(1)), int(m.group(2))))
    expected = [f"{y}.{w}" for y, w in sorted(weeks, reverse=True)[:5]]

    linked = []
    for m in re.finditer(r"(\d{4})\.(\d+)", text):
        tag = f"{int(m.group(1))}.{int(m.group(2))}"
        if tag not in linked:
            linked.append(tag)
    linked = linked[:5]

    if expected and linked != expected:
        missing = [w for w in expected if w not in linked]
        issues.append(
            f"Latest Changes is stale: links {linked or '[]'}, newest week files are {expected}"
            + (f" (missing: {missing})" if missing else "")
        )

    leaked = text.count("[[")
    if leaked:
        issues.append(f"{leaked} Obsidian wikilink(s) leaked into README.md; all links must be vanilla markdown")

    toc = vault / "global_toc.md"
    if toc.exists():
        toc_text = toc.read_text(encoding="utf-8")
        toc_names = set(re.findall(r"\[\[([^\]]+)\]\]", toc_text))
        # README shows a wikilink's *display* text: the alias after "|" when
        # present, otherwise the last path segment of the target.
        expected_display = set()
        for n in toc_names:
            target, sep, alias = n.partition("|")
            expected_display.add(
                (alias if sep else target.split("#")[0].split("/")[-1]).strip()
            )
        # Entries outside "Awesome Search/" (Clippings/, raw_articles/) are not
        # published, so kg-readme-writer emits them as plain text, not links --
        # accept the display text appearing anywhere in the README.
        linked_titles = {s.strip() for s in re.findall(r"\[([^\]]+)\]\(", text)}
        absent = sorted(d for d in expected_display - linked_titles if d not in text)
        if absent:
            issues.append(f"{len(absent)} global_toc.md entries absent from README.md, e.g. {absent[:8]}")

        # Membership is not enough: a reordered global_toc line leaves the same
        # set of entries but a README that no longer mirrors it. Compare the
        # per-line ordering too.
        toc_lines = [l for l in toc_text.strip("\n").split("\n") if l.strip()]
        rd = text.split("\n")
        try:
            start = rd.index("---", 9) + 1
        except ValueError:
            start = None
        if start is not None:
            stop = next((j for j, l in enumerate(rd) if l.strip() == "## Old List"), len(rd))
            rd_lines = [l for l in rd[start:stop] if l.strip()]
            for n, (rline, tline) in enumerate(zip(rd_lines, toc_lines)):
                want = []
                for m in re.finditer(r"\[\[([^\]]+)\]\]", tline):
                    tgt, sep, alias = m.group(1).partition("|")
                    want.append((alias if sep else tgt.strip().split("/")[-1]).strip())
                got = re.findall(r"\[([^\]]+)\]\(https://frutik", rline)
                # entries rendered as plain text (unpublished notes) are skipped
                seq = [w for w in want if w in got]
                if seq != got:
                    issues.append(
                        f"README TOC line {n} is ordered differently from global_toc.md"
                    )
                    break

    return {"issues": issues, "expected_weeks": expected, "linked_weeks": linked}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    repo_root = Path(__file__).resolve().parents[3]
    ap.add_argument("--vault", type=Path, default=repo_root / "obsidian" / "vault" / "Awesome Search")
    ap.add_argument("--output", type=Path, default=repo_root / ".scratchpad" / "kg_audit_result.json")
    args = ap.parse_args()

    readme_check = audit_derived_readme(args.vault, repo_root)

    notes = load_notes(args.vault)
    fm_violations = audit_frontmatter(notes)
    title_lookup, inbound, unresolved, adj = build_link_graph(notes)
    orphans = find_orphans(notes, inbound)
    hub_data = rank_hubs(notes, inbound)
    components = find_components(notes, adj)

    topic_titles = {t.lower(): t for t in notes if notes[t]["folder"] == "Topics"}
    topics_inbound = {t: len(inbound.get(t, [])) for t in notes if notes[t]["folder"] == "Topics"}
    low_topics = sorted([(t, c) for t, c in topics_inbound.items() if c < 3], key=lambda x: x[1])

    hub_topic_check = []
    for title, folder, count in hub_data:
        if folder != "Concepts":
            continue
        words = set(re.findall(r'\w+', title.lower()))
        match = None
        for tt_lower, tt in topic_titles.items():
            if words & set(re.findall(r'\w+', tt_lower)):
                match = tt
                break
        hub_topic_check.append({"concept": title, "inbound": count, "candidate_topic_match": match})

    comp_summaries = []
    for comp in components:
        if len(comp) < 3:
            continue
        folder_counts = defaultdict(int)
        for t in comp:
            folder_counts[notes[t]["folder"]] += 1
        comp_summaries.append({
            "size": len(comp),
            "external_links": external_link_count(notes, title_lookup, comp),
            "folder_counts": dict(folder_counts),
            "sample_titles": sorted(comp, key=lambda t: -len(inbound.get(t, [])))[:8],
            "all_titles": sorted(comp),
        })

    duplicate_sources = find_duplicate_sources(notes)

    path_style_unresolved = {}
    plain_unresolved = {}
    for title, targets in unresolved.items():
        path_style = {t for t in targets if "/" in t}
        plain = targets - path_style
        if path_style:
            path_style_unresolved[title] = sorted(path_style)
        if plain:
            plain_unresolved[title] = sorted(plain)

    output = {
        "total_notes": len(notes),
        "fm_violations": dict(fm_violations),
        "fm_violation_count": sum(len(v) for v in fm_violations.values()),
        "orphans": dict(orphans),
        "orphan_count": sum(len(v) for v in orphans.values()),
        "hub_data": hub_data,
        "hub_topic_check": hub_topic_check,
        "low_linked_topics": low_topics,
        "components": comp_summaries,
        "total_components": len(components),
        "duplicate_sources": duplicate_sources,
        "duplicate_source_count": len(duplicate_sources),
        "path_style_unresolved_links": path_style_unresolved,
        "plain_unresolved_links": plain_unresolved,
        "unresolved_link_note_count": len(unresolved),
        "readme_sync": readme_check,
        "readme_issue_count": len(readme_check["issues"]),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2, ensure_ascii=False))

    print(f"Notes scanned: {len(notes)}")
    print(f"Frontmatter violations: {output['fm_violation_count']}")
    print(f"Orphans: {output['orphan_count']}")
    print(f"Connected components (>=3 notes): {len(comp_summaries)} / {len(components)} total")
    print(f"Duplicate-source groups (same article processed twice): {len(duplicate_sources)}")
    print(f"Notes with unresolved wikilinks: {output['unresolved_link_note_count']}")
    if readme_check["issues"]:
        print(f"README.md out of sync ({len(readme_check['issues'])}):")
        for msg in readme_check["issues"]:
            print(f"  - {msg}")
        print("  fix: run the kg-readme-writer skill")
    else:
        print("README.md: in sync")
    print(f"Full results written to: {args.output}")


if __name__ == "__main__":
    main()
