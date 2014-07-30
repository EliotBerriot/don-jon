from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

test_database = create_engine('sqlite:///:memory:')

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

database = create_engine('sqlite:///:memory:')
database_session = sessionmaker(bind=database)()
