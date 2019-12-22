import os
import typing

from resource import ResourceManager
from pbrtwriter import PbrtWriter


def create(name, params):
    type_map = {
        "Fog": Fog,
        "EnvironmentMap": EnvironmentMap,
        "Rayleigh": Rayleigh,
        "Sun": Sun,
        "Rain": Rain,
    }
    if name in type_map:
        return type_map[name](**params)
    else:
        raise KeyError("Phenomenon name not found")


class EnvironmentMap:
    def __init__(self, filename: str):
        self.filename = filename
        if not ResourceManager().isFile(filename):
            print("[Warning] EnvirnmentMap: %s file does not exist" % filename)

    def write(self, pbrtwriter: PbrtWriter):
        with pbrtwriter.attribute():
            pbrtwriter.rotate(270, [1, 0, 0])
            pbrtwriter.lightSource("infinite", "integer nsamples", [16],
                                   "rgb L", [1, 1, 1], "string mapname", [self.filename])


class Fog:
    def __init__(self, I_s: float, I_a: float):
        self.I_s = I_s
        self.I_a = I_a

    def write(self, pbrtwriter: PbrtWriter):
        I_s = tuple([self.I_s]*3)
        I_a = tuple([self.I_a]*3)
        pbrtwriter.makeNamedMedium(
            "Fog", "string type", "homogeneous", "rgb sigma_s", I_s, "rgb sigma_a", I_a)
        pbrtwriter.mediumInterface("", "Fog")


class Rayleigh:
    """
        Sky's Rayleigh scattering
        Take 680, 550, 440 nm light as RGB
        From **Physically Based Sky, Atmosphere and Cloud Rendering in Frostbite**
    """

    def __init__(self):
        from math import e
        self.I_s = (5.8*e**(-6), 1.35*e**(-5), 3.31*e**(-5))

    def write(self, pbrtwriter: PbrtWriter):
        pbrtwriter.makeNamedMedium(
            "Rayleigh", "string type", "homogeneous", "rgb sigma_s", self.I_s, "rgb sigma_a", [0, 0, 0])
        pbrtwriter.mediumInterface("", "Rayleigh")


class Sun:
    def __init__(self, hour: int, scene_radius: int):
        if hour < 6 or hour > 18:
            raise ValueError("Hour should be in the range of [6, 18]")

        from math import cos, sin, pi
        theta = (hour - 12)/12*pi
        dist = scene_radius*3
        mid = scene_radius
        self.position = (mid + dist*sin(theta), dist*cos(theta), mid)

        # Empirical formula
        self.scale = 50./(80**2)*(dist**2)

    def write(self, pbrtwriter: PbrtWriter):
        pbrtwriter.lightSource("distant", "point from",
                               self.position, "blackbody L", [6500, self.scale])


class Rain:
    def __init__(self, rainfall: int, scene_radius: int):
        self.size = scene_radius*2 + 1
        self.rainfall = rainfall

    def write(self, pbrtwriter: PbrtWriter):
        from random import uniform, randint
        from tqdm import tqdm
        from util import tqdmpos

        def uni01(x): return uniform(0, 1)

        print("Preparing rain instance...")
        with pbrtwriter.attribute():
            pbrtwriter.material("glass", "float eta", [
                                1.33], "rgb Kt", [.28, .72, 1])

            for i in tqdm(range(100), ascii=True):
                with pbrtwriter.objectb("RainStreak%02d" % i):
                    for dummy_1 in range(100*self.rainfall):
                        with pbrtwriter.attribute():
                            x, y, z = map(uni01, [None]*3)
                            l = uniform(0, 0.1)
                            pbrtwriter.translate((x, y, z))
                            pbrtwriter.shape("cylinder", "float radius", [
                                             0.001], "float zmin", [-l/2], "float zmax", [l/2])

            # Pbrt cylinder is z-base.
            pbrtwriter.concatTransform([1, 0, 0, 0,
                                        0, 0, 1, 0,
                                        0, 1, 0, 0,
                                        0, 0, 0, 1])
            sz = self.size
            print("Writing rain streaks...")
            for x, y, z in tqdmpos(range(sz), range(sz), range(256)):
                ind = randint(0, 99)
                with pbrtwriter.attribute():
                    pbrtwriter.translate((x, y, z))
                    pbrtwriter.objectInstance("RainStreak%02d" % ind)
