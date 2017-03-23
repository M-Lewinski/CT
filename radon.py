import numpy as np

def createBackProjectionFilter(len):
    if len%2==0: raise NameError("Incorrect len")
    out = np.zeros(len)
    middle=int(len/2)
    out[middle]=1
    for i in range(1,middle,2):
        val=-4/(np.power(np.pi,2) * np.power(i,2))
        out[middle-i]=val
        out[middle+i] = val
    return out


def radonTransform(input, stepSize=1, stepsArray=None, detectorsNumber=100, detectorsWidth=140, output=None):
    if stepsArray is None: stepsArray = np.arange(0,180,stepSize)
    xSize = int(180/stepSize+1)

    if output is None: output = np.zeros((detectorsNumber,xSize))

    circleRadius = np.sqrt(np.power(len(input)/2,2)+np.power(len(input[0])/2,2) )
    center = (len(input[0])/2,len(input)/2)
    output = radonCircleLoop(input,output, stepsArray, stepSize, center, circleRadius,detectorsNumber,detectorsWidth)

    output /= max(output.flatten()) #Normalizacja
    return output

def inverseRadonTransform(input, stepSize=1, stepsArray=None, detectorsWidth=140, output=None, outputWidth=None, outputHeight=None):
    if stepsArray is None: stepsArray = np.arange(0,181, stepSize)
    if output is None:
        if outputHeight is None: outputHeight = len(input)
        if outputWidth is None: outputWidth = outputHeight
        output = np.zeros((outputHeight,outputWidth))

    circleRadius = np.sqrt(np.power(outputWidth/2,2)+np.power(outputHeight/2,2) )
    center = (outputWidth/2,outputHeight/2)
    output = radonCircleLoop(input,output, stepsArray, stepSize, center,circleRadius,len(input),detectorsWidth,inverse=True)

    output -= min(output.flatten())
    output /= max(output.flatten())

    return output

def radonCircleLoop(input, output, stepsArray, step, center, circleRadius, detectorsNumber, detectorsWidth, inverse=False):
    detectorDistance = (circleRadius * 2 * detectorsWidth / 180) / detectorsNumber

    for stepAngle in stepsArray:
        centralEmiterPos = (center[0] + circleRadius * np.sin(np.radians(stepAngle)),center[1] + np.cos(np.radians(stepAngle)) * circleRadius)
        centralReceiverPos = (center[0] - circleRadius * np.sin(np.radians(stepAngle)),center[1] - np.cos(np.radians(stepAngle)) * circleRadius)

        for currentDetector in range(0,detectorsNumber):
            distanceFromMainDetector = (currentDetector - (detectorsNumber / 2)) * detectorDistance

            cos = np.cos(np.radians(stepAngle))
            sin = np.sin(np.radians(stepAngle))
            emiterPos = centralEmiterPos[0] + distanceFromMainDetector * cos, centralEmiterPos[1] - distanceFromMainDetector * sin
            receiverPos = centralReceiverPos[0] + distanceFromMainDetector * cos, centralReceiverPos[1] - distanceFromMainDetector * sin
            if not inverse:
                points = BresenhamAlgorithm(input, emiterPos, receiverPos)
                if len(points) > 0: output[currentDetector][int(stepAngle/step)] = sum(points)  # Normalizacja
            else:
                color = input[currentDetector, int(stepAngle/step)]
                output = BresenhamAlgorithm(input, emiterPos, receiverPos, output, returnOrDraw=False, lineColor=color)
    return output

def filterSinogram(input):
    lines = len(input[0])
    mask = createBackProjectionFilter(13)
    for num in range(0,lines):
        input[:, num] = filter1D(input[:,num], mask=mask)
    return input

def filter1D(input, mask=None):
    output = np.zeros(len(input))
    if mask is None: mask = createBackProjectionFilter(9)
    maskSize, inputSize = len(mask), len(input)
    for X in range(0,inputSize):
        for maskX in range(-int(maskSize / 2), int(maskSize / 2) + 1):
            cX = X + maskX
            if cX >= inputSize: cX -= inputSize
            output[X] += input[cX] * mask[maskX + int(maskSize / 2)]
    return output

# returnOrDraw : Return list of values if True ; Draw line if False
def BresenhamAlgorithm(input, A, B, output=None, moreThanZeroValues=True, returnOrDraw=True, lineColor=0.5):
    if returnOrDraw and output is None: output = []
    if not returnOrDraw:
        if output is None: raise NameError("output must be given")
        outSizeX, outSizeY = len(output[0]), len(output)

    inputSizeX, inputSizeY,  = len(input[0]), len(input)
    X, Y = int(A[0]), int(A[1])
    X2, Y2 = int(B[0]), int(B[1])
    dx, dy = abs(X-X2), abs(Y-Y2)
    xAdd, yAdd = 1 if X<X2 else -1, 1 if Y<Y2 else -1

    def bresenhamLoop(X,Y,output):
        if returnOrDraw and X >= 0 and Y >= 0 and X < inputSizeX and Y < inputSizeY:
            color = input[inputSizeY - 1 - int(Y)][int(X)]
            if not moreThanZeroValues or color > 0: output.append(color)
        if not returnOrDraw and X>=0 and Y>=0 and Y<outSizeY and X < outSizeX:
            output[outSizeY - 1 - int(Y)][int(X)] += lineColor
        return X+xAdd,Y+yAdd,output

    if dx >= dy :
        yAdd = float(abs(Y-Y2))/abs(X-X2)*yAdd
        while X != X2: X,Y,output = bresenhamLoop(X,Y,output)
    else:
        xAdd = float(abs(X-X2))/abs(Y-Y2)*xAdd
        while Y != Y2: X,Y,output = bresenhamLoop(X,Y,output)
    return output
