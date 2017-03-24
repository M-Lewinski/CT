import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from skimage import data
import radon as rn
import itertools
from multiprocessing import Process

#CHANGE THIS VALUES
step = [45,40,35,30,20,15,10,5,3,2,1,0.5]
detectors = [20,40,50,60,80,100,120,140,160,180]
detWidth = [30,45,60,75,90,105,120,135,150,165,180]

def returnDifference2D(input1, input2):
    if (len(input1) != len(input2)) or (len(input1[0]) != len(input2[0])) : raise NameError("Arrays do not have the same size")
    val = 0
    for X in range(0,len(input1)):
        for Y in range(0, len(input1[0])):
           val += np.power((input1[X,Y]-input2[X,Y]),2)
    return np.sqrt(val)

def testAlgorithm(stepArr, detectorsArr, widthArr, filter, figSaveName, prefix=""):
    result = np.zeros((len(stepArr), len(detectorsArr), len(widthArr)))
    num=0
    all=len(stepArr)*len(detectorsArr)*len(widthArr)
    inData = data.imread("input.png", as_grey=True)
    inData = inData/max( inData.flatten() )

    for S, SVal in enumerate(stepArr):
        for D, DVal in enumerate(detectorsArr):
            for W, WVal in enumerate(widthArr):
                num+=1
                sinogram = rn.radonTransform(inData, stepSize=SVal, detectorsNumber=DVal, detectorsWidth=WVal)
                if filter: sinogram = rn.filterSinogram(sinogram)
                inverseRadonImage = rn.inverseRadonTransform(sinogram, stepSize=SVal, detectorsWidth=DVal, outputWidth=len(inData[0]), outputHeight=len(inData))

                #plt.imshow(inverseRadonImage, cmap='gray')
                #plt.savefig("test/"+str(SVal)+":"+str(DVal)+":"+str(WVal)+":"+str(filter)+".png")

                result[S,D,W] = returnDifference2D(inData, inverseRadonImage)
                print("{}{}. {:.2f}% --- step:{} detectorsNum:{} width:{} result:{}".format(prefix,num,(num/all*100),SVal,DVal,WVal,result[S,D,W]))

    smart4DPlot(stepArr, detectorsArr, widthArr, result, figSaveName)
    return

def plot2D(X,Y,labelX, figSaveName, labelY="variation"):
    plt.plot(X,Y,'ro')
    plt.xlabel(labelX)
    plt.ylabel(labelY)
    plt.savefig(figSaveName)
    return

def plot3D(X,Y,Z,labelX, labelY, figSaveName, labelZ="variation"):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    cartesian = np.array([ [x,y] for x in X for y in Y ])
    ax.scatter(cartesian[:,0],cartesian[:,1],Z)
    ax.set_xlabel(labelX)
    ax.set_ylabel(labelY)
    ax.set_zlabel(labelZ)
    plt.savefig(figSaveName)
    return

def plot4D(X,Y,Z,A, labelX, labelY, labelZ, figSaveName, labelA="variation"):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    cartesian = np.array([[x, y, z] for x in X for y in Y for z in Z])
    sp = ax.scatter(cartesian[:,0],cartesian[:,1],cartesian[:,2], c=A, cmap=plt.hot())
    ax.set_xlabel(labelX)
    ax.set_ylabel(labelY)
    ax.set_zlabel(labelZ)
    bar = plt.colorbar(sp)
    bar.set_label(labelA)
    plt.savefig(figSaveName)
    return

def smart4DPlot(X, Y, Z, data, figSaveName, labelX="Step", labelY="Number of detectors", labelZ="Detectors width"):
    if(len(X)==1 and len(Y)==1 and len(Z)>1 ):
        plot2D(Z, data[0,0,:], labelZ, figSaveName)
        return
    if(len(X)==1 and len(Y)>1 and len(Z)==1 ):
        plot2D(Y, data[0,:,0], labelY, figSaveName)
        return
    if(len(X)>1 and len(Y)==1 and len(Z)==1 ):
        plot2D(X, data[:,0,0], labelX, figSaveName)
        return
    if(len(X)>1 and len(Y)>1 and len(Z)==1):
        plot3D(X,Y,data[:,:,0], labelX, labelY, figSaveName)
        return
    if (len(X)==1 and len(Y) > 1 and len(Z)>1):
        plot3D(Y,Z,data[0,:,:], labelY, labelZ, figSaveName)
        return
    if (len(X)>1 and len(Y)==1 and len(Z)>1):
        plot3D(X,Z,data[:,0,:], labelX, labelZ, figSaveName)
        return
    plot4D(X,Y,Z,data,labelX,labelY,labelZ, figSaveName)
    return

def runInParallel(*fns):
  proc = []
  for fn in fns:
    p = Process(target=fn)
    p.start()
    proc.append(p)
  for p in proc:
    p.join()

def main():
    def test1():
        testAlgorithm(step, detectors, detWidth, True, "main4DFilter.pdf", prefix="test1: ")
    def test2():
        testAlgorithm(step, detectors, detWidth, False, "main4DNoFilter.pdf", prefix="test2: ")
    def test3():
        testAlgorithm([1], detectors, detWidth, True, "main3DFilterStep1.pdf", prefix="test3: ")
    def test4():
        testAlgorithm([1], detectors, detWidth, False, "main4DNoFilterStep1.pdf", prefix="test4: ")
    def test5():
        testAlgorithm(step, [100], detWidth, True, "main3DFilterDetectors100.pdf", prefix="test5: ")
    def test6():
        testAlgorithm(step, [100], detWidth, False, "main4DNoFilterDetectors100.pdf", prefix="test6: ")
    def test7():
        testAlgorithm(step, detectors, [140], True, "main3DFilterWidth140.pdf", prefix="test7: ")
    def test8():
        testAlgorithm(step, detectors, [140], False, "main4DNoFilterWidth140.pdf", prefix="test8: ")

    runInParallel(test1,test2, test3, test4, test5, test6, test7, test8)
    return


if __name__ == "__main__":
    main()
