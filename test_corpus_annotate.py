import unittest
import corpus
import corpus_annotate
from corpus import CorpusAd

class TestCorpusAnnotate(unittest.TestCase):

    def testAnnotate(self):
        corpus_annotate.annotate()
        self.assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main()