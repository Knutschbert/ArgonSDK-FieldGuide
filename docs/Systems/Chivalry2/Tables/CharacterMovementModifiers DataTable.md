Source: [CharacterMovementModifiers.csv](I:\UNCN\WS\SDK\Mods_Repos\ArgonSDK-FieldGuide\docs\Systems\Chivalry2\Tables\Data\CharacterMovementModifiers.csv)

## Dataview Tables (chunked)

```dataview
TABLE WITHOUT ID Index, ModifierCurve, Scale, MinValue, MaxValue, Acceleration, Deceleration, bDisableSprint
FROM csv("Data/CharacterMovementModifiers.csv")
```

## Regular Markdown Table

| Index | ModifierCurve | Scale | MinValue | MaxValue | Acceleration | Deceleration | bDisableSprint |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Grass | None | 1.000000 | 0.000000 | 1.000000 | 1.000000 | 1.000000 | False |
| Mud | None | 1.000000 | 0.000000 | 1.000000 | 1.000000 | 1.000000 | False |
| Uphill | None | 1.000000 | 0.000000 | 0.000000 | 0.900000 | 0.900000 | False |
| Downhill | None | 1.000000 | 0.000000 | 0.000000 | 0.900000 | 0.900000 | False |
| Water | None | 0.600000 | 0.000000 | 1.000000 | 1.000000 | 1.000000 | True |
| Crippled | None | 0.500000 | 0.000000 | 1.000000 | 1.000000 | 1.000000 | True |
| ShellShock | None | 0.500000 | 0.000000 | 1.000000 | 1.000000 | 1.000000 | True |
| MIssingLeg | None | 0.750000 | 0.000000 | 1.000000 | 1.000000 | 1.000000 | True |
| MissingBothLegs | None | 0.500000 | 0.000000 | 1.000000 | 1.000000 | 1.000000 | True |
| SlowingMud | None | 0.750000 | 0.000000 | 1.000000 | 1.000000 | 1.000000 | False |
