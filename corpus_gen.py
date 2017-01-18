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
    quantPronomes = 0

    lineNum = 0

    # fmtToken = '{0:50}'

    cps = []
    cps.append( corpus.CorpusAd("bosque/Bosque_CF_8.0.ad.txt", speechVerbs) )
    cps.append( corpus.CorpusAd("bosque/Bosque_CP_8.0.ad.txt", speechVerbs) )
    cps.append( corpus.CorpusAd("floresta/FlorestaVirgem_CF_3.0_sub.ad", speechVerbs) )

    rawFeeds = []
    quantPatterns = [0, 0, 0, 0, 0, 0, 0, 0]
    quantPatternsNoSubj = [0, 0, 0, 0, 0, 0, 0, 0]

    for c in cps:
        f, t, s, q, pronome, qPt, qPtNosubj = genByCorpus(c, lineNum, rawFeeds)

        quantFeeds += f
        quantTokens += t
        quantSentences += s
        quantQuotes += q
        quantPronomes += pronome
        quantPatterns = [x + y for x, y in zip(quantPatterns, qPt)]
        quantPatternsNoSubj = [x + y for x, y in zip(quantPatternsNoSubj, qPtNosubj)]

    test_pct = 0.2
    train, test = split_data(rawFeeds, 1 - test_pct)

    write(train, TRAIN_FILE)
    write(test, TEST_FILE)

    print("Quant. feeds: ", quantFeeds)
    print("Quant. tokens: ", quantTokens)
    print("Quant. sentences: ", quantSentences)
    print("Quant. quotes: ", quantQuotes)
    print("Quant. pronomes: ", quantPronomes)
    print("---------")
    print("Padrão 1: ", quantPatterns[1])
    print("Padrão 2: ", quantPatterns[2])
    print("Padrão 3: ", quantPatterns[3])
    print("Padrão 4: ", quantPatterns[4])
    print("Padrão 5: ", quantPatterns[5])
    print("<nosubj> Padrão 1: ", quantPatternsNoSubj[1])
    print("<nosubj> Padrão 2: ", quantPatternsNoSubj[2])
    print("<nosubj> Padrão 3: ", quantPatternsNoSubj[3])

def genByCorpus(c, lineNum, rawFeeds):
    quantTokens = 0
    quantSentences = 0
    quantQuotes = 0
    quantPronomes = 0

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
            #print("\n")
            quantSentences += 1
            rawFeed.quantSentences += 1
            """
            if piece.speechVerb:
                piece.indexSpeechVerb = indexSpeechVerb
                indexSpeechVerb += 1
            """
            patterns, patternsNoSubj = ca.annotate(piece)
            for k in patterns:
                rawFeed.quantPatterns[k] += 1
            for k in patternsNoSubj:
                rawFeed.quantPatternsNoSubj[k] += 1

            isQuote = False
            achouAutor = False
            for node in piece.nodes:
                if isValidToken(node):
                    quantTokens += 1
                    rawFeed.quantTokens += 1

                    if node.quote:
                        isQuote = True
                    if node.quote and node.nosubj:
                        quote = "-1"
                    elif node.quote:
                        quote = str(index)
                    else:
                        quote = '-'
                    author = str(index) if node.author else '-'
                    dep = node.dep if node.dep else '-'
                    pattern = node.pattern if node.pattern else '-'

                    """
                    if node.author and not achouAutor:
                        if "H:" in node.raw:
                            print(node.raw.replace("\n", ""), "\t", node.pos)
                            achouAutor = True
                    """

                    if node.author and node.txt in ("ele", "ela", "eles", "elas"):
                        quantPronomes += 1

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
                            + '\t' + quote
                            + '\t' + pattern)

            if isQuote:
                quantQuotes += 1
                rawFeed.quantQuotes += 1

                index += 1

        #print("")
        lineNum += 1
        rawFeeds.append(rawFeed)

    return len(feeds), quantTokens, quantSentences, quantQuotes, quantPronomes, ca.quantPatterns, ca.quantPatternsNoSubj

def write(rawFeeds, fileName):
    f = open(fileName, 'w+')

    f.write('word\tpos\tdep\tauthor\tquote\tpattern\n')

    quantTokens = 0
    quantSentences = 0
    quantQuotes = 0
    quantPatterns = [0, 0, 0, 0, 0, 0, 0, 0]
    quantPatternsNoSubj = [0, 0, 0, 0, 0, 0, 0, 0]

    for rawFeed in rawFeeds:
        for line in rawFeed.lines:
            f.write(line + '\n')

        quantTokens += rawFeed.quantTokens
        quantSentences += rawFeed.quantSentences
        quantQuotes += rawFeed.quantQuotes

        quantPatterns = [x + y for x, y in zip(quantPatterns, rawFeed.quantPatterns)]
        quantPatternsNoSubj = [x + y for x, y in zip(quantPatternsNoSubj, rawFeed.quantPatternsNoSubj)]

    f.close()

    print(fileName)
    print("===============")
    print("Quant. feeds: ", len(rawFeeds))
    print("Quant. tokens: ", quantTokens)
    print("Quant. sentences: ", quantSentences)
    print("Quant. quotes: ", quantQuotes)
    print("---------")
    print("Padrão 1: ", quantPatterns[1])
    print("Padrão 2: ", quantPatterns[2])
    print("Padrão 3: ", quantPatterns[3])
    print("Padrão 4: ", quantPatterns[4])
    print("Padrão 5: ", quantPatterns[5])
    print("<nosubj> Padrão 1: ", quantPatternsNoSubj[1])
    print("<nosubj> Padrão 2: ", quantPatternsNoSubj[2])
    print("<nosubj> Padrão 3: ", quantPatternsNoSubj[3])
    print("")

def isValidToken(node):
    txt = node.raw
    return (not re.search(r'[\w<\+\[\]\d\/<> ]+\:[\w\(\)<>\- ]+$' , txt, re.M)
            and node.txt != '')

def split_data(data, prob):
    """split data into fractions [prob, 1 - prob]"""
    random.seed(4114)

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
        self.quantPatterns = [0, 0, 0, 0, 0, 0, 0, 0]
        self.quantPatternsNoSubj = [0, 0, 0, 0, 0, 0, 0, 0]
    
    def addLine(self, line):
        self.lines.append(line)

if __name__ == '__main__':
    groupByFeed()