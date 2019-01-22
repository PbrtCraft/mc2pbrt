from resource import ResourceManager
from util import *

class Block:
    def __init__(self, name, state, biome_id, model_loader, biome_reader):
        self.name = name
        self.state = state
        self.ldr = model_loader
        self.bdr = biome_reader
        self.biome_id = biome_id
        # [(Model, Transform)]
        self.models = []
        
        self._build()

        self.solid_block = set([
            "stone", "podzol", "clay",
        ])

        self.solid_type = [
            "ore", "granite", "diorite", "andesite", "planks", "dirt", "block",
            "wood"
        ]

    def _is(self, y):
        return self.name == y or self.name[-len(y)-1:] == "_" + y

    def canPass(self):
        if self.name in self.solid_block:
            return False
        for t in self.solid_type:
            if self._is(t):
                return False
        return True

    def _getModel(self, name):
        model = self.ldr.getModel("block/" + name)
        if "elements" not in model :
            return None
        return model

    def _addModel(self, name, transforms = None):
        mdl = self._getModel(name)
        if not mdl:
            return
        self.models.append((mdl, transforms))

    def _build(self):
        if self.name == "air" or self.name == "cave_air":
            return
        elif self.name.find("bed") != -1:
            return

        long_plant = set(["tall_seagrass", "sunflower", "lilac", "rose_bush", 
                          "peony", "tall_grass", "large_fern"])

        if self._is("door") or self.name in long_plant:
            if self.state["half"] == "lower":
                self._addModel(self.name + "_bottom")
            elif self.state["half"] == "upper":
                self._addModel(self.name + "_top")

        elif self.name == "nether_portal":
            if self.state["axis"] == "x":
                self._addModel("nether_portal_ns")
            else:
                self._addModel("nether_portal_ew")

        elif self._is("slab"):
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

        elif self._is("trapdoor"):
            if self.state["open"] == "true":
                self._addModel(self.name + "_open")
            else:
                self._addModel(self.name + "_" + self.state["half"])

        elif self._is("stairs"):
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

        elif self._is("fence") or self._is("cobblestone_wall"):
            self._addModel(self.name + "_post")
            side = self.name + "_side"
            mp = {"north" : 0, "east" : 3, "south" : 2, "west" : 1}
            for k in mp:
                if self.state[k] == "true":
                    self._addModel(side, [
                        {"type" : "rotate", "axis" : "y", "angle" : 90*mp[k]}
                    ])

        elif self._is("fence_gate"):
            x = self.name
            if self.state["in_wall"] == "true":
                x += "_wall"
            if self.state["open"] == "true":
                x += "_open"
            self._addModel(x)

        elif self.name == "iron_bars":
            self._addModel(self.name + "_post")
            side = self.name + "_side"
            mp = {"north" : 0, "east" : 3, "south" : 2, "west" : 1}
            for k in mp:
                if self.state[k] == "true":
                    self._addModel(side, [
                        {"type" : "rotate", "axis" : "y", "angle" : 90*mp[k]}
                    ])

        elif self._is("glass_pane"):
            self._addModel(self.name + "_post")
            side = self.name + "_side"
            mp = {"north" : 0, "east" : 3, "south" : 2, "west" : 1}
            for k in mp:
                if self.state[k] == "true":
                    self._addModel(side, [
                        {"type" : "rotate", "axis" : "y", "angle" : 90*mp[k]}
                    ])
        
        elif self._is("chest"):
            pass
        
        elif self._is("sign"):
            pass

        elif self.name in ["wheat", "beetroots"]:
            self._addModel(self.name + ("_stage%s" % int(self.state["age"])))

        elif self.name in ["potatoes", "carrots"]:
            age = [0, 0, 1, 1, 2, 2, 2, 3][int(self.state["age"])]
            self._addModel(self.name + ("_stage%d" % age))

        elif self.name == "nether_wart":
            age = [0, 1, 1, 2][int(self.state["age"])]
            self._addModel("nether_wart_stage%d" % age)

        elif self.name in ["melon_stem", "pumpkin_stem"]:
            age = int(self.state["age"])
            self._addModel(self.name + ("_stage%d" % age))

        elif self.name == "cake":
            bit = int(self.state["bites"])
            if bit:
                self._addModel(self.name + ("_slice%d" % bit))
            else:
                self._addModel(self.name)

        elif self.name == "hopper":
            if self.state["facing"] != "down":
                self._addModel(self.name + "_side")
            else:
                self._addModel(self.name)

        elif self.name == "farm_land":
            if int(self.state["moisture"]) == 7:
                self._addModel("farm_land_moist")
            else:
                self._addModel("farm_land")

        elif self.name == "snow":
            h = int(self.state["layers"])
            if h == 8:
                self._addModel("snow_block")
            else:
                self._addModel("snow_height%d" % (h*2))

        elif self.name == "redstone_wire":
            # TODO : d[0] = "redstone_dust_dot"
            pass
        elif self.name == "repeater":
            # TODO : d[0] += "_1tick"
            pass
        elif self.name == "tripwire":
            # TODO
            pass
        elif self.name == "fire":
            self._addModel("fire_floor0")
        
        elif self.name == "end_gateway":
            # TODO
            pass

        else:
            self._addModel(self.name)

    def _writeElement(self, fout, ele):
        from_pt = ele["from"]
        to_pt = ele["to"]
        cube = minus(to_pt, from_pt)
        mid = mult(plus(from_pt, to_pt), .5)
        
        fout.write('AttributeBegin\n')
        fout.write('Translate %f %f %f\n' % mid)
        if "rotation" in ele:
            import math
            rot = ele["rotation"]
            axis = rot["axis"]
            org = minus([.5, .5, .5], mult(rot["origin"], 1./16))
            ang = rot["angle"]
            rxyz = {"x" : (1, 0, 0), "y" : (0, 1, 0), "z" : (0, 0, 1)}
            sxyz = {"x" : (0, 1, 1), "y" : (1, 0, 1), "z" : (1, 1, 0)}
            scale = 1/math.cos(ang/180.*math.pi)
            fout.write("Translate %f %f %f\n" % mult(org, -1))
            fout.write(("Rotate %f " % ang) + ("%d %d %d\n" % rxyz[axis]))
            if "rescale" in rot and rot["rescale"]:
                fout.write("Scale %f %f %f\n" % plus(mult(sxyz[axis], scale), rxyz[axis]))
            fout.write("Translate %f %f %f\n" % org)
        
        for facename in ele["faces"]:
            face = ele["faces"][facename]
            tex = face["texture"]
            uv = face["uv"]
            delta_f, l_f, dir_, shape = pt_map[facename]
            delta = delta_f(cube)
            l1, l2 = l_f(cube)
            if "tintindex" in face:
                if self._is("leaves"):
                    tint_color = self.bdr.getFoliageColor(self.biome_id, 0) 
                else:
                    tint_color = self.bdr.getGrassColor(self.biome_id, 0) 
                fout.write(('Material "matte" "texture Kd" "%s-color"' % tex) + 
                           ('"rgb tintMap" [%f %f %f]\n' % tint_color))
            else:
                fout.write('Material "matte" "texture Kd" "%s-color"\n' % tex)
            fout.write('AttributeBegin\n')
            fout.write('  Translate %f %f %f\n' % delta)
            if ResourceManager.inst.hasAlpha(tex + ".png"):
                fout.write('  Shape "%s" "float l1" [%f] "float l2" [%f] ' % (shape, l1, l2) +
                           '  "float dir" [%d] "texture alpha" "%s-alpha"' % (dir_, tex) +
                           '  "float u0" [%f] "float v0" [%f] "float u1" [%f] "float v1" [%f]\n' % uv)
            else:
                fout.write('  Shape "%s" "float l1" [%f] "float l2" [%f] ' % (shape, l1, l2) +
                           '  "float dir" [%d] ' % (dir_, ) +
                           '  "float u0" [%f] "float v0" [%f] "float u1" [%f] "float v1" [%f]\n' % uv)
            fout.write('AttributeEnd\n')

        fout.write('AttributeEnd\n')

    def _writeRotate(self, fout, axis, ang):
        org = (.5, .5, .5)
        fout.write("Translate %f %f %f\n" % org)
        rxyz = {"x" : (1, 0, 0), "y" : (0, 1, 0), "z" : (0, 0, 1)}
        fout.write(("Rotate %f " % ang) + ("%d %d %d\n" % rxyz[axis]))
        fout.write("Translate %f %f %f\n" % mult(org, -1))

    def _writeScale(self, fout, axis, s):
        org = (.5, .5, .5)
        fout.write("Translate %f %f %f\n" % org)
        axis_v = {"x" : (1, 0, 0), "y" : (0, 1, 0), "z" : (0, 0, 1)}
        sixa_v = {"x" : (0, 1, 1), "y" : (1, 0, 1), "z" : (1, 1, 0)}
        fout.write(("Scale %f %f %f\n" % plus(mult(axis_v[axis], s), sixa_v[axis])))
        fout.write("Translate %f %f %f\n" % mult(org, -1))

    def render(self, fout):
        if not self.models:
            return 0
            
        fout.write('AttributeBegin\n')
        if "axis" in self.state and self.name != "nether_portal":
            axis = self.state["axis"]
            if axis == "x":
                self._writeRotate(fout, "z", 90)
            elif axis == "z":
                self._writeRotate(fout, "x", 90)

        if "facing" in self.state:
            facing = self.state["facing"]
            mp = {"north" : 1, "east" : 0, "south" : 3, "west" : 2}
            if facing in mp:
                self._writeRotate(fout, "y", mp[facing]*90)
            elif facing == "down":
                self._writeRotate(fout, "z", -90)
            elif facing == "top":
                self._writeRotate(fout, "z", 90)
        
        for model, transforms in self.models:
            if transforms:
                for t in transforms:
                    if t["type"] == "rotate":
                        self._writeRotate(fout, t["axis"], t["angle"])
                    elif t["type"] == "scale":
                        self._writeScale(fout, t["axis"], t["value"])
            for ele in model["elements"]:
                self._writeElement(fout, ele)
            if transforms:
                for t in transforms[::-1]:
                    if t["type"] == "rotate":
                        self._writeRotate(fout, t["axis"], -t["angle"])
                    elif t["type"] == "scale":
                        self._writeScale(fout, t["axis"], 1/t["value"])
        fout.write('AttributeEnd\n')
        return 1

    def getUsedTexture(self):
        used_texture = set()
        for model, transform in self.models:
            for ele in model["elements"]:
                for facename in ele["faces"]: 
                    face = ele["faces"][facename]
                    tex = face["texture"]
                    if tex[0] == '#':
                        raise KeyError("Texture name not resolve")
                    used_texture.add(tex)
        return used_texture
