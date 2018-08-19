from __future__ import print_function
from random import randint, shuffle
import sys
from struct import unpack, pack as pk
from io import BytesIO as BIO
import lzwlib

up = lambda *args: unpack(*args)[0]


def parse_gif_header(input_file):
    assert input_file.read(3) == 'GIF', ''
    assert input_file.read(3) == '89a', ''
    screen_width, screen_height = unpack('HH', input_file.read(4))

    assert 32 <= screen_width <= 500, ''
    assert 32 <= screen_height <= 500, ''
    logflags = up('B', input_file.read(1))

    # the file has to contain the Global Color Table Flag
    assert logflags & 0x80, ''

    size_count = logflags & 0x07

    # global color table count
    gct_count = 2**(size_count+1)
    assert 4 <= gct_count <= 256, ''

    bgcoloridx = up('B', input_file.read(1))
    relative = 1
    input_file.seek(1, relative) # skip aspect ratio
    clrs = []
    for i in xrange(gct_count):
        clr = (up('B', input_file.read(1)), up('B', input_file.read(1)), up('B', input_file.read(1)))
        clrs.append(clr)

    assert len(clrs) > bgcoloridx, ''
    return clrs, bgcoloridx, size_count, screen_height, screen_width


class BlockType(object):
    ImageDescriptor = 0
    GraphicsControlExtension = 1
    EA = 2
    CommentBlock = 3
    ET = 4


def yield_blocks(f):
    rb = f.read(1)
    b = up('B', rb)

    while b != 0x3B:  # while it is not the end of the Gif file
        buf = ''
        buf += rb
        if b == 0x2c:  # Local Image Descriptor
            nbuf = f.read(2*4)  # size info
            eb = f.read(1)  # packed byte
            assert (up('B', eb) & 0x03) == 0, ''  # assert global table colors, and interlaced image
            nbuf += eb

            nbuf += f.read(1)
            nbuf += read_subblocks_with_length(f)
            block_type = BlockType.ImageDescriptor
        elif b == 0x21:  # extension block
            rb = f.read(1)
            buf += rb
            b = up('B', rb)

            if b == 0xF9:  # graphics control extension block
                nbuf = f.read(1)
                blksize = up('B', nbuf)
                nbuf += f.read(blksize)
                nbuf += f.read(1)
                assert nbuf[-1] == '\x00', ''
                block_type = BlockType.GraphicsControlExtension
            elif b in [0xFF, 0x01]:  # Plain Text Extension or Application Extension block
                nbuf = f.read(1)
                blksize = up('B', nbuf)
                nbuf += f.read(blksize)
                nbuf += read_subblocks_with_length(f)

                block_type = (b+3) & 0x0F
            elif b == 0xFE:  # Comment Block
                nbuf = read_subblocks_with_length(f)

                block_type = BlockType.CommentBlock
            else:
                raise Exception("unsupprted thing @{}".format(f.tell()))

        buf += nbuf

        yield block_type, buf
        rb = f.read(1)
        b = up('B', rb)

    yield None, '\x3B'

    raise StopIteration


def create_subblocks_with_buffer(buf):
    blockcount = len(buf)/0xFF
    blockcount += 1 if len(buf) % 0xFF else 0

    blocks = [
        pk('B', len(subblock))+subblock for subblock in [
            buf[i:0xFF+i] for i in xrange(0, blockcount*0xFF, 0xFF)
        ]
    ]

    return ''.join(blocks) + '\x00'


def read_subblocks_without_length(bf):
    combined_buf = ''
    while True:
        cb = ord(bf.read(1))
        if not cb:
            break

        combined_buf += bf.read(cb)
    return combined_buf


def read_subblocks_with_length(f):
    sbx = ''
    while True:
        rcb = f.read(1)
        sbx += rcb
        if rcb == '\x00':
            break

        cb = up('B', rcb)
        blk = f.read(cb)
        sbx += blk

    return sbx


def generate_divisors(char_index):
    import math
    for i in xrange(1, int(math.sqrt(char_index) + 1)):
        if char_index % i == 0:
            yield i


def decode_is_upper(tdix):
    return tdix % 2 == 1


def decode_char_index(w, h, x, y):
    if x == 0 and y == 0:
        return w * h
    if x == 0 and y == 1:
        return h >> 2
    if x == 1:
        return y >> 1

    assert False, "Wtf? values are: (w={0}, h={1}, x={2}, y={3})".format(width, height, x, y)


def encode_char_index(char_index, image_width, image_height):
    if char_index < 0x08:
        if char_index % 2 == 1:  # If the number is odd
            output_x = 0
            output_y = 1
            output_height = char_index << 2
            output_width = randint(4, image_width - 1)
        else:
            output_x = 1
            output_y = char_index << 1
            output_width = randint(4, image_width / 2)
            output_height = randint(4, image_height / 3)
    else:
        ds = list(generate_divisors(char_index))
        output_x = 0
        output_y = 0
        shuffle(ds)

        # put a random divisor
        output_height = ds[0]
        assert char_index % output_height == 0
        output_width = char_index / output_height

    return output_x, output_y, output_width, output_height


