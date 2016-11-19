# -*- coding: utf-8 -*-
#!/usr/bin/env python

from Tkinter import *
from tree import *
import ttk, tkFileDialog


root = Tk()
root.title("0.66")

menubar = Menu(root)

filemenu = Menu(menubar, tearoff = 0)
exportmenu = Menu(menubar, tearoff = 0)
viewmenu = Menu(menubar, tearoff = 0)
nb = ttk.Notebook(root)
nb.enable_traversal()
nb.pack(fill = BOTH, expand = 1)

main = Frame(nb)
f1S = Frame(nb)
f2S = Frame(nb)

visible = 1

n = None

def getItem(a):
    
    w = root.nametowidget(root.focus_get())
    root.clipboard_clear()
    root.clipboard_append(w.item(w.focus()))
    print root.selection_get(selection = "CLIPBOARD")


def toggleLeaves():
    
    global visible
    if visible: 
        for frame in [main, f1S, f2S]:
            t = frame.tree; t.detach(*n.leaves)
        visible = 0

    else:
        for frame in [main, f1S, f2S]:
            t = frame.tree; t.detach(*n.leaves)
            for item in n.leaves:
                parent = n.tree[n.tree[item].parent]
                t.reattach(item,parent.name,parent.children.index(item))
        visible = 1


for frame in [main, f1S, f2S]:

    frame.tree = ttk.Treeview(frame, height = 20);
    frame.tree.column("#0",minwidth = 350, width = 400)
    frame.scroll = ttk.Scrollbar(frame, orient = VERTICAL, command = frame.tree.yview)
    frame.tree.bind('<Control-c>', getItem)
    frame.tree.configure(yscrollcommand = frame.scroll.set)
    frame.tree['selectmode'] = 'extended'
    frame.label = ttk.Label(frame, text = '%s nodes and %s leaves in %s layers' % (0,0,0))
    frame.tree.insert('',0,'None', open = True)
    frame.tree.heading("#0",text = "File path:\t%s" % '', anchor = 'w')

    frame.label.pack(side = BOTTOM, anchor = 'w')
    frame.scroll.pack(side = RIGHT, fill = BOTH)
    frame.tree.pack(fill = BOTH, expand = 1)

    frame.tree.tag_configure('leaf', background = '#ffffe0')
    frame.tree.tag_configure('node', background = '#ffffff')
     
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
        global n, visible, filemenu, menubar
        filename = tkFileDialog.askopenfilename(parent = root)
        n = Tree(str(filename))

        for frame in [main, f1S, f2S]:
            frame.label['text'] = '%s nodes and %s leaves in %s layers' % (len(n.nodes), len(n.leaves), len(n.layers))
            frame.tree.heading("#0",text = "File path:\t%s" % filename, anchor = 'w')
            frame.tree.delete('None')
            frame.tree.insert('',0,'None', open = True)
            visible = 1            

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
            sys.stdout.write('\rPopulating tree... %.2f%%' % (float(i)/len(n.tree)*100))
        print '\n'
        filemenu.entryconfig(1, state = "normal")
        viewmenu.entryconfig(1, state = "normal")
        menubar.entryconfig(3, state = "normal")
        main.tree.focus_set()
        
    except: pass
    

def openTypes():

    try:
        global n
        types = tkFileDialog.askopenfilename(parent = root)
        n.updateTypes(str(types))
        i = 0.0
        for node in n.nodes:
            node = n.tree[node]
            f1 = n.fN(node.name, 1)
            f2 = n.fN(node.name, 2)
            f1S.tree.item(node.name, values = (len(node.mutations), node.isSource(), f1[0], f1[1], f1[2]))
            f2S.tree.item(node.name, values = (len(node.mutations), node.isSource(), f2[0], f2[1], f2[2], n.f2plus(node.name)))
            i += 1
            sys.stdout.write('\rUpdating tree... %.2f%%' % ((i/(len(n.nodes)))*100))
        print '\n'
    except: pass

        
def exportNewick():

    save = tkFileDialog.asksaveasfilename(parent = root)
    try: f = open(save, 'w'); f.write(n.Newick(None)); f.close()
    except: pass

def exportCurrent(): pass


def exportAll(): pass
    

exportmenu.add_command(label = "Current table (CSV)", command = exportCurrent)
exportmenu.add_command(label = "Full table (CSV)", command = exportAll)
exportmenu.add_command(label = "Tree (Newick format)", command = exportNewick)

viewmenu.insert_command(1, label = "Show/Hide leaves", command = toggleLeaves)
viewmenu.entryconfig(1, state = "disabled")

filemenu.add_command(label = "Open XML file", command = openXML)
filemenu.insert_command(1, label = "Import node types", command = openTypes)
filemenu.entryconfig(1, state = "disabled")
filemenu.add_separator()
filemenu.add_command(label = "Quit", command = root.destroy)

menubar.add_cascade(label = "File", menu = filemenu)
menubar.add_cascade(label = "View", menu = viewmenu)
menubar.add_cascade(label = "Export", menu = exportmenu)
menubar.entryconfig(3, state = "disabled")

root.config(menu = menubar)
root.mainloop()
