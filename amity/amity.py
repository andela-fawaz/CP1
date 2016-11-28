import random
from models.people import Person, Staff, Fellow
from models.rooms import Room, Office, LivingSpace

class Amity(object):
    livingspaces = []
    offices = []
    fellows = []
    staff = []
    people = []
    rooms = []

    @staticmethod
    def add_person(fname, lname, role, wants_accomodation='N'):
        try:
            full_names = fname + " " + lname
            full_names = full_names.upper()

            person = Staff(full_names) if role.upper() == 'STAFF' else Fellow(full_names)

            # Fellow wants accomodation
            if isinstance(person, Fellow):
                person.wants_accomodation = wants_accomodation

            return "Person Added Succesfully!"

        except TypeError:
            return 'Invalid Input'


    def create_room(self, room_type, *room_names):
        for room_name in room_names:
            if room_type.upper() == 'LS':
                room = LivingSpace(room_name)
                self.livingspaces.append(room)
            elif room_type.upper() == 'O':
                room = Office(room_name)
                self.offices.append(room)


    def allocate_space(self, person):
        pass

    def get_unallocated_people_list(self):
        pass

    def print_allocations(self):
        pass

# Amity.add_person('Fawaz', 'Farid', 'Fellow', 'Y')
# Amity.add_person('Percilla', 'Njira', 'Staff', 'N')
# Amity.add_person('Percilla', 'Njira', 'Staff', 'Y')
amity = Amity()
amity.create_room('ls', 'Scala', 'Python', 'Ruby')
print amity.livingspaces
# print Amity.people