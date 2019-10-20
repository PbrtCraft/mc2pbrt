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

        if name in ["air", "cave_air", "lava", "water"]:
            return BlockAir(name, state, biome_id)
        elif check("bed"):
            # TODO
            return BlockNotImplement(name, state, biome_id)

        # Setup Model
        if check("leaves"):
            return BlockLeaves(name, state, biome_id)

        elif check("glass"):
            return BlockGlass(name, state, biome_id)

        elif check("glass_pane"):
            return BlockGlassPane(name, state, biome_id)

        elif check("banner"):
            # TODO
            return BlockNotImplement(name, state, biome_id)

        elif prefix("infested"):
            return BlockNormal(name[9:], state, biome_id)

        elif check("chest"):
            return BlockChest(name, state, biome_id)

        elif check("sign"):
            return BlockNotImplement(name, state, biome_id)

        elif name == "bubble_column":
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
