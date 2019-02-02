from water import WaterSolver
from block import BlockSolver

class Scene:
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

    def write(self, filename):
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
        water_solver.write(fout)

        block_solver = BlockSolver(self.block)
        block_solver.write(fout, stand_pt)

        fout.write('WorldEnd\n')
