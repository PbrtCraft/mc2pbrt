# mc2pbrt

![](pbrt.png)

This repo is a program that can output a pbrt file by current player pose.
To render a minecraft scene, it takes serveral steps.

* First, the config file should be setuped.
* Second, execute `realcam.py`.
* Third, use [pbrt-v3-minecraft](https://github.com/PbrtCraft/pbrt-v3-minecraft) to render pbrt file:
    `$ ./pbrt [path-to-mc2pbrt]/scenes/[pbrtfile].pbrt`

For client part, `realcam.py` will auto collect the resource of minecraft 1.13.2,
while for server part, the user need to download the resource pack and put files into right folders.

## Config

A example is provide as `config.json`.

## Folder

* block : The model json files should be here.
* scenes/block : Texture files should be here.
* scenes/env   : Current include 2 envirnment maps from [HavenHDRI](https://hdrihaven.com/hdris/)
