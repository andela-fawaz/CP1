from dbl import Base
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
    Enum,
    ForeignKey,
)


class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    role = Column(String)
    office_id = Column(Integer, ForeignKey('office.id'))
    office = relationship("Office", back_populates="people")

    __mapper_args__ = {
        "polymorphic_on": role,
        'polymorphic_identity': 'person',
        'with_polymorphic': '*',
        }

    def get_person_details(self):
        raise NotImplementedError("This is an abstract method")

    def __repr__(self):
        return self.name


class Staff(Person):
    __tablename__ = 'staff'
    id = Column(Integer, ForeignKey('person.id'), primary_key=True, autoincrement=True)
    __mapper_args__ = {"polymorphic_identity": "Staff"}


class Fellow(Person):
    __tablename__ = 'fellow'
    id = Column(Integer, ForeignKey('person.id'), primary_key=True, autoincrement=True)
    __mapper_args__ = {"polymorphic_identity": "Fellow"}

    wants_accomodation = Column(Enum('Y', 'N'))

    livingspace_id = Column(Integer, ForeignKey('livingspaces.id'))
    livingspace = relationship("LivingSpace", back_populates="people")
