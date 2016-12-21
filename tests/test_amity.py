import unittest
from amity.amity import Amity


class TestAmity(unittest.TestCase):

    def setUp(self):
        self.amity = Amity()
        self.rooms = self.amity.livingspaces + self.amity.offices

    def test_add_person(self):
        original_people_count = len(self.amity.people)
        response = self.amity.add_person('Fawaz', 'Farid', 'Fellow', 'Y')
        new_people_count = len(self.amity.people)

        self.assertEquals(new_people_count, original_people_count + 1)
        self.assertEquals(response, "FAWAZ FARID Added Succesfully! \n")

    def test_add_person_validates_input(self):
        fname_error = self.amity.add_person(123, 'Fawaz', 'Fellow', 'Y')
        lname_error = self.amity.add_person('Farid', 123, 'Fellow', 'Y')
        role_error = self.amity.add_person('Farid', 'Fawaz', 'Person', 'Y')
        wants_accomodation_error = self.amity.add_person('Austin', 'Roy', 'Fellow', 'C')

        self.assertEquals(fname_error, "Invalid Input!")
        self.assertEqual(lname_error, "Invalid Input!")

        self.assertEqual(role_error,
                         "Invalid Role! person should be FELLOW or STAFF.",
                         msg="Should return an error for invalid role")

        self.assertEqual(wants_accomodation_error,
                         "Invalid Input! input should be Y or N.",
                         msg="Should return an error for invalid Input.")

    def test_create_room(self):
        original_room_count = len(self.rooms)
        response = self.amity.create_room('O', 'Krypton')
        new_room_count = len(self.amity.offices)

        self.assertEquals(new_room_count, original_room_count + 1)
        self.assertEquals(response, "Room(s) Created Successfully!")

    def test_create_room_creates_multiple_rooms(self):
        original_room_count = len(self.amity.livingspaces)
        response = self.amity.create_room('LS', 'Ruby', 'Python', 'PHP', 'Haskell')
        new_room_count = len(self.amity.livingspaces)

        self.assertEquals(new_room_count, original_room_count + 4)
        self.assertEquals(response, "Room(s) Created Successfully!")

    def test_create_room_validates_input(self):
        room_name_error = self.amity.create_room('O', 235)
        self.assertEquals(room_name_error,
                          "Invalid Input!",
                          msg="Should return an error for invalid inputs.")

        room_type_error_1 = self.amity.create_room('Bedroom', 'Occulus')
        room_type_error_2 = self.amity.create_room(123, 'Occulus')
        self.assertEquals(room_type_error_1, "Invalid Room Type!",
                          msg="Should return an error for invalid inputs.")

        self.assertEquals(room_type_error_2, "Invalid Input!",
                          msg="Should return an error for invalid inputs.")

    def test_room_can_only_be_created_once(self):
        self.amity.create_room('LS', 'JavaScript')
        msg = self.amity.create_room('LS', 'JavaScript')

        self.assertEqual(msg, "Room already exists!")

    def test_add_person_to_room_returns_error_if_no_rooms(self):
        self.amity.add_person('Percila', 'Njira', 'Staff', 'N')
        msg = self.amity.add_person_to_room(self.amity.people[-1], self.amity.offices)
        self.assertEqual(msg, "There are no available rooms \n")

    def test_add_person_to_room_appends_to_unallocated_list_if_no_rooms(self):
        self.amity.add_person('Percila', 'Njira', 'Staff', 'N')
        self.amity.add_person_to_room(self.amity.people[-1], self.amity.offices)

        self.assertEqual('PERCILA NJIRA', self.amity.unallocated[-1].name)

    def test_reallocates_person(self):
        self.amity.create_room('o', 'Occulus')
        self.amity.add_person('Percila', 'Njira', 'Staff', 'N')
        self.amity.allocate_space(self.amity.people[-1])
        self.amity.create_room('o', 'Krypton')

        msg = self.amity.reallocate_person('Percila Njira', 'Krypton')

        self.assertEqual(msg, "PERCILA NJIRA assigned to KRYPTON\n")

    def test_reallocate_person_returns_error_if_person_not_found(self):
        self.amity.create_room('o', 'Krypton')
        error_msg = self.amity.reallocate_person('Shem Ogumbe', 'Krypton')

        self.assertEqual(error_msg, "Person not found!")

    def test_reallocate_person_returns_error_if_room_not_found(self):
        self.amity.create_room('o', 'Occulus')
        self.amity.add_person('Shem', 'Ogumbe', 'Staff', 'N')
        self.amity.allocate_space(self.amity.people[-1])

        error_msg = self.amity.reallocate_person('Shem Ogumbe', 'Hogwarts')

        self.assertEqual(error_msg, "Room not found!")

    def test_reallocate_person_returns_error_if_staff_allocated_livingspace(self):
        self.amity.create_room('o', 'Occulus')
        self.amity.add_person('Shem', 'Ogumbe', 'Staff', 'N')
        self.amity.allocate_space(self.amity.people[-1])
        self.amity.create_room('ls', 'Scala')

        msg = self.amity.reallocate_person('Shem Ogumbe', 'Scala')

        self.assertEqual(msg, "Error! Can't assign staff a livingspace.")
