# -*- coding: utf-8 -*-
#!/usr/bin/env python
from collections import OrderedDict
from Tkinter import *
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

matplotlib.rcParams['figure.facecolor'] = 'white'

def stackProb(master, title, f1, f2, proportional = False):

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
        height = [0.8 for i in ind] if not proportional else proportional
        for i in range(len(fdata)):
            ax.barh(ind,fdata[i], align = 'center', height = height, color = colors[i], label = data.values()[0][i], left = pos, edgecolor = 'none')
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


def lineProb(master, title, xlabelticks, xlabel, ylabel, f1, f2):

    master.withdraw()

    f1 = f1.values()[-2]
    f2 = f2.values()[-2]

    ind = range(len(xlabelticks))
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

    ind = range(len(xlabelticks))
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

    plt.figure(1).canvas.set_window_title(title)
    plt.show()


f1 = OrderedDict([(2000.0, [200, 1000, 2500, 5000, 10000]), ('H13a1', [0.4796, 0.3215, 0.1519, 0.0435, 0.0036]), ('H13a1a', [0.0, 0.0019, 0.8224, 0.1757, 0.0]), ('H13a1a1', [0.0, 0.0, 0.0063, 0.7986, 0.1951]), ('H13a1a1a', [0.4796, 0.3215, 0.1519, 0.0435, 0.0036]), ('H13a1a1a+152', [0.006, 0.5105, 0.469, 0.0145, 0.0]), ('H13a1a1d1', [0.2124, 0.4772, 0.2662, 0.0437, 0.0006]), ('H13a1a1+9708', [0.4796, 0.3215, 0.1519, 0.0435, 0.0036]), ('H13a1a1+150', [0.4796, 0.3215, 0.1519, 0.0435, 0.0036]), ('H13a1a2', [0.4796, 0.3215, 0.1519, 0.0435, 0.0036]), ('H13a1a2a', [0.4796, 0.3215, 0.1519, 0.0435, 0.0036]), ('H13a1a2b', [0.4796, 0.3215, 0.1519, 0.0435, 0.0036]), ('H13a2', [0.4796, 0.3215, 0.1519, 0.0435, 0.0036]), ('H13a2a', [0.0, 0.0, 0.0, 0.0005, 0.9995]), ('pre-H13a2c', [0.4796, 0.3215, 0.1519, 0.0435, 0.0036]), ('H13a2c1', [0.4796, 0.3215, 0.1519, 0.0435, 0.0036]), ('H13a2c1+193+10237+249', [0.4796, 0.3215, 0.1519, 0.0435, 0.0036]), ('H13a2c1+193+249', [0.4796, 0.3215, 0.1519, 0.0435, 0.0036]), ('H13a2b', [0.0, 0.0, 0.0009, 0.1807, 0.8183]), ('H13a2b1', [0.0715, 0.5393, 0.3556, 0.0335, 0.0001]), ('H13a2b2a', [0.4796, 0.3215, 0.1519, 0.0435, 0.0036]), ('H13a2b2a+7340', [0.1305, 0.6589, 0.205, 0.0055, 0.0]), ('H13a2b5', [0.4796, 0.3215, 0.1519, 0.0435, 0.0036]), ('H13b', [0.4796, 0.3215, 0.1519, 0.0435, 0.0036]), ('H13b1+200', [0.0, 0.0008, 0.1268, 0.7641, 0.1083]), ('H13b1b', [0.0026, 0.1446, 0.504, 0.331, 0.0178]), ('H13b2', [0.4796, 0.3215, 0.1519, 0.0435, 0.0036]), ('H13c1', [0.4796, 0.3215, 0.1519, 0.0435, 0.0036]), ('H13c2', [0.4796, 0.3215, 0.1519, 0.0435, 0.0036]), ('\t', ['', '', '', '', '']), ('Mean contribution of each migration', [0.1536, 0.2165, 0.255, 0.1585, 0.2164]), ('Deviation from the mean', [0.0435, 0.0657, 0.0827, 0.0721, 0.0393])])
f2 = OrderedDict([(2000.0, [200, 1000, 2500, 5000, 10000]), ('H13a1', [0.4796, 0.3215, 0.1519, 0.0435, 0.0036]), ('H13a1a', [0.0, 0.0019, 0.8224, 0.1757, 0.0]), ('H13a1a1', [0.0, 0.0, 0.0058, 0.9687, 0.0255]), ('H13a1a1a', [0.4796, 0.3215, 0.1519, 0.0435, 0.0036]), ('H13a1a1a+152', [0.006, 0.5105, 0.469, 0.0145, 0.0]), ('H13a1a1d1', [0.2124, 0.4772, 0.2662, 0.0437, 0.0006]), ('H13a1a2', [0.0, 0.0, 0.0032, 0.3053, 0.6916]), ('H13a2', [0.0, 0.0, 0.0, 0.0136, 0.9864]), ('H13a2a', [0.0, 0.0, 0.0, 0.0005, 0.9995]), ('H13a2c1+193', [0.0, 0.0022, 0.1171, 0.6154, 0.2654]), ('H13a2b', [0.0, 0.0, 0.0, 0.3727, 0.6272]), ('H13a2b2a', [0.0, 0.0056, 0.4996, 0.4938, 0.0009]), ('H13b', [0.0, 0.0, 0.0, 0.009, 0.991]), ('H13b1+200', [0.0, 0.0, 0.0026, 0.6701, 0.3273]), ('H13c', [0.0, 0.0, 0.0001, 0.035, 0.9649]), ('\t', ['', '', '', '', '']), ('Mean contribution of each migration', [0.0221, 0.0656, 0.209, 0.3018, 0.4014]), ('Deviation from the mean', [0.0179, 0.0441, 0.0799, 0.0991, 0.072])])


## to be created in pyrho.py
master = Tk()

## call, add to nb:
#barProb(master, 'Proportion of founder lineages per migration date', f1.values()[0], 'Migration dates', 'Percentage of lineages (0-1)', f1, f2)
#lineProb(master, 'Proportion of founder lineages per migration date', f1.values()[0], 'Date', 'Percentage of lineages (0-1)', f1, f2)
stackProb(master, 'Proportions per migration date for individual lineages', f1, f2)
