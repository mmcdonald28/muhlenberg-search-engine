# muhlenberg-search-engine
AI project, a localized search engine based off a web crawler of 8,000 pages of my schools website.
This project uses a webCrawler to search the pages of my schools website, which creates text files containing all of the words, a file containg the link, and an inverted index containg all words, and the page number and occurencs of the word.
Multiple inverted indexes are created, based off of it includes stemming, stopwords, both, or neither.
My ranking program then reads a prompt, and reads from the chosen inverted index, and uses cosine simuluarity to rank and return the top links of the pages closest to the searched for queue.
If someone else were to use this they would have to change the file path to one in their own computer, and would just have to enter the queue when run and the inverted index to feature stemming, stopwords, etc. as prompted too in the ranking.py file.
