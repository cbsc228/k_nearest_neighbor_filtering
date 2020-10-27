import math
import operator

#open the data files
trainFile = open("u1-base.base", "r")

#read the raw data
lines1 = trainFile.readlines()

#store the raw data into lists
trainDataRaw = []

for line in lines1:
    line = line.split()
    trainDataRaw.append(line)

#get the dimensions for the full training matrix
maxTrainMovieID = 0
maxTrainUserID = 0
for i in range(len(trainDataRaw)):
    if int(trainDataRaw[i][1]) > int(maxTrainMovieID):
        maxTrainMovieID = trainDataRaw[i][1]
    if int(trainDataRaw[i][0]) > int(maxTrainUserID):
        maxTrainUserID = trainDataRaw[i][0]
        
#create the base matrices for testing and training data without values
trainData = list(range(int(maxTrainUserID) + 1))
for i in range(len(trainData)):
    trainData[i] = list(range(int(maxTrainMovieID) + 1))
    
#make all values of the matrices for testing and training -1 for comparison purposes
for i in range(len(trainData)):
    for j in range(len(trainData[i])):
        trainData[i][j] = -1

#populate the matrices for testing and trainging with their data from the input files
for i in range(len(trainDataRaw)):
    rowIndex = int(trainDataRaw[i][0])
    colIndex = int(trainDataRaw[i][1])
    movieRating = int(trainDataRaw[i][2])
    trainData[rowIndex][colIndex] = movieRating

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
        if (trainData[i] != testPoint):#makes sure to remove the test point from the training data for leave 1 out cross val
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

#need to remove the i-th data point and test on that point
testMSEs = []
for k in range(1,6):
    testPredictions = []
    for i in range(len(trainData)):
        kNearest = getNearestK(trainData, trainData[i], k)
        testPredictions.append(makePredictions(kNearest))

    testMSE = calcMeanSquaredError(trainData, testPredictions)
    testMSEs.append(testMSE)
    print("Testing Mean Squared Error for k = " + str(k) + ": " + str(testMSE))

#an impossibly large MSE value to serve as an initial comparison to find minimum MSE
minMSE = math.pow(10,8)
optimalK = 0
#find the lowest calculated MSE
for i in range(len(testMSEs)):
    if testMSEs[i] < minMSE:
        minMSE = testMSEs[i]
        optimalK = i + 1

print("Optimal k value using Leave-One-Out Cross Validation: " + str(optimalK))
print("Optimal MSE found: " + str(minMSE))