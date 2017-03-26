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
        control, leftGrid, middleGrid, rightGrid = self.controlMenu()
        self.graphMenu()
        self.imageNumber = tk.IntVar()
        sliderLabel = ttk.Labelframe(middleGrid, text="Inverse image number")
        sliderLabel.grid(row=1, column=2, pady=10, sticky=tk.W)
        self.imageNumber.set(1)
        slider = tk.Scale(sliderLabel, variable=self.imageNumber, from_=1, to=10, orient=tk.HORIZONTAL,
                          command=lambda value: self.graph.swapImage(int(value)-1))
        slider.pack(padx=10, pady=10)

    def controlMenu(self):
        padx = 10
        pady = 5
        textWidth = 20
        control = tk.Frame(self)
        control.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        leftGrid = tk.Frame(control)
        leftGrid.grid(row=1, column=1, sticky=tk.W)
        step = ttk.Labelframe(leftGrid, text=self.steps[0])
        step.grid(row=1, column=1, padx=padx, pady=pady, sticky=tk.W)
        self.stepText = tk.Text(step, width=textWidth, height=step.winfo_height())
        self.stepText.pack(padx=padx, pady=pady)
        self.stepText.insert("1.0", "1")
        detector = ttk.Labelframe(leftGrid, text=self.detectors[0])
        detector.grid(row=2, column=1, padx=padx, pady=pady, sticky=tk.W)
        self.detectorText = tk.Text(detector, width=textWidth, height=detector.winfo_height())
        self.detectorText.pack(padx=padx, pady=pady)
        self.detectorText.insert("1.0", "200")
        span = ttk.Labelframe(leftGrid, text=self.spans[0])
        span.grid(row=3, column=1, padx=padx, pady=pady, sticky=tk.W)
        self.spanText = tk.Text(span, width=textWidth, height=span.winfo_height())
        self.spanText.pack(padx=padx, pady=pady)
        self.spanText.insert("1.0", "150")
        middleGrid = tk.Frame(control)
        middleGrid.grid(row=1, column=2)
        # imagesLabel = ttk.Labelframe(control, text="Images")
        # imagesLabel.grid(row=1, column=2, pady=pady, sticky=tk.W)
        # self.values = tk.StringVar()
        # self.images = ttk.Combobox(imagesLabel, state="disabled", textvariable=self.values)
        # self.images.pack(padx=padx, pady=pady)
        transformLabel = ttk.Labelframe(middleGrid, text="transform")
        transformLabel.grid(row=3, column=2, pady=pady, sticky=tk.W)
        self.filterVar = tk.BooleanVar()
        checkButton = MyCheckButton(middleGrid, text="Filter", variable=self.filterVar, onvalue=True, offvalue=False)
        checkButton.grid(row=2, column=2,padx=padx, pady=pady, sticky=tk.W)
        checkButton.select()
        buttonTransform = ttk.Button(transformLabel, text="Transform", command=lambda: self.transform())
        buttonTransform.pack(padx=padx, pady=pady)
        # buttonTransform.grid(row=2, column=1, padx=padx, pady=pady, sticky=tk.W)

        rightGrid = tk.Frame(control)
        rightGrid.grid(row=1, column=3)
        pathFrame = ttk.Labelframe(rightGrid, text="File directory")
        pathFrame.grid(row=1, column=3, padx=padx, pady=pady, sticky=tk.W)
        buttonChoose = ttk.Button(pathFrame, text="Load file", command=lambda: self.chooseFile())
        buttonChoose.grid(row=1, column=1, padx=padx, pady=pady)
        self.pathLabel = ttk.Label(pathFrame, text=self.path)
        self.pathLabel.grid(row=1, column=2, padx=padx, pady=pady, sticky=tk.W)

        self.dicom = ttk.Labelframe(rightGrid,text="DICOM Info")
        self.dicom.grid(row=2, column=3, padx=padx, pady=pady, sticky=tk.W)
        nameDicomFrame = ttk.Labelframe(self.dicom, text="Surname and first name")
        nameDicomFrame.grid(row=1, column=1, padx=padx, pady=pady, sticky=tk.W)
        self.nameDicom = tk.Label(nameDicomFrame, text="Name")
        # self.nameDicom = tk.Text(nameDicomFrame, width=textWidth, height=nameDicomFrame.winfo_height())
        self.nameDicom.pack()
        idDicomFrame = ttk.Labelframe(self.dicom, text="Id")
        idDicomFrame.grid(row=1, column=2, padx=padx, pady=pady, sticky=tk.W)
        self.idDicom = ttk.Label(idDicomFrame, text="Id")
        # self.idDicom = tk.Text(idDicomFrame, width=textWidth, height=idDicomFrame.winfo_height())
        self.idDicom.pack()
        dateDicomFrame = ttk.Labelframe(self.dicom, text="Date")
        dateDicomFrame.grid(row=2, column=1, padx=padx, pady=pady, sticky=tk.W)
        self.dateDicom = tk.Label(dateDicomFrame, text="Date")
        # self.dateDicom = tk.Text(dateDicomFrame, width=textWidth, height=dateDicomFrame.winfo_height())
        self.dateDicom.pack()
        timeDicomFrame = ttk.Labelframe(self.dicom, text="Time")
        timeDicomFrame.grid(row=2, column=2, padx=padx, pady=pady, sticky=tk.W)
        self.timeDicom = tk.Label(timeDicomFrame, text="Time")
        # self.timeDicom = tk.Text(timeDicomFrame, width=textWidth, height=timeDicomFrame.winfo_height())
        self.timeDicom.pack()

        return control, leftGrid, middleGrid, rightGrid

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
        # self.images.config(state="readonly")
        self.path = filedialog.askopenfilename()
        self.pathLabel.config(text=self.path)
        fileExtension = self.path.split(".")
        if not fileExtension[1] == "dcm":
            # self.images["values"] = fileExtension[0].split("/")[-1]
            return


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
        main.transformImage(self.graph, self.path, step=step, detectorsNumber=detector, detectorWidth=span, filter=self.filterVar.get())


class Graph(Figure):
    plots = {}
    canvas = None
    def __init__(self, figsize=(10,10), dpi=100):
        self.inverseImages = [None]*10
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

    def swapImage(self, number):
        if self.inverseImages[number] is not None:
            self.changePlot((2,2,3), self.inverseImages[number])


def digitChecker(keep):
    table = defaultdict(type(None))
    table.update({ord(c): c for c in keep})
    return table


class MyCheckButton(tk.Checkbutton):
    def __init__(self,*args,**kwargs):
        self.var = kwargs.get('variable',tk.BooleanVar())
        kwargs['variable'] = self.var
        tk.Checkbutton.__init__(self,*args,**kwargs)

    def is_checked(self):
        return self.var.get()

