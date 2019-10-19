from block.block import BlockBase
from tuple_calculation import minus, plus
from material import Matte, Glass, Light, Foliage


class BlockAir(BlockBase):
    def build(self):
        return


class BlockChest(BlockBase):
    def build(self):
        self.addModel("entity/chest")


class BlockNormal(BlockBase):
    def build(self):
        if self.getLight():
            self.material = Light(self)
        self.useBlockstate()


class BlockNotImplement(BlockBase):
    def build(self):
        print("[Warning] %s block not implement." % self.name)


class BlockTorch(BlockBase):
    def build(self):
        self.addModel("torch")
        # Hard-code fire part
        face = {
            "uv": (0, 0, 1, 1),
            "texture": "block/sea_lantern"
        }
        eps = tuple([.001]*3)
        fire = {
            "elements": [{
                "from": minus((7/16, 8/16, 7/16), eps),
                "to": plus((9/16, 10/16, 9/16), eps),
                "faces": {
                    key: face for key in ["up", "down", "west", "east", "north", "south"]
                }
            }]
        }
        self.models.append((fire, [], Light(self)))


class BlockWallTorch(BlockBase):
    def build(self):
        self.addModel("wall_torch")
        # Hard-code fire part
        face = {
            "uv": (0, 0, 1, 1),
            "texture": "block/sea_lantern"
        }
        eps = tuple([.001]*3)
        fire = {
            "elements": [{
                "from": minus((-1/16, 11.5/16, 7/16), eps),
                "to": plus((1/16, 13.5/16, 9/16), eps),
                "rotation": {"origin": [0, 3.5, 8], "axis": "z", "angle": -22.5},
                "faces": {
                    key: face for key in ["up", "down", "west", "east", "north", "south"]
                }
            }]
        }
        self.models.append((fire, [], Light(self)))


class BlockLeaves(BlockBase):
    def build(self):
        self.material = Foliage(self)
        self.addModel(self.name)


class BlockGlass(BlockBase):
    def build(self):
        self.material = Glass(self)
        self.addModel(self.name)


class BlockFire(BlockBase):
    def build(self):
        self.material = Light(self)
        # Hard-code fire part
        face = {
            "uv": (0, 0, 1, 1),
            "texture": "block/fire"
        }
        rot = {"origin": [8, 8, 8], "axis": "y", "angle": 45, "rescale": True}
        fire = {
            "elements": [{
                "from": [0, 0, .5],
                "to": [1, 1, .5],
                "rotation": rot,
                "faces": {"north": face, "south": face}
            }, {
                "from": [.5, 0, 0],
                "to": [.5, 1, 1],
                "rotation": rot,
                "faces": {"west": face, "east": face}
            }
            ]
        }
        self.models.append((fire, [], Light(self)))
