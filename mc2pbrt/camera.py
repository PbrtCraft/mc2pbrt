def create(name, params):
    type_map = {
        "Perspective": CameraPerspective,
        "Envirnment": CameraEnvirnment,
        "Realistic": CameraRealistic,
    }
    if name in type_map:
        return type_map[name](**params)
    else:
        raise KeyError("Camera name not found")


class CameraPerspective:
    def __init__(self, fov=70):
        self.fov = fov

    def write(self, fout):
        fout.write('Camera "perspective" "float fov" [%f]\n' % self.fov)


class CameraEnvirnment:
    def __init__(self):
        pass

    def write(self, fout):
        fout.write('Camera "environment"\n')


class CameraRealistic:
    def __init__(self):
        raise NotImplementedError("Realistic Camera")
