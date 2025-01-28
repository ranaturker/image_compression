from PIL import Image
from io import BytesIO
import struct
import math

# read the image file
img = Image.open("/Users/ranaturker/Desktop/small_image61.png")

# if image is not grayscale, make it
if img.mode != "L":
    img = img.convert("L")

# make the difference image
diff_img = Image.new("L", img.size)
for y in range(img.size[1]):
    for x in range(1, img.size[0]):
        diff = img.getpixel((x, y)) - img.getpixel((x-1, y))
        diff_img.putpixel((x, y), diff)

# column-wise differences
col_diffs = []
for y in range(1, diff_img.size[1]):
    diff = diff_img.getpixel((0, y)) - diff_img.getpixel((0, y-1))
    col_diffs.append(diff)

# LZW dictionary for difference image
dictionary = {}
for i in range(256):
    dictionary[struct.pack("B", i)] = i
next_code = 256
compressed_data = []
current_code = col_diffs[0]
for code in col_diffs[1:]:
    if struct.pack("h", current_code) + struct.pack("B", code) in dictionary:
        current_code = dictionary[struct.pack("h", current_code) + struct.pack("B", code)]
    else:
        compressed_data.append(current_code)
        dictionary[struct.pack("h", current_code) + struct.pack("B", code)] = next_code
        next_code += 1
        current_code = code
compressed_data.append(current_code)

# compressed data to bytes
compressed_data_bytes = bytearray()
for code in compressed_data:
    compressed_data_bytes += struct.pack("H", code)
with open("small_image_compressed.bin", "wb") as f:
    f.write(compressed_data_bytes)

# entropy, average code length, size of compressed file, and compression ratio
entropy = 0
for count in dictionary.values():
    probability = count / len(col_diffs)
    # Calculate entropy
    entropy = 0
    for count in dictionary.values():
        probability = count / len(col_diffs)
        if probability != 0:
            entropy -= probability * math.log2(probability)

average_code_length = len(compressed_data_bytes) * 8 / len(col_diffs)
compressed_file_size = len(compressed_data_bytes)
compression_ratio = len(col_diffs) / len(compressed_data_bytes)

print(f"Entropy: {entropy}")
print(f"Average code length: {average_code_length}")
print(f"Compressed file size: {compressed_file_size} bytes")
print(f"Compression ratio: {compression_ratio:.2f}")

# read the compressed file
with open("small_image_compressed.bin", "rb") as f:
    compressed_data_bytes = f.read()

# make LZW dictionary
dictionary = {}
for i in range(256):
    dictionary[i] = struct.pack("B", i)
next_code = 256
decompressed_data = []
current_code = struct.unpack("h", compressed_data_bytes[:2])[0]
decompressed_data.append(current_code)
previous_code = current_code
for i in range(2, len(compressed_data_bytes), 2):
    current_code = struct.unpack("h", compressed_data_bytes[i:i+2])[0]
    if current_code in dictionary:
        entry = dictionary[current_code]
    else:
        entry = dictionary[previous_code] + dictionary[previous_code][0:1]
    decompressed_data.append(entry)
    dictionary[next_code] = dictionary[previous_code] + entry[0:1]
    next_code += 1
    previous_code = current_code

# regulate the difference image from the compressed data
dictionary = {}
for i in range(256):
    dictionary[i] = struct.pack("B", i)
next_code = 256
col_diffs = []
current_code = struct.unpack("h", compressed_data_bytes[:2])[0]
previous_code = current_code
col_diffs.append(current_code)
for i in range(2, len(compressed_data_bytes), 2):
    current_code = struct.unpack("h", compressed_data_bytes[i:i+2])[0]
    if current_code in dictionary:
        entry = dictionary[current_code]
    else:
        entry = dictionary[previous_code] + dictionary[previous_code][0:1]
    col_diffs.append(entry[-1])
    dictionary[next_code] = dictionary[previous_code] + entry[0:1]
    next_code += 1
    previous_code = current_code


# regulate the original image from the differences
original_img = Image.new("L", img.size)
for y in range(img.size[1]):
    original_img.putpixel((0, y), img.getpixel((0, y)))
    for x in range(1, img.size[0]):
        diff = diff_img.getpixel((x, y))
        original_value = original_img.getpixel((x-1, y)) + diff
        original_img.putpixel((x, y), original_value)

# restored image
original_img.save("restored_image.png")

# open images
original_img = Image.open("/Users/ranaturker/Desktop/small_image61.png")
restored_img = Image.open("restored_image.png")

# size of the images
width, height = original_img.size

# loop for each pixel,  compare the values
for x in range(width):
    for y in range(height):
        if original_img.getpixel((x, y)) != restored_img.getpixel((x, y)):
            print("Images are not identical")
            break
    else:
        continue
    break
else:
    print("Images are identical")