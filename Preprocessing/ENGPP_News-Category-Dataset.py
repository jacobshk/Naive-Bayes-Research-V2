import json
import csv
from stopwordsiso import stopwords



whitelist = [" ","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
stop = stopwords('en')
stop.add(" ")
stop.add('')
tagCont = {}

with open('Datasets/English datasets/News_Category_Dataset_v2.json','r',encoding='utf-8') as file:
    for entry in file:
        currEntry = json.loads(entry)
        tag = currEntry.get('category')
        headline = currEntry.get('headline')
        desc = currEntry.get('short_description')
        content = (headline + ' ' + desc).lower()
        
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
        #segment text into individual words
        content = (''.join(cleanContent)).split(' ')
        
        #remove stopwords and any whitespace elements 
        content = [i for i in content if i not in stop]

        #logic that creates a dictionary of each tag and adds all words of that tag to the value of that key
        currDict = {tag : content}
        if tag not in (tagCont.keys()):
            tagCont |=currDict
        else:
            tagCont[tag] += content

#necessary for 'fieldnames' paramter of csv DictWriter 
fieldname = ["class","words"]

file = open('Datasets/Processed English/News-Category.csv','w',encoding='utf-8')
csvWriter = csv.writer(file,delimiter=",")
for key in tagCont:
    csvWriter.writerow([key,tagCont[key]])