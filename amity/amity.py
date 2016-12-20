import random
from models.people import Staff, Fellow
from models.rooms import Office, LivingSpace
from models.dbl import DbAbsLayer

db = DbAbsLayer()
session = db.create_session()


class Amity(object):
    livingspaces = []
    offices = []
    people = []
    unallocated = []

    def add_person(self, fname, lname, role, wants_accomodation='N'):
        """Adds a person in the System.

        :param fname,lname - A string, person's first and last names.
        :param role - A String, person's role(Staff or Fellow).
        :param wants_accomodation - A string,
            does the person(if Fellow) wants accomodation?(Y/N)

        returns: success msg or error(If invalid input parameters).

        """
        try:
            role = role.upper()
            wants_accomodation = wants_accomodation.upper()

            # validation
            if role not in ('STAFF', 'FELLOW'):
                return "Invalid Role! person should be FELLOW or STAFF."

            if wants_accomodation not in ('Y', 'N'):
                return "Invalid Input! input should be Y or N."

            full_names = fname + " " + lname
            full_names = full_names.upper()

            person = Staff(name=full_names) if role == 'STAFF' else Fellow(
                name=full_names, wants_accomodation=wants_accomodation.upper())

            self.people.append(person)
            return person.name + " Added Succesfully! \n"

        except (AttributeError, TypeError):
            return 'Invalid Input!'

    def create_room(self, room_type, *room_names):
        # get all rooms
        available_rooms = [x.name for x in (self.livingspaces + self.offices)]
        try:
            # Validation
            if room_type.upper() not in('LS', 'O'):
                return "Invalid Room Type!"

            for room_name in room_names:
                room_name = room_name.upper()
                if room_name in available_rooms:
                    return "Room already exists!"

                if room_type.upper() == 'LS':
                    room = LivingSpace(name=room_name)
                    self.livingspaces.append(room)
                elif room_type.upper() == 'O':
                    room = Office(name=room_name)
                    self.offices.append(room)

            return "Room(s) Created Successfully!"

        except AttributeError:
            return "Invalid Input!"

    def allocate_space(self, person):
        """
        Allocates office to a Person(Fellow or Office)
        If person is a Fellow and wants accomodation, allocate living space.

        :param person - Instance of Person

        returns: msg - success or error message.
        """

        msg = self.add_person_to_room(person, self.offices)

        if isinstance(person, Fellow) and person.wants_accomodation == 'Y':
            msg += self.add_person_to_room(person, self.livingspaces)

        return msg

    def add_person_to_room(self, person, rooms):
        """
        Checks for available rooms then adds person to a random room.

        :param person - Instance of person

        returns: msg - success or error message.
        """
        available_rooms = rooms

        # check available offices
        for room in rooms:
            if room.is_filled():
                available_rooms.remove(room)

        if len(available_rooms) == 0:  # check if there are available rooms
            msg = "There are no available rooms \n"
            if rooms is self.offices:  # If someone misses out on an office
                self.unallocated.append(person)

        else:
            # assign random room
            random_room = random.choice(available_rooms)

            # add person to room
            random_room.people.append(person)
            # session.add(person)
            msg = person.name + " assigned to " + random_room.name + "\n"

        return msg

    def reallocate_person(self, person, room):
        """"""
        try:
            # get person
            person = filter(lambda x: x.name == person.upper(), self.people)[0]
        except IndexError:
            return "Person not found!"

        rooms = self.livingspaces + self.offices
        try:
            room = filter(lambda x: x.name == room.upper(), rooms)[0]
        except IndexError:
            return "Room not found!"

        if person in self.unallocated and isinstance(room, Office):
            self.unallocated.remove(person)

        # Remove person from original allocated room
        if isinstance(room, LivingSpace):
            for allocated_room in self.livingspaces:
                if person in allocated_room.people:
                    allocated_room.people.remove(person)
        else:
            for allocated_room in self.offices:
                if person in allocated_room.people:
                    allocated_room.people.remove(person)
        # Allocate new room
        room.add_person(person)
        return person.name + " assigned to " + room.name + "\n"

    def get_unallocated_people(self):
        # get Names of unallocated
        unallocated_list = [person.name for person in self.unallocated]
        return unallocated_list

    def get_allocations(self, file=None):
        self.rooms = self.livingspaces + self.offices
        results = {}

        for room in self.rooms:
            results[room.name] = [occupants.name for occupants in room.people]

        return results

    def load_people(self, file):
        # Check if file is .txt

        # Open file for reading.
        with open(file, 'r') as f:
            data = f.read()   # read contents of files

        people = data.splitlines()   # returns people list
        msg = ""
        for person in people:
            person_details = person.split()

            msg += self.add_person(*person_details)
            msg += self.allocate_space(self.people[-1])

        return msg

    def get_room_occupants(self, room_name):
        self.rooms = self.livingspaces + self.offices
        room_name = room_name.upper()
        try:
            room = filter(lambda x: x.name == room_name, self.rooms)[0]
            return room.get_occupants()
        except IndexError:
            return "Room not found!"

    def save_state(self):
        session.bulk_save_objects(self.people)
        session.bulk_save_objects(self.livingspaces)
        session.bulk_save_objects(self.offices)
        session.commit()
