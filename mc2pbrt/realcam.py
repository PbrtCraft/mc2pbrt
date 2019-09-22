import os
import errno

import find_minecraft
import lookat

from resource import ResourceManager
from pyanvil.world import World
from pyanvil.player import Player
from scene import Scene
from block import BlockCreator

from util import tqdmpos


class RealCam:
    """Produce a scene with radius"""

    def __init__(self, world_name, player_name, radius, samples,
                 camera, phenomenons, method):
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
        self.player = Player(self.world_path, player_name)

        # parameters of scene
        self.radius = radius
        self.samples = samples
        self.camera = camera
        self.phenomenons = phenomenons
        self.method = method

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

    def run(self, target):
        blocks = self._getBlocks()
        scene = Scene(blocks)
        scene.lookat_vec = self._getLookAt()

        scene.samples = self.samples
        scene.camera = self.camera
        scene.phenomenons = self.phenomenons
        scene.method = (self.method, "")

        scene_path = os.path.join(ResourceManager().scenes_path, target)
        scene.write(scene_path)
