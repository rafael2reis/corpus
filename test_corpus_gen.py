import unittest
import corpus
import corpus_gen
from corpus import CorpusAd

class TestCorpusGen(unittest.TestCase):

    def testGen(self):
        corpus_gen.gen()
        self.assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main()