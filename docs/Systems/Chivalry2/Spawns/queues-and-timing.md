# Queues and timing

Queuers are admission and timing policies. They decide which controller is recorded for a future
spawn and how long that controller waits; they do not create the wave themselves.

## Three recovered policies

| Policy | Admission rule | Timing model | Recovered cancellation behavior |
|---|---|---|---|
| **Wave spawn queuer** | Requires an active, eligible queue; rejects a controller already recorded. | Records respawn/wave timing metadata for the controller and adjusts the following wave schedule. | A recovered removal method searches the recorded entries and erases matching controllers. |
| **Cumulative queuer** | Requires an active queue and eligibility; rejects duplicates. | Starts from a beginning respawn time; a controller with history instead uses the recorded value plus an accumulated increment. | **Unknown** for its removal path. |
| **Group queuer** | Requires an active, valid, eligible controller; treats membership in either of its two arrays as already admitted. | Uses a shared group window. Entrants while the window is still open join the active group; later entrants go to a separate solo queue. | The recovered removal method searches only active group participants, not the solo queue. |

**Recovered.** The cumulative policy is per-controller and grows with each recorded respawn. The
group policy is shared across participants and explicitly separates late entrants. These are
different policies, not two names for the same timer.

**Unknown.** What consumes a due entry, how a solo entry is promoted into a group or spawned on its
own, whether another cancellation route covers solo entries, and which mode uses which deferred-queue
policy for players.

> [!warning] Admission is not a spawn
> Being recorded in a queue means the policy accepted the controller. It is not proof of a wave
> join or of a pawn being created. The step from a due entry to an actual spawn is not established.

??? "Cumulative timing expression"

    \[
    d_{\mathrm{next}} =
    \begin{cases}
    d_{\mathrm{start}}, & \text{when the controller has no recorded cumulative delay} \\
    d_{\mathrm{previous}} + d_{\mathrm{increment}}, & \text{when it has recorded history}
    \end{cases}
    \qquad
    t_{\mathrm{due}} = t_{\mathrm{now}} + d_{\mathrm{next}}
    \]

    Plaintext: when the cumulative queuer accepts a controller, it records the configured starting
    delay for that controller's first recorded admission. On a later admission, it records the
    controller's previous delay plus the configured cumulative increment. It also records a due world
    time by adding that chosen delay to the current world time. This is a recovered **admission** rule,
    not a measured pawn-arrival time or a schedule for every wave and mode.

??? "Additional timing and queue evidence"

    > [!info] A separate recovered queuer path
    > `NewSpawnSystemQueuer` is not one of the three deferred policies above. Its recovered request
    > path filters eligible waves, compares their `GetTimeLeft` results, and invokes `JoinSpawn` on the
    > lowest-result wave through native virtual dispatch. This establishes an implementation path for
    > that queuer, not that the path ran during an observed player respawn or that it consumes due
    > entries from the three policies above.

    **Configured.** Level and class setup exposes timing knobs such as wave interval, number of
    simultaneous waves, looping, keeping one wave active, a fast first spawn, a minimum wait time, and
    a pre-spawn delay. Different maps author different values. These settings describe the configured
    schedule; they do not by themselves show that a schedule was followed in a particular match.

    **Observed — ordinary player respawn.** In the TDM Wardenglade / InProgress sample, a controlled
    player-death test left the player without a pawn while a faction wave gained one joined controller,
    and then a new pawn appeared. A queuer instance was present with an empty bot-waiting array
    throughout. This is one sample, not a general admission rule.

    **Observed — controlled bot test.** In the TDM Courtyard / InProgress sample, adding a large number
    of bots filled the queuer's bot-waiting array immediately and produced bot pawns over the following
    samples, while sampled wave membership stayed at zero. Removing the bots returned the world to its
    earlier state. This demonstrates a bot-admission surface; it does not establish the ordinary
    player-respawn path.

    **Observed — wave objects are transient.** TDM Courtyard / InProgress and TDM Wardenglade /
    InProgress samples showed waves appearing or rotating among placed spawners; an empty wave in
    one snapshot is not evidence that waves never hold players. By contrast, the LTS Courtyard /
    WaitingToStart sample had two inactive sequences and a queuer but **no waves**. A pre-round
    absence is not a claim about LTS during play.

??? "Timing questions that remain open"

    | Question | Status |
    |---|---|
    | Which code consumes due entries from the wave, cumulative, or group queues? | **Unknown** |
    | Which deferred-queue policy does each mode use for players? | **Unknown** |
    | How are solo-queue entries promoted or cancelled? | **Unknown** |
    | What are the real wave-state transitions on a client? | **Unknown** |
    | When is player control released during the spawn? | **Unknown** |
    | Do the configured intervals and delays describe the live schedule exactly? | **Unknown** |

For the configured values by mode, see [Game modes](game-modes.md). For the evidence behind each
label, see [Evidence and limitations](spawning-evidence-and-limitations.md).
