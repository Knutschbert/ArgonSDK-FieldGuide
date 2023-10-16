Source: [CharacterStats.csv](I:\UNCN\WS\SDK\Mods_Repos\ArgonSDK-FieldGuide\docs\Systems\Chivalry2\Tables\Data\CharacterStats.csv)

```dataview
TABLE WITHOUT ID Index, MovementSpeed, SprintBaseSpeed, SprintMaxSpeed, SprintStartTime, SprintStartMinTime, SprintTime, SprintDeceleration, SpawnSpeedBoost, SpawnBoostTime
FROM csv("Data/CharacterStats.csv")
```

```dataview
TABLE WITHOUT ID Index,SpawnBoostSprintTime, SpawnBoostDeceleration, SpawnBoostEnemyDistance, SpawnBoostEnemyTime, DownedMovementSpeed, DownedSprintSpeed, Health, HealthRegen, Overheal, HealingModifier
FROM csv("Data/CharacterStats.csv")
```

```dataview
TABLE WITHOUT ID Index,Stamina, StaminaRegen, DashTime, StrafeAccelerationModifier, ArmourRating, SpecialItemMaxCharge
FROM csv("Data/CharacterStats.csv")
```

