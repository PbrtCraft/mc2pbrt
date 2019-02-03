class EnvirnmentMap:
    def __init__(self, filename):
        self.filename = filename

    def write(self, fout):
        fout.write('AttributeBegin\n')
        fout.write('    Rotate 270 1 0 0 \n')
        fout.write('    LightSource "infinite" "integer nsamples" [16] "rgb L" [1 1 1]' +
                   '"string mapname" ["%s"]\n' % self.filename)
        fout.write('AttributeEnd\n')
