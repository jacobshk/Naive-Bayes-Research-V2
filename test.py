import pickle
from collections import defaultdict
with open('Datasets/Processed English/merged-data-fileTEST.pickle','rb') as file:
    x = pickle.load(file)
    print(x.keys())