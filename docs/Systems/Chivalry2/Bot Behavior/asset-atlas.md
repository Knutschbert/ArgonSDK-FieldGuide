# Asset and function atlas

This atlas connects the guide’s plain-language concepts to the concrete classes and assets used by
the normal melee bot. Names are useful for browsing assets, inspecting a live bot, and recognizing
what a behavior configuration refers to.

!!! warning "A name is not a runtime trace"
    Listing an asset or function proves that it is configured or documented in the bot’s available
    surface. It does not prove that a specific live fight selected that asset, dispatched an event
    set, or invoked a function.

## Naming scheme

| Prefix | Meaning |
|---|---|
| `BS_` | **Behavior Set** — a collection of behavior candidates. |
| `B_` | General-purpose behavior. |
| `BC_` | Combat behavior. |
| `A_` | General-purpose action. |
| `AC_` | Combat action. |
| `I_` | Consideration input — a world-state sensor. |
| `TG_` | Target generator — a source of candidate actors or locations. |
| `_C` | The generated runtime class for a Blueprint asset. |

The authored UtilityAI assets live under `/Game/AI/Utility/` in game notation. In the local
semantic catalog, the same root is written as `AI/Utility/`.

## Controller and decision-making surfaces

| Name | Role | Status and limitation |
|---|---|---|
| `Chiv2AIController_Utility_C` | The standard melee AI controller class used by documented normal bot spawns. | **Observed/Configured.** Carries both general and combat decision-making surfaces plus the native combat controller. |
| `GeneralDecisionMakerComponent` | Holds broad world and engagement candidates. | **Observed.** Its cache can be intentionally cleared by some helper-spawn workflows. |
| `CombatDecisionMakerComponent` | Holds close-combat candidates and event-associated behavior sets. | **Observed.** It can cache normal combat behaviors even when active decision dispatch is not established. |
| [[ref:ATBLAICombatController|TBLAICombatController]] | The native controller layer for target, combat state, movement, spacing, and attack control. | **Recovered/Observed.** It can drive visible combat independently of proof of a UtilityAI winner. |

## Core normal-melee behavior sets

| Asset/class | Role | Contents or purpose |
|---|---|---|
| `BS_Combat_Melee_Normal_C` | The documented normal melee combat inventory. | `BC_Slash_C`, `BC_OverheadStab_C`, `BC_FeintAttack_C`, `BC_Block_C`, `BC_Wait_C`, `BC_Shove_C`. |
| `BS_Combat_Melee_Dumb_C` | A simplified combat-set variant. | Similar normal combat inventory without `BC_FeintAttack_C`. |
| `BS_MeleeFighter_C` | General combat-engagement behavior set. | Includes entering combat, responding to damage, and escaping close danger. |
| `BS_General_C` | General-purpose behavior set. | Includes revive, combat-zone safety, and objective movement candidates. |

**Observed:** the `_Normal` set and six cached behaviors were present on sampled direct and
owner-created bots. **Configured:** the authored `Normal` personality row names `_Dumb`.
**Unknown:** the selector/application path reconciling those surfaces and the complete
ordinary-match sequence that chooses a set and behavior.

## Normal combat behaviors

| Behavior | Main action | Configured purpose |
|---|---|---|
| `BC_Slash_C` | `AC_Attack_C` | Request `Slash`; considers time since the last attack. |
| `BC_OverheadStab_C` | `AC_Attack_C` | Request `Overhead` or `Stab`; considers attack cooldown and nearby teammates. |
| `BC_FeintAttack_C` | `AC_FeintAttack_C` | Make an attack and possibly feint; uses randomness and a behavior cooldown. |
| `BC_Block_C` | `AC_Block_C` | Hold parry briefly; considers distance and its recent-use cooldown. |
| `BC_Wait_C` | `AC_EngagedWait_C` | Provide a low-score fallback that waits while maintaining a spacing intent. |
| `BC_Shove_C` | `AC_Attack_C` | Request `Shove`; considers recent enemy blocks and cooldown. |

The combat behavior assets are under the combat-behavior area of
`/Game/AI/Utility/Behaviors/`. They are concrete authored candidates, not a hard-coded attack
rotation.

## General engagement behaviors

| Behavior | Action | Target source | Role |
|---|---|---|---|
| `B_EngageInCombat_C` | `A_EnterCombatWith_C` | `TG_PerceivedCharacters_C` | Consider a perceived enemy for normal combat engagement. |
| `B_EngageInResponseToDamage_C` | `A_EnterCombatWith_C` | `TG_PerceivedCharacters_C` | Consider engagement after receiving damage. |
| `B_CloseRangeEscapeHeat_C` | `A_MoveTo_C` | `TG_PointsAroundMe_C` | Move away from a close melee-threat area. |
| `B_GoToCombatZoneSafeSpot_C` | Movement action | Objective/location generator | General world movement option. |
| `B_RevivePlayer_C` | Revive action | Player-oriented target source | General team-support option. |
| `B_WalkAroundObjectives_C` | `A_MoveTo_C` | Destination-volume generator | General objective movement option. |

## Combat actions

