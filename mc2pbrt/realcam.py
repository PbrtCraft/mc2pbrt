import os
import errno

import find_minecraft
import lookat
import pyanvil.player

from resource import ResourceManager
from pyanvil.world import World
from block import BlockCreator, BlockSolver
from water import WaterSolver
from lava import LavaSolver

from util import tqdmpos


class RealCam:
    """Produce a scene with radius"""

    def __init__(self, world_name, player_obj, radius, samples,
                 camera, phenomenons, method, resolution):
        # World an be a full path or a world folder name
        if os.path.exists(world_name):
            world_path = world_name
        else:
            world_path = os.path.join(find_minecraft.getMinecraftFolder(),
                                      "saves", world_name)
            if not os.path.exists(world_path):
                raise FileNotFoundError(errno.ENOENT, "World not found.")
        print("Get world:", world_path)
        self.world_path = world_path
        self.player = pyanvil.player.create(self.world_path, player_obj)

        # parameters of scene
        self.radius = radius
        self.samples = samples
        self.camera = camera
        self.phenomenons = phenomenons
        self.method = method
        self.resolution = resolution

    def _getBlocks(self):
        """Get blocks by radius"""

        # Determine folder of dim
        dim_path = self.world_path
        if self.player.dim != 0:
            dim_path = os.path.join(self.world_path, "DIM%d" % self.player.dim)
        world = World(dim_path)

        r = self.radius
        sz = 2*r+1
        ys = list(range(1, 256))
        arr = [[[None]*sz for i in range(sz)] for j in ys]
        dv = range(-r, r+1)

        isx, isy, isz = map(int, self.player.pos)

        # check origin point
        origin = world.get_block((isx, isy, isz)).state.name[10:]
        if origin.find("air") == -1:
            print("[Warning] Origin point is not empty.")

        for y, dx, dz in tqdmpos(ys, dv, dv):
            bs = world.get_block((isx+dx, y, isz+dz)).state
            biome_id = world.get_biome((isx+dx, y, isz+dz))
            name = bs.name[10:]
            arr[y-ys[0]][r + dz][r + dx] = BlockCreator()(name, bs.props,
                                                          biome_id)

        return arr

    def _getLookAt(self):
        """Get lookat vector by pos of player"""
        r = self.radius
        isx, dummy_1, isz = map(int, self.player.pos)
        vec = lookat.firstPerson(self.player)
        dx, dz = isx - r, isz - r
        return (vec[0] - dx, vec[1], vec[2] - dz,
                vec[3] - dx, vec[4], vec[5] - dz,
                vec[6], vec[7], vec[8])

    def run(self, target, update_scene):
        self.lookat_vec = self._getLookAt()
        self.stand_pt = tuple(map(int, self.lookat_vec[:3]))

        target_name, target_ext = os.path.splitext(target)

        main_path = os.path.join(
            ResourceManager().scenes_path, target)

        scene_filename = target_name + "_scene" + target_ext
        scene_path = os.path.join(
            ResourceManager().scenes_path, scene_filename)

        print("Start writing main file ...")
        self._writeMain(main_path, scene_filename)

        if update_scene:
            print("Start writing scene file ...")
            self._writeScene(scene_path)

    def _writeMain(self, filename, scene_filename):
        fout = open(filename, "w")

        # The coordinate system of minecraft and pbrt is different.
        # Pbrt is lefthand base, while minecraft is righthand base.
        fout.write("Scale -1 1 1\n")

        fout.write(
            'Film "image" "integer xresolution" [%d] "integer yresolution" [%d]\n' %
            (self.resolution["Width"], self.resolution["Height"]))

        fout.write('LookAt %f %f %f  %f %f %f %f %f %f\n' % self.lookat_vec)

        self.camera.write(fout)
        self.method.write(fout)

        fout.write(
            'Sampler "lowdiscrepancy" "integer pixelsamples" [%d]\n' % self.samples)

        fout.write('WorldBegin\n')
        fout.write('Include "%s"\n' % scene_filename)
        fout.write('WorldEnd\n')

    def _writeScene(self, filename):
        fout = open(filename, "w")

        for phenomenon in self.phenomenons:
            phenomenon.write(fout)

        blocks = self._getBlocks()
        block_solver = BlockSolver(blocks)
        block_solver.write(fout, self.stand_pt)

        water_solver = WaterSolver(blocks)
        water_solver.write(fout)

        lava_solver = LavaSolver(blocks)
        lava_solver.write(fout)
