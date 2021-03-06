import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from stopwordsiso import stopwords
whitelist = [" ","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
stop = stopwords(['en'])
stop.add("")
def remove_websites(content):
    finalContent = []
    for i in range(len(content)):
        if not ('www' in content[i]):
            if not ('http' in content[i]):
                finalContent.append(content[i])
    return finalContent

#remove any non alpha numeric characters
def clean_text(content):
    cleanContent = []
    lastWasSpace = False #this var ensures there is only one space between each word, so the split function doesnt create strings of whitespace
    #remove any invalid characters (i.e. non alnums such as punctuation) and separate words by whitespace (which is preserved) into a list of strings
    for letter in content:
        if letter in whitelist:
            if letter == " ":
                if not lastWasSpace:
                    cleanContent.append(letter)
                lastWasSpace = True

            if not letter == " ":
                cleanContent.append(letter)
                lastWasSpace = False
    
    content = (''.join(cleanContent)).split(' ')
    return content

cv = CountVectorizer(lowercase = False)
with open('Datasets/English datasets/News_Category_Dataset_v2.json','r',encoding='utf-8') as jsonFile:
    
    finalContent = []
    y = []
    for entry in jsonFile:
        data = json.loads(entry)
        tag = data["category"]
        #create a list tags in parallel with finalcontent, so that the tag of each doc is associated with it by index
        description = data['short_description']
        title = data['headline']
        content = (description+' '+title).lower()
        content = clean_text(content)
        content = [i for i in content if i not in stop]
        content = remove_websites(content)
        if not (len(content) == 0):
            y.append(tag)
            finalContent.append(content)
df = pd.DataFrame()
docs = []


for i in finalContent:
    docs.append(str(i))
X = cv.fit_transform(docs)


X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.25,random_state=1,shuffle=True)
multimodel = MultinomialNB().fit(X_train,y_train)
bernmodel = BernoulliNB().fit(X_train,y_train)

print("Seed 1 Multinomial: ",multimodel.score(X_test,y_test))
print("Seed 1 Bernoulli: ",bernmodel.score(X_test,y_test))

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.25,random_state=20,shuffle=True)
multimodel = MultinomialNB().fit(X_train,y_train)
bernmodel = BernoulliNB().fit(X_train,y_train)

print("Seed 20 Multinomial: ",multimodel.score(X_test,y_test))
print("Seed 20 Bernoulli: ",bernmodel.score(X_test,y_test))

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.25,random_state=42,shuffle=True)
multimodel = MultinomialNB().fit(X_train,y_train)
bernmodel = BernoulliNB().fit(X_train,y_train)

print("Seed 42 Multinomial: ",multimodel.score(X_test,y_test))
print("Seed 42 Bernoulli: ",bernmodel.score(X_test,y_test))