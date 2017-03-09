import numpy as np


#stepsArray = array with emiter position angles (angle between line an OY)
#detectorsWidth = detectors area angle
def radonTransform(input, stepsArray=range(0,180), detectorsNumber=100, detectorsWidth=140, output=None):
    if output is None: output = np.zeros((detectorsNumber,180))

    circleRadius = np.sqrt(np.power(len(input)/2,2)+np.power(len(input[0])/2,2) )
    center = (len(input[0])/2,len(input)/2)

    output = radonCircleLoop(input,output, stepsArray,center,circleRadius,detectorsNumber,detectorsWidth)

    output[:,stepsArray]/=max(output.flatten()) #Normalizacja
    return output

def inverseRadonTransform(input, stepsArray=range(0,180), detectorsWidth=150, output=None, outputWidth=None, outputHeight=None):
    if output is None:
        if outputHeight is None: outputHeight = len(input)
        if outputWidth is None: outputWidth = outputHeight
        output = np.zeros((outputHeight,outputWidth))
    detectorsNumber=len(input)

    circleRadius = np.sqrt(np.power(outputWidth/2,2)+np.power(outputHeight/2,2) )
    center = (outputWidth/2,outputHeight/2)

    output = radonCircleLoop(input,output, stepsArray,center,circleRadius,detectorsNumber,detectorsWidth,inverse=True)

    output /= max(output.flatten())
    return output

def radonCircleLoop(input, output, stepsArray, center, circleRadius, detectorsNumber, detectorsWidth, inverse=False):
    detectorDistance = (circleRadius * 2 * detectorsWidth / 180) / detectorsNumber

    for stepAngle in stepsArray:
        centralEmiterPos = (center[0] + circleRadius * np.sin(np.radians(stepAngle)),center[1] + np.cos(np.radians(stepAngle)) * circleRadius)
        centralReceiverPos = (center[0] - circleRadius * np.sin(np.radians(stepAngle)),center[1] - np.cos(np.radians(stepAngle)) * circleRadius)

        currentDetector = 0
        while currentDetector < detectorsNumber:
            distanceFromMainDetector = (currentDetector - (detectorsNumber / 2)) * detectorDistance

            cos = np.cos(np.radians(stepAngle))
            sin = np.sin(np.radians(stepAngle))
            emiterPos = centralEmiterPos[0] + distanceFromMainDetector * cos, centralEmiterPos[1] - distanceFromMainDetector * sin
            receiverPos = centralReceiverPos[0] + distanceFromMainDetector * cos, centralReceiverPos[1] - distanceFromMainDetector * sin
            if not inverse:
                points = BresenhamAlgorithm(input, emiterPos, receiverPos)
                if len(points) > 0: output[currentDetector][stepAngle] = sum(points)  # Normalizacja
            else:
                color = input[currentDetector, stepAngle]
                output = BresenhamAlgorithm(input, emiterPos, receiverPos, output, returnOrDraw=False, lineColor=color)
            currentDetector += 1
    return output

def filter(input, mask=None):
    output=np.zeros((len(input),len(input[0])))
    if mask is None: mask = np.array([[0.1,0.2,0.3,0.2,0.1],[0.2,0.5,0.7,0.5,0.2],[0.3,0.7,1,0.7,0.3],[0.2,0.5,0.7,0.5,0.2],[0.1,0.2,0.3,0.2,0.1]])
    weightSum = sum(mask.flatten())
    maskSizeY, maskSizeX=len(mask), len(mask[0])
    inputSizeY, inputSizeX = len(input), len(input[0])


    for Y in range(0,inputSizeY):
        for X in range(0,inputSizeX):
            val=0
            for maskY in range(-int(maskSizeY/2),int(maskSizeY/2)+1):
                for maskX in range(-int(maskSizeX/2),int(maskSizeX/2)+1):
                    cY = Y+maskY
                    cX = X+maskX
                    if cY<0: cY+= inputSizeY
                    if cX<0: cX+= inputSizeX
                    if cY>=inputSizeY: cY -= inputSizeY
                    if cX>=inputSizeX: cX -= inputSizeX
                    val+=input[cY][cX]*mask[maskY+int(maskSizeY/2)][maskX+int(maskSizeX/2)]
            val/=weightSum
            output[Y][X]=val

    return output

# returnOrDraw : Return list of values if True ; Draw line if False
def BresenhamAlgorithm(input, A, B, output=None, moreThanZeroValues=True, returnOrDraw=True, lineColor=0.5):
    if returnOrDraw and output is None: output = []
    if not returnOrDraw and output is None: raise NameError("output must be given")

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

    def bresenhamLoop(X,Y,output):
        if returnOrDraw and X >= 0 and Y >= 0 and X < inputSizeX and Y < inputSizeY:
            color = input[inputSizeY - 1 - int(Y)][int(X)]
            if not moreThanZeroValues or color > 0: output.append(color)
        if not returnOrDraw and X>=0 and Y>=0 and Y<len(output) and X < len(output[0]):
            output[inputSizeY - 1 - int(Y)][int(X)] += lineColor
        Y += yAdd
        X += xAdd
        return X,Y,output

    if dx >= dy :
        yAdd = float(abs(Y-Y2))/abs(X-X2)*yAdd
        while X != X2: X,Y,output = bresenhamLoop(X,Y,output)
    else:
        xAdd = float(abs(X-X2))/abs(Y-Y2)*xAdd
        while Y != Y2: X,Y,output = bresenhamLoop(X,Y,output)
    return output
