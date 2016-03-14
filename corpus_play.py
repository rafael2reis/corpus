# module corpus_play.py
#
# Copyright (c) 2015 Rafael Reis
#
"""
corpus module - Functions to analise the Bosque corpus.

"""
__version__="1.0"
__author__ = "Rafael Reis <rafael2reis@gmail.com>"

import corpus

def preProcess():
    speechVerbs = corpus.SpeechVerbs()
    c = corpus.CorpusAd("bosque/Bosque_CP_8.0.ad.txt", speechVerbs)

    feeds = groupByFeed(c)

if __name__ == '__main__':
    groupByFeed()