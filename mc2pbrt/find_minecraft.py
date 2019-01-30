import os
import sys
import errno

def getMinecraftFolder():
    """Get Miencraft Client Folder"""
    minecraft_dir = ""
    if "APPDATA" in os.environ and sys.platform.startswith("win"):
        # Windows
        minecraft_dir = os.path.join(os.environ['APPDATA'], ".minecraft")
    elif "HOME" in os.environ:
        # For linux:
        minecraft_dir = os.path.join(os.environ['HOME'], ".minecraft")
        if not os.path.exists(minecraft_dir) and sys.platform.startswith("darwin"):
            # For Mac:
            minecraft_dir = os.path.join(os.environ['HOME'], "Library", "Application Support",
                                         "minecraft")

    if not minecraft_dir:
        raise FileNotFoundError(errno.ENOENT, "Minecraft folder not found.")

    return minecraft_dir
