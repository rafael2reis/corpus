# module corpus_annotate.py
#
# Copyright (c) 2015 Rafael Reis
#
"""
corpus module - Functions to process data in the corpus format.

"""
__version__="1.0"
__author__ = "Rafael Reis <rafael2reis@gmail.com>"

from corpus import CorpusAd
from corpus import SpeechVerbs

class Annotator:
    def __init__(self, speechVerbs=None, isFloresta=False):
        self.speechVerbs = speechVerbs
        self.isFloresta = isFloresta
        self.quotesNum = {}
        self.files = {}
        self.fileName = ''
        self.indexSpeechVerb = 1
        self.quantPatterns = [0, 0, 0, 0, 0, 0, 0, 0]
        self.quantPatternsNoSubj = [0, 0, 0, 0, 0, 0, 0, 0]
        self.patternsList = []
        self.patternsNoSubjList = []

    def annotateAll(self, corpus=None):
        #speechVerbs = SpeechVerbs()
        #c = CorpusAd("bosque/Bosque_CF_8.0.ad.txt", speechVerbs)
        #c = CorpusAd("floresta/FlorestaVirgem_CF_3.0_part.ad", speechVerbs)
        self.setFileName(corpus)
        self.openFiles()

        p = corpus.next()
        
        while p:
            f = self.findPattern(p, self.speechVerbs, self.pattern3, '3')
            """
            f = self.findPattern(p, self.speechVerbs, self.pattern1, '1')
            f = self.findPattern(p, self.speechVerbs, self.pattern1NoSubj, '1ns')
            f = self.findPattern(p, self.speechVerbs, self.pattern2, '2')
            f = self.findPattern(p, self.speechVerbs, self.pattern2NoSubj, '2ns')
            f = self.findPattern(p, self.speechVerbs, self.pattern3, '3')
            f = self.findPattern(p, self.speechVerbs, self.pattern3NoSubj, '3ns')
            if not self.isFloresta:
                f = self.findPattern5(p, self.speechVerbs, self.pattern4)
                f = self.findPattern6(p, self.speechVerbs, self.pattern5)
            """
            p = corpus.next()

        self.writeQuotationsNumber()
        self.closeFiles()
        #print("Quotations number: ", self.quotesNum)

    def setFileName(self, corpus):
        corpusFileName = corpus.fileName
        if "Floresta" in corpusFileName:
            self.fileName = "flo_cf_padrao"
        else:
            if "CF" in corpusFileName:
                self.fileName = "bos_cf_padrao"
            else:
                self.fileName = "bos_cp_padrao"

    def openFiles(self):
        for x in range(1, 7):
            self.files[str(x) + '_small'] = open(self.fileName + str(x) + '_small.txt', 'w')
            self.files[str(x) + 'ns_small'] = open(self.fileName + str(x) + '_small_nosubj.txt', 'w')
            self.files[str(x) + '_big'] = open(self.fileName + str(x) + '_big.txt', 'w')
            self.files[str(x) + 'ns_big'] = open(self.fileName + str(x) + '_big_nosubj.txt', 'w')
            
            self.quotesNum[str(x) + '_small'] = 0
            self.quotesNum[str(x) + 'ns_small'] = 0
            self.quotesNum[str(x) + '_big'] = 0
            self.quotesNum[str(x) + 'ns_big'] = 0

    def writeQuotationsNumber(self):
        for x in range(1, 7):
            self.files[str(x) + '_small'].write("Quotations number: " + str(self.quotesNum[str(x) + '_small']))
            self.files[str(x) + 'ns_small'].write("Quotations number: " + str(self.quotesNum[str(x) + 'ns_small']))
            self.files[str(x) + '_big'].write("Quotations number: " + str(self.quotesNum[str(x) + '_big']))
            self.files[str(x) + 'ns_big'].write("Quotations number: " + str(self.quotesNum[str(x) + 'ns_big']))

    def closeFiles(self):
        for x in range(1, 7):
            self.files[str(x) + '_small'].close()
            self.files[str(x) + 'ns_small'].close()
            self.files[str(x) + '_big'].close()
            self.files[str(x) + 'ns_big'].close()

    def annotate(self, p=None):
        self.patternsList = []
        self.patternsNoSubjList = []

        if p.speechVerb:
            allNodes = p.nodes
            speechNodes = p.speechNodes

            for verbNode in speechNodes:
                acc, subj = self.findAccSubj(allNodes, verbNode)

                if self.pattern1(acc, subj, verbNode, self.speechVerbs):
                    acc.markQuote()
                    acc.markPattern('1')
                    subj.markAuthor()

                    self.quantPatterns[1] += 1
                    self.patternsList.append(1)

                elif self.pattern3(acc, subj, verbNode, self.speechVerbs):
                    acc.markQuote()
                    acc.markPattern('3')
                    subj.markAuthor()

                    self.quantPatterns[3] += 1
                    self.patternsList.append(3)

                elif self.pattern2(acc, subj, verbNode, self.speechVerbs):
                    acc.markQuote()
                    acc.markPattern('2')
                    subj.markAuthor()

                    self.quantPatterns[2] += 1
                    self.patternsList.append(2)

                elif self.pattern1NoSubj(acc, subj, verbNode, self.speechVerbs):
                    acc.markQuote()
                    acc.markPattern('1nosubj')
                    acc.markNosubj()

                    self.quantPatternsNoSubj[1] += 1
                    self.patternsNoSubjList.append(1)

                elif self.pattern3NoSubj(acc, subj, verbNode, self.speechVerbs):
                    acc.markQuote()
                    acc.markPattern('3nosubj')
                    acc.markNosubj()

                    self.quantPatternsNoSubj[3] += 1
                    self.patternsNoSubjList.append(3)

                elif self.pattern2NoSubj(acc, subj, verbNode, self.speechVerbs):
                    acc.markQuote()
                    acc.markPattern('2nosubj')
                    acc.markNosubj()

                    self.quantPatternsNoSubj[2] += 1
                    self.patternsNoSubjList.append(2)

                elif not self.isFloresta:
                    # Searches for Pattern 4
                    acc, subj, acc2 = self.findAccSubjAcc(allNodes, verbNode)

                    if self.pattern4(acc, subj, acc2, verbNode, self.speechVerbs):
                        #print("ACHOU 4")

                        acc.markQuote()
                        acc.markPattern('4')
                        acc2.markQuote()
                        acc2.markPattern('4')
                        subj.markAuthor()

                        self.quantPatterns[4] += 1
                        self.patternsList.append(4)
                    else:
                        # Searches for Pattern 5
                        acc, subj, acc2 = self.searchAccSubjMinusAcc(allNodes, verbNode)

                        if self.pattern5(acc, subj, acc2, verbNode, self.speechVerbs):
                            #print("ACHOU 5")

                            acc.markQuote()
                            acc.markPattern('5')
                            acc2.markQuote()
                            acc2.markPattern('5')
                            subj.markAuthor()

                            self.quantPatterns[5] += 1
                            self.patternsList.append(5)

                self.indexSpeechVerb += 1

        return self.patternsList, self.patternsNoSubjList

    def findPattern(self, p, speechVerbs, pattern, number):
        exist = False

        if p.speechVerb:
            allNodes = p.nodes
            speechNodes = p.speechNodes

            for verbNode in speechNodes:
                acc, subj = None, None

                if self.isFloresta:
                    acc, subj = self.searchAccSubjFloresta(allNodes, verbNode)
                else:
                    acc, subj = self.searchAccSubj(allNodes, verbNode)

                if pattern(acc, subj, verbNode, speechVerbs):
                    acc.markQuote()
                    subj.markAuthor()
                    #self.saveQuote(p, subj, verbNode, acc, number)

                    exist = True
        return exist

    def saveQuote(self, p, subj, verbNode, acc, number):
        # CHANGE: tirar o IF ============
        if len(p.sentence) <= 140:
            self.quotesNum[number + '_small'] += 1
            self.writeQuotation(self.files[number + '_small'], p, subj, verbNode, acc)
        else:
            self.quotesNum[number + '_big'] += 1
            self.writeQuotation(self.files[number + '_big'], p, subj, verbNode, acc)
        # CHANGE ============

    def pattern1(self, acc, subj, verbNode, speechVerbs):
        """ 
            ACC [word="|»] [word=,] VSAY SUBJ
            ACC [word="|»] [word=,] SUBJ VSAY
        """
        return (acc and self.isValidSubj(subj) 
                    and self.hasCloseQuotesComma(acc)
                    and (verbNode.speechVerb in speechVerbs.pattern1))

    def pattern1NoSubj(self, acc, subj, verbNode, speechVerbs):
        """ 
            ACC [word="|»] [word=,] VSAY SUBJ
            ACC [word="|»] [word=,] SUBJ VSAY
        """
        return (acc and self.isNotSubj(subj) 
                    and self.hasCloseQuotesComma(acc)
                    #and self.isNoSubjVerb(verbNode)
                    and (verbNode.speechVerb in speechVerbs.pattern1))

    def pattern2(self, acc, subj, verbNode, speechVerbs):
        """
            SUBJ VSAY [word=:] [word="|«] ACC
            VSAY SUBJ[word=:] [word="|«] ACC
        """
        return (acc and self.isValidSubj(subj) 
                    and (self.hasColonOpenQuotes(subj, acc) or self.hasColonOpenQuotes(verbNode, acc))
                    and (verbNode.speechVerb in speechVerbs.pattern2))

    def pattern2NoSubj(self, acc, subj, verbNode, speechVerbs):
        """
            SUBJ VSAY [word=:] [word="|«] ACC
            VSAY SUBJ[word=:] [word="|«] ACC
        """
        return (acc and self.isNotSubj(subj)
                    #and self.isNoSubjVerb(verbNode)
                    and self.hasColonOpenQuotes(verbNode, acc)
                    and (verbNode.speechVerb in speechVerbs.pattern2))

    def pattern3(self, acc, subj, verbNode, speechVerbs):
        """
            SUBJ VSAY ACC[que]
        """
        return (acc and self.isValidSubj(subj) 
                    and self.hasChildQue(acc)
                    and (verbNode.speechVerb in speechVerbs.pattern3))

    def pattern3NoSubj(self, acc, subj, verbNode, speechVerbs):
        """
            SUBJ VSAY ACC[que]
        """
        return (acc and self.isNotSubj(subj)
                    #and self.isNoSubjVerb(verbNode)
                    and self.hasChildQue(acc)
                    and (verbNode.speechVerb in speechVerbs.pattern3))
        
    def findPattern5(self, p, speechVerbs, pattern):

        if p.speechVerb:
            allNodes = p.nodes
            speechNodes = p.speechNodes

            for verbNode in speechNodes:
                acc, subj, acc2 = None, None, None

                if self.isFloresta:
                    acc, subj, acc2 = self.searchAccSubjAccFloresta(allNodes, verbNode)
                else:
                    acc, subj, acc2 = self.searchAccSubjAcc(allNodes, verbNode)

                if pattern(acc, subj, acc2, verbNode, speechVerbs):
                    self.saveQuote(p, subj, verbNode, acc, '5')

                    return True
        return False

    def pattern4(self, acc, subj, acc2, verbNode, speechVerbs):
        """ antigo padrao 5
            ACC [word="|»] [word=,] VSAY SUBJ [word=,] [word="|«] ACC
            ACC [word="|»] [word=,] SUBJ VSAY [word=,] [word="|«] ACC
        """
        return (acc and acc2
                    and self.isValidSubj(subj)
                    and self.hasCloseQuotesComma(acc)
                    and (self.hasCommaOpenQuotes(subj, acc2) or self.hasCommaOpenQuotes(verbNode.parent, acc2))
                    and (verbNode.speechVerb in speechVerbs.pattern4))

    def findPattern6(self, p, speechVerbs, pattern):

        if p.speechVerb:
            allNodes = p.nodes
            speechNodes = p.speechNodes

            for verbNode in speechNodes:
                acc, subj, acc2 = self.searchAccSubjMinusAcc(allNodes, verbNode)

                if pattern(acc, subj, acc2, verbNode, speechVerbs):
                    self.saveQuote(p, subj, verbNode, acc, '6')

                    return True
        return False

    def pattern5(self, acc, subj, acc2, verbNode, speechVerbs):
        """ antigo padrao 6
            ACC [!="|'|»] [word=--|,] VSAY SUBJ [word=--|,] [word!=" | '|«] –ACC
            ACC [word!=""\".*|'|»"] [word="--|,"] SUBJ VSAY [word="--|,"] [word!=""\".*| '|«"] -ACC
        """
        return (acc and acc2
                    and self.isValidSubj(subj)
                    and ((self.hasCommaInBetween(acc, verbNode.parent)
                            and self.isNext(verbNode.parent, subj)
                            and self.hasCommaInBetween(subj, acc2))
                        or (self.hasDashInBetween(acc, verbNode.parent)
                            and self.isNext(subj, verbNode.parent)
                            and self.hasDashInBetween(subj, acc2)))
                    and (verbNode.speechVerb in speechVerbs.pattern5))

    def pattern7(self, acc, subj, verbNode, speechVerbs):
        """
            ACC [word=,] [word=como|conforme|segundo] VSAY SUBJ
            ACC [word=,] [word=como|conforme|segundo] SUBJ VSAY
        """
        return (acc and self.isValidSubj(subj) 
                    and (self.hasCommaWord(acc, verbNode) or self.hasCommaWord(acc, subj))
                    and (verbNode.speechVerb in speechVerbs.pattern7))

    def writeQuotation(self, file, p, subj, verbNode, acc, acc2=None):
        file.write(p.id + '\n')
        file.write(p.sentence + '\n')
        if subj:
            file.write("QUEM: " + subj.text() + '\n')
        else:
            file.write("QUEM: <nosubj>" + '\n')
        file.write(verbNode.txt + '\n')
        acc2Text = ""
        if acc2:
            acc2Text = acc2.text()
        file.write("O QUE: " + acc.text() + acc2Text + '\n\n')

    def printQuotation(self, p, subj, verbNode, acc, acc2=None):
        print(p.id)
        print(p.sentence)
        if subj:
            print("QUEM: " + subj.text())
        else:
            print("QUEM: <nosubj>")
        print(verbNode.txt)
        acc2Text = ""
        if acc2:
            acc2Text = acc2.text()
        print("O QUE: " + acc.text() + acc2Text + '\n')

    def isNext(self, before, after):
        return before.next == after

    def hasColonOpenQuotes(self, subj, acc):
        if subj.parent and subj.parent.next and subj.parent.next.next and subj.parent.next.next.next:
            return subj.parent.next.txt == ":" and subj.parent.next.next.txt in ("«", "\"") and subj.parent.next.next.next.type == 'ACC'
        else:
            return False

    def hasCloseQuotesComma(self, acc):

        if not self.isFloresta:
            if acc.next and acc.next.posterior:
                return acc.next.txt in ("»", "»\"", "\"") and acc.next.posterior.txt in (",")
        else:
            node = acc.posterior
            while node:
                if (node.txt in ("»", "»\"", "\"") 
                    and node.posterior
                    and node.posterior.txt in (",")):
                    return True

                node = node.posterior
            
            return False

    def hasCommaInBetween(self, acc, verbNode):
        if acc.next and acc.next.next:
            return acc.next.txt in (",") and acc.next.next.txt == verbNode.txt
        else:
            return False

    def hasDashInBetween(self, acc, verbNode):
        if acc.next and acc.next.next:
            return acc.next.txt in ("--") and acc.next.next.txt == verbNode.txt
        else:
            return False

    def hasCommaOpenQuotes(self, subj, acc):
        if subj.parent and subj.parent.next and subj.parent.next.next and subj.parent.next.next.next:
            return subj.parent.next.txt == "," and subj.parent.next.next.txt in ("«", "\"") and subj.parent.next.next.next.type == 'ACC'
        else:
            return False

    def hasCommaWord(self, acc, subj):
        if acc.next and acc.next.child and acc.next.child[0] and acc.next.child[0].child and acc.next.child[0].child[0] and acc.next.child[0].child[0].next and acc.next.child[0].child[0].next.child and acc.next.child[0].child[0].next.child[0]:
            return (acc.next.txt == "," 
                and acc.next.child[0].child[0].txt in ("como", "conforme", "segundo")
                and acc.next.child[0].child[0].next.child[0] == subj)
        else:
            return False 

    def hasChildQue(self, acc):
        return acc.child and acc.child[0].txt and acc.child[0].txt.lower().strip() == "que"

    def isValidSubj(self, subj):
        # TODO ver o txt do SUBJ
        return subj and subj.text().lower().strip() != "se" and subj.text().lower().strip() != "que"

    def isNotSubj(self, subj):
        return subj == None

    def isNoSubjVerb(self, verbNode):
        return "<nosubj>" in verbNode.stype

    def findAccSubj(self, allNodes, verbNode):
        if self.isFloresta:
            acc, subj = self.searchAccSubjFloresta(allNodes, verbNode)
        else:
            acc, subj = self.searchAccSubj(allNodes, verbNode)

        return acc, subj

    def findAccSubjAcc(self, allNodes, verbNode):
        if self.isFloresta:
            acc, subj, acc2 = self.searchAccSubjAccFloresta(allNodes, verbNode)
        else:
            acc, subj, acc2 = self.searchAccSubjAcc(allNodes, verbNode)

        return acc, subj, acc2

    def searchAccSubjFloresta(self, allNodes, verbNode):
        accNode = None
        subjNode = None

        leftFromVerb = True
        indexChild = 1

        for node in allNodes:
            if (node.level == verbNode.level 
                and node.parent == verbNode.parent):

                leftFromVerb, indexChild = self.markDepFloresta(node, verbNode, leftFromVerb, indexChild)

                if node.type == 'Od' or node.type == '-Od':
                    #print("accNode: ", node.raw)
                    accNode = node
                elif node.type == 'S':
                    subjNode = node

        if accNode and accNode.text().lower().strip() == 'que':
            accNode = None

        return accNode, subjNode

    def markDepFloresta(self, node, verbNode, leftFromVerb, indexChild):
        if node.txt not in ('.', ',', '»', '«', ':', ')', '('):
            if node.line == verbNode.line:
                node.markDep('Root' + str(self.indexSpeechVerb))
                leftFromVerb = False
                indexChild = 1
            elif leftFromVerb:
                node.markDep('ChildL' + str(indexChild) + ':Root' + str(self.indexSpeechVerb))
                indexChild += 1
            else:
                node.markDep('ChildR' + str(indexChild) + ':Root' + str(self.indexSpeechVerb))
                indexChild += 1

        return leftFromVerb, indexChild

    def searchAccSubj(self, allNodes, verbNode):
        accNode = None
        subjNode = None

        leftFromVerb = True
        indexChild = 1

        for node in allNodes:

            if (node.level == verbNode.parent.level 
                and node.parent == verbNode.parent.parent):

                leftFromVerb, indexChild = self.markDep(node, verbNode, leftFromVerb, indexChild)

                # Defines ACC, SUBJ labels:
                if node.type == 'ACC':
                    accNode = node
                elif node.type == 'SUBJ':
                    subjNode = node

        if accNode and accNode.text().lower().strip() == 'que':
            accNode = None

        return accNode, subjNode

    def markDep(self, node, verbNode, leftFromVerb, indexChild):
        if node.txt not in ('.', ',', '»', '«', ':', ')', '('):
            if node.line == verbNode.parent.line:
                node.markDep('Root' + str(self.indexSpeechVerb))
                leftFromVerb = False
                indexChild = 1
            elif leftFromVerb:
                node.markDep('ChildL' + str(indexChild) + ':Root' + str(self.indexSpeechVerb))
                indexChild += 1
            else:
                node.markDep('ChildR' + str(indexChild) + ':Root' + str(self.indexSpeechVerb))
                indexChild += 1

        return leftFromVerb, indexChild

    def searchAccSubjAdvl(self, allNodes, verbNode):
        accNode = None
        subjNode = None
        advl = None

        if (verbNode.parent
            and verbNode.parent.parent
            and verbNode.parent.parent.parent
            and verbNode.parent.parent.parent.type == 'ADVL'):

            advl = verbNode.parent.parent.parent

            for node in allNodes:
                
                if (node.level == verbNode.parent.level 
                    and node.parent == verbNode.parent.parent
                    and node.type == 'ACC'):
                        accNode = node
                elif (node.type == 'SUBJ'
                    and node.level == advl.level):
                        subjNode = node

        if accNode and accNode.text().lower().strip() == 'que':
            accNode = None

        return accNode, subjNode

    def searchAccSubjAcc(self, allNodes, verbNode):
        accNode = None
        acc2Node = None
        subjNode = None

        foundAcc = False

        leftFromVerb = True
        indexChild = 1

        for node in allNodes:
            
            if (node.level == verbNode.parent.level 
                and node.parent == verbNode.parent.parent):

                leftFromVerb, indexChild = self.markDep(node, verbNode, leftFromVerb, indexChild)

                if node.type == 'ACC': 
                    if not foundAcc:
                        accNode = node
                        foundAcc = True
                    else:
                        acc2Node = node
                elif node.type == 'SUBJ':
                    subjNode = node

        return accNode, subjNode, acc2Node

    def searchAccSubjAccFloresta(self, allNodes, verbNode):
        accNode = None
        acc2Node = None
        subjNode = None

        foundAcc = False

        leftFromVerb = True
        indexChild = 1

        for node in allNodes:
            
            if (node.level == verbNode.level 
                and node.parent == verbNode.parent):
                if node.type == 'Od': 
                    if not foundAcc:
                        accNode = node
                        foundAcc = True
                    else:
                        acc2Node = node
                elif node.type == 'S':
                    subjNode = node

        return accNode, subjNode, acc2Node

    def searchAccSubjMinusAcc(self, allNodes, verbNode):
        accNode = None
        acc2Node = None
        subjNode = None

        for node in allNodes:
            
            if (node.level == verbNode.parent.level 
                and node.parent == verbNode.parent.parent):
                if node.type == 'ACC': 
                    accNode = node
                elif node.type == '-ACC':
                    acc2Node = node        
                elif node.type == 'SUBJ':
                    subjNode = node

        return accNode, subjNode, acc2Node