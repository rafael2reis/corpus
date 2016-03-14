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

def annotate():
    speechVerbs = SpeechVerbs()
    c = CorpusAd("bosque/Bosque_CP_8.0.ad.txt", speechVerbs)

    p = c.next()
    while p:
        #f = findPattern(p, speechVerbs, pattern3)
        #f = findPattern(p, speechVerbs, pattern1)
        #f = findPattern(p, speechVerbs, pattern3NoSubj)
        #f = findPattern(p, speechVerbs, pattern2)
        #f = findPattern(p, speechVerbs, pattern7)
        #f = findPattern5(p, speechVerbs, pattern5)
        f = findPattern6(p, speechVerbs, pattern6)

        p = c.next()

def findPattern(p, speechVerbs, pattern):
    if p.speechVerb:
        allNodes = p.nodes
        speechNodes = p.speechNodes

        for verbNode in speechNodes:
            acc, subj = searchAccSubj(allNodes, verbNode)

            if pattern(acc, subj, verbNode, speechVerbs):
                printQuotation(p, subj, verbNode, acc)

                return True
    return False

def pattern1(acc, subj, verbNode, speechVerbs):
    """ 
        ACC [word="|»] [word=,] VSAY SUBJ
        ACC [word="|»] [word=,] SUBJ VSAY
    """
    return (acc and isValidSubj(subj) 
                and hasCloseQuotesComma(acc)
                and (verbNode.speechVerb in speechVerbs.pattern1))

def pattern1NoSubj(acc, subj, verbNode, speechVerbs):
    """ 
        ACC [word="|»] [word=,] VSAY SUBJ
        ACC [word="|»] [word=,] SUBJ VSAY
    """
    return (acc and isNotSubj(subj) 
                and hasCloseQuotesComma(acc)
                and isNoSubjVerb(verbNode)
                and (verbNode.speechVerb in speechVerbs.pattern1))

def pattern2(acc, subj, verbNode, speechVerbs):
    """
        SUBJ VSAY [word=:] [word="|«] ACC
        VSAY SUBJ[word=:] [word="|«] ACC
    """
    return (acc and isValidSubj(subj) 
                and (hasColonOpenQuotes(subj, acc) or hasColonOpenQuotes(verbNode, acc))
                and (verbNode.speechVerb in speechVerbs.pattern2))

def pattern2NoSubj(acc, subj, verbNode, speechVerbs):
    """
        SUBJ VSAY [word=:] [word="|«] ACC
        VSAY SUBJ[word=:] [word="|«] ACC
    """
    return (acc and isNotSubj(subj)
                and isNoSubjVerb(verbNode)
                and hasColonOpenQuotes(verbNode, acc)
                and (verbNode.speechVerb in speechVerbs.pattern2))

def pattern3(acc, subj, verbNode, speechVerbs):
    """
        SUBJ VSAY ACC[que]
    """
    return (acc and isValidSubj(subj) 
                and hasChildQue(acc)
                and (verbNode.speechVerb in speechVerbs.pattern3))

def pattern3NoSubj(acc, subj, verbNode, speechVerbs):
    """
        SUBJ VSAY ACC[que]
    """
    return (acc and isNotSubj(subj)
                and isNoSubjVerb(verbNode)
                and hasChildQue(acc)
                and (verbNode.speechVerb in speechVerbs.pattern3))
    
def findPattern5(p, speechVerbs, pattern):
    if p.speechVerb:
        allNodes = p.nodes
        speechNodes = p.speechNodes

        for verbNode in speechNodes:
            acc, subj, acc2 = searchAccSubjAcc(allNodes, verbNode)

            if pattern(acc, subj, acc2, verbNode, speechVerbs):
                printQuotation(p, subj, verbNode, acc, acc2)

                return True
    return False

def pattern5(acc, subj, acc2, verbNode, speechVerbs):
    """
        ACC [word="|»] [word=,] VSAY SUBJ [word=,] [word="|«] ACC
        ACC [word="|»] [word=,] SUBJ VSAY [word=,] [word="|«] ACC
    """
    return (acc and acc2
                and isValidSubj(subj)
                and hasCloseQuotesComma(acc)
                and (hasCommaOpenQuotes(subj, acc2) or hasCommaOpenQuotes(verbNode.parent, acc2))
                and (verbNode.speechVerb in speechVerbs.pattern5))

