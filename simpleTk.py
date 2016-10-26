#!/usr/bin/env python

from Tkinter import *
import ttk
from stats import *
import tkFileDialog


class Viewer(Frame):

    def __init__(self, master):

        Frame.__init__(self, root)
        
        self.tree = ttk.Treeview(root, height = 20, columns = \
                    ('Mutations', 'Status', 'Rho', 'Age', \
                     'SE', 'Confidence interval'))
        self.tree.column("#0",minwidth = 350, width = 600)
        self.scroll = ttk.Scrollbar( root, orient=VERTICAL, \
                                     command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scroll.set)

        for column in self.tree['columns']:
            self.tree.heading(column, text=column, anchor= 'w')
            self.tree.column(column, width = 65)
        self.tree.column('Confidence interval', width = 150)
        self.tree.insert('',0,'None', open = True)


        for node in n.tree.values():
            if node.name in n.leaves:
                self.tree.insert(node.parent,'end', \
                                 iid = node.name, text = node.name, \
                            values = (len(node.mutations), \
                                      node.isSource(),'--','--','--','--'))
            elif node.name in n.nodes:
                xnode = Tree(node.name,n.subtree(node.name))
                self.tree.insert(str(node.parent),'end', iid = node.name, \
                                 text = node.name, values = (len(node.mutations), \
                                    node.isSource(), Rho(xnode)[1], Age(xnode)[1], \
                            StDev(xnode)[1], ConfidenceInterval(xnode)), open = True)

        self.label = ttk.Label(root, text= '%s nodes and %s leaves in %s layers' % \
                               (len(n.nodes), len(n.leaves), len(n.layers)))

        self.label.grid(row = 1, sticky=(W))
        self.scroll.grid(row = 0, column = 1, sticky=(N,S))
        self.tree.grid(row = 0, column = 0)
        

root = Tk()
root.title("PyRHO")

filename = tkFileDialog.askopenfilename(parent = root)
n = Tree("",str(filename))

Viewer(root)
root.mainloop()
