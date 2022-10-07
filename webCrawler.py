"""Get the initial URL. The initial URL is an entry point for the web crawler, which links to the web page that needs to
 be crawled; While crawling the web page, we need to fetch the HTML content of the page, then parse it to get the URLs
 of all the pages linked to this page. Put these URLs into a queue; Loop through the queue, read the URLs from the queue
 one by one, for each URL, crawl the corresponding web page, then repeat the above crawling process; Check whether the
 stop condition is met. If the stop condition is not set, the crawler will keep crawling until it cannot get a new URL."""
import os
import re
from urllib.request import urlopen
import requests
from nltk.tokenize import word_tokenize
from urllib3 import Retry

# Queue of valid files, counters for pages retrieved, as well as abs and rel files, initial url, and a str for the
# title of all my output .txt files, will have a number concatenated onto the end later
queue = list()
url = "http://www.muhlenberg.edu/"
queue.append(url)
docFile = "doc"
txtFile = "txt"

# Loop 8000 times, for 8000 urls crawled (max i have ever crawled is 8300)
for fileNum in range(0, 8000):  # J doing five for now to set up rest of program

    # Setting path, I am outputting the .txt files to a folder in my computer
    path = "/Users/matt/Documents/searchEngineLinks"
    os.chdir(path)

    currentFile = queue.pop(0)

    # This while loop determines if a file is valid, for ease I am just using muhlenberg.edu urls
    # This checks to make sure it's a valid link (status code 200) with muhlenberg.edu in the address
    # I also did not use capstone urls, since we no longer use capstone, and I was getting weird errors with them
    bool = False
    while bool is False:
        bool = True
        if "muhlenberg.edu" not in currentFile or "capstone" in currentFile or "wescoeadmissions" in currentFile or "video" in currentFile:
            bool = False
        else:
            r = requests.get(currentFile)
            if r.status_code != 200:
                #print(currentFile)
                bool = False
        if bool is False:
            currentFile = queue.pop(0)

    #print(currentFile)
    #print(r.text)

    # Regular expression: looks after href, for 1 or more numbers, letters, or any of the special symbols included.
    # I have one reg expression for urls with single quotes, and one for urls with double quotes, so I get them all
    links1 = re.findall(r"href=\'([a-zA-z0-9\.\_\#\?\:\/\-\\.]*)", r.text)
    fileList = re.findall(r"href=\"([a-zA-z0-9\.\_\#\?\:\/\-\\.]*)", r.text)

    # Combines the two sets of urls
    for i in links1:
        fileList.append(i)

    # Now that we have all the links, we must clean them, and remove the invalid ones
    # Also validates that
    # validLinks = []
    for i in fileList:
        if "png" in i:
            pass
        elif "svg" in i:
            pass
        elif "webmanifest" in i:
            pass
        elif "ico" in i:
            pass
        elif "css" in i:
            pass
        elif "http" in i:
            if i not in queue:
                queue.append(i)
                #validLinks.append(i)
        else:
            if "#" in i:
                i = re.sub('\#', '', i)
            temp = url + i
            if temp not in queue:
                queue.append(temp)
                #validLinks.append(temp)

    tempNum = fileNum + 1
    tempDocFile = str(docFile) + str(tempNum)
    tempDocFile = tempDocFile + ".txt"
    # print(tempTxtFile)

    # Write to the .txt file
    #with open(tempDocFile, 'w') as f:
    #    f.write(currentFile)
        #f.write("\n")
        #f.write(str(validLinks))

    # Change path to write to the tokens doc
    path = "/Users/matt/Documents/searchEngineTokens"
    os.chdir(path)

    # COMMENTED DUE TO USE OF BS4 BELOW
    # Set of regular expressions to extract the words from <p> tags and headers
    # <p> tags first
    tokens = []
    temp = re.findall(r"<p>([a-zA-z0-9\ \.\,\_\#\?\:\/\-\\.]*)", r.text)
    for i in temp:
        tokenize = word_tokenize(i)
        for j in tokenize:
            tokens.append(j)

    # Now headers
    temp2 = re.findall(r"<h[0-9]([a-zA-z0-9\ \.\,\_\"\#\?\>\=\:\/\-\\.]*)", r.text)
    for i in temp2:
        words = re.findall(">([a-zA-z0-9\ \.\,\_\"\#\?\>\=\:\/\-\\.]*)", str(i))
        for j in words:
            tokenize = word_tokenize(j)
            for k in tokenize:
                tokens.append(k)

    print("tokens ", tokens)
    print(fileNum)

    # Concatenate to str for writing to file
    tempTxtFile = str(txtFile) + str(tempNum)
    tempTxtFile = tempTxtFile + ".txt"
    # print(tempTxtFile)

    # Write to the .txt file
    with open(tempTxtFile, 'w') as f:
        #f.write(currentFile)
        #f.write("\n")
        for i in tokens:
            f.write(i)
            f.write(" ")

