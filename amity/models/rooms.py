from dbl import Base
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
)


class Room(object):
    capacity = 0
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def get_occupants(self):
        """
        Get all Occupants of a Room
        :returns - A list of Objects(People)
        """
        return self.people

    def add_person(self, person):
        """
        Add person to a room
        :params Instance of person
        """
        # Check if room is filled.
        if len(self.people) < self.capacity:
            self.people.append(person)

    def is_filled(self):
        """
        Checks if a room is filled.
        :returns - Bool(True/False)
        """
        people = self.get_occupants()
        if len(people) == self.capacity:
            return True
        return False


class Office(Room, Base):
    __tablename__ = "office"
    capacity = 6

    people = relationship('Person', back_populates='office')


class LivingSpace(Room, Base):
    capacity = 4
    __tablename__ = "livingspaces"
    people = relationship('Fellow', back_populates='livingspace')
