
import sys
import random
import string

PLAYER1 = 1
PLAYER2 = 2

class Node:
    def __init__(self, _label, _value):
        self.parent = None
        self.label = _label
        self.value = _value
        self.children = []

    def addChild(self, child):
        self.children.append(child)
        child.parent = self
        
    def isLeaf(self):
        return len(self.children) == 0
    
    
    def getTreeString(self, n):
        #print "WORKING ON " + n.label + " with parent "#+ n.parent.label
        result = "NODE: " + n.label + " " + str(n.value)
        for c in n.children:
            result += "\n" + self.getTreeString(c)
        return result
    
    
    def getGraphvizString(self):
        result = 'digraph mygraph {\n'
        self.node_count = 0
        result += self.getGraphvizHelper(self)
        return result + "}"
        
        
    def getGraphvizHelper(self, n):        
        #print "WORKING ON " + n.label + " with parent "#+ n.parent.label
        result = '''\tn%d [label="%s%d"]\n''' % (n.value, n.label, n.value)
        #result = '''\tn%d [shape=point]\n''' % (n.value)
        for c in n.children:
            result += '''\tn%d -> n%d \n''' % (n.value, c.value)
            result += self.getGraphvizHelper(c)
        return result
    
    
    
    def __str__(self):
        return self.getTreeString(self)
        


def buildTreeHelper(n, bf, depth):
    if depth == 0:
        return
    
    for i in range(random.randrange(bf)):
        child = Node(random.choice(string.ascii_uppercase), random.randrange(1000))
        #print n.label , " GETTING CHILD ", child.label
        n.addChild(child)
        buildTreeHelper(child, bf, depth-1)
        #print "DONE " + child.label
    

def buildRandomTree(bf, max_depth):
    node1 = Node(random.choice(string.ascii_uppercase), random.randrange(1000))
    buildTreeHelper(node1, bf, max_depth)    
    return node1

   


def alphabeta(node, depth, alpha, beta, player):
    if node.isLeaf() or depth == 0:
        return node.value
    
    if player == PLAYER1:
        # max player
        v = -sys.maxint-1
        for child in node.children:
            child_v = alphabeta(child, depth-1, alpha, beta, PLAYER2)
            v = max(v, child_v)
            alpha = max(alpha, v)
            if alpha > beta:
                print "PRUNING!"
                break
        return v
    else:
        # min player
        v = sys.maxint
        for child in node.children:
            child_v = alphabeta(child, depth-1, alpha, beta, PLAYER1)
            v = min(v, child_v)
            beta = min(beta, v)
            if alpha > beta:
                print "PRUNING!"
                break
        return v



bf = 5
depth = 8
tree = buildRandomTree(bf, depth)

open("tree.dot", 'w').write(tree.getGraphvizString())

#print tree
max_depth = 100
start_player = PLAYER1

print alphabeta(tree, max_depth, -sys.maxint-1, sys.maxint, PLAYER1)








