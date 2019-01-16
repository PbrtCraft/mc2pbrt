from find_minecraft import getMinecraftFolder
import os, shutil
import tempfile
import zipfile
from tqdm import tqdm

def copyModelToFolder():
    """Copy Model.json into folder"""
    minecraft_dir = getMinecraftFolder()
    version = "1.13.2"
    version_file = os.path.join(minecraft_dir, "versions", version, version + ".jar")
    with tempfile.TemporaryDirectory() as temp_dir:
        with zipfile.ZipFile(version_file, 'r') as vzip:
            vzip.extractall(temp_dir)
        
        block_model_dir = os.path.join(temp_dir, "assets", "minecraft", "models", "block")
        local_block_folder = os.path.join(".", "block")
        for filename in tqdm(os.listdir(block_model_dir), ascii=True):
            if filename.endswith(".json"):
                full_filename = os.path.join(block_model_dir, filename)
                shutil.copy(full_filename, local_block_folder)

def checkModelFolder():
    """Check if the folder has model json file"""
    local_block_folder = os.path.join(".", "block")
    json_list = [fn for fn in os.listdir(local_block_folder) if fn.endswith(".json")]
    # Check with hash function ?
    return len(json_list) > 0