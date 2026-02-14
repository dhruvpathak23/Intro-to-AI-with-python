import csv
import random

from sklearn.svm import SVC
from sklearn.linear_model import Perceptron
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split # 1. Import this

model = Perceptron()

# Read data in from file
with open("banknotes.csv") as f:
    reader = csv.reader(f)
    next(reader)

    evidence = []
    labels = []

    # 2. Separate evidence and labels immediately
    for row in reader:
        evidence.append([float(cell) for cell in row[:4]])
        labels.append("Authentic" if row[4] == "0" else "Counterfeit")

# 3. Use train_test_split to shuffle and split the data
# test_size=0.5 means 50% for testing, 50% for training
X_training, X_testing, Y_training, Y_testing = train_test_split(
    evidence, labels, test_size=0.50
)

# Train model on training set
model.fit(X_training, Y_training)

# Make prediction on the testing set
predictions = model.predict(X_testing)

# Compute how well we performed
correct = 0
incorrect = 0
total = 0

for actual, predicted in zip(Y_testing, predictions):
    total += 1
    if actual == predicted:
        correct += 1
    else:
        incorrect += 1

# Print the results
print(f"Results for model {type(model).__name__}") 
print(f"Correct: {correct}")    
print(f"Incorrect: {incorrect}") 
print(f"Accuracy: {100 * correct / total:.2f}%")