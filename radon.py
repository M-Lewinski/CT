import numpy as np


#stepsArray = array with emiter position angles (angle between line an OY)
#detectorsWidth = detectors area angle
def radonTransform(input, stepsArray=range(0,180), detectorsNumber=180, detectorsWidth=140):
    output = np.zeros((detectorsNumber,180))

    circleRadius = np.sqrt(np.power(len(input)/2,2)+np.power(len(input[0])/2,2) )
    center = (len(input)/2,len(input[0])/2)

    detectorDistance = (circleRadius*2*detectorsWidth/180)/detectorsNumber

    startPoint = (center[0],center[1]+circleRadius)
    max = 0
    for stepAngle in stepsArray:
        centralEmiterPos = (startPoint[0]+circleRadius*np.sin(np.radians(stepAngle)), center[1]+np.cos(np.radians(stepAngle))*circleRadius)
        centralReceiverPos = (startPoint[0]-circleRadius*np.sin(np.radians(stepAngle)), center[1]-np.cos(np.radians(stepAngle))*circleRadius)

        currentDetector = 0
        while currentDetector < detectorsNumber:
            distanceFromMainDetector = (currentDetector-(detectorsNumber/2))*detectorDistance

            cos = np.cos(np.radians(stepAngle))
            sin = np.sin(np.radians(stepAngle))

            emiterPos=centralEmiterPos[0]+distanceFromMainDetector*cos, centralEmiterPos[1]-distanceFromMainDetector*sin
            receiverPos=centralReceiverPos[0]+distanceFromMainDetector*cos, centralReceiverPos[1]-distanceFromMainDetector*sin

            points=BresenhamAlgorithm(input,emiterPos,receiverPos)
            if len(points)>0 : output[currentDetector, stepAngle] = sum(points)    #Normalizacja
            if output[currentDetector, stepAngle] > max : max = output[currentDetector, stepAngle]
            currentDetector+=1

    output/=max #Normalizacja
    return output

def inverseRadonTransform(input):
    output = np.zeros((250,250))

    return output

def filter(input):

    return input

def BresenhamAlgorithm(input, A, B, moreThanZeroValues=True):
    output = []
    inputSizeX = len(input[0])
    inputSizeY = len(input)
    X, Y = int(A[0]), int(A[1])
    X2, Y2 = int(B[0]), int(B[1])

    dx = abs(X-X2)
    dy = abs(Y-Y2)

    if X<X2 : xAdd = 1
    else : xAdd = -1
    if Y<Y2 : yAdd = 1
    else : yAdd = -1

    if dx > dy :
        yAdd = float(abs(Y-Y2))/abs(X-X2)*yAdd
        while X != X2:
            if X>=0 and Y>=0 and X<inputSizeX and Y<inputSizeY:
                color = input[inputSizeY-1-int(Y)][X]
                if not moreThanZeroValues or color>0: output.append(color)
            Y+=yAdd
            X+=xAdd
    else:
        xAdd = float(abs(X-X2))/abs(Y-Y2)*xAdd
        while Y != Y2:
            if X >= 0 and Y >= 0 and X < inputSizeX and Y < inputSizeY:
                color = input[inputSizeY-1-Y][int(X)]
                if not moreThanZeroValues or color>0: output.append(color)
            X+=xAdd
            Y+=yAdd
    return output
