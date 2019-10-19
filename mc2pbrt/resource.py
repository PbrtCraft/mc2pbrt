import os
import shutil
import tempfile
import zipfile
import json
from tqdm import tqdm
from PIL import Image

from tuple_calculation import mult
from find_minecraft import getMinecraftFolder
from util import singleton


@singleton
class ResourceManager:
    '''
    ResourceManager try to build the folder structure:
        * workdir/
            * scenes/
                * block/
                * env/
                * (folders under textures)
                * target.pbrt
            * assets/
                * (folders under assets/minecraft except textures)
            * config.json
    '''

    def __init__(self):
        work_dir = os.getcwd()
        self.work_dir = work_dir
        if os.path.exists(os.path.join(work_dir, "resource.json")):
            with open("resource.json") as f:
                config = json.load(f)
        else:
            config = {}

        self.version_jar = os.path.join(work_dir, config.get("VersionJar", ""))
        self.scenes_path = os.path.join(work_dir, "scenes")
        self.assets_path = os.path.join(work_dir, "assets")
        if not os.path.isdir(self.scenes_path):
            self.setup()

        self.model_loader = ModelLoader(
            os.path.join(self.assets_path, "models"))
        self.blockstate_loader = BlockstateLoader(
            os.path.join(self.assets_path, "blockstates"))
        self.table_alpha = {}

    def isFile(self, fn):
        full_filename = os.path.join(self.scenes_path, fn)
        return os.path.isfile(full_filename)

    def hasAlpha(self, texture_fn):
        """Check if texture file has alpha channel

        Args:
            texture_fn: filename of texture.
        Returns:
            Texture has alpha channel or not.
        """
        if texture_fn not in self.table_alpha:
            full_filename = os.path.join(self.scenes_path, texture_fn)
            image = Image.open(full_filename)
            self.table_alpha[texture_fn] = len(image.mode) == 4

        return self.table_alpha[texture_fn]

    def setup(self):
        """Setup all resource"""
        self.setupModelAndTexture()
        self.setupFire()

    def setupVersionJar(self):
        """Get path of version jar"""
        if self.version_jar:
            if not os.path.isfile(self.version_jar):
                print("[Warning] %s does not exist." % self.version_jar)
                self.version_jar = ""
            else:
                return

        minecraft_dir = getMinecraftFolder()
        # TODO: Choose by user
        version = "1.14.4"
        version_file = os.path.join(
            minecraft_dir, "versions", version, version + ".jar")
        if not os.path.exists(version_file):
            print(
                "Default file path [%s] does not exist. Please input version resource file:" % version_file)
            version_file = input()

        self.version_jar = version_file

    def setupModelAndTexture(self):
        """
           1. Copy Model.json into folder
           2. Copy Texture into folder
        """
        self.setupVersionJar()
        with tempfile.TemporaryDirectory() as temp_dir:
            with zipfile.ZipFile(self.version_jar, 'r') as vzip:
                vzip.extractall(temp_dir)

            assets_path = os.path.join(temp_dir, "assets", "minecraft")
            os.rename(os.path.join(assets_path, "textures"), self.scenes_path)
            os.rename(assets_path, self.assets_path)

    def setupFire(self):
        """Setup cropped fire texture"""
        fire = os.path.join(self.scenes_path, "block", "fire.png")
        if os.path.isfile(fire):
            return
        fire_source = os.path.join(self.scenes_path, "block", "fire_0.png")
        img = Image.open(fire_source)
        area = (0, 0, 16, 16)
        cropped_img = img.crop(area)
        cropped_img.save(fire)


