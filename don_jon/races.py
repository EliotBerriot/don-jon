from builtin_attributes import BaseAttribute
from utils import NameObject
from registries import races as races_registry
from utils import ugettext_lazy as _


class BaseRace(NameObject):
    modify = {}

@races_registry.register
class Elf(BaseRace):

    verbose_name = _('Elfe')
    modify = {
        "dexterity": lambda original_value: original_value + 2,
        "constitution": lambda original_value: original_value - 2,
    }

@races_registry.register
class Human(BaseRace):

    verbose_name = _('Humain')