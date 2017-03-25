import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from skimage import data
import radon as rn
from multiprocessing import Process

#CHANGE THIS VALUES
step = [45,40,35,30,20,15,10,5,3,2,1,0.5]
detectors = [400,350,300,250,200,150,100,50,25]
detWidth = [30,45,60,75,90,105,120,135,150,165,180]

def returnDifference2D(input1, input2):
    if (len(input1) != len(input2)) or (len(input1[0]) != len(input2[0])) : raise NameError("Arrays do not have the same size")
    val = 0
    for X in range(0,len(input1)):
        for Y in range(0, len(input1[0])):
           val += np.power((input1[X,Y]-input2[X,Y]),2)
    return np.sqrt(val)

def testIterations(step, detectors, width, filter, figSaveName, prefix=""):
    inData = data.imread("input.png", as_grey=True)
    inData = inData/max( inData.flatten() )
    num=0
    stepsArray = np.arange(0, 180, step)
    result = np.zeros(len(stepsArray))
    sinogram = None
    inverseImage = None
    for S, SVal in enumerate(stepsArray):
        num += 1
        sinogram = rn.radonTransform(inData, step, [SVal], detectors, width, sinogram, normalize=False)
        sin2 = sinogram.copy()
        sin2 /= max(sin2.flatten())
        if filter:
             sin2 = rn.filterSinogram(sin2)
             inverseImage = rn.inverseRadonTransform(sin2, step, [SVal], detectorsWidth=width,
                                                          outputWidth=len(inData[0]), outputHeight=len(inData), output=inverseImage, normalize=False)
        else:
            inverseImage = rn.inverseRadonTransform(sin2, step, [SVal], detectorsWidth=width,
                                                     outputWidth=len(inData[0]), outputHeight=len(inData), output=inverseImage, normalize=False)

        copy = inverseImage.copy()
        for X in range(0,len(copy)):
            for Y in range(0,len(copy[0])):
                if copy[X][Y] <0: copy[X][Y] =0;
        copy /= max(copy.flatten())
        result[S] = returnDifference2D(inData, copy)
        print(
            "{}{}. {:.2f}% --- step:{} detectorsNum:{} width:{} result:{}".format(prefix, num, (num / len(stepsArray) * 100), SVal,
                                                                                  detectors, width, result[S]))

    plot2D(stepsArray, result, "interation", figSaveName, line="bo")
    saveDataToFile(step,detectors,width,result,figSaveName)

    return


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
                inverseRadonImage = rn.inverseRadonTransform(sinogram, stepSize=SVal, detectorsWidth=WVal, outputWidth=len(inData[0]), outputHeight=len(inData))

                result[S,D,W] = returnDifference2D(inData, inverseRadonImage)
                print("{}{}. {:.2f}% --- step:{} detectorsNum:{} width:{} result:{}".format(prefix,num,(num/all*100),SVal,DVal,WVal,result[S,D,W]))

    smart4DPlot(stepArr, detectorsArr, widthArr, result, figSaveName)
    return

def plot2D(X,Y,labelX, figSaveName, labelY="variation", line='--bo'):
    plt.gcf().clear()
    plt.plot(X,Y,line)
    plt.xlabel(labelX)
    plt.ylabel(labelY)
    plt.savefig(figSaveName+".pdf")
    return

def plot3D(X,Y,Z,labelX, labelY, figSaveName, labelZ="variation"):
    plt.gcf().clear()
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    cartesian = np.array([ [x,y] for x in X for y in Y ])
    ax.scatter(cartesian[:,0],cartesian[:,1],Z)
    ax.set_xlabel(labelX)
    ax.set_ylabel(labelY)
    ax.set_zlabel(labelZ)
    plt.savefig(figSaveName+".pdf")
    return

def plot4D(X,Y,Z,A, labelX, labelY, labelZ, figSaveName, labelA="variation"):
    plt.gcf().clear()
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    cartesian = np.array([[x, y, z] for x in X for y in Y for z in Z])
    plt.gca().invert_yaxis()
    sp = ax.scatter(cartesian[:,0],cartesian[:,1],cartesian[:,2], c=A, cmap=plt.hot(), marker="h")
    ax.set_xlabel(labelX)
    ax.set_ylabel(labelY)
    ax.set_zlabel(labelZ)
    bar = plt.colorbar(sp)
    bar.set_label(labelA)
    plt.savefig(figSaveName+".pdf")
    plt.show()
    return

def saveDataToFile(X, Y, Z, data, figSaveName):
    with open(figSaveName+"txt","w") as file:
        file.write(str(X)+"\n\n")
        file.write(str(Y)+"\n\n")
        file.write(str(Z)+"\n\n")
        file.write(str(data)+"\n\n")

def smart4DPlot(X, Y, Z, data, figSaveName, labelX="Step", labelY="Number of detectors", labelZ="Detectors width"):
    saveDataToFile(X,Y,Z,data,figSaveName)

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
        testAlgorithm(step, detectors, detWidth, True, "main4DFilter", prefix="test1: ")
    def test2():
        testAlgorithm(step, detectors, detWidth, False, "main4DNoFilter", prefix="test2: ")
    def test3():
        testAlgorithm([1], [200], detWidth, True, "main2DFilterStep1Detectors200", prefix="test3: ")
    def test4():
        testAlgorithm([1], [200], detWidth, False, "main2DNoFilterStep1Detectors200", prefix="test4: ")
    def test5():
        testAlgorithm(step, [200], [170], True, "main2DFilterDetectors200Width170", prefix="test5: ")
    def test6():
        testAlgorithm(step, [200], [170], False, "main2DNoFilterDetectors200Width170", prefix="test6: ")
    def test7():
        testAlgorithm([1], detectors, [170], True, "main2DFilterStep1Width170", prefix="test7: ")
    def test8():
        testAlgorithm([1], detectors, [170], False, "main2DNoFilterStep1Width170", prefix="test8: ")
    def test9(): #TEST ITERACJI
        testIterations(1, 200, 170, True, "testIterationsFilterStep1Ditectors200Width170", prefix="test9: ")
    def test10():  # TEST ITERACJI
        testIterations(1, 200, 170, False, "testIterationsNoFilterStep1Ditectors200Width170", prefix="test10: ")


    runInParallel(test1,test2,test3,test4,test5,test6,test7,test8,test9,test10)
    return


if __name__ == "__main__":
    main()
