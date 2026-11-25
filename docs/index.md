# ArgonSDK Field Guide

A community field guide for modding **Chivalry 2** with [ArgonSDK](https://github.com/Chiv2-Community/ArgonSDK) — the unofficial Unreal Engine 4 project that mirrors Torn Banner's development environment.

> [!tip] New here? Start with the [[Introduction]], then check the [[Requirements]] and pick a walkthrough from the [[Tutorials Overview]].

## Start here

- **[[Introduction]]** — what ArgonSDK is, assets, and the mod development process
- **[[Requirements]]** — tools and project setup you need before you begin
- **[[Tutorials Overview]]** — step-by-step: cosmetic and gameplay mods
- **[[Chivalry 2 Systems Overview]]** — how Torn Banner's systems work (spawns, maps, bots, abilities)
- **[[Glossary]]** — terms used throughout the guide

## Purpose of this guide

1. Explain how to mod Chivalry 2 using [ArgonSDK](https://github.com/Chiv2-Community/ArgonSDK), concisely.
2. Aggregate the knowledge collected by the modding community in one place.

## What's covered

- General modding concepts for Chivalry 2
- [[Tutorials Overview|Tutorials]] for creating cosmetic and gameplay mods
- Overviews and details of the systems built by Torn Banner — the spawn system, weapons, game modes and objectives, bot behavior, and more

> [!note] Growing guide
> Some areas are still being written, including a tools-and-resources section and case studies of mods released by [Chivalry 2 Unchained](https://discord.com/invite/chiv2unchained) (GiantSlayers, FilthyPeasants, FlashBlades). Have something to contribute? Reach out on Discord.

## Two ways to read it

This guide is available in two versions:

#### 1. [Obsidian.md](https://obsidian.md/) vault (this repository)

![[FG_View_Obsidian.png]]

> [!tip] Nihi
> This guide is written and maintained in the Obsidian note-taking app. It offers better search and navigation than the web version — see [(LOCAL) Obsidian vs. Web Version](Glossary/ArgonSDK.md).

#### 2. Exported [web version](https://knutschbert.github.io/ArgonSDK-FieldGuide/)

![[FG_View_Web.png]]

## C++ class documentation

Generated doxygen-style documentation of Torn Banner's C++ classes and selected Blueprints is available [here](https://github.com/Chiv2-Community/chiv2-tblcpp-obsidian-clean). It provides:

- Class function names and arguments
- Class properties and their access levels
- Blueprint node previews (where applicable)

> [!important]
> This documentation is currently available only as an Obsidian vault.

![[Readme_obs_preview.png]]

![[Readme_obs_graph.png]]

## BlueprintUE embeds

Several pages embed a self-hosted version of [BlueprintUE](https://blueprints.polehammer.net/):

- Copy-paste the embedded snippets directly into Unreal Engine's Blueprint editor.
- Create and share your own snippets with other users.

<iframe src="https://blueprints.polehammer.net/render/p7ursbys/" scrolling="no" allowfullscreen width="100%" height="300"></iframe>

> [!fail]
> If you can't see the embed above this note, please leave a message on Discord.
