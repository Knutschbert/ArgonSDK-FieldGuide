# Decision-making and scoring

When a bot has more than one possible behavior, it does not simply choose the one with the largest
named weight. Each behavior starts with a relative bias, then its considerations make it more or
less suitable for the current situation.

The result is best understood as a ranking signal:

> “Given this target and situation, how suitable is this behavior compared with the other available
> behaviors?”

It is not a published percentage chance, and it is not a promise that the behavior will visibly run.

## The decision vocabulary

| Part | Role in a decision |
|---|---|
| **Behavior set** | A group of possible behaviors. |
| **Behavior** | One candidate, such as Slash, Block, Wait, or Shove. |
| **Weight** | The candidate’s starting relative bias. |
| **Consideration** | A test that changes suitability based on the present situation. |
| **Input** | The world signal a consideration reads. |
| **Curve** | The function that turns the input into a 0–1 influence. |
| **Action** | The request made if the behavior is selected. |
| **Target generator** | A way to produce candidate targets, when a behavior needs one. |

## What the normal combat behaviors are configured to consider

The normal melee combat set includes the following authored candidates:

| Behavior | Relative weight | Main configured concerns | Requested action |
|---|---:|---|---|
| Slash | 1 | Time since the last attack | Request a slash attack. |
| Overhead/Stab | 2 | Attack cooldown and nearby teammates | Request overhead or stab. |
| Feint attack | 1 | Randomness and time since the last feint behavior | Request an attack followed by a possible feint. |
| Block | 1 | Distance and time since the last block behavior | Hold parry briefly. |
| Wait | 1 | A constant low fallback score | Maintain its configured spacing intent and wait. |
| Shove | 2 | Recent enemy blocks and shove cooldown | Request shove. |

**Configured:** these are the normal melee behavior definitions.  
**Unknown:** which one wins in every ordinary-match combat situation.

!!! tip "How to read the table"
    A weight of 2 does not mean “twice as likely to happen.” The other conditions can reduce a
    candidate sharply, and the decision system also has active-action and interruption rules.

## Inputs are measurements, not decisions

An input reports a world value. The behavior decides how much to care about that value through its
curve.

| Input category | Example reader question |
|---|---|
| Distance | “Is the current combat target close enough?” |
| Time since last attack or behavior | “Has this action cooled down enough?” |
| Nearby allies | “Would this attack be awkward around teammates?” |
| Recent blocks | “Has the opponent recently blocked enough that a shove is attractive?” |
| Random value | “Should this lower-frequency variation be considered now?” |
| Constant | “Should this behavior retain a small fallback value?” |

The same input type can behave differently in two behaviors because each behavior can give it a
different range and curve.

## Curves turn measurements into preference

Inputs are normalized to a 0–1 range and then transformed by curves. A curve can make a behavior:

- steadily more attractive as a value rises;
- steadily less attractive as a value rises;
- almost unchanged until a threshold;
- strongly responsive to small changes;
- best in a middle band.

For example, a close-range defensive behavior can use a distance curve that scores well nearby and
poorly far away. A cooldown can use a curve that holds a behavior back immediately after use, then
allows it to recover.

The exact score-shaping formulas are in [behavior and movement formulas](formulas.md). That page
also explains why several considerations are combined as strong, softened multipliers rather than
as a simple average.

## Target generation differs between general and combat behavior

Some behavior types need to find a target first. A general engagement behavior can search for an
appropriate enemy or a movement behavior can search for a destination.

Normal melee **combat** behaviors are different: their target-generator field is empty. They are
configured around the controller’s already-established combat target.

This gives combat decision-making a simple practical dependency:

1. the controller needs a valid combat target;
2. combat behaviors evaluate the situation relative to that target;
3. a selected action requests combat work against that target.

If there is no valid target, a target-dependent candidate can be unsuitable even if its nominal
weight is high.

## From eligible to selected to complete

These stages should not be collapsed into one:

| Stage | Meaning |
|---|---|
| **Present** | The behavior exists in a set or runtime cache. |
| **Eligible** | Its target/context and basic conditions allow it to be considered. |
| **Scored** | Its considerations have produced a candidate score. |
| **Selected** | The decision system has chosen it over alternatives. |
| **Active** | Its action is currently in progress. |
| **Complete or interrupted** | Its action has reported completion or has been replaced under the action rules. |

!!! warning "Present is not selected"
    A live inventory can prove the first stage. It cannot, by itself, prove the later stages.
    This distinction is especially important for event behaviors, because a bot can cache the
    possible reactions without an observed event dispatch.

## Active actions and interruption

Actions are not necessarily instantaneous. Attack, block, wait, movement, and event-response
actions can persist until a combat-state transition, a timer, or another completion condition says
they are done.

The decision system has rules for whether an active action is ready to finish or may be interrupted.
This means a newly attractive behavior does not always replace the current action immediately.

**Recovered:** an active matching action can be preserved, while a completed or interruptible action
can be replaced by a new winner.  
**Unknown:** a complete public equation that combines all active-action, inertia, and
target-switching effects into the final score for every ordinary fight.

## Worked conceptual example

Imagine a bot that is close to its combat target shortly after using block:

1. The Block behavior’s distance input may favor blocking because the opponent is nearby.
2. Its “time since block” input may still penalize it because the bot blocked recently.
3. The combined score therefore may be lower than the distance alone suggests.
4. Wait, Slash, or another candidate can remain competitive.
5. Even if Block looks good, an existing active action may still be allowed to finish first.

This example explains the model. It does not claim a recorded bot must choose one particular result.

## What this controls, does not control, and leaves unknown

| Category | Summary |
|---|---|
| **Controls** | Weights, input ranges, curves, and considerations shape the relative suitability of authored behavior candidates. |
| **Does not control by itself** | A behavior’s weight or a single favorable input does not guarantee its selection or immediate execution. |
| **Unknown** | The complete ordinary-match winner trace and one closed-form model for inertia, active actions, target switching, and all runtime decision cadence. |
