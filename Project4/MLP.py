from featureselection2 import main
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

        self.hidden_weights = [[],[],[],[],[],[],[],[],[],[]]
        self.input_weights  = [[],[],[],[],[],[],[],[],[],[],[]]

        self.inputs = []

        self.target_labels = []
        self.learning_rate = 0.1

    def prepare(self):
        ''' Just getting things ready, opening files and setting variables'''
        print("\nCreating the features files. \n")
        self.target_labels = main()
        self.feature_file_TRAIN = open('image_features_TRAIN.txt', 'r')
        self.feature_file_TEST = open('image_features_TEST.txt', 'r')
        
        for i in range(self.num_hidden):
            for j in range(self.num_input):
                self.input_weights[i].append(random.uniform(-0.1, 0.1))

        for i in range(self.num_output):
            for j in range(self.num_hidden):
                self.hidden_weights[i].append(random.uniform(-0.1, 0.1))

    # The following functions are all just equations such as the derivatives or the sigmoid 
    # along with the logic required to update the weights.
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
        
    '''def print_weights(self):
        print("These are the weights every 100 epochs: ")
        print("These are the weights of the inputs:                            These are the weights of the hidden layer:")
        for x in range(self.ad)'''
    
    # Calls the prediction function to begin the process of training the weights
    # Only trains if the prediction was wrong otherwise, continue
    def train(self):
        for a in range(1000): # 1000 epochs according to pdf
            
            if (a%100 == 0): #Do we really need to print out the weights? There is about 180 weights total. It would be overwhelming unless you can think of a smart way to show them 
                print("100 epochs passed")
            for line in self.feature_file_TRAIN:

                features = line.split(',')
                features = [float(x) for x in features]

                self.predict(features)
                self.inputs = features[0:7]

                target = features[-1]

                passed_iteration = False
                for x in range(len(self.output_of_output)):
                    if (self.output_of_output[x] == 1):
                        if (x == target):
                            passed_iteration = True
                        else:
                            passed_iteration = False

                if (not passed_iteration):
                    self.back_propagate()
            self.feature_file_TRAIN.seek(0)

    # Begins the prediction. Calculates the sum of the inputs from input and 
    # hidden layers and save the outputs into lists that will be used for back propagation
    def predict(self, features):
        ''' Does the input times weight calculation for all inputs on the neuron'''
        input_sums = []
        for i in range((self.num_input)):
            sum = 0
            for h in range((self.num_hidden)):
                sum += features[i] * self.input_weights[h][i]
            input_sums.append(sum)
        
        self.output_of_hidden = []
        for each_sum in input_sums:
            self.output_of_hidden.append(self.sigmoid_function(each_sum))
        
        hidden_sums = []
        for h in range((self.num_input)):
            sum = 0
            for o in range((self.num_output)):
                sum += self.output_of_hidden[h] * self.hidden_weights[o][h]
            hidden_sums.append(sum)
        
        self.output_of_output = []
        for each_sum in hidden_sums:
            self.output_of_output.append(self.sigmoid_function(each_sum))
 
    # This function first calculates the derivative values from the output and hidden layers 
    # then uses those values to update the weights
    def back_propagate(self, targets):
        self.output_derivative_values = [] #Clear the lists 
        for x in range((self.num_output)):
            derived_value = self.derivative_output_error(self.output_of_output[x], targets[x]) # I NEED TO TELL IT THE TARGETS FOR EACH OF THE 10 NEURONS

            
            self.output_derivative_values.append(derived_value)
        
        self.hidden_derivative_values = []
        for x in range((self.num_hidden)):
            derived_value = self.derivative_hidden_error(self.output_of_hidden[x], self.hidden_weights[x])
            self.hidden_derivative_values.append(derived_value)

        self.adjust_hidden_weigths()

        self.adjust_input_weights()
    
    # Begins the testing phase of the program. 
    # Not much else to say 
    def test(self):
        print("\nBeginning the tests")
        prediction_vector = [] 
        Correct_count = 0
        pos = 0
        for line in self.feature_file_TEST:
            features = line.split(',')
            features = [float(x) for x in features]
            self.predict(features)

            target = features[-1]
            result = target
            correct = True

            for x in range(len(self.output_of_output)):
                if (self.output_of_output[x] == 1):
                    if (x == target):
                        continue
                    else:
                        correct = False
                        result = x

            prediction_vector.append(result)

            if (correct):
                Correct_count += 1

        self.create_test_result_file(prediction_vector)
        print("Success Ratio: ", round(Correct_count/(len(prediction_vector)), 2))

    # Creates the output file 
    # after the tests
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
