from find_minecraft import getMinecraftFolder
import os, shutil
import tempfile
import zipfile
from tqdm import tqdm

def setup():
    """
       1. Copy Model.json into folder
       2. Copy Texture into folder
    """

    has_model = checkModelFolder()
    has_texture = checkTextureFolder()

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
            local_block_folder = os.path.join(".", "block")
            for filename in tqdm(os.listdir(block_model_dir), ascii=True):
                if filename.endswith(".json"):
                    full_filename = os.path.join(block_model_dir, filename)
                    shutil.copy(full_filename, local_block_folder)
        
        if not has_texture:
            print("Copy texture files...")
            texture_dir = os.path.join(temp_dir, "assets", "minecraft", "textures", "block")
            local_texture_folder = os.path.join(".", "scenes", "block")
            for filename in tqdm(os.listdir(texture_dir), ascii=True):
                full_filename = os.path.join(texture_dir, filename)
                shutil.copy(full_filename, local_texture_folder)


def checkModelFolder():
    """Check if the folder has model json file"""
    local_block_folder = os.path.join(".", "block")
    json_list = [fn for fn in os.listdir(local_block_folder) if fn.endswith(".json")]
    # Check with hash function ?
    return len(json_list) > 0


def checkTextureFolder():
    """Check if the folder has texture pngs"""
    local_textures_folder = os.path.join(".", "scenes", "block")
    png_list = [fn for fn in os.listdir(local_textures_folder) if fn.endswith(".png")]
    # Check with hash function ?
    return len(png_list) > 0
