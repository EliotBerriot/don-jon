from utils import AttrDict, AttrOrderedDict
from builtin_attributes import *
from races import *
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
             for modified_attribute, modifier_function in attribute.modify.items():
                if hasattr(modifier_function, '__call__'):
                    # a lambda or a callback was passed to modify
                    f = modifier_function
                else:
                    # a string was passed, try to look for a method with the same name on the attribute
                    f = getattr(attribute, modifier_function)
                print(self('race').value)
                self(modified_attribute).modifiers[modifier_function] = f
