import numpy as np
import copy, random, os, pandas as pd
import matplotlib.pyplot as plt
import warnings

'''def handle_warning(message, category, filename, lineno, file=None, line=None):
    print('A warning occurred:')
    print(message)
    print('Do you wish to continue?')

    while True:
        response = input('y/n: ').lower()
        if response not in {'y', 'n'}:
            print('Not understood.')
        else:
            break

    if response == 'n':
        raise category(message)

warnings.showwarning = handle_warning'''            # THIS IS FOR DEBUGGING PURPOSES

class CNN:
    def __init__(self):
        self.filters = [] # THESE NEVER CHANGE DURING THE BACK PROPAGATION
        self.TEST = []      # Contains the test images
        self.TRAIN = []     # Contains the training images
        self.W5_weights = [] # This one should have 2000*100 weights
        self.W0_weights = [] # This should be the 100 * 10
        self.learning_rate = 0.01
        self.labels = []
        self.derived_values_output = []
        self.derived_values_hidden = []
        self.values_of_hidden = []
        self.values_of_output = []
        self.best_W0_weights = []
        self.best_W5_weights = []
        self.best_correct_count = 0
        self.W5_bias_weights = []
        self.W0_bias_weights = []
    
    def setup(self):
        # Set up the filter values
        try:
            filter_file = open("filters.txt")
        except(FileNotFoundError, IOError):
            print ("The file was not found or the name of the file is not correct")
            print ("The name of the file has to be filters.txt")
        filters = []
        blocks = []
        column = []
        for i in range(9):
            column.append('')
        for i in range(9):
            blocks.append(copy.deepcopy(column))
        for i in range(20):
            filters.append(copy.deepcopy(blocks))

        row = 0
        column = 0
        line_count = 0

        for line in filter_file:
            values = line.split()
            line_count += 1
            for v in range(len(values)):
                filters[v][column][row] = (values[v])
            row +=1 
            if (row == 9):
                row = 0
            if line_count == 9:
                column += 1
                line_count = 0
        self.filters = np.array(filters)

        # Set up the images 
        self.TRAIN, self.TEST = self.extract_images()
        self.TRAIN = self.TRAIN[0:100]
        self.TEST = self.TEST[0:100]

        # Give random values to the weights
        for x in range(2000):
            self.W5_weights.append([])
            for y in range(100):
                self.W5_weights[x].append(random.uniform(-1.0, 1.0))
        self.W5_weights = np.array(self.W5_weights)
        
        for x in range(100):
            self.W0_weights.append([])
            for y in range(10):
                self.W0_weights[x].append(random.uniform(-1.0, 1.0))
        self.W0_weights = np.array(self.W0_weights)

        for x in range(100):
            self.W5_bias_weights.append(random.uniform(-1.0, 1.0))

        for x in range(10):
            self.W0_bias_weights.append(random.uniform(-1.0, 1.0))
        

    def open_images(self, path):
        print("Opening and extracting images from: " + path)
        images = []
        data = pd.read_csv(path)

        for i in range(0, data.shape[0]):              
            row = data.iloc[i].to_numpy()
            images.append(row)
        return images

    def extract_images(self):
        #randomize = [1,2,3,4,5,6,7,8,9]
        #randomize = [0]
        randomize = [0, 1, 5]
        random.shuffle(randomize)
        total_images = []
        total_test_images = []

        for x in randomize:
            images = self.open_images("data_set/train" + str(x) + ".csv")
            total_images += images

        random.shuffle(total_images)

        random.shuffle(randomize)
        for x in randomize:
            test_i = self.open_images("data_set/valid" + str(x) + ".csv")
            total_test_images += test_i

        return total_images, total_test_images

    def convo(self, image, output):
        # Apply the filter to the all the pixels of the image
        Fposx, Fposy = 0, 0
        image = image[1:]
        np.array(image)
        image = image.reshape([28, 28])
        filters = self.filters.tolist()
        filter_count = 0
        result = 0
        for f in filters:
            for posx in range(20):
                for posy in range(20):
                    for x in range(len(f)):
                        for y in range(len(f[x])): 
                            result += image[posx + x][posy + y] * float(f[y][x])
                    output[filter_count][posx][posy] = result
            filter_count += 1
                    
    def RELU(self, matrix):
        # If greater than 0 then leave alone, otherwise, turn negative
        new_matrix = matrix
        for f in range(len(matrix)):
            for x in range(len(matrix[f])):
                for y in range(len(matrix[f][x])):
                    if matrix[f][x][y] < 0:
                        new_matrix[f][x][y] = 0
        return new_matrix

    def pool(self, matrix):
        # Average the vlaues in a 2 x 2 windows? and replace those 4 values by the average?
        new_matrix = []
        stride = []
        result = []
        for i in range(10):
            result.append(0.0)
        for i in range(10):
            stride.append(copy.deepcopy(result))
        for i in range(20):
            new_matrix.append(copy.deepcopy(stride))

        posx_new, posy_new = 0, 0
        for f in range(len(matrix)):
            for x in range(0, len(matrix[f]), 2):
                for y in range(0, len(matrix[f][x]), 2):
                    average = (matrix[f][x][y] + matrix[f][x+1][y] + matrix[f][x][y+1] + matrix[f][x+1][y+1]) / 4
                    new_matrix[f][posx_new][posy_new] = average
                    posy_new += 1
                    if (posy_new == 10):
                        posy_new = 0
                        posx_new += 1
            posy_new, posx_new = 0, 0

        return new_matrix

    def reshape(self, matrix):
        # Flatten out the results after the pooling 
        new_matrix = np.array(matrix)
        new_matrix = new_matrix.reshape([1, 2000])
        return new_matrix

    def multiply_by_hidden(self, matrix):
        # Multiply the values by the weigths for the hidden layer
        row, column = matrix.shape
        if row != 1 or column != 2000:
            print ("There was an error with the shape of the matrix after reshape")
            exit(1)
        hidden_node_values = matrix.dot( self.W5_weights)
        temp = hidden_node_values.tolist()
        for x in range(len(temp[0])):
            temp[0][x] += 1 * self.W5_bias_weights[x]
        hidden_node_values = np.array(temp)
        return hidden_node_values

    def second_RELU(self, matrix):
        # Get rid of negative values in the 1 by 100 matrix
        new_matrix = []
        matrix = matrix.tolist()
        for x in matrix[0]:
            if x < 0:
                new_matrix.append(0)
            else:
                new_matrix.append(x)
        return new_matrix
    
    def multiply_by_output(self, matrix):
        # Multiply the values of hidden layer by wieghts of output layer
        matrix = np.array(matrix)
        output_of_output = matrix.dot( self.W0_weights)
        temp = output_of_output.tolist()
        for x in range(len(temp)):
            temp[x] += 1 * self.W0_bias_weights[x]
        output_of_output = np.array(temp)
        return output_of_output

    def soft_max(self, matrix):
        matrix = matrix.tolist()
        classification_percent = []
        total = sum(matrix)
        for e in matrix:
            classification_percent.append(e/ total)
        return classification_percent
    
    def back_propagation(self, classifications, expected, output_of_hidden, output_of_reshape):
        # Begin the back propagation, only W5 AND W0 change, not the filters
        self.derivatives_of_output(classifications, expected)
        self.derivatives_of_hidden(output_of_hidden)
        self.update_output_weights(output_of_hidden)
        self.update_hidden_weights(output_of_reshape)

    def derivatives_of_output(self, classifications, expected):
        self.derived_values_output = []
        for i in range(len(classifications)):
            y = classifications[i]
            t = expected[i]
            self.derived_values_output.append( (y - t) * y * (1 - y))

    def derivatives_of_hidden(self, output_of_hidden):
        self.derived_values_hidden = []
        summation = 0
        temp = output_of_hidden.tolist()
        for x in range(len(self.W0_weights)):
            for y in range(len(self.W0_weights[x])):
                summation += self.W0_weights[x][y] * self.derived_values_output[y]
            self.derived_values_hidden.append(temp[0][x] * (1 - temp[0][x]) * summation)
    
    def update_output_weights(self, output_of_hidden):
        # This updates the weights for the output layer
        for x in range(len(self.W0_weights)):
            for y in range(len(self.W0_weights[x])):
                temp = self.learning_rate * self.derived_values_output[y] * output_of_hidden[0][x]
                self.W0_weights[x][y] = self.W0_weights[x][y] - temp

        for x in range(len(self.W0_bias_weights)):
            self.W0_bias_weights[x] = self.W0_bias_weights[x] - self.learning_rate * self.derived_values_output[x] * output_of_hidden[0][x]
    
    def update_hidden_weights(self, output_of_reshape):
        # This updates the weights for the hidden layer
        for x in range(len(self.W5_weights)):
            for y in range(len(self.W5_weights[x])):
                self.W5_weights[x][y] = self.W5_weights[x][y] - self.learning_rate * self.derived_values_hidden[y] * output_of_reshape[0][x] 

        for x in range(len(self.W5_bias_weights)):
            self.W5_bias_weights[x] = self.W5_bias_weights[x] - self.learning_rate * self.derived_values_hidden[x] * output_of_reshape[0][x]

    def train(self):
        # Do the training operations

        image_count = 0
        convo_result = []
        stride = []
        result = []
        for i in range(20):
            result.append(0.0)
        for i in range(20):
            stride.append(copy.deepcopy(result))
        for i in range(20):
            convo_result.append(copy.deepcopy(stride))

        for image in self.TRAIN:

            if (image_count % 10 == 0):
                print("\nIt has processed 100 images\nThere are %i left" % (len(self.TRAIN) - image_count))
            image_count += 1

            self.convo(image, convo_result)

            RELU_result = self.RELU(convo_result)

            Pool_result = self.pool(RELU_result)

            Reshape_result = self.reshape(Pool_result)

            Hidden_layer_result  = self.multiply_by_hidden(Reshape_result)

            Second_RELU_output = self.second_RELU(Hidden_layer_result)

            Output_layer_output = self.multiply_by_output(Second_RELU_output)

            classification = self.soft_max(Output_layer_output)

            if (classification.index(max(classification)) != image[0]):
                expected = [0] * 10
                expected[image[0]] = 1
                self.back_propagation(classification, expected, Hidden_layer_result, Reshape_result) 

    def test(self):
        # Do the test operations
        correct_count = 0
        image_count = 0

        convo_result = []
        stride = []
        result = []
        for i in range(20):
            result.append(0.0)
        for i in range(20):
            stride.append(copy.deepcopy(result))
        for i in range(20):
            convo_result.append(copy.deepcopy(stride))

        for image in self.TEST:
            
            if (image_count % 100 == 0):
                print("It has processes 100 images\nThere are %i left" % (len(self.TEST) - image_count))
            image_count += 1
            self.convo(image, convo_result)

            RELU_result = self.RELU(convo_result)

            Pool_result = self.pool(RELU_result)

            Reshape_result = self.reshape(Pool_result)

            Hidden_layer_result  = self.multiply_by_hidden(Reshape_result)

            Second_RELU_output = self.second_RELU(Hidden_layer_result)

            Output_layer_output = self.multiply_by_output(Second_RELU_output)

            classification = self.soft_max(Output_layer_output)

            if (classification.index(max(classification)) == image[0]):
                correct_count += 1

        if correct_count > self.best_correct_count:
            self.best_correct_count = correct_count/(len(self.TEST))
            self.best_W0_weights = self.W0_weights
            self.best_w5_weights = self.W5_weights

    def epochs(self):
        N = input("How many epochs should be run (must be a number): ")
        for x in range(int(N)):
            self.train() 
            self.test()
    
    def final_results(self):
        print("The best network had a success ration of: %f" % self.best_correct_count)
        


if __name__=='__main__':

    cnn = CNN()
    cnn.setup()
    cnn.epochs()
    cnn.final_results()