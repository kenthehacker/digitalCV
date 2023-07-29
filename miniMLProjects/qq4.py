import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import tensorflow as tf
import csv
import matplotlib.pyplot as plt
from tensorflow.python.keras.api._v2 import keras
from tensorflow.python.ops.gen_batch_ops import batch
from tensorflow.python.ops.gen_data_flow_ops import SparseConditionalAccumulator
from tensorflow.keras.datasets import mnist
import numpy as np
(trainX, trainy), (testX, testy) = mnist.load_data()

#makes running the algo faster: 
trainX = tf.keras.utils.normalize(trainX, axis=1)
testX = tf.keras.utils.normalize(testX, axis=1)




numLayers = 10
epochNum = 2
addSigmoid = False 
numSigmoid = 2

def neural_network(x_train, y_train, x_test, y_test):
       # Implement model
       #model = tf.keras.Model()
        model = tf.keras.models.Sequential()
        model.add(tf.keras.layers.Flatten()) #there's dense layer and we have to flatten it
        #hidden layers: Dense(numNeuron, )
        for i in range(numLayers):
            model.add(tf.keras.layers.Dense(128, activation = tf.nn.relu))
        #last layer has 10 beacuse we have 10 different classes
        if addSigmoid:
            for i in range(numSigmoid):
                model.add(tf.keras.layers.Dense(128, activation = tf.keras.activations.sigmoid))
        model.add(tf.keras.layers.Dense(10, activation = tf.nn.relu))

        #define params for training
        model.compile(optimizer='adam', loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), metrics=['accuracy'])
        history = model.fit(x_train, y_train, epochs=epochNum)
        #print(history.history)

        Loss,Accuracy = model.evaluate(x_test,y_test)
        #print("eOut "+str(Loss))
        #print("out samp Accuracy "+str(Accuracy))

        test_loss = history.history['loss']
        test_acc = history.history['accuracy']
        predictions = 0

        model.save("terminator")
        newModel = tf.keras.models.load_model('terminator')
       #TODO: SOFT LAYER
        softMaxlayer = tf.keras.layers.Softmax()
        newModel.add(softMaxlayer)
        predictions = newModel.predict([x_test])
       # Fit and evaluate
       # Calculate predictions
        return test_loss, test_acc, predictions

#test_loss, test_acc, predictions = neural_network(trainX, trainy, testX, testy)

#part b 4 different models
#model 1: epoch = 3 layer = 3
numLayers = 3
epochNum = 3
addSigmoid = False
test_loss, test_acc, predictions = neural_network(trainX, trainy, testX, testy)

for i in range(5):
    print("Predicted as "+str(np.argmax(predictions[i])))
    plt.imshow(testX[i])
    plt.show()


#'''
fig, ax = plt.subplots(4,2)

for i in range(4):
    xValues = [0,1,2,3,4,5,6,7,8,9]
    yValues = predictions[i]
    ax[i, 0].bar(xValues,yValues)
    ax[i, 1].imshow(testX[i])
plt.show()    
#'''
print("model 1 results")
print("testLoss: "+str(test_loss))
print("testAcc: "+str(test_acc))
print("")
#'''
#model 2: epoch = 20, layer = 50
numLayers = 50
epochNum = 20
addSigmoid = False
test_loss, test_acc, predictions = neural_network(trainX, trainy, testX, testy)
print("model 2 results")
print("testLoss: "+str(test_loss))
print("testAcc: "+str(test_acc))
print("")

#model 3: add sigmoid function epoch  = 3, layer = 3
numLayers = 3
epochNum = 3
addSigmoid = True
test_loss, test_acc, predictions = neural_network(trainX, trainy, testX, testy)
print("model 3 results")
print("testLoss: "+str(test_loss))
print("testAcc: "+str(test_acc))
print("")


#'''


#solution for part a, 60000 samples:
f, axarr = plt.subplots(5,5)
counter = 0
for x in range(5):
    for y in range(5):
        axarr[x,y].imshow(trainX[counter])
        counter += 1
plt.show()
