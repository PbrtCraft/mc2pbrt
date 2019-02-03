class EnvirnmentMap:
    def __init__(self, filename):
        self.filename = filename

    def write(self, fout):
        fout.write('AttributeBegin\n')
        fout.write('    Rotate 270 1 0 0 \n')
        fout.write('    LightSource "infinite" "integer nsamples" [16] "rgb L" [1 1 1]' +
                   '"string mapname" ["%s"]\n' % self.filename)
        fout.write('AttributeEnd\n')


class Fog:
    def __init__(self, I_s, I_a):
        self.I_s = I_s
        self.I_a = I_a

    def write(self, fout):
        I_s = tuple([self.I_s]*3)
        I_a = tuple([self.I_a]*3)
        fout.write('MakeNamedMedium "Fog" "string type" "homogeneous" ' +
                   '"rgb sigma_s" [%f %f %f]\n' % I_s +
                   '"rgb sigma_a" [%f %f %f]\n' % I_a)
        fout.write('MediumInterface "" "Fog"\n')
