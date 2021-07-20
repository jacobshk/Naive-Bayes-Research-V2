import csv
import json
import unicodedata 
#stopwordsiso = dedicated list of stop words in multiple languages -- comparable stop words for chinese/english
from stopwordsiso import stopwords
#pynlpir = chinese text segmentation package
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

stop = stopwords(["zh"])
j=0


#Step 1: Compile data from file into dictionary of label:sentence
#combine all sentences of same label, such that each key only occurs once
#because the idea is to measure the occurence of a word relative to a certain label, individual sentences are meaningless
#(i.e. bag of words model)

labelContent = {}
with open('Datasets/Chinese datasets/long text/dev.json','r',encoding='utf-8') as file:
    for entry in file:
        currLine = json.loads(entry)
        label = currLine.get('label')
        content = currLine.get('sentence')
        #Remove punctuation/stop words as each entry is added, rather than going over entire dictionary after its been created
        #Remove punctuation 
        content = puncRemover.replace_keywords(content)
        #Segment text into individual words 
        content = pynlpir.segment(content,pos_tagging=False)

        cleanContent = []
        #get rid of unicode (i..e /xa0)
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

        currDict = {label : cleanContent}
        if label not in (labelContent.keys()):
            labelContent |=currDict
        else:
            labelContent[label] += cleanContent

fieldname = ["class","words"]

file = open('Datasets/Processed Chinese/long-text.csv','w',encoding='utf-8')
csvWriter = csv.writer(file,delimiter=",")
for key in labelContent:
    csvWriter.writerow([key,labelContent[key]])