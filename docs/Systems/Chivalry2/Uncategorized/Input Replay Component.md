Controller Component which allows you to record and replay player inputs.
See [[ref:UInputReplayComponent]]

<iframe width="560" height="315" src="https://www.youtube.com/embed/xXJyTHf9GaE?si=tBqGWcFSvqak454-" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

Recorded data is written to a binary file. It can be loaded and played back on an NPC or yourself*
Resulting `.input` files are written to `%LocalAppData%\Chivalry 2\Saved\InputReplay\*.input`
The filename can be specified by user.
This component offers other functions, for example stitching input replays together.
### What is recorded
- Mouse movement
- WASD movement
- All attacks
- Crouch
- Battlecry
### What isn’t recorded
- Emotes
### Caveats
- By default, bots are locked to a walking state. Make sure you don’t sprint while recording
- Turning on the spot is a bit tricky. You may need to exaggerate your turns
  
\* by default, mouse movement overrides input replay on yourself
# Minimal Example
1. Add a [[ref:UInputReplayComponent]] to your local [[ref:ATBLPlayerController]] using the [[ref:CreateInputReplayComponent|CreateInputReplayComponent]] node.
2. Record a `.input` file using [[ref:TBLPlayerController::InputRec|InputRec]].
3. Spawn an NPC using [[ref:SpawnTBLAIFromClass]] and make it a [[ref:SetDummyBot|dummy bot]].
4. Play the recorded file [[ref:InputReplayComponent::InputPlay|on the NPC]] or [[ref:TBLPlayerController::InputPlay|on yourself]].
## BlueprintUE
<div class="bue-embed" data-bp="input-replay" data-height="600px"></div>
