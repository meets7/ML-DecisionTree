import dtree

class classifier:

	def classify(self, instanceData, decisionTree):
		
		attributes = instanceData[0][:-1]
		classification = ''
		correctClassification = incorrectClassification = 0
		for instance in instanceData[1:]:
			node = decisionTree.root
			while True:
				if node.isLeaf:
					classification = node.attribute
					break
				else:
					attributeIndex = attributes.index(node.attribute)
					if instance[attributeIndex] == '0':
						node = node.leftChild
					else:
						node = node.rightChild

			if classification == instance[-1]:
				correctClassification = correctClassification + 1
			else:
				incorrectClassification = incorrectClassification + 1

		print str((correctClassification*100)/(correctClassification + incorrectClassification)) + '%'



