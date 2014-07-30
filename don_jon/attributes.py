from utils import AttrDict, AttrOrderedDict
from builtin_attributes import *
from races import *
from registries import attributes, races, ManagedAttributes
import sys

attributes.autodiscover(apps=('don_jon',))
races.autodiscover(apps=('don_jon',))
class Empty:
    pass

default_attributes = AttrOrderedDict()

default_attributes['global'] = (
    Name,
    Level,  
    Race,
)

default_attributes['defense'] = (
    Armor_Class,    
)

default_attributes['abilities'] = (
    Strength,
    Dexterity,
    Constitution,
    Wisdom,
    Intelligence,
    Charisma,    
    
)

class AttributesManager(object):

    attributes_cls = default_attributes  

    def __init__(self, character, **kwargs):
        self._attributes = ManagedAttributes()
        self.character = character
        self.setup_attributes()
        self.sync()

    def setup_attributes(self):
        for section, attributes in self.attributes_cls.items():
            for attribute in attributes:
                if hasattr(self, attribute.clsname()):
                    # an attribute with the same name alredy exists !
                    raise ValueError('Attribute {0} already set'.format(attribute.clsname()))
                attr = attribute(base_value=getattr(self.character, attribute.clsname()), manager=self, section=section)
                self._attributes.register(data=attr, name=attribute.clsname())
                setattr(self, attribute.clsname(), attr)

    def reset_mofifiers(self):
        for name, attribute in self._attributes.items():
            self.get(name).modifiers.clear()

    def setup_modifiers(self):
        self.reset_mofifiers()
        
        for name, attribute in self._attributes.items():
            if attribute.chosen:
                # race, gifts, etc.
                try:
                    modifiers = attribute.raw_value.modify.items()
                except AttributeError:
                    # no value has been set
                    pass
            else:
                # commons attributes (strength, armor, etc.)
                modifiers = attribute.modify.items()

            for modified_attribute, modifier_function in modifiers:
                if hasattr(modifier_function, '__call__'):
                    # a lambda or a callback was passed to modify
                    f = modifier_function
                else:
                    # a string was passed, try to look for a method with the same name on the attribute
                    f = getattr(attribute, modifier_function)

                self.get(modified_attribute).modifiers.register(data=f, name=attribute.clsname())

    def sync(self):
        self.setup_modifiers()
        for name, attribute in self._attributes.items():
            char_attr = getattr(self.character, name, None)
            if char_attr is not None:
                setattr(self.character, name, attribute.value)

    def get(self, attribute, not_found=None):
        return self._attributes.get(attribute, not_found)
