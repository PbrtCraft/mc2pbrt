import sys
from tqdm import tqdm

def eprint(msg):
    sys.stderr.write("[Error] " + msg + "\n")

plus  = lambda p,q : tuple(map(float, [p[i]+q[i] for i in range(3)]))
minus = lambda p,q : tuple(map(float, [p[i]-q[i] for i in range(3)]))
mult  = lambda p,f : tuple([float(p[i])*f for i in range(3)]) 

plus_i  = lambda p,q : tuple(map(int, [p[i]+q[i] for i in range(3)]))

pt_map = {
    "east"  : (lambda c : ( c[0]/2,  0,  0), lambda c : (c[1], c[2]),  1, "quadx"),
    "west"  : (lambda c : (-c[0]/2,  0,  0), lambda c : (c[1], c[2]), -1, "quadx"),
    "up"    : (lambda c : (  0, c[1]/2,  0), lambda c : (c[0], c[2]),  1, "quady"),
    "down"  : (lambda c : (  0,-c[1]/2,  0), lambda c : (c[0], c[2]), -1, "quady"),
    "north" : (lambda c : (  0,  0, c[2]/2), lambda c : (c[1], c[0]),  1, "quadz"),
    "south" : (lambda c : (  0,  0,-c[2]/2), lambda c : (c[1], c[0]), -1, "quadz")
}

cullface_map = {
    "east"  : (1, 0, 0),
    "west"  : (-1, 0, 0), 
    "up"    : (0, 1, 0),
    "down"  : (0, -1, 0),
    "north" : (0, 0, 1),
    "south" : (0, 0, -1),
}

class Block:
    def __init__(self, name, state, model_loader):
        self.name = name
        self.state = state
        self.ldr = model_loader
        # [(Model, Transform)]
        self.models = []
        
        self._build()

    def _is(self, y):
        return self.name == y or self.name[-len(y)-1:] == "_" + y

    def _getModel(self, name):
        model = self.ldr.getModel("block/" + name)
        if "elements" not in model :
            return None
        return model

    def _addModel(self, name, transforms = None):
        mdl = self._getModel(name)
        if not mdl:
            #eprint("Fail to load model-%s" % name)
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
                if self._is("brick_slab"):
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
            if shape == "straight":
                self._addModel(self.name)
            elif shape == "inner_left":
                self._addModel(self.name + "_inner", [
                    {"type" : "rotate", "axis" : "y", "angle" : 90}
                ])
            elif shape == "inner_right":
                self._addModel(self.name + "_inner")
            elif shape == "outer_left":
                self._addModel(self.name + "_outer", [
                    {"type" : "rotate", "axis" : "y", "angle" : 90}
                ])
            elif shape == "outer_right":
                self._addModel(self.name + "_outer")

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

        elif self.name in ["wheat", "beetroots"]:
            self._addModel(self.name + ("_stage%s" % int(self.state["age"])))

        elif self.name in ["potatoes", "carrots"]:
            age = [0, 0, 1, 1, 2, 2, 2, 3][int(self.state["age"])]
            self._addModel(self.name + ("_stage%d" % age))

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
                self._addModel(self.name + "_moist")
            else:
                self._addModel(self.name)

        elif self.name == "redstone_wire":
            # TODO : d[0] = "redstone_dust_dot"
            pass
        elif self.name == "repeater":
            # TODO : d[0] += "_1tick"
            pass
        elif self.name == "tripwire":
            # TODO
            pass
        else:
            self._addModel(self.name)

    def _writeRotate2(self, fout, axis, ang):
        org = (.5, .5, .5)
        fout.write("Translate %f %f %f\n" % org)
        rxyz = {"x" : (1, 0, 0), "y" : (0, 1, 0), "z" : (0, 0, 1)}
        fout.write(("Rotate %f " % ang) + ("%d %d %d\n" % rxyz[axis]))
        fout.write("Translate %f %f %f\n" % mult(org, -1))

    def _writeRotate(self, fout, rot):
        import math
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

    def _writeElement(self, fout, ele):
        from_pt = ele["from"]
        to_pt = ele["to"]
        cube = minus(to_pt, from_pt)
        mid = mult(plus(from_pt, to_pt), .5)
        
        fout.write('AttributeBegin\n')
        fout.write('Translate %f %f %f\n' % mid)
        if "rotation" in ele:
            self._writeRotate(fout, ele["rotation"])
        
        for facename in ele["faces"]:
            face = ele["faces"][facename]
            tex = face["texture"]
            uv = face["uv"]
            delta_f, l_f, dir_, shape = pt_map[facename]
            delta = delta_f(cube)
            l1, l2 = l_f(cube)
            if "tintindex" in face:
                fout.write('Material "matte" "texture Kd" "%s-color" "rgb I" [.2 .7 .0]\n' % tex)
            else:
                fout.write('Material "matte" "texture Kd" "%s-color"\n' % tex)
            fout.write('AttributeBegin\n')
            fout.write('  Translate %f %f %f\n' % delta)
            fout.write('  Shape "%s" "float l1" [%f] "float l2" [%f] ' % (shape, l1, l2) + 
                       '  "float dir" [%d] "texture alpha" "%s-alpha"' % (dir_, tex) +
                       '  "float u0" [%f] "float v0" [%f] "float u1" [%f] "float v1" [%f]\n' % uv)
            fout.write('AttributeEnd\n')

        fout.write('AttributeEnd\n')

    def render(self, fout):
        if not self.models : return
            
        fout.write('AttributeBegin\n')
        if "axis" in self.state and self.name != "nether_portal":
            axis = self.state["axis"]
            if axis == "x":
                self._writeRotate2(fout, "z", 90)
            elif axis == "z":
                self._writeRotate2(fout, "x", 90)

        if "facing" in self.state:
            facing = self.state["facing"]
            mp = {"north" : 1, "east" : 0, "south" : 3, "west" : 2}
            if facing in mp:
                self._writeRotate2(fout, "y", mp[facing]*90)
            elif facing == "down":
                self._writeRotate2(fout, "z", -90)
            elif facing == "top":
                self._writeRotate2(fout, "z", 90)
        
        for model, transforms in self.models:
            if transforms:
                for t in transforms:
                    if t["type"] == "rotate":
                        self._writeRotate2(fout, t["axis"], t["angle"])
            for ele in model["elements"]:
                self._writeElement(fout, ele)
            if transforms:
                for t in transforms[::-1]:
                    if t["type"] == "rotate":
                        self._writeRotate2(fout, t["axis"], -t["angle"])
        fout.write('AttributeEnd\n')

    def getUsedTexture(self):
        used_texture = set()
        for model, transform in self.models:
            for ele in model["elements"]:
                for facename in ele["faces"]: 
                    face = ele["faces"][facename]
                    tex = face["texture"]
                    if tex[0] == '#':
                        eprint("Cannot resolve texture.")
                        exit(1)
                    used_texture.add(tex)
        return used_texture


