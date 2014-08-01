from builtin_attributes import BaseAttribute
from utils import NameObject
from registries import races as races_registry
from utils import ugettext_lazy as _, get_modifier_function


class BaseRace(NameObject):
    modify = {}
    
@races_registry.register
class Elf(BaseRace):

    verbose_name = _('Elfe')

    modify = {
        "dexterity": get_modifier_function("+", 2),
        "constitution": get_modifier_function("-", 2),
    }

@races_registry.register
class Human(BaseRace):

    verbose_name = _('Humain')