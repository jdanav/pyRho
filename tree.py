# -*- coding: utf-8 -*-

import re
from collections import defaultdict as ddict, OrderedDict as odict
from copy import copy
from node import Node

class Tree:

    def __init__(self, name, source):

        self.name = name
        self.tree = odict()
        self.nodes = []
        self.leaves = []
        self.noLabel = 0
        self.buildTree(source)


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
            else: self.leaves.append(node.name)
            node.siblings = [i.name for i in self.tree.values()
                             if i.parent == node.parent]
            node.siblings.remove(node.name)


    def __str__(self):

        return "Tree name: %s\n\n%s nodes and %s leaves" \
               % (self.name, len(self.nodes), len(self.leaves))


    def printLayer(self, layer, prints = 1):

        output = ''
        output += "Nodes in layer %s:\n" % layer
        for node in self.tree.values():
            if node.layer == layer: output += node+ ' \n'
        if prints: print output
        else: return output


    def printTree(self, tree = {}, prints = 1):
        output = ''
        tree = self.tree if tree == {} else tree
        for i in range(len(tree)-1):
            M = tree.values()[i]
            N = tree.values()[i+1]
            char = u'└─ ' if N.layer < M.layer else u'├─ '
            output += '   ' * (M.layer-1)
            output += "%s %s\n" % (char, M.name)
        output += '   ' * (N.layer-1)
        output += "%s %s\n" % (u'└─ ', N.name)
        if prints: print output
        else: return output


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
        return subtree
