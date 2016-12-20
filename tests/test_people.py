import unittest
from amity.models.people import Person, Fellow, Staff


class PeopleTest(unittest.TestCase):
    def setUp(self):
        self.staff = Staff()
        self.fellow = Fellow()

    def test_fellow_is_instance_of_person(self):
        self.assertTrue(Person, type(self.fellow))

    def test_staff_is_instance_of_person(self):
        self.assertTrue(Person, type(self.staff))
