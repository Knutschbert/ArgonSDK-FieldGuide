---
name: field-guide-reader-review
description: Review an existing ArgonSDK Field Guide section after drafting or a first technical build for modder usefulness, omitted authoring guidance, evidence accuracy, clarity, diagrams/tables, optional details, reference links, and dual Obsidian/MkDocs rendering. Use for requests to verify or improve a completed section, not for first-draft authoring (use field-guide-docs).
---

# Second-pass reader verification

This is an editorial and evidence review **after** drafting, not merely a
successful build. Use it alongside `field-guide-docs/SKILL.md` and the
repository's `AGENTS.md`. A fresh reviewer is preferable; if the drafter is
also the reviewer, state that the pass was self-review, not independent
verification. Keep fixes scoped to the section and its navigation. Track
substantial, separately scoped changes with Beads before editing.

## Inputs and limits

1. Read the section landing page, every focused page, `.pages`, its parent
   overview, related links, and the documentation skill. Check the working
   tree first; do not overwrite unrelated local edits.
2. Identify the claim authority: a current promotion brief or source records,
   with dated revisions. A newer brief may supersede older Unknown lists while
   older notes still support configuration detail.
3. For each consequential assertion, write a *working* crosswalk in issue notes
   (not a reader page): **page/claim → exact source → Configured / Recovered /
   Observed [ordinary, accelerated, controlled] / Inferred / Unknown**.
   Header declarations and decoded Blueprint branches are available surfaces,
   not recovered native execution or proof of ordinary dispatch. A returned
   object is not necessarily installed, and a negative probe is sample-bounded.
4. If evidence is absent, keep the item Unknown or omit it. Do not launch a
   game, change gameplay state, run broad Ghidra analysis, or manufacture a
   modding recipe to fill a gap. Escalate new research to a separate tracked
   investigation.

## Read as a modder

Ask of each page:

- What is the reader trying to inspect, configure, or understand? Does the
  first paragraph answer that question before naming implementation internals?
- Map the section's main reader questions before deciding where diagrams
  belong. A single overview diagram is rarely enough for a section with
  different ownership, state transitions, and mode-specific branches. Consider
  **several focused diagrams** where they make relationships easier to
  understand: an ownership split, one representative stage chain with its
  terminal branch, and an observed round timeline can each answer a different
  question. Prefer them to dense prose; avoid decorative diagrams or one giant
  all-modes flowchart. Keep the adjacent table for exact values when useful.
- For every proposed arrow, ask **what establishes this edge**: configured
  successor wiring, recovered implementation, an ordinary observation, an
  accelerated expiry, a controlled test, or inference? Label the diagram's
  scope and evidence in its introduction or on the relevant edge. Never join
  two separate experiments into a continuous flow, label a configured edge as
  observed, draw an unobserved natural caller, or turn an object's return into
  current-stage installation. Omit a speculative arrow rather than disguising
  it with a dashed line. State unobserved branches nearby as Unknown.
- Use concise, familiar node labels and choose a readable direction (including
  on narrow screens). Every nontrivial Mermaid diagram needs an immediately
  adjacent `Plaintext:` explanation that recovers its nodes, transitions,
  evidence qualifier, and most important Unknown when Mermaid is unavailable.
  Don't hard-code colors in the diagram; use shared styling and inspect both
  Material schemes. Check arrows/labels don't overlap in rendered output.
- Would a mode comparison, property matrix, or outcome table clarify values,
  units, and boundaries? Avoid tables that only repeat paragraphs.
- For an authoring topic, are the verified class names, World Settings,
  settings instances, level hooks, actors, and initialization/termination
  relationships discoverable? Distinguish a **sampled shipped-map example**
  from a tested new-map recipe. Never say a hook *must* be used merely because
  it exists in an export.
- Are unfamiliar terms defined and are related systems linked? Keep the key
  distinction and operational Unknowns visible. Collapse **optional**
  examples, glossaries, long inventories, or experimental contrasts with
  `??? "Title"` where supported; never hide a safety or evidence caveat.
- Can the reader act on a referenced API name? Check
  `hooks/reference-inventory.json` `links` keys before adding `[[ref:…]]`.
  Prefer a few meaningful native/class/interface links over a link on every
  noun. The reference is a separate website and bare `[[ref:…]]` currently
  shows as text in Obsidian; retain enough local explanation to stand alone.
- Is the prose needlessly dominated by “sampled,” “controlled,” or tracker
  language? Preserve the qualification beside its claim but write the main
  sentence for a human reader. Avoid raw addresses, hashes, paths, issue
  history, capture procedures, and unneeded instance suffixes.

## Verify the artifact

1. Compare adjacent pages for contradictory counts, labels, scope, and
   terminology. Keep focused filenames unique across the vault (RoamLinks
   resolves by filename); use relative Markdown links for README/TLDR and
   primary navigation. Check the section and parent `.pages`.
2. Run the documented MkDocs build, inspect warnings **and rendered output**.
   Confirm new `[[ref:…]]` URLs, `???` content, tables, and Mermaid appear as
   intended. Check the Obsidian Markdown reading experience; for new
   diagrams/theme styling, check Material light and dark schemes and plaintext
   fallback. Note unrelated pre-existing warnings separately.
3. Run `git diff --check` and inspect changed/untracked files. Do not commit,
   push, or sync without owner authority.
4. Report: **critical factual fixes**, **modder usability changes**, **optional
   polish**, **evidence still Unknown**, and **validation result** with paths.
   Name unperformed checks honestly. Close only issues whose acceptance
   criteria passed. A build alone is not an editorial verdict.

## Calibration examples

- **Stages:** a successful build would not reveal that a modder still needs
  the World Settings/level-hook/placed-stage matrix or that a direct FFA
  completion return is not a current-stage installation.
- **Spawns:** a placed spawner is not a dispatched respawn. Keep the uncertain
  admission path visible even if a component table and diagram are otherwise
  clear.
- **Bot Behavior:** an authored candidate list is not an observed decision
  winner. Keep the configuration/selection distinction visible and collapse
  only optional details.
