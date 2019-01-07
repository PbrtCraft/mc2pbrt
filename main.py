import sys
import json

import world

from model import ModelLoader
from pbrtwriter import PbrtWriter

with open(sys.argv[1], "r") as f:
    settings = json.load(f)

w = world.World(settings["World"])
r = settings["Radius"]
sz = 2*r+1
y_range = settings["YRange"]
ys = list(range(y_range[0], y_range[1]))
arr = [[[None]*sz for i in range(sz)] for j in ys]
dv = range(-r, r+1)
sx, sy, sz = settings["Origin"]

# check origin point

origin = w.get_block((sx, sy, sz)).state.name[10:]
if origin.find("air") == -1:
    print("[Warning] Origin point is not empty.")

from tqdm import tqdm

for y, dx, dz in tqdm([(y, dx, dz) for y in ys for dx in dv for dz in dv]):
    bs = w.get_block((sx+dx, y, sz+dz)).state
    name = bs.name[10:]
    arr[y-ys[0]][r + dz][r + dx] = [name, bs.props]

model_loader = ModelLoader("/home/master/06/mukyu99/GitDoc/mc2pbrt")
mp = PbrtWriter(model_loader)
mp.setBlocks(arr)

if "Samples" in settings:
    mp.samples = settings["Samples"]

if "Camera" in settings:
    mp.camera = settings["Camera"]

if "LookatVec" in settings:
    mp.lookat_vec = tuple(map(float, settings["LookatVec"]))

if "Method" in settings:
    arg_str = ""
    if "MethodArg" in settings:
        arg_str = settings["MethodArg"]
    mp.method = (settings["Method"], arg_str)


mp.writeFile(sys.argv[2])
