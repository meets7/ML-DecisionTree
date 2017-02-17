class Node:
    
    def __init__(self):
        self.attribute = ""
        self.leftChild = None
        self.rightChild = None
        #corresponding to feature value of data equal to true
        self.positiveInstances = [] 
        #corresponding to feature value of data equal to false
        self.negativeInstances = []
        self.allNodeInstances = []
        self.isLeaf = False
        self.visited = False

class BinaryTree:
    def __init__(self, depth):
        self.nodes = []
        self.depth = depth

def main():
    print "This is the tree.py file." # my code here

if __name__ == "__main__":
    main()