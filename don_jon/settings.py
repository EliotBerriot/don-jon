from sqlalchemy import create_engine

test_database = create_engine('sqlite:///:memory:')

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

