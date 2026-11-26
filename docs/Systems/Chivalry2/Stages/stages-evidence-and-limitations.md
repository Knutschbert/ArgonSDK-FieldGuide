# Evidence, limits, and terminology

This section documents sampled maps and bounded observations. It is designed to
be useful without turning available configuration or a controlled probe into a
universal game rule.

## How to read the labels

| Label | Meaning |
|---|---|
| **Configured** | Authored world settings, serialized actors, level hooks, or defaults. This shows an available setup, not necessarily live dispatch. |
| **Recovered** | A validated native implementation. This says what the recovered body does, not which ordinary event called it. |
| **Observed** | A live measurement. It is qualified as bot-driven ordinary state, controlled trigger, or accelerated expiry where that matters. |
| **Unknown** | The available evidence does not establish it. |

Here **ordinary** means that the measured outcome was not directly written
for the test. An ordinary bot-driven round is still not evidence about human
combat or about every map.

## Important limits

- **Representative maps only:** one sampled map per mode does not establish
  cross-map authoring or lifecycle generality.
- **Controlled versus ordinary:** direct score, ticket, method, or round-count
  changes reveal a response path; they do not identify an ordinary gameplay
  caller.
- **Single-process observations:** authority order, replication delay, and
  RepNotify timing need a multi-client or server/client comparison.
- **Bounded negative results:** no stage-interface actor was observed in the
  sampled LTS/Arena reads; that does not prove absence across those modes.

## What remains unknown

| Area | Unknown |
|---|---|
| FFA | Ordinary score-limit kill dispatch, selected victor, natural tied-score sudden death, and the virtual award override's effect. |
| TDM | The natural caller of draw, exact killer/victim pairing and faction-loss rule for ticket changes, and ordinary defeat/draw selection. |
| Arena and LTS | The exact native life writer and ordinary victory caller, all faction-selection branches, LTS scored-stage instantiation, and level round-event dispatch. |
| TO | Ordinary objective score sources, draw usage, and timeout behavior for stages 2–5. |
| Networking | Authority ordering and replication/RepNotify timing. |
| Maps | Whether the sampled behavior generalizes to other maps in each mode. |

The observed Arena bot round did establish per-faction life-pool decrements and
a round-win/post-match sequence. Its native writer and caller remain unknown;
do not replace the observed result with a broader negative claim.

??? "Glossary"

    | Term | Meaning in this guide |
    |---|---|
    | **Stage** | A mode-owned lifecycle unit that can start, become ready, and provide a possible next state. |
    | **Round** | The native Arena-derived lifecycle observed in sampled LTS and Arena modes. |
    | **Ticket** | A per-faction count used by the sampled TDM ticket stage. |
    | **Timeout stage** | A stage whose relevant readiness path is duration expiry. |
    | **Victory stage** | A terminal or result-stage object that may become current in some sampled handoffs. |
    | **Transition stage** | A stage used as transition or warmup context before another active stage. |
    | **Current stage** | The stage presently exposed by a staged mode. A returned object is not automatically current. |
    | **Readiness** | The condition that permits a stage to complete; its source differs by implementation. |
