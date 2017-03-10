import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import radon as rn
import numpy as np
from PIL import Image,ImageTk
from skimage import data, color, measure
from tkinter import *
from tkinter import filedialog


step = np.pi/180
detectorsNumber = 35
detectorWidth = np.pi/6

def main():
    # path = filedialog.askopenfilename()
    inData = data.imread("input.png", as_grey=True)

    plt.subplot(2, 2, 1)
    plt.title("Original image")
    plt.imshow(inData, cmap='gray')

    plt.subplot(2, 2, 2)
    plt.xlabel("Emiter/detector rotation")
    plt.ylabel("Number of receiver")
    plt.title("Radon transform image")

    radonImage = rn.radonTransform(inData)
    plt.imshow(radonImage, cmap='gray')

    # radonImage = rn.radonTransform(inData,[0])
    # for i in range(1,180):
    #    radonImage = rn.radonTransform(inData,[i],output=radonImage)
    #    plt.imshow(radonImage,cmap='gray')

    inverseRadonImage = rn.inverseRadonTransform(radonImage)

    plt.subplot(2, 2, 3)
    plt.title("Inverse Radon transform image")
    plt.imshow(inverseRadonImage, cmap='gray')

    filterImage = rn.filter(inverseRadonImage)
    plt.subplot(2, 2, 4)
    plt.title("Filtered image")
    plt.imshow(filterImage, cmap='gray')

    plt.show()


if __name__ == "__main__":
    main()

def mainPanel():
    global mainPanel,imagePanel
    mainPanel
    root = Tk()
