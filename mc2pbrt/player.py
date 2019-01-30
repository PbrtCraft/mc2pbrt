import json, gzip
import http.client

import pyanvil.nbt as nbt
import pyanvil.stream as stream

class Player:
    def __init__(self, world_path, username):
        uuid = self._username_to_uuid(username)
        uuid_fn = self._uuid_to_filename(uuid)
        player_path = world_path + '/playerdata/' + uuid_fn + ".dat"
        with gzip.open(player_path, mode='rb') as p:
            in_stream = stream.InputStream(p.read())
            p_data = nbt.parse_nbt(in_stream)

        self.pos = [c.get() for c in p_data.get("Pos").children]
        self.rot = [c.get() for c in p_data.get("Rotation").children]

    def _uuid_to_filename(self, uuid):
        return "-".join([uuid[:8], uuid[8:12], uuid[12:16], uuid[16:20], uuid[20:]])

    def _username_to_uuid(self, username):
        """Get the UUID of the player."""
        get_args = ""

        http_conn = http.client.HTTPSConnection("api.mojang.com")
        http_conn.request("GET", "/users/profiles/minecraft/" + username + get_args, 
                          headers={'User-Agent':'Minecraft Username -> UUID', 'Content-Type':'application/json'})
        response = http_conn.getresponse().read().decode("utf-8")

        if not response and timestamp is None: # No response & no timestamp
            return self.get_uuid(0) # Let's retry with the Unix timestamp 0.
        if not response: # No response (player probably doesn't exist)
            return ""

        json_data = json.loads(response)
        try:
            uuid = json_data['id']
        except KeyError as e:
            print("KeyError raised:", e);

        return uuid


if __name__ == "__main__":
    with open("test.json", "r") as f:
        setting = json.load(f)

    p = Player(setting["World"], setting["Player"])
    print(p.pos, p.rot)
