import json
import gzip
import os
import http.client

import pyanvil.nbt as nbt
import pyanvil.stream as stream


def create(world_path, obj):
    if isinstance(obj, str):
        return Player(world_path, username=obj)
    if "name" in obj:
        return Player(world_path, username=obj["name"])
    elif "uuid" in obj:
        return Player(world_path, uuid=obj["uuid"])
    raise KeyError("Player should be create with name or uuid")


class Player:
    def __init__(self, world_path: str, username: str = "", uuid: str = ""):
        if uuid == "":
            uuid = self._username_to_uuid(username)

        uuid_fn = self._uuid_to_filename(uuid)
        player_path = os.path.join(world_path, "playerdata", uuid_fn + ".dat")
        with gzip.open(player_path, mode='rb') as player_file:
            in_stream = stream.InputStream(player_file.read())
            p_data = nbt.parse_nbt(in_stream)

        self.pos = [c.get() for c in p_data.get("Pos").children]
        self.rot = [c.get() for c in p_data.get("Rotation").children]
        self.dim = p_data.get("Dimension").get()

    def _uuid_to_filename(self, uuid: str) -> str:
        return "-".join([uuid[:8], uuid[8:12], uuid[12:16], uuid[16:20], uuid[20:]])

    def _username_to_uuid(self, username: str) -> str:
        """Get the UUID of the player."""
        http_conn = http.client.HTTPSConnection("api.mojang.com")
        header = {'User-Agent': 'Minecraft Username -> UUID',
                  'Content-Type': 'application/json'}
        http_conn.request(
            "GET", "/users/profiles/minecraft/" + username, headers=header)
        response = http_conn.getresponse().read().decode("utf-8")

        if not response:
            raise KeyError("player probably doesn't exist")

        json_data = json.loads(response)
        return json_data['id']
