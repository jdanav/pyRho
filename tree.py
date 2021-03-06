# -*- coding: utf-8 -*-

import re
from collections import defaultdict as ddict, OrderedDict as odict
from copy import copy
from math import sqrt, exp, log

class Node:

    def __init__(self, name, parent, mutations, layer):

        self.name = name
        self.parent = parent
        self.children = []
        self.mutations = mutations.split(',') if mutations else []
        self.layer = layer
        self.type = [0,0,0,0]
        self.extra = {i:'--' for i in ('Rho','Age','SE','CI')}


    def isSource(self):

        t = self.type
        if self.children == []:
            return {'[0, 0, 1, 0]':'Sink',
                    '[1, 0, 0, 0]':'Source','[0, 1, 0, 0]':'Source',
                    '[0, 0, 0, 1]':'Undefined','[0, 0, 0, 0]':'Undefined'}[str(t)]
        else: return t


class Tree:

    def __init__(self, source):

        self.tree = odict()
        self.nodes = []
        self.leaves = []
        self.layers = odict()
        self.noLabel = 0
        self.subtrees = {}
        self.viable = 0
        self.buildTree(source)
        self.root = self.tree.values()[0]


    def buildTree(self, source):

        if type(source) == str:
            f = open(source,'r')
            layers, l = ddict(list), 1
            layers[0] = None
            F = f.readlines(); f.close()
            Fl = len(F)
            for i in xrange(Fl):
                match = re.search('Id=(.*) HG=(.*)>', F[i])
                if "/Node" in F[i]: l -= 1
                elif match is None: pass
                else:
                    node = Node(match.group(1).strip('" '), layers[l-1], match.group(2).strip('" /,'), l)
                    if node.name == "NoLabel":
                        self.noLabel += 1
                        node.name = node.name + "_%s" % self.noLabel
                    if node.name in self.tree:
                        self.viable = [node.name, i+1]
                        return
                    self.tree[node.name] = node
                    if l >= 2: self.tree[layers[l-1]].children.append(node.name)
                    if not node.layer in self.layers:
                        self.layers[node.layer] = [node.name]
                    else: self.layers[node.layer].append(node.name)
                    if not "/>" in F[i]:
                        layers[l] = node.name; l += 1
                        self.nodes.append(node.name)
                        self.subtrees[node.name] = odict(([node.name, node],))
                    else: self.leaves.append(node.name)
                    if node.parent:
                        parent = self.tree[node.parent]
                        node.htmID = parent.htmID + '_%s' % parent.children.index(node.name)
                    else: node.htmID = 'table1_0'
                    for x in layers.values()[1:l+1]:
                        if node.layer > self.tree[x].layer: self.subtrees[x][node.name] = copy(node)
            self.viable = 1
        else: return


    def updateSubs(self):

        for sub in self.subtrees.values():
            for k in sub.keys(): sub[k] = copy(self.tree[k])


    def updateTypes(self, types = ''):

        if types == '': return
        else:
            for i in self.tree.values(): i.type = [0,0,0,0]
            f = open(types, 'r')
            codes = f.readlines()
            f.close()
            for line in codes:
                line = line.strip('\r\n').split('\t')
                if line[0] in self.leaves:
                    leaf = self.tree[line[0]]
                    if line[1] in ["Sink", "sink", "SINK"]:
                        leaf.type = [0,0,1,0]
                    elif line[1] in ["Source","source", "SOURCE"]:
                        leaf.type = [1,0,0,0] if leaf.mutations != [] else [0,1,0,0]
                    else: leaf.type = [0,0,0,1]
        self.updateNodes()
        self.updateSubs()
        self.nsrc, self.nsnk, self.nudf = 0, 0, 0
        for i in self.leaves:
            if self.tree[i].isSource() == "Source": self.nsrc += 1
            elif self.tree[i].isSource() == "Sink": self.nsnk += 1
            else: self.nudf += 1


    def updateNodes(self):

        for layer in xrange(len(self.layers), 1, -1):
            for node in self.layers[layer]:
                parent = self.tree[node].parent
                if node in self.leaves and self.tree[node].isSource() != "Undefined":
                    for i in xrange(4):
                        self.tree[parent].type[i] += self.tree[node].type[i]
                elif node in self.leaves and self.tree[node].isSource() == "Undefined":
                    self.tree[parent].type[3] += 1
                elif node in self.nodes:
                    if self.tree[node].type[0] > 0 or self.tree[node].type[1] > 0:
                        self.tree[parent].type[0] += 1
                    if self.tree[node].type[2] >= 1:
                        self.tree[parent].type[2] += 1
                    else: self.tree[parent].type[3] += 1


    def Newick(self, node, string = ''):

        if node == None:
            children = self.layers[1]
            string = ')'
            for child in children:
                string = ',' + self.Newick(child, string)
            string = '(' + string[1:]
        else:
            string = '%s' % (node) + string
            if self.tree[node].children == []: return string
            string = ')' + string
            for child in self.tree[node].children:
                string = ',' + self.Newick(child, string)
            string = '(' + string[1:]
        return string
   

    def treeToHTML(self, page):

        pagename = page + '.html'
        infile = open(pagename,'r')
        htm = infile.readlines(); infile.close()
        out = open(pagename,'w')
        if page == 'base':
            head, tail = htm[:33], htm[-2:]
            layer = [0 for i in self.layers]
            out.write(''.join(head))
            for node in self.tree.values():
                tr = '<tr id="%s" class="%s">' % (node.htmID, 'node' if node.name in self.nodes else 'leaf')
                td1 = '<td id="%s " onclick="treetable_toggleRow(\'%s\');">%s•&nbsp;%s</td>' % (node.name, node.htmID, '&nbsp;' *4 *(node.layer-1), node.name)
                if node.name in self.nodes:
                    xnode = self.subtrees[node.name]
                    td2 = ['<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>' \
                        % (len(node.mutations), len(set(xnode.keys()) & set (self.leaves)), \
                        self.Rho(node.name, xnode), self.StErr(xnode), self.Age(node.name), self.ConfidenceInterval(node.name))]
                else: td2 = ['<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>' % (len(node.mutations), '--','--','--','--','--')]
                line = tr+td1+''.join(td2)+'</tr>\n'
                out.write(line)
        elif page == 'f1':
            head, tail = htm[:32], htm[-2:]
        elif page == 'f2':
            head, tail = htm[:33], htm[-2:]
        out.write(''.join(tail))
        out.close()

    def Rho(self, root, sub, f = False):

        if not f and self.tree[root].extra['Rho'] != '--':
            return self.tree[root].extra['Rho']
        else:
            mutCount = 0
            for leaf in (set(sub.keys()) & set(self.leaves)):
                mutCount += self.mutationCount(root, leaf)
            rho = float(mutCount)/ len((set(sub.keys()) & set(self.leaves)))
            self.tree[root].extra['Rho'] = rho
            return round(rho, 3)


    def mutationCount(self, root, node, mutCount = 0):

        mutCount += len(self.tree[node].mutations)
        parent = self.tree[node].parent
        if parent != root:
            mutCount = self.mutationCount(root, parent, mutCount)
        return mutCount


    def removeNode(self, sub, node):

        for child in self.tree[node].children:
            if child in sub.keys(): sub = self.removeNode(sub, child)
        x = sub.pop(node)
        return sub


    def Age(self, node):

        rho = self.Rho(node, self.subtrees[node])
        age = (exp(-exp(-0.0263 *(rho + 40.2789))) *rho *3624)
        return round(age, 3)


    def StErr(self, sub, f = False):

        if not f and sub.values()[0].extra['SE'] != '--':
            return sub.values()[0].extra['SE']
        tSum = 0.0
        leaves = set(sub.keys()) & set(self.leaves)
        nodes = set(sub.keys()[1:]) & set(self.nodes)
        for leaf in leaves: tSum += len(self.tree[leaf].mutations)
        for nd in nodes:
            if not f: lv = set(self.subtrees[nd].keys()) & set(self.leaves)
            else: lv = set(self.subtrees[nd].keys()) & set([i for i in self.leaves if self.tree[i].isSource() == 'Sink'])
            tSum += len(self.tree[nd].mutations) * len(lv) **2
        se = sqrt(tSum/(len(leaves)**2))
        if not f: sub.values()[0].extra['SE'] = se
        return round(se, 3)


    def ConfidenceInterval(self, node):

        rho = self.Rho(node, self.subtrees[node])
        se = self.StErr(self.subtrees[node])
        lower = max(exp(-exp(-0.0263 * ((rho - (1.96 * se)) + 40.2789))) * (rho - (1.96 * se)) * 3624.0, 0)
        upper = exp(-exp(-0.0263 * ((rho + (1.96 * se)) + 40.2789))) * (rho + (1.96 * se)) * 3624.0;
        return round(lower, 3), round(upper, 3)


    def fN(self, node, N = 1):

        t = self.tree[node].type
        if N == 1:
            if t[0] >= N and t[2] > 0:
                self.tree[node].extra['f1'] = True
                return self.fStats(node, N)
            else: return ['N/A','N/A','N/A'] if node in self.nodes else ['--','--','--']
        elif N == 2:
            if t[0] >= N:
                self.tree[node].extra['f2'] = True
                return self.fStats(node, N)
            else: return ['N/A','N/A','N/A'] if node in self.nodes else ['--','--','--']


    def fStats(self, node, N):

        sub = copy(self.subtrees[node])
        for i in xrange(len(sub)-1, 0, -1):
            tp = sub.values()[i].type
            if tp[0] > (N-1) or sub.values()[i].isSource() in ["Source", "Undefined"]: ##or tp[1] > (N-1)
                sub = self.removeNode(sub, sub.keys()[i])
        leaves = set(sub.keys()) & set(self.leaves)
        if len(leaves) == 0:
            self.tree[node].extra.pop('f%s' % N)
            return ['N/A','N/A','N/A']
        elif len(leaves) == 1:
            self.tree[node].extra['f%s' % N] = [1,0,0]
        else:
            self.tree[node].extra['f%s' % N] = [len(leaves), self.Rho(node, sub, True), self.StErr(sub, True)]
        return self.tree[node].extra['f%s' % N]


    def f2plus(self, node):

        if node in self.leaves: return '--'
        parent  = self.tree[node].parent
        if parent == None: self.tree[node].extra['f2+'] = True
        elif 'f2' in self.tree[node].extra.keys() and 'f2' in self.tree[parent].extra.keys():
            self.tree[node].extra['f2+'] = True
        else: self.tree[node].extra['f2+'] = False
        return self.tree[node].extra['f2+']


    def migrationProbs(self, migrations, mutationRate, f, effective):

        probabilities = odict()
        probabilities[mutationRate] = migrations
        MC = [0.0 for M in xrange(len(migrations))]
        DM = [0.0 for M in xrange(len(migrations))]
        t_leaves = 0
        for i in self.nodes:
            node = self.tree[i]
            if 'f%s' % f in node.extra:
                fval = node.extra['f%s' % f]
                N = fval[1]/(fval[2]**2) if effective and fval[1] > 0 else fval[0]
                vals = [exp(- N * ((float(M)/mutationRate) - fval[1] * log(float(M)/mutationRate))) for M in migrations]
                probs = [round(val/sum(vals),4) for val in vals]
                probabilities[node.name] = probs
                t_leaves += fval[0]
                for M in xrange(len(migrations)):
                    MC[M] += probabilities[node.name][M] * fval[0]
                    DM[M] += (1 - probabilities[node.name][M]) * probabilities[node.name][M] * fval[0]**2
        probabilities['\t'] = ['' for i in xrange(len(migrations))]
        probabilities['Mean contribution of each migration'] = [round(x/sum(MC),4) for x in MC]
        probabilities['Deviation from the mean'] = [round((x**0.5)/t_leaves,4) for x in DM]
        return probabilities
