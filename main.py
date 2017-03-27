
from reportlab.platypus.paraparser import sizeDelta


import matplotlib.pyplot as plt
import radon as rn
import numpy as np
from skimage import data, color, measure
import gui


def transformImage(graph, image, step=0.5, detectorsNumber=200, detectorWidth=150, filter=True):
    graph.changePlot((2,2,1),image)
    sinogram = rn.radonTransform(image, stepSize=step, detectorsNumber=detectorsNumber, detectorsWidth=detectorWidth)
    graph.plots[(2,2,2)][1] = sinogram.copy()
    graph.plots[(2,2,2)][0].imshow(sinogram, cmap='gray', extent=[0,180,len(sinogram),0], interpolation=None)
    graph.canvas.show()
    graph.changePlot((2,2,2), np.array(sinogram.copy()[:]*255).astype(np.uint8))
    if filter: sinogram = rn.filterSinogram(sinogram)
    graph.inverseImages = rn.inverseRadonTransform(sinogram, stepSize=step, detectorsWidth=detectorWidth)
    graph.changePlot((2, 2, 3), graph.inverseImages[-1])

def main():
    app = gui.MainGui()
    app.mainloop()

if __name__ == "__main__":
    main()
