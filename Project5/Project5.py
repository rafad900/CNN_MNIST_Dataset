import numpy as np
import copy, random, os, pandas as pd
import matplotlib.pyplot as plt
import warnings
import time

class CNN:
    def __init__(self):
        self.filters = np.zeros([20,9,9]) # THESE NEVER CHANGE DURING THE BACK PROPAGATION
        self.TRAIN = []     # Contains the training images
        self.nhidden = 100

        # self.W5_weights = np.zeros([2000, self.nhidden ], dtype =float)
        # self.W0_weights = np.zeros([100,10], dtype = float)

        self.W5_weights = (np.random.rand( 2000,self.nhidden)-0.5)*2/np.sqrt(2000 )
        self.W0_weights = (np.random.rand(self.nhidden, 10)-0.5)*2/np.sqrt(self.nhidden)        # Give random values to the weights
        self.learning_rate = .000001
        self.derived_values_hidden = np.zeros([2000, self.nhidden ], dtype =float)
        self.derived_values_output = np.zeros([100,10], dtype = float)
        self.best_ratio =  0
        self.filteredTrain = np.empty([10000,2001])
        self.found_file = False
        self.ran_one_epoch = False
        self.filtered_data = np.empty([10000,2001])
        self.TESTfile_name = ""
        self.epoch_best_ratio = 0


    def find_csv_filtered_file(self):
        if (os.path.isfile("filtereddata.csv") or self.ran_one_epoch):
            print("filtereddata.csv was found. Extracting data right now.")
            self.found_file = True 
            open_file = pd.read_csv("filtereddata.csv", header=None)
            i = 0
            for line in range(open_file.shape[0]):
                temp = open_file.iloc[line].to_numpy()
                self.filtered_data [i] =  temp 
                i+=1


    def setup(self):
        # Set up the filter values
        try:
            filter_file = open("filters.txt")
        except(FileNotFoundError, IOError):
            print ("The file was not found or the name of the file is not correct")
            print ("The name of the file has to be filters.txt")

        row = 0
        column = 0
        line_count = 0

        for line in filter_file:
            values = line.split()
            line_count += 1
            for v in range(len(values)):
                self.filters[v][column][row] = (values[v])
            row +=1 
            if (row == 9):
                row = 0
            if line_count == 9:
                column += 1
                line_count = 0

        self.find_csv_filtered_file()

        if (not self.found_file):
            self.TRAIN = self.extract_images()

        

    def open_images(self, path):
        print("Opening and extracting images from: " + path)
        images = []
        data = pd.read_csv(path,  header=None)

        for i in range(0, data.shape[0]):              
            row = data.iloc[i].to_numpy()
            images.append(row)
        return images

    def extract_images(self):
        randomize = [0,1,2,3,4,5,6,7,8,9]
        random.shuffle(randomize)
        total_images = []

        for x in randomize:
            images = self.open_images("data_set/train" + str(x) + ".csv")
            total_images += images

        random.shuffle(total_images)
        return total_images

    
    def convo(self, image, output):
        # Apply the filter to the all the pixels of the image
        image = image[1:]
        np.array(image)
        image = image.reshape([28, 28])
        # loop over the input image, "sliding" the filter across
	    # each (x, y)-coordinate from left-to-right and top to
	    # bottom
        for y in np.arange(0, 20 ):
            for x in np.arange(0, 20):
                # extract the slice of the image
                image_slice = image[y :y  + 9, x :x  + 9]
                # perform the actual convolution by taking the
                # element-wise multiplicate then summing the matrix
                for i in range (20):
                    result = np.einsum('ij,ij',image_slice,self.filters[i])
                    output[i][y][x] = result
          

    def pool(self, matrix):
        # Average the values in a 2 x 2 windows? and replace those 4 values by the average?
        new_matrix = np.zeros([20,10,10], dtype = float)
        posx_new, posy_new = 0, 0
        for f in range(10):
            for x in range(0, 10, 2):
                for y in range(0, 20, 2):
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
        return matrix.reshape([1, 2000])

    def multiply_by_hidden(self, matrix):
        # Multiply the values by the weigths for the hidden layer
        row, column = matrix.shape
        if row != 1 or column != 2000:
            print ("There was an error with the shape of the matrix after reshape")
            exit(1)
        hidden_node_values = np.dot( matrix ,self.W5_weights)
        return hidden_node_values

    
    def multiply_by_output(self, matrix):
        # Multiply the values of hidden layer by weights of output layer
        output_of_output = np.dot( matrix ,self.W0_weights)
        return output_of_output

    def soft_max(self, matrix):
        normalisers = np.sum(np.exp(matrix),axis=1)*np.ones((1,np.shape(matrix)[0]))
        return np.transpose(np.transpose(np.exp(matrix))/normalisers)
        # e_x = np.exp(matrix - np.max(matrix))
        # return (e_x)/ (e_x.sum())
    
    #     back_propagation(classification, expected, Second_RELU_output, Reshape_result, image_count) 
    def back_propagation(self, classifications, expected, output_of_hidden, output_of_reshape, image_count):
        # Begin the back propagation, only W5 AND W0 change, not the filters
        delta = np.zeros([1,10], dtype = float)
        delta = self.derivatives_of_output(classifications, expected, output_of_hidden)
        self.derivatives_of_hidden(output_of_hidden, output_of_reshape, delta)
        if (image_count % 100 == 0):
            self.update_output_weights()
            self.update_hidden_weights()
            self.derived_values_hidden = np.zeros([2000, self.nhidden ], dtype =float)
            self.derived_values_output = np.zeros([100,10], dtype = float)

    def derivatives_of_output(self, classifications, expected, output_of_hidden):
        delta = np.subtract(np.array(expected ) , classifications )
        self.derived_values_output = np.add(self.derived_values_output , np.dot( np.transpose(output_of_hidden), delta))
        return delta
        

    def derivatives_of_hidden(self, output_of_hidden , output_of_reshape, delta):
        e5 = np.dot(delta , np.transpose(np.array(self.W0_weights)))
        self.derived_values_hidden = np.add(self.derived_values_hidden ,  np.dot (np.transpose(output_of_reshape), e5.clip(0) ) )#delta5 = RELU(e5)

    
    def update_output_weights(self):
        # This updates the weights for the output layer
        self.derived_values_output =  np.true_divide(self.derived_values_output , 100)
        self.W0_weights = np.add(self.W0_weights , self.derived_values_output * self.learning_rate)

    
    def update_hidden_weights(self):
        # This updates the weights for the hidden layer
        self.derived_values_hidden =  np.true_divide(self.derived_values_hidden , 100)
        self.W5_weights = np.add(self.W5_weights , self.derived_values_hidden * self.learning_rate)


    def train(self):
        # Do the training operations
        image_count = 0
        correct_count = 0
                
        convo_result = np.zeros([20,20,20])

        if (self.ran_one_epoch):
            self.find_csv_filtered_file()
            self.ran_one_epoch = False

        i = 0
        if (not self.found_file):
            print("Its running from scratch")
            for image in self.TRAIN:
                image_count += 1

                self.convo(image, convo_result)

                RELU_result = convo_result.clip(0) # first RELU

                Pool_result = self.pool(RELU_result)

                Reshape_result = self.reshape(Pool_result)

                a = Reshape_result.tolist()
                a[0].insert(0, image[0])

                aReshape_result = np.array(a)
                self.filteredTrain[image_count -1] = aReshape_result
               
                Hidden_layer_result  = self.multiply_by_hidden(Reshape_result)

                Second_RELU_output =  Hidden_layer_result.clip(0)

                Output_layer_output = self.multiply_by_output(Second_RELU_output)

                classification = self.soft_max(Output_layer_output)

                # print ( np.argmax(classification) ,"::::::",image[0])
                expected = [0] * 10
                expected[int(image[0])] = 1
                self.back_propagation(classification, expected, Second_RELU_output, Reshape_result, image_count) 

                if (np.argmax(classification) == image[0]):
                    correct_count += 1
                if (image_count % 100 == 0):
                    i+=1
                    ratio = correct_count/100
                    print ("Batch",i,"with ratio: ",ratio )
                    # print("\nIt has processed 100 images\nThere are %i left" % (len(self.filtered_data) - image_count))
                    if (ratio > self.best_ratio):
                        self.best_ratio = ratio
                    if (ratio > self.epoch_best_ratio ):
                        self.epoch_best_ratio = ratio

                    correct_count = 0
            np.savetxt('filtereddata.csv' , self.filteredTrain, delimiter=',', newline='\n',fmt='%g')
            self.ran_one_epoch = True
        else:
            print("Beginning training from data from filtereddata.csv")
            np.random.shuffle(self.filtered_data)

            for image in self.filtered_data:
                image_count += 1
                data = image[1:]
                data.reshape(1,2000)
                Reshape_result = data.reshape(1,2000)              
            
                Hidden_layer_result  = self.multiply_by_hidden(Reshape_result)

                Second_RELU_output =  Hidden_layer_result.clip(0)

                Output_layer_output = self.multiply_by_output(Second_RELU_output)

                classification = self.soft_max(Output_layer_output)

                # print ( np.argmax(classification) ,"::::::",int (image[0]))
                expected = [0] * 10
                expected[int(image[0])] = 1

                self.back_propagation(classification, expected, Second_RELU_output, Reshape_result, image_count) 

                if (np.argmax(classification) == image[0]):
                    correct_count += 1
                if (image_count % 100 == 0):
                    i+=1
                    ratio = correct_count/100
                    print ("Batch",i,"with ratio: ",ratio )
                    # print("\nIt has processed 100 images\nThere are %i left" % (len(self.filtered_data) - image_count))
                    if (ratio > self.epoch_best_ratio ):
                        self.epoch_best_ratio = ratio

                    if (ratio > self.best_ratio):
                        self.best_ratio = ratio

                    correct_count = 0

    




    def test(self):
        # Do the test operations
        image = self.TEST[0]

        convo_result = np.zeros([20,20,20])

        self.convo(image, convo_result)

        RELU_result = convo_result.clip(0) # first RELU

        Pool_result = self.pool(RELU_result)

        Reshape_result = self.reshape(Pool_result)

        Hidden_layer_result  = self.multiply_by_hidden(Reshape_result)

        Second_RELU_output =  Hidden_layer_result.clip(0)

        Output_layer_output = self.multiply_by_output(Second_RELU_output)

        classification = self.soft_max(Output_layer_output)


        if (np.argmax(classification) == image[0]):
            print( "The image was classified correctly. It was",image[0] )
        else:
            print( "The image was NOT classified correctly. It was",image[0] ,"but the result was",np.argmax(classification) )
            
        


    def epochs(self):              
        N = input("How many epochs should be run (must be a number): ")
        for x in range(int(N)):
            self.train() 
            print ("EPOCH",x+1,"with best success ratio: ", self.epoch_best_ratio)
            self.epoch_best_ratio = 0
        self.final_results()
      
        while(True):
            self.TESTfile_name = input("Enter the file name containing test image (0 to EXIT): ")
            if (self.TESTfile_name == '0'):
                print (" THANK YOU. Good Bye!!")
                break
            self.TEST = self.open_images(str(self.TESTfile_name) + ".csv")
            self.test()
        
    def final_results(self):
        print("The best  success ratio : " , self.best_ratio)
        


if __name__=='__main__':
    cnn = CNN()
    cnn.setup()
    cnn.epochs()
