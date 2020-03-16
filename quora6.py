# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 16:19:15 2018

@author: ying.g.sun
"""

import pandas as pd
from sklearn import preprocessing
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
#from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
#from sklearn.tree import DecisionTreeClassifier
#from sklearn.neighbors import KNeighborsClassifier
#from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
#from sklearn.naive_bayes import GaussianNB
#from sklearn.svm import SVC
#from sklearn.ensemble import RandomForestClassifier
#from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score
from sklearn import model_selection
from nltk.corpus import stopwords
import numpy as np
#from xgboost import DMatrix
from lightgbm import LGBMClassifier
import re
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from mlxtend.feature_selection import SequentialFeatureSelector as SFS
from mlxtend.plotting import plot_sequential_feature_selection as plot_sfs

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

print('stage1')
#############tfidf############  
le = preprocessing.LabelEncoder()
Y = le.fit_transform(target) 
del target

#stoplist = set('for a of the and to in'.split())

texts = [document.replace("'",'') for document in question]

questiont = [document.replace("'",'') for document in questiont]


    
print('stage2')

count_vect = CountVectorizer(strip_accents ='unicode',ngram_range = (1,2),analyzer = 'word',token_pattern = r'\b\w+\b',max_df=0.8,min_df = 2)
X_counts = count_vect.fit_transform(texts)
tfidf_transformer = TfidfTransformer()
X = tfidf_transformer.fit_transform(X_counts)
X_new_counts = count_vect.transform(questiont)
X_new = tfidf_transformer.transform(X_new_counts)
del question

print('stage3')
##############select model##########
validation_size = 0.20
seed = 7
scoring = 'f1'
X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(texts, Y, test_size=validation_size, random_state=seed)

X_counts = count_vect.fit_transform(X_train)
X_train = tfidf_transformer.fit_transform(X_counts)
X_new_counts = count_vect.transform(X_validation)
X_validation = tfidf_transformer.transform(X_new_counts)
                
##########predict###########                
clf = LogisticRegression(class_weight = 'balanced')
#clf = LGBMClassifier(boosting_type = 'goss',class_weight = 'balanced')                
clf.fit(X_train, Y_train)

def chooseth(X_validation,Y_validation,X_train,Y_train):
    score = 0
    thre = 0
    threshold = [i * 0.01 for i in range(100)]
    clf = LogisticRegression(class_weight = 'balanced')               
    clf.fit(X_train, Y_train)
    for i in threshold:
        probab = clf.predict_proba(X_validation)
        predictions = np.zeros(len(Y_validation))
        predictions[probab[:,1]>i] = 1
        if f1_score(Y_validation, predictions)>score:
            score = f1_score(Y_validation, predictions)
            thre = i
        print(i)
    return thre,score
    
#def choosefeature(X_validation,Y_validation,X_train,Y_train):
#    rfe = RFE(estimator=clf, n_features_to_select=1, verbose = 2,step=0.1)
#    rfe.fit(X_train, Y_train)
#    ranking = rfe.ranking_
     
#predictions = clf.predict(X_validation)
probab = clf.predict_proba(X_validation)
predictions = np.zeros(len(Y_validation))
predictions[probab[:,1]>0.78] = 1

print(f1_score(Y_validation, predictions))
print(confusion_matrix(Y_validation, predictions))
print(classification_report(Y_validation, predictions))

clf = LogisticRegression(class_weight = 'balanced')
#clf = LGBMClassifier(boosting_type = 'goss',class_weight = 'balanced')
clf.fit(X,Y)
probab = clf.predict_proba(X_new)
predictions = probab[:,1]>0.78

###########output############
#output = {'qid':qid,
#          'prediction':predictions
#          }
#df = pd.DataFrame(output,columns = ['qid','prediction'])
#df.to_csv('C:/Users/ying.g.sun/Documents/Kaggle/Quora/submission.csv',index = False)
#0.6358017626187479