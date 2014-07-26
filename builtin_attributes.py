
class BaseAttribute(object):
    
    modify = {}
    default = None

    def __init__(self, character=None, value=None, **kwargs):
        self.modifiers = {}
        self.character = character
        if value is not None:
            self._value = value
        else:
            self._value = self.default

    @classmethod
    def clsname(cls):
        return cls.__name__.lower()

    @property
    def name(self):
        return self.__class__.clsname(self.__class__)

    @property
    def value(self):
        v = self._value
        for modifier_name, modifier in self.modifiers.items():
            v = modifier(v)
        return v

    @value.setter
    def value(self, value):
        self._value = value

# Global

class Level(BaseAttribute):
    default = 1

# Abilities 

class Ability(BaseAttribute):
    default = 10

    @property
    def mod(self):
        return (self.value / 2) - 5

class Strength(Ability):
    pass

class Dexterity(Ability):
    
    modify = {
        'armor_class': "dex_bonus",
    }
    

    def dex_bonus(self, original_value, **kwargs):
        return original_value + self.mod

class Constitution(Ability):
    pass

class Wisdom(Ability):
    pass

class Intelligence(Ability):
    pass

class Charisma(Ability):
    pass

# defense

class Armor_Class(BaseAttribute):
    default = 10