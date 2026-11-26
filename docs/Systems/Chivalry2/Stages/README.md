# Chivalry 2 stages and rounds

If you are inspecting a map or making a mod, the first question is whether the
mode expects a stage actor from the level or owns its own match lifecycle. This
section explains how sampled Chivalry 2 matches move toward a result. It covers
the stage actors used by Free-for-All (FFA),
Team Deathmatch (TDM), and Team Objective (TO), alongside the native round
state observed in Last Team Standing (LTS) and Arena.

## Start here

[Read the TL;DR first.](TLDR.md)

The smallest useful model is not one universal stage system:

1. In the sampled **FFA** and **TO** maps, placed stage actors were active.
2. In sampled **TDM**, the mode created its ticket stage at runtime.
3. In sampled **LTS** and **Arena**, native round and life state was visible on
   the game mode and game state; no stage-interface actor was observed in those
   bounded samples.

These are observations of representative maps, not a classification rule for
every Chivalry 2 map.

> [!warning] The guide's most important reading rule
> A configured hook, placed actor, or decoded implementation is not proof that
> it ran in an ordinary match. This guide marks whether a claim is
> **Configured**, **Recovered**, **Observed**, or **Unknown**, and identifies
> controlled and accelerated observations rather than presenting them as normal
> gameplay.

## Reading paths

| If you want to understand… | Read… |
|---|---|
| The shortest correct mental model | [Stages and rounds TL;DR](TLDR.md) |
| Which layer owns a stage or round | [Stage and round overview](stages-overview.md) |
| How FFA, TDM, and TO differ as staged modes | [Staged modes](stages-staged-modes.md) |
| How LTS and Arena use native round state | [Native-round modes](stages-native-round-modes.md) |
| Which World Settings, hooks, and actors the sampled maps author | [Map authoring surfaces](stages-map-authoring.md) |
| Why there is no universal match timer query | [Timers and readiness](stages-timers-and-readiness.md) |
| How a match can end and when a successor becomes current | [Endings and handoff](stages-endings-and-handoff.md) |
| What remains unproven and what the terms mean | [Evidence, limits, and terminology](stages-evidence-and-limitations.md) |

## Evidence labels

| Label | Meaning in this guide |
|---|---|
| **Configured** | Present in authored level data, defaults, a placed actor, or declared hook. It may be available without being dispatched in the sampled match. |
| **Recovered** | Established from a validated native implementation. It describes what that implementation does, not necessarily a live caller. |
| **Observed** | Measured in a live match. The surrounding text says whether it was an ordinary bot-driven run, an accelerated expiry, or a controlled trigger. |
| **Unknown** | Not established by the available evidence. |

## Scope

The guide describes selected FFA, TDM, LTS, Arena, and TO maps. It does not
claim that their authoring or terminal behavior applies to every map, nor does
it document experiment procedures, raw implementation details, or player-facing
strategies.
