import csv
import unicodedata 
from stopwordsiso import stopwords
#pynlpir = chinese text segmentation package
import pynlpir
#flashtext = module with flashtext algorithm that performs string search/replacement faster than native python string functions
from flashtext import KeywordProcessor

#dictionary in format "replacement value" = ["values", "to", "be"," replaced"]
keywordDictionary = {
    ' ': [".",",","。","，","、","：","；","？","！","「","『","』","」","‧","《","》","〈","〉","﹏﹏﹏ ","……","——"," ——","–","～ ","\"","“","”","】","【","?","(",")",'\\','/']
}
puncRemover = KeywordProcessor()
puncRemover.add_keywords_from_dict(keywordDictionary)
blacklist = ['\n',' ','”','“',".",",",'!','@','#','$','%','^','&','*','`','~',"=",'-','_','+','|','\\','<','>','.','?','(',')','[',']','/',".","0","1","2","3","4","5","6","7","8","9","0","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z",'\x08','\u200b',"A",'B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','X','Y','Z']
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

            currDict = {tag : cleanContent}
            if tag not in (tagCont.keys()):
                tagCont |=currDict
            else:
                tagCont[tag] += cleanContent
            
        z+=1

fieldname = ["class","words"]

file = open('Datasets/Processed Chinese/chinese_news.csv','w',encoding='utf-8')
csvWriter = csv.writer(file,delimiter=",")
for key in tagCont:
    csvWriter.writerow([key,tagCont[key]])