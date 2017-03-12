import matplotlib.pyplot as plt
import radon as rn
from skimage import data, color, measure

step = 2
detectorsNumber = 100
detectorWidth = 130

def main():
    inData = data.imread("input.png", as_grey=True)

    plt.subplot(2, 2, 1)
    plt.title("Original image")
    plt.imshow(inData, cmap='gray')

    plt.subplot(2, 2, 2)
    plt.xlabel("Emiter/detector rotation")
    plt.ylabel("Number of receiver")
    plt.title("Radon transform image")

    radonImage = rn.radonTransform(inData, stepSize=step, detectorsNumber=detectorsNumber, detectorsWidth=detectorWidth)
    plt.imshow(radonImage, cmap='gray', extent=[0,180,len(radonImage),0], interpolation=None)

    # radonImage = rn.radonTransform(inData,[0])
    # for i in range(1,180):
    #    radonImage = rn.radonTransform(inData,[i],output=radonImage)
    #    plt.imshow(radonImage,cmap='gray')

    inverseRadonImage = rn.inverseRadonTransform(radonImage, stepSize=step, detectorsWidth=detectorWidth, outputHeight=256, outputWidth=256)

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
