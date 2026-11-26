# Spawning components

This page describes what each layer owns. Names are kept where they help readers identify an asset;
this is not a complete symbol atlas.

## Native and authored layers

| Component | Kind | What it owns | Evidence boundary |
|---|---|---|---|
| **Spawn sequence** | Native actor | Spawner list, current position, active-wave set, faction, wave timing, loop and concurrency settings. Authority-only forced spawning. | **Recovered:** selection and concurrency checks. **Unknown:** activation path and all tie-breakers. |
| **Spawner** | Native actor | Location components, reservations, scoring, current wave, spawn events, and possession timing. Normal, forward, and forced wave starts. | **Recovered:** wave creation/configuration. **Unknown:** reservation and location-selection flow. |
| **Group spawner** | Native actor | Child-spawner records and a selection-mode field. | **Declared:** native header fields; typed placements are **Configured** in indexed maps. **Unknown:** child selection and refill behavior. |
| **Spawn wave** | Native actor | Joinable controllers, spawn timing and state, capacity, special-spawn setup, control restriction, controller membership/history, and a replicated joined-player-state list. | **Recovered:** join and end bookkeeping. **Unknown:** the full state machine and replication timing. |
| **Spawn queuer** | Native policy object | Activation state and request/remove hooks for admission. | **Recovered:** the policy surface. **Unknown:** which mode selects which policy for players. |
| **Wave spawn queuer** | Queue policy | Respawn and wave timing with timed controller entries. | **Recovered:** admission records timing metadata. **Unknown:** the consumer of due entries. |
| **Cumulative spawn queuer** | Queue policy | Per-controller accumulated respawn delay and history. | **Recovered:** the delay is computed and persisted on admission. **Unknown:** dispatch and removal. |
| **Group spawn queuer** | Queue policy | Shared group-wave window, active participants, and a separate solo queue. | **Recovered:** late entrants go to the solo queue; the recovered removal method searches only group participants. **Unknown:** solo promotion and alternate cancellation. |
| **New spawn system queuer** | Native policy object and observed instance | Filters candidate waves and can choose the lowest `GetTimeLeft` result before invoking native virtual `JoinSpawn`; also seen under the mode in TDM Courtyard / InProgress, TDM Wardenglade / InProgress, and LTS Courtyard / WaitingToStart samples. | **Recovered:** its candidate-selection and join path. **Observed:** presence during respawn samples with an empty bot-waiting array. **Inferred:** the mode owns it as a policy. **Unknown:** whether its path admitted the sampled player and how the mode creates/selects it. |
| **Base spawner** | Authored Blueprint | Spawn camera, fade/HUD presentation, spawn-area cleanup, and authored stage actions. | **Configured.** **Unknown:** which paths are reachable in an ordinary match. |
| **Run-in spawner** | Authored Blueprint, derived from base spawner | Spline and autorun settings, wave parameter overrides, movement calls, and a control-restriction check. | **Configured:** typed placements are indexed by map and variant. **Unknown:** which placed path runs in an ordinary spawn and when control is released. |

??? "Names readers will encounter"

    | Name | Layer and ownership | Evidence boundary | Read next |
    |---|---|---|---|
    | **[[ref:ASpawnSequence|SpawnSequence]]** | Native actor that orders available spawners and limits active waves. | **Recovered:** selection and concurrency checks; activation remains **Unknown**. | [How spawning works](how-spawning-works.md) |
    | **`ASpawner`** | Native actor that creates and configures a wave at a placed location. | **Recovered:** wave factory/configuration role; location selection remains **Unknown**. | [Spawner types](Spawner.md) |
    | **[[ref:ASpawnWave|ASpawnWave]]** | Native actor holding controller membership, timing, state, and the replicated joined-player-state list. | **Recovered:** join and end bookkeeping; full lifecycle remains **Unknown**. | [How spawning works](how-spawning-works.md) |
    | **[[ref:UNewSpawnSystemQueuer|NewSpawnSystemQueuer]]** | Native admission policy that can select a candidate wave and request its join. | **Recovered:** its candidate-selection path; **Observed:** instances in bounded mode samples; sampled player use remains **Unknown**. | [Queues and timing](queues-and-timing.md) |
    | **`BaseSpawner_C`** | Authored Blueprint layer for spawn camera, HUD, cleanup, and stage actions. | **Configured:** it provides presentation behavior; ordinary-match reachability is **Unknown**. | [Spawner types](Spawner.md) |
    | **`RunInSpawner_C`** | Authored `BaseSpawner_C` variant for run-in movement and presentation. | **Configured:** movement/control-restriction surface; ordinary-match use is **Unknown**. | [Spawner types](Spawner.md) |

    These names identify layers that are useful for browsing assets or live objects. They do not
    identify the actor or path chosen by a particular spawn.

??? "How to read evidence labels"

    - **Recovered** describes implementation behavior established from the game code and written in
      player-facing terms. It does not claim that a call ran in a particular match.
    - **Configured** describes something authored into a level, class, or default. It is an inventory
      of what is available, not a record of what was selected.
    - **Observed** describes a bounded live sample. Keep the map and match state in mind when reading it.
    - **Unknown** marks a genuine gap. It is not a hint about the most likely answer.

## Ownership versus presentation

Recovered native actors expose selection, wave creation, membership bookkeeping, and release
operations; the function that wrote membership in the observed respawn is still **Unknown**.
The authored spawner Blueprints sit around that core
and provide what the player sees during a spawn — camera work, HUD state, movement along an authored
path, and checks of the wave's control restriction.

> [!info] Why the split matters
> Seeing camera or run-in behavior does not prove which native spawner was selected, and seeing a
> wave with membership does not prove which authored presentation path ran. Keep the two layers
> separate when interpreting a match.

## Related pages

- [How spawning works](how-spawning-works.md)
- [Queues and timing](queues-and-timing.md)
- [Spawner types](Spawner.md)
