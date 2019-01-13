import sys, math, nbt, gzip, zlib, stream, time

class BlockState:
    def __init__(self, name, props):
        self.name = name
        self.props = props

    def __str__(self):
        return 'BlockState(' + self.name + ',' + str(self.props) + ')'


class Block:
    AIR = None
    def __init__(self, state):
        self.state = state

    def __str__(self):
        return 'Block(' + str(self.state) + ')'

    def get_state(self):
        return self.state

Block.AIR = Block(BlockState('minecraft:air', {}))


class ChunkSection:
    def __init__(self, blocks, raw_section, y_index):
        self.blocks = blocks
        self.raw_section = raw_section
        self.y_index = y_index

    def get_block(self, block_pos):
        x = block_pos[0]
        y = block_pos[1]
        z = block_pos[2]

        return self.blocks[x + z * 16 + y * 16 ** 2]


class Chunk:
    def __init__(self, xpos, zpos, raw_nbt):
        self.xpos = xpos
        self.zpos = zpos
        self._build(raw_nbt)
        
    def _build(self, raw_nbt):
        sections = {}
        level_node = raw_nbt.get('Level')
        for section in level_node.get('Sections').children:
            flatstates = [c.get() for c in section.get('BlockStates').children]
            pack_size = int((len(flatstates) * 64) / (16**3))
            states = [
                Chunk._read_width_from_loc(flatstates, pack_size, i) for i in range(16**3)
            ]
            palette = [ 
                BlockState(
                    state.get('Name').get(),
                    state.get('Properties').to_dict() if state.has('Properties') else {}
                ) for state in section.get('Palette').children
            ]
            blocks = [
                Block(palette[state]) for state in states
            ]
            sections[section.get('Y').get()] = ChunkSection(blocks, section, section.get('Y').get())

        self.sections = sections
        self.biome_table = [b.get() for b in level_node.get('Biomes').children]

    def _read_width_from_loc(long_list, width, possition):
        offset = possition * width
        # if this is split across two nums
        if (offset % 64) + width > 64:
            # Find the lengths on each side of the split
            side1len = 64 - ((offset) % 64)
            side2len = ((offset + width) % 64)
            # Select the sections we want from each
            side1 = Chunk._read_bits(long_list[int(offset/64)], side1len, offset % 64)
            side2 = Chunk._read_bits(long_list[int((offset + width)/64)], side2len, 0)
            # Join them
            comp = (side2 << side1len) + side1
            return comp
        else:
            comp = Chunk._read_bits(long_list[int(offset/64)], width, offset % 64)
            return comp

    def _read_bits(num, width, start):
        # create a mask of size 'width' of 1 bits
        mask = (2 ** width) - 1
        # shift it out to where we need for the mask
        mask = mask << start
        # select the bits we need
        comp = num & mask
        # move them back to where they should be
        comp = comp >> start

        return comp

    def get_block(self, block_pos):
        return self.get_section(block_pos[1]).get_block([n % 16 for n in block_pos])

    def get_biome(self, block_pos):
        z = block_pos[2]%16
        x = block_pos[0]%16
        return self.biome_table[z*16 + x]

    def get_section(self, y):
        key = int(y/16)
        if key not in self.sections:
            self.sections[key] = ChunkSection(
                [Block.AIR]*4096,
                nbt.CompoundTag('None'),
                key
            )
        return self.sections[key]

    def __str__(self):
        return "Chunk(" + str(self.xpos) + "," + str(self.zpos) + ")"


class World:
    def __init__(self, file_name, save_location=''):
        self.file_name = file_name
        self.save_location = save_location
        self.chunks = {}

    def get_block(self, block_pos):
        chunk_pos = self._get_chunk(block_pos)
        chunk = self.get_chunk(chunk_pos)
        return chunk.get_block(block_pos)

    def get_biome(self, block_pos):
        chunk_pos = self._get_chunk(block_pos)
        chunk = self.get_chunk(chunk_pos)
        return chunk.get_biome(block_pos)

    def get_chunk(self, chunk_pos):
        if chunk_pos not in self.chunks:
            self._load_chunk(chunk_pos)

        return self.chunks[chunk_pos]

    def _load_chunk(self, chunk_pos):
        with open(self.save_location + '/' + self.file_name + '/region/' + self._get_region_file(chunk_pos), mode='rb') as region:
            locations = [[
                        int.from_bytes(region.read(3), byteorder='big', signed=False) * 4096, 
                        int.from_bytes(region.read(1), byteorder='big', signed=False) * 4096
                    ] for i in range(1024) ]

            timestamps = region.read(4096)

            chunk = self._load_binary_chunk_at(region, locations[((chunk_pos[0] % 32) + (chunk_pos[1] % 32) * 32)][0])
            self.chunks[chunk_pos] = chunk

    def _load_binary_chunk_at(self, region_file, offset):
        region_file.seek(offset)
        datalen = int.from_bytes(region_file.read(4), byteorder='big', signed=False)
        compr = region_file.read(1)
        decompressed = zlib.decompress(region_file.read(datalen))
        data = nbt.parse_nbt(stream.InputStream(decompressed))
        chunk_pos = (data.get('Level').get('xPos').get(), data.get('Level').get('zPos').get())
        chunk = Chunk(
            chunk_pos[0],
            chunk_pos[1],
            data
        )
        return chunk

    def _get_region_file(self, chunk_pos):
        return 'r.' + '.'.join([str(x) for x in self._get_region(chunk_pos)]) + '.mca'


    def _get_chunk(self, block_pos):
        return (math.floor(block_pos[0] / 16), math.floor(block_pos[2] / 16))

    def _get_region(self, chunk_pos):
        return (math.floor(chunk_pos[0] / 32), math.floor(chunk_pos[1] / 32))
