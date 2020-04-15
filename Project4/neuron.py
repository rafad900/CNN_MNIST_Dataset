from featureSelection import main
import os
import random

class Neuron:
    def __init__(self):
        self.feature_file = 0
        self.weights = []
        self.threshold = 0

    def prepare(self):
        if (os.path.exists('seven_and_nine_features.txt')):
            print("\nIt found the file ")
            self.feature_file = open('seven_and_nine_features.txt', 'r')
        else:
            print("\nIt did not find the file, calling main from featureSelection.py")
            main()
            self.feature_file = open('seven_and_nine_features.txt', 'r')
        for i in range(4):
            self.weights.append(random.uniform(-0.1, 0.1))
        
    def train(self):
        for line in self.feature_file:
            features = line.split(',')
            result = self.predict(features)
            if (result != int(features[-1])):
                a = 1


    def adjust_weights(self, result, target):
        w0 = self.weights[0] - 1
    def predict(self, features):
        sum = 0
        for i in range(len(self.weights)):
            sum += features[i] * self.weights
        if (sum <= 0):
            return 7
        else: return 9
            
    
if __name__=='__main__':
    print("\n\nThis module will create the neuron and train it using the data from the file created in the featureSelection.py")
    print("If the file does not exits, then it will create it and use it")
    neuron = Neuron()
    neuron.prepare()
    neuron.train()

