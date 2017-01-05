#!/usr/bin/env python

import matplotlib
matplotlib.use('TkAgg')

from Tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt

fwin = Tk()
fwin.wm_title("Plots")

plot = Figure(figsize = (6, 5), dpi= 95)
plot.subplots_adjust(hspace =.6)
matplotlib.rcParams.update({'font.size':10})

x1 = np.linspace(0.0, 5.0)
x2 = np.linspace(0.0, 2.0)

y1 = np.cos(2 * np.pi * x1) * np.exp(-x1)
y2 = np.cos(2 * np.pi * x2)

a = plot.add_subplot(2, 1, 1, title = "Test\n", xlabel = "x axis", ylabel = "y axis")
a.plot(x1, y1)

b = plot.add_subplot(2, 1, 2, xlabel = "x axis", ylabel = "y axis")
b.plot(x2, y2, '.-')

canvas = FigureCanvasTkAgg(plot, master = fwin)
canvas.show()
canvas.get_tk_widget().pack(side = TOP, fill = BOTH, expand=1)

toolbar = NavigationToolbar2TkAgg(canvas, fwin)
toolbar.update()
canvas._tkcanvas.pack(side = TOP, fill = BOTH, expand=1)

fwin.mainloop()
