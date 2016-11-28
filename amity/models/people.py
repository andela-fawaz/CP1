class Person(object):

    def __init__(self, name):
        self.name = name

    def get_person_details(self):
        raise NotImplementedError("This is an abstract method")

    def allocate_office(self):
        pass


class Staff(Person):
    pass

class Fellow(Person):
    wants_livingspace = 'N'
