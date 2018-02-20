import unittest
import maxutil

class testMaxFunctions(unittest.TestCase):
    def test_maxseq(self):
        self.assertEqual(maxutil.maxseq('abc'), 1)
        self.assertEqual(maxutil.maxseq('aaxxxt'), 3)

    def test_maxdiff(self):
        self.assertEqual(maxutil.maxdiff([5,23,1,0]),22)
        self.assertEqual(maxutil.maxdiff([23,5,1,0]),18)

if __name__ == '__main__':
    unittest.main(verbosity=2, exit=False)
