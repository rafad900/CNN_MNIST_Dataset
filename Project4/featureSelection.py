import numpy as np
import pandas as pd

def verticalIntersections(image):
    # go through column and changes and get the max 

def horizontalIntersection(image):
    # same thing as vertical but for row

def calculateSymmetry(image):
    count = 0
    for x in range(19):
        for y in range(19):
            count = count + (image[x][y] != images[28-x][y]) # This is xor
    return count 

def calculateDensity(image):
    count = 0
    for x in range(28):
        for y in range(28):
            count = count + image[x][y]
    return count/255

def featureExtraction(data): 
    print("Doing the feature extration")
    # Pull out the data from the two sets and run them through the feature extractors


def open_images(path_7, path_9):
    print("Opening and extracting images")
    images_7 = []
    images_9 = []
    data_7 = pd.read_csv(path_7)
    data_9 = pd.read_csv(path_9)
    headers_7 = data_7.columns.values
    headers_9 = data_7.columns.values
    
    pixels_7 = data_7.drop(headers_7[0], axis=1)
    pixels_9 = data_9.drop(headers_9[0], axis=1)

    for i in range(0, 999):
        row_7 = pixels_7.iloc[i].to_numpy()
        row_9 = pixels_9.iloc[i].to_numpy()
        grid_7 = np.reshape(row_7, (28, 28))
        grid_9 = np.reshape(row_9, (28, 28))
        data_7.append(grid_7)
        data_9.append(grid_9)
    return data_7, data_9

def main():
    images_7_path = input("Path to the images of 7:  ")
    images_9_path = input("Path to the images of 9:  ")

    images_7, images_9 = open_images(images_7_path, images_9_path)


if __name__=='__main__':
    file_path = raw_input("Here is the feature extraction, feed me a file:   ")
    featureExtraction(file_path)