class WaterSolver:
    def __init__(self, block):
        self.block = block
        self.Y = len(self.block)
        self.Z = len(self.block[0])
        self.X = len(self.block[0][0])
        self.level = [[[None]*self.X for i in range(self.Z)] for j in range(self.Y)]

        self._build()

        self.eps = 0.05

    def _build(self):
        print("Building water level...")
        for x,y,z in tqdm([(x, y, z) for x in range(self.X) for y in range(self.Y) for z in range(self.Z)]):
            b = self.block[y][z][x]
            if b.name == "water" or b.name == "flowing_water":
                self.level[y][z][x] = int(b.state["level"])
            elif "waterlogged" in b.state:
                if b.state["waterlogged"] == "true":
                    self.level[y][z][x] = 0
    
    def _level2height(self, l):
        if l >= 8: return 1.
        if l == 0: return 1. - self.eps
        return (1-self.eps)*(8-l)/7.

    def getLevel(self, pt):
        x, y, z = pt
        if x < 0 or x >= self.X : return None
        if y < 0 or y >= self.Y : return None
        if z < 0 or z >= self.Z : return None
        return self.level[y][z][x]

    def render(self, fout):
        print("Writing water blocks...")
        for x,y,z in tqdm([(x, y, z) for x in range(self.X) for y in range(self.Y) for z in range(self.Z)]):
            if self.level[y][z][x] == None: continue
            pt = (x, y, z)
            h = self._level2height(self.level[y][z][x])
            fout.write('AttributeBegin\n')
            fout.write('Translate %f %f %f\n' % plus(pt, (.5, h/2, .5)))
            cube = (1, h/2, 1)
            for facename in pt_map:
                cull_pt = plus_i(cullface_map[facename], pt)
                if self.getLevel(cull_pt) != None:
                    print("Culling face..")
                    continue
                delta_f, l_f, dir_, shape = pt_map[facename]
                delta = delta_f(cube)
                l1, l2 = l_f(cube)
                fout.write('Material "glass"\n')
                fout.write('AttributeBegin\n')
                fout.write('  Translate %f %f %f\n' % delta)
                fout.write('  Shape "%s" "float l1" [%f] "float l2" [%f] ' % (shape, l1, l2) + 
                           '  "float dir" [%d]' % dir_)
                fout.write('AttributeEnd\n')
            fout.write('AttributeEnd\n')


