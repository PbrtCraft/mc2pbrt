# mc2pbrt

![](https://travis-ci.com/PbrtCraft/mc2pbrt.svg?branch=master)

![](pbrt.png)

This repo is a program that can output a pbrt file by current player pose.
To render a minecraft scene, it takes serveral steps.

* First, the config file should be setuped. See **Config**.
* Second, execute `main.py`.
* Third, use [pbrt-v3-minecraft](https://github.com/PbrtCraft/pbrt-v3-minecraft) to render pbrt file:
    `$ ./pbrt [path-to-mc2pbrt]/scenes/[pbrtfile].pbrt`

For client part, mc2pbrt will auto collect the resource of minecraft 1.14.4,
while for server part, the user need to download the resource pack and put files into right folders.

## Config

Example:

```json
{
  "Samples" : 256,
  "Camera" : {
    "name" : "Perspective",
    "fov" : 75
  },
  "World" : "Idea",
  "Player" : "Mudream",
  "Phenomenons" : [
    {
      "name": "EnvironmentMap",
      "params": {
        "filename": "env/aristea_wreck_4k.exr"
      }
    }
  ],
  "Method" : {
    "name": "path",
    "params": {},
  },
  "Radius" : 16,
  "Target" : "example.pbrt"
}
```

* Samples: Samples per pixel, default value is 16.
* Camera: Pbrt camera name and parameter, default value is a perspective camera with fov = 70.
* World: World name (if envirnment is minecraft client) or a full path to world
* Player: ID of player. Allow two type of input:
  - Use player name:
    - dict: `{"name": "Player name"}`
    - string: `"Player name"`
  - Use player UUID: `{"uuid": "Player uuid"}`
* Phenomenons: A list of phenomenons, see more detail at **Phenomenons System**.
* Method: Render method, default is path tracing.
* Radius: Render block radius
* Target: Output filename, default is `target.pbrt`

Here is a shorter config file:

```json
{
  "World" : "Idea",
  "Player" : "Mudream",
  "Radius" : 32,
  "Phenomenons": [
    {
      "name": "Sun",
      "params": {
        "hour": 16,
        "scene_radius": 4
      }
    }
  ]  
}
```

### Phenomenons System

#### EnvironmentMap

Use envirnment light map as sky. Parameters:

* `filename`: map filename

#### Sun

Write a blackbody with T=6500 to simulate sun. Parameters:

* `hour`: Simulate time, shound be in range of [6, 18]. 
* `scene_radius`: Radius of scene.

#### Fog

Use homogeneous volume to simulate fog.
Note that this fog will shield envlight.
Parameters:

* `I_s`: Scatter scalar
* `I_a`: Absorb scalar 

#### Rain

Generate many cylinder to simulate rain drop.

Parameters:

* `rainfall`: quantity of rain
