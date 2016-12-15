from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import create_engine

Base = declarative_base()


class DbAbsLayer(object):
    # Database Abstraction Layer
    def __init__(self):
        self.engine = create_engine('sqlite:///amity.db')
        # create any tables that don't yet exist
        Base.metadata.create_all(self.engine)

    def create_session(self):
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        return self.session

    def clear_db(self):
        # drop all tables
        Base.metadata.drop_all(self.engine)
        # create tables to maintain schema
        Base.metadata.create_all(self.engine)
