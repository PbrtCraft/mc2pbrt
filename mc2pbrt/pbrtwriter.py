import sys
import typing


class PbrtBlock:
    def __init__(self, fout, name, suffix=""):
        self.fout = fout
        self.name = name
        self.suffix = suffix

    def __enter__(self):
        self.fout.write("%sBegin%s\n" % (self.name, self.suffix))

    def __exit__(self, type, value, traceback):
        self.fout.write("%sEnd\n" % self.name)


class PbrtWriter:
    def __init__(self, fout: typing.io):
        self.fout = fout

    def _writeNumber(self, num: typing.Union[int, float]):
        if isinstance(num, int):
            self.fout.write("%d" % num)
        elif isinstance(num, float):
            self.fout.write("%f" % num)
        else:
            raise TypeError("num should be int of float")

    def _writeListOfNumber(self, num_list: list):
        for i, num in enumerate(num_list):
            if i:
                self.fout.write(" ")
            self._writeNumber(num)

    def _writeParams(self, params: list):
        if len(params) % 2 != 0:
            raise ValueError("Number of parameter should be even")

        for i in range(len(params)//2):
            param_name = params[2*i]
            params_value = params[2*i+1]
            self.fout.write('"%s" ' % param_name)
            if isinstance(params_value, str):
                self.fout.write('"%s"' % params_value)
            elif isinstance(params_value, int) or isinstance(params_value, float):
                self.fout.write('[')
                self._writeNumber(params_value)
                self.fout.write(']')
            elif isinstance(params_value, list) or isinstance(params_value, tuple):
                self.fout.write('[')
                self._writeListOfNumber(params_value)
                self.fout.write(']')
            else:
                raise TypeError(
                    "Type of parameter should be string, number or list of number")

            self.fout.write(" ")

    def _writeObj(self, obj: str, name: str, *params):
        self.fout.write('%s "%s" ' % (obj, name))
        self._writeParams(params)
        self.fout.write("\n")

    def camera(self, name: str, *params):
        self._writeObj("Camera", name, *params)

    def integrator(self, name: str, *params):
        self._writeObj("Integrator", name, *params)

    def shape(self, name: str, *params):
        self._writeObj("Shape", name, *params)

    def material(self, name: str, *params):
        self._writeObj("Material", name, *params)

    def lightSource(self, name: str, *params):
        self._writeObj("LightSource", name, *params)

    def areaLightSource(self, name: str, *params):
        self._writeObj("AreaLightSource", name, *params)

    def film(self, name: str, *params):
        self._writeObj("Film", name, *params)

    def sampler(self, name: str, *params):
        self._writeObj("Sampler", name, *params)

    def texture(self, name: str, number_type: str, type_name: str, *params):
        self.fout.write('Texture "%s" "%s" "%s"' %
                        (name, number_type, type_name))
        self._writeParams(params)
        self.fout.write("\n")

    def makeNamedMedium(self, name: str, type_name: str, *params):
        self.fout.write('MakeNamedMedium "%s" "%s"' % (name, type_name))
        self._writeParams(params)
        self.fout.write("\n")

    def mediumInterface(self, a: str, name: str):
        self.fout.write('MediumInterface "%s" "%s"' % (a, name))

    def objectInstance(self, name: str):
        self.fout.write('ObjectInstance "%s"' % name)

    def include(self, name: str):
        self.fout.write('Include "%s"' % name)

    def rotate(self, ang: float, vec: list):
        self.fout.write("Rotate %.2f " % float(ang))
        self._writeListOfNumber(vec)
        self.fout.write("\n")

    def translate(self, vec: list):
        self.fout.write("Translate ")
        self._writeListOfNumber(vec)
        self.fout.write("\n")

    def scale(self, vec: list):
        self.fout.write("Scale ")
        self._writeListOfNumber(vec)
        self.fout.write("\n")

    def concatTransform(self, mat: list):
        self.fout.write("ConcatTransform [")
        self._writeListOfNumber(mat)
        self.fout.write("]\n")

    def lookAt(self, vec: list):
        self.fout.write("LookAt ")
        self._writeListOfNumber(vec)
        self.fout.write("\n")

    def attribute(self):
        return PbrtBlock(self.fout, "Attribute")

    def objectb(self, name: str):
        return PbrtBlock(self.fout, "Object", ' "%s"' % name)

    def world(self):
        return PbrtBlock(self.fout, "World")
