# Stage and round overview

A **stage** is a mode-owned unit that can start, decide whether it is ready to
finish, and produce a possible next state. A **round** is the native
Arena-derived lifecycle used in the sampled LTS and Arena matches. The names
describe different ownership models in the evidence available here; they are
not interchangeable labels for every map.

## The sampled ownership split

| Sampled mode family | What owned the active lifecycle | What was observed |
|---|---|---|
| FFA | A placed timeout stage under a staged game mode | The placed stage was active during the sampled match. |
| TDM | A ticket stage created by the mode | A dynamic ticket stage was active; no placed ticket-stage actor was needed in the sampled map. |
| TO | Placed scored stages under a staged game mode | The first placed scored stage became current after a transition stage. |
| LTS and Arena | Native Arena-derived round/life state | Native round fields were active; no stage-interface actor was found in the bounded samples. |

This is an **Observed** comparison of one representative map per mode. It does
not prove that another map cannot use a different setup.

## What a staged mode can expose

**Declared:** [[ref:IStageInterface|the stage interface]] includes operations
for starting a stage, checking readiness, reporting time and identity, and
completing a stage. **Configured:** levels can provide
[[ref:GetFirstStage|a first-stage hook]], while
[[ref:ATBLWorldSettings|World Settings]] can select a default game mode and a
[[ref:UTBLGameModeSettings|mode settings object]].

Those surfaces describe what the game is equipped to use. They do not show that
a particular hook or branch ran in the sampled match. For example, a level can
contain a stage-start hook without evidence that the native-round LTS or Arena
sample dispatched it.

## Current, previous, and next

In the sampled staged modes, the game mode can expose a **current stage** and,
after a handoff, a **previous stage**. A stage can report completion and supply
a candidate next state. What the mode does with that result is mode-specific:
some sampled TDM and TO readiness paths installed a successor as current, while
the captured FFA score-limit path entered post-match with its timeout stage
still current.

> [!warning]
> Do not turn “a stage returned an object” into “the object became current.”
> The direct FFA completion experiment returned a victory object without
> changing the current stage. See [Endings and handoff](stages-endings-and-handoff.md).

## Transition and warmup context

**Configured / decoded:** the staged-mode setup includes a transition-stage
path that can wrap or precede a first stage, using level and world-settings
configuration. **Observed:** the sampled TO match had a transition stage as its
previous stage when its first scored stage was current.

The observation does not independently establish which construction path made
that transition instance. It is therefore safer to say that a transition stage
was present in the sample than to claim every TO map uses the same warmup path.

## Native round context

**Observed:** sampled LTS and Arena matches exposed round number, rounds,
and life-related state on [[ref:AArenaGameMode|native Arena-derived modes]] and
their game state. This guide calls that a native-round lifecycle to separate
it from the active stage actors observed in FFA, TDM, and TO.

No stage-interface actor was observed in the bounded LTS/Arena reads. That is a
limited observation, not proof that such an actor never exists in those modes.
See [Native-round modes](stages-native-round-modes.md) for the relevant
boundaries.

For the fields and hooks a modder can inspect in the sampled maps, see
[Map authoring surfaces](stages-map-authoring.md).
