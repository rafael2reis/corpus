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
import random

TRAIN_FILE = 'gen/corpus-bosquequotes-train.txt'
TEST_FILE = 'gen/corpus-bosquequotes-test.txt'

def gen():
    speechVerbs = corpus.SpeechVerbs()

    quantFeeds = 0
    quantTokens = 0
    quantSentences = 0
    quantQuotes = 0

    lineNum = 0

    # fmtToken = '{0:50}'

    cps = []
    cps.append( corpus.CorpusAd("bosque/Bosque_CF_8.0.ad.txt", speechVerbs) )
    cps.append( corpus.CorpusAd("bosque/Bosque_CP_8.0.ad.txt", speechVerbs) )
    cps.append( corpus.CorpusAd("floresta/FlorestaVirgem_CF_3.0_sub.ad", speechVerbs) )

    rawFeeds = []

    for c in cps:
        f, t, s, q = genByCorpus(c, lineNum, rawFeeds)

        quantFeeds += f
        quantTokens += t
        quantSentences += s
        quantQuotes += q

    test_pct = 0.2
    train, test = split_data(rawFeeds, 1 - test_pct)

    write(train, TRAIN_FILE)
    write(test, TEST_FILE)

    print("Quant. feeds: ", quantFeeds)
    print("Quant. tokens: ", quantTokens)
    print("Quant. sentences: ", quantSentences)
    print("Quant. quotes: ", quantQuotes)

def genByCorpus(c, lineNum, rawFeeds):
    quantTokens = 0
    quantSentences = 0
    quantQuotes = 0

    feeds = corpus.groupByFeed(c)

    speechVerbs = corpus.SpeechVerbs()
    ca = Annotator(speechVerbs, isFloresta=c.isFloresta)

    for feed in feeds:
        rawFeed = RawFeed()

        rawFeed.addLine('#' + str(lineNum))
        rawFeed.addLine('##' + feed.pieces[0].source)
        index = 0

        ca.indexSpeechVerb = 1
        for piece in feed.pieces:
            #print(piece.index)
            quantSentences += 1
            rawFeed.quantSentences += 1
            """
            if piece.speechVerb:
                piece.indexSpeechVerb = indexSpeechVerb
                indexSpeechVerb += 1
            """
            ca.annotate(piece)

            isQuote = False
            for node in piece.nodes:
                if isValidToken(node.raw):
                    quantTokens += 1
                    rawFeed.quantTokens += 1

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
                    rawFeed.addLine(node.txt 
                            + '\t' + node.pos
                            + '\t' + dep
                            + '\t' + author
                            + '\t' + quote)

            if isQuote:
                quantQuotes += 1
                rawFeed.quantQuotes += 1

                index += 1

        #print("")
        lineNum += 1
        rawFeeds.append(rawFeed)

    return len(feeds), quantTokens, quantSentences, quantQuotes

def write(rawFeeds, fileName):
    f = open(fileName, 'w+')

    quantTokens = 0
    quantSentences = 0
    quantQuotes = 0

    for rawFeed in rawFeeds:
        for line in rawFeed.lines:
            f.write(line + '\n')

        quantTokens += rawFeed.quantTokens
        quantSentences += rawFeed.quantSentences
        quantQuotes += rawFeed.quantQuotes

    f.close()

    print(fileName)
    print("===============")
    print("Quant. feeds: ", len(rawFeeds))
    print("Quant. tokens: ", quantTokens)
    print("Quant. sentences: ", quantSentences)
    print("Quant. quotes: ", quantQuotes)
    print("")

def isValidToken(txt):
    return not re.search(r'[\w<]+\:[\w\(\)<>]+$' , txt, re.M)

def split_data(data, prob):
    """split data into fractions [prob, 1 - prob]"""
    results = [], []
    for row in data:
        results[0 if random.random() < prob else 1].append(row)
    return results

class RawFeed:

    def __init__(self):
        self.lines = []
        self.quantTokens = 0
        self.quantSentences = 0
        self.quantQuotes = 0
    
    def addLine(self, line):
        self.lines.append(line)

if __name__ == '__main__':
    groupByFeed()