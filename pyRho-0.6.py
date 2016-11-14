# -*- coding: utf-8 -*-
#!/usr/bin/env python

from Tkinter import *
from tree import *
import ttk, tkFileDialog


root = Tk()
root.title("0.6")

menubar = Menu(root)

filemenu = Menu(menubar, tearoff = 0)

nb = ttk.Notebook(root)
nb.enable_traversal()
nb.pack(fill = BOTH, expand = 1)

main = Frame(nb)
f1S = Frame(nb)
f2S = Frame(nb)

n = None

for frame in [main, f1S, f2S]:

    frame.tree = ttk.Treeview(frame, height = 20)
    frame.tree.column("#0",minwidth = 350, width = 400)
    frame.scroll = ttk.Scrollbar(frame, orient = VERTICAL, command = frame.tree.yview)

    frame.tree.configure(yscrollcommand = frame.scroll.set)
    frame.tree['selectmode'] = 'extended'

    frame.label = ttk.Label(frame, text = '%s nodes and %s leaves in %s layers' % (0,0,0))
    frame.tree.insert('',0,'None', open = True)
    frame.tree.heading("#0",text = "File path:\t%s" % '', anchor = 'w')

    frame.label.pack(side = BOTTOM, anchor = 'w')
    frame.scroll.pack(side = RIGHT, fill = BOTH)
    frame.tree.pack(fill = BOTH, expand = 1)

    frame.tree.tag_configure('leaf', background = '#ffffff')
    frame.tree.tag_configure('node', background = '#ffffe0')
     
main.tree['columns'] = ('Mutations','Leaves', u'ρ (Rho)', 'SE', 'Age', 'Confidence interval')
for column in main.tree['columns']:
    main.tree.heading(column, text=column, anchor = 'w')
    main.tree.column(column, width = 50, stretch = True)
main.tree.column('Age', width = 60)
main.tree.column('Mutations', width = 65)
main.tree.column('Confidence interval', width = 150)

f1S.tree['columns'] = ('Mutations','Type','Leaves','f1','SE')
for column in f1S.tree['columns']:
    f1S.tree.heading(column, text = column, anchor = 'w')
    f1S.tree.column(column, width = 50, stretch = True)
f1S.tree.column('Type', width = 65)
f1S.tree.column('Mutations', width = 65)

f2S.tree['columns'] = ('Mutations','Type','Leaves','f2','SE', 'f2+')
for column in f2S.tree['columns']:
    f2S.tree.heading(column, text = column, anchor = 'w')
    f2S.tree.column(column, width = 50, stretch = True)
f2S.tree.column('Type', width = 65)
f2S.tree.column('Mutations', width = 65)

nb.add(main, text = "Tree information")
nb.add(f1S, text = "f1 statistics")
nb.add(f2S, text = "f2 statistics")

        
def openXML():

    try:
        global n, filemenu
        filename = tkFileDialog.askopenfilename(parent = root)
        n = Tree(str(filename))

        for frame in [main, f1S, f2S]:
            frame.label['text'] = '%s nodes and %s leaves in %s layers' % (len(n.nodes), len(n.leaves), len(n.layers))
            frame.tree.heading("#0",text = "File path:\t%s" % filename, anchor = 'w')
            frame.tree.delete('None')
            frame.tree.insert('',0,'None', open = True)

        i = 0
        for node in n.tree.values():

            if node.name in n.leaves:
                main.tree.insert(node.parent,'end', iid = node.name, text = node.name, tags = ('leaf'), values = (len(node.mutations), '--','--','--','--','--'))
                f1S.tree.insert(node.parent,'end', iid = node.name, text = node.name, tags = ('leaf'), values = (len(node.mutations), node.isSource(),'--','--','--'))
                f2S.tree.insert(node.parent,'end', iid = node.name, text = node.name, tags = ('leaf'), values = (len(node.mutations), node.isSource(),'--','--','--', '--'))
            elif node.name in n.nodes:
                xnode = n.subtrees[node.name]
                f1 = n.fN(node.name, 1)
                f2 = n.fN(node.name, 2)
                main.tree.insert(str(node.parent),'end', iid = node.name, text = node.name, tags = ('node'), values = (len(node.mutations), len(set(xnode.keys()) & set (n.leaves)), n.Rho(node.name, xnode), n.StErr(xnode), n.Age(node.name), n.ConfidenceInterval(node.name)), open = True)
                f1S.tree.insert(str(node.parent),'end', iid = node.name, text = node.name, tags = ('node'), values = (len(node.mutations), '--', f1[0], f1[1], f1[2]), open = True)
                f2S.tree.insert(str(node.parent),'end', iid = node.name, text = node.name, tags = ('node'), values = (len(node.mutations), '--', f2[0], f2[1], f2[2], n.f2plus(node.name)), open = True)
            i += 1
            sys.stdout.write('\rWriting to window... %.0f%%' % (float(i)/len(n.tree)*100))
        print '\n'
        filemenu.entryconfig(1, state="normal")
    except: print
    

def openTypes():

    try:
        global n
        notebook = root.winfo_children()[1]
        frames = notebook.winfo_children()
        types = tkFileDialog.askopenfilename(parent = root)
        n.updateTypes(str(types))
        i = 0.0
        for node in n.tree.values():
            if node.name in n.leaves:
                frames[1].winfo_children()[0].item(node.name, values = (len(node.mutations), node.isSource(),'--','--','--', '--'))
                frames[2].winfo_children()[0].item(node.name, values = (len(node.mutations), node.isSource(),'--','--','--', '--'))
            else:
                f1 = n.fN(node.name, 1)
                f2 = n.fN(node.name, 2)
                frames[1].winfo_children()[0].item(node.name, values = (len(node.mutations), node.isSource(), f1[0], f1[1], f1[2]))
                frames[2].winfo_children()[0].item(node.name, values = (len(node.mutations), node.isSource(), f2[0], f2[1], f2[2], n.f2plus(node.name)))
            i += 1
        print '\n'
    except: print
    
filemenu.add_command(label = "Open XML file", command = openXML)
filemenu.insert_command(1, label = "Import node types", command = openTypes)
filemenu.entryconfig(1, state="disabled")

filemenu.add_separator()
filemenu.add_command(label = "Quit", command = root.destroy)
menubar.add_cascade(label = "File", menu = filemenu)

root.config(menu = menubar)
root.mainloop()
