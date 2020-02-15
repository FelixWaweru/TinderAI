import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Importing the dataset
dataset = pd.read_csv('Churn_Modelling.csv')

# Data in Column 3 to 12 are Independent Variables and thus wil be needed
# Column are counted from 0 and we select from Column 3 to row 12(+1)
X = dataset.iloc[:, 3:13].values

# The Column with results used to train the model (Column 13)
y = dataset.iloc[:, 13].values


# Encoding the Independent Variables(Assigning int values to text data in columns)
# Encoder for the countries column(Columns counted from 0)
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
labelencoder_X1 = LabelEncoder()
X[:, 1] = labelencoder_X1.fit_transform(X[:, 1])

# Encoder for the Gender column(Columns counted from 0)
labelencoder_X2 = LabelEncoder()
X[:, 2] = labelencoder_X2.fit_transform(X[:, 2])

# Creates Dummy variables for the country column
onehotencoder = OneHotEncoder(categorical_features = [1])
X = onehotencoder.fit_transform(X).toarray()
# We drop column 0 by making X have column 1 to the last one(Prevent Dummy variable trap)
X =X[:, 1:]


# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

# Feature Scaling
# Feature scaling is used to convert variables to a uniform standard to prevent bias
# Eg. The model might assume 3000km is larger than and 5Km before feature scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# Import Keras and the modules we will use in the ANN
import keras
from keras.models import Sequential
from keras.layers import Dense

# Fitting classifier to the Training set
# Create your classifier here
classifier = Sequential()

# This is where we define and add the output and input layer

# The number of output_dim is roughly (input layers + 1) /2
# First Hidden layer i.e first neuron
classifier.add(Dense(output_dim = 6, init = 'uniform', activation = 'relu', input_dim = 11))

# Second hidden layer i.e second neuron
classifier.add(Dense(output_dim = 6, init = 'uniform', activation = 'relu'))

# Output layer
# This layer will have only one output_dim since the output will be one value
# We use the sigmoid function so that we can get the range of values that will
# be used to show the probability that a customer will leave the bank
classifier.add(Dense(output_dim = 1, init = 'uniform', activation = 'sigmoid'))

# Compiling the ANN
classifier.compile(optimizer = 'adam',loss = 'binary_crossentropy', metrics = ['accuracy'])

#Fitting the ANN to the training set
classifier.fit(X_train, y_train, batch_size = 10, epochs = 100)

# Predicting the Test set results
y_pred = classifier.predict(X_test)
# We convert the data into true false statements
y_pred = (y_pred>0.5)

# Single customer Homework prediction
homework_prediction = classifier.predict(np.array())

# Making the Confusion Matrix
# Used to check the accuracy out the ANN predictions
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)

# Calculating the percentage accuracy of the model using data from the confusion matrix
correct_train_data = cm[0][0]
correct_test_data = cm[1][1]
accuracy = ((correct_train_data + correct_test_data)/2000)*100
print("The system is " + str(accuracy) + "% accurate.")