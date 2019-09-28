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
        raise KeyError("Phenomenon name not found")


class PathTracing:
    def __init__(self, maxdepth: int = 5):
        self.maxdepth = maxdepth

    def write(self, fout):
        fout.write(
            'Integrator "path" "integer maxdepth" [%d]\n' % self.maxdepth)


class BidirectionalPathTracing:
    def __init__(self, maxdepth: int = 5):
        self.maxdepth = maxdepth

    def write(self, fout):
        fout.write(
            'Integrator "bdpt" "integer maxdepth" [%d]\n' % self.maxdepth)


class MetropolisLightTransport:
    def __init__(self, maxdepth: int = 5):
        self.maxdepth = maxdepth

    def write(self, fout):
        fout.write(
            'Integrator "mlt" "integer maxdepth" [%d]\n' % self.maxdepth)


class StochasticProgressivePhotonMapping:
    def __init__(self, maxdepth: int = 5):
        self.maxdepth = maxdepth

    def write(self, fout):
        fout.write(
            'Integrator "sppm" "integer maxdepth" [%d]\n' % self.maxdepth)
