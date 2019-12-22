from util import tqdmpos

from tuple_calculation import plus

from pbrtwriter import PbrtWriter
from liquid.liquid import LiquidSolver


class WaterSolver(LiquidSolver):
    """Write the water in then scene."""

    def build(self):
        print("Building water level...")
        for x, y, z in tqdmpos(range(self.X), range(self.Y), range(self.Z)):
            b = self.block[y][z][x]
            if b.name == "water" or b.name == "flowing_water":
                self.level[y][z][x] = int(b.state["level"])
            elif "waterlogged" in b.state:
                if b.state["waterlogged"] == "true":
                    self.level[y][z][x] = 0
            elif b._is("seagrass") or b.name == "kelp_plant":
                self.level[y][z][x] = 0

    def write(self, pbrtwriter: PbrtWriter):
        print("Writing water blocks...")

        pbrtwriter.material("glass", "float eta", [
                            1.33], "rgb Kt", [.28, .72, 1])
        self._write(pbrtwriter)
