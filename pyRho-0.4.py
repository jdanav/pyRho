# -*- coding: utf-8 -*-
#!/usr/bin/env python

from Tkinter import *
from stats import *
import ttk, tkFileDialog


root = Tk()
root.title("PyRHO 0.4")
root.option_add('*tearOff', FALSE)


filename = tkFileDialog.askopenfilename(parent = root)
types = tkFileDialog.askopenfilename(parent = root)
n = Tree(str(filename), str(types))

nb = ttk.Notebook(root)
nb.pack()

main = Frame(nb)
f1S = Frame(nb)
f2S = Frame(nb)

for frame in [main, f1S, f2S]:

    frame.tree = ttk.Treeview(frame, height = 20)
    frame.tree.column("#0",minwidth = 350, width = 400)
    frame.scroll = ttk.Scrollbar(frame, orient=VERTICAL, \
                                 command=frame.tree.yview)

    frame.tree.configure(yscrollcommand=frame.scroll.set)

    frame.label = ttk.Label(frame, text= \
                            '%s nodes and %s leaves in %s layers' % \
                           (len(n.nodes), len(n.leaves), len(n.layers)))
    
    frame.tree.insert('',0,'None', open = True)
    frame.tree.heading("#0",text="File path:\t%s" % filename, anchor = 'w')

    frame.label.grid(row = 1, sticky=(W))
    frame.scroll.grid(row = 0, column = 1, sticky=(N,S))
    frame.tree.grid(row = 0, column = 0)

    
main.tree['columns'] = ('Mutations','Leaves', u'ρ (Rho)', 'SE', 'Age', \
                        'Confidence interval')
for column in main.tree['columns']:
    main.tree.heading(column, text=column, anchor= 'w')
    main.tree.column(column, width = 50, stretch = True)
main.tree.column('Age', width = 60)
main.tree.column('Mutations', width = 65)
main.tree.column('Confidence interval', width = 150)

for node in n.tree.values():
    if node.name in n.leaves:
        main.tree.insert(node.parent,'end', \
                         iid = node.name, text = node.name, \
                    values = (len(node.mutations), '--','--','--','--','--'))
    elif node.name in n.nodes:
        xnode = Tree(n.subtree(node.name))
        main.tree.insert(str(node.parent),'end', iid = node.name, \
                         text = node.name, values = (len(node.mutations), \
                                            len(xnode.leaves), Rho(xnode), \
                                            StErr(xnode), Age(xnode), \
                                            ConfidenceInterval(xnode)), open = True)


    
f1S.tree['columns'] = ('Mutations','Type','Leaves','f1','SE')
for column in f1S.tree['columns']:
    f1S.tree.heading(column, text=column, anchor= 'w')
    f1S.tree.column(column, width = 50, stretch = True)
f1S.tree.column('Type', width = 65)
f1S.tree.column('Mutations', width = 65)

for node in n.tree.values():
    if node.name in n.leaves:
        f1S.tree.insert(node.parent,'end', \
                         iid = node.name, text = node.name, \
                    values = (len(node.mutations), node.isSource(),'--','--','--'))
    elif node.name in n.nodes:
        f1 = fN(n, node.name, 1)
        xnode = Tree(n.subtree(node.name))
        f1S.tree.insert(str(node.parent),'end', iid = node.name, \
                         text = node.name, values = (len(node.mutations), node.isSource(), \
                                                     f1[0], f1[1], f1[2]), open = True)



f2S.tree['columns'] = ('Mutations','Type','Leaves','f2','SE')
for column in f2S.tree['columns']:
    f2S.tree.heading(column, text=column, anchor= 'w')
    f2S.tree.column(column, width = 50, stretch = True)
f2S.tree.column('Type', width = 65)
f2S.tree.column('Mutations', width = 65)

for node in n.tree.values():
    if node.name in n.leaves:
        f2S.tree.insert(node.parent,'end', \
                         iid = node.name, text = node.name, \
                    values = (len(node.mutations), node.isSource(),'--','--','--'))
    elif node.name in n.nodes:
        f2 = fN(n, node.name, 2)
        xnode = Tree(n.subtree(node.name))
        f2S.tree.insert(str(node.parent),'end', iid = node.name, \
                         text = node.name, values = (len(node.mutations), node.isSource(), \
                                                     f2[0], f2[1], f2[2]), open = True)


nb.add(main, text = "Tree information")
nb.add(f1S, text = "f1 statistics")
nb.add(f2S, text = "f2 statistics")

root.mainloop()
