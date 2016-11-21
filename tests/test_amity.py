
import unittest
from amity.amity import Amity


class TestAmity(unittest.TestCase):

    def test_add_person(self):
        original_people_count = len(Amity.people)
        response = Amity.add_person('Fawaz', 'Farid', 'Fellow', 'Y')
        new_people_count = len(Amity.people)

        self.assertEquals(new_people_count, original_people_count + 1)
        self.assertEquals(response, "Person Added Succesfully!")

    def test_person_names_validation(self):
        response = Amity.add_person('Farid', 123, 'Fellow', 'Y')
        self.assertEquals(response, "Invalid Name!", msg="Should return an error for invalid inputs.")

    def test_create_room(self):
        original_room_count = len(Amity.rooms)
        response = Amity.create_room('Office', 'Krypton')
        new_room_count = len(Amity.rooms)

        self.assertEquals(new_room_count, original_room_count + 1)
        self.assertEquals(response, "Room(s) Created Succesfully!")


    def test_create_multiple_rooms(self):
        original_room_count = len(Amity.rooms)
        response = Amity.create_room('LivingSpace', 'Ruby', 'Python', 'PHP', 'Haskell')
        new_room_count = len(Amity.rooms)

        self.assertEquals(new_room_count, original_room_count + 4)
        self.assertEquals(response, "Room(s) Created Succesfully!") 

    def test_room_names_validation(self):
        response = Amity.create_room('Office', 235)
        self.assertEquals(response, "Invalid Input! Name is not a string", msg="Should return an error for invalid inputs.")

    def test_room_type_validation(self):
        response = Amity.create_room('Bedroom', 'Occulus')
        self.assertEquals(response, "Invalid Room Type!", msg="Should return an error for invalid inputs.")

    def test_reallocate_person(self):
        pass
