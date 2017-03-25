
from reportlab.platypus.paraparser import sizeDelta


import matplotlib.pyplot as plt
import radon as rn
import numpy as np
from skimage import data, color, measure
import gui

step = 1
detectorsNumber = 100
detectorWidth = 180
filter=True

def transformImage(graph, path):
    # inData = data.imread("input.png", as_grey=True)
    inData = data.imread(path, as_grey=True)
    graph.changePlot((2,2,1),inData)
    sinogram = rn.radonTransform(inData, stepSize=step, detectorsNumber=detectorsNumber, detectorsWidth=detectorWidth)
    graph.plots[(2,2,2)].imshow(sinogram, cmap='gray', extent=[0,180,len(sinogram),0], interpolation=None)
    graph.canvas.show()
    if filter: sinogram = rn.filterSinogram(sinogram)
    inverseRadonImage = rn.inverseRadonTransform(sinogram, stepSize=step, detectorsWidth=detectorWidth, outputWidth=256, outputHeight=256)
    graph.changePlot((2, 2, 3), inverseRadonImage)

def main():
    app = gui.MainGui()
    app.mainloop()

if __name__ == "__main__":
    main()
