import unittest
from amity.models.rooms import Room, LivingSpace, Office

class TestRooms(unittest.TestCase):

    def test_office_is_instance_of_room(self):
        self.assertTrue('Room', type(Office))

    def test_livingspace_is_instance_of_room(self):
        self.assertTrue('Room', type(LivingSpace))