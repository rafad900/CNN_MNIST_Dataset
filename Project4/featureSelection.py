import csv

def featureExtraction(inputImage): 
    print("Doing the feature extration")
    file = open(inputImage, 'r')
    spamreader = csv.reader(file, delimiter=' ', quotechar='|')
    for row in spamreader:
        print(', '.join(row[:-10]))

    #xpos, ypos = 0, 0
    # We want to read the values of the file 28 pixels at a time. 
    # the images are 28 by 28. 
    '''while (xpos < inputImage):
        print("this here")'''

if __name__=='__main__':
    file_path = raw_input("Here is the feature extraction, feed me a file:   ")
    featureExtraction(file_path)



