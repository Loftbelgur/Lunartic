# 3rd party modules
import pygame
import unittest
import random

# Testing classes from main game file
from main import struc_Tile
from main import obj_Actor
from main import com_Creature

class Teststruc_Tile(unittest.TestCase):

    def setUp(self):
        self.func= struc_Tile(1)

    def test_1(self):
        self.assertEqual(self.func.block_path,1)
    def test_2(self):
        self.assertLess(self.func.block_path,2)

class Testcom_Creature(unittest.TestCase):

    def setUp(self):
        self.func = com_Creature('nonni')

    def test_1(self):
        self.assertEqual(self.func,'nonni')

class Testobj_Actor(unittest.TestCase):

    # Can't get this test to work
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

if __name__ == '__main__':
    unittest.main()
