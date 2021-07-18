import csv
import pickle 
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
tagCont = {}
stop = stopwords(["zh"])

z=0
tagWords = {}
with open('Datasets/Chinese datasets/chinese_news.csv',encoding='utf-8') as file:
    csvReader = csv.reader(file,delimiter = ',')
    for row in csvReader:
        if(z>0):
            tag = row[1]
            headline = row[2]
            content = row[3]
            
            #Combine headline/content, segment
            headCont = headline + content
            #Remove punctuation 
            headCont = puncRemover.replace_keywords(headCont)
            #Segment text into individual words 
            headCont = pynlpir.segment(headCont,pos_tagging=False)
            #Remove whitespace, 
            headCont = [i for i in headCont if i not in whitespace]
            #Remove \n artifacts
            headCont = [s.replace('\n', '') for s in headCont]

            

            #Remove any english characters or numbers
            elementsToBePopped = []
            for i in range(len(headCont)): #go through all elements of content list
                blacklisted = False
                word = headCont[i]
                for j in range(len(word) ): #go through all characters of element i 
                    if(word[j] in blacklist):
                        elementsToBePopped.append(i)
                        blacklisted = True
                        break
                    if(blacklisted):
                        break         
            j=0
            for i in range(len(elementsToBePopped)):
                headCont.pop(elementsToBePopped[i]-j)
                j+=1 #necessary to pop correct index as every pop decreases total list size by 1
            
            #remove stop words
            headCont = [i for i in headCont if i not in stop]           
            currDict = {tag : headCont}
            if tag not in (tagCont.keys()):
                tagCont |=currDict
            else:
                tagCont[tag] += headCont
            
        z+=1
    pickle.dump(tagCont,open('Datasets/Processed Chinese/chinese_news.pickle','wb'))

        