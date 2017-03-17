import matplotlib.pyplot as plt
import radon as rn
from skimage import data


step = 2
detectorsNumber = 120
detectorWidth = 130

def main():
    inData = data.imread("input.png", as_grey=True)

    plt.subplot(2, 3, 1)
    plt.title("Original image")
    plt.imshow(inData, cmap='gray')

    plt.subplot(2, 3, 2)
    plt.xlabel("Emiter/detector rotation")
    plt.ylabel("Number of receiver")
    plt.title("Radon transform image")

    radonImage = rn.radonTransform(inData, stepSize=step, detectorsNumber=detectorsNumber, detectorsWidth=detectorWidth)
    plt.imshow(radonImage, cmap='gray', extent=[0,180,len(radonImage),0], interpolation=None)
    inverseRadonImage = rn.inverseRadonTransform(radonImage, stepSize=step, detectorsWidth=detectorWidth)
    plt.subplot(2, 3, 4)
    plt.title("Inverse Radon transform image")
    plt.imshow(inverseRadonImage, cmap='gray')



    filteredSinogram = rn.filterSinogram(radonImage)
    plt.subplot(2, 3, 3)
    plt.title("Filtered sinogram")
    plt.imshow(filteredSinogram, cmap='gray', extent=[0,180,len(radonImage),0], interpolation=None)


    inverseRadonFilteredImage = rn.inverseRadonTransform(filteredSinogram, stepSize=step, detectorsWidth=detectorWidth)
    plt.subplot(2, 3, 5)
    plt.title("Inverse filtered Radon transform image")
    plt.imshow(inverseRadonFilteredImage, cmap='gray')

    plt.show()


if __name__ == "__main__":
    main()
