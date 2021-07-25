#https://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html
#https://heartbeat.fritz.ai/naive-bayes-classifier-in-python-using-scikit-learn-13c4deb83bcf
#https://machinelearningmastery.com/prepare-text-data-machine-learning-scikit-learn/
#http://scikit.ml/stratification.html
import numpy
import pandas
import csv
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn import metrics
from skmultilearn.model_selection import iterative_train_test_split
from collections import OrderedDict
from skmultilearn.model_selection.measures import get_combination_wise_output_matrix

df = pandas.read_csv('Datasets/Processed English/merged-data-file.csv', delimiter=',',names=['class','words'],encoding='utf-8')

#step 1: calculate fraction of vocabulary in each class
#x is independent var/feature -- words themselves. X should be an array like obj of shape (# of docs, # of unique words)
X = df.drop('class',axis=1)
with open('Datasets/Processed English/merged-data-fileTEST.pickle','rb') as file:
    x = pickle.load(file)
newDF = pandas.DataFrame(list(x.items())) 

x = newDF.drop(columns=0)
print(x.shape)
#y is dependent var/label -- class of words
y = df['class']
#initial X is a one dimensional dataframe of each class' entire data in one entry per class. This splits the data's entries into multiple columns


#split data into train/test splits, use 25% of data for testing
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.25,random_state = 42)

#create a sparse matrix of words; each word is assigned a number and frequency is counted (i.e. word "x" occurs n amount of times in class Z), rows are classes, columns are words
#Countvectorizer assigns each word an index (identifier) and associates frequency counts with it; how many times it occurs in each class
cv = CountVectorizer()

X_train = cv.fit_transform(X_train.words)
X_test = cv.transform(X_test.words)


#model = MultinomialNB().fit(X_train,y_train)
# print(model.predict(X_test))
