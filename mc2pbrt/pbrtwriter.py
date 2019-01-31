from tqdm import tqdm

from block import Block
from resource import ResourceManager
from water import WaterSolver

from tuple_calculation import plus_i, plus, mult

class BlockSolver:
    """Write all solid block in the scene"""

    def __init__(self, block):
        self.block = block
        self.Y = len(self.block)
        self.Z = len(self.block[0])
        self.X = len(self.block[0][0])
        self.used_texture = set()
        self._preloadUsedTexture()

    def _inBlock(self, pt):
        x, y, z = pt
        return x >= 0 and x < self.X and y >= 0 and y < self.Y and z >= 0 and z < self.Z

    def _preloadUsedTexture(self):
        print("Preloading used texture...")
        self.used_texture = set()
        for x in range(self.X):
            for y in range(self.Y):
                for z in range(self.Z):
                    self.used_texture = self.used_texture | self.block[y][z][x].getUsedTexture()

    def render(self, fout, start_pt):
        print("Writing solid blocks...")
        for fn in self.used_texture:
            fout.write('Texture "%s-color" "spectrum" "imagemap" "string filename" "%s.png"\n' % (fn, fn))
            if ResourceManager().hasAlpha(fn + ".png"):
                fout.write('Texture "%s-alpha" "float" "imagemap" "bool alpha" "true" "string filename" "%s.png"\n' % (fn, fn))

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
    def __init__(self):
        self.camera_cmd = None
        self.lookat_vec = None
        self.samples = 16
        self.method = ("sppm", "")

        self.envlight = None

    def setBlocks(self, block):
        self.block = block

    def _writeEnvLight(self, fout):
        if not self.envlight: return
        fout.write('AttributeBegin\n')
        fout.write('    Rotate 270 1 0 0 \n')
        fout.write('    LightSource "infinite" "integer nsamples" [16] "rgb L" [1 1 1]' +
                   '"string mapname" ["%s"]\n' % self.envlight)
        fout.write('AttributeEnd\n')

    def writeFile(self, filename):
        print("Start write file ...")
        fout = open(filename, "w")

        # The coordinate system of minecraft and pbrt is different.
        # Pbrt is lefthand base, while minecraft is righthand base.
        fout.write("Scale -1 1 1\n")

        fout.write('Film "image" "integer xresolution" [960] "integer yresolution" [480]\n')

        fout.write('LookAt %f %f %f  %f %f %f %f %f %f\n' % self.lookat_vec)
        stand_pt = tuple(map(int, self.lookat_vec[:3]))

        camera_cmd = self.camera_cmd or 'Camera "environment"'
        fout.write(camera_cmd + "\n")

        fout.write('Integrator "%s" %s\n' % self.method)
        fout.write('Sampler "lowdiscrepancy" "integer pixelsamples" [%d]\n' % self.samples)

        fout.write('WorldBegin\n')

        self._writeEnvLight(fout)

        water_solver = WaterSolver(self.block)
        water_solver.render(fout)

        block_solver = BlockSolver(self.block)
        block_solver.render(fout, stand_pt)

        fout.write('WorldEnd\n')
