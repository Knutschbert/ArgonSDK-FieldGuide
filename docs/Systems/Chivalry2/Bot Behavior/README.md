# Chivalry 2 bot behavior guide

This guide explains how the game's normal melee bots are assembled, how their behavior candidates
are configured, how combat movement is controlled, and which parts can safely be tuned or reused.

## Start here

Bots are best understood as several connected layers:

1. **Behavior sets** provide groups of possible behaviors.
2. **Behaviors** describe a possible choice, such as Slash, Block, Wait, or Shove.
3. **Considerations** score how suitable that choice appears in the current situation.
4. **Actions** turn a chosen behavior into requests, such as attack, block, wait, or movement intent.
5. The **native combat controller** manages combat target, movement, facing, spacing, and combat
   state while the bot is fighting.

These layers are related, but they are not interchangeable. A bot can have behavior objects cached
without evidence that it is selecting them, and a bot can visibly fight through its combat
controller without proving which UtilityAI behavior started that fight.

!!! warning "The guide’s most important reading rule"
    **Configured** behavior is not necessarily **selected** behavior. A list of actions or event
    reactions tells us what the bot is equipped to consider; it does not, by itself, identify the
    winner of a live decision.

## Reading paths

| If you want to understand… | Read… |
|---|---|
| Why bot behavior is not a single script | [How bots work](how-bots-work.md) |
| How weights, inputs, and curves shape a choice | [Decision-making and scoring](decision-making.md) |
| The equations behind score shaping and spacing | [Behavior and movement formulas](formulas.md) |
| How documented considerations change from 0 to 1 | [Curve explorer](curve-explorer.md) |
| The exact `BS_*`, `BC_*`, `AC_*`, `I_*`, `TG_*`, and controller names | [Asset and function atlas](asset-atlas.md) |
| What attacks, blocks, feints, and reactions request | [Combat actions and reactions](combat-actions-and-reactions.md) |
| How a bot approaches, faces, circles, and maintains range | [Movement and spacing](movement-and-spacing.md) |
| What difficulty and tuning settings can safely change | [Tuning and difficulty](tuning-and-difficulty.md) |
| Which conclusions are firm and which remain open | [Evidence and limitations](evidence-and-limitations.md) |

## Evidence labels

The guide labels material by what supports it:

| Label | Meaning |
|---|---|
| **Observed** | Directly seen on a live bot in documented conditions. |
| **Configured** | Present in an authored behavior, behavior set, or class configuration. |
| **Recovered** | Established from the game implementation and described here in player-facing terms. |
| **Unknown** | Not established by the available evidence. |

The label tells you what a statement means. For example, an **Observed** spacing response says a
controlled test changed spacing; a **Configured** attack entry says an authored behavior can request
that attack. Neither statement alone proves a complete ordinary-match decision trace.

## Glossary

| Term | Meaning |
|---|---|
| **Decision maker** | A component that owns behavior candidates and can evaluate decisions. Normal melee controllers have general and combat-focused decision-making surfaces. |
| **Behavior set** | A named collection of behavior classes. It is an inventory of candidates, not a fight script. |
| **Behavior** | One candidate activity, with a relative weight, considerations, one action, and sometimes a target generator. |
| **Consideration** | A condition that turns a world signal into a 0–1 influence on a behavior’s score. |
| **Input** | The sensor behind a consideration, such as distance, elapsed time, nearby allies, or a random value. |
| **Curve** | The mapping that turns a normalized input into a preference or penalty. |
| **Action** | The work requested when a behavior is selected, such as issuing an attack order or holding block. |
| **Target generator** | A source of candidate targets for a behavior. Normal melee combat behaviors instead use the controller’s existing combat target. |
| **Combat target** | The actor currently being fought by the combat controller. |
| **Native combat controller** | The controller layer that owns combat mode, target, movement, spacing, facing, and attack state. |
| **Personality** | A configuration layer that can choose or override behavior-set and event-reaction settings. |
| **Event behavior** | A behavior candidate associated with a combat event such as an incoming attack or parry success. |

## What this guide is and is not

This guide avoids implementation-dump detail and speculative explanations. It also does not provide
instructions for enabling UtilityAI on sparring bots.
