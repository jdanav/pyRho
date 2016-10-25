class Node:

    def __init__(self, name, parent, mutations, layer):

        self.name = name
        self.parent = parent
        self.children = []
        self.siblings = []
        self.mutations = mutations.split(',') if mutations else []
        self.layer = layer
        self.founder = False
        self.source = False

    def __str__(self):

        return '\n%s\nMutations: %s\n\nParent: %s \
                    \nChildren: %s\nSiblings: %s' \
               % (self.name, ' '.join(self.mutations), \
                  self.parent, ' '.join(self.children), \
                  ' '.join(self.siblings))


    def toggleFounder(self):

        self.founder = not self.founder
        return "%s founder status: %s\n" % (self.name, self.founder)


    def toggleSource(self):

        self.source = not self.source
        return "Node %s is source" % self.name if self.source \
              else "Node %s is sink" % self.name
