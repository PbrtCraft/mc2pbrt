import sys
import json
import phenomenon
import camera
import method

from realcam import RealCam


if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        settings = json.load(f)

    phs = []
    for ph in settings.get("Phenomenons", []):
        phs.append(phenomenon.create(ph["name"], ph["params"]))

    json_camera = settings.get("Camera", None)
    if json_camera is None:
        cam = camera.CameraPerspective()
    else:
        cam = camera.create(json_camera["name"], json_camera["params"])

    json_method = settings.get("Method", None)
    if json_method is None:
        use_method = method.PathTracing()
    else:
        use_method = method.create(json_method["name"], json_method["params"])

    rc = RealCam(
        world_name=settings["World"],
        player_name=settings["Player"],
        radius=settings["Radius"],
        samples=settings.get("Samples", 16),
        camera=cam,
        method=use_method,
        phenomenons=phs,
    )

    rc.run(settings.get("Target", "target.pbrt"))
