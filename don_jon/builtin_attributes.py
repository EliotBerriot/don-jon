#!/usr/bin/python
# -*- coding: utf-8 -*-

from utils import NameObject, D
import fields
from utils import ugettext_lazy as _
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from registries import Modifiers, races as races_registry, classes as classes_registry

class BaseAttribute(NameObject, Column):
    
    modify = {}
    default_value = None
    chosen = False
    field = None
    initial = None
    data_type = Integer
    _base_value = None
    random = False
    readonly = False
    def __init__(self, *args, **kwargs):
        self.modifiers = Modifiers()
        self.section = kwargs.pop('section', None)
        super(NameObject, self).__init__()
        super(Column, self).__init__(self.clsname(), self.data_type)
        self.manager = kwargs.get('manager')
        if kwargs.get('base_value') is not None:
            self.base_value = kwargs.get('base_value')
        else:
            self.base_value = self.get_default_value()

    def _constructor(self, name, type_, **kwargs):
        """Needed by SQLAlchemy"""
        col = BaseAttribute(name, type_, **kwargs)
        return col

    @property
    def base_value(self):
        return self._base_value

    @base_value.setter
    def base_value(self, new_value):
        self._base_value = new_value
        if self.manager is not None:
            # update model value
            setattr(self.manager.character, self.clsname(), self.value)

    def roll(self):
        """generate a random value for this attribute"""
        raise NotImplementedError

    @property
    def value(self):
        """
            Return modified base_value
        """
        v = self.base_value
        for modifier_name, modifier in self.modifiers.items():
            v = modifier(v, self.manager.character)
        return v

    def __str__(self):
        return str(self.value)
        

    def get_default_value(self):
        return self.default_value

    def get_initial_data(self, **kwargs):
        """
        Return initial data for form field
        """
        return self.initial
    
    def form_field(self, **kwargs):
        return self.field(
            initial=self.get_initial_data(), 
            default=self.get_default_value(),
            label=self.verbose_name,
            attribute=self
        )


    @property
    def modifiers_descriptions(self):
        """return a list of tuples with modifiers, and the amount modified"""
        b = self.base_value
        descriptions = []
        for modifier_name, modifier in self.modifiers.items():
            mod_value = modifier(b, self.manager.character) - b
            descriptions.append((modifier_name, mod_value))

        return descriptions

    
class StringAttribute(BaseAttribute):
    data_type = String
    field = fields.StringField

class IntAttribute(BaseAttribute):
    data_type = Integer
    field = fields.IntegerField

class SingleChoiceAttribute(BaseAttribute):
    field = fields.SingleChoiceField
    choices = [] # should be an iterable of label/value tuples


    def __init__(self, *args, **kwargs):
        self.choices = self.get_choices()
        super(SingleChoiceAttribute, self).__init__(*args, **kwargs)

    def get_choices(self):
        return self.choices

    @property
    def base_value(self):
        """returns a string"""
        return self._choice[0]

    @property
    def raw_value(self):
        """returns the the raw class"""
        return self._choice[1]

    @base_value.setter
    def base_value(self, new_value):
        try:
            c = [c for c in self.choices if c[0] == new_value or c[1] == new_value][0]
        except IndexError:
            c = None
        self._choice = c
        if self.manager is not None:
            setattr(self.manager.character, self.clsname(), self.value)


from utils import random_name
# Global

class Name(StringAttribute):

    verbose_name = _('Name')

    @property
    def default_value(self):
        name = random_name()
        return name

class Level(IntAttribute):
    default_value = 1
    verbose_name = _('Niveau')

class Speed(IntAttribute):
    default_value = 9
    verbose_name = _('Vitesse')
    readonly = True

class LifePoints(IntAttribute):
    verbose_name = _('Points de vie')
    default_value = 1
    random = True

    def roll(self):
        total = 0
        for i in range(1, self.manager.character.level+1):
            add = D(self.manager.character.attributes.get('class').raw_value.life_dice).value
            add += self.manager.character.attributes.get('constitution').mod
            if add <= 0:
                add = 1
            total += add
        return total

from registries import attributes

class Race(SingleChoiceAttribute):
    chosen = True
    verbose_name = _('Race')
    data_type = String
    default_value = "human"


    def get_choices(self):
        r = races_registry.items()
        return r

    def get_initial_data(self, **kwargs):
        
        return races_registry.values()
        

class Class(SingleChoiceAttribute):
    chosen = True
    verbose_name = _('Classe')
    data_type = String
    default_value = "warrior"

    def get_choices(self):
        r = classes_registry.items()
        return r

    def get_initial_data(self, **kwargs):
        
        return classes_registry.values()
# Abilities 

class Ability(IntAttribute):
    default_value = 10

    @property
    def mod(self):
        return (self.value / 2) - 5

    def form_field(self, **kwargs):
        """Add modificator field to form"""
        widgets = super(Ability, self).form_field(**kwargs)
        return widgets 

class Strength(Ability):
    
    verbose_name = _('Force')


class Dexterity(Ability):
    
    verbose_name = _(u'Dextérité')
    modify = {
        'armor_class': "dex_bonus",
    }
    

    def dex_bonus(self, original_value, *args, **kwargs):
        return original_value + self.mod

class Constitution(Ability):
    
    verbose_name = _('Constitution')

class Wisdom(Ability):
    
    verbose_name = _('Sagesse')

class Intelligence(Ability):
    
    verbose_name = _('intelligence')

class Charisma(Ability):
    
    verbose_name = _('Charisme')

# defense

class Armor_Class(IntAttribute):

    verbose_name = _(u"Classe d'armure")
    default_value = 10