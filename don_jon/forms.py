#!/usr/bin/python
# -*- coding: utf-8 -*-

from models import Character
from PySide import QtGui
from utils import ugettext_lazy as _

class CharacterForm(object):
    enabled_fields = ('global', 'abilities', 'defense')

    model = Character
    def __init__(self, parent=None, instance=None, **kwargs):
        self.parent = parent
        if instance is not None:
            self.instance = instance
        else:
            self.instance = self.model()

        self.fields = {}
        for section in self.enabled_fields:
            for attribute_cls in self.instance.attributes.attributes_cls.get(section, []):
                self.fields[attribute_cls.clsname()] = self.instance.attributes.get(attribute_cls.clsname()).form_field()


    def validate(self):
        return True

    def process(self):
        if self.validate():
            for name, field in self.fields.items():
                self.instance.attributes.get(name).base_value = field.value

            return self.instance
        else:
            raise ValidationError 


    def save(self):
        char = self.process()
        char.attributes.sync()

        char.display()

    def display(self):
        form_layout = QtGui.QVBoxLayout()
        form_layout.addStretch(1)

        for section in self.enabled_fields:
            s = QtGui.QGroupBox(section)
            s_layout = QtGui.QFormLayout()
            for attribute_cls in self.instance.attributes.attributes_cls.get(section, []):
                s_layout.addRow(*self.fields[attribute_cls.clsname()].display())

            s.setLayout(s_layout)
            form_layout.addWidget(s)

        save = QtGui.QPushButton(_("Sauvegarder"), self.parent)
        form_layout.addWidget(save)
        save.clicked.connect(lambda: self.save())

        return form_layout