# The mod's assets

While RAC-2Modern is loaded, OpenRAC's port reads a level's files from `level_NN/` here before the
level's own files, by the same relative path (OpenRAC's `docs/port/MODS.md`, section 3, "Assets").

| Folder | Level |
|---|---|
| `level_00/` | Aranos (tutorial) |
| `level_01/` | Oozla |

What a level folder can hold is listed in `docs/ARCHITECTURE.md` at the top of the repository.
Every picture, model and sound here has a row in `ASSETS.tsv` there.
