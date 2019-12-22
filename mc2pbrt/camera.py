import typing

from pbrtwriter import PbrtWriter


def create(name, params):
    type_map = {
        "Perspective": Perspective,
        "Environment": Environment,
        "Realistic": Realistic,
        "Orthographic": Orthographic,
    }
    if name in type_map:
        return type_map[name](**params)
    else:
        raise KeyError("Camera name not found")


class Perspective:
    def __init__(self, fov: int = 70):
        self.fov = fov

    def write(self, pbrtwriter: PbrtWriter):
        pbrtwriter.camera("perspective", "float fov", [self.fov])


class Environment:
    def __init__(self):
        pass

    def write(self, pbrtwriter: PbrtWriter):
        pbrtwriter.camera("environment")


class Orthographic:
    def __init__(self):
        pass

    def write(self, pbrtwriter: PbrtWriter):
        pbrtwriter.camera("orthographic")


class Realistic:
    def __init__(self):
        pass

    def write(self, pbrtwriter: PbrtWriter):
        pbrtwriter.camera("realistic")
