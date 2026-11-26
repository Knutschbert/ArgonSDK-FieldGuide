# Spawner types

Spawners are actors that can start spawn waves at placed locations. The native
[[ref:ASpawner|ASpawner]] contract and the authored `BaseSpawner_C` Blueprint
branch expose related surfaces; do not mistake their names for a fully
verified compiled-class ancestry. The list below is an authored inventory,
not a record of which spawner a live match selected.

## Base Spawner hierarchy

The indexed Blueprint hierarchy below is complete for the available catalog.
The catalog lists `Spawner` as `BaseSpawner_C`'s parent; it does not establish
the exact compiled-class mapping to the native header tree. Its named
descendants are authored Blueprint classes, not proof of live selection.

```text
BaseSpawner_C (catalog parent: Spawner)
├── CagedSpawner_C
├── FenceSpawner_C
├── MovingBaseSpawner_C
├── TutorialSpawner_C
├── BP_FreeableVIPSpawner_C
└── RunInSpawner_C
    ├── RunInSpawner_Long_TG_C
    ├── RunInSpawner_Medium_C
    └── RunInSpawner_Short_C
```

`BaseSpawner_C` has six direct indexed children; only `RunInSpawner_C` has further indexed
descendants. The available generated reference site has a target for native `ASpawner`, but not for
these Blueprint classes, so their names remain class identifiers rather than broken reference links.

For the typed map inventory and configuration highlights of each variant, see
[Spawner variants](Spawner%20Variants.md).

## What the hierarchy means

- **BaseSpawner_C** is the common authored presentation layer: spawn camera, fade and HUD
  presentation, spawn-area cleanup, and stage actions. **Configured.**
- **RunInSpawner_C** adds spline/autorun settings, movement calls, wave parameter overrides, and a
  check of the wave's control restriction. **Configured.**
- The remaining descendants are authored special-purpose variants. Their runtime selection is
  **Unknown** unless a specific match sample establishes it.

For the mechanics behind these variants, see [Components](components.md) and
[How spawning works](how-spawning-works.md).

??? "Other named spawner surfaces"

    These named surfaces are useful when browsing authored content, but do not extend the verified
    `BaseSpawner_C` tree above.

    | Surface | What is established |
    |---|---|
    | [[ref:AGroupSpawner|Group Spawner]] | **Declared:** native `ASpawner` child with child-spawner records and a selection-mode field; actual child selection is **Unknown**. |
    | [[ref:ASeatSpawner|Seat Spawner]] | **Declared:** native `ASpawner` child with seat-entry and selection fields. Its relationship to `BaseSpawner_C` is not established here. |
    | [[ref:ASimpleSpawner|Simple Spawner]] | **Declared:** native `ASpawner` child with a maximum-player-count override; no typed placement was found in the indexed maps. |
    | Tent, Horse, Peasant, and Cinematic spawners | Named authored variants in the guide's previous inventory. Their parent classes and runtime selection are **Unknown** here. |

??? "Related tutorial and native reference"

    > [!NOTE] Tutorial
    > [[T2 Create a Free-For-All Map (FFA)]]

    [[ref:ASpawner]] — see its public functions in the generated reference.
