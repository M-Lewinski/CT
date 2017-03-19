import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from skimage import data
import radon as rn

#CHANGE THIS VALUES
step = [20,15]
detectors = [20,40]
detWidth = [30,45,60]

def returnDifference2D(input1, input2):
    if (len(input1) != len(input2)) or (len(input1[0]) != len(input2[0])) : raise NameError("Arrays do not have the same size")
    val = 0
    for X in range(0,len(input1)):
        for Y in range(0, len(input1[0])):
           val += np.power((input1[X,Y]-input2[X,Y]),2)
    return np.sqrt(val)

def testAlgorithm(stepArr, detectorsArr, widthArr, filter, figSaveName):
    result = np.zeros((len(stepArr), len(detectorsArr), len(widthArr)))
    num=0
    all=len(stepArr)*len(detectorsArr)*len(widthArr)
    inData = data.imread("input.png", as_grey=True)

    for S, SVal in enumerate(stepArr):
        for D, DVal in enumerate(detectorsArr):
            for W, WVal in enumerate(widthArr):
                num+=1
                sinogram = rn.radonTransform(inData, stepSize=SVal, detectorsNumber=DVal, detectorsWidth=WVal)
                if filter: sinogram = rn.filterSinogram(sinogram)
                inverseRadonImage = rn.inverseRadonTransform(sinogram, stepSize=SVal, detectorsWidth=DVal, outputWidth=len(inData[0]), outputHeight=len(inData))
                result[S][D][W] = returnDifference2D(inData, inverseRadonImage)
                print("{}. {:.2f}% --- step:{} detectorsNum:{} width:{} result:{}".format(num,(num/all*100),SVal,DVal,WVal,result[S][D][W]))

    # ADD 4D plot visualization and save fig
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # plt.savefig(figSaveName)

    print(result)

    return


def main():
    testAlgorithm(step, detectors, detWidth, False, "output.png")

    return


if __name__ == "__main__":
    main()