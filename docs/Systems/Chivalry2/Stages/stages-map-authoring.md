# Stage and round authoring surfaces

**Modder's question:** when inspecting a map, which values belong in World
Settings, which actors or level hooks supply a stage, and which state belongs
to the game mode? These are **configured examples from sampled shipped maps**,
not a tested checklist for making a new map. In particular, the presence of a
hook does not show that an ordinary match calls it.

## Start with the map's World Settings

[[ref:ATBLWorldSettings|TBL World Settings]] exposes `DefaultGameMode` and an
instanced `GameModeSettings` object derived from
[[ref:UTBLGameModeSettings|TBLGameModeSettings]]. Choose a settings object that
matches the chosen mode; do not infer the mode from a map-name prefix alone.
World Settings also exposes stage-ending configuration and warmup/sequence
surfaces, but their exact use depends on the mode and map.

| Sampled map | Configured game mode | Settings or round values to inspect | First-stage responsibility |
|---|---|---|---|
| FFA Tournament Grounds | `Mode_FFA_C` | `Settings_FFA_C`: score limit and match duration; defaults include score 35 and 900 seconds, with player-count scaling available. | Level `GetFirstStage` returns the placed `FFATimeoutStage_C`. |
| TDM Tournament Grounds | `Mode_TDM_C` | `Settings_TDM_C`: tickets and match duration; the sample started with 75 per faction and 600 seconds. | The mode creates `TDMStage_C` from its settings; the level exposes `Start TDM Stage`, not a placed ticket stage. |
| TO Bridgetown | `StagedGameMode_C` | `UseNewStageIdNumbers`, stage-ending configuration, and scored-stage initialization values; no `GameModeSettings` reference was present in this export. | Level `GetFirstStage` initializes and returns the first of five placed scored stages. |
| LTS Tournament Grounds | Native [[ref:ALTSGameMode|LTSGameMode]] | [[ref:ULTSGameModeSettings|LTSGameModeSettings]] on World Settings; round count, lives, and delays are fields on the Arena-derived mode. | Native round state was observed; a level stage-start hook exists but its ordinary dispatch is unknown. |
| Arena Courtyard | Native [[ref:AArenaGameMode|ArenaGameMode]] | [[ref:UArenaGameModeSettings|ArenaGameModeSettings]] on World Settings; round count, lives, and timing belong to the native mode. | Round events and a stage-start hook are authored; no stage-interface actor was observed in the bounded match. |

**Configured** values are not guaranteed gameplay results. For example, FFA
and TDM settings can scale values by player count; a default in an asset is
not necessarily the active value in a different match.

## How the sampled staged maps provide a first stage

[[ref:GetFirstStage|GetFirstStage]] is the level Blueprint interface entry
used by the sampled FFA and TO staged maps. For FFA, the level returns a placed
timeout-stage actor of the expected class. A decoded FFA branch can create a
fallback timeout stage if the level result is absent or unsuitable; **no
sampled map was observed using the fallback**. Do not treat that fallback as
permission to omit the level setup from an untested new map.

For TDM, the sampled level did not place a `TDMStage_C`. The mode created and
initialized one from `Settings_TDM_C` and exposed a `Start TDM Stage` level
hook. Its presence in the map is **Configured**; this guide does not assert
when that hook ran in an ordinary match.

For TO Bridgetown, `GetFirstStage` initializes five placed `ScoredStage_C`
actors, wires score-successor and timeout destinations, and returns stage 1.
The following table describes its **authored initialization**, not ordinary
objective progress or a recommendation for other maps:

| Placed stage | Stage ID | Initial/max score | Duration | On score / on timeout |
|---|---:|---:|---:|---|
| 1 | 10 | 0 / 1000 | 330 s | Stage 2 / defender victory |
| 2 | 20 | 0 / 1000 | 300 s | Stage 3 / defender victory |
| 3 | 30 | 0 / 3500 | 240 s | Stage 4 / defender victory |
| 4 | 40 | 0 / 1200 | 300 s | Stage 5 / defender victory |
| 5 | 50 | 0 / 1300 | 300 s | Attacker victory / defender victory |

These score and duration values come from the level's initialization graph,
**not** simply the placed actors' serialized defaults. A controlled test
advanced the score branch through all five stages, while an accelerated
stage-1 timeout installed defender victory. Ordinary objective-to-score
sources, later timeout outcomes, and behavior on another TO map are unknown.

??? "Transition stage and stage-ending configuration"

    A staged-mode path can wrap the level's first stage in a transition stage
    using World Settings warmup and spawner-binding surfaces. The sampled TO
    match had a transition stage as its previous stage, but that observation
    does not identify which construction path produced the instance.

    Bridgetown configures `UseNewStageIdNumbers` and a last-stage ID of 50.
    The [[ref:FStageEndingConfig|stage-ending configuration]] and the placed
    stages' IDs are separate surfaces. Do not copy these numbers into another
    map without checking its authored chain and mode configuration.

## Native rounds are not staged-map recipes

[[ref:AArenaGameMode|ArenaGameMode]] declares `Rounds`, `TeamLives`,
`FinalLives`, `TimeBetweenRounds`, `RoundTimeLimit`, and
`PreCountdownDelay`; [[ref:ALTSGameMode|LTSGameMode]] derives from it.
`LTSGameModeSettings` also exposes optional round-count override fields.
The sampled Arena map has three initial spawners per faction and a configured
round time limit of zero; its bot-driven round was untimed. Neither a generic
maximum-player value nor adding a bot to start a probe establishes the
authoring requirements of a 1v1 map.

No `LTSScoredStage_C` was found in the sampled LTS match, and the authored
level `Start TDM Stage` or round-event bindings do not prove ordinary
dispatch. Inspect the actual mode, settings, and level event wiring before
adapting a native-round map.

> [!warning] Not a verified new-map recipe
> These examples identify shipped-map configuration and a few bounded live
> results. They do not establish every required field, hook consumer, spawn
> arrangement, replication rule, or success condition for a new map. Validate
> your own map and match state rather than assuming a copied setup will run.

For runtime ownership see [Stage and round overview](stages-overview.md);
for timing and completion see
[Timers and readiness](stages-timers-and-readiness.md) and
[Endings and handoff](stages-endings-and-handoff.md).
