from level1 import LZWCoding
import os
import sys

path = "/Users/ranaturker/Desktop/rana.txt"

l = LZWCoding(path, 12)
output_path= l.write_compressed_file()
print("output path: ",output_path)
decom_path = l.decompress_file(output_path)
print("Path of decompressed file: " + decom_path)
original_size = os.path.getsize("/Users/ranaturker/Desktop/rana.txt")
compressed_size = os.path.getsize(output_path)
code_length = compressed_size * 8 / original_size * 12
print("Code length: {:.2f} bits/symbol".format(code_length))
compression_ratio = original_size / compressed_size
print("Compression ratio: {:.2f}".format(compression_ratio))

# read original file
with open("/Users/ranaturker/Desktop/rana.txt", "r") as f:
    original_text = f.read()

# read decompressed file
with open(decom_path, "r") as f:
    decompressed_text = f.read()

# compare them
if original_text == decompressed_text:
    print("Original text and decompressed version match. ")
else:
    print("Error for the decompression part. Original text and decompressed version do not match. ")