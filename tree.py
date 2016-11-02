# -*- coding: utf-8 -*-

import re
from collections import defaultdict as ddict, OrderedDict as odict
from copy import copy
from node import Node
from random import randint

class Tree:

    def __init__(self, name, source, types = ''):

        self.name = name
        self.tree = odict()
        self.nodes = []
        self.leaves = []
        self.layers = odict()
        self.noLabel = 0
        self.buildTree(source)
        self.updateTypes(types)

    def buildTree(self, source):

        if type(source) == str:
            f = open(source,'r')
            layers, l = ddict(list), 1
            layers[0] = None
            for i in f.readlines():
                match = re.search('Id=(.*) HG=(.*)>', i)
                if "/Node" in i: l -= 1
                elif match is None: pass
                else:
                    node = Node(match.group(1).strip('" '), layers[l-1],
                                match.group(2).strip('" /,'), l)
                    if node.name == "NoLabel":
                        self.noLabel += 1
                        node.name = node.name + "_%s" % self.noLabel
                    self.tree[node.name] = node
                    if not node.layer in self.layers:
                        self.layers[node.layer] = [node.name]
                    else: self.layers[node.layer].append(node.name)
                    if not "/>" in i:
                        layers[l] = node.name; l += 1
            f.close()
        elif type(source) == type(self.tree):
            self.tree = source
        else: print "Invalid input"; return ''

        for node in self.tree.values():
            node.children = [i.name for i in self.tree.values()
                             if i.parent == node.name]
            if len(node.children) > 0: self.nodes.append(node.name)
            else:
                self.leaves.append(node.name)

            node.siblings = [i.name for i in self.tree.values()
                             if i.parent == node.parent]
            node.siblings.remove(node.name)


    def __str__(self):

        return "Tree name: %s\n\n%s nodes and %s leaves" \
               % (self.name, len(self.nodes), len(self.leaves))


    def removeNode(self, node):

        for child in self.tree[node].children:
            if child in self.tree: self.removeNode(child)
        x = self.tree.pop(node)
        if node in self.leaves: self.leaves.remove(node)
        else: self.nodes.remove(node)
        

    def subtree(self, root):

        subtree = odict()
        idx = self.tree.keys().index(root)
        layer = self.tree[root].layer
        subtree[root] = copy(self.tree[root])
        while idx < len(self.tree)-1:
            idx += 1
            node = self.tree[self.tree.keys()[idx]]
            if node.layer > layer:
                subtree[node.name] = copy(node)
            else: break
        for node in subtree:
            subtree[node].type = self.tree[node].type
        return subtree


    def updateTypes(self, types = ''):

        if types == '': pass
        else:
            f = open(types, 'r')
            codes = f.readlines()
            f.close()
            for line in codes:
                line = line.strip('\n').split('\t')
                if line[0] in self.leaves:
                    leaf = self.tree[line[0]]
                    if line[1] in ["Sink", "sink", "SINK"]:
                        leaf.type = [0,0,1]
                    elif line[1] in ["Source","source", "SOURCE"]:
                        leaf.type = [1,0,0] if \
                        leaf.mutations != [] else [0,1,0]
                    else: leaf.type = [0,0,0]
        self.updateNodes()

    def updateNodes(self):

        for layer in range(len(self.layers), 1, -1):
            for node in self.layers[layer]:
                parent = self.tree[node].parent
                if node in self.leaves and \
                   self.tree[node].type != [0,0,0]:                    
                    for i in range(3):
                        self.tree[parent].type[i] += \
                                self.tree[node].type[i]
                elif node in self.nodes:
                    if self.tree[node].type[:1] > [0,0]:
                        self.tree[parent].type[0] += 1
                    else: self.tree[parent].type[2] += 1
            
