"""
MkDocs hook: resolve `[[ref:Symbol]]` wiki-style links into the separately-built
C++/BP reference site, using docs/assets/reference-inventory.json.

Syntax (in any docs page):
    [[ref:ATBLPlayerController]]            -> link, text = ATBLPlayerController
    [[ref:TBLPlayerController]]             -> same page (prefix-stripped alias)
    [[ref:ATBLPlayerController|the PC]]     -> link, custom text "the PC"
    [[ref:ATBLPlayerController#members]]    -> link to an anchor on that page

Unresolved symbols are left as plain text and logged as a warning (the build does
not fail). Regenerate the inventory with hooks/gen_reference_inventory.py whenever
the reference content changes.
"""
import json
import logging
import os
import re

import mkdocs.plugins

log = logging.getLogger("mkdocs.hooks.ref_links")


# `ref:` is this hook's own link namespace. The roamlinks plugin scans raw
# markdown (including code blocks) and warns about any [[...]] it can't resolve
# to a file, so it emits false "unable to find ref:..." warnings for our links
# and for the syntax examples on the Reference page. Drop exactly those records,
# leaving all genuine roamlinks warnings intact.
class _DropRefWarnings(logging.Filter):
    def filter(self, record):
        return "unable to find ref:" not in record.getMessage()


_ref_filter = _DropRefWarnings()
for _name in ("mkdocs.plugins.mkdocs_roamlinks_plugin.plugin",
              "mkdocs.plugins.mkdocs_roamlinks_plugin"):
    logging.getLogger(_name).addFilter(_ref_filter)
for _h in logging.getLogger("mkdocs").handlers:
    _h.addFilter(_ref_filter)

_INVENTORY_PATH = os.path.join(os.path.dirname(__file__), "reference-inventory.json")

_REF_RE = re.compile(
    r"\[\[ref:\s*"
    r"(?P<sym>[^\]|#]+?)\s*"          # symbol
    r"(?:#(?P<frag>[^\]|]+?))?\s*"     # optional #anchor
    r"(?:\|\s*(?P<text>[^\]]+?)\s*)?"  # optional |display text
    r"\]\]"
)

# Code regions to leave untouched: fenced blocks and inline code spans.
_CODE_RE = re.compile(r"(```.*?```|~~~.*?~~~|``.+?``|`[^`\n]*`)", re.S)

_links = None
_missing = set()


def _load():
    global _links
    if _links is not None:
        return _links
    try:
        with open(os.path.normpath(_INVENTORY_PATH), "r", encoding="utf-8") as fh:
            _links = json.load(fh).get("links", {})
        log.info("ref_links: loaded %d reference link keys", len(_links))
    except (OSError, ValueError) as exc:
        log.warning("ref_links: could not load reference inventory (%s); "
                    "[[ref:...]] links will not resolve", exc)
        _links = {}
    return _links


@mkdocs.plugins.event_priority(50)  # run before roamlinks (default priority 0)
def on_page_markdown(markdown, page=None, config=None, files=None, **kwargs):
    links = _load()
    if not links or "[[ref:" not in markdown:
        return markdown

    def repl(m):
        sym = m.group("sym").strip()
        frag = m.group("frag")
        text = m.group("text") or sym
        url = links.get(sym)
        if not url:
            key = sym.lower()
            if key not in _missing:
                _missing.add(key)
                src = getattr(getattr(page, "file", None), "src_uri", "?")
                log.warning("ref_links: unresolved [[ref:%s]] (in %s)", sym, src)
            return text  # leave as plain text, don't break the build
        if frag:
            url = url + "#" + frag.strip()
        return f"[{text}]({url})"

    # Split out code regions (odd indices) and only rewrite the prose between them.
    parts = _CODE_RE.split(markdown)
    for i in range(0, len(parts), 2):
        if "[[ref:" in parts[i]:
            parts[i] = _REF_RE.sub(repl, parts[i])
    return "".join(parts)
