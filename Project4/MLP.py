from featureSelection import main
import os
import random
import math
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score 
from sklearn.metrics import classification_report 

''' The MLP will have 10 output neurons, 7 inputs and 1 hidden layer of 11 neurons. 
I choose this from rule of thumb online that hidden should have
(output + input) * 2/3 neurons. '''

class MLP:

    def __init__(self):
        # Stuff with files 
        self.feature_file_TRAIN = 0
        self.feature_file_TEST = 0
        self.test_file = 0
        # Count of neurons 
        self.num_output = 10
        self.num_input = 7
        self.num_hidden = 11
        # Weights, values, and others 
        self.output_of_hidden = []
        self.output_of_output = []

        self.output_derivative_values = []
        self.hidden_derivative_values = []

        self.hidden_weights = [[]]
        self.input_weights = [[]]

        self.inputs = []

        self.target_labels = []
        self.learning_rate = 0.1

    def prepare(self):
        ''' Just getting things ready, opening files and setting variables'''
        print("\nCreating the features files. \n")
        self.target_labels = main()
        self.feature_file_TRAIN = open('seven_and_nine_features_TRAIN.txt', 'r')
        self.feature_file_TEST = open('seven_and_nine_features_TEST.txt', 'r')
        for i in range(7):
            self.output_weights.append(random.uniform(-0.1, 0.1))
            self.input_weights.append(random.uniform(-0.1, 0.1))
        for i in range(self.num_input):
            for j in range(self.num_hidden):
                self.input_weights

    def derivative_output_error(self, prediction_y, target_t):
        return ((prediction_y - target_t) * prediction_y * (1 - prediction_y))

    def derivative_hidden_error(self, prediction_a, weigth_CK):
        first_half = ( prediction_a * ( 1 - prediction_a ))
        second_half = 0
        for k in range(self.num_output):
            second_half += weigth_CK * self.output_derivative_values[k]
        return first_half * second_half

    def adjust_hidden_weigths(self):
        randomized = [] # This makes the weigths be updated in random order
        for i in range(len(self.num_hidden)):
            randomized.append(i)
        random.shuffle(randomized)
        for w in randomized:
            for k in range(len(self.hidden_weights[w])):
                self.hidden_weights[w][k] = self.hidden_weights[w][k] - (self.learning_rate * self.output_derivative_values[k] * self.output_of_hidden[w])

    def adjust_input_weights(self):
        randomized = []
        for i in range(len(self.num_hidden)):
            randomized.append(i)
        random.shuffle(randomized)
        for i in randomized:
            for k in range(len(self.input_weights[i])):
                self.input_weights[i][k] = self.input_weights[i][k] - (self.learning_rate * self.hidden_derivative_values[k] * self.inputs[i])

    def sigmoid_function(self, value):
        return 1 / (1 + math.exp(-1 * value))
        
    def train(self):
        for a in range(1000): # 1000 epochs according to pdf
            if (a%100 == 0):
                print("These are the weigths every 100 epochs: ", end='')
                print(self.weights)
            for line in self.feature_file_TRAIN:

                features = line.split(',')
                self.predict(features)

                targets = [features[7], features[8], features[9], features[10], features[11], features[12],
                    features[13], features[14], features[15], features[16]]

                for x in range(len(self.output_of_output)):
                    if (self.output_of_output[x] != targets[x]): 
                        self.back_propagate()
            self.feature_file_TRAIN.seek(0)

    def predict(self, features):
        ''' Does the input times weight calculation for all inputs on the neuron'''
        input_sums = []
        for h in range(len(self.num_hidden)):
            sum = 0
            for i in range(len(self.input_weights[h])):
                sum += features[i] * self.input_weights[h][i]
            input_sums.append(sum)
        
        self.output_of_hidden = []
        for each_sum in input_sums:
            self.output_of_hidden.append(self.sigmoid_function(each_sum))
        
        hidden_sums = []
        for o in range(len(self.num_output)):
            sum = 0
            for i in range(len(self.hidden_weights[o])):
                sum += self.output_of_hidden[o] * self.hidden_weights[o][i]
            hidden_sums.append(sum)
        
        self.output_of_output = []
        for each_sum in hidden_sums:
            self.output_of_output.append(self.sigmoid_function(each_sum))
 

    def back_propagate(self, targets):
        self.output_derivative_values = []
        for x in range(len(self.num_output)):
            derived_value = self.derivative_output_error(self.output_of_output[x], targets[x])
            self.output_derivative_values.append(derived_value)
        
        self.hidden_derivative_values = []
        for x in range(len(self.num_hidden)):
            derived_value = self.derivative_hidden_error(self.output_of_hidden[x], self.hidden_weights[x])
            self.hidden_derivative_values.append(derived_value)

        self.adjust_hidden_weigths()

        self.adjust_input_weights()
    
    def test(self):
        ''' Begins the test, similar to train, except you don't adjust weights if it gets it wrong'''
        prediction_vector = [] 
        Correct_count = 0
        for line in self.feature_file_TEST:
            features = line.split(',')
            self.predict(features)
            index = self.output_of_output.index(1)
            prediction_vector.append(index)
            if (index == features[17]):
                Correct_count += 1
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
    neuron = MLP()
    neuron.prepare()
    neuron.train()
    neuron.test()
