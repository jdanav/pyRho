# -*- coding: utf-8 -*-
#!/usr/bin/env python

from Tkinter import *
from tree import *
import ttk, tkFileDialog, tkSimpleDialog, tkMessageBox

root = Tk()
root.title("0.7")
root.iconbitmap(default = 'favicon.ico')
root.label = ttk.Label(root, text = 'Ready')
root.label.pack(side = BOTTOM, anchor = 'w')
root.geometry('850x490')
root.minsize(850, 490)

menubar = Menu(root)

filemenu = Menu(menubar, tearoff = 0)
exportmenu = Menu(menubar, tearoff = 0)
optmenu = Menu(menubar, tearoff = 0)
compmenu = Menu(optmenu, tearoff = 0)
nb = ttk.Notebook(root)

nb.enable_traversal()
nb.pack(fill = BOTH, expand = 1)

main = Frame(nb)
f1S = Frame(nb)
f2S = Frame(nb)
clust = Frame(nb)

visible = 1

n = None


class rangeWindow(tkSimpleDialog.Dialog):

    def body(self, master):
        self.resizable(0,0)
        self.desc = Label(master, text = "Specify a valid range for the migration dates\n")
        Label(master, text="Latest:").grid(row = 1)
        Label(master, text="Earliest:").grid(row = 2)
        Label(master, text="Migration every").grid(row = 3)
        Label(master, text = " years").grid(row = 3,column = 2)

        self.e1 = Entry(master, width = 8)
        self.e2 = Entry(master, width = 8)
        self.e3 = Entry(master, width = 8)
        self.desc.grid(row = 0, columnspan = 3)
        self.e1.grid(row = 1, column = 1)
        self.e2.grid(row = 2, column = 1)
        self.e3.grid(row = 3, column = 1)
        self.e1.insert(0,'1')
        self.e2.insert(0,'10000')
        self.e3.insert(0,'1000')
        return self.e1

    def apply(self):
        start = int(self.e1.get())
        stop = int(self.e2.get())
        step = int(self.e3.get())
        self.range = range(start, stop+step, step)
        ## ensure start < stop and step < stop
        if self.range[-1] > stop: self.range.pop()


def getItem(a):

    w = root.nametowidget(root.focus_get())
    root.clipboard_clear()
    root.clipboard_append(w.item(w.focus()))
    print root.selection_get(selection = "CLIPBOARD")


def toggleLeaves():

    global visible
    if visible:
        for frame in [main, f1S, f2S]:
            try:
                t = frame.tree; t.detach(*n.leaves)
            except: pass
        visible = 0
    else:
        for frame in [main, f1S, f2S]:
            try:
                t = frame.tree; t.detach(*n.leaves)
                for item in n.leaves:
                    parent = n.tree[n.tree[item].parent]
                    t.reattach(item,parent.name,parent.children.index(item))
            except: pass
        visible = 1


for frame in [main, f1S, f2S, clust]:
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

clust.xscroll = ttk.Scrollbar(clust, orient = HORIZONTAL, command = clust.tree.xview)
clust.tree.configure(xscrollcommand = clust.xscroll.set)

main.tree['columns'] = ('Mutations','Leaves', u'ρ (Rho)', 'SE', 'Age', 'Confidence interval')
f1S.tree['columns'] = ('Mutations','Type','Leaves',u'ƒ1','SE')
f2S.tree['columns'] = ('Mutations','Type','Leaves',u'ƒ2','SE', u'ƒ2+')

for frame in [main, f1S, f2S]:
    for column in frame.tree['columns']:
        frame.tree.heading(column, text = column, anchor = 'w')
        frame.tree.column(column, width = 50, stretch = True)
    frame.tree.column('Mutations', width = 65)
main.tree.column('Confidence interval', width = 150)
main.tree.column('Age', width = 60)
f1S.tree.column('Type', width = 65)
f2S.tree.column('Type', width = 65)


nb.add(main, text = "Tree information")
nb.add(f1S, text = u"ƒ1 statistics", state = 'disabled')
nb.add(f2S, text = u"ƒ2 statistics", state = 'disabled')
nb.add(clust, text = 'Founder analysis', state = 'disabled')


