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

    def __str__(self):

        return '\n%s\nMutations: %s\n\nParent: %s \
                    \nChildren: %s\nSiblings: %s' \
               % (self.name, ' '.join(self.mutations), \
                  self.parent, ' '.join(self.children), \
                  ' '.join(self.siblings))


    def isSource(self):

        t = self.type
        if t == [0,0,1,0]: return "Sink"
        elif t == [1,0,0,0] or t == [0,1,0,0]: return "Source"
        elif t == [0,0,0,1] or (t == [0,0,0,0] and \
                        self.children == []): return "Undefined"
        else: return t
