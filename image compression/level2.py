import struct
import os
import math

# lzw dictionary
def compress_lzw(data):
    dictionary_size = 256
    dictionary = {chr(i): i for i in range(dictionary_size)}
    compressed_data = []
    current_sequence = ""
    for symbol in data:
        symbol = chr(symbol)
        sequence = current_sequence + symbol
        if sequence in dictionary:
            current_sequence = sequence
        else:
            compressed_data.append(dictionary[current_sequence])
            dictionary[sequence] = dictionary_size
            dictionary_size += 1
            current_sequence = symbol
    if current_sequence:
        compressed_data.append(dictionary[current_sequence])
    return compressed_data

with open("/Users/ranaturker/Desktop/small_image.png", 'rb') as f:
    data = f.read()

# convert grayscale pixel values
pixels = []
for i in range(0, len(data), 1):
    pixel = struct.unpack('B', data[i:i+1])[0]
    pixels.append(pixel)

# Compress part with LZW
compressed_pixels = compress_lzw(pixels)

# compressed data to bytes
compressed_data = bytearray()
for i in range(0, len(compressed_pixels), 2):
    byte = (compressed_pixels[i] << 4) | compressed_pixels[i+1]
    compressed_data.append(pixel)

# create compress image
with open('compressed_image.bin', 'wb') as f:
    f.write(compressed_data)

# entropy of the original version
entropy = 0
total_pixels = len(pixels)
histogram = [0]*256
for pixel in pixels:
    histogram[pixel] += 1
for count in histogram:
    if count > 0:
        probability = count / total_pixels
        entropy -= probability * math.log2(probability)

# average code length for the compressed version
total_bits = len(compressed_data) * 8
average_code_length = total_bits / total_pixels

# size of the compressed version
compressed_file_size = os.path.getsize('compressed_image.bin')

# compression ratio
compression_ratio = len(data) / compressed_file_size

def decompress_lzw(data):
    dictionary_size = 256
    dictionary = {i: chr(i) for i in range(dictionary_size)}
    current_sequence = chr(data[0])
    decompressed_data = [current_sequence]
    for symbol in data[1:]:
        if symbol in dictionary:
            sequence = dictionary[symbol]
        elif symbol == dictionary_size:
            sequence = current_sequence + current_sequence[0]
        else:
            raise ValueError('Bad compressed k: %s' % symbol)
        decompressed_data.append(sequence)
        dictionary[dictionary_size] = current_sequence + sequence[0]
        dictionary_size += 1
        current_sequence = sequence
    return ''.join(decompressed_data)

# read compressed data
with open('compressed_image.bin', 'rb') as f:
    compressed_data = f.read()

# Decompress part with LZW algorithm
decompressed_pixels = decompress_lzw(compressed_data)

# create grayscale pixel values for decompressed version
pixels = []
for symbol in decompressed_pixels:
    pixels.append(ord(symbol))


with open('restored_image.png', 'wb') as f:
    f.write(bytearray(pixels))

# compare original file and the restored version
with open("/Users/ranaturker/Desktop/small_image.png", 'rb') as f:
    original_data = f.read()

if original_data == bytearray(pixels):
    print("Original image and the restored version are same.")
else:
    print("Original image and the restored version are not same.")
# Print the results
print(f"Entropy: {entropy:.4f}")
print(f"Average Code Length: {average_code_length:.4f} bits")
print(f"Compressed File Size: {compressed_file_size} bytes")
print(f"Compression Ratio: {compression_ratio:.4f}")

