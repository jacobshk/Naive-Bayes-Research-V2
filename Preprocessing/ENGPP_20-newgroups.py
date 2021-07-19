import pickle
import csv
import sys

maxInt = sys.maxsize
while True:
    # decrease the maxInt value by factor 10 
    # as long as the OverflowError occurs.

    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)

j=0

tagCont = {}

with open('Datasets/English datasets/20newsgroup_preprocessed.csv',encoding='utf-8') as file:
    csvReader = csv.reader(file,delimiter=';')
    for entry in csvReader:
        if(j>0):
            content = entry[2]
            tag = entry[0]

            currDict = {tag : content}
            if tag not in (tagCont.keys()):
                tagCont |=currDict
            else:
                tagCont[tag] += content
            
        j+=1
fieldname = []
for key in tagCont:
    fieldname.append(key)

file = open('Datasets/Processed English/20-newsgroup.csv','w',encoding='utf-8')
csvWriter = csv.DictWriter(file,fieldnames=fieldname)
csvWriter.writeheader()
for key in tagCont:
    csvWriter.writerow({key : tagCont[key]})