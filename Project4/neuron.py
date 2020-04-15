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
        for i in range(7):
            self.weights.append(random.uniform(-0.1, 0.1))
        
    def train(self):
        for a in range(1000): # 1000 epochs according to pdf
            for line in self.feature_file:
                features = line.split(',')
                result = self.predict(features)
                if (result != int(features[-1])):
                    self.adjust_weights(result, features)

    def adjust_weights(self, result, features):
        y, t = 0, 0
        if (int(features[-1]) == 9):
            t = 1
        if (int(features[-1]) == 9):
            y == 1
        w0 = self.weights[0] - 0.1*(y - t) * -1
        w1 = self.weights[1] - 0.1*(y - t) * features[0]
        w2 = self.weights[2] - 0.1*(y - t) * features[1]
        w3 = self.weights[3] - 0.1*(y - t) * features[2]
        w4 = self.weights[4] - 0.1*(y - t) * features[3]
        w5 = self.weights[5] - 0.1*(y - t) * features[4]
        w6 = self.weights[6] - 0.1*(y - t) * features[5]
        self.weights = [w0, w1, w2, w3, w4, w5, w6]

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

