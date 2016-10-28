# -*- coding: utf-8 -*-
#!/usr/bin/env python

from Tkinter import *
import ttk
from stats import *
import tkFileDialog
from copy import copy


root = Tk()
root.title("PyRHO")

filename = tkFileDialog.askopenfilename(parent = root)
types = tkFileDialog.askopenfilename(parent = root)
n = Tree(str(filename),str(filename), str(types))

nb = ttk.Notebook(root)
nb.pack()

main = Frame(nb)
f1S = Frame(nb)
f2S = Frame(nb)

for frame in [main, f1S, f2S]:

    frame.tree = ttk.Treeview(frame, height = 20, columns = \
                ('Mutations', 'Type', 'Leaves', u'ρ (Rho)', 'SE', \
                 'Age', 'Confidence interval', 'Leaves f1', 'f1', \
                 'SE f1', 'Leaves f2', 'f2', 'SE f2'))
    frame.tree.column("#0",minwidth = 350, width = 400)
    frame.scroll = ttk.Scrollbar(frame, orient=VERTICAL, \
                                 command=frame.tree.yview)

    frame.tree.configure(yscrollcommand=frame.scroll.set)

    frame.label = ttk.Label(frame, text= \
                            '%s nodes and %s leaves in %s layers' % \
                           (len(n.nodes), len(n.leaves), len(n.layers)))

    for column in frame.tree['columns']:
        frame.tree.heading(column, text=column, anchor= 'w')
        frame.tree.column(column, width = 50)
    frame.tree.column('Age', width = 60)
    frame.tree.column('Mutations', width = 65)
    frame.tree.column('Confidence interval', width = 150)
    frame.tree.column('Type', width = 65)
    frame.tree.insert('',0,'None', open = True)


    for node in n.tree.values():
        if node.name in n.leaves:
            frame.tree.insert(node.parent,'end', \
                             iid = node.name, text = node.name, \
                        values = (len(node.mutations), \
                                  node.isSource(),'--','--','--','--','--',\
                                  '--','--','--','--','--','--'))
        elif node.name in n.nodes:
            f1 = fN(n, node.name, 1)
            f2 = fN(n, node.name, 2)
            xnode = Tree(node.name,n.subtree(node.name))
            frame.tree.insert(str(node.parent),'end', iid = node.name, \
                             text = node.name, values = (len(node.mutations), \
                                (node.isSource() if node.children == [] else node.type),\
                                Rho(xnode)[1], Rho(xnode)[2], \
                                StDev(xnode)[1], Age(xnode)[1], \
                                ConfidenceInterval(xnode), f1[0][1],\
                                f1[0][2], f1[1][1], f2[0][1], \
                                f2[0][2], f2[1][1]), open = True)

    frame.label.grid(row = 1, sticky=(W))
    frame.scroll.grid(row = 0, column = 1, sticky=(N,S))
    frame.tree.grid(row = 0, column = 0)

main.tree["displaycolumns"] = ('Mutations','Leaves',u'ρ (Rho)', 'SE', 'Age', 'Confidence interval')

f1S.tree["displaycolumns"] = ('Mutations','Type','Leaves f1','f1','SE f1')
f1S.tree.heading('Leaves f1', text='Leaves', anchor= 'w')
f1S.tree.heading('SE f1', text='SE', anchor= 'w')

f2S.tree["displaycolumns"] = ('Mutations','Type','Leaves f2','f2','SE f2')
f2S.tree.heading('Leaves f2', text='Leaves', anchor= 'w')
f2S.tree.heading('SE f2', text='SE', anchor= 'w')

nb.add(main, text = "Tree information")
nb.add(f1S, text = "f1 statistics")
nb.add(f2S, text = "f2 statistics")

root.mainloop()

