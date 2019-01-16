import sys
import json

import world

from model import ModelLoader
from biome import Biome
from pbrtwriter import PbrtWriter
from player import Player

with open("config.json", "r") as f:
    settings = json.load(f)

from find_minecraft import getMinecraftFolder 
import os

# current works for client
world_path = os.path.join(getMinecraftFolder(), "saves", settings["World"])

print("Get world:", world_path)

w = world.World(world_path)
r = settings["Radius"]
sz = 2*r+1
y_range = settings["YRange"]
ys = list(range(y_range[0], y_range[1]))
arr = [[[None]*sz for i in range(sz)] for j in ys]
dv = range(-r, r+1)

player = Player(world_path, settings["Player"])

isx, isy, isz = map(int, player.pos)
sx, sy, sz = player.pos 

# check origin point

origin = w.get_block((isx, isy, isz)).state.name[10:]
if origin.find("air") == -1:
    print("[Warning] Origin point is not empty.")

from tqdm import tqdm

for y, dx, dz in tqdm([(y, dx, dz) for y in ys for dx in dv for dz in dv],
                      ascii=True):
    bs = w.get_block((isx+dx, y, isz+dz)).state
    biome_id = w.get_biome((isx+dx, y, isz+dz))
    name = bs.name[10:]
    arr[y-ys[0]][r + dz][r + dx] = [name, bs.props, biome_id]

model_loader = ModelLoader(".")
biome_reader = Biome()
mp = PbrtWriter(model_loader, biome_reader)
mp.setBlocks(arr)

map_eye_y = sy+1.8-y_range[0]

from math import cos, sin, pi
theta, phi = player.rot
phi = -phi
tx, ty, tz = sin(theta)*cos(phi), sin(phi), cos(theta)*cos(phi)
phi += pi/2
nx, ny, nz = sin(theta)*cos(phi), sin(phi), cos(theta)*cos(phi)
nx, ny, nz = 0, 1, 0
mp.lookat_vec = (r, map_eye_y, r, r + tx, map_eye_y + ty, r + tz, nx, ny, nz) 

if "Samples" in settings:
    mp.samples = settings["Samples"]

if "Camera" in settings:
    mp.camera_cmd = settings["Camera"]

if "EnvLight" in settings:
    mp.envlight = settings["EnvLight"]

if "Method" in settings:
    arg_str = ""
    if "MethodArg" in settings:
        arg_str = settings["MethodArg"]
    mp.method = (settings["Method"], arg_str)

mp.writeFile(settings["Target"])
