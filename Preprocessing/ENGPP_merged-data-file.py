import csv
from stopwordsiso import stopwords
import pickle
from collections import defaultdict
tagCont = defaultdict(list)
whitelist = [" ","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
whitespace = [' ','']
z=0
t = 0
stop = stopwords(['en'])
stop.add("")

def remove_websites(content):
    finalContent = []
    for i in range(len(content)):
        if not ('www' in content[i]):
            if not ('http' in content[i]):
                finalContent.append(content[i])
    return finalContent

#remove any non alpha numeric characters
def clean_text(content):
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
    
    content = (''.join(cleanContent)).split(' ')
    return content

with open('Datasets/English datasets/merged_data_file.csv','r',encoding='utf-8') as file:
    tagReader = csv.reader(file,delimiter=',')
    for entry in tagReader:
        tag = entry[1]
        if tag not in tagCont.keys():
            if not tag == "Category":
                tagCont[tag] = None

with open('Datasets/English datasets/merged_data_file.csv','r',encoding='utf-8') as file:
    csvReader = csv.reader(file,delimiter=',')
    
    for entry in csvReader:
        if(z>0):
            cat = entry[1]
            description = entry[2]
            title = entry[3]

            content = (title+' '+description).lower()
            content = clean_text(content)
            
            #remove stopwords
            content = [i for i in content if i not in stop]
            
            #remove websites
            content = remove_websites(content)
            if tagCont[cat] == None:
                tagCont[cat] = content
            elif not tagCont[cat] == None:
                tagCont[cat].append(content)
        z+=1



file = open('Datasets/Processed English/merged-data-fileTEST.pickle','wb')
for key in tagCont:
    pickle.dump(tagCont,file)



f = open('Datasets/Processed English/merged-data-file.csv','w',encoding='utf-8')
csvWriter = csv.writer(f,delimiter=",")
for key in tagCont:
    csvWriter.writerow([key,tagCont[key]])
