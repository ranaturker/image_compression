import tkinter as tk
from tkinter import filedialog
from PIL import *
from PIL import Image
import numpy as np
from functions import convolve
from functions import threshold
from functions import np2PIL

window = tk.Tk()
window.title("File Selector")

selected_file_label = tk.Label(window, text="")
selected_file_label.pack()

#  function for browse the file
def browse_file():
    file_path = filedialog.askopenfilename()
    selected_file_label.config(text=file_path)
    img = readPILimg(file_path)
    arr = PIL2np(img)

    my_filter = np.array([[-1, 0, 1 ], [-1, 0, 1 ], [-1, 0, 1]])
    im_out = convolve(arr,my_filter)
    im_out = threshold(im_out, 60, 0,100)
    new_img = np2PIL(im_out)
    new_img.show()

    new_img.save(r"/Users/ranaturker/Desktop/processed_image.png")


# button for browse the file
browse_button = tk.Button(window, text="Select Image", command=browse_file)
browse_button.pack()

# exit button
exit_button = tk.Button(window, text="Exit", command=window.destroy)
exit_button.pack()

def readPILimg(file_path):
    img = Image.open(file_path)
    img.show()
    img_gray = color2gray(img)
    img_gray.show()
    img_gray.save(r"/Users/ranaturker/Desktop/gray_image.png") # save the gray image
    return img_gray

def color2gray(img):
    img_gray = img.convert('L')
    return img_gray

def PIL2np(img):
    nrows = img.size[0]
    ncols = img.size[1]
    imgarray = np.array(img.convert("L"))
    return imgarray


window.mainloop()