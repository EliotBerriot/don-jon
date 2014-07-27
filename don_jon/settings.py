from sqlalchemy import create_engine

database = create_engine('sqlite:///:memory:', echo=True)

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

