from util import tqdmpos

from tuple_calculation import plus

from pbrtwriter import PbrtWriter
from liquid.liquid import LiquidSolver


class LavaSolver(LiquidSolver):
    """Write the lava in then scene."""

    def build(self):
        print("Building lava level...")
        for x, y, z in tqdmpos(range(self.X), range(self.Y), range(self.Z)):
            b = self.block[y][z][x]
            if b.name == "lava" or b.name == "flowing_lava":
                self.level[y][z][x] = int(b.state["level"])

    def write(self, pbrtwriter: PbrtWriter):
        print("Writing lava blocks...")

        with pbrtwriter.attribute():
            pbrtwriter.areaLightSource("diffuse", "blackbody L", [1400, 100])
            self._write(pbrtwriter)
