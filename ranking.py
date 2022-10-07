import json
import math
import os
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

txtStr1 = "doc"
txtStr2 = ".txt"
path = "/Users/matt/Documents"
os.chdir(path)
stopWordsSet = set(stopwords.words("english"))
ps = PorterStemmer()
stopWords = True
stemming = True

# Open the inverted list
# CHANGE FILE HERE TO IMPLEMENT / TAKE AWAY STEMMING / STOP WORDS
with open('invertedIdxB.json') as infile:
    invertedIdx = json.load(infile)

# Re-make the max frequency list, stop words var and stemming var
if invertedIdx.pop("StemmingTrueOrFalse") == 1:
    stemming = True
if invertedIdx.pop("StopWordTrueOrFalse") == 1:
    stemming = True
maxFreq = invertedIdx.pop("MaxFrequencyList")

#for key in invertedIdx:
    #print(key, invertedIdx[key])

query = input("Search engine! Please enter a search: \n")
# query = "Muhlenberg education yay Lacrosse"

newQuery = ""

split = query.split()
# For each word in line
for j in split:  # j current word
    # Implementing stop words and stemming
    if stemming and stopWords:
        newQuery = newQuery + " " + ps.stem(j)
        if j in stopWordsSet:
            continue
    elif stemming:
        newQuery = newQuery + " " + ps.stem(j)
    elif stopWords:
        if j in stopWordsSet:
            continue
    else:
        newQuery = query

numerator = [""]
denomQ = [""]
denomD = [""]
cosineSimilarity = {}
N = len(maxFreq) - 1
# [SUM Wij * Wiq]  /  |dj| * |q| COSINE SIM EQ

# Loops once for each doc
for i in range(0, N):
    i = i + 1
    line = newQuery.split()

    # First, check if the at least 1 term of the query is in the current document, if not skip to next loop/doc
    exists = False
    for word in line:
        # If the word isn't in the inverted idx (meaning it appears in 0 docs) skip to next word
        if invertedIdx.get(word) is not None:
            # For each occurrence of the word in the inverted idx
            for occurrences in invertedIdx[word]:
                if occurrences[0] == i:
                    exists = True
        else:
            continue

    # If none of the words exist skip to next doc
    if not exists:
        numerator.append("")
        denomQ.append("")
        denomD.append("")
        continue
    else:
        numerator.append(0)
        denomQ.append(0)
        denomD.append(0)

        # For each term in the query, increment the value of the correct key for that term
        temp = dict()
        for word in line:
            if temp.get(word) is None:
                temp[word] = 1
            else:
                temp[word] = temp.get(word) + 1

        # Get the max freq of the query
        maxQuery = 0
        for key in temp:
            if temp[key] >= maxQuery:
                maxQuery = temp[key]

        # Loop through each word of the query AGAIN, now to calculate tf-idf/cosine signature
        for word in line:
            # for each word, find the td idf of that word in both the query, and the current doc
            if word in invertedIdx:
                # Only need to calculate idf once
                idf = N / (len(invertedIdx[word]))

                # td-idf of word in query
                tfQ = temp.get(word) / maxQuery
                tfIdfQ = tfQ * idf

                # td-idf of word in document
                tfD = 0
                # Looks at the inv index to see if the document we are looking at has the query word in it
                # If not, the tf would be 0 making everything 0, so the tfD remains 0 as it was defined above
                for j in invertedIdx[word]:
                    if j[0] == i:
                        tfD = j[1] / maxFreq[i]
                tfIdfD = tfD * idf

                # Adding the weight of the term in the query times the weight of the term in the document
                # For weight of term in the document * weight of term in the query
                numerator[i] = numerator[i] + (tfIdfD * tfIdfQ)

                # Adding the term's tfIdf for the Query and Document into the lists for |dj| and |q|
                denomQ[i] = denomQ[i] + tfIdfQ ** 2
                denomD[i] = denomD[i] + tfIdfQ ** 2

        # Add the cosine similarity at the correct index
        cosineSimilarity[i] = numerator[i] / (math.sqrt(denomQ[i]) * math.sqrt(denomD[i]))

# Looping through documents complete

if len(cosineSimilarity) == 0:
    print("No results found")
else:
    # Reverses and sorts the dict, saves to list
    sorted_dict = {}
    sorted_keys = reversed(sorted(cosineSimilarity, key=cosineSimilarity.get))

    for w in sorted_keys:
        sorted_dict[w] = cosineSimilarity[w]

    #print(cosineSimilarity)
    # Create a list of the doc numbers of the top 10 documents
    output = []
    if len(sorted_dict) < 10:
        for key in sorted_dict:
            output.append(key)
    else:
        counter = 0
        for key in sorted_dict:
            if counter == 10:
                break
            else:
                output.append(key)
                counter = counter + 1
            #print(sorted_dict.get(i))
    #print(output)

    # Print the relevant urls
    path = "/Users/matt/Documents/searchEngineLinks"
    os.chdir(path)

    print("Top results for the search: ", query)
    for j in output:
        tempStr = txtStr1 + str(j) + txtStr2
        for url in open(tempStr):
            print(url)






