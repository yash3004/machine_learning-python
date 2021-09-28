#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 22:31:37 2021

@author: yash
"""

#the nlp for the project
#importing the librabies
import pandas as pd
import numpy as np
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
df = pd.read_csv('etsy.csv')
#chechling the null values

print(df.isnull().any(axis = 0))
x = df.iloc[:,1].values
y = []

import pickle 


# In[8]:


def check_review(reviewText):
    #load the model from the pikle file
    file = open('pickle_model_tfidf.pkl','rb')
    recreated_model = pickle.load(file)
    
    
    vocab_file = open('features.pkl','rb')
    recreated_vocab = pickle.load(vocab_file)
    
    from sklearn.feature_extraction.text import TfidfVectorizer
    recreated_vect = TfidfVectorizer(vocabulary = recreated_vocab)

    reviewText_vectorized = recreated_vect.fit_transform([reviewText])
    
    
    
    return recreated_model.predict(reviewText_vectorized)
for i in x:
    a = check_review(i)
    y.append(a)
print(len(a))

import pandas as pd
df = pd.DataFrame()
df['Reviews'] = x
df['positivity'] = y

df.to_csv("balanced_rev_2.csv" , index = True)