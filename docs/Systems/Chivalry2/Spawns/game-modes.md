# Spawning by game mode

Modes differ in what their level scripts author and in what live samples show. This page keeps those
two things separate: a configured sequence is not a confirmed respawn path, and one live sample is
not a rule for a whole mode.

| Mode | Configured | Observed | Unknown |
|---|---|---|---|
| **FFA** | Level scripts author a sequence reference and an activation call; maps expose different scoring and distance settings. | FFA Fighting Pit / InProgress had a single active looping sequence with one spawner and one empty wave with a short pre-spawn delay. | Whether that configuration is the ordinary player-respawn path; full actor and sequence inventories. |
| **TDM** | Separate faction sequences; Courtyard authors group-spawner references and Wardenglade authors named faction spawner references. Maps differ in simultaneous waves and interval length, with loop and fast-first-spawn flags. | TDM Courtyard / InProgress samples alternated between no live sequences and active faction sequences; a queuer instance under the mode object and faction-paired empty waves were present. TDM Wardenglade / InProgress showed a wave gaining one joined controller and then a new pawn. | Queue selection, which callable wrote membership, and whether the observed path holds on other maps. |
| **LTS** | Round and life settings on the mode; level scripts expose initial-spawner names and match-state presentation. | LTS Courtyard / WaitingToStart had two inactive faction sequences and a queuer but no waves. | Whether LTS bypasses, constrains, or uses the shared sequence/spawner/wave path, and when sequences activate. |
| **TO** | Stage scripts reference faction spawners, run-in spawners, sequence activation, and forward spawning. | No ordinary-match forward spawn was established. | Which concrete spawner a stage event selects in the catalog build, and whether forward spawns occur in ordinary play. |

??? "FFA details"

    **Configured.** Small FFA maps each author a level-script spawn-sequence reference and an
    activation call. Visible defaults differ: one map uses an FFA scoring method with a
    minimum-distance setting and penalty, another exposes larger minimum-distance values, and a third
    excerpt does not show equivalent numbers. Catalog truncation prevents a complete actor inventory.

    **Observed.** In FFA Fighting Pit / InProgress, a single active looping sequence had one
    configured spawner and one empty, non-control-restricted wave with a short pre-spawn delay. No
    joined or queued player was present, so this does not establish an ordinary respawn path.

??? "TDM details"

    **Configured.** Courtyard and Wardenglade author separate Agatha and Mason sequence construction
    and initialization paths:

    | Map | Authored spawner references | Simultaneous waves | Seconds between waves | Other visible flags |
    |---|---|---:|---:|---|
    | **Courtyard** | One named group-spawner reference per faction sequence | 2 | 7.5 s | Loop, keep one wave active, fast first spawn, and timing-to-half-interval override |
    | **Wardenglade** | Three named faction spawner references per faction sequence | 1 | 10 s | Loop, keep one wave active, fast first spawn, and timing-to-half-interval override |

    These are authored configuration values, not measured respawn periods or a guarantee that either
    sequence ran in a particular match. The visible catalog data does not establish complete spawner
    membership, a scorer class, queue selection, or the effect of each timing flag.

    **Observed.** TDM Courtyard / InProgress samples had no live sequence objects in one sample, a
    queuer instance under the mode object, and faction-paired empty waves; a later sample had active
    faction sequences. Adding bots filled the queuer's bot-waiting array and produced pawns while
    sampled wave membership stayed zero. **Inferred:** the mode owns that queuer as a policy; its
    creation was not observed.

    **Observed.** In TDM Wardenglade / InProgress, a controlled player-death test left the player
    without a pawn while a faction wave gained one joined controller; a new pawn was then possessed. A
    control callable fired during the test, while the sampled spawn-related callables did not. This is
    a bounded negative result for those entry points in that sample; the function that wrote the
    membership is **Unknown**.

??? "LTS details"

    **Configured.** Round and life settings are exposed on the mode, and level scripts reference
    initial spawner names and match-state presentation. The sampled catalog surface did not expose a
    sequence activation or queue relation, so the selected settings and path remain unestablished.

    **Observed.** LTS Courtyard / WaitingToStart already had two inactive faction sequence objects and
    a queuer, with no waves. Sequences can therefore exist before activation; what activates them is
    **Unknown**.

??? "Team Objective details"

    **Configured.** Bridgetown and Coxwell level scripts expose faction- and stage-specific spawner
    references, run-in-named objects, sequence calls, and both normal and forward spawn call shapes.

    **Unknown.** Catalog truncation kept a stage entry from being tied to a concrete receiver in the
    catalog build. A bounded recovery against a different source build found a receiver-specific stage
    path, but it cannot prove the catalog build's path. No ordinary-match forward spawn is established.

??? "How to read the mode samples"

    > [!warning] Keep samples and rules separate
    > Each Observed statement above comes from a specific map and match state. Do not read it as a
    > universal mode rule, and do not use it to fill the Unknown entries in the table.

For the queue policies behind these samples, see [Queues and timing](queues-and-timing.md).
