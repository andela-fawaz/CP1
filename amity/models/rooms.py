class Room(object):

    capacity = 0

    def __init__(self, name):
        self.name = name
        self.people = []

    def __repr__(self):
        return self.name

    def get_occupants(self):
        return self.people

    def add_person(self, person):
        """
        Add person to a room
        @params Instance of person
        """
        # Check if room is filled.
        if len(self.people) < self.capacity:
            self.people.append(person)
            if isinstance(self, LivingSpace):
                # person.allocate_livingspace
                pass
            else:
                # person.allocate_office
                pass




class Office(Room):
    capacity = 6


class LivingSpace(Room):
    capacity = 4
