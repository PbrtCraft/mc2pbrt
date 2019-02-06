import json
import phenomenon
import camera

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

    json_camera = settings.get("Camera", None)
    if json_camera is None:
        cam = camera.CameraPerspective()
    else:
        if json_camera["name"] == "perspective":
            cam = camera.CameraPerspective(json_camera["fov"])
        elif json_camera["name"] == "envirnment":
            cam = camera.CameraEnvirnment()
        elif json_camera["name"] == "realistic":
            cam = camera.CameraRealistic()
        else:
            cam = camera.CameraPerspective()

    rc = RealCam(
        world_name = settings["World"],
        player_name = settings["Player"],
        radius = settings["Radius"],
        samples = settings.get("Samples", 16),
        camera = cam,
        method = settings.get("Method", 'path'),
        phenomenons = phs,
    )

    rc.run(settings.get("Target", "target.pbrt"))
