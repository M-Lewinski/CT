import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import Image,ImageTk
import main
import os.path as os
from tkinter import messagebox
from collections import defaultdict
import string

class MainGui(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        tk.Tk.wm_title(self, "CT")
        self.path = "No file"
        self.digitChecker = digitChecker(string.digits)
        self.steps = ["Step", 1, 45]
        self.detectors = ["Detectors count", 25, 400]
        self.spans = ["Span width", 30, 180]
        self.controlMenu()
        self.graphMenu()

    def controlMenu(self):
        padx = 10
        pady = 5
        textWidth = 20
        control = tk.Frame(self)
        control.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        step = ttk.Labelframe(control, text=self.steps[0])
        step.grid(row=1, column=1, padx=padx, pady=pady, sticky=tk.W)
        self.stepText = tk.Text(step, width=textWidth, height=step.winfo_height())
        self.stepText.pack(padx=padx, pady=pady)
        detector = ttk.Labelframe(control, text=self.detectors[0])
        detector.grid(row=2, column=1, padx=padx, pady=pady, sticky=tk.W)
        self.detectorText = tk.Text(detector, width=textWidth, height=detector.winfo_height())
        self.detectorText.pack(padx=padx, pady=pady)
        span = ttk.Labelframe(control, text=self.spans[0])
        span.grid(row=3, column=1, padx=padx, pady=pady, sticky=tk.W)
        self.spanText = tk.Text(span, width=textWidth, height=span.winfo_height())
        self.spanText.pack(padx=padx, pady=pady)
        pathFrame = ttk.Labelframe(control, text="File directory")
        pathFrame.grid(row=1, column=2, pady=pady, sticky=tk.W)
        buttonChoose = ttk.Button(pathFrame, text="Load file", command=lambda: self.chooseFile())
        buttonChoose.grid(row=1, column=1, padx=padx, pady=pady)
        self.pathLabel = ttk.Label(pathFrame, text=self.path)
        self.pathLabel.grid(row=1, column=2, padx=padx, pady=pady)
        imagesLabel = ttk.Labelframe(control, text="Images")
        imagesLabel.grid(row=2, column=2, pady=pady, sticky=tk.W)
        self.images = ttk.Combobox(imagesLabel, state="disabled")
        self.images.pack(padx=padx, pady=pady)
        buttonTransform = ttk.Button(control, text="Transform", command=lambda: self.transform())
        buttonTransform.grid(row=4, column=1, padx=padx, pady=pady, sticky=tk.W)

    def graphMenu(self):
        container = tk.Frame(self)
        container.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        ttk.Scrollbar(container)
        self.graph = Graph()
        container.tkraise()
        canvas = FigureCanvasTkAgg(self.graph, container)
        self.graph.canvas = canvas
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    def chooseFile(self):
        self.path = filedialog.askopenfilename()
        self.pathLabel.config(text=self.path)

    def checkText(self, value, textBox):
        valueInt = value.translate(self.digitChecker)
        name = textBox[0]
        lowerBound = textBox[1]
        upperBound = textBox[2]
        please = "Please input into the " + name + " entry box, number between " + str(lowerBound) + " and " + str(upperBound)
        if valueInt == "":
            messagebox.showinfo(title="Wrong param", message=("No number\n" + please))
            return None
        else:
            valueInt = int(valueInt)
        if valueInt < lowerBound:
            messagebox.showinfo(title="Wrong param", message=("Value bellow lower bound\n" + please))
            return None
        elif valueInt > upperBound:
            messagebox.showinfo(title="Wrong param", message=("Value above upper bound\n" + please))
            return None
        return valueInt

    def transform(self):
        if not os.isfile(self.path):
            messagebox.showinfo(title="No file", message="Please choose existing file")
            return
        step = self.checkText(self.stepText.get("1.0", "end-1c"), self.steps)
        if step is None:
            return
        detector = self.checkText(self.detectorText.get("1.0", "end-1c"), self.detectors)
        if detector is None:
            return
        span = self.checkText(self.spanText.get("1.0", "end-1c"), self.spans)
        if span is None:
            return
        main.transformImage(self.graph, self.path)


class Graph(Figure):
    plots = {}
    canvas = None

    def __init__(self, figsize=(10,10), dpi=100):
        Figure.__init__(self, figsize=figsize, dpi=dpi)
        titles = [{"title": "Original image"}, {"title": "Radon transform image", "xlabel": "Emiter/detector rotation", "ylabel": "Number of receiver"},
                 {"title": "Inverse Radon transform image"}]
        for i in range(0, 3):
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


def digitChecker(keep):
    table = defaultdict(type(None))
    table.update({ord(c): c for c in keep})
    return table