def encode_char(char_index, char_is_upper, image_width, image_height, global_color_table_last_index, d=3):
    # if idx % 2 == 0 char is lower
    idx = randint(0, (global_color_table_last_index - 1) / 2) * 2 + char_is_upper
    x, y, w, h = encode_char_index(char_index, image_width, image_height)
    return write_character_blocks(d, w, h, x, y, idx)


def get_hiding_values(flag):
    flag_upper_set = list(set(flag.upper()))
    shuffle(flag_upper_set)
    flag_upper_str = ''.join(flag_upper_set)
    assert len(flag_upper_str) <= 2**6, ''
    return flag_upper_str, [(flag_upper_str.index(c.upper()), int(c.isupper())) for c in flag]


def hide_flag(input_file, flag, output_file):
    global_colors, bgcoloridx, size_count, image_height, image_width = parse_gif_header(input_file)
    flag_unique_chars, flag_indexed_repr = get_hiding_values(flag)
    hdr_end = input_file.tell()
    input_file.seek(0)
    output_file.write(input_file.read(hdr_end))
    fc = 0

    # Add a comment block
    output_file.write('\x21\xFE')
    output_file.write(create_subblocks_with_buffer('RDBNB' + flag_unique_chars))
    output_file.flush()

    for block_type, block_buffer in yield_blocks(input_file):
        print('.', end='')
        if block_type == BlockType.CommentBlock:
            continue
        if block_type == BlockType.GraphicsControlExtension:
            if flag_indexed_repr:
                delay = up('<H', block_buffer[4:6])
                assert delay >= 6
                # Slow the delay
                block_buffer = block_buffer[:4] + pk('<H', delay - 3) + block_buffer[6:]
            output_buffer = block_buffer

        elif block_type == BlockType.ImageDescriptor:
            fc += 1
            total_raw_blocks_data = ''
            block_bio = BIO(block_buffer)
            image_descriptor_header = block_bio.read(10)

            LZWMinimumCodeSize = ord(block_bio.read(1))
            total_raw_blocks_data = read_subblocks_without_length(block_bio)

            indices, _ = lzwlib.Lzwg.decompress(
                total_raw_blocks_data, LZWMinimumCodeSize)

            xxx = unpack('<B H H H H B', image_descriptor_header)

            cmprs, codes = lzwlib.Lzwg.compress(
                indices, LZWMinimumCodeSize)

            if flag_indexed_repr:
                char_index, char_is_upper = flag_indexed_repr.pop(0)
                output_buffer += encode_char(char_index, char_is_upper,
                                             image_width, image_height, len(global_colors) - 1)
        else:
            output_buffer = block_buffer

        output_file.write(output_buffer)
    output_file.flush()
    assert not flag_indexed_repr, ''

    return 0


def read_char_map(input_file):
    assert '\x21\xFE' == input_file.read(2), 'Missing comment block'
    s = read_subblocks_without_length(input_file)
    assert s.startswith('RDBNB'), 'missing map in the comment block'
    s = s[len('RDBNB'):]
    assert s, "empty map!"
    return s

# The index of the character is hidden in x or y or w or h
# The is_upper is hidden in the transparent_color_index
def write_character_blocks(delay, w, h, x, y, transparent_color_index):

    assert 0 <= transparent_color_index <= 255
    assert 0 <= delay < 2**16

    indices = [transparent_color_index] * (w * h)
    buf = BIO('')

    # write the graphics control block
    buf.write('\x21\xF9\x04\x05')
    buf.write(pk('H', delay))
    buf.write(pk('B', transparent_color_index))
    buf.write('\x00')  # Terminator

    # after it, write a local image descriptor block
    buf.write('\x2c')
    buf.write(pk('H', x))
    buf.write(pk('H', y))
    buf.write(pk('H', w))
    buf.write(pk('H', h))
    buf.write('\x00')

    LZWMinimumCodeSize = 8

    # Compress the
    cmprs, _ = lzwlib.Lzwg.compress(
        indices, LZWMinimumCodeSize)

    obuf = pk('B', LZWMinimumCodeSize) + create_subblocks_with_buffer(cmprs)

    buf.write(obuf)
    buf.seek(0)
    return buf.read()


def extract_flag(input_file):
    parse_gif_header(input_file)
    char_map = read_char_map(input_file)

    delays = []
    char_values = []
    fc = 0

    blocks = list(yield_blocks(input_file))

    for block_index, (block_type, block_buffer) in enumerate(blocks):
        if block_type != BlockType.GraphicsControlExtension:
            continue

        delay = up('<H', block_buffer[4:6])

        if delay == 7:
            break
        if delay == 4:
            continue

        tidx = up('B', block_buffer[6])
        block_type, block_buffer = blocks[block_index+1]

        x = up('<H', block_buffer[1:3])
        y = up('<H', block_buffer[3:5])
        width = up('<H', block_buffer[5:7])
        height = up('<H', block_buffer[7:9])

        char = char_map[decode_char_index(width, height, x, y)]
        char_is_upper = decode_is_upper(tidx)
        
        if not char_is_upper:
            char = char.lower()

        print(char, end='')

    return 0


if __name__ == '__main__':
    print(extract_flag(open('secret.gif', 'rb')))
