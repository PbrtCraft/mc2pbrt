from util import singleton
from block.block import BlockBase
from block.blocktypes import *


@ singleton
class BlockCreator:
    def __init__(self):
        self.db = {}

    def __call__(self, name, state, biome_id):
        key = (name, tuple(sorted(state.items())), biome_id)
        if key not in self.db:
            self.db[key] = self._create(name, state, biome_id)
        return self.db[key]

    def _create(self, name, state, biome_id):
        def check(y): return name == y or name[-len(y)-1:] == "_" + y

        def prefix(y):
            return len(name) >= len(y)+1 and name[:len(y)+1] == y + "_"

        if name in ["air", "cave_air"]:
            return BlockAir(name, state, biome_id)
        elif check("bed"):
            # TODO
            return BlockNotImplement(name, state, biome_id)

        # Setup Model
        if check("door") or name in BlockBase.LONG_PLANT:
            return BlockHeight2(name, state, biome_id)

        elif check("leaves"):
            return BlockLeaves(name, state, biome_id)

        elif check("glass"):
            return BlockGlass(name, state, biome_id)

        elif check("banner"):
            # TODO
            return BlockNotImplement(name, state, biome_id)

        elif prefix("infested"):
            return BlockNormal(name[9:], state, biome_id)

        elif name == "nether_portal":
            return BlockNetherPortal(name, state, biome_id)

        elif check("slab"):
            return BlockSlab(name, state, biome_id)

        elif check("trapdoor"):
            return BlockTrapDoor(name, state, biome_id)

        elif check("stairs"):
            return BlockStairs(name, state, biome_id)

        elif check("fence") or check("wall"):
            return BlockFenceType(name, state, biome_id)

        elif check("fence_gate"):
            return BlockFenceGate(name, state, biome_id)

        elif name == "iron_bars":
            return BlockIronBars(name, state, biome_id)

        elif check("glass_pane"):
            return BlockGlassPane(name, state, biome_id)

        elif check("chest"):
            return BlockNotImplement(name, state, biome_id)

        elif check("sign"):
            return BlockNotImplement(name, state, biome_id)

        elif name in ["wheat", "beetroots", "melon_stem", "pumpkin_stem"]:
            return BlockStages(name, state, biome_id)

        elif name in ["potatoes", "carrots"]:
            def stage(x): return [0, 0, 1, 1, 2, 2, 2, 3][x]
            return BlockStages(name, state, biome_id, stage)

        elif name == "nether_wart":
            def stage(x): return [0, 1, 1, 2][x]
            return BlockStages(name, state, biome_id, stage)

        elif name == "cake":
            return BlockCake(name, state, biome_id)

        elif name == "hopper":
            return BlockHopper(name, state, biome_id)

        elif name == "farm_land":
            return BlockFarmLand(name, state, biome_id)

        elif name == "snow":
            return BlockSnow(name, state, biome_id)

        elif name == "redstone_wire":
            # TODO : d[0] = "redstone_dust_dot"
            return BlockNotImplement(name, state, biome_id)

        elif name == "repeater":
            # TODO : d[0] += "_1tick"
            return BlockNotImplement(name, state, biome_id)

        elif name == "tripwire":
            # TODO
            return BlockNotImplement(name, state, biome_id)

        elif name == "bubble_column":
            # TODO
            return BlockNotImplement(name, state, biome_id)

        elif name == "scaffolding":
            # TODO
            return BlockNotImplement(name, state, biome_id)

        elif name == "bamboo":
            # TODO
            return BlockNotImplement(name, state, biome_id)

        elif name == "sweet_berry_bush":
            # TODO
            return BlockNotImplement(name, state, biome_id)

        elif name == "cocoa":
            # TODO
            return BlockNotImplement(name, state, biome_id)

        elif name == "fire":
            return BlockFire(name, state, biome_id)

        elif name == "end_gateway":
            # TODO
            return BlockNotImplement(name, state, biome_id)

        elif name == "torch":
            return BlockTorch(name, state, biome_id)

        elif name == "wall_torch":
            return BlockWallTorch(name, state, biome_id)

        else:
            return BlockNormal(name, state, biome_id)