class PbrtWriter:
    def __init__(self, model_loader):
        self.mldr = model_loader
        
        self.camera_cmd = None
        self.lookat_vec = None
        self.samples = 16
        self.method = ("photonmap", "")

    def readFile(self, filename):
        f = open(filename, "r")
        self.block = json.load(f)

    def setBlocks(self, block):
        self.block = block

    def _preloadUsedData(self):
        self.used_texture = set()
        self.Y = len(self.block)
        self.Z = len(self.block[0])
        self.X = len(self.block[0][0])
        for x in range(self.X):
            for y in range(self.Y):
                for z in range(self.Z):
                    d = self.block[y][z][x]
                    self.block[y][z][x] = Block(d[0], d[1], self.mldr)
                    self.used_texture = self.used_texture | self.block[y][z][x].getUsedTexture()

    def _writeLight(self, fout, pt):
        fout.write('AttributeBegin\n')
        fout.write('    Rotate 270 1 0 0 \n')
        fout.write('    LightSource "infinite" "integer nsamples" [4] "rgb L" [1 1 1]' + 
                       '"string mapname" ["env/aristea_wreck_1k.png"]\n')
        fout.write('AttributeEnd\n')

    def _writeWater(self, fout, block_data, pt):
        fout.write('AttributeBegin\n')
        fout.write('Translate %f %f %f\n' % plus(pt, (.5, .45, .5)))
        cube = (1, .45, 1)
        for facename in pt_map:
            delta_f, l_f, dir_, shape = pt_map[facename]
            delta = delta_f(cube)
            l1, l2 = l_f(cube)
            fout.write('Material "glass"\n')
            fout.write('AttributeBegin\n')
            fout.write('  Translate %f %f %f\n' % delta)
            fout.write('  Shape "%s" "float l1" [%f] "float l2" [%f] ' % (shape, l1, l2) + 
                       '  "float dir" [%d]' % dir_)
            fout.write('AttributeEnd\n')

        fout.write('AttributeEnd\n')

    def writeFile(self, filename):
        print("Start write file ...")
        self._preloadUsedData()
        fout = open(filename, "w")

        fout.write('Film "image"\n')
        if not self.lookat_vec:
            fout.write('LookAt %f %f %f  %f %f 0  0 1 0\n' % (self.X/2, 4, self.Z/2+1, self.X/2, 4))
        else:
            fout.write('LookAt %f %f %f  %f %f %f %f %f %f\n' % self.lookat_vec) 

        if not self.camera_cmd:
            fout.write('Camera "environment"\n')
        else:
            fout.write(self.camera_cmd + "\n")

        fout.write('SurfaceIntegrator "%s" %s\n' % self.method)
        fout.write('Sampler "bestcandidate" "integer pixelsamples" [%d]\n' % self.samples)

        fout.write('WorldBegin\n')

        for fn in self.used_texture:
            fout.write('Texture "%s-color" "spectrum" "imagemap" "string filename" "%s.png"\n' % (fn, fn))
            fout.write('Texture "%s-alpha" "float" "alphamap" "string filename" "%s.png"\n' % (fn, fn))

        self._writeLight(fout, (self.X/2, self.Y/2 + 10, self.Z/2))
        
        water_solver = WaterSolver(self.block)
        water_solver.render(fout)
        
        print("Writing lights...")
        for x,y,z in tqdm([(x, y, z) for x in range(self.X) for y in range(self.Y) for z in range(self.Z)]):
            pt = (x, y, z)
            name = self.block[y][z][x].name
            if name == "torch" or name == "jack_o_lantern":
                fout.write("AttributeBegin\n")
                fout.write('AreaLightSource "diffuse" "rgb L" [ .5 .5 .5 ]\n')
                fout.write('Translate %f %f %f\n' % pt)
                self.block[y][z][x].render(fout)
                fout.write("AttributeEnd\n")

        print("Writing blocks...")
        for x,y,z in tqdm([(x, y, z) for x in range(self.X) for y in range(self.Y) for z in range(self.Z)]):
            pt = (x, y, z)
            fout.write('Translate %f %f %f\n' % pt)
            self.block[y][z][x].render(fout)
            fout.write('Translate %f %f %f\n' % mult(pt, -1))

        fout.write('WorldEnd\n')
