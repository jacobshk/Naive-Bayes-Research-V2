import csv
import unicodedata 
from stopwordsiso import stopwords
#pynlpir = chinese text segmentation package
import pynlpir
#flashtext = module with flashtext algorithm that performs string search/replacement faster than native python string functions
from flashtext import KeywordProcessor

#dictionary in format "replacement value" = ["values", "to", "be"," replaced"]
keywordDictionary = {
    ' ': [".",",","。","，","、","：","；","？","！","「","『","』","」","‧","《","》","〈","〉","﹏﹏﹏ ","……","——"," ——","–","～ ","\"","“","”","】","【","?","(",")",'\\','/','\xa0']
}
whitespace = [' ','”','“',".",","]
puncRemover = KeywordProcessor()
puncRemover.add_keywords_from_dict(keywordDictionary)
blacklist = [".","0","1","2","3","3000","4","5","6","7","8","9","0","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A",'B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','X','Y','Z']
pynlpir.open()
tagCont = {}
stop = stopwords(["zh"])
stop.add('【')
stop.add('】')
stop.add('\u3000')

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
            #get rid of unicode (i..e /xa0)
            for i in range(len(headCont)):
                headCont[i] = unicodedata.normalize('NFKC',headCont[i])
            #Remove any english characters or numbers
            elementsToBePopped = []
            for i in range(len(headCont)): #go through all elements of content list
                blacklisted = False
                word = headCont[i]
                for j in range(len(word) ): #go through all characters of element i 
                    if(word[j] in blacklist):
                        elementsToBePopped.append(i)
                        blacklisted = True
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

fieldname = []
for key in tagCont:
    fieldname.append(key)

with open('Datasets/Processed Chinese/chinese_news.csv','w',encoding='utf-8') as file:
    csvWriter = csv.DictWriter(file,fieldnames=fieldname)
    csvWriter.writeheader()
    for key in tagCont:
        csvWriter.writerow({key : tagCont[key]})