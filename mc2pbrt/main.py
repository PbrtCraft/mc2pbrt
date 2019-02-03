import json
import phenomenon

from realcam import RealCam

if __name__ == "__main__":
    with open("config.json", "r") as f:
        settings = json.load(f)

    phs = []
    if "EnvLight" in settings:
        phs = [
            phenomenon.EnvirnmentMap(settings["EnvLight"])
        ]

    rc = RealCam(
        world_name = settings["World"],
        player_name = settings["Player"],
        radius = settings["Radius"],
        samples = settings.get("Samples", 16),
        camera_cmd = settings.get("Camera", 'Camera "environment"'),
        method = settings.get("Method", 'path'),
        phenomenons = phs,
    )

    rc.run(settings.get("Target", "target.pbrt"))
