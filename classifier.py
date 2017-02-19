import dtree

class classifier:

	def classify(self, instanceData, rootNode, attributes):
		
		classification = ''
		correctClassificationCount = incorrectClassificationCount = 0

		for instance in instanceData[1:]:
			node = rootNode
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
				correctClassificationCount = correctClassificationCount + 1
			else:
				incorrectClassificationCount = incorrectClassificationCount + 1

		return correctClassificationCount*100/float(correctClassificationCount + incorrectClassificationCount)



