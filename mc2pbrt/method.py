import typing

from pbrtwriter import PbrtWriter


def create(name, params):
    type_map = {
        "PathTracing": PathTracing,
        "path": PathTracing,
        "BidirectionalPathTracing": BidirectionalPathTracing,
        "bdpt": BidirectionalPathTracing,
        "MetropolisLightTransport": MetropolisLightTransport,
        "mlt": MetropolisLightTransport,
        "StochasticProgressivePhotonMapping": StochasticProgressivePhotonMapping,
        "sppm": StochasticProgressivePhotonMapping,
    }
    if name in type_map:
        return type_map[name](**params)
    else:
        raise KeyError("Method name not found")


class PathTracing:
    def __init__(self, maxdepth: int = 5):
        self.maxdepth = maxdepth

    def write(self, pbrtwriter: PbrtWriter):
        pbrtwriter.integrator("path", "integer maxdepth", [self.maxdepth])


class BidirectionalPathTracing:
    def __init__(self, maxdepth: int = 5):
        self.maxdepth = maxdepth

    def write(self, pbrtwriter: PbrtWriter):
        pbrtwriter.integrator("bdpt", "integer maxdepth", [self.maxdepth])


class MetropolisLightTransport:
    def __init__(self, maxdepth: int = 5):
        self.maxdepth = maxdepth

    def write(self, pbrtwriter: PbrtWriter):
        pbrtwriter.integrator("mlt", "integer maxdepth", [self.maxdepth])


class StochasticProgressivePhotonMapping:
    def __init__(self, maxdepth: int = 5):
        self.maxdepth = maxdepth

    def write(self, pbrtwriter: PbrtWriter):
        pbrtwriter.integrator("sppm", "integer maxdepth", [self.maxdepth])
