import numpy as np
import pandas as pd

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
    for x in range(19):
        for y in range(19):
            count = count + (int(image[x][y]) != int(image[27-x][y])) # This is xor
    return count 

# calculates the density
def calculateDensity(image):
    count = 0
    for x in range(28):
        for y in range(28):
            count = count + int(image[x][y])
    return count/255

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
    
    pixels = data.drop(headers[0], axis=1)

    for i in range(0, data.shape[0]):              
        row = pixels.iloc[i].to_numpy()
        grid = np.reshape(row, (28, 28))
        images.append(grid)
    return labels, images

# Main driver of all the code
def main():
    images_7_path = input("Path to the images of 7:  ")
    images_9_path = input("Path to the images of 9:  ")
    images_TEST_path = input("Path to the test images of 7 and 9: ")

    labels_7, images_7 = open_images(images_7_path)
    labels_9, images_9 = open_images(images_9_path)
    labels_T, images_TEST = open_images(images_TEST_path)

    feature_file_TRAIN = open('seven_and_nine_features_TRAIN.txt', 'w')
    feature_file_TEST = open('seven_and_nine_features_TEST.txt', 'w')

    print("Doing feature extraction")
    for image in images_7:
        #print(image)     DEBUGGING PURPOSES
        features = featureExtraction(image)
        for f in features:
            feature_file_TRAIN.write("%s, " % str(f))
        feature_file_TRAIN.write("0\n")

    for image in images_9:
        #print(image)       DEBUGGING PURPOSES
        features = featureExtraction(image)
        for f in features:
            feature_file_TRAIN.write("%s, " % str(f))
        feature_file_TRAIN.write("1\n")

    for image in images_TEST:
        features = featureExtraction(image)
        i = 0
        for f in features:
            feature_file_TEST.write("%s, " % str(f))
        if (labels_T[i] == '7'):
            feature_file_TEST.write("0\n")
        else: 
            feature_file_TEST.write("1\n")
        i += 1
    
    feature_file_TRAIN.close()
    feature_file_TEST.close()

# Caller if invoked directly
if __name__=='__main__':
    print("\n\nFeatureSelection.py will extract features from the images and save them to a file called \"seven and nine features\" in this folder")
    print("Each row of the folder will contain the density, symmetry, vertical average and max, horizontal average and max and their label in that order")
    print("There are 1998 rows, first half are images of number 7 and other half are 9\n")
    main()


