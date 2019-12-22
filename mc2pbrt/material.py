import biome

from pbrtwriter import PbrtWriter


class Foliage:
    def __init__(self, block):
        self.block = block

    def write(self, pbrtwriter: PbrtWriter, face):
        tex = face["texture"]
        tint_color = biome.getFoliageColor(self.block.biome_id, 0)
        pbrtwriter.material("translucent", "texture Kd", "%s-color" % tex,
                            "rgb reflect", tint_color, "rgb transmit", tint_color)


class Grass:
    def __init__(self, block):
        self.block = block

    def write(self, pbrtwriter: PbrtWriter, face):
        tex = face["texture"]
        tint_color = biome.getGrassColor(self.block.biome_id, 0)
        pbrtwriter.material("translucent", "texture Kd", "%s-color" % tex,
                            "rgb reflect", tint_color, "rgb transmit", tint_color)


class Matte:
    def __init__(self, block):
        self.block = block

    def write(self, pbrtwriter: PbrtWriter, face):
        tex = face["texture"]
        if "tintindex" in face:
            if self.block._is("leaves"):
                tint_color = biome.getFoliageColor(self.block.biome_id, 0)
            else:
                tint_color = biome.getGrassColor(self.block.biome_id, 0)
            pbrtwriter.material("matte", "texture Kd", "%s-color" %
                                tex, "rgb tintMap", tint_color)
        else:
            pbrtwriter.material("matte", "texture Kd", "%s-color" % tex)


class Glass:
    def __init__(self, block):
        self.block = block

    def write(self, pbrtwriter: PbrtWriter, face):
        tex = face["texture"]
        pbrtwriter.material("glass", "texture Kr", "%s-color" % tex)


class Light:
    FULL_LIGHT = 5.

    def __init__(self, block):
        self.block = block

    def write(self, pbrtwriter: PbrtWriter, face):
        tex = face["texture"]
        light = self.block.getLight()
        le = (light/15.)**2*Light.FULL_LIGHT

        pbrtwriter.areaLightSource(
            "texlight", "texture L", "%s-color" % tex, "rgb scale", (le, le, le))