def openXML():

    try:
        global n, visible, filemenu, menubar
        filename = tkFileDialog.askopenfilename(parent = root, filetypes = [('XML files', '.xml'), ('all files', '.*')])
        n = Tree(filename.encode('utf-8'))
        for i in range(1,4): nb.tab(i, state = 'disabled')
        if n.viable != 1: return
        for frame in [main, f1S, f2S]:
            frame.tree.heading("#0",text = "File path:\t%s" % filename, anchor = 'w')
            frame.tree.delete('None'); frame.tree.insert('',0,'None', open = True)
            visible = 1
        root.label['text'] = '%s internal nodes and %s leaves in %s layers' % (len(n.nodes), len(n.leaves), len(n.layers))

        i = 0
        for node in n.tree.values():
            if node.name in n.leaves:
                main.tree.insert(node.parent,'end', iid = node.name, text = node.name, tags = ('leaf'), values = (len(node.mutations), '--','--','--','--','--'))
            elif node.name in n.nodes:
                xnode = n.subtrees[node.name]
                main.tree.insert(str(node.parent),'end', iid = node.name, text = node.name, tags = ('node'), values = (len(node.mutations), len(set(xnode.keys()) & set (n.leaves)), n.Rho(node.name, xnode), n.StErr(xnode), n.Age(node.name), n.ConfidenceInterval(node.name)), open = True)
            i += 1
            sys.stdout.write('\rPopulating tree... %s/%s' % (i, len(n.tree)))
        sys.stdout.write('\n')
        for i in [1,4,5,6]: filemenu.entryconfig(i, state = "normal")
        menubar.entryconfig(2, state = "normal")
        main.tree.focus_set()
    except: sys.stdout.write('\n')


def openTypes():

    try:
        global n
        types = tkFileDialog.askopenfilename(parent = root, filetypes = [('text files', '.txt'), ('all files', '.*')])
        n.updateTypes(types.encode('utf-8'))
        i = 0
        f1S.tree.delete('None'); f1S.tree.insert('',0,'None', open = True)
        f2S.tree.delete('None'); f2S.tree.insert('',0,'None', open = True)
        for node in n.tree:
            node = n.tree[node]
            f1 = n.fN(node.name, 1)
            f2 = n.fN(node.name, 2)
            f1S.tree.insert(str(node.parent),'end', iid = node.name, text = node.name, tags = ('node' if node.name in n.nodes else 'leaf'), values = (len(node.mutations), node.isSource(), f1[0], f1[1], f1[2]), open = True)
            f2S.tree.insert(str(node.parent),'end', iid = node.name, text = node.name, tags = ('node' if node.name in n.nodes else 'leaf'), values = (len(node.mutations), node.isSource(), f2[0], f2[1], f2[2], n.f2plus(node.name)), open = True)
            i += 1
            sys.stdout.write('\rUpdating tree... %s/%s' % (i, len(n.tree)))
        sys.stdout.write('\n')
        optmenu.entryconfig(0, state = "normal")
        root.label['text'] = '%s internal nodes and %s leaves in %s layers (%s sources and %s sinks, %s undefined)' % (len(n.nodes), len(n.leaves), len(n.layers), n.nsrc, n.nsnk, n.nudf)
        for i in range(1,3): nb.tab(i, state = 'normal')
        nb.tab(3, state = 'disabled')
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
        header = ['Node','Leaves','Rho','Standard error','Age','Confidence interval',u'ƒ1 leaves',u'ƒ1 Rho',u'ƒ1 SE',u'ƒ2 leaves',u'ƒ2 Rho',u'ƒ2 SE',u'ƒ2+ eligible']
        if current == main.tree:
            header = header[:6]
            f.write('\t'.join(header))
            for node in n.nodes:
                w = [node] + [str(i) for i in main.tree.item(node)['values'][1:]]
                f.write('\n' + '\t'.join(w))
        elif current == f1S.tree:
            xna = tkMessageBox.askyesno("Save table", "Exclude non-candidate (N/A) nodes?")
            header = [header[0]] + header[6:9]
            f.write('\t'.join(header))
            for node in n.nodes:
                w = [node] + [str(i) for i in f1S.tree.item(node)['values'][2:]]
                if xna == True and 'N/A' in w: pass
                else: f.write('\n' + '\t'.join(w))
        elif current == f2S.tree:
            xna = tkMessageBox.askyesno("Save table", "Exclude non-candidate (N/A) nodes?")
            header = [header[0]] + header[9:]
            f.write('\t'.join(header))
            for node in n.nodes:
                if xna == True and 'N/A' in w: pass
                else: f.write('\n' + '\t'.join(w))
        else:
            f.write('Node ID\t')
            header = clust.tree['columns']
            f.write('\t'.join(header))
            for node in n.nodes:
                if clust.tree.exists(node):
                    w = [node] + [str(i) for i in clust.tree.item(node)['values']]
                    f.write('\n' + '\t'.join(w))
            x = 'Mean contribution of each migration'
            w = [x] + [str(i) for i in clust.tree.item(x)['values']]
            f.write('\n\n' + '\t'.join(w))
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


