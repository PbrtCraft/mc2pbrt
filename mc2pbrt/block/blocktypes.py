from block.block import BlockBase
from tuple_calculation import minus, plus
from material import Matte, Glass, Light, Foliage

class BlockAir(BlockBase):
    def _build(self):
        return

class BlockNormal(BlockBase):
    def _build(self):
        if self.getLight():
            self.material = Light(self)
        self._addModel(self.name)

class BlockNotImplement(BlockBase):
    def _build(self):
        print("[Warning] %s block not implement." % self.name)

class BlockHeight2(BlockBase):
    def _build(self):
        if self.state["half"] == "lower":
            self._addModel(self.name + "_bottom")
        elif self.state["half"] == "upper":
            self._addModel(self.name + "_top")

class BlockNetherPortal(BlockBase):
    def _build(self):
        self.material = Light(self)
        if self.state["axis"] == "x":
            self._addModel("nether_portal_ns")
        else:
            self._addModel("nether_portal_ew")

class BlockSlab(BlockBase):
    def _build(self):
        if self.state["type"] == "double":
            if self._is("cobblestone_slab"):
                self._addModel(self.name[:-5])
            elif self.name == "stone_slab":
                self._addModel("stone_slab_double")
            elif self._is("brick_slab"):
                self._addModel(self.name[:-10] + "bricks")
            else:
                self._addModel(self.name[:-4] + "planks")
        elif self.state["type"] == "top":
            self._addModel(self.name + "_top")
        else:
            self._addModel(self.name)

class BlockTrapDoor(BlockBase):
    def _build(self):
        if self.state["open"] == "true":
            self._addModel(self.name + "_open")
        else:
            self._addModel(self.name + "_" + self.state["half"])

class BlockStairs(BlockBase):
    def _build(self):
        shape = self.state["shape"]
        transform = []
        model_name = self.name
        if shape[:5] in ["inner", "outer"]:
            model_name += "_" + shape[:5]
        if shape[-4:] == "left":
            transform.append({"type" : "rotate", "axis" : "y", "angle" : 90})
        if self.state["half"] == "top":
            transform.append({"type" : "scale", "axis" : "y", "value" : -1})
        self._addModel(model_name, transform)

class BlockFenceType(BlockBase):
    def _build(self): 
        self._addModel(self.name + "_post")
        side = self.name + "_side"
        mp = {"north" : 0, "east" : 3, "south" : 2, "west" : 1}
        for k in mp:
            if self.state[k] == "true":
                self._addModel(side, [
                    {"type" : "rotate", "axis" : "y", "angle" : 90*mp[k]}
                ])

class BlockFenceGate(BlockBase):
    def _build(self):
        x = self.name
        if self.state["in_wall"] == "true":
            x += "_wall"
        if self.state["open"] == "true":
            x += "_open"
        self._addModel(x)

class BlockIronBars(BlockBase):
    def _build(self):
        self._addModel(self.name + "_post")
        side = self.name + "_side"
        mp = {"north" : 0, "east" : 3, "south" : 2, "west" : 1}
        for k in mp:
            if self.state[k] == "true":
                self._addModel(side, [
                    {"type" : "rotate", "axis" : "y", "angle" : 90*mp[k]}
                ])

class BlockGlassPane(BlockBase):
    def _build(self):
        self._addModel(self.name + "_post")
        side = self.name + "_side"
        mp = {"north" : 0, "east" : 3, "south" : 2, "west" : 1}
        for k in mp:
            if self.state[k] == "true":
                self._addModel(side, [
                    {"type" : "rotate", "axis" : "y", "angle" : 90*mp[k]}
                ])

class BlockStages(BlockBase):
    """For plant with multiple stages"""
    def __init__(self, name, state, biome_id, stage_func = None):
        if stage_func is None:
            self.stage_func = lambda x: x
        else:
            self.stage_func = stage_func
        super(BlockStages, self).__init__(name, state, biome_id) 

    def _build(self):
        age = int(self.state["age"])
        self._addModel(self.name + ("_stage%d" % self.stage_func(age)))

class BlockCake(BlockBase):
    def _build(self):
        bit = int(self.state["bites"])
        if bit:
            self._addModel(self.name + ("_slice%d" % bit))
        else:
            self._addModel(self.name)

class BlockHopper(BlockBase):
    def _build(self): 
        if self.state["facing"] != "down":
            self._addModel(self.name + "_side")
        else:
            self._addModel(self.name)

class BlockFarmLand(BlockBase):
    def _build(self):
        if int(self.state["moisture"]) == 7:
            self._addModel("farm_land_moist")
        else:
            self._addModel("farm_land")

class BlockSnow(BlockBase):
    def _build(self):
        h = int(self.state["layers"])
        if h == 8:
            self._addModel("snow_block")
        else:
            self._addModel("snow_height%d" % (h*2))

class BlockTorch(BlockBase):
    def _build(self):
        self._addModel("torch")
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
                    key : face for key in ["up", "down", "west", "east", "north", "south"]
                }
            }]
        }
        self.models.append((fire, [], Light(self)))

class BlockWallTorch(BlockBase):
    def _build(self):
        self._addModel("wall_torch")
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
                "rotation": { "origin": [ 0, 3.5, 8 ], "axis": "z", "angle": -22.5 },
                "faces": {
                    key : face for key in ["up", "down", "west", "east", "north", "south"]
                }
            }]
        }
        self.models.append((fire, [], Light(self)))

class BlockLeaves(BlockBase):
    def _build(self):
        self.material = Foliage(self)
        self._addModel(self.name)

class BlockGlass(BlockBase):
    def _build(self):
        self.material = Glass(self)
        self._addModel(self.name)
