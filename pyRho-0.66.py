# -*- coding: utf-8 -*-
#!/usr/bin/env python

from Tkinter import *
from tree import *
import ttk, tkFileDialog, tkSimpleDialog


root = Tk()
root.title("0.66")
root.iconbitmap(default = 'favicon.ico')
root.label = ttk.Label(root, text = '--')
root.label.pack(side = BOTTOM, anchor = 'w')

menubar = Menu(root)

filemenu = Menu(menubar, tearoff = 0)
exportmenu = Menu(menubar, tearoff = 0)
optmenu = Menu(menubar, tearoff = 0)
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
    frame.tree.insert('',0,'None', open = True)
    frame.tree.heading("#0",text = "File path:\t%s" % '', anchor = 'w')
    frame.scroll.pack(side = RIGHT, fill = BOTH)
    frame.tree.pack(fill = BOTH, expand = 1)
    frame.tree.tag_configure('leaf', background = '#ffffe0')
     
main.tree['columns'] = ('Mutations','Leaves', u'ρ (Rho)', 'SE', 'Age', 'Confidence interval')
for column in main.tree['columns']:
    main.tree.heading(column, text=column, anchor = 'w')
    main.tree.column(column, width = 50, stretch = True)
main.tree.column('Age', width = 60)
main.tree.column('Mutations', width = 65)
main.tree.column('Confidence interval', width = 150)

f1S.tree['columns'] = ('Mutations','Type','Leaves','f1','SE')
f2S.tree['columns'] = ('Mutations','Type','Leaves','f2','SE', 'f2+')
for frame in [f1S,f2S]:
    for column in frame.tree['columns']:
        frame.tree.heading(column, text = column, anchor = 'w')
        frame.tree.column(column, width = 50, stretch = True)
    frame.tree.column('Type', width = 65)
    frame.tree.column('Mutations', width = 65)
    
nb.add(main, text = "Tree information")
nb.add(f1S, text = "f1 statistics")
nb.add(f2S, text = "f2 statistics")

        
def openXML():

    try:
        global n, visible, filemenu, menubar
        filename = tkFileDialog.askopenfilename(parent = root, filetypes = [('XML files', '.xml'), ('all files', '.*')])
        n = Tree(str(filename))

        for frame in [main, f1S, f2S]:
            frame.tree.heading("#0",text = "File path:\t%s" % filename, anchor = 'w')
            frame.tree.delete('None'); frame.tree.insert('',0,'None', open = True)
            visible = 1            
        root.label['text'] = '%s nodes and %s leaves in %s layers' % (len(n.nodes), len(n.leaves), len(n.layers))

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
            sys.stdout.write('\rPopulating tree... %s/%s' % (i, len(n.tree)))
        sys.stdout.write('\n')
        for i in [1,4,5]: filemenu.entryconfig(i, state = "normal")
        menubar.entryconfig(2, state = "normal")
        main.tree.focus_set()
    except: sys.stdout.write('\n')
    

def openTypes():

    try:
        global n
        types = tkFileDialog.askopenfilename(parent = root, filetypes = [('text files', '.txt'), ('all files', '.*')])
        n.updateTypes(str(types))
        i = 0
        for node in n.tree:
            node = n.tree[node]
            f1 = n.fN(node.name, 1)
            f2 = n.fN(node.name, 2)
            f1S.tree.item(node.name, values = (len(node.mutations), node.isSource(), f1[0], f1[1], f1[2]))
            f2S.tree.item(node.name, values = (len(node.mutations), node.isSource(), f2[0], f2[1], f2[2], n.f2plus(node.name)))
            i += 1
            sys.stdout.write('\rUpdating tree... %s/%s' % (i, len(n.tree)))
        sys.stdout.write('\n')
        root.label['text'] = '%s nodes and %s leaves in %s layers (%s sources and %s sinks, %s undefined)' % (len(n.nodes), len(n.leaves), len(n.layers), n.nsrc, n.nsnk, n.nudf)
    except: sys.stdout.write('\n')

        
def exportNewick():

    global n
    save = tkFileDialog.asksaveasfilename(parent = root, initialfile = "%s_newick.txt" % n.root.name)
    try: f = open(save, 'w'); f.write(n.Newick(None)); f.close()
    except: pass


