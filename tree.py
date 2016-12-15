# -*- coding: utf-8 -*-

import re, sys
from collections import defaultdict as ddict, OrderedDict as odict
from copy import copy
from math import sqrt, exp


class Node:

    def __init__(self, name, parent, mutations, layer):

        self.name = name
        self.parent = parent
        self.children = []
        self.siblings = []
        self.mutations = mutations.split(',') if mutations else []
        self.layer = layer
        self.type = [0,0,0,0]
        self.extra = {i:'--' for i in ('Rho','Age','SE','CI')}


    def isSource(self):

        t = self.type
        if t == [0,0,1,0] and self.children == []: return "Sink"
        elif (t == [1,0,0,0] or t == [0,1,0,0]) and self.children == []: return "Source"
        elif (t == [0,0,0,1] or t == [0,0,0,0]) and self.children == []: return "Undefined"
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
            for i in range(Fl):
                sys.stdout.write('\rLoading file... %s/%s' % (i+1, Fl))
                match = re.search('Id=(.*) HG=(.*)>', F[i])
                if "/Node" in F[i]: l -= 1
                elif match is None: pass
                else:
                    node = Node(match.group(1).strip('" '), layers[l-1], match.group(2).strip('" /,'), l)
                    if node.name == "NoLabel":
                        self.noLabel += 1
                        node.name = node.name + "_%s" % self.noLabel
                    if node.name in self.tree: sys.stdout.write('\nWarning! Multiple copies of %s' % node.name); return
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
                    for x in layers.values()[1:l+1]:
                        if node.layer > self.tree[x].layer: self.subtrees[x][node.name] = copy(node)
            self.viable = 1
            sys.stdout.write('\n')
        else: sys.stdout.write('\n')


    def updateSubs(self, j, c):

        for sub in self.subtrees.values():
            for k in sub.keys(): sub[k] = copy(self.tree[k])
            j += 1
            sys.stdout.write('\rUpdating types... %s/%s' % (j,(c + len(self.tree) + len(self.subtrees))))


    def updateTypes(self, types = ''):

        if types == '': return
        else:
            for i in self.tree.values(): i.type = [0,0,0,0]
            f = open(types, 'r')
            codes = f.readlines()
            f.close()
            j = 0
            for line in codes:
                line = line.strip('\n').split('\t')
                if line[0] in self.leaves:
                    leaf = self.tree[line[0]]
                    if line[1] in ["Sink", "sink", "SINK"]:
                        leaf.type = [0,0,1,0]
                    elif line[1] in ["Source","source", "SOURCE"]:
                        leaf.type = [1,0,0,0] if leaf.mutations != [] else [0,1,0,0]
                    else: leaf.type = [0,0,0,1]
                j += 1
                sys.stdout.write('\rUpdating types... %s/%s' % (j,(len(codes) + len(self.tree) + len(self.subtrees))))
        self.updateNodes(j, len(codes))
        self.updateSubs(j + len(self.tree), len(codes))
        self.nsrc, self.nsnk, self.nudf = 0, 0, 0
        for i in self.leaves:
            if self.tree[i].isSource() == "Source": self.nsrc += 1
            elif self.tree[i].isSource() == "Sink": self.nsnk += 1
            else: self.nudf += 1
        sys.stdout.write('\n')


    def updateNodes(self, j, c):

        for layer in range(len(self.layers), 1, -1):
            for node in self.layers[layer]:
                parent = self.tree[node].parent
                if node in self.leaves and self.tree[node].isSource() != "Undefined":
                    for i in range(4):
                        self.tree[parent].type[i] += self.tree[node].type[i]
                elif node in self.leaves and self.tree[node].isSource() == "Undefined":
                    self.tree[parent].type[3] += 1
                elif node in self.nodes:
                    if self.tree[node].type[:2] > [0,0]:
                        self.tree[parent].type[0] += 1
                    if self.tree[node].type[2] >= 1:    #elif
                        self.tree[parent].type[2] += 1
                    else: self.tree[parent].type[3] += 1
                j += 1
                sys.stdout.write('\rUpdating types... %s/%s' % (j,(c + len(self.tree) + len(self.subtrees))))


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
        for i in range(len(sub)-1, 0, -1):
            tp = sub.values()[i].type
            if tp[0] > (N-1) or sub.values()[i].isSource() in ["Source", "Undefined"]: #or tp[1] > (N-1)
                sub = self.removeNode(sub, sub.keys()[i])
        leaves = set(sub.keys()) & set(self.leaves)
        if len(leaves) == 0: self.tree[node].extra.pop('f%s' % N); return ['N/A','N/A','N/A']
        elif len(leaves) == 1: return [1,0,0]
        else:
            return len(leaves), self.Rho(node, sub, True), self.StErr(sub, True)


    def f2plus(self, node):

        if node in self.leaves: return '--'
        parent  = self.tree[node].parent
        if parent == None: self.tree[node].extra['f2+'] = True
        elif 'f2' in self.tree[node].extra.keys() and 'f2' in self.tree[parent].extra.keys():
            self.tree[node].extra['f2+'] = True
        else: self.tree[node].extra['f2+'] = False
        return self.tree[node].extra['f2+']
