# Evidence and limitations

The bot has several layers, and different evidence can establish different things. This page keeps
the guide precise about what is known, what is configured, and what remains open.

## Evidence labels

| Label | Meaning |
|---|---|
| **Observed** | Seen on a live bot under documented conditions. |
| **Configured** | Present in a behavior, set, action, or controller configuration. |
| **Recovered** | Established implementation behavior, described here in game-facing terms. |
| **Unknown** | Not established by the available evidence. |

## Current model at a glance

| Topic | What is established | Important limit |
|---|---|---|
| Normal combat inventory | Normal melee bots can have Slash, Overhead/Stab, Feint, Block, Wait, and Shove candidates. | Candidate presence does not identify the winner of a live decision. |
| Behavior scoring | Inputs are normalized and curved; behavior considerations combine into a score. | The complete final winner model is not represented as one known public equation. |
| Combat target and engagement | A controller can establish a combat target, enter combat, and drive combat movement. | Visible engagement does not prove a General behavior was the recorded cause. |
| Native movement | Native combat movement can approach, maintain range, face a target, and produce lateral motion. | Public deterministic control of lateral direction and strength is not established. |
| Spacing | Close-pressure range is a verified controller-side spacing control in controlled tests. | Some written fields and named intents can be reset or overridden by active behavior/action paths. |
| Waypoint movement | Path-following can make repeatable scripted rings and routes. | It is not the same as native combat orbiting and tends to face movement direction. |
| Event behavior sets | Multiple incoming-attack, shove, parry-success, damage, and guard-break response inventories are configured. | A configured set is not proof that an event dispatched it or that one of its behaviors won. |
| Personality and variants | Normal and simplified variants exist; sampled direct/owner-created bots cached `_Normal`, while the authored `Normal` row names `_Dumb`. | The row-to-bot selector and application path are not reconciled; do not generalize the sampled cache to all default bots. |
| Ordinary-match causality | Some direct normal-bot combat observations exist. | A complete normal-match trace from perception through each selected behavior to each visible action is not established. |

## What not to infer

### A behavior cache is not an action log

Runtime behavior objects can be present because a decision maker materialized its configured sets.
That gives useful information about available candidates and their parameters. It does not prove:

- that the decision maker is actively evaluating them;
- that a particular behavior was selected;
- that its action is currently in progress;
- that it caused the visible swing, block, or movement.

### Native combat is not proof of one specific UtilityAI winner

A controller can visibly pursue a target, maintain spacing, face an opponent, attack, and cycle
through combat states. That establishes the controller’s combat layer. It does not alone tell us
whether a General behavior, Combat behavior, external setup, or another path caused the engagement.

### Authored reaction options are not a reaction replay

An incoming-attack set can contain block, dodge, wait, or jab options. A parry-success set can
contain riposte and shove options. That tells us what the bot is configured to consider.

It does not establish:

- that the event was received by the decision layer;
- that the event set was evaluated;
- which candidate scored highest;
- whether an active action prevented an immediate replacement;
- what reaction will happen in every fight.

### A controlled test is not every match

Controlled tests are useful because they isolate a target, range, behavior weight, or movement
condition. Ordinary matches add moving targets, teammates, objectives, attacks, hits, pathing,
timing, and broader AI state. A controlled result should be read as evidence for the tested
relationship, not as a complete model of all match behavior.

## Why some questions remain unknown

| Kind of gap | Example | Safe interpretation |
|---|---|---|
| No suitable live observation | No naturally active ordinary AI is available in the current world. | Do not manufacture ordinary-match causality from a test spawn. |
| No supported public control | Runtime lateral variation affects combat movement but has no stable public tuning interface. | Do not publish private or guessed controls as a recipe. |
| Incomplete causal trace | A configured event set exists, but a winner is not attributed during a live reaction. | Describe it as an available reaction inventory, not a guaranteed response. |
| Different layers overlap | A controller fights while a behavior cache exists. | Keep controller execution separate from decision selection. |

## How to use the guide responsibly

Use the guide to answer one of these questions:

- **What can this bot consider?** Read the behavior and asset pages.
- **Why might this candidate become more or less attractive?** Read decision-making and formulas.
- **What produces target-facing combat movement?** Read movement and spacing.
- **What settings are safe to tune?** Read tuning and difficulty.
- **How certain is a claim?** Return to this page and check its evidence label.

When a result matters for a new control system, validate it in the specific context where it will be
used. The guide supplies a map of the known surfaces and their limits; it is not a substitute for
measuring a new runtime behavior.
