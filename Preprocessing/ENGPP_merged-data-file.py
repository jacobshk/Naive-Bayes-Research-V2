import csv
from stopwordsiso import stopwords

tagCont = {}
whitelist = [" ","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
whitespace = [' ','']
z=0
stop = stopwords(['en'])
stop.add("")


with open('Datasets/English datasets/merged_data_file.csv','r',encoding='utf-8') as file:
    csvReader = csv.reader(file,delimiter=',')
    for entry in csvReader:
        if(z>0):
            tag = entry[1]
            description = entry[2]
            title = entry[3]

            content = (title+description).lower()
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
            
            #remove stopwords
            content = [i for i in content if i not in stop]
            
            #remove websites
            finalContent = []
            for i in range(len(content)):
                if not ('http' in content[i]):
                    finalContent.append(content[i])

            currDict = {tag : finalContent}
            if tag not in (tagCont.keys()):
                tagCont |=currDict
            else:
                tagCont[tag] += finalContent 
        z+=1
fieldname = ["class","words"]

file = open('Datasets/Processed English/merged-data-file.csv','w',encoding='utf-8')
csvWriter = csv.writer(file,delimiter=",")
for key in tagCont:
    csvWriter.writerow([key,tagCont[key]])