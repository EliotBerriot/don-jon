from attributes import AttributesManager, default_attributes
from utils import NameObject
from settings import Base
from meta import classmaker

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import synonym
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.declarative.api import DeclarativeMeta
from sqlalchemy.ext.hybrid import hybrid_property


def attribute_getter(name):
    def getter(self):
        return self.attributes(name).value
    return getter

def attribute_setter(name):
    def setter(self, new_value):
        setattr(self, '_'+name, new_value)
        self.attributes(name).value = new_value
    return setter

class CharacterMeta(DeclarativeMeta):
    """
        Add columns to character class
    """
    def __new__(metacls, name, bases, dct): 
        cls = super(CharacterMeta, metacls).__new__(metacls, name, bases, dct)
        for section, columns in default_attributes.items():
            for column in columns:
                name = column.clsname()
                setattr(cls, name, column())
                #s = hybrid_property(attribute_getter(name), attribute_setter(name))
                #setattr(cls, name, s)
        return cls


class Character(NameObject, Base):

    __metaclass__ = CharacterMeta
    __tablename__ = 'character'
    id = Column(Integer, primary_key=True)

    

    def __init__(self, *args, **kwargs):        
        NameObject.__init__(self)
        Base.__init__(self, *args, **kwargs)
        self.attributes = AttributesManager(character=self, **kwargs)

    def display(self):

        for section, attributes in self.attributes.attributes_cls.items():
            print('{0}\n{1}\n'.format(section, "*" * len(section)))

            for a in attributes:
                attribute = self.attributes.get(a.clsname())
                key = attribute.clsname()
                if isinstance(attribute.value, type):
                    value = attribute.value.clsname()
                else:
                    value = attribute.value
                print('{0}: {1}'.format(key, value))

            print('\n')

class CharacterGenerator(object):

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def create(self, **kwargs):
        kw = self.kwargs.copy()
        kw.update(kwargs)
        return Character(**kw)
