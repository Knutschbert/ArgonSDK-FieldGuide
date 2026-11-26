# Timers and readiness

The active stage or round owns the useful completion information. There is no
single timer query that safely describes every sampled mode.

## Why a zero time query can mislead

**Observed:** in sampled FFA and TDM matches, a stage-level query and a native
game-state time query could read zero while the active
`TimeObjectiveComponent` still counted down. A zero result therefore does not
mean the active match timer is exhausted, paused, or ready to complete.

The reader-facing rule is simple: use the timer and terminal state that belong
to the active implementation, not a generic query alone.

## Readiness differs by stage type

| Active implementation | Configured / decoded readiness surface | Observed boundary |
|---|---|---|
| FFA timeout stage | Duration expiry | The mode's score-limit check is separate from this stage's readiness. |
| TDM ticket stage | Attacker terminal flag, defender terminal flag, or draw flag | On timeout, the component's expiry event sets a terminal condition before readiness; a controlled ticket-zero or draw trigger can set one while the timer still has time left. |
| TO scored stage | Duration expiry **or** configured maximum score | The score-successor chain was reached after controlled score changes; ordinary objective sources remain unknown. |
| Native Arena/LTS round | Native round/life fields | A single generic stage timer was not established as the owner. |

“Configured / decoded” identifies available logic, not an ordinary live
caller. The table deliberately avoids treating the same condition as proven
runtime behavior in every map.

## What was measured

**Observed, accelerated expiry:** the active FFA and TDM timer components
reached zero and the matches completed. The captures establish that component
expiry can drive those sampled terminal paths; they do not measure ordinary
real-time pacing.

**Observed, controlled terminal state:** TDM ticket exhaustion and draw probes
made the stage ready through terminal flags while the component still had time
left. Those actions establish how the readiness path responds, not the natural
event that invokes it.

**Observed, controlled score:** the sampled TO stage chain advanced when each
current stage reached its configured score threshold. This establishes the
successor behavior of that readiness route, not which ordinary objective event
awards score.

## Practical interpretation

When reading a match state:

1. Identify the active stage or native round owner.
2. Read that implementation's component timer, score, lives, tickets, or
   terminal flags together.
3. Treat a generic zero time result as incomplete information.
4. Keep the cause of a terminal state separate from the fact that it became
   ready.

For the mode-specific ownership and limits, see
[Staged modes](stages-staged-modes.md) and
[Native-round modes](stages-native-round-modes.md). For terminal outcomes after
readiness, see [Endings and handoff](stages-endings-and-handoff.md).
