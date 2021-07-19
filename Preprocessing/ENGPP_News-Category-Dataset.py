import json
import csv
from stopwordsiso import stopwords



whitelist = [" ","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
stop = stopwords('en')
stop.add(" ")
stop.add('')
tagCont = {}
reject = []
finalContent = []


with open('Datasets/English datasets/News_Category_Dataset_v2.json','r',encoding='utf-8') as file:
    for entry in file:
        currEntry = json.loads(entry)
        tag = currEntry.get('category')
        headline = currEntry.get('headline')
        desc = currEntry.get('short_description')
        content = (headline + ' ' +desc).lower()
        
        cleanContent = []
        #remove invalid characters (i.e. grammar, numbers, etc.)
        for i in range(len(content)):
            letter = content[i]
            if letter in whitelist:
                cleanContent.append(letter)
        content = ''.join(cleanContent)

        #segment text into individual words
        content = content.split(' ')
        
        #remove stopwords and whitespace elements 
        content = [i for i in content if i not in stop]

        #logic that creates a dictionary of each tag and adds all words of that tag to the value of that key
        currDict = {tag : content}
        if tag not in (tagCont.keys()):
            tagCont |=currDict
        else:
            tagCont[tag] += content

#necessary for 'fieldnames' paramter of csv DictWriter 
fieldname = []
for key in tagCont:
    fieldname.append(key)


file = open('Datasets/Processed English/News-Category.csv','w',encoding='utf-8')
csvWriter = csv.DictWriter(file,fieldnames=fieldname)
csvWriter.writeheader()
for key in tagCont:
    csvWriter.writerow({key : tagCont[key]})
