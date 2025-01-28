import os

class LZWCoding:
    def __init__(self, path, codelength = 12):
        self.path = path
        self.compressed = []
        self.decompressed = []
        self.codelength = codelength

    def compress(self, uncompressed):


        # LZW dictionary
        dict_size = 256
        dictionary = {chr(i): i for i in range(dict_size)}

        w = ""
        result = []
        for c in uncompressed:
            wc = w + c
            if wc in dictionary:
                w = wc
            else:
                result.append(dictionary[w])

                dictionary[wc] = dict_size
                dict_size += 1
                w = c


        if w:
            result.append(dictionary[w])
        return result

    def get_compressed_data(self, path):
        with open(path, "rb") as file:
            bit_string = ""
            byte = file.read(1)
            while (len(byte) > 0):
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, '0')
                bit_string += bits
                byte = file.read(1)
        return bit_string

    def decompress(self, compressed):

        from io import StringIO
        print("from decompressed: compressed data: ", compressed)
        # LZW dictionary
        dict_size = 256
        dictionary = {i: chr(i) for i in range(dict_size)}

        result = StringIO()
        w = chr(compressed.pop(0))
        result.write(w)
        for k in compressed:
            if k in dictionary:
                entry = dictionary[k]
            elif k == dict_size:
                entry = w + w[0]
            else:
                raise ValueError('Error compressed k: %s' % k)
            result.write(entry)

            dictionary[dict_size] = w + entry[0]
            dict_size += 1

            w = entry
        return result.getvalue()

    def pad_encoded_text(self, encoded_text):
        extra_padding = 8 - len(encoded_text) % 8
        for i in range(extra_padding):
            encoded_text += "0"

        padded_info = "{0:08b}".format(extra_padding)
        print("about padded: ", padded_info)
        encoded_text = padded_info + encoded_text
        return encoded_text

    def get_byte_array(self, padded_encoded_text):
        if (len(padded_encoded_text) % 8 != 0):
            print("sorry, encoded text not padded properly")
            exit(0)

        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i + 8]
            b.append(int(byte, 2))
        return b

    def int_array_to_binary_string(self,int_array):
        import math
        bitstr = ""
        bits = self.codelength
        for num in int_array:
            for n in range(bits):
                if num & (1 << (bits - 1 - n)):
                    bitstr += "1"
                else:
                    bitstr += "0"
        return(bitstr)

    def write_compressed_file(self):
        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + ".bin"
        output_path_2 = filename + "_out.txt"

        with open(self.path, 'r+') as file, open(output_path, 'wb') as output , open(output_path_2, 'w+') as file2:
            text = file.read()
            text = text.rstrip()
            int_encoded = self.compress(text)
            file2.write(str(int_encoded))
            encoded_text = self.int_array_to_binary_string(int_encoded)
            padded_encoded_text = self.pad_encoded_text(encoded_text)
            b = self.get_byte_array(padded_encoded_text)
            output.write(bytes(b))

        print("Compressed")
        file2.close()
        return output_path
#decoder part
    def remove_padding(self, padded_encoded_text):
        padded_info = padded_encoded_text[:8]
        extra_padding = int(padded_info, 2)
        padded_encoded_text = padded_encoded_text[8:]
        encoded_text = padded_encoded_text[:-1 * extra_padding]
        int_codes = []
        for bits in range(0, len(encoded_text),self.codelength):
            int_codes.append(int(encoded_text[bits:bits+self.codelength],2))
        return int_codes

    def decompress_file(self, input_path):
        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + "_decompressed" + ".txt"

        with open(input_path, 'rb') as file, open(output_path, 'w') as output:
            bit_string = ""

            byte = file.read(1)
            while (len(byte) > 0):
                byte = ord(byte)
                print("byte :", byte)
#                bits = bin(byte)[2:].rjust(8, '0')
                bits = bin(byte)[2:].rjust(8, '0')
                bit_string += bits
                byte = file.read(1)
            print()
            encoded_text = self.remove_padding(bit_string)
            print("decompressed_file - encoded integers", encoded_text)
            decompressed_text = self.decompress(encoded_text)

            output.write(decompressed_text)

        print("Decompressed")
        return output_path