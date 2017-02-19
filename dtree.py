import copy
import tree
import math
import classifier
from random import randint

class ID3DecisionTree():
    
    def __init__(self, givenHeuristic):
        self.root = tree.Node()
        self.heuristic = givenHeuristic

    def generate(self, node, attributes):
         
        node.negativeInstances = self.getInstances(node.allNodeInstances,'0')
        node.positiveInstances = self.getInstances(node.allNodeInstances,'1')
        entropy = self.getHeuristicValue(len(node.negativeInstances), len(node.positiveInstances))
        if entropy == 0:
            node.isLeaf = True
            node.attribute = '0' if node.negativeInstances else '1' #Assign either 0 or 1
            return
        elif not attributes: #Check if no attributes are left to split tree
            node.isLeaf = True
            node.attribute = '0' if len(node.negativeInstances) > len(node.positiveInstances) else '1'
            return
        else:
            node.attribute = self.getNodeAttribute(node.allNodeInstances, entropy, attributes)
            node.leftChild  = tree.Node()
            node.rightChild = tree.Node()
            node.leftChild.allNodeInstances = self.getAllNodeInstances(node.allNodeInstances, node.attribute, attributes,'0')
            node.rightChild.allNodeInstances = self.getAllNodeInstances(node.allNodeInstances, node.attribute, attributes,'1')

            #left subtree check
            if len(node.leftChild.allNodeInstances) == 0:
                node.leftChild = None
                node.rightChild = None
                node.attribute = '1'
                node.isLeaf = True
                return

            #right subtree check
            if len(node.rightChild.allNodeInstances) == 0:
                node.leftChild = None
                node.rightChild = None
                node.attribute = '0'
                node.isLeaf = True
                return
            
            #Recursive calls for left and right subtrees
            self.generate(node.leftChild, attributes)
            self.generate(node.rightChild, attributes)

    def getAllNodeInstances(self, parentAllInstances, attribute, allAttributes,value):
        instancesCorrespondingToGivenValue = []
        attributeIndex = allAttributes.index(attribute)
        for inst in parentAllInstances:
            if inst[attributeIndex] == value:
                instancesCorrespondingToGivenValue.append(inst)
        return instancesCorrespondingToGivenValue

    def getNodeAttribute(self, instances, entropy, attributes):
        gains = {}
        for attributeIndex, attribute in enumerate(attributes):
            gains[attribute] = self.getGainForAttribute(instances, entropy, attributeIndex)

        maxGainAttribute = max(gains, key=gains.get)
        return maxGainAttribute
    
    def getGainForAttribute(self, instances, entropy, attributeIndex):
        attributeValueCollection = dict.fromkeys(['0','1'])
        attributeValueCollection['0'] = dict.fromkeys(['negativeCount', 'positiveCount'],0)
        attributeValueCollection['1'] = dict.fromkeys(['negativeCount', 'positiveCount'],0)
        for instance in instances:
            attributeValue = instance[attributeIndex]
            targetAttributeValue = instance[-1]
            if targetAttributeValue == '1':
                attributeValueCollection[attributeValue]['positiveCount'] = attributeValueCollection[attributeValue]['positiveCount'] + 1
            else:
                attributeValueCollection[attributeValue]['negativeCount'] = attributeValueCollection[attributeValue]['negativeCount'] + 1
        
        zeroEntropy = self.getHeuristicValue(attributeValueCollection['0']['negativeCount'],attributeValueCollection['0']['positiveCount'])
        oneEntropy = self.getHeuristicValue(attributeValueCollection['1']['negativeCount'],attributeValueCollection['1']['positiveCount'])
        totalSamplesConsidered = len(instances)
        zeroSamples = attributeValueCollection['0']['negativeCount'] + attributeValueCollection['0']['positiveCount']
        oneSamples = attributeValueCollection['1']['negativeCount'] + attributeValueCollection['1']['positiveCount']

        expectedEntropy = (zeroSamples/float(totalSamplesConsidered)) * zeroEntropy + (oneSamples/float(totalSamplesConsidered)) * oneEntropy 
        gain = entropy - expectedEntropy
        return gain

    def getInstances(self, data, instanceType):
        instances = []
        for instance in data:
            if instance[-1] == instanceType: #class matches instanceType
                instances.append(instance)
        return instances

    def getHeuristicValue(self, negativeSamplesCount, positiveSamplesCount):

        if self.heuristic == "infogain":
            return self.getEntropy(negativeSamplesCount, positiveSamplesCount)
        else:
            return self.getVarianceImpurity(negativeSamplesCount, positiveSamplesCount)

    def getEntropy(self, negativeSamplesCount, positiveSamplesCount):
        totalCount = negativeSamplesCount + positiveSamplesCount
        if totalCount == 0:
            return 0
        pMinus = negativeSamplesCount/float(totalCount)
        pPlus = positiveSamplesCount/float(totalCount)
        
        if pMinus == 0:
            return -(pPlus) * math.log(pPlus,2)
        if pPlus == 0:
            return -(pMinus) * math.log(pMinus,2)
        
        return -(pMinus) * math.log(pMinus,2) - (pPlus) * math.log(pPlus,2)
         
    def getVarianceImpurity(self, k0, k1):
        k = k0 + k1
        if k == 0 or k1 == 0 or k0 == 0:
            return 0
        pMinus = k0/float(k)
        pPlus = k1/float(k)
        impurity = pMinus * pPlus
        return impurity  

    def getPrunedDecisionTree(self, l, k, data, attributes, currentAccuracy):
        classifer = classifier.classifier()
        d_best = copy.deepcopy(self)
        bestAccuracy = currentAccuracy
        for i in range(l):
            d_prime = copy.deepcopy(d_best)
            m = randint(1,k)
            for j in range(1,m):
                allNodesList = self.getAllNodes(d_prime.root)
                n = len(allNodesList)
                if n == 1 or n == 0:
                    continue
                else:
                    p = randint(0,n - 1)
                self.pruneSubTree(allNodesList[p])
            
            accuracy = classifer.classify(data,d_prime.root,attributes)
            if accuracy > bestAccuracy:
                d_best = d_prime
                bestAccuracy = accuracy

        return d_best

    def getAllNodes(self, rootNode):
        allNodesList = []
        nodequeue = [rootNode]
        while nodequeue:
            node = nodequeue.pop(0)
            if node is not None and node.isLeaf == False:
                allNodesList.append(node)
                nodequeue.append(node.leftChild)
                nodequeue.append(node.rightChild)
        return allNodesList

    def pruneSubTree(self, randomNode):
        randomNode.attribute = '0' if len(randomNode.negativeInstances) > len(randomNode.positiveInstances) else '1'
        randomNode.isLeaf = True
        randomNode.leftChild = None
        randomNode.rightChild = None






