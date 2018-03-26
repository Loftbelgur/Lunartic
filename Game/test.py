# 3rd party modules
import pygame
import unittest

# Testing classes from main game file
from firstrl import struc_Tile
from firstrl import obj_Actor

class Teststruc_Tile(unittest.TestCase):

    def setUp(self):
        self.func= struc_Tile(1)

    def test_1(self):
        self.assertEqual(self.func.block_path,1)
    def test_2(self):
        self.assertLess(self.func.block_path,2)

class Testobj_Actor(unittest.TestCase):

    def setUp(self):
        self.func= obj_Actor(1,1,1,1,1,1)
        """
    def test_1(self):
        self.assertEqual(self.func.x,1)
        self.assertEqual(self.func.y,1)
        self.assertEqual(self.func.name_object,1)
        self.assertEqual(self.func.sprite,1)
        self.assertEqual(self.func.creature,1)
        self.assertEqual(self.func.ai,1)
    """
    def test_2(self):
        self.assertEqual(self.func)

if __name__ == '__main__':
    unittest.main()
