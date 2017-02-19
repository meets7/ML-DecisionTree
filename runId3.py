import csv
import dtree
import utility
import classifier
import tree
import sys

def main():
    #Read command line arguments
    if len(sys.argv) < 7:
    	print "Incorrect number of arguments given. \n Usage: python runId3.py <K> <L> <path-to-training-set> <path-to-validation-set> <path-to-test-set> <to-print> \n to-print can be yes/no"
    	return

    print sys.argv[0]
    k = int(sys.argv[1])
    l = int(sys.argv[2])
    trainingDataPath = sys.argv[3]
    validationDataPath = sys.argv[4]
    testDataPath = sys.argv[5]
    toPrint = sys.argv[6]
    # k = 8
    # l = 25
    # trainingDataSetPath = "data_sets2/training_set.csv"
    # # validationDataSetPath = sys.argv[4]
    # testDataSetPath = "data_sets2/test_set.csv"
    # toPrint = "yes"

    #Read data from files
    data = utility.readCSV(trainingDataPath)
    validationData = utility.readCSV(validationDataPath)
    testData = utility.readCSV(testDataPath)

    #Separate attributes' row from data
    originalTrainingAttributes = list(data[0][:-1])
    data.remove(data[0])
    originalValidationAttributes = list(validationData[0][:-1])
    validationData.remove(validationData[0])
    originalTestDataAttributes = list(testData[0][:-1])
    testData.remove(testData[0])

    #Generate decision treeusing information gain heuristic
    trainingAttributes = originalTrainingAttributes[:]
    myDecisionTree = dtree.ID3DecisionTree("infogain")
    myDecisionTree.root.allNodeInstances = data
    myDecisionTree.generate(myDecisionTree.root, trainingAttributes)
    
    if toPrint == "yes":
        tree.printInorder(myDecisionTree.root, 0)

    #Run classification on test data
    instanceClassifier = classifier.classifier()
    accuracy = instanceClassifier.classify(testData, myDecisionTree.root, originalTestDataAttributes)
    utility.prettyPrintResults(accuracy,myDecisionTree.heuristic)

    #After pruning
    validationAttributes = originalValidationAttributes[:]
    prunedTree1 = myDecisionTree.getPrunedDecisionTree(l,k,validationData,validationAttributes, accuracy)
    accuracy = instanceClassifier.classify(testData, prunedTree1.root, originalTestDataAttributes)
    utility.prettyPrintResults(accuracy,myDecisionTree.heuristic, "after pruning")

    #Run ID3 using impurity variance heuristic
    trainingAttributes = originalTrainingAttributes[:]
    myDecisionTree2 = dtree.ID3DecisionTree("impurityVariance")
    myDecisionTree2.root.allNodeInstances = data
    myDecisionTree2.generate(myDecisionTree2.root, trainingAttributes)

    if toPrint == "yes":
        tree.printInorder(myDecisionTree2.root, 0)
    
    #Run generated decision tree classification on test data
    # instanceClassifier = classifier.classifier()
    accuracy = instanceClassifier.classify(testData, myDecisionTree2.root, originalTestDataAttributes)
    utility.prettyPrintResults(accuracy,myDecisionTree2.heuristic)

    #After pruning
    validationAttributes = originalValidationAttributes[:]
    prunedTree2 = myDecisionTree2.getPrunedDecisionTree(l,k,validationData,validationAttributes, accuracy)
    accuracy = instanceClassifier.classify(testData, prunedTree2.root, originalTestDataAttributes)
    utility.prettyPrintResults(accuracy,myDecisionTree2.heuristic, "after pruning")

if __name__ == "__main__":
    main()