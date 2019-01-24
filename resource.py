from find_minecraft import getMinecraftFolder
import os, shutil
import tempfile
import zipfile
from tqdm import tqdm
from PIL import Image

class ResourceManager:
    inst = None
    def __init__(self):
        ResourceManager.inst = self
        self.local_model_folder = os.path.join(".", "block")
        self.local_texture_folder = os.path.join(".", "scenes", "block")
        self.setup()

        self.table_alpha = {}

    def hasAlpha(self, texture_fn):
        """Check if texture file has alpha channel"""
        if texture_fn not in self.table_alpha:
            full_filename = os.path.join(self.local_texture_folder, "..", texture_fn) 
            image = Image.open(full_filename)
            self.table_alpha[texture_fn] = len(image.mode) == 4

        return self.table_alpha[texture_fn]

    def setup(self):
        """
           1. Copy Model.json into folder
           2. Copy Texture into folder
        """

        has_model = self.checkModelFolder()
        has_texture = self.checkTextureFolder()

        if has_model and has_texture:
            return

        minecraft_dir = getMinecraftFolder()
        version = "1.13.2"
        version_file = os.path.join(minecraft_dir, "versions", version, version + ".jar")
        with tempfile.TemporaryDirectory() as temp_dir:
            with zipfile.ZipFile(version_file, 'r') as vzip:
                vzip.extractall(temp_dir)
            
            if not has_model: 
                print("Copy model json files...", )
                block_model_dir = os.path.join(temp_dir, "assets", "minecraft", "models", "block")
                for filename in tqdm(os.listdir(block_model_dir), ascii=True):
                    if filename.endswith(".json"):
                        full_filename = os.path.join(block_model_dir, filename)
                        shutil.copy(full_filename, self.local_model_folder)
            
            if not has_texture:
                print("Copy texture files...")
                texture_dir = os.path.join(temp_dir, "assets", "minecraft", "textures", "block")
                for filename in tqdm(os.listdir(texture_dir), ascii=True):
                    full_filename = os.path.join(texture_dir, filename)
                    shutil.copy(full_filename, self.local_texture_folder)

    def checkModelFolder(self):
        """Check if the folder has model json file"""
        json_list = [fn for fn in os.listdir(self.local_model_folder) if fn.endswith(".json")]
        # Check with hash function ?
        return len(json_list) > 0

    def checkTextureFolder(self):
        """Check if the folder has texture pngs"""
        png_list = [fn for fn in os.listdir(self.local_texture_folder) if fn.endswith(".png")]
        # Check with hash function ?
        return len(png_list) > 0
