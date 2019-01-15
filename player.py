class Player:
    def __init__(self, world_path, username):
        from username_to_uuid import UsernameToUUID
        import nbt, stream, gzip
        utuuid = UsernameToUUID(username)
        uuid_fn = self._uuid_to_filename(utuuid.get_uuid()) 
        player_path = world_path + '/playerdata/' + uuid_fn + ".dat"
        with gzip.open(player_path, mode='rb') as p:
            in_stream = stream.InputStream(p.read())
            p_data = nbt.parse_nbt(in_stream)

        self.pos = [c.get() for c in p_data.get("Pos").children]
        self.rot = [c.get() for c in p_data.get("Rotation").children]

    def _uuid_to_filename(self, uuid):
        return "-".join([uuid[:8], uuid[8:12], uuid[12:16], uuid[16:20], uuid[20:]])


if __name__ == "__main__":
    import json
    with open("test.json", "r") as f:
        setting = json.load(f)

    p = Player(setting["World"], setting["Player"])
    print(p.pos, p.rot)
