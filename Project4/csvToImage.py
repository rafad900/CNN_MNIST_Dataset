import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('Project4_Data_set/train0.csv')
headers = data.columns.values

label = data[headers[0]]

pixels = data.drop(headers[0], axis=1)

# D_1d is a row or a column of some kind 
for i in range(0,1):
    plt.figure()
    D_1d = pixels.iloc[i].to_numpy()
    print(D_1d)
    grid_data = np.reshape(D_1d, (28, 28))
    plt.imshow(grid_data,interpolation="none",cmap="gray")
plt.show()

print("The label is: " ,label[i])