def calcMigs(fv = 1):

    rof = tkMessageBox.askyesno("Migration dates", "Would you like to specify a range?")
    if rof == True:
        try:
            _ = Tk()
            _.withdraw()
            migrations = rangeWindow(_,title = "Migration dates").range
        except: return
    else:
        try:
            howmany = tkSimpleDialog.askinteger(parent = root, title = 'Migration dates', prompt = 'How many migrations?')
            migrations = [tkSimpleDialog.askinteger(parent = root, title = 'Migration dates', prompt = 'Input date %s' % (i+1), initialvalue = '%s' % ((i+1) * 1000)) for i in range(howmany)]
            ## ensure all migration dates are different (set?)
        except: return
    mutationRate = tkSimpleDialog.askfloat(parent = root, title = 'Mutation rate', prompt = 'Input the mutation rate', initialvalue = '1000')
    probs = n.migrationProbs(migrations,mutationRate, fv)
    clust.tree.delete('None'); clust.tree.insert('',0,'None', open = True)
    clust.tree.heading("#0",text = "Mutation rate: %s" % probs.keys()[0], anchor = 'w')
    clust.scroll.pack(side = RIGHT, fill = BOTH)
    clust.xscroll.pack(side = BOTTOM, fill = BOTH)
    clust.tree['columns'] = [str(i) for i in probs.values()[0]]
    for column in clust.tree['columns']:
        colwidth = int(clust.tree.winfo_width()) - int(clust.tree.column('#0')['width']) - 1
        if len(clust.tree['columns']) * 50 <= colwidth:
            clust.tree.column(column, width = colwidth/len(clust.tree['columns']), stretch = True)
        else: clust.tree.column(column, width = 50, stretch = True)
        clust.tree.heading(column, text = column, anchor = 'w')
    for item in probs.keys()[1:]:
        clust.tree.insert('None','end', iid = item, text = item, values = [str(i) for i in probs[item]], open = True)
    nb.tab(3, state = 'normal')


def calcMigsF2():

    calcMigs(fv = 2)


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
        while nodes < (maxnodes - 1): # closes > sqrt(maxnodes)*0.75
            nl = randint(-5000,5000) if closes > 10 and last[-3] == '/' \
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


def findNode():

    global n, visible
    current = root.nametowidget(root.focus_get())
    try:
        nid = tkSimpleDialog.askstring(parent = root, title = 'Select node', prompt = 'Input a valid Node ID')
        if nid in n.leaves and visible == 0: nid = n.tree[nid].parent
        current.see(nid)
        current.selection_set(nid)
    except: pass


optmenu.add_cascade(label = "Compute migration clusters", menu = compmenu)

compmenu.add_command(label = u"ƒ1", command = calcMigs)
compmenu.add_command(label = u"ƒ2", command = calcMigsF2)

optmenu.add_separator()
optmenu.add_command(label = "Show/Hide leaves", command = toggleLeaves)
optmenu.add_command(label = "Find node", command = findNode)
optmenu.entryconfig(0, state = "disabled")

filemenu.add_command(label = "Open XML file", command = openXML)
filemenu.add_command(label = "Import node types", command = openTypes)
filemenu.add_command(label = "Generate random tree", command = genXML)
filemenu.entryconfig(1, state = "disabled")
filemenu.add_separator()
filemenu.add_command(label = "Export tree (Newick format)", command = exportNewick)
filemenu.add_command(label = "Save current table (TSV)", command = saveTable)
filemenu.add_command(label = "Save all statistics (TSV)", command = saveAll)
filemenu.entryconfig(4, state = "disabled")
filemenu.entryconfig(5, state = "disabled")
filemenu.entryconfig(6, state = "disabled")
filemenu.add_separator()
filemenu.add_command(label = "Quit", command = root.destroy)

menubar.add_cascade(label = "File", menu = filemenu)
menubar.add_cascade(label = "Options", menu = optmenu)
menubar.entryconfig(2, state = "disabled")

root.config(menu = menubar)
root.mainloop()
