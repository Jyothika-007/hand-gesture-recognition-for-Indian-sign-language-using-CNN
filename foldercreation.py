# Importing the Libraries Required

import os
import string
from string import ascii_uppercase, digits

# Creating the directory Structure

if not os.path.exists("dataSet"):
    os.makedirs("dataSet")

if not os.path.exists("dataSet/static/trainingData"):
    os.makedirs("dataSet/static/trainingData")

if not os.path.exists("dataSet/static/testingData"):
    os.makedirs("dataSet/static/testingData")

# Making folder  0 (i.e blank) in the training and testing data folders respectively
for i in range(0):
    if not os.path.exists("dataSet/static/trainingData/" + str(i)):
        os.makedirs("dataSet/static/trainingData/" + str(i))

    if not os.path.exists("dataSet/static/testingData/" + str(i)):
        os.makedirs("dataSet/static/testingData/" + str(i))

# Making Folders from A to Z in the training and testing data folders respectively

for i in string.ascii_uppercase+digits:
    if not os.path.exists("dataSet/static/trainingData/" + i):
        os.makedirs("dataSet/static/trainingData/" + i)
    
    if not os.path.exists("dataSet/static/testingData/" + i):
        os.makedirs("dataSet/static/testingData/" + i)

