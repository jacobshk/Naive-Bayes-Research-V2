import csv
import unicodedata
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from stopwordsiso import stopwords
import pynlpir
#flashtext = module with flashtext algorithm that performs string search/replacement faster than native python string functions
from flashtext import KeywordProcessor

#this dictionary functions as a blacklist for the original string: the other blacklist is necessary as it as used when parsing through each individual string in the created list of strings
keywordDictionary = {
    ' ': [".",",","。","，","、","：","；","？","！","「","『","』","」","‧","《","》","〈","〉","﹏﹏﹏ ","……","——"," ——","–","～ ","\"","“","”","】","【","?",'[',']','┃','●''[',']','/',".","0","1","2","3","4","5","6","7","8","9","0","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z",'\x08','\u200b',"A",'B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','X','Y','Z']
}
puncRemover = KeywordProcessor()
puncRemover.add_keywords_from_dict(keywordDictionary)
blacklist = [' ','”','“',".",",",'!','@','#','$','%','^','&','*','`','~',"=",'-','_','+','|','\\','<','>','.','?','(',')','[',']','/',".","0","1","2","3","4","5","6","7","8","9","0","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z",'\x08','\u200b',"A",'B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','X','Y','Z']
pynlpir.open()
whitelist = [" ","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
stop = stopwords(['zh'])
stop.add("")

#remove any non chinese characters
def clean_text(content):
    cleanContent = []
    for word in content:
                word = unicodedata.normalize('NFKC',word)
                #remove stop words
                if word not in stop:                                   
                    i = len(word)
                    for letter in word:
                        if letter in blacklist:
                            break
                        #if none of the letters in the word are in the blacklist (i.e. if the for loop doesnt break while parsing through the word), then append entire word to cleanContent
                        if(letter == word[i-1]):
                            if not letter == " ":
                                cleanContent.append(word)
    return cleanContent

cv = CountVectorizer(lowercase = False)
with open('Datasets/Chinese datasets/chinese_news.csv','r',encoding='utf-8') as csvFile:
    csvReader = csv.reader(csvFile,delimiter =',')
    finalContent = []
    y = []
    for row in csvReader:
        tag = row[1]
        headline = row[2]
        content = row[3]
        headCont = headline + content
        content = puncRemover.replace_keywords(content)
        content = pynlpir.segment(content,pos_tagging=False)
        content = clean_text(content)

        if not (len(content) == 0):
            y.append(tag)
            finalContent.append(content)
        

df = pd.DataFrame()
docs = []

for i in finalContent:
    docs.append(str(i))
X = cv.fit_transform(docs)

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.25,random_state=24,shuffle=True)
model = MultinomialNB().fit(X_train,y_train)
print(model.score(X_test,y_test))