from math import sqrt, exp
from tree import Tree

def Rho(tree):

    if 'Rho' in tree.tree.values()[0].extra.keys():
        print 'Rho already computed'
        return tree.tree.values()[0].extra['Rho']
    mutCount = 0
    for leaf in tree.leaves:
        mutCount += mutationCount(leaf, tree)
    rho = float(mutCount)/ len(tree.leaves)
    tree.tree.values()[0].extra['Rho'] = \
        (rho, len(tree.leaves), '{:.3f}'.format(rho))
    return (rho, len(tree.leaves), '{:.3f}'.format(rho))


def StDev(tree):

    if 'SE' in tree.tree.values()[0].extra.keys():
        return tree.tree.values()[0].extra['SE']
    tSum = 0.0
    for node in tree.tree.values()[1:]:
        if node.name in tree.leaves: tSum += len(node.mutations)
        else: tSum += len(node.mutations) * \
                      (len(Tree('',tree.subtree(node.name)).leaves)) **2
    sd = sqrt(tSum/(len(tree.leaves)**2))
    tree.tree.values()[0].extra['SE'] = (sd, '{:.3f}'.format(sd))
    return (sd, '{:.3f}'.format(sd))


def Age(tree):

    if 'Age' in tree.tree.values()[0].extra.keys():
        return tree.tree.values()[0].extra['Age']
    rho = Rho(tree)[0]
    age = (exp(-exp(-0.0263 *(rho + 40.2789))) *rho *3624)
    tree.tree.values()[0].extra['Age'] = (age, '{:.3f}'.format(age))
    return (age, '{:.3f}'.format(age))


def ConfidenceInterval(tree):

    if 'CI' in tree.tree.values()[0].extra.keys():
        return tree.tree.values()[0].extra['CI']
    rho = Rho(tree)[0]
    sd = StDev(tree)[0]
    lower = max(exp(-exp(-0.0263 * ((rho - (1.96 * sd)) + 40.2789)))* \
            (rho - (1.96 * sd)) * 3624.0, 0)
    upper = exp(-exp(-0.0263 * ((rho + (1.96 * sd)) + 40.2789)))* \
            (rho + (1.96 * sd)) * 3624.0;
    tree.tree.values()[0].extra['CI'] = \
        '{:.3f}'.format(lower), '{:.3f}'.format(upper)
    return '{:.3f}'.format(lower), '{:.3f}'.format(upper)


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
            return fStats(Tree('',tree.subtree(node)), N)
        else: return (['','NE','NE'], ['NE','NE'])
    elif N == 2:
        if t[0] >= N:
            return fStats(Tree('',tree.subtree(node)), N)
        else: return (['','NE','NE'], ['NE','NE'])
    
def fStats(tree, N):

    nodes = tree.tree.values()
    for i in range(len(nodes)-1, 0, -1):
        if nodes[i].type[0] > (N-1) or nodes[i].type[1] > (N-1) \
           or nodes[i].isSource() in ["Source", "Undefined"]:
            tree.removeNode(nodes[i].name)            
    if len(tree.leaves) == 0: return (['',0,'--'], ['--','--']) #N/As
    elif len(tree.leaves) == 1: return (['',1,0], [0,0])
    else: return Rho(tree), StDev(tree)
