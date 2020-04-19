from featureSelection import main
import os
import random
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score 
from sklearn.metrics import classification_report 


class Neuron:

    # SELF IN THE FUNCTION AND STUFF JUST MEANS THAT IT BELONGS TO THE CLASS 
    def __init__(self):
        self.feature_file_TRAIN = 0
        self.feature_file_TEST = 0
        self.weights = []
        self.threshold = 0
        self.test_file = 0
        self.target_labels = []

    def prepare(self):
        ''' Just getting things ready, opening files and setting variables'''
        if (os.path.exists('seven_and_nine_features_TRAIN.txt') and os.path.exists('seven_and_nine_features_TEST.txt')):
            print("\nIt found the file ")
            self.feature_file_TRAIN = open('seven_and_nine_features_TRAIN.txt', 'r')
            self.feature_file_TEST = open('seven_and_nine_features_TEST.txt', 'r')
        else:
            print("\nIt did not find the file, calling main from featureSelection.py")
            self.target_labels = main()
            self.feature_file_TRAIN = open('seven_and_nine_features_TRAIN.txt', 'r')
            self.feature_file_TEST = open('seven_and_nine_features_TEST.txt', 'r')
        for i in range(7):
            self.weights.append(random.uniform(-0.1, 0.1))
        print("These are the starting weights: ", end='')
        print(self.weights)
        print()
        
    def train(self):
        for a in range(1000): # 1000 epochs according to pdf
            if (a%100 == 0):
                print("These are the weigths every 100 epochs: ", end='')
                print(self.weights)
            for line in self.feature_file_TRAIN:
                features = line.split(',')
                result = self.predict(features)
                if (result != int(features[-1])):
                    self.adjust_weights(result, features)
            #print("These are the weights at the end of iteration: ", end='')
            #print(self.weights)                    DEBUGGING PURPOSES
            self.feature_file_TRAIN.seek(0)

        
    def adjust_weights(self, result, features):
        ''' This is called when the training label doesn't match the actual label'''
        y, t = result, int(features[-1])
        w0 = self.weights[0] - 0.1*(y - t) * -1
        w1 = self.weights[1] - 0.1*(y - t) * float(features[0])
        w2 = self.weights[2] - 0.1*(y - t) * float(features[1])
        w3 = self.weights[3] - 0.1*(y - t) * float(features[2])
        w4 = self.weights[4] - 0.1*(y - t) * float(features[3])
        w5 = self.weights[5] - 0.1*(y - t) * float(features[4])
        w6 = self.weights[6] - 0.1*(y - t) * float(features[5])
        self.weights = [w0, w1, w2, w3, w4, w5, w6]

    def predict(self, features):
        ''' Does the input times weight calculation for all inputs on the neuron'''
        sum = 0
        for i in range(len(self.weights)):
            sum += float(features[i]) * self.weights[i]
        if (sum <= 0):
            return 0
        else: return 1
    
    def test(self):
        ''' Begins the test, similar to train, except you don't adjust weights if it gets it wrong'''
        prediction_vector = [] 
        i = 0
        Correct_count = 0
        for line in self.feature_file_TEST:
            features = line.split(',')
            result = self.predict(features)
            if (result == 0):
                prediction_vector.append('7')
                if (self.target_labels[i] == 7):
                    Correct_count+=1
            else:
                prediction_vector.append('9')
                if (self.target_labels[i] == 9):
                    Correct_count+=1
            i+=1
        self.create_test_result_file(prediction_vector)
        print("Success Ratio: ", round(Correct_count/(len(prediction_vector)), 2))

    
    def create_test_result_file(self, vector):
        print("\n\nCreating new file that will contain predicted labels seperated by space\n")
        test_predictions = open("test_prediction.txt", 'w')
        for v in vector:
            test_predictions.write("%s " % v)
        test_predictions.close()


if __name__=='__main__':
    print("\n\nThis module will create the neuron and train it using the data from the file created in the featureSelection.py")
    print("If the file does not exits, then it will create it and use it")
    neuron = Neuron()
    neuron.prepare()
    neuron.train()
    neuron.test()
