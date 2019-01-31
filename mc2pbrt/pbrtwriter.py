from tqdm import tqdm

from block import Block
from resource import ResourceManager

from tuple_calculation import plus_i, plus, mult

class WaterSolver:
    """Write the water in then scene."""

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
        for x, y, z in tqdm([(x, y, z) for x in range(self.X) for y in range(self.Y) for z in range(self.Z)],
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
        if x < 0 or x >= self.X: return None
        if y < 0 or y >= self.Y: return None
        if z < 0 or z >= self.Z: return None
        return self.level[y][z][x]

    def getHeight(self, pt):
        l = self.getLevel(pt)
        if l == None: return None
        return self._level2height(l)

    def calAvg(self, xs):
        cnt = 0
        sum_xs = 0
        for x in xs:
            cnt += 1
            sum_xs += x or 0
        return sum_xs/cnt

    def render(self, fout):
        print("Writing water blocks...")
        fout.write('Material "glass" "float eta" [1.33] "rgb Kt" [.28 .72 1]\n')
        for x, y, z in tqdm([(x, y, z) for x in range(self.X) for y in range(self.Y) for z in range(self.Z)],
                            ascii=True):
            if self.level[y][z][x] == None: continue
            pt = (x, y, z)
            h = self._level2height(self.level[y][z][x])
            fout.write('AttributeBegin\n')
            fout.write('Translate %f %f %f\n' % plus(pt, (.5, 0, .5)))
            #cube = (1, h/2, 1)

            if self.getLevel((x, y+1, z)) != None:
                # When a water block is on current block, the water should be full.
                ps = [1]*9
            else:
                dt = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]
                hs = [None]*9
                for i in range(9):
                    hs[i] = self.getHeight((x+dt[i][1], y, z+dt[i][0]))

                ps = [[0, 1, 3, 4], [1, 4], [1, 2, 4, 5],
                      [3, 4], [4], [4, 5],
                      [3, 4, 6, 7], [4, 7], [4, 5, 7, 8]]

                ps = [self.calAvg(map(lambda x: hs[x], p)) for p in ps]

            if self.getLevel((x, y+1, z)) is None:
                from math import pi
                fout.write('AttributeBegin\n')
                fout.write('  Translate -.5 0 -.5\n')
                fout.write('  Shape "heightfield" "integer nv" [3] "integer nu" [3]\n' +
                           '  "float Py" [%f %f %f %f %f %f %f %f %f]' % tuple(ps))
                fout.write('AttributeEnd\n')

            if self.getLevel((x, y-1, z)) is None:
                fout.write('Shape "quady"\n')

            def param(pts):
                flat_pts = []
                for pt in pts:
                    flat_pts += list(pt)
                return "[" + " ".join(map(str, flat_pts)) + "]"

            def trimesh(mv, pts, inds):
                fout.write('AttributeBegin\n')
                fout.write('  Translate %f %f %f\n' % mv)
                fout.write('  Shape "trianglemesh" "point P" %s ' % param(pts) +
                           '  "integer indices" %s' % param(inds))
                fout.write('AttributeEnd\n')

            def rev(inds):
                ret = list(inds)
                for i in range(len(ret)):
                    tri = ret[i]
                    ret[i] = (tri[0], tri[2], tri[1])
                return ret

            indx = [(0, 1, 2), (1, 3, 2), (2, 3, 4), (3, 5, 4)]
            if self.getLevel((x-1, y, z)) is None:
                pts = [
                    (0, 0, -.5), (0, ps[0], -.5),
                    (0, 0, 0), (0, ps[3], 0),
                    (0, 0, .5), (0, ps[6], .5),
                ]
                trimesh((-.5, 0, 0), pts, rev(indx))

            if self.getLevel((x+1, y, z)) is None:
                pts = [
                    (0, 0, -.5), (0, ps[2], -.5),
                    (0, 0, 0), (0, ps[5], 0),
                    (0, 0, .5), (0, ps[8], .5),
                ]
                trimesh((.5, 0, 0), pts, indx)

            if self.getLevel((x, y, z-1)) is None:
                pts = [
                    (-.5, 0, 0), (-.5, ps[0], 0),
                    (0, 0, 0), (0, ps[1], 0),
                    (.5, 0, 0), (.5, ps[2], 0),
                ]
                trimesh((0, 0, -.5), pts, indx)

            if self.getLevel((x, y, z+1)) is None:
                pts = [
                    (-.5, 0, 0), (-.5, ps[6], 0),
                    (0, 0, 0), (0, ps[7], 0),
                    (.5, 0, 0), (.5, ps[8], 0),
                ]
                trimesh((0, 0, .5), pts, rev(indx))

            fout.write('AttributeEnd\n')


class BlockSolver:
    """Write all solid block in th scene"""

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

            fout.write('Translate %f %f %f\n' % pt)
            cnt += b.render(fout)
            fout.write('Translate %f %f %f\n' % mult(pt, -1))

            if b.canPass():
                for delta in deltas:
                    que.put(plus_i(delta, pt))
        print("Render", cnt, "blocks")


class PbrtWriter:
    def __init__(self, biome_reader):
        self.bdr = biome_reader

        self.camera_cmd = None
        self.lookat_vec = None
        self.samples = 16
        self.method = ("sppm", "")

        self.envlight = None
        self.used_texture = set()

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
                    self.block[y][z][x] = Block(d[0], d[1], d[2], self.bdr)
                    self.used_texture = self.used_texture | self.block[y][z][x].getUsedTexture()

    def _writeEnvLight(self, fout):
        if not self.envlight: return
        fout.write('AttributeBegin\n')
        fout.write('    Rotate 270 1 0 0 \n')
        fout.write('    LightSource "infinite" "integer nsamples" [16] "rgb L" [1 1 1]' +
                   '"string mapname" ["%s"]\n' % self.envlight)
        fout.write('AttributeEnd\n')

    def writeFile(self, filename):
        print("Start write file ...")
        self._preloadUsedData()
        fout = open(filename, "w")

        # The coordinate system of minecraft and pbrt is different.
        # Pbrt is lefthand base, while minecraft is righthand base.
        fout.write("Scale -1 1 1\n")

        fout.write('Film "image" "integer xresolution" [960] "integer yresolution" [480]\n')

        lookat_vec = self.lookat_vec or (self.X/2, 4, self.Z/2+1, self.X/2, 4, 0, 0, 1, 0)
        fout.write('LookAt %f %f %f  %f %f %f %f %f %f\n' % lookat_vec)
        stand_pt = tuple(map(int, lookat_vec[:3]))

        camera_cmd = self.camera_cmd or 'Camera "environment"'
        fout.write(camera_cmd + "\n")

        fout.write('Integrator "%s" %s\n' % self.method)
        fout.write('Sampler "lowdiscrepancy" "integer pixelsamples" [%d]\n' % self.samples)

        fout.write('WorldBegin\n')

        for fn in self.used_texture:
            fout.write('Texture "%s-color" "spectrum" "imagemap" "string filename" "%s.png"\n' % (fn, fn))
            if ResourceManager().hasAlpha(fn + ".png"):
                fout.write('Texture "%s-alpha" "float" "imagemap" "bool alpha" "true" "string filename" "%s.png"\n' % (fn, fn))

        self._writeEnvLight(fout)

        water_solver = WaterSolver(self.block)
        water_solver.render(fout)

        block_solver = BlockSolver(self.block)
        block_solver.render(fout, stand_pt)

        fout.write('WorldEnd\n')
