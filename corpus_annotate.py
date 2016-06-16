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
        self.quotesNum = 0

    def annotateAll(self, corpus=None):
        #speechVerbs = SpeechVerbs()
        #c = CorpusAd("bosque/Bosque_CF_8.0.ad.txt", speechVerbs)
        #c = CorpusAd("floresta/FlorestaVirgem_CF_3.0_part.ad", speechVerbs)
        p = corpus.next()
        
        while p:
            f = self.findPattern(p, self.speechVerbs, self.pattern1)
            #f = self.findPattern(p, self.speechVerbs, self.pattern1NoSubj)
            #f = self.findPattern(p, self.speechVerbs, self.pattern2)
            #f = self.findPattern(p, self.speechVerbs, self.pattern2NoSubj)
            #f = self.findPattern(p, self.speechVerbs, self.pattern3)
            #f = self.findPattern(p, self.speechVerbs, self.pattern3NoSubj)
            #f = self.findPattern5(p, self.speechVerbs, self.pattern5)
            #f = self.findPattern6(p, self.speechVerbs, self.pattern6)

            p = corpus.next()

        print("Quotations number: ", self.quotesNum)

    def annotate(self, piece=None):
        #f = findPattern(p, speechVerbs, pattern3)
        #f = findPattern(p, speechVerbs, pattern3NoSubj)
        f = self.findPattern(p, self.speechVerbs, self.pattern1)
        #f = findPattern(p, speechVerbs, pattern1NoSubj)
        #f = findPattern(p, speechVerbs, pattern2)
        #f = findPattern(p, speechVerbs, pattern2NoSubj)
        #f = findPattern5(p, speechVerbs, pattern5)
        #f = findPattern6(p, speechVerbs, pattern6)

    def findPattern(self, p, speechVerbs, pattern):
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
                    self.quotesNum += 1
                    self.printQuotation(p, subj, verbNode, acc)

                    exist = True
        return exist

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
                    and self.isNoSubjVerb(verbNode)
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
                    and self.isNoSubjVerb(verbNode)
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
                    and self.isNoSubjVerb(verbNode)
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
                    self.quotesNum += 1
                    printQuotation(p, subj, verbNode, acc, acc2)

                    return True
        return False

    def pattern5(self, acc, subj, acc2, verbNode, speechVerbs):
        """
            ACC [word="|»] [word=,] VSAY SUBJ [word=,] [word="|«] ACC
            ACC [word="|»] [word=,] SUBJ VSAY [word=,] [word="|«] ACC
        """
        return (acc and acc2
                    and self.isValidSubj(subj)
                    and self.hasCloseQuotesComma(acc)
                    and (self.hasCommaOpenQuotes(subj, acc2) or self.hasCommaOpenQuotes(verbNode.parent, acc2))
                    and (verbNode.speechVerb in speechVerbs.pattern5))

    def findPattern6(self, p, speechVerbs, pattern):

        if p.speechVerb:
            allNodes = p.nodes
            speechNodes = p.speechNodes

            for verbNode in speechNodes:
                acc, subj, acc2 = self.searchAccSubjMinusAcc(allNodes, verbNode)

                if pattern(acc, subj, acc2, verbNode, speechVerbs):
                    self.quotesNum += 1
                    self.printQuotation(p, subj, verbNode, acc, acc2)

                    return True
        return False

    def pattern6(self, acc, subj, acc2, verbNode, speechVerbs):
        """
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
                    and (verbNode.speechVerb in speechVerbs.pattern6))

    def pattern7(self, acc, subj, verbNode, speechVerbs):
        """
            ACC [word=,] [word=como|conforme|segundo] VSAY SUBJ
            ACC [word=,] [word=como|conforme|segundo] SUBJ VSAY
        """
        return (acc and self.isValidSubj(subj) 
                    and (self.hasCommaWord(acc, verbNode) or self.hasCommaWord(acc, subj))
                    and (verbNode.speechVerb in speechVerbs.pattern7))

    def printQuotation(self, p, subj, verbNode, acc, acc2=None):
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
            if acc.next and acc.next.next:
                return acc.next.txt in ("»", "»\"", "\"") and acc.next.next.txt in (",")
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

    def searchAccSubjFloresta(self, allNodes, verbNode):
        accNode = None
        subjNode = None

        for node in allNodes:
            if (node.level == verbNode.level 
                and node.parent == verbNode.parent):
                #print("# ", node.raw)
                if node.type == 'Od' or node.type == '-Od':
                    #print("accNode: ", node.raw)
                    accNode = node
                elif node.type == 'S':
                    subjNode = node

        if accNode and accNode.text().lower().strip() == 'que':
            accNode = None

        return accNode, subjNode

    def searchAccSubj(self, allNodes, verbNode):
        accNode = None
        subjNode = None

        for node in allNodes:
            
            if (node.level == verbNode.parent.level 
                and node.parent == verbNode.parent.parent):
                if node.type == 'ACC':
                    accNode = node
                elif node.type == 'SUBJ':
                    subjNode = node

        if accNode and accNode.text().lower().strip() == 'que':
            accNode = None

        return accNode, subjNode

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

        for node in allNodes:
            
            if (node.level == verbNode.parent.level 
                and node.parent == verbNode.parent.parent):
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