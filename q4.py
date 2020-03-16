# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 15:58:54 2018

@author: ying.g.sun
"""

import pandas as pd
from keras import models
from keras import layers
from sklearn import preprocessing
from keras.preprocessing.text import Tokenizer
import matplotlib.pyplot as plt
from sklearn.metrics import f1_score
from keras.preprocessing.sequence import pad_sequences
from sklearn import model_selection
import numpy as np
import keras.backend as K
import tensorflow as tf


########################
def precision(y_true,y_pred,threshold):
     true_positives = K.sum(K.round(K.clip(y_true*y_pred,0,1)+0.5-threshold))
     predicted_positives = K.sum(K.round(K.clip(y_pred,0,1)+0.5-threshold))
     precision = true_positives/(predicted_positives+K.epsilon())
     return precision

def recall(y_true,y_pred,threshold):
     true_positives = K.sum(K.round(K.clip(y_true*y_pred,0,1)+0.5-threshold))
     possible_positives = K.sum(K.round(K.clip(y_true,0,1)+0.5-threshold))
     recall = true_positives/(possible_positives+K.epsilon())
     return recall

def fbeta_score(y_true,y_pred,threshold,beta=1):
     if beta<0:
         raise ValueError('The lowest choosable beta is zero (only precision).')
         
     if K.sum(K.round(K.clip(y_true,0,1)+0.5-threshold)) == 0:
         return 0
     
     p = precision(y_true,y_pred,threshold)
     r = recall(y_true,y_pred,threshold)
     bb = beta**2
     fbeta_score = (1+bb)*(p*r)/(bb*p+r+K.epsilon())
     return fbeta_score

def fmeasure(y_true,y_pred):
     initial = -99.0
     threshold = [i * 0.01 for i in range(50)]
     for i in threshold:
         b = fbeta_score(y_true,y_pred,i,beta =1)
         initial = tf.cond(b>initial,lambda:b,lambda:initial)
     return initial

#########input data##########
file = 'C:/Users/ying.g.sun/Documents/kaggle/quora/train.csv'
data = pd.read_csv(file)
values = data.values
del data
#qid = values[:,0]
question = values[:,1]
target = values[:,2]
del values

file = 'C:/Users/ying.g.sun/Documents/Kaggle/Quora/test.csv'
data = pd.read_csv(file)
value = data.values
del data
questiont = value[:,1]
qid = value[:,0]
del value


##########tokenize########
le = preprocessing.LabelEncoder()
Y = le.fit_transform(target) 

texts = [document.replace("'",'') for document in question]
questiont = [document.replace("'",'') for document in questiont]

tokenizer = Tokenizer(num_words=10000)#5000#15000
tokenizer.fit_on_texts(texts)
X = tokenizer.texts_to_sequences(texts)
X_test = tokenizer.texts_to_sequences(questiont)

validation_size = 0.20
seed = 7
X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=validation_size, random_state=seed)

vocab_size = len(tokenizer.word_index) + 1  # Adding 1 because of reserved 0 index

print(texts[2])
print(X_train[2])

maxlen = 100

X_train = pad_sequences(X_train, padding='post', maxlen=maxlen)
X_validation = pad_sequences(X_validation, padding='post', maxlen=maxlen)
X_test = pad_sequences(X_test, padding='post', maxlen=maxlen)

###########model###########
embedding_dim = 32
max_words = 10000

model = models.Sequential()
model.add(layers.Embedding(max_words, embedding_dim,input_length=maxlen))
model.add(layers.Dropout(0.2))
model.add(layers.LSTM(32))
model.add(layers.Dropout(0.2))
model.add(layers.Dense(1, activation='sigmoid'))
model.compile(optimizer='rmsprop',
              loss='binary_crossentropy',
              metrics=['accuracy',fmeasure])
model.summary()

history = model.fit(X_train, Y_train,
                    epochs=20,
                    validation_split = 0.2,
                    batch_size=512)#512#32

#################33
history_dict = history.history
loss_values = history_dict['loss']
val_loss_values = history_dict['val_loss']
epochs = range(1, 21)
plt.plot(epochs, loss_values, 'bo', label='Training loss')
plt.plot(epochs, val_loss_values, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

############evaluate#########
def chooseth(Y_validation,y_pred):
     score = 0
     thre = 0
     threshold = [i * 0.01 for i in range(100)]
     for i in threshold:
         predictions = np.zeros(len(Y_validation))
         predictions[y_pred[:,0]>i] = 1
         if f1_score(Y_validation, predictions)>score:
             score = f1_score(Y_validation, predictions)
             thre = i
         print(i)
     return thre,score

ypred = model.predict(X_validation)
print(f1_score(Y_validation, ypred))

###(0.28, 0.6319238839863176)