from block import BlockSolver
from water import WaterSolver
from lava import LavaSolver


class Scene:
    def __init__(self, block):
        self.block = block

        self.lookat_vec = None

        self.camera = None
        self.method = None
        self.samples = 16

        self.phenomenons = []

    def write(self, filename):
        print("Start write file ...")
        fout = open(filename, "w")

        # The coordinate system of minecraft and pbrt is different.
        # Pbrt is lefthand base, while minecraft is righthand base.
        fout.write("Scale -1 1 1\n")

        fout.write(
            'Film "image" "integer xresolution" [960] "integer yresolution" [480]\n')

        fout.write('LookAt %f %f %f  %f %f %f %f %f %f\n' % self.lookat_vec)
        stand_pt = tuple(map(int, self.lookat_vec[:3]))

        self.camera.write(fout)
        self.method.write(fout)

        fout.write(
            'Sampler "lowdiscrepancy" "integer pixelsamples" [%d]\n' % self.samples)

        fout.write('WorldBegin\n')

        for phenomenon in self.phenomenons:
            phenomenon.write(fout)

        block_solver = BlockSolver(self.block)
        block_solver.write(fout, stand_pt)

        water_solver = WaterSolver(self.block)
        water_solver.write(fout)

        lava_solver = LavaSolver(self.block)
        lava_solver.write(fout)

        fout.write('WorldEnd\n')
