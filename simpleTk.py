#!/usr/bin/env python

from Tkinter import *
import ttk
from stats import *
import tkFileDialog


root = Tk()
root.title("Tree viewer")

filename = tkFileDialog.askopenfilename(parent = root)
n = Tree("",str(filename))

tree = ttk.Treeview(root, height = 20, columns = \
                    ('Mutations', 'Rho', 'Age', \
                     'Standard error', 'Confidence interval'))
tree.column("#0",minwidth = 350, width = 600)
for column in tree['columns']:
    tree.heading(column, text=column, anchor= 'w')
    tree.column(column, width = len(column) * 15)
tree.insert('',0,'None', open = True)


for node in n.tree.values():
    if node.name in n.leaves:
        tree.insert(node.parent,'end',iid = node.name, text = node.name, \
                    values = (len(node.mutations),'--','--','--','--'))
    elif node.name in n.nodes:
        xnode = Tree(node.name,n.subtree(node.name))
        op = False
        for child in node.children:
            if child in n.nodes: op = True; break
        tree.insert(str(node.parent),'end', iid = node.name, text = node.name, \
                    values = (len(node.mutations), Rho(xnode)[1], Age(xnode)[1], \
                    StDev(xnode)[1], ConfidenceInterval(xnode)), open = op)

tree.grid()
root.mainloop()
