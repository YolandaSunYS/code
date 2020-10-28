# -*- coding: utf-8 -*-
"""
Created on Tue May  7 16:17:38 2019

@author: v-yisun
"""

import pandas as pd
from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.charfilter import *
from janome.tokenfilter import *
import re
import numpy as np
from gensim import corpora,models
from collections import defaultdict
import xlwt

from sklearn import preprocessing
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from lightgbm import LGBMClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn import model_selection
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import log_loss
#######################function###################
def is_asian(char):
    
    """Is the character Asian?"""
    IDEOGRAPHIC_SPACE = 0x3000
    # 0x3000 is ideographic space (i.e. double-byte space)
    # Anything over is an Asian character
    return ord(char) > IDEOGRAPHIC_SPACE

def cutwords(word):
    sent = ''
    w = word[0]
    a = is_asian(word[0])
    for i in range(1,len(word)):
        b = is_asian(word[i])
        if a == b:
            w = w+word[i]
        else:
            sent = sent+w+' '
            a = b
            w = word[i]
    sent = sent+w
    return sent


#######################read data#######################################
df = pd.read_excel(r"D:\Documents\work\emotion\decode18_成形後データ_fixed.xlsx")

df1 = pd.read_excel(r"D:\Documents\work\emotion\TechSummit2018_fixed.xlsx")

df2 = pd.concat([df,df1])

data = df2[['Tweet','Sentiment']]  

df3 = pd.read_excel(r"D:\Documents\work\emotion\#decode19_test_20190514_marked_fixed.xlsx")
                    
df4 = pd.read_excel(r"D:\Documents\work\emotion\#decode19_test_20190524_marked.xlsx") 
                    
df5 = pd.read_excel(r"D:\Documents\work\emotion\#decode19_20190529_1630_marked_feedback.xlsx")                     
                    
data1 = pd.concat([data,df3[['Message','Sentiment']],df4[['Message','Sentiment']],df5[['Message','Sentiment']]])                    
                 
tweet = list(data1.groupby(['Tweet']).groups.keys())

Senti = data1.groupby(['Tweet'])['Sentiment'].first().values

df = pd.read_excel(r"D:\Documents\work\emotion\#decode19_20190530.xlsx")
                   
tweet1 = df['Message'].values

###############################ETL#################################
text = tweet.copy()
char_filters = [UnicodeNormalizeCharFilter()]
tokenizer = Tokenizer()
token_filters = [CompoundNounFilter(), LowerCaseFilter()]#POSKeepFilter(['名詞','形容詞']),
a = Analyzer(char_filters, tokenizer, token_filters)
tdesc = []
for i in range(len(text)):
    newsen = ''
    #mySent = re.sub('[?•()（）_→【】|...”「、>:」!,."...%*-]', ' ', text[i])
    mySent = text[i]
    #mySent = mySent.replace('?',' ')
    try:
        sen = mySent.strip()
        tokens = a.analyze(sen)#,wakati=True)
        for j in tokens:
            if ('\\' not in j.surface) and ('/' not in j.surface) and ('@' not in j.surface):
                newsen = newsen + cutwords(j.surface)+' ' 
        newsen = re.sub('[@=#¥~^<。$;+⇒•()（）_→【】{}|...”「、>:」!,."...%*-]', '', newsen)
        newsen = newsen.replace('?',' ').replace('[',' ').replace(']',' ')  
        newsen = re.sub(r'[0-9]+', ' ', newsen)
        tdesc.append(newsen)
        print(newsen)
    except:
        print('abnormal!') 

text = tweet1.copy()
char_filters = [UnicodeNormalizeCharFilter()]
tokenizer = Tokenizer()
token_filters = [CompoundNounFilter(), LowerCaseFilter()]#POSKeepFilter(['名詞','形容詞']),
a = Analyzer(char_filters, tokenizer, token_filters)
tdesc1 = []
for i in range(len(text)):
    newsen = ''
    #mySent = re.sub('[?•()（）_→【】|...”「、>:」!,."...%*-]', ' ', text[i])
    mySent = text[i]
    #mySent = mySent.replace('?',' ')
    try:
        sen = mySent.strip()
        tokens = a.analyze(sen)#,wakati=True)
        for j in tokens:
            if ('\\' not in j.surface) and ('/' not in j.surface) and ('@' not in j.surface):
                newsen = newsen + cutwords(j.surface)+' ' 
        newsen = re.sub('[@=#¥~^<。$;+⇒•()（）_→【】{}|...”「、>:」!,."...%*-]', '', newsen)
        newsen = newsen.replace('?',' ').replace('[',' ').replace(']',' ')  
        newsen = re.sub(r'[0-9]+', ' ', newsen)
        tdesc1.append(newsen)
        print(newsen)
    except:
        print('abnormal!')         
#######################prepare data#####################################
le = preprocessing.LabelEncoder()
Y = le.fit_transform(Senti) 

#####################predict another dataset############
count_vect = CountVectorizer(strip_accents ='unicode',ngram_range = (1,2),analyzer = 'word',token_pattern = r'\b\w+\b',max_df=0.8,min_df = 2)
X_counts = count_vect.fit_transform(tdesc)
tfidf_transformer = TfidfTransformer()
X_train = tfidf_transformer.fit_transform(X_counts)

X_new_counts = count_vect.transform(tdesc1)
X_validation = tfidf_transformer.transform(X_new_counts) 

clf = GradientBoostingClassifier()
clf.fit(X_train, Y)  
predictions = clf.predict(X_validation)

################output###########################################
filename=xlwt.Workbook()  
sheet=filename.add_sheet("output")  
for i in range(len(predictions)):
    if predictions[i] == 2:
        sheet.write(i,0,'POSITIVE')  
    elif predictions[i] == 1:
        sheet.write(i,0,'NEUTRAL')
    else:
        sheet.write(i,0,'NEGATIVE')

filename.save(r'D:\Documents\work\emotion\output.xls')   ##########改路径
