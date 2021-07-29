from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB, BernoulliNB

cv = CountVectorizer(lowercase = False)

train_data = fetch_20newsgroups(subset='train')
test_data = fetch_20newsgroups(subset='test')

X_train = cv.fit_transform(train_data.data)
y_train = train_data.target

X_test = cv.transform(test_data.data)
y_test = test_data.target

multimodel = MultinomialNB().fit(X_train,y_train)
bernmodel = BernoulliNB().fit(X_train,y_train)

print("Multinomial:"+multimodel.score(X_test,y_test))
print("Bernoulli:"+bernmodel.score(X_test,y_test))