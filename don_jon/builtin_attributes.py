from utils import NameObject
import fields
from utils import ugettext_lazy as _
from sqlalchemy import Column, Integer, String

class BaseAttribute(NameObject, Column):
    
    modify = {}
    default_value = None
    chosen = False
    field = None
    initial = None
    data_type = Integer
    def __init__(self, character=None, value=None, **kwargs):
        super(NameObject, self).__init__()
        super(Column, self).__init__(self.clsname(), self.data_type)
        self.modifiers = {}
        self.character = character
        if value is not None:
            self._value = value
        else:
            self._value = self.default_value

    @property
    def value(self):
        v = self._value
        for modifier_name, modifier in self.modifiers.items():
            v = modifier(v)
        return v

    @value.setter
    def value(self, value):
        self._value = value

    def __str__(self):
        return str(self.value)
        
    def __repr__(self):
        if self.chosen:
            return self.value.__repr__()
        return str(self.value)

    
    def get_initial_data(self, **kwargs):
        """
        Return initial data for form field
        """
        return self.initial
    
    def form_field(self, **kwargs):
        return self.field(initial=self.get_initial_data(), label=self.verbose_name)

class IntAttribute(BaseAttribute):
    data_type = Integer
    field = fields.IntegerField

class SingleChoiceAttribute(BaseAttribute):
    field = fields.SingleChoiceField

    
# Global

class Level(IntAttribute):
    default_value = 1
    verbose_name = _('Niveau')

from registries import attributes

@attributes.register
class Race(SingleChoiceAttribute):
    chosen = True
    default = None
    verbose_name = _('Race')

    def get_initial_data(self, **kwargs):
        from registries import races as races_registry
        return races_registry.values()
        
# Abilities 

class Ability(IntAttribute):
    default_value = 10

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
    default_value = 10