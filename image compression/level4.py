import numpy as np
from PIL import Image

def lzw_compress(data):
    dictionary = {}
    index = 256
    for i in range(index):
        dictionary[chr(i)] = i

    w = ''
    result = []
    for c in data:
        wc = w + chr(c)
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            dictionary[wc] = index
            index += 1
            w = chr(c)
    if w:
        result.append(dictionary[w])

    return np.array(result)

# load the image
image = Image.open(r"/Users/ranaturker/Desktop/small_image.png").convert('L')

# image to a numpy array
data = np.array(image)

# compress
compressed_data = lzw_compress(data.flatten().astype(np.uint8).tobytes())

with open("compressed.dat", "wb") as f:
    f.write(compressed_data)

# compression metrics
compressed_size = len(compressed_data)
original_size = data.size * data.itemsize
compression_ratio = original_size / compressed_size

p = np.bincount(data.flatten(), minlength=256).astype(np.float64)
p /= p.sum()
mask = p > 0
b_entropy = -np.sum(p[mask] * np.log2(p[mask]))

num_symbols = len(np.unique(data))
if num_symbols > 1:
    avg_code_length = np.ceil(np.log2(num_symbols))
else:
    avg_code_length = 0


print("Original size:", original_size)
print("Compressed size:", compressed_size)
print("Compression ratio:", compression_ratio)
print("Entropy:", b_entropy)
print("Average code length:", avg_code_length)