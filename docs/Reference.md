---
title: C++/BP Reference
---

# C++/BP Reference

Generated doxygen-style documentation of Torn Banner's C++ classes and selected
Blueprints lives in a **separate, independently-built site** so its thousands of
pages don't slow this guide down or crowd its search. Use the box below to search
it, or [open the full reference site](https://knutschbert.github.io/chiv2-tblcpp-mkdocs-clean/).

> [!tip] Two independent searches
> The search box in the header searches **this guide**. The box below searches the
> **C++/BP reference** only — separate data. It matches substrings, so typing
> `TBLPlayerController` finds `ATBLPlayerController`.

<div class="ref-search" data-placeholder="Search C++/BP reference (classes, structs, nodes…)"></div>

## Linking to the reference from any page

Anywhere in the guide you can link a symbol with `[[ref:Name]]`:

- `[[ref:ATBLPlayerController]]` or `[[ref:TBLPlayerController]]` — class (prefix optional)
- `[[ref:SpawnTBLAIFromClass]]` — a Blueprint node/function
- `[[ref:TBLPlayerController::InputPlay]]` — an owner-qualified node (for names that
  repeat across classes)
- `[[ref:ATBLPlayerController|the player controller]]` — custom link text

These resolve to the published reference site on the web build. See the
[[Input Replay Component]] page for a live example.
