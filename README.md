# RAC-2Modern

*Ratchet & Clank 2: Going Commando* (*Locked and Loaded* in Europe), given a modern look, one
planet at a time.

> **På svenska.** RAC-2Modern är en fan-remaster av Going Commandos två första planeter,
> **Aranos** och **Oozla**. Den körs ovanpå [OpenRAC](https://github.com/OpenRAC/OpenRAC), den
> dekompilerade PC-porten av spelet. Målet är en look i stil med de nya Ratchet & Clank-spelen, med
> nya material, ljus, texturer och modeller. Du behöver din egen skiva, och repot innehåller inget
> från spelet. Så här testar du: [docs/TESTA.md](docs/TESTA.md).

## What it is

RAC-2Modern is a mod for [OpenRAC](https://github.com/OpenRAC/OpenRAC), which decompiles the
PlayStation 2 game into C and runs it natively on PC from the player's own disc. OpenRAC already
draws the game with a modern Vulkan renderer (Enhanced graphics: probe lighting, modern shadows,
ambient occlusion, a material system). RAC-2Modern adds the content: new materials, lights,
textures and models, starting with:

| Level | Planet | Status |
|---|---|---|
| 0 | Aranos (tutorial) | planned |
| 1 | Oozla | planned |

The first target is the European disc (`SCES_516.07`, OpenRAC's `rac2-pal`).

**Status: 0.1.0, foundation.** The mod installs and loads, but it does not change anything on
screen yet. What comes next is in the [roadmap](docs/ROADMAP.md).

## Try it

You need OpenRAC's launcher and your own Going Commando disc as an `.iso` or `.chd`.

1. Install the [OpenRAC launcher](https://github.com/OpenRAC/OpenRAC/releases/latest), point it at
   the folder with your disc image, and play once.
2. On the **Mods** tab, choose **Add from a link** and paste
   `https://github.com/dakajod-lab/RAC-2Modern`.
3. Switch **RAC-2Modern** on, keep the **Mods** switch under Play on, and press Play.

Step by step, in Swedish, with what to report: [docs/TESTA.md](docs/TESTA.md).

## How it fits together

- **OpenRAC** is the engine: the launcher, the decompiled game, and the renderer.
- **`rac2-modern/`** is a script mod with an `assets/` folder. While it is loaded, the port reads
  each level's files from `assets/level_NN/` before the level extracted from the disc: material
  catalogs, authored lights, textures and meshes.
- **Engine features** that OpenRAC does not have yet, such as normal and roughness maps for
  replacement models, are written as pull requests to OpenRAC, so that its official launcher
  ships them.

Details are in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Layout

| Path | What it is |
|---|---|
| [`rac2-modern/`](rac2-modern/README.md) | the mod the launcher installs: manifest, script, `assets/` |
| [`docs/`](docs/) | roadmap, architecture, the testing guide |
| [`tools/`](tools/) | the content check, the SDK fetcher |
| [`ASSETS.tsv`](ASSETS.tsv) | where every picture, model and sound in the mod comes from |
| `openrac-mods.json`, `sdk.lock` | how the launcher and CI find the mod and the SDK it is packaged with |

## Rules

Nothing from the game disc and nothing ripped from other games goes into this repository. Every
asset is our own work and is listed in `ASSETS.tsv`. CI checks both. See
[CONTENT_POLICY.md](CONTENT_POLICY.md).

## License

GPL-3.0-or-later ([LICENSE](LICENSE)), like OpenRAC's port and launcher.

RAC-2Modern is an unofficial fan project. It is not affiliated with or endorsed by Sony Interactive
Entertainment or Insomniac Games. Ratchet & Clank is a trademark of Sony Interactive Entertainment.
