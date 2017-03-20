import tkinter

import matplotlib
from reportlab.platypus.paraparser import sizeDelta

matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import matplotlib.pyplot as plt
import radon as rn
import numpy as np
from PIL import Image,ImageTk
from skimage import data, color, measure
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

step = np.pi/180
detectorsNumber = 35
detectorWidth = np.pi/6

def transformImage(graph):
    # path = filedialog.askopenfilename()
    inData = data.imread("input.png", as_grey=True)
    graph.changePlot((2,2,1),inData)
    radonImage = rn.radonTransform(inData)
    graph.changePlot((2, 2, 2), radonImage)
    inverseRadonImage = rn.inverseRadonTransform(radonImage)
    graph.changePlot((2, 2, 3), inverseRadonImage)
    filterImage = rn.filter(inverseRadonImage)
    graph.changePlot((2, 2, 4), filterImage)


class MainGui(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        tk.Tk.wm_title(self,"CT")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid(row=2, column=1)
        graph = Graph()
        button = ttk.Button(container, text="Transform", command=lambda: transformImage(graph))
        button.pack(pady=10, padx=10)
        container.tkraise()
        canvas = FigureCanvasTkAgg(graph, container)
        graph.canvas = canvas
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)


class Graph(Figure):
    plots = {}
    canvas = None
    def __init__(self, figsize=(10,10), dpi=100):
        Figure.__init__(self, figsize=figsize, dpi=dpi)
        titles = [{"title": "Original image"}, {"title": "Radon transform image", "xlabel": "Emiter/detector rotation", "ylabel": "Number of receiver"},
                 {"title": "Inverse Radon transform image"}, {"title": "Filtered image"}]
        for i in range(0, 4):
            plt = self.add_subplot(2, 2, i+1)
            if "title" in titles[i]:
                plt.set_title(titles[i]["title"])
            if "xlabel" in titles[i]:
                plt.set_xlabel(titles[i]["xlabel"])
            if "ylabel" in titles[i]:
                plt.set_ylabel(titles[i]["ylabel"])
            self.plots[(2, 2, i+1)] = plt


    def changePlot(self,plot,image,cmap="gray"):
        self.plots[plot].imshow(image,cmap=cmap)
        self.canvas.show()


def main():
    app = MainGui()
    app.mainloop()

if __name__ == "__main__":
    main()
