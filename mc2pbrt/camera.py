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