class ModelLoader:
    def __init__(self, path="."):
        self.path = path
        self.db = {}
        self.builtin_list = set(["entity/chest"])

    def _resolveTexture(self, data, texname):
        if texname[0] != '#':
            return texname
        if "textures" in data and texname[1:] in data["textures"]:
            return data["textures"][texname[1:]]
        return texname

    def _resolveElements(self, data):
        if "elements" in data:
            for ele in data["elements"]:
                for facename in ele["faces"]:
                    face = ele["faces"][facename]
                    face["texture"] = self._resolveTexture(
                        data, face["texture"])
            return True
        return False

    def _resolveTextures(self, data):
        if "textures" in data:
            texs = data["textures"]
            for tex in texs:
                texs[tex] = self._resolveTexture(data, texs[tex])
            return True
        return False

    def _getModel(self, name):
        if name in self.builtin_list:
            data = self._builtin(name)
        else:
            with open(self.path + "/" + name + ".json", "r") as f:
                data = json.load(f)

        self._resolveElements(data)

        if "parent" in data and data["parent"] not in ["block/block", "block/thin_block"]:
            par_data, dummy_1 = self._getModel(data["parent"])
            if "textures" in data:
                if "textures" not in par_data:
                    par_data["textures"] = {}
                for tex in data["textures"]:
                    par_data["textures"][tex] = data["textures"][tex]

            flag_eles = self._resolveElements(par_data)
            flag_texs = self._resolveTextures(par_data)
            if flag_eles or flag_texs:
                return par_data, data["parent"]
        return data, ""

    def _builtin(self, name):
        if name == "entity/chest":
            # Source: https://gist.github.com/Choonster/e8668c195eecf800cb5dc53538a9c848
            return {
                "textures": {
                    "0": "entity/chest/normal"
                },
                "elements": [
                    {
                        "name": "Base",
                        "from": [1.0, 0.0, 1.0],
                        "to": [15.0, 10.0, 15.0],
                        "faces": {
                            "north": {"texture": "#0", "uv": [3.5, 8.25, 7.0, 10.75]},
                            "east": {"texture": "#0", "uv": [0.0, 8.25, 3.5, 10.75]},
                            "south": {"texture": "#0", "uv": [10.5, 8.25, 14.0, 10.75]},
                            "west": {"texture": "#0", "uv": [7.0, 8.25, 10.5, 10.75]},
                            "up": {"texture": "#0", "uv": [3.5, 4.75, 7.0, 8.25]},
                            "down": {"texture": "#0", "uv": [10.5, 4.75, 7.0, 8.25]}
                        }
                    },
                    {
                        "name": "Knob",
                        "from": [7.0, 8.0, 0.0],
                        "to": [9.0, 12.0, 1.0],
                        "faces": {
                            "north": {"texture": "#0", "uv": [0.25, 0.25, 0.75, 1.25]},
                            "east": {"texture": "#0", "uv": [0.0, 0.25, 0.25, 1.25]},
                            "south": {"texture": "#0", "uv": [1.0, 0.25, 1.5, 1.25]},
                            "west": {"texture": "#0", "uv": [0.75, 0.25, 1.0, 1.25]},
                            "up": {"texture": "#0", "uv": [0.75, 0.0, 0.25, 0.25]},
                            "down": {"texture": "#0", "uv": [1.25, 0.0, 0.75, 0.25]}
                        }
                    },
                    {
                        "name": "Lid",
                        "from": [1.0, 9.0, 1.0],
                        "to": [15.0, 14.0, 15.0],
                        "faces": {
                            "north": {"texture": "#0", "uv": [3.5, 3.5, 7.0, 4.75]},
                            "east": {"texture": "#0", "uv": [0.0, 3.5, 3.5, 4.75]},
                            "south": {"texture": "#0", "uv": [10.5, 3.5, 14.0, 4.75]},
                            "west": {"texture": "#0", "uv": [7.0, 3.5, 10.5, 4.75]},
                            "up": {"texture": "#0", "uv": [3.5, 0.0, 7.0, 3.5]},
                            "down": {"texture": "#0", "uv": [10.5, 0.0, 7.0, 3.5]}
                        }
                    }
                ]
            }

    def getModel(self, name):
        if name not in self.db:
            model, par = self._getModel(name)
            self.db[name] = (model, par)
            if "elements" in model:
                for ele in model["elements"]:
                    ele["from"] = mult(ele["from"], 1./16)
                    ele["to"] = mult(ele["to"], 1./16)
                    for facename in ele["faces"]:
                        face = ele["faces"][facename]
                        uv = [0., 0., 1., 1.]
                        if "uv" in face:
                            uv = list(face["uv"])
                            for i in range(4):
                                uv[i] /= 16.
                        # swap UV
                        uv = [uv[1], uv[0], uv[3], uv[2]]
                        if name == "entity/chest":
                            # Don't know why
                            uv[0] = 1 - uv[0]
                            uv[2] = 1 - uv[2]
                        face["uv"] = tuple(uv)
        return self.db[name]


class BlockstateLoader:
    def __init__(self, path):
        self.path = path
        self.db = {}

    def _getBlockstate(self, name):
        with open(self.path + "/" + name + ".json", "r") as f:
            return json.load(f)

    def getBlockstate(self, name):
        if name not in self.db:
            self.db[name] = self._getBlockstate(name)
        return self.db[name]
