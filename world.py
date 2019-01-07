import sys, math, nbt, gzip, zlib, stream, time

class BlockState:
    def __init__(self, name, props):
        self.name = name
        self.props = props

    def __str__(self):
        return 'BlockState(' + self.name + ',' + str(self.props) + ')'

class Block:
    def __init__(self, state):
        self.state = state
        self.dirty = False

    def __str__(self):
        return 'Block(' + str(self.state) + ')'

    def set_state(self, state):
        self.dirty = True
        self.state = state

    def get_state(self):
        return self.state

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

    def serialize(self):
        serial_section = self.raw_section
        # for b in self.blocks:
        #     if b.dirty:
        #         print("DirtyBlock:", b.get_state())
        dirty = any([b.dirty for b in self.blocks])
        if dirty:
            self.palette = list(set([b.get_state() for b in self.blocks]))
            serial_section.add_child(nbt.ByteTag('Y', self.y_index))
            serial_section.add_child(self._serialize_palette())
            serial_section.add_child(self._serialize_blockstates())
        
        if not serial_section.has('SkyLight'):
            serial_section.add_child(nbt.ByteArrayTag('SkyLight', [nbt.ByteTag('None', -1) for i in range(2048)]))

        if not serial_section.has('BlockLight'):
            serial_section.add_child(nbt.ByteArrayTag('BlockLight', [nbt.ByteTag('None', -1) for i in range(2048)]))

        return serial_section

    def _serialize_palette(self):
        serial_palette = nbt.ListTag('Palette', nbt.CompoundTag.clazz_id)
        for i in range(len(self.palette)):
            state = self.palette[i]
            state.id = i
            palette_item = nbt.CompoundTag('None', children=[
                nbt.StringTag('Name', state.name)
            ])
            if len(state.props) != 0:
                serial_props = nbt.CompoundTag('Properties')
                for name, val in state.props.items():
                    serial_props.add_child(nbt.StringTag(name, str(val)))
                palette_item.add_child(serial_props)
            serial_palette.add_child(palette_item)
        
        return serial_palette

    def _serialize_blockstates(self):
        serial_states = nbt.LongArrayTag('BlockStates')
        width = math.ceil(math.log(len(self.palette), 2))
        if width < 4:
            width = 4
        data = 0
        for block in reversed(self.blocks):
            data = (data << width) + block.state.id

        mask = (2 ** 64) - 1
        for i in range(int((len(self.blocks) * width)/64)):
            lng = data & mask
            lng = int.from_bytes(lng.to_bytes(8, byteorder='big', signed=False), byteorder='big', signed=True)
            serial_states.add_child(nbt.LongTag('', lng))
            data = data >> 64
        return serial_states

class Chunk:

    def __init__(self, xpos, zpos, sections, raw_nbt):
        self.xpos = xpos
        self.zpos = zpos
        self.sections = sections
        self.raw_nbt = raw_nbt
        
    def get_block(self, block_pos):
        return self.get_section(block_pos[1]).get_block([n % 16 for n in block_pos])

    def get_section(self, y):
        key = int(y/16)
        if key not in self.sections:
            self.sections[key] = ChunkSection(
                [Block(BlockState('minecraft:air', {})) for i in range(4096)],
                nbt.CompoundTag('None'),
                key
            )
        return self.sections[key]

    def find_like(self, string):
        results = []
        for sec in self.sections:
            section = self.sections[sec]
            for x1 in range(16):
                for y1 in range(16):
                    for z1 in range(16):
                        if string in section.get_block((x1, y1, z1)).state.name:
                            results.append((
                                (x1 + self.xpos * 16, y1 + sec * 16, z1 + self.zpos * 16), 
                                section.get_block((x1, y1, z1))
                            ))
        return results

    # Blockstates are packed based on the number of values in the pallet. 
    # This selects the pack size, then splits out the ids
    def unpack(raw_nbt):
        sections = {}
        for section in raw_nbt.get('Level').get('Sections').children:
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

        return sections

    def pack(self):
        new_sections = nbt.ListTag('Sections', nbt.CompoundTag.clazz_id, children=[
            self.sections[sec].serialize() for sec in self.sections
        ])
        self.raw_nbt.get('Level').add_child(new_sections)

        return self.raw_nbt

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

    def __str__(self):
        return "Chunk(" + str(self.xpos) + "," + str(self.zpos) + ")"

class World:
    def __init__(self, file_name, save_location=''):
        self.file_name = file_name
        self.save_location = save_location
        self.chunks = {}

    def __enter__(self):
        return self
    
    def __exit__(self, typ, val, trace):
        pass

    def get_block(self, block_pos):
        chunk_pos = self._get_chunk(block_pos)
        chunk = self.get_chunk(chunk_pos)
        return chunk.get_block(block_pos)

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
            Chunk.unpack(data),
            data
        )
        return chunk

    def _get_region_file(self, chunk_pos):
        return 'r.' + '.'.join([str(x) for x in self._get_region(chunk_pos)]) + '.mca'


    def _get_chunk(self, block_pos):
        return (math.floor(block_pos[0] / 16), math.floor(block_pos[2] / 16))

    def _get_region(self, chunk_pos):
        return (math.floor(chunk_pos[0] / 32), math.floor(chunk_pos[1] / 32))
