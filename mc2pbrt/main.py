import sys
import json
import phenomenon
import camera
import method

from argparse import ArgumentParser

from realcam import RealCam


if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument("--filename", type=str, help="Filename")
    parser.add_argument("--no-update-scene",
                        action='store_true', help="Use old scene file")
    args = parser.parse_args()

    with open(args.filename, "r", encoding="utf-8") as f:
        settings = json.load(f)

    phs = []
    for ph in settings.get("Phenomenons", []):
        phs.append(phenomenon.create(ph["name"], ph["params"]))

    json_camera = settings.get("Camera", None)
    if json_camera is None:
        cam = camera.Perspective()
    else:
        cam = camera.create(json_camera["name"], json_camera["params"])

    json_method = settings.get("Method", None)
    if json_method is None:
        use_method = method.PathTracing()
    else:
        use_method = method.create(json_method["name"], json_method["params"])

    rc = RealCam(
        world_name=settings["World"],
        player_obj=settings["Player"],
        radius=settings["Radius"],
        samples=settings.get("Samples", 16),
        camera=cam,
        method=use_method,
        phenomenons=phs,
        resolution=settings.get("Resolution", {"Width": 960, "Height": 480}),
    )

    rc.run(
        target=settings.get("Target", "target.pbrt"),
        update_scene=not args.no_update_scene,
    )
