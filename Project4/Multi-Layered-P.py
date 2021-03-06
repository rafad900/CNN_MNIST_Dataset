from featureselection2 import main
import os
import random
import math

class MLP:

    def __init__(self):
        # Stuff with files 
        self.feature_file_TRAIN = 0
        self.feature_file_TEST = 0
        self.test_file = 0
        # Count of neurons 
        self.num_output = 10
        self.num_input = 7
        # Weights, values, and others 
        self.output_of_output = []

        self.input_weights = [[],[],[],[],[],[],[],[],[],[]]
        self.lowest_error_weights  = [[],[],[],[],[],[],[],[],[],[]]
        self.inputs = []
        self.success_ration = 0

        self.target_labels = []
        self.learning_rate = 0.1

    def prepare(self):
        ''' Just getting things ready, opening files and setting variables'''
        print("\nCreating the features files. \n")
        self.target_labels = main()
        self.feature_file_TRAIN = open('image_features_TRAIN.txt', 'r')
        self.feature_file_TEST = open('image_features_TEST.txt', 'r')
        
        for i in range(self.num_output):
            for j in range(self.num_input):
                self.input_weights[i].append(random.uniform(-0.1, 0.1))

    def adjust_input_weights(self, targets):
        '''randomized = []
        for i in range((self.num_output)):
            randomized.append(i)
        random.shuffle(randomized)'''
        for i in range((self.num_output)):
            for k in range(len(self.input_weights[i])):
                if (targets[i] == self.output_of_output[i]):
                    continue 
                self.input_weights[i][k] = self.input_weights[i][k] - (self.learning_rate * (self.output_of_output[i] - targets[i]) * self.inputs[k]) # THIS MIGHT BE OFF BY THE inputs[k]  
    
    def create_all_targets(self, target):
        targets = [0,0,0,0,0,0,0,0,0,0]  # One value for each of the ouput neurons 
        targets[int(target)] = 1
        return targets

    def print_weights(self, value):
        print("{} epochs passed, each line is an output neuron with weights from each of the 7 inputs: ".format(str(value)))
        for x in range(len(self.input_weights)):
            print("Output  %i Weights: " % (x), end='')
            print(self.input_weights[x])
        print("------------------------------------------------------------------------------------------------")

    # Calls the prediction function to begin the process of training the weights
    # Only trains if the prediction was wrong otherwise, continue
    def train(self):
        print("\nBeginning to train the network\n")
        for a in range(1000): # 1000 epochs according to pdf
            
            if (a%100 == 0): #Do we really need to print out the weights? Theres about 70 of them. Can you think of a smart way to do it?
                self.print_weights(a)
                ratio = self.test()
                if (ratio > self.success_ration):
                    self.success_ration = ratio
                    self.lowest_error_weights = self.input_weights
            
            for line in self.feature_file_TRAIN:
                
                features = line.split(',')
                features = [float(x) for x in features]

                self.predict(features)
                self.inputs = features[0:7]

                target = features[-1]
                all_targets = self.create_all_targets(target)

                passed_iteration = False
                for x in range(len(self.output_of_output)):
                    if (self.output_of_output[x] == 1):
                        if (x == target):
                            passed_iteration = True
                            continue
                        else:
                            passed_iteration = False # If the incorrect index of the output list is activated, the it did not pass
                            break
                
                if (not passed_iteration):
                    self.adjust_input_weights(all_targets)
                
            self.feature_file_TRAIN.seek(0)
        
        self.input_weights = self.lowest_error_weights


    # Begins the prediction. Calculates the sum of the inputs from input and 
    # hidden layers and save the outputs into lists that will be used for back propagation
    def predict(self, features):
        ''' Does the input times weight calculation for all inputs on the neuron'''
        input_sums = []
        for i in range((self.num_output)):
            sum = 0
            for h in range((self.num_input)):
                sum += features[h] * self.input_weights[i][h]
            input_sums.append(sum)
        
        self.output_of_output = []
        for each_sum in input_sums:
            if (each_sum <= 0):
                self.output_of_output.append(0)
            else:
                self.output_of_output.append(1)
    
    # Begins the testing phase of the program. 
    # Not much else to say 
    def test(self):
        self.prediction_vector = [] 
        Correct_count = 0
        pos = 0
        for line in self.feature_file_TEST:
            features = line.split(',')
            features = [float(x) for x in features]
            self.predict(features)

            target = features[-1]
            result = target
            correct = False

            for x in range(len(self.output_of_output)):
                if (self.output_of_output[x] == 1):
                    if (x == target):
                        correct = True
                    else:
                        result = x

            self.prediction_vector.append(result)

            if (correct):
                Correct_count += 1

        self.feature_file_TEST.seek(0)
        return round(Correct_count/(len(self.prediction_vector)), 2)

    # Creates the output file 
    # after the tests
    def create_test_result_file(self ):
        print("\n\nCreating new file that will contain predicted labels seperated by space\n")
        test_predictions = open("test_prediction.txt", 'w')
        for v in self.prediction_vector:
            test_predictions.write("%s " % v)
        test_predictions.close()


if __name__=='__main__':
    print("\n\nThis module will create the neuron and train it using the data from the file created in the featureSelection.py")
    print("If the file does not exits, then it will create it and use it")
    neuron = MLP()
    neuron.prepare()
    neuron.train()
    print("\nBeginning the tests")
    ratio = neuron.test()
    neuron.create_test_result_file()
    print("Best success Ratio: ", ratio)

