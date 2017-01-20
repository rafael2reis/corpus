# module corpus_gen.py
#
# Copyright (c) 2016 Rafael Reis
#
"""
baseline generator module - Just a copy of corpus_gen.py, with
some codes to generate a baseline Extractor. It's not finished 
at all.

What need to be done is creating a method with lines 160-183
and test if the parser is correct. It just need to colect all Roots
in the dependency annotation. Inside a Root object, there is an array
with its children. Each child (dep) has an attribute size, with the 
number of tokens it has.

Lines 221-269 is the baseline itself: for each Root, the system
says the quote is the Dep in which size is maximum (among its
siblings). The author is either:

1) The left most Dep or
2) If (1) is Dep Size Max, the Dep before or
3) If Dep Size Max is the only Dep, author is "Dummy"

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

    # BASELINE
    corr = 0.0
    incorr = 0.0
    corrD = 0.0 # Correct Dummy
    incorrD = 0.0 # Incorrect Dummy

    quot = 0.0 # Num of real quotations
    corrQuot = 0.0 # Num of correct quotations

    # Direct Quotes
    dCorr = 0.0
    dIncorr = 0.0
    dCorrQuot = 0.0 

    # Indirect Quotes
    iCorr = 0.0
    iIncorr = 0.0
    iCorrQuot = 0.0
    # /BASELINE

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

            # Base line
            depLast = '-'
            depSize = 0
            piece.roots = []
            root = Root()
            rootLast = '-'
            #
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

                    # BASELINE
                    rootCurr = dep[-1:]
                    if rootCurr != rootLast:
                        if rootLast != '-':
                            print("rootCurr, rootLast:", rootCurr, rootLast)
                            print("deps:", len(root.deps))
                            piece.roots.append(root)
                            root = Root()
                        rootLast = rootCurr

                    if dep != depLast:
                        if depLast[:4] != 'Root' and depLast != '-':
                            o = Dep()
                            o.label = depLast
                            o.size = depSize
                            o.quote = quote != '-'
                            o.author = author != '-'
                            o.pattern = pattern
                            root.addDep(o)
                        depLast = dep
                        depSize = 1
                    else:
                        depSize += 1
                    # /BASELINE

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

            # BASE LINE ----------------------
            for r in piece.roots:
                depMax = Dep()
                depLeft = Dep()

                i = 0
                size = len(r.deps)

                print("size: ", size)

                for d in r.deps:
                    if d.quote:
                        print("pattern: ", d.pattern)
                        quot += 1

                        indirect =  '3' in d.pattern
                        if indirect:
                            iCorrQuot += 1
                        else:
                            dCorrQuot += 1

                    if d.size > depMax.size:
                        depMax = d

                    if i == 0 or (i + 1 < size):
                        depLeft = d

                    i += 1

                if depMax.quote:
                    indirect = '3' in depMax.pattern
                    corrQuot += 1

                    if depLeft.author:
                        corr += 1

                        if indirect:
                            iCorr += 1
                        else:
                            dCorr += 1
                    else:
                        incorr += 1

                        if indirect:
                            iIncorr += 1
                        else:
                            dIncorr += 1
                else:
                    incorrD += 1
            # /BASELINE ----------------------

        #print("")
        lineNum += 1
        rawFeeds.append(rawFeed)

    # BASELINE
    pQuoteX = corrQuot / (corrQuot + incorrD)
    rQuoteX = corrQuot / quot

    dPrecision = dCorr / (dCorr + dIncorr)
    dRecall = dCorr / dCorrQuot

    iPrecision = iCorr / (iCorr + iIncorr)
    iRecall = iCorr / iCorrQuot

    precision = corr / (corr + incorr + incorrD)
    recall = corr / quot

    print("BASELINE:\n")
    print("Direct Association:--------------------------")
    print("P =", dPrecision)
    print("R =", dRecall)
    print("\nIndirect Association:--------------------------")
    print("P =", iPrecision)
    print("R =", iRecall)
    print("\nQuote Extraction:-------------")
    print("P =", pQuoteX)
    print("R =", rQuoteX)
    print("\nAll:--------------------------")
    print("P =", precision)
    print("R =", recall)
    # /BASELINE

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

class Root:

    def __init__(self):
        self.deps = []
    
    def addDep(self, line):
        self.deps.append(line)

class Dep:

    def __init__(self):
        self.label = ''
        self.size = 0
        self.quote = False
        self.author = False
        self.pattern = ''

if __name__ == '__main__':
    groupByFeed()