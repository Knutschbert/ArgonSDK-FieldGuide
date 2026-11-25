# Behavior and movement formulas

This page explains the parts of bot behavior that can be expressed as equations without pretending
that the entire decision system is a known mathematical model.

## Reading the formulas

The formulas below describe **configured scoring** and the verified portions of **spacing
selection**. They do not prove that a behavior was evaluated, selected, or executed during a
particular fight.

!!! warning "A score is not a recorded decision"
    A behavior can be configured with a weight and considerations while the decision loop is
    inactive, while another layer drives combat, or while another candidate wins. Treat the
    equations as an explanation of the authored scoring machinery, not a replay of every bot
    action.

## From a world value to a consideration score

An input reads a world value such as distance, elapsed time, or a nearby-team influence. Its
configured range turns that value into a normalized quantity:

\[
  x = \operatorname{clamp}\left(
    \frac{v-v_{\min}}{v_{\max}-v_{\min}},
    0,
    1
  \right)
\]

Plaintext:

```text
normalized = clamp((value - range_min) / (range_max - range_min), 0, 1)
```

Where:

| Symbol | Meaning |
|---|---|
| \(v\) | The value read from the game world. |
| \(v_{\min}\), \(v_{\max}\) | The configured meaningful range for that input. |
| \(x\) | A normalized value from 0 to 1. |

The bot then maps \(x\) through a configured curve and clamps the result to a score from 0 to 1:

\[
  c = \operatorname{clamp}\bigl(f(x; M,K,C,B), 0, 1\bigr)
\]

Plaintext:

```text
consideration_score = clamp(curve(normalized, M, K, C, B), 0, 1)
```

The common curve shapes are:

| Curve | Formula before final clamping | Reader interpretation |
|---|---|---|
| Linear | \(M(x-C)+B\) | A steady preference or penalty as the input rises. |
| Polynomial | \(M(x-C)^K+B\) | A preference or penalty that can be gentle at first and steep later, or the reverse. |
| Logistic | \(\frac{M}{e^{-10K(x-C-0.5)}+1}+B\) | A threshold-like S curve. |
| Normal | \(M e^{-30K(x-C-0.5)^2}+B\) | A middle-band preference: not too low, not too high. |
| Sine | \(\frac{\sin((x-C)2\pi)M+1}{2}+B\) | A periodic variation; uncommon in the documented melee behaviors. |

`M` controls direction and strength, `K` controls shape or steepness, `C` moves the curve
horizontally, and `B` supplies its base level. A positive `M` generally rewards larger inputs;
a negative `M` generally penalizes them.

??? info "Other supported curve types"
    The underlying system also has Logit curves. They are part of the general scoring machinery,
    but they are not necessary to understand the documented normal melee examples. The technical
    research record contains the full curve catalog.

## Combining considerations into a behavior score

A behavior begins with a base value \(W\), derived from its relative weight and decision context.
For \(n\) considerations, the known behavior scorer uses a compensation amount:

\[
  a = 1-\frac{1}{n}
\]

Each consideration score \(c_i\) contributes a softened multiplier:

\[
  q_i = c_i \left(1+(1-c_i)a\right)
\]

The resulting configured behavior score is:

\[
  S = W\prod_{i=1}^{n} q_i
\]

Plaintext:

```text
compensation = 1 - 1 / number_of_considerations
adjusted_i = score_i * (1 + (1 - score_i) * compensation)
behavior_score = base_weight * product(adjusted_i)
```

This is not plain multiplication. A high consideration score changes little. A low score strongly
reduces the behavior, but compensation makes the reduction less abrupt than multiplying the raw
scores alone.

If there are no considerations, the behavior retains its base value. While scoring, a behavior can
stop evaluating later considerations once the running result is already too low to matter.

### Example: a close-range block candidate

The normal melee block behavior has a distance consideration. In reader terms:

1. Measure distance to the current combat target.
2. Normalize that distance against the behavior's configured distance range.
3. Curve it so close targets score well and distant targets score poorly.
4. Multiply that result with the behavior's other condition(s) and its base weight.

This explains why a block candidate can become unattractive at range. It does **not** establish
that the block action will win, because other candidates, active actions, and decision rules can
still affect the outcome.

## What the formulas do not quantify

The equations above are evidence-backed for input normalization, curve evaluation, and the
consideration combination step. They do not provide a complete probability model of combat:

- A behavior weight is a relative bias, not a percentage chance.
- Inertia and active-action modifiers exist, but their complete effect on final winner selection
  should not be represented as a known closed-form equation here.
- The final decision process can preserve, interrupt, or replace an active action.
- A configured behavior may never be evaluated in a particular live situation.

## A supportable spacing model

The native combat controller selects a spacing goal from the current combat context. In simplified
form:

\[
  d_{\text{requested}} =
  \begin{cases}
    d_{\text{attack}} & \text{when an active attack order supplies a usable attack distance} \\
    d_{\text{facehug}} & \text{for the facehug intent} \\
    d_{\text{own-range}} & \text{for the bot's own attack-range intent} \\
    d_{\text{enemy-range}} & \text{for the outside-enemy-range intent} \\
    d_{\text{standoff}} & \text{for the standoff intent}
  \end{cases}
\]

The controller then applies a runtime engagement-distance variation:

\[
  d_{\text{goal}} = d_{\text{requested}} \times \nu(t)
\]

Plaintext:

```text
goal_distance = selected_spacing_distance * runtime_variance(time)
```

The existence of the time-varying variance is established, but it is not a supported public tuning
control and should not be assigned a made-up equation. The realized range also depends on
navigation, target motion, combat state, and controller updates, so it should not be treated as
identical to \(d_{\text{goal}}\).

## What this controls, does not control, and leaves unknown

| Category | Summary |
|---|---|
| **Controls** | Configured inputs and curves shape a candidate's score; verified spacing settings can change the requested distance goal. |
| **Does not control by itself** | A single weight, curve, or strafe request does not guarantee a selected action or deterministic orbit. |
| **Unknown** | The complete closed-form winner-selection model, the public control of runtime strafe variance, and exact ordinary-match decision causality. |

## Technical source boundary

These equations are compiled from the preserved UtilityAI scoring documentation and the
bot-behavior research record. The latter contains the technical implementation evidence; this page
intentionally presents only the user-facing conclusion.
