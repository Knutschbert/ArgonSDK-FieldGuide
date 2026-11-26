# Spawner types

Spawners are the actors that start spawn waves at placed locations. The native base type is
[[ref:ASpawner]]; authored variants add presentation, movement, and special-case behavior. The list
below is an authored inventory, not a record of which spawner a live match selected.

## Base Spawner hierarchy

The indexed authored hierarchy below is complete for the available catalog. `BaseSpawner_C` derives
from [[ref:ASpawner]]; its named descendants are Blueprint classes, not proof of live selection.

```text
ASpawner
└── BaseSpawner_C
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
    | [[ref:AGroupSpawner|Group Spawner]] | Native type that aggregates child spawners with a selection mode. **Recovered** surface; child selection is **Unknown**. |
    | [[ref:ASeatSpawner|Seat Spawner]] | A native reference surface for a seat-oriented spawner. Its relationship to `BaseSpawner_C` is not established here. |
    | Tent, Horse, Peasant, and Cinematic spawners | Named authored variants in the guide's previous inventory. Their parent classes and runtime selection are **Unknown** here. |

??? "Related tutorial and native reference"

    > [!NOTE] Tutorial
    > [[T2 Create a Free-For-All Map (FFA)]]

    [[ref:ASpawner]] — see its public functions in the generated reference.
