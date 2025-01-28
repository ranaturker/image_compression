from PIL import *
from PIL import Image
import numpy as np

def main():
    img = readPILimg()
    arr = PIL2np(img)

    my_filter = np.array([[-1, 0, 1 ], [-1, 0, 1 ], [-1, 0, 1]])
    im_out = convolve(arr,my_filter)
    im_out = threshold(im_out, 60, 0,100)
    new_img = np2PIL(im_out)
    new_img.show()

def readPILimg():
    img = Image.open(r"/Users/ranaturker/Desktop/small_image61.png")
    img.show()
    img_gray = color2gray(img)
    img_gray.show()
    #img_gray.save('/Users/gokmen/Dropbox/vision-python/images/brick-house-gs','png')
    #new_img = img.resize((256,256))
    #new_img.show()
    return img_gray

def color2gray(img):
    img_gray = img.convert('L')
    return img_gray

def PIL2np(img):
    nrows = img.size[0]
    ncols = img.size[1]
    print("nrows, ncols : ", nrows,ncols)
    imgarray = np.array(img.convert("L"))
    return imgarray

def np2PIL(im):
    print("size of arr: ",im.shape)
    img = Image.fromarray(np.uint8(im))
    return img

def convolve(im,filter):
    (nrows, ncols) = im.shape
    (k1,k2) = filter.shape
    k1h = int((k1 -1) / 2)
    k2h = int((k2 -1) / 2)
    im_out = np.zeros(shape = im.shape)
    print("image size , filter size ", nrows, ncols, k1, k2)
    for i in range(1, nrows - 1):
        for j in range(1, ncols - 1):
            sum = 0.
            for l in range(-k1h, k1h + 1):
                for m in range(-k2h, k2h + 1 ):
                    sum += im[i - l][j - m] * filter[l][m]
            im_out[i][j] = sum
    return im_out
def threshold(im,T, LOW, HIGH):
    (nrows, ncols) = im.shape
    for i in range(nrows):
        for j in range(ncols):
            if abs(im[i][j]) <  T :
                im[i][j] = LOW
            else:
                im[i][j] = HIGH
    return im



if __name__=='__main__':
    main()