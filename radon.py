import random
from time import sleep

import numpy as np

#dff


#stepsArray = array with emiter position angles (angle between line an OY)
#detectorsWidth = detectors area angle
def radonTransform(input, stepsArray=range(0,180), detectorsNumber=180, detectorsWidth=90):
    output = np.zeros((detectorsNumber,180))

    circleRadius = np.sqrt(np.power(len(input)/2,2)+np.power(len(input[0])/2,2) )
    center = (len(input)/2,len(input[0])/2)

    detectorDistance = (circleRadius*2*detectorsWidth/180)/detectorsNumber

    print(circleRadius, center, detectorDistance)

    startPoint = (center[0],center[1]+circleRadius)
    for stepAngle in stepsArray:
        centralEmiterPos = (startPoint[0]+circleRadius*np.sin(np.radians(stepAngle)), center[1]+np.cos(np.radians(stepAngle))*circleRadius)
        centralReceiverPos = (startPoint[0]-circleRadius*np.sin(np.radians(stepAngle)), center[1]-np.cos(np.radians(stepAngle))*circleRadius)

        currentDetector = 0
        while currentDetector < detectorsNumber:
            distanceFromMainDetector = (currentDetector-(detectorsNumber/2))*detectorDistance

            cos = np.cos(np.radians(stepAngle))
            sin = np.cos(np.radians(stepAngle))
            emiterPos=centralEmiterPos[0]+distanceFromMainDetector*cos,centralEmiterPos[1]+distanceFromMainDetector*sin
            receiverPos=centralReceiverPos[0]+distanceFromMainDetector*cos,centralReceiverPos[1]+distanceFromMainDetector*sin

            print(emiterPos, receiverPos)

            points=BresenhamAlgorithm(input,emiterPos,receiverPos)
            output[currentDetector, stepAngle] = sum(points)/len(points)    #Normalizacja
            currentDetector+=1
    return output

def inverseRadonTransform(input):
    output = np.zeros((250,250))

    return output

def filter(input):

    return input

def BresenhamAlgorithm(input, A, B):
    #TODO

    return [0.1,0.2]
