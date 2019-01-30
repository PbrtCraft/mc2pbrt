class Matte:
    def __init__(self, block):
        self.block = block

    def write(self, fout, face):
        tex = face["texture"]
        if "tintindex" in face:
            if self.block._is("leaves"):
                tint_color = self.block.bdr.getFoliageColor(self.block.biome_id, 0)
            else:
                tint_color = self.block.bdr.getGrassColor(self.block.biome_id, 0)
            fout.write(('Material "matte" "texture Kd" "%s-color"' % tex) +
                       ('"rgb tintMap" [%f %f %f]\n' % tint_color))
        else:
            fout.write('Material "matte" "texture Kd" "%s-color"\n' % tex)


class Glass:
    def __init__(self, block):
        self.block = block

    def write(self, fout, face):
        tex = face["texture"]
        fout.write('Material "glass" "texture Kr" "%s-color"\n' % tex)


class Light:
    FULL_LIGHT = 5.
    def __init__(self, block):
        self.block = block

    def write(self, fout, face):
        tex = face["texture"]
        light = self.block.getLight()
        le = (light/15.)**2*Light.FULL_LIGHT
        fout.write(('AreaLightSource "texlight" "texture L" "%s-color"' % tex) +
                    '"rgb scale" [%f %f %f]\n' % (le, le, le))
