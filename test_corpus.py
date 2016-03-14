import unittest
import corpus
from corpus import CorpusAd

class TestCorpus(unittest.TestCase):
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testLoadSpeechVerbs(self):
        verbs = corpus.SpeechVerbs()

        self.assertEqual(len(verbs), 8)

    def testInitSuccess(self):
        c = CorpusAd("bosque/Bosque_CF_8.0.ad.txt")

        self.assertEqual(len(c.raw), 177483)

    def testInitFailNone(self):
        self.assertRaises(corpus.InvalidArgumentException, CorpusAd, None)

    def testInitFailInvalid(self):
        self.assertRaises(IOError, CorpusAd, "invalid.txt")

    def testNext(self):
        c = CorpusAd("bosque/Bosque_CF_8.0.ad.txt")

        p = c.next()
        c.next()
        c.next()
        c.next()

        self.assertNotEqual(p, None)

    def testHasSpeechVerb(self):
        c = CorpusAd("bosque/Bosque_CF_8.0.ad.txt")

        v = c.getSpeechVerb("==========MV:v-fin('dizer' <fs-subst> <nosubj> PR 3S IND)é")
        self.assertEqual(v, 'dizer')

    def testNodeNextPrevious(self):
        c = CorpusAd("bosque/Bosque_CF_8.0.ad.txt")
        p = c.next()

        node = p.nodes[0]
        i = 0
        while node.next:
            print(node.next.txt, node.next.level, node.next.stype)
            node = node.next
            i += 1

        self.assertEqual(i, 1)

    def testNodeNextPrevious2(self):
        c = CorpusAd("bosque/Bosque_CF_8.0.ad.txt")
        c.next()
        p = c.next()

        node = p.nodes[18]
        i = 0
        while node.next:
            print("|", node.next.txt, "|", node.next.level, node.next.stype)
            node = node.next
            i += 1

        self.assertEqual(i, 5)

if __name__ == '__main__':
    unittest.main()