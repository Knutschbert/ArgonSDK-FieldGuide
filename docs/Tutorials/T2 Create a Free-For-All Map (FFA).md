---
number headings: first-level 2, max 3, 1.1
---
## 1 Requirements
-  Unreal Engine 4.25.4
-  [recursively cloned](https://explainshell.com/explain?cmd=git+clone+--recursive) version of our  [[ArgonSDK#Repository]] 

## 2 Introduction
In this tutorial, we will create a simple FFA Map Using Sublevels (More info: [UE Docs: Sublevels](https://docs.unrealengine.com/4.27/en-US/Basics/Levels/CollaborateWithSublevels))

We will create 2 Sub-Levels:
- ``Atmospherics`` (reusable)
	- Lights, Sky
- ``FFA``
	- Spawner
	  
> [!faq]
> Splitting the level into these parts will allow you to reuse atmospherics in other levels, thus saving time when you’re just exploring. Alternatively you can create a single Level containing all actors in this tutorial


## 3 Atmospherics Level
### 3.1 Create a new Level
1. Navigate to `Content/Mods` directory  in `Content Browser
   ![[Pasted image 20231030162414.png]]
2. Create a new folder within and open it
   (`Right Click`→`New Folder` or using the `CTRL+N` shortcut)
3. Create a new Level and give it a name (e.g. `Example_Atmospherics`)
   `Right Click` → `Level`
    Open the level after naming
    ![[ffa_atm_create.gif]]
### 3.2 Add lights and fog to your Scene

1. In the `Place Actors` frame, search for and drag following actors into your scene:
   
   - ``Directional Light``
   - ``Sky Light``
   - ``Exponential Height Fog``
   - ``Sky Atmosphere``
   - ``Sphere Reflection Capture``
     
     ![[ffa_light_actors.gif]]

2. Activate `Atmosphere/Fog Sun Light` for the Directional Light in `Details` window
   > [!info]
> 
This allows you to adjust sun’s position with by moving your mouse while holding `CTRL+L`

   ![[Pasted image 20231030164948.png]]
### 3.3 (Optional) Reduce fog scattering
Set `Directional/Fog Inscattering Color`s  to black for the ``ExponentialHeightFog`` actor
### 3.4 (Optional) Group actors
Within the ``World Outliner``, select all actors and move them to a separate folder.
- `Right Click` → `Move To` →`Create New Folder`
  ![[Pasted image 20231030172109.png]]

## 4 FFA Level
### 4.1 Create a new ``Level`` in the same directory (e.g. `FFA_Example`)
![[Pasted image 20231030172859.png]]
### 4.2 Add Atmospherics Sublevel
1. Open the `Levels` window if not visible
	`Window` → `Levels`
2. Drag-And-Drop your Atmospherics level into the list.
3. `Right-Click` on the Level and change the `Streaming Method` to `Always Loaded`
   
   ![[Pasted image 20231030223405.png]]
4. Double-Click the `Persistent Level` entry to make it the active level
   ![[Pasted image 20231030223432.png]]
### 4.3 Create a floor
1. Drag-and-Drop a `Cube` from `Place Actors` window into your scene
   ![[Pasted image 20231030173708.png]]
2. Adjust the scale
   - Apply a `Material Instance` of your liking (e.g. `LS_StoneFloor02`)
   - Set Actor Scale values to ($X=50, Y=50, Z=0.1$) in the `Details` window
   ![[Pasted image 20231030173835.png|500]]
### 4.4 World Settings
1. Open `World Settings` window if not visible (`Window`→`World Settings`)
2. Adjust following Settings:
   - `Map Name`, `Map Description`: Visible when the map loads ingame
   - `Attacking Faction` : `FFA`
   - `Gamemode Type` : `Free for All`
   - `Kill Z` : -5000 _(this ensures that players/bots die when falling off the edge)_

### 4.5 Initial Spawners

1. Open your `Content Browser` and add a `BaseSpawner`  actor to your level
   ![[Pasted image 20231030180447.png]]
2. Adjust it’s Row/Column count and spacing in the `Details` window
   In this example, we’ll use a 4x4 grid with a spacing of 500
   ![[Pasted image 20231030180917.png]]
   The spawner visualization will reflect the changes immediately
   ![[Pasted image 20231030182632.png|500]]
3. In `World Settings`, assign the Spawner to `Attacker Initial Spawn`
   ![[Pasted image 20231030182921.png]]
4. Save your progress (`CRTL+SHIFT+A` to save everything)
### 4.6 Navigation Mesh (Bots)
A Navigation mesh will allow bots to plan their movements in the environment according to their current task. 

> [!note]
> 
YT videos explaining UE4 NavMeshes are available in [[Additional Ressources#^f89b4d|Additional Resources: Navigation]]

1. Drag a `Nav Mesh Bounds Volume` from the `Place Actors` window into your scene.
2. Scale and adjust it’s position to cover an area within your floor mesh
   _Press P to enable mesh visualization. Orange is your friend_
   ![[ffa_navmesh.gif]]
## 5 Testing your Map
### 5.1 Add to the list of packaged maps
1. `Right-Click` the `_Atmospherics` map in `Contentbrowser`
   - Select `Copy Reference` (_this will copy an internal path to clipboard_)
2. Open `Project Settings`
	1. Type “cook” in the search bar
	2. Add a new entry to `List of maps to include in a packaged build`
	3. Paste the copied reference and adjust the path. For example:
	   - Copied: `World'/Game/Mods/FieldGuide/Examples/Maps/Example_Atmospherics.Example_Atmospherics'`
	   - Target: `/Game/Mods/FieldGuide/Examples/Maps/Example_Atmospherics`
	![[Pasted image 20231030183852.png]]

### 5.2 Build, Cook, Copy
1. Build the scene lighting by clicking on `Build`
   ![[Pasted image 20231030184001.png]]
2. Save the map (`CTRL+SHIFt+S`)
3. Cook the map (``File`` → ``Cook Content for Windows``)
   _This step will create cooked assets under `ArgonSDK/Saved/Cooked/WindowsNoEditor/TBL/Content/<YourFolder>`_
   ![[Pasted image 20231030184903.png]]
4. (Optional) copy the cooked assets to game directory
   > [!note]
> This step is not required if your cooked `Mods` directory is symlinked to your game’s content directory

   1. Navigate to `ArgonSDK\Saved\Cooked\WindowsNoEditor\TBL\Content\`
   2. Copy the `Mods` folder to your Game’s Content dir (`Chivalry2\TBL\Content`)
### 5.3 Testing your map
> [!info]
> 
The [[Mod Loader GUI]] automatically detects custom maps in the `/Content/Mods` directory (also those loaded from a pak file). 

1. Launch the moddable version of the game using `Unchained Launcher`
2. Set $NumBots<=15$ , since we only added 16 spawn slots
3. Select `Custom` in the gamemode field. Your map should now be visible in the combo box to the left
   ![[Pasted image 20231030211428.png|500]]

After loading into map you should be able to spawn alongside bots.
   ![[Chivalry 2 Screenshot 2023.10.30 - 21.45.17.59.png]]
   
> [!hint]
> 
You and bots will spawn only once. Implementing Spawn Waves requires additional components and will be explained in next tutorial

> [!note]
> _Example maps created in this tutorial are available under `/Content/Mods/FieldGuide/Examples/Maps`_
## 6 P.S.

