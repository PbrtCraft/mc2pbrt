import os
import errno

import find_minecraft

from resource import ResourceManager
from pyanvil.world import World
from pyanvil.player import Player
from scene import Scene
from block import BlockCreator

from util import tqdmpos

class RealCam:
    """Produce a scene with radius"""

    def __init__(self, world_name, player_name, radius, samples,
                       camera_cmd, phenomenons, method):
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
        self.camera_cmd = camera_cmd
        self.phenomenons = phenomenons
        self.method = method

    def _laglongToCoord(self, theta, phi):
        """Convert lagtitude and longitude to xyz coordinate."""
        from math import cos, sin, pi
        theta, phi = -theta/180*pi, -phi/180*pi
        return sin(theta)*cos(phi), sin(phi), cos(theta)*cos(phi)

    def _getBlocks(self):
        """Get blocks by radius"""
        world = World(self.world_path)
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
            arr[y-ys[0]][r + dz][r + dx] = BlockCreator()(name, bs.props, biome_id)

        return arr

    def _getLookAt(self):
        """Get lookat vector by pos of player"""
        r = self.radius
        theta, phi = self.player.rot
        sx, sy, sz = self.player.pos
        tx, ty, tz = self._laglongToCoord(theta, phi) 
        nx, ny, nz = self._laglongToCoord(theta, phi + 90)
        map_eye_y = sy+1.8-1
        return (r, map_eye_y, r, r + tx, map_eye_y + ty, r + tz, nx, ny, nz)

    def run(self, target):
        blocks = self._getBlocks()
        scene = Scene(blocks)
        scene.lookat_vec = self._getLookAt()

        scene.samples = self.samples 
        scene.camera_cmd = self.camera_cmd 
        scene.phenomenons = self.phenomenons
        scene.method = (self.method, "")

        scene_path = os.path.join(ResourceManager().scene_folder, target)
        scene.write(scene_path)
