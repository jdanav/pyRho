from math import sqrt, exp
from tree import Tree

def Rho(tree):

    mutCount = 0
    for leaf in tree.leaves:
        mutCount += mutationCount(leaf, tree)
    rho = float(mutCount)/ len(tree.leaves)
    return (rho, '{:.3f}'.format(rho))


def StDev(tree):

    tSum = 0.0
    for node in tree.tree.values()[1:]:
        if node.name in tree.leaves: tSum += len(node.mutations)
        else: tSum += len(node.mutations) * \
                      (len(Tree('',tree.subtree(node.name)).leaves)) **2
    sd = sqrt(tSum/(len(tree.leaves)**2))
    return (sd, '{:.3f}'.format(sd))


def Age(tree):

    rho = Rho(tree)[0]
    age = (exp(-exp(-0.0263 *(rho + 40.2789))) *rho *3624)
    return (age, '{:.3f}'.format(age))


def ConfidenceInterval(tree):
    
    rho = Rho(tree)[0]
    sd = StDev(tree)[0]
    lower = exp(-exp(-0.0263 * ((rho - (1.96 * sd)) + 40.2789)))* \
            (rho - (1.96 * sd)) * 3624.0
    upper = exp(-exp(-0.0263 * ((rho + (1.96 * sd)) + 40.2789)))* \
            (rho + (1.96 * sd)) * 3624.0;
    return '{:.3f}'.format(lower), '{:.3f}'.format(upper)


##def StatAllNodes(tree):
##
##    subtrees = [ Tree(node, tree.subtree(node)) for node in tree.nodes]
##    print "{:30}".format("Node"), "{:8}".format("  GDist"), \
##          "{:6}".format("   Age"), \
##          "{:8}".format("  SE  Confidence interval"), "\n" + "=" * 60
##    for sub in subtrees:
##        print "{:30}".format(sub.name), "{:7.4f}".format(Rho(sub)), \
##              "{:7.1f}".format(Age(sub)), "{:5.1f}".format(StDev(sub)),\
##              "{:18}".format(" ".join(ConfidenceInterval(sub)))
##    print "=" * 60 + "\n", "{:30}".format("Node"), \
##          "{:8}".format("  GDist"), "{:6}".format("   Age"),\
##          "{:8}".format("  SE  Confidence interval\n\n")    


def mutationCount(node, tree, mutCount = 0):

    mutCount += len(tree.tree[node].mutations)
    parent = tree.tree[node].parent
    if parent != tree.tree.keys()[0]:
        mutCount = mutationCount(parent, tree, mutCount)
    return mutCount


#if __name__ == '__main__':
#    n = Tree("H13","C:\Users\Dan\Desktop\PyRHO\H13.xml")
#    StatAllNodes(n)
