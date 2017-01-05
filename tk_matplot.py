#!/usr/bin/env python

import matplotlib
matplotlib.use('TkAgg')

from Tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt


matplotlib.rcParams['font.size'] = 10
matplotlib.rcParams['figure.facecolor'] = 'white'


fwin = Tk()
fwin.iconbitmap(default = 'favicon.ico')
fwin.wm_title("Plots")

plot = Figure(figsize = (6, 5), dpi= 95)
plot.subplots_adjust(hspace =.6)
canvas = FigureCanvasTkAgg(plot, master = fwin)

x1 = np.linspace(0.0, 5.0)
x2 = np.linspace(0.0, 5.0)

y1 = np.cos(2 * np.pi * x1) * np.exp(-x1)
y2 = np.cos(2 * np.pi * x2)

a = plot.add_subplot(2, 1, 1, title = "Test\n", xlabel = "x axis", ylabel = "y axis")
pos = a.get_position()
a.set_position([pos.x0, pos.y0, pos.width * 0.85, pos.height])

series1 = a.plot(x1, y1, ',', label = 'Series 1')
series2 = a.plot(x2, y2, '--', label = 'Series 2')

lga = a.legend(loc = 'center left', bbox_to_anchor = (1, 0.5), prop={'size':10})
lga.get_frame().set_alpha(0.4)

lines = [series1, series2]
lined = dict()
for legline, origline in zip(lga.get_lines(), lines):
    legline.set_picker(5)
    lined[legline] = origline[0]


def onpick(event):
    legline = event.artist
    origline = lined[legline]
    vis = not origline.get_visible()
    origline.set_visible(vis)
    if vis:
        legline.set_alpha(1.0)
    else:
        legline.set_alpha(0.2)
    canvas.draw()

canvas.mpl_connect('pick_event', onpick)

# b = plot.add_subplot(2, 1, 2, xlabel = "x axis", ylabel = "y axis")
# b.plot(x2, y2, '.-')

canvas.show()
canvas.get_tk_widget().pack(side = TOP, fill = BOTH, expand=1)

toolbar = NavigationToolbar2TkAgg(canvas, fwin)
toolbar.update()
canvas._tkcanvas.pack(side = TOP, fill = BOTH, expand=1)

fwin.mainloop()
