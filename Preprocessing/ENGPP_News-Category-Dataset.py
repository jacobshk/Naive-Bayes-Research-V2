import json
import pickle
from stopwordsiso import stopwords


whitelist = [" ","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
whitespace = [' ','']
stop = stopwords('en')
tagCont = {}

with open('Datasets/English datasets/News_Category_Dataset_v2.json','r',encoding='utf-8') as file:
    for entry in file:
        currEntry = json.loads(entry)
        tag = currEntry.get('category')
        headline = currEntry.get('headline')
        desc = currEntry.get('short_description')
        content = headline + ' ' +desc
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

        currDict = {tag : content}
        if tag not in (tagCont.keys()):
            tagCont |=currDict
        else:
            tagCont[tag] += content
pickle.dump(tagCont,open('Datasets/Processed English/News-Category-Dataset.pickle','wb'))