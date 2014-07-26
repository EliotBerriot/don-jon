from utils import NameObject
import widgets
from utils import ugettext_lazy as _

class BaseAttribute(NameObject):
    
    modify = {}
    default = None
    chosen = False
    field = None
    def __init__(self, character=None, value=None, **kwargs):
        self.modifiers = {}
        self.character = character
        if value is not None:
            self._value = value
        else:
            self._value = self.default


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
        raise NotImplementedError

    def form_row(self, **kwargs):
        return self.verbose_name + " : ", self.form_field()

    def form_field(self, **kwargs):
        return self.field(initial=self.get_initial_data())

class IntAttribute(BaseAttribute):
    pass

class SingleChoiceAttribute(BaseAttribute):
    field = widgets.SingleChoice

    
# Global

class Level(IntAttribute):
    default = 1


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