def saveTable():

    global n
    current = root.nametowidget(root.focus_get())
    save = tkFileDialog.asksaveasfilename(parent = root, initialfile = "%s_table.txt" % n.root.name)
    try:
        f = open(save,'w')
        header = ['Node','Leaves','Rho','Standard error','Age','Confidence interval','f1 leaves','f1 Rho','f1 SE','f2 leaves','f2 Rho','f2 SE','f2+ eligible']
        if current == main.tree:
            header = header[:6]
            f.write('\t'.join(header))
            for node in n.nodes:
                w = [node] + [str(i) for i in main.tree.item(node)['values'][1:]]
                f.write('\n' + '\t'.join(w))
        elif current == f1S.tree:
            header = [header[0]] + header[6:9]
            f.write('\t'.join(header))
            for node in n.nodes:
                w = [node] + [str(i) for i in f1S.tree.item(node)['values'][2:]]
                f.write('\n' + '\t'.join(w))
        else:
            header = [header[0]] + header[9:]
            f.write('\t'.join(header))
            for node in n.nodes:
                w = [node] + [str(i) for i in f2S.tree.item(node)['values'][2:]]
                f.write('\n' + '\t'.join(w))
        f.close()
        sys.stdout.write('%s successfully created\n' % (save))
    except: sys.stdout.write('\n')
    
            
def saveAll():

    global n
    save = tkFileDialog.asksaveasfilename(parent = root, initialfile = "%s_table.txt" % n.root.name)
    try:
        f = open(save,'w')
        f.write('\t'.join(['Node','Leaves','Rho','Standard error','Age','Confidence interval','f1 leaves','f1 Rho','f1 SE','f2 leaves','f2 Rho','f2 SE','f2+ eligible']))
        for node in n.nodes:
            w = [node] + [str(i) for i in main.tree.item(node)['values'][1:]] + [str(i) for i in f1S.tree.item(node)['values'][2:]] + [str(i) for i in f2S.tree.item(node)['values'][2:]]
            f.write('\n' + '\t'.join(w))
        f.close()
        sys.stdout.write('%s successfully created\n' % (save))
    except: sys.stdout.write('\n')

    
def genXML():

    try:
        maxnodes = tkSimpleDialog.askinteger(parent = root, title = 'Number of nodes', prompt = 'Input an integer greater than one')
        if maxnodes < 2: return
        filename = tkFileDialog.asksaveasfilename(parent = root, initialfile = "autogen.xml")
        from random import randint
        closes = 1; nodes = 1
        f = open(filename, 'w')
        last = '<Node Id="NoLabel" HG="%s">\n' % ','.join(['x' for i in range(randint(0,12))])
        f.write(last)
        subtree = True
        while nodes < (maxnodes - 1):
            nl = randint(-1000,1000) if closes > (sqrt(maxnodes)*0.75) and last[-3] == '/' \
                 else (randint(-2,1) if last[-3] == '"' \
                       else (randint(-2,6) if closes > 1 \
                             else 1))
            if nl <= 0:
                last = '\t' * closes + '<Node Id="NoLabel" HG="%s" />\n' % ','.join(['x' for i in range(randint(0,6))])
                nodes += 1
            elif nl in [1,2,3]:
                last = '\t' * closes + '<Node Id="NoLabel" HG="%s">\n' % ','.join(['x' for i in range(randint(0,6))])
                closes += 1; nodes += 1
            else:
                closes -= 1
                last = '\t' * closes + '</Node>\n'
            f.write(last)
        if last[-3] == '"':
            f.write('\t' * closes + '<Node Id="NoLabel" HG="%s" />\n' % ','.join(['x' for i in range(randint(0,6))]))
        while closes > 0:
            f.write('\t' * (closes-1) + '</Node>\n')
            closes -= 1
        f.close()
    except: sys.stdout.write('\n')

    
optmenu.add_command(label = "Export tree (Newick format)", command = exportNewick)
optmenu.add_command(label = "Show/Hide leaves", command = toggleLeaves)

filemenu.add_command(label = "Open XML file", command = openXML)
filemenu.add_command(label = "Import node types", command = openTypes)
filemenu.add_command(label = "Generate random tree", command = genXML)
filemenu.entryconfig(1, state = "disabled")
filemenu.add_separator()
filemenu.add_command(label = "Save current table (TSV)", command = saveTable) 
filemenu.add_command(label = "Save all (TSV)", command = saveAll) 
filemenu.entryconfig(4, state = "disabled")
filemenu.entryconfig(5, state = "disabled")
filemenu.add_separator()
filemenu.add_command(label = "Quit", command = root.destroy)

menubar.add_cascade(label = "File", menu = filemenu)
menubar.add_cascade(label = "Options", menu = optmenu)
menubar.entryconfig(2, state = "disabled")

root.config(menu = menubar)
root.mainloop()
