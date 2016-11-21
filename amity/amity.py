class Amity(object):
    people = []
    rooms = []

    @staticmethod
    def add_person(fname, lname, type, allocation):
        if not isinstance(fname, str) or not isinstance(lname, str):
            return "Invalid Name!"
        else:
            full_names = fname + " " + lname
            full_names = full_names.upper()

            Amity.people.append({
                full_names : {
                    'type' : 'Fellow',
                    'room_allocated' : 'Scala',
                },
            })
            return "Person Added Succesfully!"

    @staticmethod
    def create_room(self, *args):
        pass

    def print_allocations(self):
        pass
