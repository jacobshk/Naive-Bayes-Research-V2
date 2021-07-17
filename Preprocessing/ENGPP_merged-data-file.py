import pickle
import csv
from stopwordsiso import stopwords

tagCont = {}
whitelist = [" ","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
whitespace = [' ','']
z = 0
stop = stopwords(['en'])

with open('Datasets/English datasets/merged_data_file.csv','r',encoding='utf-8') as file:
    csvReader = csv.reader(file,delimiter=',')
    for entry in csvReader:
        if(z>0):
            tag = entry[1]
            description = entry[2]
            title = entry[3]

            content = title+description
            content = content.lower()
            cleanContent = []
            for i in range(len(content)):
                letter = content[i]
                if letter in whitelist:
                    cleanContent.append(letter)
            content = ''.join(cleanContent)
            content = content.split(' ')
            #remove whitespace
            content = [i for i in content if i not in whitespace]
            #remove stopwords
            content = [i for i in content if i not in stop]
            
            elementsToBePopped = []
            for i in range(len(content)):
                if('http' in content[i]):
                    elementsToBePopped.append(i)
            l=0
            for i in range(len(elementsToBePopped)):
                content.pop(elementsToBePopped[i] - l)
                l+=1

            currDict = {tag : content}
            if tag not in (tagCont.keys()):
                tagCont |=currDict
            else:
                tagCont[tag] += content
            
        z+=1
pickle.dump(tagCont,open('Datasets/Processed English/merged-data-file.pickle','wb'))