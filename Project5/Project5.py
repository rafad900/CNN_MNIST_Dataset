import numpy as np
import copy, random, os, pandas as pd

class CNN:
    def __init__(self):
        self.filters = [] # THESE NEVER CHANGE DURING THE BACK PROPAGATION
        self.TEST = []      # Contains the test images
        self.TRAIN = []     # Contains the training images
        self.W5_weights = [] # This one should have 2000*100 weights
        self.W0_weights = [] # This should be the 100 * 10
        self.learning_rate = 0.01
        self.labels = []
    
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
            column.append()
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

        # Give random values to the weights
        for x in range(2000):
            self.W5_weights.append([])
            for y in range(100):
                self.W5_weights[x].append(random.uniform(-1.0, 1.0))
        
        for x in range(100):
            self.W0_weights.append([])
            for y in range(10):
                self.W0_weights[y].append(random.uniform(-1.0, 1.0))
        

    def open_images(self, path):
        print("Opening and extracting images")
        images = []
        data = pd.read_csv(path)

        for i in range(0, data.shape[0]):              
            row = data.iloc[i].to_numpy()
            images.append(row)
        return images

    def extract_images(self):
        randomize = [1,2,3,4,5,6,7,8,9]
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

    def convo(self):
        #apply the filter to the images 
        return 0

    def RELU(self):
        # If greater than 0 then leave alone, otherwise, turn negative
        return 0

    def pool(self):
        # Average the vlaues in a 2 x 2 windows? and replace those 4 values by the average?
        return 0

    def reshape(self):
        # Flatten out the results after the pooling 
        return 0

    def multiply_by_hidden(self):
        # Multiply the values by the weigths for the hidden layer
        return 0
    
    def multiply_by_output(self):
        # Multiply the values of hidden layer by wieghts of output layer
        return 0

    def soft_max(self):
        # Classification of image
        return 0
    
    def back_propagation(self):
        # Begin the back propagation, only W5 AND W0 change, not the filters
        return 0

    def train(self):
        # Do the training operations
        return 0

    def test(self):
        # Do the test operations
        return 0