import csv
import dtree
import utility
import classifier

def main():
    data = utility.readCSV("data_sets1/training_set.csv")
    myDecisionTree = dtree.ID3DecisionTree()
    # myDecisionTree = dtree.ImpurityVarianceDecisionTree()
    myDecisionTree.generate(data)

    myDecisionTree.inorder(myDecisionTree.root, 0)
    #Run generated decision tree classification on validationData
    validationData = utility.readCSV("data_sets1/test_set.csv")
    instanceClassifier = classifier.classifier()
    instanceClassifier.classify(validationData, myDecisionTree)



if __name__ == "__main__":
    main()