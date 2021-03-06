# -*- coding: utf-8 -*-
"""PCA.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1It7iEDWNRIjmFb6dcnuY8zoqks6Kmpu2
"""

# Dependencies.
import numpy as np
from PIL import Image
from google.colab import drive
from collections import defaultdict

"""# **<center>1. Download the dataset and understand the format.</center>**"""

# Mount the Google drive into the runtime.
drive.mount('/content/gdrive')

"""# **<center>2. Generate the data matrix D and the labels vector y.</center>**"""

# Commented out IPython magic to ensure Python compatibility.
from sklearn.datasets import load_boston
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
# %matplotlib inline
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import RFE
from sklearn.linear_model import RidgeCV, LassoCV, Ridge, Lasso
from mpl_toolkits.mplot3d import Axes3D
import plotly
import plotly.graph_objs as go
from plotly.offline import *
from sklearn import datasets, linear_model
from sklearn.model_selection import train_test_split

# Store all images as vectors.
dataset_train = []

# The ORL dataset has 40 subjects each having 10 images.
for i in range(1, 41):
  for j in range(1, 6):
  
    # Each subject has a folder containing its images.
    folder_path = '/content/gdrive/My Drive/att-database-of-faces/s' + str(i) + '/'
    
    # Convert each image into a 10304-dimensional vector.
    img = Image.open(folder_path + str(j) + '.pgm')
    vec = np.array(img).reshape(10304)
    
    dataset_train.append(vec)
    
    
# Generate the data matrix D.
D_train = np.array([example for example in dataset_train])
D_train = D_train.reshape((200, 10304))

# Generate the label vector y.
# The key point here is that we know that the data in the data matrix is 
# ordered, i.e. all the images with label 1 come before those with label 2 
# and so on.
labels_train = []

for i in range(1, 41):
  labels_train.append(i * np.ones((5, 1)))
  
y_train = np.stack(labels_train, axis=0)

# Store all images as vectors.
dataset_test = []

# The ORL dataset has 40 subjects each having 10 images.
for i in range(1, 41):
  for j in range(6, 11):
  
    # Each subject has a folder containing its images.
    folder_path = '/content/gdrive/My Drive/att-database-of-faces/s' + str(i) + '/'
    
    # Convert each image into a 10304-dimensional vector.
    img = Image.open(folder_path + str(j) + '.pgm')
    vec = np.array(img).reshape(10304)
    
    dataset_test.append(vec)
    
    
# Generate the data matrix D.
D_test = np.array([example for example in dataset_test])
D_test = D_test.reshape((200, 10304))

# Generate the label vector y.
# The key point here is that we know that the data in the data matrix is 
# ordered, i.e. all the images with label 1 come before those with label 2 
# and so on.
labels_test = []

for i in range(1, 41):
  labels_test.append(i * np.ones((5, 1)))
  
y_test = np.stack(labels_test, axis=0)

"""# **<center>3. Split the dataset into training and test sets.</center>**"""





y_test=y_test.transpose(2,0,1).reshape(1,-1)

y_train=y_train.transpose(2,0,1).reshape(1,-1)

pd.DataFrame(y_train)

pd.DataFrame(y_test)

X_train=D_train
X_test=D_test

y_test=y_test.transpose()
y_train=y_train.transpose()

print (X_train.shape)
print (X_test.shape)
print (y_train.shape)
print (y_test.shape)

from sklearn.preprocessing import StandardScaler # x_std hwa el data xtrain 
X_std = X_train
X_test=X_test

pd.DataFrame(X_std)

mean_vec = np.mean(X_std, axis=0)
cov_mat = (X_std - mean_vec).T.dot((X_std - mean_vec)) / (X_std.shape[0]-1)

cov_mat = np.cov(X_std.T)

eig_vals, eig_vecs = np.linalg.eig(cov_mat)

print('Eigenvectors \n%s' %eig_vecs)
print('\nEigenvalues \n%s' %eig_vals)

eig_vals, eig_vecs = np.linalg.eigh(cov_mat)

pd.DataFrame(eig_vals)

pd.DataFrame(eig_vecs)

for ev in eig_vecs:
    np.testing.assert_array_almost_equal(1.0, np.linalg.norm(ev))
print('Everything ok!')



# Make a list of (eigenvalue, eigenvector) tuples
eig_pairs = [(np.abs(eig_vals[i]), eig_vecs[:,i]) for i in range(len(eig_vals))]

# Sort the (eigenvalue, eigenvector) tuples from high to low
eig_pairs.sort(key=lambda x:x[0],reverse=True)

# Visually confirm that the list is correctly sorted by decreasing eigenvalues
print('Eigenvalues in descending order:')
for i in eig_pairs:
    print(i[0])

#0.8 alpha
total = np.array(eig_vals).sum()
sum=0
for i in range(1,int(0.8*10304)): 
 sum=sum+eig_pairs[0][0]
fraction = sum / total * 100
print(fraction)

#0.85 alpha
total = np.array(eig_vals).sum()
sum=0
for i in range(1,int(0.85*10304)): 
 sum=sum+eig_pairs[0][0]
fraction = sum / total * 100
print(fraction)

#0.9 alpha
total = np.array(eig_vals).sum()
sum=0
for i in range(1,int(0.9*10304)): 
 sum=sum+eig_pairs[0][0]
fraction = sum / total * 100
print(fraction)

#0.95 alpha
total = np.array(eig_vals).sum()
sum=0
for i in range(1,int(0.95*10304)): 
 sum=sum+eig_pairs[0][0]
fraction = sum / total * 100
print(fraction)

tot = np.sum(eig_vals)
var_exp = [(i / tot)*100 for i in sorted(eig_vals, reverse=True)]
cum_var_exp = np.cumsum(var_exp)

with plt.style.context('seaborn-whitegrid'):
    plt.figure(figsize=(10, 10))

    plt.bar(range(10304), var_exp, alpha=0.5, align='center',
            label='individual explained variance')
    plt.step(range(10304), cum_var_exp, where='mid',
             label='cumulative explained variance')
    plt.ylabel('Explained variance ratio')
    plt.xlabel('Principal components')
    plt.legend(loc='best')
    plt.tight_layout()
plt.savefig('PREDI2.png', format='png', dpi=1200)
plt.show()

matrix_w= np.hstack((eig_pairs[0][1][:,np.newaxis],eig_pairs[1][1][:,np.newaxis],eig_pairs[2][1][:,np.newaxis],eig_pairs[3][1][:,np.newaxis],eig_pairs[4][1][:,np.newaxis],eig_pairs[5][1][:,np.newaxis]))

projection_train = X_std.dot(matrix_w)
projection_test = X_test.dot(matrix_w)

projection_train

"""**KNN classifier**

**evaluating KNN**
"""

from sklearn.neighbors import KNeighborsClassifier
 neigh = KNeighborsClassifier(n_neighbors=3)
 neigh.fit(projection_train, y_train) 

neigh.predict(projection_test)

"""**classifier tuning for PCA**"""



error = []

for i in range(1, 40):
    knn = KNeighborsClassifier(n_neighbors=i)
    knn.fit(projection_train, y_train)
    pred_i = knn.predict(projection_test)
    error.append((np.sum(pred_i != y_train.transpose()))/200)

error

plt.figure(figsize=(12, 6))
plt.plot(range(1, 40), error, color='red', linestyle='dashed', marker='o',
         markerfacecolor='blue', markersize=10)
plt.title('Error Rate K Value')
plt.xlabel('K Value')
plt.ylabel('Mean Error')

