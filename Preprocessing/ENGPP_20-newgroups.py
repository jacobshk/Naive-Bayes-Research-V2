import pickle
import os 

# for folders in os.walk(r'D:/Naive-Bayes-Research-v2/Datasets/English datasets/20_newsgroup/20_newsgroup'):
#     for subdirectory in folders[1]:
#         for file in subdirectory:
#             print(folders)
# currDict = {tag : headCont}
#             if tag not in (tagCont.keys()):
#                 tagCont |=currDict
#             else:
#                 tagCont[tag] += headCont

folderFile = {}
#this approach is at least a little inefficient but for this use case its functional enough (i.e. the code only needs to be run once for the research, thus no scalability is required)
for root, dirs, files in os.walk(r'D:/Naive-Bayes-Research-v2/Datasets/English datasets/20_newsgroup/20_newsgroup'):
    for item in dirs:
        for subroot, subdirs, subfiles in os.walk(r'D:/Naive-Bayes-Research-v2/Datasets/English datasets/20_newsgroup/20_newsgroup/'+item): #efficiency is overrated 
            for i in range(len(subfiles)):
                f = open(r'D:/Naive-Bayes-Research-v2/Datasets/English datasets/20_newsgroup/20_newsgroup/'+item+'/'+subfiles[i])
                for line in f:
                    print(f.readline())
                break
            break
        break
    break

        