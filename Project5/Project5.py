import numpy as np
import copy, random, os, pandas as pd
import matplotlib.pyplot as plt
import warnings
import time

class CNN:
    def __init__(self):
        self.filters = np.zeros([20,9,9]) # THESE NEVER CHANGE DURING THE BACK PROPAGATION
        self.TEST = []      # Contains the test images
        self.TRAIN = []     # Contains the training images
        self.W5_weights = [] # This one should have 2000*100 weights
        self.W0_weights = [] # This should be the 100 * 10
        self.learning_rate = .000001
        self.nhidden = 100
        self.labels = []
        self.derived_values_hidden = np.zeros([1, self.nhidden ], dtype =float)
        self.derived_values_output = np.zeros([1,10], dtype = float)
        self.best_W0_weights = []
        self.best_W5_weights = []
        self.best_correct_count = 0
        self.filteredTrain = np.empty([10000,2000])



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

        # Set up the images 
        self.TRAIN, self.TEST = self.extract_images()
  
        # Give random values to the weights
        num_in, num_out = 2000 , 10 
        self.W5_weights = (np.random.rand( num_in,self.nhidden)-0.5)*2/np.sqrt(num_in )
        self.W0_weights = (np.random.rand(self.nhidden, num_out)-0.5)*2/np.sqrt(self.nhidden)

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
        #randomize = [0]
        # randomize = [7, 9]
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

        random.shuffle(total_test_images)
    

        return total_images, total_test_images

    
    def convo(self, image, output):
        # Apply the filter to the all the pixels of the image
        image = image[1:]
        np.array(image)
        image = image.reshape([28, 28])
        # loop over the input image, "sliding" the kernel across
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
        e_x = np.exp(matrix - np.max(matrix))
        return (e_x)/ (e_x.sum())
    
    #     back_propagation(classification, expected, Second_RELU_output, Reshape_result, image_count) 
    def back_propagation(self, classifications, expected, output_of_hidden, output_of_reshape, image_count):
        # Begin the back propagation, only W5 AND W0 change, not the filters
        self.derivatives_of_output(classifications, expected, output_of_hidden)
        self.derivatives_of_hidden(output_of_hidden, output_of_reshape)
        if (image_count % 100 == 0):
            self.update_output_weights()
            self.update_hidden_weights()
            self.derived_values_hidden = np.zeros([1, self.nhidden ], dtype =float)
            self.derived_values_output = np.zeros([1,10], dtype = float)

    def derivatives_of_output(self, classifications, expected, output_of_hidden):
        for i in range(len(classifications)):
            y = classifications[0][i]
            t = expected[i]
            for j in range (len(output_of_hidden[0])):
                self.derived_values_output[0][i] += ( (y - t))  * output_of_hidden[0][j]  # dWo = dWo + y5' * delta
        

    def derivatives_of_hidden(self, output_of_hidden , output_of_reshape):
        delta = np.array(self.derived_values_output)
        w0_ = np.transpose(np.array(self.W0_weights))
        e5 = np.dot(delta, w0_)
        delta5 = e5.clip(0)  #delta5 = RELU(e5)
        temp = np.dot (np.transpose(output_of_reshape), delta5)
        dW5 = np.array(self.derived_values_hidden)
        np.add(dW5, temp)

    
    def update_output_weights(self):
        # This updates the weights for the output layer
        for x in range(len(self.W0_weights)):
            for y in range(len(self.W0_weights[x])):
                self.derived_values_output[0][y] = (self.derived_values_output[0][y])/ 100 
                self.W0_weights[x][y] += (self.learning_rate * self.derived_values_output[0][y])
    
    def update_hidden_weights(self):
        # This updates the weights for the hidden layer
        for x in range(len(self.W5_weights)):
            for y in range(len(self.W5_weights[x])):
                self.derived_values_hidden[0][y] = (self.derived_values_hidden[0][y])/100
                self.W5_weights[x][y] += self.W5_weights[x][y] + self.learning_rate


    def train(self):
        # Do the training operations
        image_count = 0
        correct_count = 0
                
        convo_result = np.zeros([20,20,20])

        i = 0
        for image in self.TRAIN:
            image_count += 1
            # print(image_count)
            start_time = time.time()

            self.convo(image, convo_result)

            RELU_result = convo_result.clip(0) # first RELU

            Pool_result = self.pool(RELU_result)

            Reshape_result = self.reshape(Pool_result)

            time_taken = time.time() - start_time

            # print ("TIME FOR FILTERING 1 IMAGE: ", time_taken)
            
            # Reshape_result.reshape(2000)
            # self.filteredTrain[image_count -1] = Reshape_result
            # if (image_count % 100 == 0):
            #     print ("Done filtering 100 images")
        
        # np.savetxt('filtereddata.csv' , self.filteredTrain, delimiter=',', newline='\n',fmt='%g')


            Hidden_layer_result  = self.multiply_by_hidden(Reshape_result)

            Second_RELU_output =  Hidden_layer_result.clip(0)

            Output_layer_output = self.multiply_by_output(Second_RELU_output)

            classification = self.soft_max(Output_layer_output)

            # print ( np.argmax(classification) ,"::::::",image[0])
            expected = [0] * 10
            expected[image[0]] = 1
            classification = classification.tolist()
            self.back_propagation(classification, expected, Second_RELU_output, Reshape_result, image_count) 

            if (np.argmax(classification) == image[0]):
                correct_count += 1
            if (image_count % 100 == 0):
                i+=1
                print ("Batch",i,"with ratio: ", correct_count/100)
                correct_count = 0
                print("\nIt has processed 100 images\nThere are %i left" % (len(self.TRAIN) - image_count))

    def test(self):
        # Do the test operations

        convo_result = np.zeros([20,20,20])

        correct_count = 0
        image_count = 0

        # self.TEST = self.TEST[0:10]
        i = 0
        for image in self.TEST:
            image_count += 1

            self.convo(image, convo_result)

            RELU_result = convo_result.clip(0) # first RELU

            Pool_result = self.pool(RELU_result)

            Reshape_result = self.reshape(Pool_result)

            # time_taken = time.time() - start_time

            Hidden_layer_result  = self.multiply_by_hidden(Reshape_result)

            Second_RELU_output =  Hidden_layer_result.clip(0)

            Output_layer_output = self.multiply_by_output(Second_RELU_output)

            classification = self.soft_max(Output_layer_output)

            self.convo(image, convo_result)

            RELU_result = convo_result.clip(0) # first RELU

            Pool_result = self.pool(RELU_result)

            Reshape_result = self.reshape(Pool_result)

            Hidden_layer_result  = self.multiply_by_hidden(Reshape_result)

            Second_RELU_output =  Hidden_layer_result.clip(0)

            Output_layer_output = self.multiply_by_output(Second_RELU_output)

            classification = self.soft_max(Output_layer_output)

            # print ( np.argmax(classification) ,"::::::",image[0])
            if (np.argmax(classification) == image[0]):
                correct_count += 1
            
            if (image_count % 100 == 0):
                i+=1
                print ("Batch",i,"with ratio: ", correct_count/100)
                correct_count = 0
                print("It has processes 100 images\nThere are %i left" % (len(self.TEST) - image_count))

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