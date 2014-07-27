from utils import AttrDict, AttrOrderedDict
from builtin_attributes import *
from races import *
from registries import attributes, races
import sys

attributes.autodiscover(apps=('don_jon',))
races.autodiscover(apps=('don_jon',))

class Empty:
    pass

default_attributes = AttrOrderedDict()

default_attributes['global'] = (
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
    attributes = {}
    def __init__(self, character, **kwargs):
        self.character = character

        self.setup_attributes()
        self.setup_modifiers()

    def setup_attributes(self):
        for section, attributes in self.attributes_cls.items():
            for attribute in attributes:
                if hasattr(self, attribute.clsname()):
                    # an attribute with the same name alredy exists !
                    raise ValueError('Attribute {0} already set'.format(attribute.clsname()))
                attr = attribute(base_value=getattr(self.character, attribute.clsname()), manager=self)
                self.attributes[attribute.clsname()] = attr
                setattr(self, attribute.clsname(), attr)

    def setup_modifiers(self):
        for name, attribute in self.attributes.items():
            if attribute.chosen:
                # race, gifts, etc.
                try:
                    modifiers = attribute.base_value.modify.items()
                except AttributeError:
                    # no value has been set
                    pass
            else:
                # commons attributes (strength, armor, etc.)
                modifiers = attribute.modify.items()
            print("loop", name, modifiers)
            for modified_attribute, modifier_function in modifiers:
                if hasattr(modifier_function, '__call__'):
                    # a lambda or a callback was passed to modify
                    f = modifier_function
                else:
                    # a string was passed, try to look for a method with the same name on the attribute
                    f = getattr(attribute, modifier_function)
                getattr(self, modified_attribute).modifiers[modifier_function] = f

        print("modifiers", self.strength.modifiers)
class DefaultAttributesManager(dict):

    _attributes_list = default_attributes

    def __init__(self, character, **kwargs):
        super(DefaultAttributesManager, self).__init__()
        self.character = character
        self.kwargs = kwargs
        self.setup_attributes()
        self.setup_modifiers()

    def __call__(self, attribute,):

        return self[attribute]

    def setup_attributes(self):
        for section, attributes in self._attributes_list.items():
            for attribute in attributes:
                if self.get(attribute.clsname(), Empty) != Empty:
                    # an attribute with the same name alredy exists !
                    raise ValueError('You declared the same attribute twice')

                self[attribute.clsname()] = attribute(value=self.kwargs.get(attribute.clsname(), None))
        
    def setup_modifiers(self):
        for name, attribute in self.items():
            if attribute.chosen:
                # race, gifts, etc.
                try:
                    modifiers = attribute.value.modify.items()
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
                self(modified_attribute).modifiers[modifier_function] = f
