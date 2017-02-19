class Node:
    
    def __init__(self):
        self.attribute = ""
        self.leftChild = None
        self.rightChild = None
        self.positiveInstances = []    #corresponding to feature value of data equal to true
        self.negativeInstances = []    #corresponding to feature value of data equal to false
        self.allNodeInstances = []
        self.isLeaf = False
        self.visited = False
    
def printInorder(node, depth):
    # if node is None:
    #     return
    # if node.isLeaf:
    #     print node.attribute
    # else:
    #     formattingstring = ""
    #     for i in range(depth):
    #         formattingstring = formattingstring + "| " 
        
    #     value = "0" if node.rightChild else "1"
    #     outputString = formattingstring + node.attribute + " = " + value + " : "
    #     print outputString
    
    # printInorder(node.leftChild, depth + 1)
    # formattingstring = ""
    # if node.isLeaf == False:
    #     for i in range(depth):
    #         formattingstring = formattingstring + "| " 
        
    #     value = "0" if node.rightChild else "1"
    #     outputString = formattingstring + node.attribute + " = " + value + " : "
    #     print outputString

    # printInorder(node.rightChild, depth + 1)
    if node is None:
        return

    if node.isLeaf == False or node.isLeaf == None:
        formattingstring = ""
        for i in range(depth):
            formattingstring = formattingstring + "| "

        if (node.leftChild != None):
            if(node.leftChild.attribute == None):
                outputString = formattingstring + node.attribute + " = " + "0"
                print(outputString)
            else:
                outputString = formattingstring + node.attribute + " = " + "0" + " : " + str(node.leftChild.attribute)
                print(outputString)
            printInorder(node.leftChild, depth + 1)
        else:
            return

        if(node.rightChild != None):
            if(node.rightChild.attribute == None):
                outputString = formattingstring + node.attribute + " = " + "1"
                print(outputString)
            else:
                outputString = formattingstring + node.attribute + " = " + "1" + " : " + str(node.rightChild.attribute)
                print(outputString)
            printInorder(node.rightChild, depth + 1)
        else:
            return

def main():
    print "This is the tree.py file." # my code here

if __name__ == "__main__":
    main()