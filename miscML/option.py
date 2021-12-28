import numpy as np
import tensorflow as tf
import scipy.stats as stats
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


'''
#combining SPY
index = 1
frames = []
while (index<=96):
    fileName = r"spy/spy"+str(index)+r".txt"
#    print(fileName)
    tempDF = pd.read_csv(fileName)
    frames.append(tempDF)
    index = index+1

spyResult = pd.concat(frames)
spyResult.to_csv('spyMerged.csv')
print("done SPY")

#combining QQQ
index = 1
frames = []
while (index<=60):
    fileName = r"qqq/qqq"+str(index)+r".txt"
#    print(fileName)
    tempDF = pd.read_csv(fileName)
    frames.append(tempDF)
    index = index+1

spyResult = pd.concat(frames)
spyResult.to_csv('qqqMerged.csv')
print("done QQQ")

#combining AAPL
index = 1
aaplframes = []
while (index<=48):
    fileName = r"apple/aapl"+str(index)+r".txt"
#    print(fileName)
    tempDF = pd.read_csv(fileName)
    aaplframes.append(tempDF)
    index = index+1

aaplResult = pd.concat(aaplframes)
spyResult.to_csv('aaplMerged.csv')
print("done aapl")

#combining VIX
index = 1
VIXframes = []
while (index<=108):
    fileName = r"vix/vix"+str(index)+r".txt"
#    print(fileName)
    tempDF = pd.read_csv(fileName)
    VIXframes.append(tempDF)
    index = index+1

vixResult = pd.concat(VIXframes)
vixResult.to_csv('vixMerged.txt')
print("done VIX")
'''

dataSet = pd.read_csv("tiny.txt")


for i in list(dataSet):
    dataSet[i].replace(' ', np.nan, inplace=True)
    dataSet[i].replace('', np.nan, inplace=True)
    #dataSet[i].replace('  ', np.nan, inplace=True)

dataSet = dataSet.dropna()
dataSet = dataSet.reset_index(drop=True)
dataSet.pop(' [QUOTE_READTIME]')
dataSet.pop(' [QUOTE_DATE]')
dataSet.pop(' [QUOTE_TIME_HOURS]')
dataSet.pop(' [EXPIRE_DATE]')
dataSet.pop(' [C_SIZE]')
dataSet.pop(' [P_SIZE]')
dataSet.pop(' [STRIKE]')
dataSet.pop('[QUOTE_UNIXTIME]')

dataSet.pop(' [EXPIRE_UNIX]')
dataSet.pop(' [STRIKE_DISTANCE]')

dataSet = dataSet.astype(float)
avgPut = (dataSet[' [P_BID]']+dataSet[' [P_ASK]'])/2
avgCall = (dataSet[' [C_BID]']+dataSet[' [C_ASK]'])/2
dataSet[' [avgCall]'] = avgCall
dataSet[' [avgPut]'] = avgPut
dataSet.pop(' [P_BID]')
dataSet.pop(' [C_BID]')
dataSet.pop(' [P_ASK]')
dataSet.pop(' [C_ASK]')


putDataSet = putDataSet = dataSet.copy()
putDataSet.reset_index(drop=True)
putDataSet.pop(' [C_DELTA]')
putDataSet.pop(' [C_GAMMA]')
putDataSet.pop(' [C_VEGA]')
putDataSet.pop(' [C_THETA]')
putDataSet.pop(' [C_RHO]')
putDataSet.pop(' [C_IV]')
putDataSet.pop(' [C_VOLUME]')
putDataSet.pop(' [C_LAST]')
putDataSet.pop(' [P_LAST]')
putDataSet.pop(' [avgCall]')

callDataSet = dataSet.copy()
callDataSet.reset_index(drop=True)
callDataSet.pop(' [P_DELTA]')
callDataSet.pop(' [P_GAMMA]')
callDataSet.pop(' [P_VEGA]')
callDataSet.pop(' [P_THETA]')
callDataSet.pop(' [P_RHO]')
callDataSet.pop(' [P_IV]')
callDataSet.pop(' [P_VOLUME]')
callDataSet.pop(' [P_LAST]')
callDataSet.pop(' [C_LAST]')
callDataSet.pop(' [avgPut]')

#above gets rid of bid/ask so it wont be in the feature. the label is the avg of bid/ask and seperates into put/call dataframes
#below seperates feature and labels
callTrain = callDataSet.sample(frac = 0.85, random_state = 0)
callTest = callDataSet.drop(callTrain.index)
putTrain = putDataSet.sample(frac = 0.85, random_state = 0)
putTest = putDataSet.drop(putTrain.index)

callTrainFeature = callTrain.copy()
callTestFeature = callTest.copy()
putTrainFeature = putTrain.copy()
putTestFeature = putTest.copy()

callTrainLabel = callTrainFeature.pop(' [avgCall]')
callTestLabel = callTestFeature.pop(' [avgCall]')
putTrainLabel = putTrainFeature.pop(' [avgPut]')
putTestLabel = putTestFeature.pop(' [avgPut]')
print("reached")





def generateModel(numReluLayers128, numReluLayers64, numSigmoid):
    model = tf.keras.models.Sequential()
    for i in range(numReluLayers128):
        model.add(tf.keras.layers.Dense(128, activation = tf.nn.relu))
    for i in range(numReluLayers64):
        model.add(tf.keras.layers.Dense(64, activation = tf.nn.relu))
    for i in range(numSigmoid):
        model.add(tf.keras.layers.Dense(64, activation = tf.nn.sigmoid))
    model.add(tf.keras.layers.Dense(units=1))
    #model.compile(optimizer='adam', loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), metrics=['accuracy'])
    model.compile(loss='mean_absolute_error', optimizer=tf.keras.optimizers.Adam(0.001))
    
    return model

def trainModelAndUse(model, trainX, trainY, testX, testY, epoch, batchSize):
    trainX = tf.keras.utils.normalize(trainX, axis=1)#normalises features
    #history = model.fit(trainX, trainY, validation_split = .15, verbose=True, epochs=epoch, batch_size=batchSize)
    history = model.fit(trainX, trainY, validation_split = .15, verbose=True, epochs=epoch)
    predictions = model.predict(testX).flatten()
    print("size: "+str(len(predictions)))
    size = len(predictions)
    error = ((predictions - testY)**2)/size
    plt.hist(error, bins=25)
    plt.xlabel("error")
    _ = plt.ylabel('Count')
    plt.show()
    model.save("optionV2NeuralNet")
    rawError = predictions-testY
    plt.hist(rawError, bins=25)
    plt.xlabel("raw error")
    _ = plt.ylabel('Count')
    plt.show()
    print("average rawError "+str(np.average(rawError)/size))
    print("median rawError: "+str(np.median(rawError)))
    print("stdv rawError "+str(np.var(rawError)))


basicNN = generateModel(4,4,10)
print("was there nan? " + str(callTrainFeature.isnull().values.any()))
trainModelAndUse(basicNN, callTrainFeature, callTrainLabel, callTestFeature, callTestLabel, 100, 10)

