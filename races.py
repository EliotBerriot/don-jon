from builtin_attributes import BaseAttribute
from utils import NameObject


class Race(BaseAttribute):
    pass


class BaseRace(NameObject):
    pass

    
class Elf(BaseRace):

    modify = {
        "dexterity": lambda original_value: original_value + 2,
        "constitution": lambda original_value: original_value - 2,
    }