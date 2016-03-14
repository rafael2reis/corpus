# module corpus_gen.py
#
# Copyright (c) 2016 Rafael Reis
#
"""
corpus generator module - Functions to generate a Corpus based on GloboQuotes format.

"""
__version__="1.0"
__author__ = "Rafael Reis <rafael2reis@gmail.com>"

import re
import corpus

def gen():
    speechVerbs = corpus.SpeechVerbs()
    c = corpus.CorpusAd("bosque/Bosque_CP_8.0.ad.txt", speechVerbs)

    feeds = corpus.groupByFeed(c)
    lineNum = 0

    fmtToken = '{0:50}'

    for feed in feeds:
    	print('#' + str(lineNum))
    	print('##')

    	for piece in feed.pieces:
    		for node in piece.nodes:
    			if isValidToken(node.raw):
    				print(fmtToken.format(node.txt) + node.pos)

    	print("")
    	lineNum += 1

def isValidToken(txt):
	return not re.search(r'[\w<]+\:[\w\(\)<>]+$' , txt, re.M)

if __name__ == '__main__':
    groupByFeed()