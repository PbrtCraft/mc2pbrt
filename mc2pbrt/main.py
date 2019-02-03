import json
import phenomenon

from realcam import RealCam

if __name__ == "__main__":
    with open("config.json", "r") as f:
        settings = json.load(f)

    phs = []
    for ph in settings.get("Phenomenons", []):
        if ph[0] == "Fog":
            phs.append(phenomenon.Fog(ph[1], ph[2]))
        elif ph[0] == "EnvLight":
            phs.append(phenomenon.EnvirnmentMap(ph[1]))
        elif ph[0] == "Sun":
            phs.append(phenomenon.Sun(ph[1], ph[2]))
        elif ph[0] == "Rain":
            phs.append(phenomenon.Rain(ph[1], ph[2]))
        else:
            print("[Warning] %s phenomenon not found." % ph[0])

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
