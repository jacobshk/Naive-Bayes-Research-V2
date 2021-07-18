import pickle 
import json
#stopwordsiso = dedicated list of stop words in multiple languages -- comparable stop words for chinese/english
from stopwordsiso import stopwords
#pynlpir = chinese text segmentation package
import pynlpir
#flashtext = module with flashtext algorithm that performs string search/replacement faster than native python string functions
from flashtext import KeywordProcessor

#dictionary in format "replacement value" = ["values", "to", "be"," replaced"]
keywordDictionary = {
    ' ': [".",",","。","，","、","：","；","？","！","「","『","』","」","‧","《","》","〈","〉","﹏﹏﹏ ","……","——"," ——","–","～ ","\"","“","”","】","【","?"]
}
whitespace = [' ','”','“',".",","]
puncRemover = KeywordProcessor()
puncRemover.add_keywords_from_dict(keywordDictionary)
blacklist = [".","0","1","2","3","4","5","6","7","8","9","0","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
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
            #Remove whitespace artifacts
        content = [i for i in content if i not in whitespace]
        elementsToBePopped = []

        #remove all elements containing any english characters or numbers
        for i in range(len(content)): #go through all elements of content list
            blacklisted = False
            word = content[i]
            for j in range(len(word) ): #go through all characters of element i 
                if(word[j] in blacklist):
                    elementsToBePopped.append(i)
                    blacklisted = True
                    break
                if(blacklisted):
                    break         
        j=0
        for i in range(len(elementsToBePopped)):
            content.pop(elementsToBePopped[i]-j)
            j+=1 #necessary to pop correct index as every pop decreases total list size by 1
        
        #remove stop words
        content = [i for i in content if i not in stop]           
        
        currDict = {label : content}
        if label not in (labelContent.keys()):
            labelContent |=currDict
        else:
            labelContent[label] += content

file = open('Datasets/Processed Chinese/long-text.pickle','wb')
pickle.dump(labelContent,file)