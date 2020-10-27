import math
import operator

#open the data files
trainFile = open("u1-base.base", "r")
testFile = open("u1-test.test", "r")

#read the raw data
lines1 = trainFile.readlines()
lines2 = testFile.readlines()

#store the raw data into lists
trainDataRaw = []
testDataRaw = []
for line in lines1:
    line = line.split()
    trainDataRaw.append(line)
    
for line in lines2:
    line = line.split()
    testDataRaw.append(line)

#get the dimensions for the full training matrix
maxTrainMovieID = 0
maxTrainUserID = 0
for i in range(len(trainDataRaw)):
    if int(trainDataRaw[i][1]) > int(maxTrainMovieID):
        maxTrainMovieID = trainDataRaw[i][1]
    if int(trainDataRaw[i][0]) > int(maxTrainUserID):
        maxTrainUserID = trainDataRaw[i][0]
        
#get the dimensions of the full testing matrix
maxTestMovieID = 0
maxTestUserID = 0
for i in range(len(testDataRaw)):
    if int(testDataRaw[i][1]) > int(maxTestMovieID):
        maxTestMovieID = testDataRaw[i][1]
    if int(testDataRaw[i][0]) > int(maxTestUserID):
        maxTestUserID = testDataRaw[i][0]
        
#determine the maximum user ID and maximum movie ID
maxMovieID = 0
maxUserID = 0
if maxTestMovieID > maxTrainMovieID:
    maxMovieID = maxTestMovieID
else:
    maxMovieID = maxTrainMovieID
if maxTestUserID > maxTrainUserID:
    maxUserID = maxTestUserID
else:
    maxUserID = maxTrainUserID
        
        
#create the base matrices for testing and training data without values
trainData = list(range(int(maxUserID) + 1))
testData = list(range(int(maxUserID) + 1))
for i in range(len(trainData)):
    trainData[i] = list(range(int(maxMovieID) + 1))
for i in range(len(testData)):
    testData[i] = list(range(int(maxMovieID) + 1))
    
#make all values of the matrices for testing and training -1 for comparison purposes
for i in range(len(trainData)):
    for j in range(len(trainData[i])):
        trainData[i][j] = -1
for i in range(len(testData)):
    for j in range(len(testData[i])):
        testData[i][j] = -1

#populate the matrices for testing and trainging with their data from the input files
for i in range(len(trainDataRaw)):
    rowIndex = int(trainDataRaw[i][0])
    colIndex = int(trainDataRaw[i][1])
    movieRating = int(trainDataRaw[i][2])
    trainData[rowIndex][colIndex] = movieRating

for i in range(len(testDataRaw)):
    rowIndex = int(testDataRaw[i][0])
    colIndex = int(testDataRaw[i][1])
    movieRating = int(testDataRaw[i][2])
    testData[rowIndex][colIndex] = movieRating

#is passes 2 individual rows from the entire data sets, calculates their euclidean distance
def calcEuclidDist(person1, person2):
    dist = 0
    for i in range(1, len(person1)):
        dist = pow((person1[i] - person2[i]), 2)
    dist = math.sqrt(dist)
    return dist

#finds the nearest k neightbors to a given test point
def getNearestK(trainData, testPoint, k):
    distances = []
    for i in range(0, len(trainData)):
        dist = calcEuclidDist(trainData[i], testPoint)
        distances.append((trainData[i], dist))
    distances.sort(key = operator.itemgetter(1))
    kNearest = []
    for i in range(0,k):
        kNearest.append(distances[i][0])
    return kNearest

#makes predictions for a given user given its neighbors. bases predictions on average of neighbor ratings
def makePredictions(kNearest):
    predictions = []
    for j in range(len(kNearest[0])):#for each movie rating
        neighborRatings = []
        for i in range(len(kNearest)):#for each user
            if int(kNearest[i][j]) == -1:
                neighborRatings.append(2.5)
            else:
                neighborRatings.append(kNearest[i][j])
            totalRatings = 0
            for i in range(len(neighborRatings)):
                totalRatings = totalRatings + neighborRatings[i]
            averageRating = totalRatings / len(neighborRatings)
        predictions.append(averageRating)
    return predictions

#calculaes the mean squared error for a set given the matrix of its predictions
def calcMeanSquaredError(dataSet, predictions):
    numPoints = 0
    summation = 0
    for i in range(len(dataSet)):
        for j in range(len(dataSet[i])):
            if dataSet[i][j] != -1:
                numPoints = numPoints + 1
                summation = summation + math.pow((dataSet[i][j] - predictions[i][j]), 2)
    mse = summation / numPoints
    return mse

k = 3

#find the nearest neighbors and make predictions
testPredictions = []
for i in range(len(testData)):
    kNearest = getNearestK(trainData, testData[i], k)
    testPredictions.append(makePredictions(kNearest))

#find and print the mse
testMSE = calcMeanSquaredError(testData, testPredictions)

print("Testing Mean Squared Error: " + str(testMSE))



    