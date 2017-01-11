# -*- coding: utf-8 -*-
#!/usr/bin/env python

from tree import *
from Tkinter import *
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
matplotlib.use('TkAgg')

matplotlib.rcParams['figure.facecolor'] = 'white'


def stackProb(master, title, f1, f2):

    master.withdraw()

    for data, loc in zip((f1,f2), ((1,1),(1,4))):
        ax = plt.subplot2grid((10,7), loc, rowspan = 9, colspan = 2)
        ax.invert_yaxis()
        colors = 'rgbykmc'
        labels = [i for i in data.keys()[1:-3]]
        ind = range(len(labels))
        ax.axes.set_xlim([0,1]); ax.axes.set_ylim([-1, len(ind)])
        fdata = [[data[y][M] for y in data.keys()[1:-3]] for M in range(len(data.values()[0]))]
        pos = [0 for i in ind]

        for i in range(len(fdata)):
            ax.barh(ind,fdata[i], align = 'center', color = colors[i], label = data.values()[0][i], left = pos, edgecolor = 'none')
            pos = [pos[j] + fdata[i][j] for j in range(len(fdata[i]))]
        ax.set_yticks(ind); ax.set_yticklabels(labels)
        ax.set_xticklabels(['%s%%' % i for i in range(0,101,20)])
        for spine in ax.spines: ax.spines[spine].set_color('none')
        ax.tick_params(axis='both', color ='none')
        if data == f1:
            ax.set_title(u'ƒ1\n')
            ax.legend(loc = 'upper center', bbox_to_anchor=(1.32,1), ncol = 1, handlelength = 0.7, fontsize = 12)
        else:
            ax.set_title(u'ƒ2\n')
            ax.yaxis.tick_right()
    plt.suptitle('\n%s\n' % title, fontsize = 'large')
    plt.figure(1).canvas.set_window_title(title)
    plt.show()


def rangeProb(master, title, xlabelticks, xlabel, ylabel, f1, f2):

    master.withdraw()

    f1 = f1.values()[-2]
    f2 = f2.values()[-2]

    ind = np.arange(len(xlabelticks))
    fig, ax = plt.subplots()

    f1line = ax.plot(xlabelticks, f1, label = u'ƒ1', lw = 2)
    f2line = ax.plot(xlabelticks, f2, label = u'ƒ2', lw = 2)

    ax.legend(loc = 'best')
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.set_title('%s\n' % title)

    plt.figure(1).canvas.set_window_title(title)
    plt.show()


def barProb(master, title, xlabelticks, xlabel, ylabel, f1, f2):

    master.withdraw()

    f1Means, f1Devs = f1.values()[-2], f1.values()[-1]
    f2Means, f2Devs = f2.values()[-2], f2.values()[-1]

    ind = np.arange(len(xlabelticks))
    width = 0.25
    fig, ax = plt.subplots()

    f1bars = ax.bar(ind, f1Means, width, color='r', yerr = f1Devs, label = u'ƒ1', error_kw = dict(ecolor='black', lw=1, capsize=3, capthick=1))
    f2bars = ax.bar(ind + width, f2Means, width, color='y', yerr = f2Devs, label = u'ƒ2', error_kw = dict(ecolor='black', lw=1, capsize=3, capthick=1))

    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.set_title('%s\n' % title)
    ax.set_xticks(ind + width)
    ax.set_xticklabels((str(i) for i in xlabelticks))

    ax.legend(loc = 'best', handlelength = 0.7)

    plt.figure(1).canvas.set_window_title('0.7')
    plt.show()
