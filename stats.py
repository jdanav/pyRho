from math import sqrt, exp
from tree import Tree

def Rho(tree, f = False):

    if not f and tree.root.extra['Rho'] != '--':
        return tree.root.extra['Rho']
    else:
        mutCount = 0
        for leaf in tree.leaves:
            mutCount += mutationCount(leaf, tree)
        rho = float(mutCount)/ len(tree.leaves)
        tree.root.extra['Rho'] = rho
        return rho


def StErr(tree, f = False):

    if not f and tree.root.extra['SE'] != '--':
        return tree.root.extra['SE']
    tSum = 0.0
    for node in tree.leaves: tSum += len(tree.tree[node].mutations)
    for node in tree.nodes[1:]:  tSum += len(tree.tree[node].mutations) * \
                      (len(Tree(tree.subtree(node)).leaves)) **2
    se = sqrt(tSum/(len(tree.leaves)**2))
    tree.root.extra['SE'] = se
    return se


def Age(tree):

    rho = Rho(tree)
    age = (exp(-exp(-0.0263 *(rho + 40.2789))) *rho *3624)
    return age


def ConfidenceInterval(tree):

    rho = Rho(tree)
    se = StErr(tree)
    lower = max(exp(-exp(-0.0263 * ((rho - (1.96 * se)) + 40.2789)))* \
            (rho - (1.96 * se)) * 3624.0, 0)
    upper = exp(-exp(-0.0263 * ((rho + (1.96 * se)) + 40.2789)))* \
            (rho + (1.96 * se)) * 3624.0;
    return (lower, upper)


def mutationCount(node, tree, mutCount = 0):

    mutCount += len(tree.tree[node].mutations)
    parent = tree.tree[node].parent
    if parent != tree.tree.keys()[0]:
        mutCount = mutationCount(parent, tree, mutCount)
    return mutCount


def fN(tree, node, N = 1):

    t = tree.tree[node].type
    if N == 1:
        if t[0] >= N and t[2] > 0:
            return fStats(Tree(tree.subtree(node)), N)
        else: return ['NE','NE','NE']
    elif N == 2:
        if t[0] >= N:
            return fStats(Tree(tree.subtree(node)), N)
        else: return ['NE','NE','NE']
    
def fStats(tree, N):

    f = True
    nodes = tree.tree.values()
    for i in range(len(nodes)-1, 0, -1):
        if nodes[i].type[0] > (N-1) or nodes[i].type[1] > (N-1) \
           or nodes[i].isSource() in ["Source", "Undefined"]:
            tree.removeNode(nodes[i].name)            
    if len(tree.leaves) == 0: return [0,'--','--'] #N/As
    elif len(tree.leaves) == 1: return [1,0,0]
    else: return len(tree.leaves), Rho(tree, f), StErr(tree, f)
