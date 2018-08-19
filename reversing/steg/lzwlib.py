from io import BytesIO as BIO


class Bitstream(object):
    def __init__(self, buf=None, raw=None, bits=None):
        self.bytes = buf or BIO(raw)
        self.bits = bits or []

    def __len__(self):
        curr = self.bytes.tell()
        last = self.bytes.seek(0, 2)
        self.bytes.seek(curr)
        total = len(self.bits) + (last - curr)*8
        return total

    def _write_bits(self, newbits):
        self.bits += newbits

    def write(self, v, count):
        newbits = [1 if v & (1 << i) else 0 for i in range(count)]
        self._write_bits(newbits)

    def _read_bits(self, count):
        bytes_for_bits = count/8 + (1 if (count % 8) else 0)

        raw_bytes = self.bytes.read(bytes_for_bits)
        for b in raw_bytes:
            self.bits += [1 if ord(b) & (1 << i) else 0 for i in range(8)]

    def _makeint(self, bitcount):
        assert bitcount < 13, bitcount
        x = 0
        for i in xrange(bitcount):
            b = self.bits.pop(0)
            x |= (b << i)

        return x

    def readByte(self):
        return chr(self.read(8))

    def read(self, bitcount):
        current_bit_count = len(self.bits)
        if current_bit_count < bitcount:
            self._read_bits(bitcount - current_bit_count)

        return self._makeint(bitcount)


class Lzwg(object):

    @classmethod
    def extract_info_from_imagedatadescriptor(cls, buf):
        buf.seek(1+2*4, 1)
        desc_flags = ord(buf.read(1))
        assert desc_flags == 0, 'flags: {:08b}'.format(desc_flags)

        lzw_min_codesize = ord(buf.read(1))
        size = ord(buf.read(1))
        subblocks = []
        while size:
            subblocks.append(buf.read(size))
            size = ord(buf.read(1))

        return lzw_min_codesize, subblocks

    @classmethod
    def _get_initialized_code_table(cls, lzw_min_codesize):
        max_indx = 2**(lzw_min_codesize) - 1 + 2  # 2 for CC and EOI codes
        return [[i] for i in xrange(max_indx + 1)]

    @classmethod
    def decompress(cls, buf, lzw_min_codesize=2):
        can_insert_to_table = True
        index_stream = []
        current_bits_per_code = initial_bits_per_code = lzw_min_codesize+1
        code_table = cls._get_initialized_code_table(lzw_min_codesize)
        bits = Bitstream(raw=buf)
        codes = []
        CLEAR_CODE = len(code_table) - 2
        EOI_CODE = len(code_table) - 1
        assert CLEAR_CODE == bits.read(
            initial_bits_per_code), 'first code is not CC'
        pc = c = bits.read(initial_bits_per_code)
        codes.append(CLEAR_CODE)
        codes.append(c)

        index_stream.extend(code_table[c])
        k = None
        while len(bits):

            c = bits.read(current_bits_per_code)
            codes.append(c)

            if c == CLEAR_CODE:
                code_table = cls._get_initialized_code_table(lzw_min_codesize)
                current_bits_per_code = initial_bits_per_code
                pc = c = bits.read(initial_bits_per_code)
                codes.append(c)
                index_stream.extend(code_table[c])
                can_insert_to_table = True
                continue

            if c == EOI_CODE:
                assert len(bits) == 0 or (len(bits) <= 8 and bits.read(len(bits)
                                                                       ) == 0), '{} left: {}'.format(len(bits), bits.bits)
                break

            if len(code_table) > c:
                index_stream.extend(code_table[c])
                k = code_table[c][:1]
                if can_insert_to_table:
                    code_table.append(code_table[pc] + k)
            else:
                k = code_table[pc][:1]
                index_stream.extend(code_table[pc] + k)
                if can_insert_to_table:
                    code_table.append(code_table[pc] + k)

            if len(code_table) - 1 == (2**current_bits_per_code) - 1:
                if current_bits_per_code < 12:
                    current_bits_per_code += 1
                else:
                    can_insert_to_table = False

            assert current_bits_per_code < 13, 'bad bits per code'

            pc = c

        return index_stream, codes

    @classmethod
    def _compress_indices_using_table(cls, indices, lzw_min_codesize):
        code_table = cls._get_initialized_code_table(lzw_min_codesize)
        CLEAR_CODE = len(code_table) - 2
        EOI_CODE = len(code_table) - 1
        current_bits_per_code = initial_bits_per_code = lzw_min_codesize+1

        yield CLEAR_CODE, current_bits_per_code
        intermediate_index_buffer = [indices[0]]

        for indx in indices[1:]:
            k = indx
            if intermediate_index_buffer + [k] in code_table:
                intermediate_index_buffer.append(k)
            else:
                code_table.append(intermediate_index_buffer+[k])
                new_idx = code_table.index(intermediate_index_buffer)

                yield new_idx, current_bits_per_code
                intermediate_index_buffer = [k]
                k = None

                if len(code_table) == 2**12 - 1-1:
                    yield CLEAR_CODE, current_bits_per_code

                    current_bits_per_code = initial_bits_per_code
                    code_table = cls._get_initialized_code_table(
                        lzw_min_codesize)
                    # code_table.append(intermediate_index_buffer+[k])

            if len(code_table) == 2**current_bits_per_code + 1:
                current_bits_per_code += 1

        yield code_table.index(intermediate_index_buffer), current_bits_per_code
        yield EOI_CODE, current_bits_per_code

    @classmethod
    def compress(cls, indices, lzw_min_codesize=2):
        bits = Bitstream()
        comcodes = []
        cmprsd = ''
        for c, bits_per_code in cls._compress_indices_using_table(indices, lzw_min_codesize):
            comcodes.append(c)
            bits.write(c, bits_per_code)
            while len(bits) >= 8:
                b = bits.readByte()
                cmprsd += b

        if len(bits) > 0:
            assert len(bits) < 8, 'bitstream has more than a byte left!: {}'.format(
                bits.bits)
            bits.write(0, 8-len(bits))
            b = bits.readByte()
            cmprsd += b

        return cmprsd, comcodes
