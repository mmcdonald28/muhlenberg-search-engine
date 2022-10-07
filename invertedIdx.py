import json
import os
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

path = "/Users/matt/Documents"
os.chdir(path)

fileNum = -1
dir = "searchEngineTokens"
for path in os.listdir(dir):
    if os.path.isfile(os.path.join(dir, path)):
        fileNum += 1

path = "/Users/matt/Documents/searchEngineTokens"
os.chdir(path)

# Flags for stemming and stop words
stopWords = False
stemming = False

# Variables
stopWordsSet = set(stopwords.words("english"))
ps = PorterStemmer()
docNumber = 1
txtStr1 = "txt"
txtStr2 = ".txt"
invertedIdx = dict()
maxFreq = [""]

# Loops for each document
for i in range(0, fileNum):
    # temporaryDict to hold max count of word for this doc
    temp = {}
    # Concatenates the string for the document name
    tempStr = txtStr1 + str(docNumber) + txtStr2
    # for each line in the txt file
    for line in open(tempStr):  # line current line
        split = line.split()
        # For each word in line
        for j in split:  # j current word
            currentWord = j
            # Implementing stop words and stemming
            if stemming and stopWords:
                currentWord = ps.stem(currentWord)
                if currentWord in stopWordsSet:
                    continue
            elif stemming:
                currentWord = ps.stem(currentWord)
            elif stopWords:
                if currentWord in stopWordsSet:
                    continue
            # inc the count of this word in the temporary dict
            if temp.get(currentWord) is None:
                temp[currentWord] = 1
            else:
                temp[currentWord] = temp[currentWord] + 1

            # If the word isnt in the index yet, add a list like [docNum, 1]
            # If the word is already in the index check to see if you need to increment or add a new one for teh file
            if currentWord not in invertedIdx:
                invertedIdx[currentWord] = []
                invertedIdx[currentWord].append([docNumber, 1])
            else:
                boolean = False
                for k in invertedIdx[currentWord]:
                    if docNumber == k[0]:
                        boolean = True
                        k[1] = k[1] + 1  # For future ref make sure u didn't fuck anything up here
                if not boolean:
                    invertedIdx[currentWord].append([docNumber, 1])

    # Adding the highest word freq of that doc to the list
    # Protects against error with documents with no words on them
    if temp != {}:
        docMaxFreq = max(temp, key=temp.get)
        maxFreq.append(temp.get(docMaxFreq))
    docNumber = docNumber + 1

print(invertedIdx, "\n")
print(maxFreq)

# Putting the max freq list in the inverted index, just so I can move it over easily in the json file
# It will be taken back out as a list when the inverted idx is taken out of the json file
invertedIdx["MaxFrequencyList"] = maxFreq

# Using same method to transfer over stop words +
if stopWords:
    invertedIdx["StopWordTrueOrFalse"] = 1
else:
    invertedIdx["StopWordTrueOrFalse"] = 0

if stemming:
    invertedIdx["StemmingTrueOrFalse"] = 1
else:
    invertedIdx["StemmingTrueOrFalse"] = 0


# Writing inv idx to a doc
path = "/Users/matt/Documents"
os.chdir(path)

with open("invertedIdx.json", "w") as outfile:
    json.dump(invertedIdx, outfile, indent=4)
    #json.dump(maxFreq, outfile, indent=4)