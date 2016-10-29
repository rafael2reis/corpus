import unittest
import corpus
import corpus_annotate
from corpus import CorpusAd
from corpus import SpeechVerbs
from corpus_annotate import Annotator

class TestCorpusAnnotate(unittest.TestCase):

    def testAnnotate(self):
        speechVerbs = SpeechVerbs()
        """c = CorpusAd("bosque/Bosque_CF_8.0.ad.txt", speechVerbs)
        ann = Annotator(speechVerbs, isFloresta=c.isFloresta)
        ann.annotateAll(c)

        c = CorpusAd("bosque/Bosque_CP_8.0.ad.txt", speechVerbs)
        ann = Annotator(speechVerbs, isFloresta=c.isFloresta)
        ann.annotateAll(c)
        
        c = CorpusAd("floresta/FlorestaVirgem_CF_3.0_part.ad", speechVerbs)
        ann = Annotator(speechVerbs, isFloresta=c.isFloresta)
        ann.annotateAll(c)
        """
        
        c = CorpusAd("floresta/TESTE_Floresta_Claudinha.txt", speechVerbs)
        ann = Annotator(speechVerbs, isFloresta=c.isFloresta)
        ann.annotateAll(c)

        self.assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main()