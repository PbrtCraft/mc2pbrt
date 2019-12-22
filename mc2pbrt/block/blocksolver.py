from resource import ResourceManager
from tuple_calculation import plus_i, mult_i

from pbrtwriter import PbrtWriter


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
                    self.used_texture = self.used_texture | self.block[y][z][x].getUsedTexture(
                    )

    def write(self, pbrtwriter: PbrtWriter, start_pt):
        print("Writing solid blocks...")
        for fn in self.used_texture:
            pbrtwriter.texture("%s-color" % fn, "spectrum",
                               "imagemap", "string filename", "%s.png" % fn)
            if ResourceManager().hasAlpha(fn + ".png"):
                pbrtwriter.texture("%s-alpha" % fn, "float", "imagemap",
                                   "bool alpha", "true", "string filename", "%s.png" % fn)

        import queue
        que = queue.Queue()
        rendered = set()
        deltas = [(1, 0, 0), (-1, 0, 0), (0, 1, 0),
                  (0, -1, 0), (0, 0, 1), (0, 0, -1)]
        que.put(start_pt)
        for delta in deltas:
            next_pt = plus_i(delta, start_pt)
            if not self._inBlock(next_pt):
                continue
            que.put(next_pt)

        cnt = 0
        while not que.empty():
            pt = que.get()
            if not self._inBlock(pt):
                continue
            if pt in rendered:
                continue
            rendered.add(pt)
            x, y, z = pt
            b = self.block[y][z][x]

            if not b.empty():
                pbrtwriter.translate(pt)
                cnt += b.write(pbrtwriter)
                pbrtwriter.translate(mult_i(pt, -1))

            if b.canPass():
                for delta in deltas:
                    next_pt = plus_i(delta, pt)
                    if not self._inBlock(next_pt):
                        continue
                    if next_pt in rendered:
                        continue
                    que.put(next_pt)
        print("Render", cnt, "blocks")
