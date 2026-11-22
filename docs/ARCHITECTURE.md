# How RAC-2Modern sits on OpenRAC

RAC-2Modern makes content. OpenRAC is the engine. This page lists what OpenRAC already does, where
our files go, and what has to be added to OpenRAC itself. Links point at OpenRAC's `develop`
branch as of November 2026.

## OpenRAC, in short

- The **launcher** sets a game up from the player's own disc, extracts its levels, installs mods
  and plays the native port. Nothing derived from the game is downloaded.
- The **port** is the decompiled game, built for PC. Its renderer draws each kind of thing the PS2
  drew (terrain, ties, shrubs, mobys, sky, particles, 2D) natively, from the extracted levels
  ([docs/port/RENDERER.md](https://github.com/OpenRAC/OpenRAC/blob/develop/docs/port/RENDERER.md)).
- **Enhanced graphics** (Vulkan, experimental) adds probe GI baked on the player's computer, modern
  shadows, GTAO, FSR upscaling, Forward+ local lights, and a material system with lit, glass, fur,
  wet fur and foliage shading
  ([port/enhanced](https://github.com/OpenRAC/OpenRAC/blob/develop/port/enhanced/README.md),
  [port/materials](https://github.com/OpenRAC/OpenRAC/blob/develop/port/materials/README.md)).
  The launcher offers it for all three Going Commando discs, PAL included
  ([launcher/core/src/enhanced.rs](https://github.com/OpenRAC/OpenRAC/blob/develop/launcher/core/src/enhanced.rs)).

## Where our files go

`rac2-modern/` is a script mod (`"type": "script"`) with `"assets": "assets"`. While it is loaded,
the port reads a level's files from `rac2-modern/assets/level_NN/` before that level's own, by the
same relative path. Later mods come first, and every mod comes before the data packs
([MODS.md, section 3, "Assets"](https://github.com/OpenRAC/OpenRAC/blob/develop/docs/port/MODS.md#assets)).

| File in `assets/level_NN/` | What it does | Read by |
|---|---|---|
| `material-overrides.json` | the level's material catalog: which surface is metal, glass, foliage or emissive, and its roughness, tint and reflections. Merged last, so it wins | `port/scene/material_overrides.cpp` |
| `object-lights.json` | point and spot lights attached to object types | `port/enhanced/lighting/object_lights.cpp` |
| `textures/<name>.png` | a replacement for the level's texture of that name: any size, same shape | the level loader |
| `mobys/`, `ties/`, `shrubs/`, `terrain.glb` | replacement models, as OpenRAC's packs lay them out | the level loader |
| `classes.json` | added or replaced render classes (`{"moby": {"1234": {"mesh": ...}}}`) | the level loader |

The levels we start with, by the numbers OpenRAC loads them by
([editor/games.py](https://github.com/OpenRAC/OpenRAC/blob/develop/editor/games.py)):

| Folder | Level |
|---|---|
| `assets/level_00/` | Aranos (tutorial) |
| `assets/level_01/` | Oozla |

The manifest names only the PAL disc (`"games": {"rac2": ["pal"]}`). The discs number many
textures and classes differently, so a material rule written against PAL names may not fit the US
discs. They can be added once each rule has been checked on them.

## Models and textures

OpenRAC exports a level's models (glTF, with the game's skeletons) and textures (PNG) and imports
edited ones back ([editor/MODDING.md](https://github.com/OpenRAC/OpenRAC/blob/develop/editor/MODDING.md)).
The rules we design for:

- **Characters and objects** (mobys) keep the game's bones (`joint_NNN`), at most four weights a
  vertex, and need UVs. The port animates them from the game's own data.
- **Terrain** may have any number of vertices. Its lighting is its vertex colours. Ratchet still
  walks on the original collision, so the surfaces he stands on must stay where they were.
- **Textures** may be any size up to 8192 a side, but keep their shape, because the game's UVs
  stretch a texture over its whole area.
- **Data packs** (`"format": 1`) record hashes of what they replace, so that one pack works with
  every disc.

## What OpenRAC does not have yet

The look of the modern games needs more per-pixel detail than a colour texture and one roughness
value per material. OpenRAC's materials are set per material slot. Its import reads no normal,
roughness, metallic or occlusion maps. These become OpenRAC pull requests (roadmap, M6):

1. **Normal maps** for replacement models and terrain, with tangents from the glTF.
2. **Roughness, metallic and occlusion maps** (glTF's packed `metallicRoughnessTexture` and
   `occlusionTexture`).
3. Whatever else the two levels turn out to need.

Work on OpenRAC happens in a fork of OpenRAC and goes upstream as pull requests. Then the official
launcher ships it, and testers need nothing extra.
