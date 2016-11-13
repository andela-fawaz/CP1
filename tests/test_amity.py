
import unittest
from amity.amity import Amity


class TestAmity(unittest.TestCase):
    """
    This is the test for the Amity class which,
    contains functionality for allocating rooms to people.
    """
    def setUp(self):
        self.amity = Amity()
