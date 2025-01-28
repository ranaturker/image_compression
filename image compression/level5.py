from PIL import Image
import numpy as np
import struct
img = Image.open(r"/Users/ranaturker/Desktop/small_image.png").convert('L')
img_arr = np.asarray(img)

# row-wise differences
row_diff = np.diff(img_arr, axis=1)

# column-wise differences
col_diff = np.vstack((np.zeros((1, img_arr.shape[1])), np.diff(img_arr, axis=0)))

row_diff = np.hstack((np.zeros((img_arr.shape[0], 1)), row_diff))
diff_img = row_diff + col_diff

# difference image
from matplotlib import pyplot as plt
plt.imshow(diff_img, cmap='gray')
plt.show()

# print the non zero values and their positions
for i in range(1, diff_img.shape[0]):
    for j in range(1, diff_img.shape[1]):
        if diff_img[i,j] != 0:
            print(f"Non-zero value at position ({i}, {j}) with value {diff_img[i,j]}")

from collections import defaultdict

# make LZW dictionary
dictionary = defaultdict(int)
for i in range(diff_img.shape[0]):
    for j in range(diff_img.shape[1]):
        if diff_img[i,j] != 0:
            if diff_img[i,j] not in dictionary:
                dictionary[diff_img[i,j]] = len(dictionary)

# encoding difference image with LZW
encoded_diff_img = [dictionary[diff_img[0,0]]]
for i in range(1, diff_img.shape[0] * diff_img.shape[1]):
    current_value = diff_img.flatten()[i]
    previous_value = diff_img.flatten()[i-1]
    if current_value in dictionary:
        encoded_diff_img.append(dictionary[current_value])
        dictionary[previous_value * 256 + current_value] = len(dictionary)
    else:
        encoded_diff_img.append(dictionary[previous_value * 256 + current_value])
        dictionary[current_value] = len(dictionary)

# pack the encoded values into bytes
packed_values = [struct.pack('B', x) for x in encoded_diff_img]

# packed bytes into a bytearray
encoded_diff_img = bytearray(b''.join(packed_values))

with open('compressed_file.lzw', 'wb') as f:
    f.write(encoded_diff_img)
import math

# entropy
symbol_counts = {}
total_symbols = len(encoded_diff_img)
for symbol in encoded_diff_img:
    if symbol not in symbol_counts:
        symbol_counts[symbol] = 0
    symbol_counts[symbol] += 1

entropy = 0
for count in symbol_counts.values():
    probability = count / total_symbols
    entropy -= probability * math.log2(probability)

# average code length
average_code_length = 0
for count in symbol_counts.values():
    probability = count / total_symbols
    average_code_length += probability * math.log2(probability)
average_code_length *= -1

# size of compressed file
compressed_file_size = len(encoded_diff_img)

# compression ratio
original_file_size = img_arr.size * img_arr.itemsize
compression_ratio = original_file_size / compressed_file_size

# Print results
print(f"Entropy: {entropy:.2f}")
print(f"Average code length: {average_code_length:.2f} bits")
print(f"Size of compressed file: {compressed_file_size} bytes")
print(f"Compression ratio: {compression_ratio:.2f}")

import struct

# read the compressed file
with open('compressed_file.lzw', 'rb') as f:
    compressed_data = f.read()

# regulate LZW dictionary
dictionary = {}
for i in range(256):
    dictionary[i] = bytes([i])

index = 256
prev_code = None
decoded_data = bytearray()

# redintegrate the difference image from the compressed data
for byte in compressed_data:
    code = byte
    if prev_code is not None:
        if code in dictionary:
            decoded_data += dictionary[code]
            dictionary[index] = dictionary[prev_code] + dictionary[code][:1]
            index += 1
        else:
            decoded_data += dictionary[prev_code] + dictionary[prev_code][:1]
            dictionary[index] = dictionary[prev_code] + dictionary[prev_code][:1]
            index += 1
    prev_code = code

# redintegrate the original version from differences
diff_img = np.zeros((img_arr.shape[0], img_arr.shape[1]), dtype=np.int16)
current_row = 0
current_col = 0
for byte in decoded_data:
    diff_img[current_row, current_col] = byte - 128
    current_col += 1
    if current_col == img_arr.shape[1]:
        current_row += 1
        current_col = 0

row_diff = diff_img - np.hstack((np.zeros((diff_img.shape[0], 1)), diff_img[:, :-1]))
col_diff = diff_img - np.vstack((np.zeros((1, diff_img.shape[1])), diff_img[:-1, :]))
img_arr_restored = np.zeros((img_arr.shape[0], img_arr.shape[1]), dtype=np.uint8)

for i in range(img_arr.shape[0]):
    for j in range(img_arr.shape[1]):
        img_arr_restored[i,j] = min(255, max(0, img_arr[i,j] + row_diff[i,j] + col_diff[i,j]))


from matplotlib import pyplot as plt
plt.imshow(img_arr_restored, cmap='gray')
plt.show()
import cv2

# save the restored image as a PNG file
cv2.imwrite('restored_image.png', img_arr_restored)
import matplotlib.pyplot as plt


plt.subplot(121)
plt.imshow(img_arr, cmap='gray')
plt.title('Original Image')


plt.subplot(122)
plt.imshow(img_arr_restored, cmap='gray')
plt.title('Restored Image')

plt.show()