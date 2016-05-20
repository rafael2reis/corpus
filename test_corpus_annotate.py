import unittest
import corpus
import corpus_annotate
from corpus import CorpusAd
from corpus import SpeechVerbs
from corpus_annotate import Annotator

class TestCorpusAnnotate(unittest.TestCase):

    def testAnnotate(self):
        speechVerbs = SpeechVerbs()
        c = CorpusAd("bosque/Bosque_CF_8.0.ad.txt", speechVerbs)

        ann = Annotator(speechVerbs, isFloresta=False)
        ann.annotateAll(c)
        
        self.assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main()