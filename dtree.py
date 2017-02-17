import tree
import math

class ID3DecisionTree():
    
    def __init__(self):
        # self.depth = 0
        self.root = tree.Node()

    def generate(self, data):
        
        #First row are class attributes except last element
        attributes = list(data[0][:-1])
        data.remove(data[0])

        self.root.allNodeInstances = data        
        nodeQueue = [self.root]
        while nodeQueue:
            node = nodeQueue.pop(0) 
            node.negativeInstances = self.getInstances(node.allNodeInstances,'0')
            node.positiveInstances = self.getInstances(node.allNodeInstances,'1')
            entropy = self.getEntropy(len(node.negativeInstances), len(node.positiveInstances))
            if entropy == 0:
                node.isLeaf = True
                node.attribute = '0' if node.negativeInstances else '1' #Assign either 0 or 1
            elif not attributes: #no attributes left to split tree
                node.isLeaf = True
                node.attribute = '0' if len(node.negativeInstances) > len(node.positiveInstances) else '1'
            else:
                node.attribute = self.getNodeAttribute(node.allNodeInstances, entropy, attributes)
                node.leftChild  = tree.Node()
                node.rightChild = tree.Node()
                node.leftChild.allNodeInstances = self.getAllNodeInstances(node.allNodeInstances, node.attribute, attributes,'0')
                node.rightChild.allNodeInstances = self.getAllNodeInstances(node.allNodeInstances, node.attribute, attributes,'1')
                nodeQueue.append(node.leftChild)
                nodeQueue.append(node.rightChild)

                #left subtree node addition
                if len(node.leftChild.allNodeInstances) == 0:
                    node.leftChild.attribute = '0' if len(node.negativeInstances) > len(node.positiveInstances) else '1'
                    node.leftChild.isLeaf = True
                    nodeQueue.remove(node.leftChild)
                
                attributes.remove(node.attribute)
                
                #right subtree node addition
                if len(node.rightChild.allNodeInstances) == 0:
                    node.rightChild.attribute = '0' if len(node.negativeInstances) > len(node.positiveInstances) else '1'
                    node.rightChild.isLeaf = True
                    nodeQueue.remove(node.rightChild)

    @classmethod
    def getAllNodeInstances(self, parentAllInstances, attribute, allAttributes,value):
        instancesCorrespondingToGivenValue = []
        attributeIndex = allAttributes.index(attribute)
        for inst in parentAllInstances:
            if inst[attributeIndex] == value:
                instancesCorrespondingToGivenValue.append(inst)
        return instancesCorrespondingToGivenValue

    @classmethod
    def getNodeAttribute(self, instances, entropy, attributes):
        gains = {}
        for attributeIndex, attribute in enumerate(attributes):
            gain = self.getGainForAttribute(instances, entropy, attributeIndex)
            gains[attribute] = gain

        maxGainAttribute = max(gains, key=gains.get)
        return maxGainAttribute
    
    @classmethod
    def getGainForAttribute(self, instances, entropy, attributeIndex):
        attributeValueCollection = dict.fromkeys(['0','1'])
        attributeValueCollection['0'] = dict.fromkeys(['negativeCount', 'positiveCount'],0)
        attributeValueCollection['1'] = dict.fromkeys(['negativeCount', 'positiveCount'],0)
        for instance in instances:
            attributeValue = instance[attributeIndex]
            classValue = instance[-1]
            if classValue == '1':
                attributeValueCollection[attributeValue]['positiveCount'] = attributeValueCollection[attributeValue]['positiveCount'] + 1
            else:
                attributeValueCollection[attributeValue]['negativeCount'] = attributeValueCollection[attributeValue]['negativeCount'] + 1

        zeroEntropy = self.getEntropy(attributeValueCollection['0']['negativeCount'],attributeValueCollection['0']['positiveCount'])
        oneEntropy = self.getEntropy(attributeValueCollection['1']['negativeCount'],attributeValueCollection['1']['positiveCount'])
        totalSamplesConsidered = len(instances)
        zeroSamples = attributeValueCollection['0']['negativeCount'] + attributeValueCollection['0']['positiveCount']
        oneSamples = attributeValueCollection['1']['negativeCount'] + attributeValueCollection['1']['positiveCount']

        expectedEntropy = (zeroSamples/float(totalSamplesConsidered)) * zeroEntropy + (oneSamples/float(totalSamplesConsidered)) * oneEntropy 
        gain = entropy - expectedEntropy
        return gain

    @classmethod
    def getInstances(self, data, instanceType):
        instances = []
        for instance in data:
            if instance[-1] == instanceType: #class matches instanceType
                instances.append(instance)
        return instances
    
    @classmethod
    def getEntropy(self, negativeSamplesCount, positiveSamplesCount):
        totalCount = negativeSamplesCount + positiveSamplesCount
        if totalCount == 0:
            return 0
        pMinus = negativeSamplesCount/float(totalCount)
        pPlus = positiveSamplesCount/float(totalCount)
        
        if pMinus == 0:
            entropy = -(pPlus) * math.log(pPlus,2)
        elif pPlus == 0:
            entropy = -(pMinus) * math.log(pMinus,2)
        else:
            entropy = -(pMinus) * math.log(pMinus,2) - (pPlus) * math.log(pPlus,2)
        return entropy  

    def inorder(self, node, depth):
        if node is None:
            return
        if node.isLeaf:
            print node.attribute
        else:
            print ""
            formattingstring = ""
            for i in range(depth):
                formattingstring = formattingstring + "| " 
            
            value = "0" if node.rightChild is not None else "1"
            print formattingstring + node.attribute + " = " + value + " : "
        
        self.inorder(node.leftChild, depth + 1)
        formattingstring = ""
        if node.isLeaf == False:
            for i in range(depth):
                formattingstring = formattingstring + "| " 
            
            value = "0" if node.rightChild is not None else "1"
            print formattingstring + node.attribute + " = " + value + " : "

        self.inorder(node.rightChild, depth + 1)

