Source: [Abilities.csv](I:\UNCN\WS\SDK\Mods_Repos\ArgonSDK-FieldGuide\docs\Systems\Chivalry2\Tables\Data\Abilities.csv)

## Dataview Tables (chunked)

```dataview
TABLE WITHOUT ID Index, Animation, AnimationSection, AttackType, AbilitySpec, HeavyAttack, StartCombatState, HorseStartCombatState, bUseThrownAttackType
FROM csv("Data/Abilities.csv")
```

## Regular Markdown Table

| Index | Animation | AnimationSection | AttackType | AbilitySpec | HeavyAttack | StartCombatState | HorseStartCombatState | bUseThrownAttackType |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Slash | Slash | None | None | None | SlashHeavy | None | None | False |
| SlashHeavy | SlashHeavy | None | None | None | None | None | None | False |
| Overhead | Overhead | None | None | None | OverheadHeavy | None | None | False |
| OverheadHeavy | OverheadHeavy | None | None | None | None | None | None | False |
| Stab | Stab | None | None | None | StabHeavy | None | None | False |
| StabHeavy | StabHeavy | None | None | None | None | None | None | False |
| Parry | Parry | None | None | None | None | Release | None | False |
| SprintAttack | SprintAttack_LeapingOverhead | None | None | None | None | None | None | False |
| Shove | Kick_Front | None | None | None | None | None | None | False |
| KickLow | Kick_Low | None | None | None | None | None | None | False |
| Jab | Jab_Body_LeftHook | None | None | None | None | None | None | False |
| Headbutt | Jab_Body_Headbutt | None | None | None | None | None | None | False |
| InitiativeAttack | Jab_Body_LeftHook | None | None | None | None | None | None | False |
| SprintShove | SprintTackle_Shove | None | None | None | None | None | None | False |
| Special | Special_PowerUppercut | None | None | None | None | None | None | False |
| Throw | Throw_Overhead | None | None | None | None | None | None | True |
| ShootBow | Slash | None | None | None | None | None | None | False |
| DownedPunch | Downed_Punch | None | None | None | None | DownedPunch | None | False |
| SwitchItem | None | None | None | None | None | SwitchItem | None | False |
| ShootBallista | Trigger_Ballista | None | None | None | None | None | None | False |
| ShootCatapult | None | None | None | None | None | None | None | False |
| Emote | None | None | None | None | None | Emote | None | False |
| HorseKickFront | Kick | Front | None | None | None | HorseSlowdown | Kick | False |
| HorseKickBack | Kick | Back | None | None | None | HorseSlowdown | Kick | False |
| HorseEmote | Emote | Battlecry | None | None | None | HorseEmote | None | False |
| SpearPlant | Special_PowerUppercut | None | None | None | None | None | None | False |
| SpearCharge | SprintAttack_LeapingOverhead | None | None | None | None | None | None | False |
| LanceCharge | Special_PowerStab | None | None | None | None | None | None | False |
| Dash | None | None | None | None | None | Dash | None | False |
| DashLeft | None | None | None | None | None | Dash | None | False |
| DashRight | None | None | None | None | None | Dash | None | False |
| DashBack | None | None | None | None | None | Dash | None | False |
| Jump | None | None | None | None | None | Jump | None | False |
| FistSpecial | Special_PowerUppercut | None | None | None | None | None | None | False |
| CrossbowAttack | Slash | None | None | None | None | None | None | False |
| BatteringRamAttack | None | None | None | None | None | None | None | False |
| BatteringRamCharge | None | None | None | None | None | None | None | False |
| LoadItem | Throw_Overhead | None | None | None | None | None | None | False |
| HorseSpecial | Mount_Charge | None | None | None | None | None | None | False |
| HorseJump | Leap | Leap_Start | None | None | None | HorseJump | None | False |
| HorseCharge | Charge | Charge | None | None | None | HorseCharge | None | False |
| UseItem | None | None | None | None | None | Use | None | False |
| EmoteHeld | None | None | None | None | None | Emote | None | False |
| QuickThrow | Throw_Quick | None | None | None | None | None | None | True |
| SprintCharge | SprintAttack_Charge | None | None | None | None | None | None | False |
| DropItem | None | None | None | None | None | None | None | False |
| UseBandage | None | None | None | None | None | Use | None | False |
| TopplingStoneCharge | None | None | None | None | None | None | None | False |
| TopplingStoneAttack | None | None | None | None | None | None | None | False |
| HorseDashForward | Dash | Forward | None | None | None | HorseSlowdown | None | False |
| HorseDashForwardRight | Dash | Forward_Right | None | None | None | HorseSlowdown | None | False |
| HorseDashRight | Dash | Right | None | None | None | HorseSlowdown | None | False |
| HorseDashBackRight | Dash | Back_Right | None | None | None | HorseSlowdown | None | False |
| HorseDashBack | Dash | Back | None | None | None | HorseSlowdown | None | False |
| HorseDashBackLeft | Dash | Back_Left | None | None | None | HorseSlowdown | None | False |
| HorseDashLeft | Dash | Left | None | None | None | HorseSlowdown | None | False |
| HorseDashForwardLeft | Dash | Forward_Left | None | None | None | HorseSlowdown | None | False |
| ShootBombard | None | None | None | None | None | None | None | False |