| Action | Function in human terms | Important configured detail |
|---|---|---|
| `AC_Attack_C` | Ask the controller to pursue an allowed attack. | Requests attack-oriented spacing before its attack request. |
| `AC_FeintAttack_C` | Attack, then possibly request a feint during the appropriate phase. | Has authored attack and feint lists. |
| `AC_Block_C` | Request a temporary parry hold. | Normal Block overrides the action’s hold time with a shorter value. |
| `AC_EngagedWait_C` | Maintain its configured spacing intent while waiting. | Used by `BC_Wait_C`. |
| `AC_Dodge_C` | Request a dodge response. | Used by certain event-associated defensive behaviors. |
| `AC_Riposte_C` | Request a riposte-style follow-up. | Used by parry-success behavior options. |
| `A_EnterCombatWith_C` | Give an enemy target to the combat controller and request engagement. | The documented bridge from general engagement behavior to combat-controller target/state. |
| `A_MoveTo_C` | Move toward a chosen target or location using path following. | This is waypoint/path movement, not native combat strafe. |

## Common consideration inputs

| Input | Reads | Used by |
|---|---|---|
| `I_TimeSinceLastAttack` | Time since the controller’s last attack. | Slash and Overhead/Stab cooldown shaping. |
| `I_TimeSinceLastDidBehavior` | Time since a configured behavior last ran. | Block, Feint, and Shove cooldown shaping. |
| `I_Distance` | Distance to the current target. | Close-range Block preference and event-defense conditions. |
| `I_InfluenceCurrent` | An influence value at the current point. | Overhead/Stab’s nearby-teammate consideration. |
| `I_Random` | A random consideration value. | Feint frequency shaping. |
| `I_TimesEnemyRecentlyBlockedMe` | Count of recent enemy blocks against the bot. | Shove pressure shaping. |
| `I_Constant` | A fixed configured value. | Wait fallback and Shove base influence. |

These inputs feed curves and then behavior scoring. See [decision-making and scoring](decision-making.md)
and [behavior and movement formulas](formulas.md).

## Target generators

| Generator | Role | Where it matters |
|---|---|---|
| `TG_PerceivedCharacters_C` | Produces perceived character candidates. | General engagement behavior. |
| `TG_PointsAroundMe_C` | Produces nearby candidate points. | Escape/positioning behavior. |
| `TG_DestinationVolume_WithAITag_C` | Produces tagged destination locations. | Objective movement. |
| `None` on normal `BC_*` combat behaviors | Uses the existing controller combat target instead of generating candidates. | Core normal melee combat behaviors. |

## Event behavior sets and their candidates

| Set | Notable contained candidates | Reader interpretation |
|---|---|---|
| `BS_Event_AttackIncoming_Advanced_C` | `BC_BlockIncomingAttack_C`, `BC_DodgeBack_C`, `BC_Wait_C` | Authored incoming-attack response options. |
| `BS_Event_AttackIncoming_C` | Adds `BC_Jab_C` to the base response inventory. | A broader authored incoming-attack variant. |
| `BS_Event_AttackIncoming_Dumb_C` | Simplified incoming-attack variant. | Omits Jab. |
| `BS_Event_ParrySuccess_C` | `BC_Riposte_C`, `BC_CounterWithShove_C`, `BC_RiposteWithFeint_C` | Authored post-parry pressure options. |
| `BS_DamageCaused_C` | Slash, Overhead/Stab, Wait. | Authored continuation options after causing damage. |
| `BS_Event_ShoveIncoming_C` | Attack-through-shove, block, dodge-back options. | Authored shove response inventory. |
| `BS_ParryBreakSuccess_C` | `BC_Wait_C`, `BC_PunishGuardBreak_C` | Authored guard-break/CC opportunity options. |

## Combat-controller functions

These names identify supported controller-facing operations. They explain the control surface; they
are not a generic instruction to force a normal bot’s decision loop.

| Function | Plain-language effect | Important limit |
|---|---|---|
| `Engage` | Set a combat target and begin entering combat. | Requires valid parameters and a valid target; it is not evidence of a General decision winner. |
| `Disengage` | Request leaving combat. | Clears combat engagement rather than merely stopping one movement request. |
| `Attack` | Store and pursue an allowed attack order. | Direct external invocation has a narrower validation history than native behavior-driven use. |
| `StrafeAndKeepDistance` | Store spacing and strafe intent. | It is not a deterministic strafe command; active behavior paths can overwrite its values. |
| `HoldBlock` | Hold defensive input. | Competes with other controller action requests and combat state. |
| `ReleaseBlock` | Remove the controller’s held-block request. | Does not describe every possible block source. |
| `Dodge` | Request movement-direction dodge behavior. | Depends on combat context and available dodge behavior. |

## Where to use the names

- Browse `/Game/AI/Utility/` to inspect the authored behavior, action, input, or target-generator
  configuration.
- Read the guide pages first to understand what role a name plays.
- Use the names to recognize a live inventory or asset reference.
- Treat a live cache as evidence of configured availability, not proof of a selected winner.

For the evidence boundaries that apply to all entries, read
[Evidence and limitations](evidence-and-limitations.md).
