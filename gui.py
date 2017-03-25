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

class MainGui(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        tk.Tk.wm_title(self, "CT")
        self.path = "No file"
        padx = 10
        pady = 10
        textWidth = 20
        control = tk.Frame(self)
        control.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        step = ttk.Label(control, text="Step:")
        step.grid(row=1, column=1, padx=padx, pady=pady)
        stepText = tk.Text(control, width=textWidth, height=step.winfo_height())
        stepText.grid(row=1, column=2)
        detector = ttk.Label(control, text="Detectors:")
        detector.grid(row=2, column=1, padx=padx, pady=pady)
        detectorText = tk.Text(control, width=textWidth, height=detector.winfo_height())
        detectorText.grid(row=2, column=2, padx=padx, pady=pady)
        span = ttk.Label(control, text="Span:")
        span.grid(row=3, column=1, padx=padx, pady=pady)
        spanText = tk.Text(control, width=textWidth, height=span.winfo_height())
        spanText.grid(row=3, column=2, padx=padx, pady=pady)
        buttonChoose = ttk.Button(control, text="Choose file", command=lambda: self.chooseFile())
        buttonChoose.grid(row=1, column=3, padx=padx, pady=pady)
        self.pathLabel = ttk.Label(control, text=self.path)
        self.pathLabel.grid(row=1, column=4)
        buttonTransform = ttk.Button(control, text="Transform", command=lambda: transform(graph, path=self.path))
        buttonTransform.grid(row=5, column=1, padx=padx, pady=pady)
        container = tk.Frame(self)
        container.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        ttk.Scrollbar(container)
        graph = Graph()
        container.tkraise()
        canvas = FigureCanvasTkAgg(graph, container)
        graph.canvas = canvas
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    def chooseFile(self):
        self.path = filedialog.askopenfilename()
        self.pathLabel.set

def transform(graph, path="input.png"):
    if not os.isfile(path):
        messagebox.showinfo(title="No file", message="Please choose existing file")
        return
    main.transformImage(graph,path)

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
