import unittest
from Bankareikningur import bankareikningur
from subprocess import call

class testBankareikningur(unittest.TestCase):
    a= bankareikningur()

    def setUp(self):
        self.func = bankareikningur()

    def test_1(self):
        self.assertTrue(True)
    def test_2(self):
        self.assertEqual(self.func.reikningur, 0)
    def test_3(self):
        self.assertEqual(self.a.reikningur, 0)
    def test_4(self):
        self.a.reikningur += 4*10**(-8)
        self.AssertAlmostEqual(self.func.reikningur, self.a.reikningur)
    def test_values(self):
        self.b= int(self.a.reikningur)
        print(self.b)
    def test_true(self):
        self.assertEqual(self.func.taka_ut(-1000), False)
        # self.assertRaises(ValueError, self.a.saekja_stodu(), -0.1)

if __name__ == '__main__':
    unittest.main()
