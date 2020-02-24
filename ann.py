import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Importing the dataset
dataset = pd.read_csv('swipe_data.csv')

# Data in Column 3 to 8 are Independent Variables and thus wil be needed
# Column are counted from 0 and we select from Column 3 to row 8(+1)
X = dataset.iloc[:, 3:9].values

# The Column with results used to train the model (Column 13)
y = dataset.iloc[:, 9].values



# Encoding the Independent Variables(Assigning int values to text data in columns)
# Encoder for the Job column(Columns counted from 0)
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
labelencoder_X1 = LabelEncoder()
X[:, 4] = labelencoder_X1.fit_transform(X[:, 4])

# Encoder for the School column(Columns counted from 0)
labelencoder_X2 = LabelEncoder()
X[:, 5] = labelencoder_X2.fit_transform(X[:, 5])


# Encoder for the Swipe column(Columns counted from 0)
labelencoder_y1 = LabelEncoder()
y = labelencoder_y1.fit_transform(y)

onehotencoder = OneHotEncoder(categorical_features = [5])
X = onehotencoder.fit_transform(X).toarray()
X =X[:, 1:]


# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

# Feature Scaling
# Feature scaling is used to convert variables to a uniform standard to prevent bias
# Eg. The model might assume 3000km is larger than and 5Km before feature scaling
# from sklearn.preprocessing import StandardScaler
# sc = StandardScaler()
# X_train = sc.fit_transform(X_train)
# X_test = sc.transform(X_test)

# Import Keras and the modules we will use in the ANN
import keras
from keras.models import Sequential
from keras.layers import Dense

# Fitting classifier to the Training set
# Create your classifier here
classifier = Sequential()

# This is where we define and add the output and input layer
# The output_dim is the number of nodes in the layer
# The number of output_dim is roughly (input layers + 1) /2
# init is used to initialize the weights
# activation is the activation function used in the neuron
# First Hidden layer i.e first neuron
classifier.add(Dense(output_dim = 3, init = 'uniform', activation = 'relu', input_dim = 6))

# Output layer
# This layer will have only one output_dim since the output will be one value
# We use the sigmoid function so that we can get the range of values that will
# be used to show the probability that a customer will leave the bank
classifier.add(Dense(output_dim = 1, init = 'uniform', activation = 'sigmoid'))

# Compiling the ANN
# Initializes Stochastic Gradient Descent
classifier.compile(optimizer = 'adam',loss = 'binary_crossentropy', metrics = ['accuracy'])

#Fitting the ANN to the training set
# The batch size is the number of turns after which to adjust the weights
# After the weights have been adjusted for every row of data, that is called an epoch
classifier.fit(X_train, y_train, batch_size = 10, epochs = 2000)

classifier.save('TinderAIModel.h5')

# Predicting the Test set results
y_pred = classifier.predict(X_test)
# We convert the data into true false statements
y_pred = (y_pred>0.5)

# Making the Confusion Matrix
# Used to check the accuracy out the ANN predictions
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)

# Calculating the percentage accuracy of the model using data from the confusion matrix
correct_train_data = cm[0][0]
correct_test_data = cm[1][1]
accuracy = ((correct_train_data + correct_test_data)/40)*100
print("The system is " + str(accuracy) + "% accurate.")

# Plots a line graph showing correlations within the data
sns.set_style("darkgrid")
plt.xlabel("Age")
plt.ylabel("Swipe Probability")
# Sets the Range of ages in the graph between 18 and 30
plt.xlim(18, 30)
# Sets the Range of Swipe in the graph between 0.0 and 1.0
plt.ylim(0.0, 1.0)
sns.lineplot(X[:, 1], y, color='orange')