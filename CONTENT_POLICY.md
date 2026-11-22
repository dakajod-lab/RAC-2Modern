# Content policy

This repository is public. Everything in it must be ours to share. `tools/check_content.py` checks
these rules on every push and pull request.

## Never commit

- **Anything from the game disc:** disc images (`.iso`, `.chd`, ...), the executable
  (`SCES_516.07` and the like), WADs, sounds, movies, save files, and anything the OpenRAC
  launcher exports or dumps from your disc (`exports/`, `texture_dumps/`, extracted levels).
  These are your disc's data, for your own use only.
- **Assets taken from other games**, including the modern Ratchet & Clank games, and assets
  whose license does not allow redistribution under this project's license.
- **Pictures made by upscaling or retouching the game's own textures.** These are derived from
  the disc. A tool that upscales them on the player's own computer is fine. Its output is not.

## Allowed

- **Our own work:** pictures, models, sounds and materials made from scratch, by hand or by a
  script in this repository.
- **Names and hashes** that identify the game's files without copying them: a material rule
  may name `textures/terrain_0091.png` or a texture's hash, and a pack may record the hashes
  OpenRAC's import writes (`editor/MODDING.md` in OpenRAC).
- **Numbers learned by looking**, such as a light's position or a material's roughness.

## Provenance

Every picture, model and sound in a mod's `assets/` folder has a row in
[`ASSETS.tsv`](ASSETS.tsv):

| Column | What it holds |
|---|---|
| `path` | the file, from the repository's top |
| `origin` | `original` (made by hand) or `procedural` (made by a script in this repository) |
| `author` | who made it |
| `license` | normally `GPL-3.0-or-later` |
| `source` | the file it was made from: a `.blend`, a script in this repository, or a short description |

Models are committed as `.glb`, not as a `.gltf` with a separate `.bin`. The check refuses every
`.bin` file, because PS2 game files use that extension too.

## Working data

Keep your exports and dumps outside the repository, or in `private/`, which git ignores. Share them
only privately, and only with people who own the game.
