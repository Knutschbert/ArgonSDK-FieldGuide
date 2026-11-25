#!/usr/bin/env python3
"""
Generate reference-inventory.json for the C++/BP reference cross-links.

Scans the separately-built reference MkDocs project (chiv2-tblcpp-mkdocs-clean)
and emits a single JSON file that powers BOTH:

  * the build-time `[[ref:Symbol]]` link hook (hooks/ref_links.py), and
  * the client-side reference search box (docs/javascripts/ref-search.js).

The reference site is built and published independently; this script only reads
its Markdown source to map each symbol -> published URL. Re-run it whenever the
reference content changes.

Writes two files:
  * --links-out  (default hooks/reference-inventory.json): symbol/alias -> URL map,
    read at build time by hooks/ref_links.py. Not published (kept out of docs/).
  * --search-out (default docs/assets/reference-search.json): a small
    [{name,url,kind}] list, published and fetched by the client-side search box.

Usage:
    python3 hooks/gen_reference_inventory.py \
        [--src /path/to/chiv2-tblcpp-mkdocs-clean/docs] \
        [--base https://knutschbert.github.io/chiv2-tblcpp-mkdocs-clean/] \
        [--links-out hooks/reference-inventory.json] \
        [--search-out docs/assets/reference-search.json]
"""
import argparse
import json
import os
import re
import sys

DEFAULT_SRC = "/mnt/p/code/chiv/2026/chiv2-tblcpp-mkdocs-clean/docs"
DEFAULT_BASE = "https://knutschbert.github.io/chiv2-tblcpp-mkdocs-clean/"
DEFAULT_LINKS_OUT = "hooks/reference-inventory.json"
DEFAULT_SEARCH_OUT = "docs/assets/reference-search.json"

# Doxygen-style filename prefixes to strip when deriving a symbol from a filename.
FILE_PREFIXES = ("class", "struct", "namespace", "interface", "union", "group", "dir")
# Unreal type prefixes: a single capital followed by another capital (AFoo, UFoo, FFoo, EFoo...).
UE_PREFIX_RE = re.compile(r"^[AUFEIST](?=[A-Z])")

TITLE_RE = re.compile(r"^title:\s*(.+?)\s*$")
ALIASES_RE = re.compile(r"^aliases:\s*(.+?)\s*$")


def read_front_matter(path):
    """Return (title, [aliases]) from a page's YAML front matter, if present."""
    title, aliases = None, []
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            first = fh.readline()
            if first.strip() != "---":
                return title, aliases
            for _ in range(40):  # front matter is tiny; cap the scan
                line = fh.readline()
                if line == "" or line.strip() == "---":
                    break
                m = TITLE_RE.match(line)
                if m:
                    title = m.group(1).strip().strip('"').strip("'")
                    continue
                m = ALIASES_RE.match(line)
                if m:
                    raw = m.group(1).strip().strip("[]")
                    aliases = [a.strip().strip('"').strip("'") for a in raw.split(",") if a.strip()]
    except OSError:
        pass
    return title, aliases


def url_for(rel_md, base):
    """Map a docs-relative .md path to its published directory-URL."""
    rel = rel_md[:-3]  # drop .md
    parts = rel.split("/")
    if parts[-1].lower() in ("index", "readme"):
        parts = parts[:-1]
    path = "/".join(parts)
    return base.rstrip("/") + "/" + (path + "/" if path else "")


def symbol_from_filename(stem):
    for p in FILE_PREFIXES:
        if stem.startswith(p) and len(stem) > len(p) and stem[len(p)].isupper():
            return stem[len(p):]
    return stem


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=DEFAULT_SRC)
    ap.add_argument("--base", default=DEFAULT_BASE)
    ap.add_argument("--links-out", dest="links_out", default=DEFAULT_LINKS_OUT)
    ap.add_argument("--search-out", dest="search_out", default=DEFAULT_SEARCH_OUT)
    args = ap.parse_args()

    if not os.path.isdir(args.src):
        sys.exit(f"reference docs dir not found: {args.src}")

    entries = []          # [{name, url, kind}] for the search box
    name_to_url = {}       # primary lookup for the link hook
    collisions = set()

    def add_alias(alias, url):
        if not alias:
            return
        if alias in name_to_url and name_to_url[alias] != url:
            collisions.add(alias)
        else:
            name_to_url[alias] = url

    for root, _dirs, files in os.walk(args.src):
        for fn in files:
            if not fn.endswith(".md"):
                continue
            full = os.path.join(root, fn)
            rel = os.path.relpath(full, args.src).replace(os.sep, "/")
            stem = fn[:-3]
            url = url_for(rel, args.base)
            title, aliases = read_front_matter(full)

            symbol = title or symbol_from_filename(stem)
            kind = "page"
            for p in FILE_PREFIXES:
                if stem.startswith(p) and stem[len(p):len(p) + 1].isupper():
                    kind = p
                    break

            entries.append({"name": symbol, "url": url, "kind": kind})

            # Lookup keys: the symbol, its explicit aliases, the raw filename stem,
            # and a copy with the leading Unreal type prefix stripped.
            add_alias(symbol, url)
            for a in aliases:
                add_alias(a, url)
            add_alias(stem, url)
            stripped = UE_PREFIX_RE.sub("", symbol)
            if stripped != symbol:
                add_alias(stripped, url)

            # BP node/function pages live at <Owner>/nodes/<Node>.md — add
            # owner-qualified keys so names that repeat across owners (e.g.
            # InputPlay) can be disambiguated as Owner::Node / Owner.Node.
            parts = rel.split("/")
            if len(parts) >= 3 and parts[-2] == "nodes":
                owner = parts[-3]
                owner_alts = {owner, UE_PREFIX_RE.sub("", owner)}
                for ow in owner_alts:
                    add_alias(ow + "::" + symbol, url)
                    add_alias(ow + "." + symbol, url)

    # Drop ambiguous aliases so a link never silently points at the wrong page.
    for c in collisions:
        name_to_url.pop(c, None)

    entries.sort(key=lambda e: e["name"].lower())
    src_name = os.path.basename(os.path.dirname(args.src.rstrip("/")))

    # 1) links map — read at build by the hook; kept out of docs/ (not published).
    links_doc = {
        "base": args.base,
        "generated_from": src_name,
        "links": name_to_url,
        "ambiguous": sorted(collisions),
    }
    os.makedirs(os.path.dirname(args.links_out) or ".", exist_ok=True)
    with open(args.links_out, "w", encoding="utf-8") as fh:
        json.dump(links_doc, fh, ensure_ascii=False, separators=(",", ":"))

    # 2) search list — small, published, fetched by the client search box.
    search_doc = {
        "base": args.base,
        "generated_from": src_name,
        "count": len(entries),
        "entries": entries,
    }
    os.makedirs(os.path.dirname(args.search_out) or ".", exist_ok=True)
    with open(args.search_out, "w", encoding="utf-8") as fh:
        json.dump(search_doc, fh, ensure_ascii=False, separators=(",", ":"))

    print(f"links: {args.links_out} ({len(name_to_url)} keys, {len(collisions)} ambiguous dropped)")
    print(f"search: {args.search_out} ({len(entries)} entries)")


if __name__ == "__main__":
    main()
