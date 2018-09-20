# imports for getting and manipulating data
import requests, zlib
import pandas as pd
import numpy as np

# sklearn models
from sklearn.svm import LinearSVC

# other helpful sklearn imports 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.utils import shuffle
from sklearn.metrics import accuracy_score
from scipy.sparse import hstack

import nltk
from nltk import word_tokenize
nltk.download('all')

data = pd.read_csv('data.csv')
data.text = data.text.astype(str)

def getPosTags(text):
    posTags = nltk.pos_tag(nltk.word_tokenize(text))
    justTags = []
    for tags in posTags:
        justTags.append(tags[1])
    return justTags

data['posTags_list'] = data['text'].apply(lambda x: getPosTags(x))
data['posTags_string'] = data['posTags_list'].apply(lambda x: ' '.join([str(tag) for tag in x]))

tfidf_vectorizer_text = TfidfVectorizer()
tfidf_vectorizer_pos = TfidfVectorizer()

data_tfidf_text = tfidf_vectorizer_text.fit_transform(data['text'])
data_tfidf_pos = tfidf_vectorizer_pos.fit_transform(data['posTags_string'])

data_tfidf = hstack([data_tfidf_pos, data_tfidf_text]).toarray()
data_tfidf = pd.DataFrame(data_tfidf)

split = int(len(data)*0.75)
y_train = data['isClickbait'][:split].values
y_test = data['isClickbait'][split:].values
X_train = data_tfidf[:split].values
X_test = data_tfidf[split:].values

svm = LinearSVC()

svm.fit(X_train, y_train)
predictions = svm.predict(X_test)

print('Support Vector Machine', accuracy_score(y_test, predictions))

from sklearn.externals import joblib

joblib.dump(svm, 'svm.pkl') 
joblib.dump(tfidf_vectorizer_text, 'tfidf_vectorizer_text.pkl')
joblib.dump(tfidf_vectorizer_pos, 'tfidf_vectorizer_pos.pkl')