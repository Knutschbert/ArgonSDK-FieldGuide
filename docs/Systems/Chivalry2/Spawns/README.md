# Chivalry 2 spawning guide

This guide explains how the game brings players and bots into a match: which actors place and order
spawns, how a spawn wave collects players, how queue policies affect timing, and which parts are
authored map setup rather than live behavior. It describes the ordinary player-spawn system, not
generic actor placement or what a character does after spawning.

## Start here

[Read the visual overview first.](Spawn%20System%20Overview.md)

**Inferred — working mental model:** spawning is best understood as five connected layers:

1. **Spawn sequences** order waves across a set of spawners and control how many can be active.
2. **Spawners** create and configure a wave at a placed location.
3. **Spawn waves** hold joining controllers, expose state, and release their spawner when they end.
4. **Queue policies** decide who is admitted and how respawn timing is accumulated.
5. **Authored spawner Blueprints** add camera, HUD, run-in movement, and control-restriction
   presentation on top of the native actors.

This five-layer picture is **Inferred**: the individual handoffs are recovered below, but complete
mode ownership and dispatch are not fully traced. The layers are related but not interchangeable.
A sequence object can exist without being active,
a spawner can be placed without being selected, and a wave can hold membership that a particular
callable did not write.

> [!warning] The guide's most important reading rule
> **Configured** spawning is not the same as **dispatched** spawning. A placed sequence, a queuer
> instance observed under a mode object, or a callable method in the implementation tells us what the
> game is equipped to do. It
> does not, by itself, identify the path that produced a particular live spawn.

## Reading paths

| If you want to understand… | Read… |
|---|---|
| The smallest correct mental model, with a diagram | [Spawn System Overview](Spawn%20System%20Overview.md) |
| How the layers connect and where each handoff is established | [How spawning works](how-spawning-works.md) |
| What each sequence, spawner, wave, and queuer owns | [Components](components.md) |
| How wave, cumulative, and group queues differ | [Queues and timing](queues-and-timing.md) |
| What FFA, TDM, LTS, and TO configure and what was observed | [Game modes](game-modes.md) |
| Which spawner variants are named in authored assets | [Spawner types](Spawner.md) |
| Where each spawner variant is placed and what it configures | [Spawner variants](Spawner%20Variants.md) |
| Which conclusions are firm and which remain open | [Evidence and limitations](spawning-evidence-and-limitations.md) |

## Evidence labels

The guide labels material by what supports it:

| Label | Meaning |
|---|---|
| **Observed** | Directly seen in a documented live match or controlled test. |
| **Configured** | Present in an authored level, class, or default configuration. |
| **Recovered** | Established from the game implementation, described here in player-facing terms. |
| **Inferred** | A working explanation supported by evidence but not fully traced. |
| **Unknown** | Not established by the available evidence. |

Labels belong to individual claims. For example, a **Configured** faction sequence says a map
author set one up; it does not prove that an ordinary respawn used it. A **Recovered** call body says
the implementation can do something; it does not prove that call ran in a given match.

??? "Glossary"

    | Term | Meaning |
    |---|---|
    | **Spawn sequence** | An actor that orders waves across spawners and limits how many run at once. |
    | **Spawner** | An actor that creates and configures a spawn wave at a placed location. |
    | **Forward spawn** | An authored forward-spawning call shape appears in Team Objective stage scripts. The concrete receiver and its general runtime meaning are **Unknown** in the catalog build. |
    | **Spawn wave** | A temporary actor that collects joining controllers and tracks spawn timing and state. |
    | **Wave state** | The wave's progression label, such as not started, spawning, or ending. |
    | **Queuer** | A policy layer that admits controllers and schedules when they can spawn. It appears under a mode in samples; mode ownership is **Inferred**, not observed creation. |
    | **Group spawner** | A spawner that aggregates child spawners and a selection mode. |
    | **Run-in spawner** | An authored spawner variant with movement and presentation behavior for entering play. |
    | **Control restriction** | A wave flag governing whether player control is limited during the spawn. |
    | **Admission** | Adding a controller to a wave or queue; distinct from creating the pawn. |

??? "Scope and reading limits"

    This guide keeps named surfaces where they help readers, but it avoids raw implementation dumps,
    speculative call chains, and instructions for authoring a new spawn system. Where the mechanism
    that produced a live spawn is not established, the guide says so instead of filling the gap with
    the most plausible story.