class ImpurityVarianceDecisionTree():

    def __init__(self):
        self.root = tree.Node()
    
    def generate(self, data):
        self.root.allNodeInstances = data
        
        #First row are class attributes except last element
        attributes = list(data[0][:-1])
        
        nodeQueue = [self.root]
        while nodeQueue:
            node = nodeQueue.pop(0) 
            node.negativeInstances = self.getInstances(node.allNodeInstances,'0')
            node.positiveInstances = self.getInstances(node.allNodeInstances,'1')
            varianceImpurity = self.getVarianceImpurity(len(node.negativeInstances), len(node.positiveInstances))
            if varianceImpurity == 0:
                node.isLeaf = True
                node.attribute = '1' if len(node.positiveInstances) != 0 else '0' #Assign either 0 or 1
            elif not attributes: #no attributes left to split tree
                node.isLeaf = True
                node.attribute = '0' if len(node.negativeInstances) > len(node.positiveInstances) else '1'
            else:
                node.attribute = self.getNodeAttribute(node.allNodeInstances, varianceImpurity, attributes)
                node.leftChild  = tree.Node()
                node.rightChild = tree.Node()
                node.leftChild.allNodeInstances = self.getAllNodeInstances(node.allNodeInstances, node.attribute, attributes,'0')
                node.rightChild.allNodeInstances = self.getAllNodeInstances(node.allNodeInstances, node.attribute, attributes,'1')
                nodeQueue.append(node.leftChild)
                nodeQueue.append(node.rightChild)

                #left subtree node addition
                if len(node.leftChild.allNodeInstances) == 0:
                    node.leftChild.attribute = '0' if len(node.negativeInstances) > len(node.positiveInstances) else '1'
                    node.leftChild.isLeaf = True
                
                attributes.remove(node.attribute)
                    # nodeQueue.append(node.leftChild)
                
                #right subtree node addition
                if len(node.rightChild.allNodeInstances) == 0:
                    node.rightChild.attribute = '0' if len(node.negativeInstances) > len(node.positiveInstances) else '1'
                    node.rightChild.isLeaf = True
                # else:
                #     attributes.remove(node.attribute)
                    # nodeQueue.append(node.rightChild)

    @classmethod
    def getAllNodeInstances(self, allInstances, attribute, allAttributes,value):
        instancesCorrespondingToGivenValue = []
        attributeIndex = allAttributes.index(attribute)
        for inst in allInstances[1:]:
            if inst[attributeIndex] == value:
                instancesCorrespondingToGivenValue.append(inst)
        return instancesCorrespondingToGivenValue

    @classmethod
    def getNodeAttribute(self, instances, varianceImpurity, attributes):
        gains = {}
        for attributeIndex, attribute in enumerate(attributes):
            gain = self.getGainForAttribute(instances, varianceImpurity, attributeIndex)
            gains[attribute] = gain

        maxGainAttribute = max(gains, key=gains.get)
        return maxGainAttribute
    
    @classmethod
    def getGainForAttribute(self, instances, varianceImpurity, attributeIndex):
        attributeValueCollection = dict.fromkeys(['0','1'])
        attributeValueCollection['0'] = dict.fromkeys(['negativeCount', 'positiveCount'],0)
        attributeValueCollection['1'] = dict.fromkeys(['negativeCount', 'positiveCount'],0)
        for instance in instances[1:]:
            attributeValue = instance[attributeIndex]
            classValue = instance[-1]
            if classValue == '1':
                attributeValueCollection[attributeValue]['positiveCount'] = attributeValueCollection[attributeValue]['positiveCount'] + 1
            else:
                attributeValueCollection[attributeValue]['negativeCount'] = attributeValueCollection[attributeValue]['negativeCount'] + 1

        zeroImpurity = self.getVarianceImpurity(attributeValueCollection['0']['negativeCount'],attributeValueCollection['0']['positiveCount'])
        oneImpurity = self.getVarianceImpurity(attributeValueCollection['1']['negativeCount'],attributeValueCollection['1']['positiveCount'])
        totalSamplesConsidered = len(instances)
        zeroSamples = attributeValueCollection['0']['negativeCount'] + attributeValueCollection['0']['positiveCount']
        oneSamples = attributeValueCollection['1']['negativeCount'] + attributeValueCollection['1']['positiveCount']

        expectedImpurity = (zeroSamples/float(totalSamplesConsidered)) * zeroImpurity + (oneSamples/float(totalSamplesConsidered)) * oneImpurity 
        gain = varianceImpurity - expectedImpurity
        return gain

    @classmethod
    def getInstances(self, data, instanceType):
        instances = []
        for i in range(1,len(data)):
            if data[i][-1] == instanceType: #class matches instanceType
                instances.append(i)
        return instances
    
    @classmethod
    def getVarianceImpurity(self, k0, k1):
        k = k0 + k1
        if k == 0 or k1 == 0 or k0 == 0:
            return 0
        pMinus = k0/float(k)
        pPlus = k1/float(k)
        impurity = pMinus * pPlus
        return impurity  