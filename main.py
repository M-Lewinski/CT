import matplotlib.pyplot as plt
import radon as rn
from skimage import data

step = 0.5
detectorsNumber = 100
detectorWidth = 180
filter=True

def main():
    inData = data.imread("input.png", as_grey=True)

    plt.subplot(2, 2, 1)
    plt.title("Original image")
    plt.imshow(inData, cmap='gray')

    plt.subplot(2, 2, 2)
    plt.xlabel("Emiter/detector rotation")
    plt.ylabel("Number of receiver")
    plt.title("Radon sinogram")

    sinogram = rn.radonTransform(inData, stepSize=step, detectorsNumber=detectorsNumber, detectorsWidth=detectorWidth)
    plt.imshow(sinogram, cmap='gray', extent=[0,180,len(sinogram),0], interpolation=None)

    if filter: sinogram = rn.filterSinogram(sinogram)


    inverseRadonImage = rn.inverseRadonTransform(sinogram, stepSize=step, detectorsWidth=detectorWidth, outputWidth=256, outputHeight=256)
    plt.subplot(2, 2, 3)
    plt.title("Inverse Radon transform image")
    plt.imshow(inverseRadonImage, cmap='gray')

    plt.show()


if __name__ == "__main__":
    main()
