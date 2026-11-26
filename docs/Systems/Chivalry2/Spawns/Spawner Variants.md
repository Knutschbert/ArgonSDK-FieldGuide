# Spawner variants and map usage

This page answers a narrower question than [Spawner types](Spawner.md): which authored spawner
classes are actually placed in maps, and what configuration do they expose? The counts below are
**Configured** typed actor exports in the indexed map data; “maps” counts map assets containing
that type. They are not spawn counts, unique physical locations, or records of which spawner a
live match selected.

> [!warning] Placement is not selection
> A typed map export proves that a class was authored into a level. It does not prove that a
> sequence chose it, that a wave started there, or that it produced an observed player spawn.

## Variant inventory

| Variant | Authored placements | Maps | Where readers will encounter it |
|---|---:|---:|---|
| `RunInSpawner_C` | 1,863 | 49 | Team Objective and FFA maps; the most widely placed authored variant. |
| `BaseSpawner_C` | 544 | 31 | Directly placed alongside its descendants, including Brawl and FFA maps. |
| `FenceSpawner_C` | 271 | 11 | Tournament Arena, Hippodrome, Fighting Pit, Lionspire, and Courtyard. |
| `GroupSpawner` | 258 | 52 | Native group aggregator placed across many objectives and modes. |
| `CagedSpawner_C` | 44 | 4 | All four Falmire variants: FFA, LTS, TDM, and Team Objective. |
| `RunInSpawner_Long_TG_C` | 26 | 4 | Coxwell and the Tournament Arena/LTS/TDM variants. |
| `RunInSpawner_Short_C` | 9 | 3 | Tournament Arena, LTS, and TDM. |
| `MovingBaseSpawner_C` | 8 | 2 | Library and Raid Team Objective. |
| `RunInSpawner_Medium_C` | 6 | 3 | Tournament Arena, LTS, and TDM. |
| `SeatSpawner` | 2 | 2 | Brawl maps at Rudhelm Hall and Cathedral. |
| `BP_FreeableVIPSpawner_C` | 1 | 1 | Falmire Team Objective. |
| `TutorialSpawner_C` | 1 | 1 | Tutorial. |
| `SimpleSpawner` | 0 | 0 | No typed map placement in the indexed data. |

The native `GroupSpawner`, `SeatSpawner`, and `SimpleSpawner` entries are separate from the
authored `BaseSpawner_C` branch. They are included here because typed placement makes their authored
use visible, not because the two hierarchies have been merged.

## Worked map examples

### Falmire

Falmire is the clearest example of several variants appearing in one map family:

- **CagedSpawner_C** is placed in FFA, LTS, TDM, and Team Objective Falmire.
- **BP_FreeableVIPSpawner_C** is placed in Team Objective Falmire at the VIP spawn. Its authored
  wave parameters specify `WarHeroSpawn_C` and a private-wave flag; live use was not observed.
- **GroupSpawner** is also placed in Team Objective Falmire.

These are authored placements. They do not show which caged, group, or VIP spawner was selected for
a particular death or objective stage.

### Tournament Grounds

Across the indexed Tournament Grounds map variants, authored placements
include **FenceSpawner_C** and all three Run-In subtypes:

- `RunInSpawner_Long_TG_C`
- `RunInSpawner_Medium_C`
- `RunInSpawner_Short_C`

The subtypes differ mainly in camera offset and spawn-gate configuration, not in a demonstrated
runtime rule.

## Configuration highlights

??? "Base and authored presentation"

    - **BaseSpawner_C**: spawn name “Main Force”, fade time 0.4, start-camera offset, vulnerable time
      1.75, and a player-kill stage action.
    - **BaseSpawner_C** also carries camera fade, HUD marker, possession hooks, and cleanup of
      constructables and horses.
    - These are authored defaults; they are not evidence that a particular spawn used them.

??? "Caged and Fence spawners"

    - **CagedSpawner_C**: cage actor and state, caged-character list, exit point and key, eject
      velocity, and a two-second free delay. It permits invalid spawn locations and skips pawn
      overlap checks.
    - **FenceSpawner_C**: `FenceSpawn` animation, one player per wave, three-second pre-spawn,
      two-second vulnerability delay, and skipped location validation.

??? "Movement and special-case variants"

    - **MovingBaseSpawner_C**: attach-on-spawn enabled, replication enabled, and a relative-location
      map for waiting entries.
    - **BP_FreeableVIPSpawner_C**: Iron Maiden spawn animation, fade time 0.5, one player per wave,
      three-second pre-spawn, and a two-second vulnerability delay.
    - **TutorialSpawner_C**: no child-specific properties or functions were surfaced in the indexed
      data.

??? "Run-In family"

    - **RunInSpawner_C**: spline and autorun settings, a three-second stop delay, sprint movement,
      follow-first-spawned behavior, and wave sound overrides.
    - **RunInSpawner_Long_TG_C**: spawn-gate array, replicated start state, two-second pre-spawn, and
      a higher camera offset.
    - **RunInSpawner_Medium_C**: two-second pre-spawn and a middle camera offset.
    - **RunInSpawner_Short_C**: two-second pre-spawn, a shorter camera offset, and a slight downward
      rotation.

## What remains unknown

> [!info] Runtime selection is not established
> The indexed data tells us where classes are placed and how they are configured. It does not
> identify which class served an observed spawn, how a group spawner selected a child, or whether a
> Run-In path ran in an ordinary match.

For the ownership model around these actors, see [How spawning works](how-spawning-works.md). For the
component responsibilities, see [Components](components.md). For the evidence labels used across the
guide, see [Evidence and limitations](spawning-evidence-and-limitations.md).
