#!/usr/bin/python
# -*- coding: utf-8 -*-

from models import Character
from PySide import QtGui
from utils import ugettext_lazy as _


class CharacterForm(object):
    enabled_fields = ('race', 'level', 'strength', 'dexterity', 'constitution')

    model = Character
    def __init__(self, parent, instance=None, **kwargs):
        self.parent = parent
        if instance is not None:
            self.instance = instance
        else:
            self.instance = self.model()

        self.fields = {}
        for field in self.enabled_fields:
            self.fields[field] = self.instance.attributes.get(field).form_field()


    def validate(self):
        return True

    def process(self):
        if self.validate():
            for field in self.enabled_fields:
                self.instance.attributes.get(field).base_value = self.fields[field].value

            return self.instance
        else:
            raise ValidationError 


    def save(self):
        char = self.process()
        char.attributes.sync()

        char.display()

    def display(self):
        form_layout = QtGui.QFormLayout()
           
        for field in self.enabled_fields:
            form_layout.addRow(*self.fields[field].display())

        save = QtGui.QPushButton(_("Sauvegarder"), self.parent)
        form_layout.addRow(save)
        save.clicked.connect(lambda: self.save())

        return form_layout