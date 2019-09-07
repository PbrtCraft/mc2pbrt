import os

from resource import ResourceManager


class EnvirnmentMap:
    def __init__(self, filename):
        self.filename = filename
        if not os.path.isfile(os.path.join(ResourceManager().scene_folder, filename)):
            print("[Warning] EnvirnmentMap: %s file does not exist" % filename)

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


class Rayleigh:
    """
        Sky's Rayleigh scattering
        Take 680, 550, 440 nm light as RGB
        From **Physically Based Sky, Atmosphere and Cloud Rendering in Frostbite**
    """

    def __init__(self):
        from math import e
        self.I_s = (5.8*e**(-6), 1.35*e**(-5), 3.31*e**(-5))

    def write(self, fout):
        fout.write('MakeNamedMedium "Rayleigh" "string type" "homogeneous" ' +
                   '"rgb sigma_s" [%f %f %f]\n' % self.I_s +
                   '"rgb sigma_a" [0 0 0]\n')
        fout.write('MediumInterface "" "Rayleigh"\n')


class Sun:
    def __init__(self, hour, scene_radius):
        if hour < 6 or hour > 18:
            raise ValueError("Hour should be in the range of [6, 18]")

        from math import cos, sin, pi
        theta = (hour - 12)/12*pi
        dist = scene_radius*3
        mid = scene_radius
        self.position = (mid + dist*sin(theta), dist*cos(theta), mid)

        # Empirical formula
        self.scale = 50./(80**2)*(dist**2)

    def write(self, fout):
        fout.write('LightSource "distant" "point from" [%f %f %f]' % self.position +
                   '"blackbody L" [6500 %f]' % self.scale)


class Rain:
    def __init__(self, rainfall, scene_radius):
        self.size = scene_radius*2 + 1
        self.rainfall = rainfall

    def write(self, fout):
        from random import uniform, randint
        from tqdm import tqdm
        from util import tqdmpos

        def uni01(x): return uniform(0, 1)

        print("Preparing rain instance...")
        fout.write('AttributeBegin\n')
        fout.write(
            'Material "glass" "float eta" [1.33] "rgb Kt" [.28 .72 1]\n')
        for i in tqdm(range(100), ascii=True):
            fout.write('ObjectBegin "RainStreak%02d"\n' % i)
            for dummy_1 in range(100*self.rainfall):
                fout.write('AttributeBegin\n')
                x, y, z = map(uni01, [None]*3)
                l = uniform(0, 0.1)
                fout.write('Translate %f %f %f\n' % (x, y, z))
                fout.write('Shape "cylinder" "float radius" [0.001] ' +
                           '"float zmin" [%f] "float zmax" [%f]\n' % (-l/2, l/2))
                fout.write('AttributeEnd\n')
            fout.write('ObjectEnd\n')

        # Pbrt cylinder is z-base.
        fout.write('ConcatTransform [1 0 0 0 ' +
                   '0 0 1 0 ' +
                   '0 1 0 0 ' +
                   '0 0 0 1]\n')
        sz = self.size
        print("Writing rain streaks...")
        for x, y, z in tqdmpos(range(sz), range(sz), range(256)):
            ind = randint(0, 99)
            fout.write('AttributeBegin\n')
            fout.write("Translate %d %d %d\n" % (x, y, z))
            fout.write('ObjectInstance "RainStreak%02d"\n' % ind)
            fout.write('AttributeEnd\n')
        fout.write('AttributeEnd\n')
