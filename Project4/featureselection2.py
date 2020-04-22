import numpy as np
import pandas as pd
import random
import os
from numpy import array
# Turns the image into black and white
def getBlWhImage(image):
    pixels = []
    for x in range(28):
        for y in range(28):
            if (int(image[x][y]) > 128):
                pixels.append(1)
            else:
                pixels.append(0)
    return np.reshape(pixels, (28, 28))

# Gets the number of intersections in black and white image
def verticalIntersections(image):
    counts = []
    prev = 0
    for y in range(28):
        count = 0
        for x in range(28):
            current = int(image[x][y])
            if (prev != current):
                count += 1
            prev = current
        counts.append(count) 
    average = sum(counts)/28
    maximum = max(counts)
    return average, maximum

# Horizontal intersctions in black white image 
def horizontalIntersection(image):
    counts = []
    prev = 0
    for x in range(28):
        count = 0
        for y in range(28):
            current = int(image[x][y])
            if (prev != current):
                count += 1
            prev = current
        counts.append(count) 
    average = sum(counts)/28
    maximum = max(counts)
    return average, maximum

# Calculates the symmetry in image
def calculateSymmetry(image):
    count = 0
    for x in range(28):
        for y in range(28):
            count = count + (int(image[x][y]) ^ int(image[27-x][y])) # This is xor
    return count/(28*28) 

# calculates the density
def calculateDensity(image):
    count = 0
    for x in range(28):
        for y in range(28):
            count = count + int(image[x][y])
    return count/(28*28)

# calls the feature extraction functions and returns values as list
def featureExtraction(image): 
    density = calculateDensity(image)
    symmetry = calculateSymmetry(image)
    black_white = getBlWhImage(image)
    verticalAvg, verticalMax = verticalIntersections(black_white)
    horizontalAvg, horizontalMax = horizontalIntersection(black_white)
    return [density, symmetry, verticalAvg, verticalMax, horizontalAvg, horizontalMax]

# Opens the csv files and extract the images from them and returns them 
def open_images(path):
    print("Opening and extracting images")
    images = []
    data = pd.read_csv(path)
    headers = data.columns.values

    labels = data[headers[0]]
    labels = labels.values.tolist()
    
    pixels = data.drop(headers[0], axis=1)

    for i in range(0, data.shape[0]):              
        row = pixels.iloc[i].to_numpy()
        grid = np.reshape(row, (28, 28))
        images.append(grid)
    return labels, images

# Main driver of all the code
def main():
    # images_7_path = input("Path to the images of 7:  ")
    # images_9_path = input("Path to the images of 9:  ")
    # images_TEST_path = input("Path to the test images of 7 and 9: ")

    randomize = [1,2,3,4,5,6,7,8,9]
    random.shuffle(randomize)
    total_labels = []
    total_images = []
    total_test_images = []
    total_test_labels = []
    for x in randomize:
        labels, images = open_images("Project4_Data_set/train" + str(x) + ".csv")
        test_l, test_i = open_images("Project4_Data_set/valid" + str(x) + ".csv")
        total_images += images
        total_labels += labels  
        total_test_images += test_i
        total_test_labels += test_l

    if (not os.path.exists("image_features_TRAIN.txt")):
        feature_file_TRAIN = open('image_features_TRAIN.txt', 'w')
        print("Doing feature extraction on training images")
        i = 0
        for image in total_images:
            features = featureExtraction(image)
            feature_file_TRAIN.write("-1, ")
            for f in features:
                feature_file_TRAIN.write("%s, " % str(f))
            label = total_labels[i]
            if (label == 0):
                feature_file_TRAIN.write("0\n")
            elif (label == 1):
                feature_file_TRAIN.write("1\n")
            elif (label == 2):
                feature_file_TRAIN.write("2\n")
            elif (label == 3):
                feature_file_TRAIN.write("3\n")
            elif (label == 4):
                feature_file_TRAIN.write("4\n")
            elif (label == 5):
                feature_file_TRAIN.write("5\n")
            elif (label == 6):
                feature_file_TRAIN.write("6\n")
            elif (label == 7):
                feature_file_TRAIN.write("7\n")
            elif (label == 8):
                feature_file_TRAIN.write("8\n")
            elif (label == 9):
                feature_file_TRAIN.write("9\n")
            i += 1   
        feature_file_TRAIN.close()

    if (not os.path.exists("image_features_TEST.txt")):
        print("Doing feature extraction on test images")
        feature_file_TEST = open('image_features_TEST.txt', 'w')
        i = 0
        for image in total_test_images:
            features = featureExtraction(image)
            feature_file_TEST.write("-1, ")
            for f in features:
                feature_file_TEST.write("%s, " % str(f))
            label = total_test_labels[i]
            if (label == 0):
                feature_file_TEST.write("0\n")
            elif (label == 1):
                feature_file_TEST.write("1\n")
            elif (label == 2):
                feature_file_TEST.write("2\n")
            elif (label == 3):
                feature_file_TEST.write("3\n")
            elif (label == 4):
                feature_file_TEST.write("4\n")
            elif (label == 5):
                feature_file_TEST.write("5\n")
            elif (label == 6):
                feature_file_TEST.write("6\n")
            elif (label == 7):
                feature_file_TEST.write("7\n")
            elif (label == 8):
                feature_file_TEST.write("8\n")
            elif (label == 9):
                feature_file_TEST.write("9\n")
            i += 1  
        feature_file_TEST.close()
        
    return total_test_labels

# Caller if invoked directly
if __name__=='__main__':
    print("\n\nFeatureSelection.py will extract features from the images and save them to a file called \"seven and nine features\" in this folder")
    print("Each row of the folder will contain the density, symmetry, vertical average and max, horizontal average and max and their label in that order")
    print("There are 1998 rows, first half are images of number 7 and other half are 9\n")
    main()