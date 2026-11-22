--!strict
-- RAC-2Modern (https://github.com/dakajod-lab/RAC-2Modern): a modern look for Going Commando.
--
-- The look is data in assets/ (material catalogs, lights, textures and models). The port reads it
-- for each level while this mod is loaded (OpenRAC's docs/port/MODS.md, section 3, "Assets"). This
-- script takes no hooks. It writes one line in the game's log, so that a tester can see the mod ran
-- and on which disc.

openrac.log(`RAC-2Modern is on: {openrac.game} {openrac.version}, mod interface {openrac.api}`)
