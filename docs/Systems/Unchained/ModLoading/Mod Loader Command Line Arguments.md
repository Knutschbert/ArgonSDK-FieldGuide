| Parameter             | Example                                        | Description                                              |
| --------------------- | ---------------------------------------------- | -------------------------------------------------------- |
| --next-map-name       | --next-map-name ffa_wardenglade                | Sets the map the server will travel to after login       |
| --next-map-mod-actors | --next-map-mod-actors GiantSlayers,ManlyMen,.. | Comma-Separated list of mod actors to enable on next map |
| --all-mod-actors      | --all-mod-actors GiantSlayers,…                | List of available mods (required for Mod Loader GUI)     | 


-  `--next-map-name ffa_wardenglade`
    Sets the map the server will travel to after login      
- `--all-mod-actors FlashBlades,GiantSlayers,TestMod`
  let the mod loader know which mods are available
- `--next-map-mod-actors GiantSlayers,ManlyMen,..`
    Comma-Separated list of mod actors (pak names) to enable on next map
With this you should be able to load into the map and enable mods (you'd have to DL pak releases manually)
if you want to change mods between maps, you can do `servertravel to_raid?mods=FlashBlades,...`