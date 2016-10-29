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
from corpus_annotate import Annotator

def gen():
    speechVerbs = corpus.SpeechVerbs()
    c = corpus.CorpusAd("bosque/Bosque_CF_8.0.ad.txt", speechVerbs)

    feeds = corpus.groupByFeed(c)
    lineNum = 0

    fmtToken = '{0:50}'

    quantTokens = 0
    quantSentences = 0
    quantQuotes = 0

    speechVerbs = corpus.SpeechVerbs()
    ca = Annotator(speechVerbs)

    for feed in feeds:
        print('#' + str(lineNum))
        print('##')
        index = 0

        for piece in feed.pieces:
            #print(piece.index)
            quantSentences += 1
            ca.annotate(piece)

            isQuote = False
            for node in piece.nodes:
                if isValidToken(node.raw):
                    quantTokens += 1

                    if node.quote:
                        isQuote = True
                    quote = str(index) if node.quote else '-'
                    author = str(index) if node.author else '-'
                    dep = node.dep if node.dep else '-'

                    """
                    print(fmtToken.format(node.txt) 
                            + fmtToken.format(node.pos)
                            + fmtToken.format(author)
                            + fmtToken.format(quote))
                    """
                    print(node.txt 
                            + '\t' + node.pos
                            + '\t' + dep
                            + '\t' + author
                            + '\t' + quote)

            if isQuote:
                quantQuotes += 1
                index += 1

        #print("")
        lineNum += 1

    print("Quant. feeds: ", len(feeds))
    print("Quant. tokens: ", quantTokens)
    print("Quant. sentences: ", quantSentences)
    print("Quant. quotes: ", quantQuotes)

def isValidToken(txt):
    return not re.search(r'[\w<]+\:[\w\(\)<>]+$' , txt, re.M)

if __name__ == '__main__':
    groupByFeed()