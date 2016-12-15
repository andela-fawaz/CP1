"""
amity

Usage:
    amity create_room (Living|Office) <room_name>...
    amity add_person <first_name> <last_name> (Fellow|Staff) [<wants_accomodation>]
    amity reallocate_person <employee_id> <new_room_name>
    amity load_people
    amity print_allocations [--o=filename.txt]
    amity print_unallocated [--o=filename.txt]
    amity print_room <room_name>
    amity save_state [--db=sqlite_database]
    amity load_state <sqlite_database>
    amity (-i | --interactive)

Options:
    -h --help                         Show this screen.
    -v --version                      Show version.

Examples:
    amity hello

Help:
    For help using this tool, please open an issue on the Github repository:
    https://github.com/fawazfarid/amityville
"""

"""
Usage:

Options:
    -h --help     Show this screen.
    -i --interactive  Interactive Mode
    -v --version
"""
import cmd
import sys
from docopt import docopt, DocoptExit
from amity.amity import Amity


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as exit:
            # Thrown when args do not match

            print("You have entered an invalid command!")
            print(exit)
            return

        except SystemExit:
            # Prints the usage for --help

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


class Interactive (cmd.Cmd):
    prompt = "(amity) "

    # file = None
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.amity = Amity()

    @docopt_cmd
    def do_create_room(self, args):
        """Usage: create_room (living|office) <room_name>..."""
        room_type = "LS" if args['living'] else "O"
        room_names = args['<room_name>']

        self.amity.create_room(room_type, *room_names)

    @docopt_cmd
    def do_add_person(self, args):
        """Usage: \
        add_person <first_name> <last_name> (fellow|staff)\
             [<wants_accomodation>]"""
        first_name = args['<first_name>']
        last_name = args['<last_name>']
        role = "Fellow" if args['fellow'] else "Staff"
        wants_accomodation = args['<wants_accomodation>']

        msg = self.amity.add_person(first_name, last_name, role, wants_accomodation)
        print(msg)

        # Allocate Space to the latest entry
        msg = self.amity.allocate_space(self.amity.people[-1])
        print msg

    @docopt_cmd
    def do_reallocate_person(self, args):
        """Usage: reallocate_person <first_name> <last_name> <new_room_name>"""
        person = args['<first_name>'] + " " + args['<last_name>']
        room = args['<new_room_name>']
        print(self.amity.reallocate_person(person, room))

    @docopt_cmd
    def do_load_people(self, arg):
        """Usage: load_people"""
        msg = self.amity.load_people('data/people.txt')
        print msg

    @docopt_cmd
    def do_print_allocations(self, args):
        """Usage: print_allocations [--o=filename.txt]"""
        rooms = self.amity.get_allocations()
        if args['--o']:
            # Write to File
            with open(args['--o'], 'w') as f:
                for room, occupants in rooms.iteritems():
                    f.write(room + '\n')
                    f.write(('-'*30) + '\n')
                    for occupant in occupants:  # ", ".join(occupants) better way
                        f.write(occupant + ', ')
                    f.write('\n\n')
        # print
        for room, occupants in rooms.iteritems():
                    print(room)
                    print('-'*30)
                    for occupant in occupants:  # ", ".join(occupants) better way
                        print(occupant + ', ')
                    print('\n')

    @docopt_cmd
    def do_print_unallocated(self, args):
        """Usage: print_unallocated [--o=filename.txt]"""
        unallocated_people = self.amity.get_unallocated_people()
        if len(unallocated_people) == 0:
            print "No unallocated people."
        else:
            print(", ".join(unallocated_people))

    @docopt_cmd
    def do_print_room(self, args):
        """Usage: print_room <room_name>"""
        people = self.amity.get_room_occupants(args['<room_name>'])
        print(people)

    @docopt_cmd
    def do_save_state(self, args):
        """Usage: save_state [--db=sqlite_database]"""
        print(self.amity.save_state())

    @docopt_cmd
    def do_load_state(self, args):
        """Usage: load_state <sqlite_database>"""
        print(self.amity.load_state(args))

    def do_quit(self, arg):
        """Quits out of the interactive mode"""
        print "Goodbye!"
        exit()


opt = docopt(__doc__, sys.argv[1:])

if opt["--interactive"]:
    Interactive().cmdloop()

print(opt)

# if __name__ == '__main__':
#     main()
