import unittest
from amity.models.rooms import Room, LivingSpace, Office


class TestRooms(unittest.TestCase):
    def setUp(self):
        self.office = Office('Krypton')
        self.ls = LivingSpace('Scala')

    def test_office_is_instance_of_room(self):
        self.assertTrue(Room, type(self.office))

    def test_livingspace_is_instance_of_room(self):
        self.assertTrue(Room, type(self.ls))