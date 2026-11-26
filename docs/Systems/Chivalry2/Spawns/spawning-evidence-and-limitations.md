# Evidence and limitations

Spawning has several layers, and different evidence establishes different things. This page keeps
the guide precise about what is known, what is configured, what was seen, and what remains open.

## Evidence labels

| Label | Meaning |
|---|---|
| **Observed** | Seen in a documented live match or controlled test. |
| **Configured** | Present in an authored level, class, or default configuration. |
| **Recovered** | Established implementation behavior, described here in player-facing terms. |
| **Inferred** | A supported working explanation that has not been fully traced. |
| **Unknown** | Not established by the available evidence. |

## Current model at a glance

| Topic | What is established | Important limit |
|---|---|---|
| Sequence selection | Eligibility, activity, concurrency, and unlocked-spawner checks are recovered. | All tie-breakers and per-mode activation are not mapped. |
| Spawner wave creation | Post-match and special-spawn rejection, wave creation, faction precedence, and overrides are recovered. | Location scoring and reservations are not described. |
| Wave membership | A recovered `JoinSpawn` body records joined and historical controllers plus a replicated joined-player-state list; a recovered end body releases the spawner. | The live writer in the TDM Wardenglade / InProgress respawn was not attributed. |
| Wave state | Not started, spawning, and ending are named states; an authority wave can reach ending. | The full transition table and replication timing are unknown. |
| Queue admission | Cumulative, group, and wave queues have distinct admission and timing rules. | Due-entry dispatch and solo-queue handling are unknown. |
| Queue-to-join path | `NewSpawnSystemQueuer` filters eligible waves, compares `GetTimeLeft`, and invokes `JoinSpawn` on the lowest-result candidate through a native virtual call (**Recovered**). | It was not recorded in the sampled respawn; the score's meaning and live attribution are **Unknown**. |
| Observed queuer | A queuer instance appeared under the mode in TDM Courtyard / InProgress, TDM Wardenglade / InProgress, and LTS Courtyard / WaitingToStart samples, with an empty bot-waiting array. Mode ownership is **Inferred**. | Its role in ordinary player admission is not established. |
| Bot admission | A controlled bot addition in TDM Courtyard / InProgress filled the queuer's bot-waiting array and produced pawns. | That is a bot surface, not the ordinary player-respawn path. |
| Player respawn | TDM Wardenglade / InProgress showed a pawnless player, a wave with one joined controller, then a new pawn. | The native function that wrote that membership and created the pawn was not attributed in that sample. |
| Authored spawner behavior | Base and run-in spawners configure presentation, movement, and control-restriction checks. | Which authored path runs in an ordinary spawn is not established. |
| Mode differences | FFA, TDM, LTS, and TO author different sequences, spawners, and timing values. | One sample per mode cannot establish a universal mode rule. |
| Team Objective forward spawns | Stage scripts reference forward spawning and run-in spawners. | The catalog build's stage-to-spawner receiver binding is unknown. |

??? "What not to infer"

    ### A configured spawner is not a selected spawner

    A level script can author a sequence reference, a faction sequence, a run-in spawner, or a forward
    spawn call. That is an inventory of what the map is equipped to do. It does not prove that a given
    death or objective advanced through that exact actor.

    ### A recovered callable is not a recorded call

    Recovered implementation bodies establish what the game is capable of doing and how an operation
    is structured. They do not prove that a particular callable ran in a particular match. A body that
    can add a controller to a wave is not, by itself, the writer of an observed membership change.

    ### A missing call at one entry point is not a whole-path explanation

    In the TDM Wardenglade / InProgress respawn sample, several spawn-related callables produced no
    events while a control callable did fire. That supports a bounded negative result for those entry
    points. It does not identify the function that actually performed the spawn, and it should not be
    generalized to every respawn.

    ### An empty wave is not a never-used wave

    Wave objects appear and rotate across placed spawners. A snapshot with zero joined controllers says
    only that the wave was empty at that moment. It is not evidence that membership cannot change later.

    ### A controlled test is not every match

    Bot-addition and player-death tests isolate one condition in one world at one time. Ordinary
    matches add objectives, teammates, attacks, timing, and other game state. Read a controlled result
    as evidence for the tested relationship, not as a complete model of spawning.

??? "Why some questions remain unknown"

    | Kind of gap | Example | Safe interpretation |
    |---|---|---|
    | No attributed live path | A wave gains a member, but the writing function was not identified. | Report the visible sequence and name the writer Unknown. |
    | Negative result with a control | Sampled callables do not fire while a control callable does. | State the negative result for those callables in that sample only. |
    | Incomplete static surface | A deferred queue policy admits controllers, but its due-entry consumer is not recovered. | Describe admission, not the full spawn. |
    | Catalog truncation | A stage entry cannot be bound to a concrete receiver in the catalog build. | Keep the stage reference as configured and the receiver as Unknown. |
    | Single-sample evidence | One map shows a sequence or queuer in a specific match state. | State the map and state; do not infer a mode-wide rule. |

??? "Open questions"

    1. Did the observed player respawn use the recovered `NewSpawnSystemQueuer` → `JoinSpawn` path,
       and which native function creates the pawn?
    2. What activates a queue and selects a spawner and wave in each mode?
    3. What are the full wave-state transitions and replication timing?
    4. How do deferred queue entries reach a wave, and how are solo-queue entries promoted or cancelled?
    5. Do FFA, TDM, LTS, and TO differ in selection and scoring, or only in authored configuration?
    6. Which authored run-in spawner paths run in ordinary player spawns, and when is control released?
    7. Which spawn data is authoritative, replicated, or only local presentation and mode state?
    8. Does LTS bypass, constrain, or use the shared sequence/spawner/wave path?
    9. Which concrete spawner does a Team Objective stage select in the catalog build?
    10. How far do these bounded samples generalize to other maps and match states?

??? "How to use the guide responsibly"

    - To know what a spawner can do, read [Components](components.md) and
      [Spawner types](Spawner.md) with the Configured label in mind.
    - To understand the ownership model, read [How spawning works](how-spawning-works.md) and treat
      Inferred steps as a working model.
    - To check timing and queue behavior, read [Queues and timing](queues-and-timing.md).
    - To compare modes, read [Game modes](game-modes.md) and keep each Observed claim with its sample.
    - When a result matters for a new system, measure it in the context where it will be used. This
      guide is a map of known surfaces and their limits, not a substitute for measuring a live spawn.
