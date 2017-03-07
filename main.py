import matplotlib.pyplot as plt
import radon as rn
import numpy as np
from skimage import data, color, exposure, measure

step=np.pi/180
detectorsNumber=35
detectorWidth=np.pi/6

def main():
    inData = data.imread("input.png", as_grey=True)
    inData = color.rgb2grey(inData)

    radonImage = rn.radonTransform(inData)
    inverseRadonImage = rn.inverseRadonTransform(radonImage)
    filterImage = rn.filter(inverseRadonImage)




    plt.subplot(2, 2, 1)
    plt.title("Original image")
    plt.imshow(color.gray2rgb(inData))

    plt.subplot(2, 2, 2)
    plt.title("Radon transform image")
    plt.imshow(color.gray2rgb(radonImage))

    plt.subplot(2, 2, 3)
    plt.title("Inverse Radon transform image")
    plt.imshow(color.gray2rgb(inverseRadonImage))

    plt.subplot(2, 2, 4)
    plt.title("Filtered image")
    plt.imshow(color.gray2rgb(filterImage))

    plt.show()

if __name__ == "__main__":
    main()