def findPattern6(p, speechVerbs, pattern):
    if p.speechVerb:
        allNodes = p.nodes
        speechNodes = p.speechNodes

        for verbNode in speechNodes:
            acc, subj, acc2 = searchAccSubjMinusAcc(allNodes, verbNode)

            if pattern(acc, subj, acc2, verbNode, speechVerbs):
                printQuotation(p, subj, verbNode, acc, acc2)

                return True
    return False

def pattern6(acc, subj, acc2, verbNode, speechVerbs):
    """
        ACC [!="|'|»] [word=--|,] VSAY SUBJ [word=--|,] [word!=" | '|«] –ACC
        ACC [word!=""\".*|'|»"] [word="--|,"] SUBJ VSAY [word="--|,"] [word!=""\".*| '|«"] -ACC
    """
    return (acc and acc2
                and isValidSubj(subj)
                and ((hasCommaInBetween(acc, verbNode.parent)
                        and isNext(verbNode.parent, subj)
                        and hasCommaInBetween(subj, acc2))
                    or (hasDashInBetween(acc, verbNode.parent)
                        and isNext(subj, verbNode.parent)
                        and hasDashInBetween(subj, acc2)))
                and (verbNode.speechVerb in speechVerbs.pattern6))

def pattern7(acc, subj, verbNode, speechVerbs):
    """
        ACC [word=,] [word=como|conforme|segundo] VSAY SUBJ
        ACC [word=,] [word=como|conforme|segundo] SUBJ VSAY
    """
    return (acc and isValidSubj(subj) 
                and (hasCommaWord(acc, verbNode) or hasCommaWord(acc, subj))
                and (verbNode.speechVerb in speechVerbs.pattern7))

def printQuotation(p, subj, verbNode, acc, acc2=None):
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

def isNext(before, after):
    return before.next == after

def hasColonOpenQuotes(subj, acc):
    if subj.parent and subj.parent.next and subj.parent.next.next and subj.parent.next.next.next:
        return subj.parent.next.txt == ":" and subj.parent.next.next.txt in ("«", "\"") and subj.parent.next.next.next.type == 'ACC'
    else:
        return False

def hasCloseQuotesComma(acc):
    if acc.next and acc.next.next:
        return acc.next.txt in ("»", "»\"", "\"") and acc.next.next.txt in (",")
    else:
        return False

def hasCommaInBetween(acc, verbNode):
    if acc.next and acc.next.next:
        return acc.next.txt in (",") and acc.next.next.txt == verbNode.txt
    else:
        return False

def hasDashInBetween(acc, verbNode):
    if acc.next and acc.next.next:
        return acc.next.txt in ("--") and acc.next.next.txt == verbNode.txt
    else:
        return False

def hasCommaOpenQuotes(subj, acc):
    if subj.parent and subj.parent.next and subj.parent.next.next and subj.parent.next.next.next:
        return subj.parent.next.txt == "," and subj.parent.next.next.txt in ("«", "\"") and subj.parent.next.next.next.type == 'ACC'
    else:
        return False

def hasCommaWord(acc, subj):
    if acc.next and acc.next.child and acc.next.child[0] and acc.next.child[0].child and acc.next.child[0].child[0] and acc.next.child[0].child[0].next and acc.next.child[0].child[0].next.child and acc.next.child[0].child[0].next.child[0]:
        return (acc.next.txt == "," 
            and acc.next.child[0].child[0].txt in ("como", "conforme", "segundo")
            and acc.next.child[0].child[0].next.child[0] == subj)
    else:
        return False 

def hasChildQue(acc):
    return acc.child and acc.child[0].txt and acc.child[0].txt.lower() == "que"

def isValidSubj(subj):
    # TODO ver o txt do SUBJ
    return subj and subj.txt.lower() != "se"

def isNotSubj(subj):
    return subj == None

def isNoSubjVerb(verbNode):
    return "<nosubj>" in verbNode.stype

def searchAccSubj(allNodes, verbNode):
    accNode = None
    subjNode = None

    for node in allNodes:
        
        if (node.level == verbNode.parent.level 
            and node.parent == verbNode.parent.parent):
            if node.type == 'ACC':
                accNode = node
            elif node.type == 'SUBJ':
                subjNode = node

    return accNode, subjNode

def searchAccSubjAcc(allNodes, verbNode):
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

def searchAccSubjMinusAcc(allNodes, verbNode):
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