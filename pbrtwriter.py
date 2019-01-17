import sys
from tqdm import tqdm

from block import Block
from util import *

from resource import ResourceManager

class WaterSolver:
    def __init__(self, block):
        self.block = block
        self.Y = len(self.block)
        self.Z = len(self.block[0])
        self.X = len(self.block[0][0])
        self.level = [[[None]*self.X for i in range(self.Z)] for j in range(self.Y)]

        self._build()

        # Full water block is lower than normal block
        self.eps = 0.05

    def _build(self):
        print("Building water level...")
        for x,y,z in tqdm([(x, y, z) for x in range(self.X) for y in range(self.Y) for z in range(self.Z)],
                          ascii=True):
            b = self.block[y][z][x]
            if b.name == "water" or b.name == "flowing_water":
                self.level[y][z][x] = int(b.state["level"])
            elif "waterlogged" in b.state:
                if b.state["waterlogged"] == "true":
                    self.level[y][z][x] = 0
            elif b._is("seagrass") or b.name == "kelp_plant":
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
        fout.write('Material "glass"\n')
        for x,y,z in tqdm([(x, y, z) for x in range(self.X) for y in range(self.Y) for z in range(self.Z)],
                          ascii=True):
            if self.level[y][z][x] == None: continue
            pt = (x, y, z)
            h = self._level2height(self.level[y][z][x])
            fout.write('AttributeBegin\n')
            fout.write('Translate %f %f %f\n' % plus(pt, (.5, h/2, .5)))
            cube = (1, h/2, 1)
            for facename in pt_map:
                cull_pt = plus_i(cullface_map[facename], pt)
                if self.getLevel(cull_pt) != None:
                    continue
                delta_f, l_f, dir_, shape = pt_map[facename]
                delta = delta_f(cube)
                l1, l2 = l_f(cube)
                fout.write('AttributeBegin\n')
                fout.write('  Translate %f %f %f\n' % delta)
                fout.write('  Shape "%s" "float l1" [%f] "float l2" [%f] ' % (shape, l1, l2) + 
                           '  "float dir" [%d]' % dir_)
                fout.write('AttributeEnd\n')
            fout.write('AttributeEnd\n')


class LightSolver:
    def __init__(self, block):
        self.block = block
        self.Y = len(self.block)
        self.Z = len(self.block[0])
        self.X = len(self.block[0][0])

    def render(self, fout):
        print("Writing lights...")
        for x,y,z in tqdm([(x, y, z) for x in range(self.X) for y in range(self.Y) for z in range(self.Z)],
                          ascii=True):
            pt = (x, y, z)
            b = self.block[y][z][x]
            if b.isLight():
                fout.write("AttributeBegin\n")
                fout.write('AreaLightSource "diffuse" "rgb L" [ .5 .5 .5 ]\n')
                fout.write('Translate %f %f %f\n' % pt)
                self.block[y][z][x].render(fout)
                fout.write("AttributeEnd\n")


class BlockSolver:
    def __init__(self, block):
        self.block = block
        self.Y = len(self.block)
        self.Z = len(self.block[0])
        self.X = len(self.block[0][0])

    def _inBlock(self, pt):
        x, y, z = pt
        return x >= 0 and x < self.X and y >= 0 and y < self.Y and z >= 0 and z < self.Z

    def render(self, fout, start_pt):
        print("Writing solid blocks...")
        import queue
        que = queue.Queue()
        rendered = set()
        deltas = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
        que.put(start_pt)
        for delta in deltas:
            que.put(plus_i(delta, start_pt))

        cnt = 0
        while not que.empty():
            pt = que.get()
            if not self._inBlock(pt): continue
            if pt in rendered: continue
            rendered.add(pt)
            x, y, z = pt
            b = self.block[y][z][x]

            # shouldn't render light as a block
            # light solver should deal with it
            if not b.isLight():
                fout.write('Translate %f %f %f\n' % pt)
                cnt += b.render(fout)
                fout.write('Translate %f %f %f\n' % mult(pt, -1))
            if b.canPass():
                for delta in deltas:
                    que.put(plus_i(delta, pt))
        print("Render", cnt, "blocks")


class PbrtWriter:
    def __init__(self, model_loader, biome_reader):
        self.mldr = model_loader
        self.bdr = biome_reader
        
        self.camera_cmd = None
        self.lookat_vec = None
        self.samples = 16
        self.method = ("photonmap", "")

        self.envlight = None 

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
                    self.block[y][z][x] = Block(d[0], d[1], d[2], self.mldr, self.bdr)
                    self.used_texture = self.used_texture | self.block[y][z][x].getUsedTexture()

    def _writeEnvLight(self, fout):
        if not self.envlight : return
        fout.write('AttributeBegin\n')
        fout.write('    Rotate 270 1 0 0 \n')
        fout.write('    LightSource "infinite" "integer nsamples" [4] "rgb L" [1 1 1]' + 
                       '"string mapname" ["%s"]\n' % self.envlight)
        fout.write('AttributeEnd\n')

    def writeFile(self, filename):
        print("Start write file ...")
        self._preloadUsedData()
        fout = open(filename, "w")
        fout.write("Scale -1 1 1\n")

        fout.write('Film "image" "integer xresolution" [960] "integer yresolution" [480]\n')

        lookat_vec = self.lookat_vec or (self.X/2, 4, self.Z/2+1, self.X/2, 4, 0, 0, 1, 0)
        fout.write('LookAt %f %f %f  %f %f %f %f %f %f\n' % self.lookat_vec) 
        stand_pt = tuple(map(int, self.lookat_vec[:3]))

        camera_cmd = self.camera_cmd or 'Camera "environment"'
        fout.write(camera_cmd + "\n")

        fout.write('SurfaceIntegrator "%s" %s\n' % self.method)
        fout.write('Sampler "bestcandidate" "integer pixelsamples" [%d]\n' % self.samples)

        fout.write('WorldBegin\n')

        for fn in self.used_texture:
            fout.write('Texture "%s-color" "spectrum" "imagemap" "string filename" "%s.png"\n' % (fn, fn))
            if ResourceManager.inst.hasAlpha(fn + ".png"):
                fout.write('Texture "%s-alpha" "float" "alphamap" "string filename" "%s.png"\n' % (fn, fn))

        self._writeEnvLight(fout)
        
        water_solver = WaterSolver(self.block)
        water_solver.render(fout)

        light_solver = LightSolver(self.block)
        light_solver.render(fout)

        block_solver = BlockSolver(self.block)
        block_solver.render(fout, stand_pt)

        fout.write('WorldEnd\n')
