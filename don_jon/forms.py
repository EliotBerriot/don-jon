#!/usr/bin/python
# -*- coding: utf-8 -*-

from models import Character
from PySide import QtGui
from utils import ugettext_lazy as _
from widgets import Icon

class CharacterForm(object):
    enabled_fields = ('global', 'abilities', 'defense')

    model = Character
    def __init__(self, session, parent=None, instance=None, **kwargs):
        self.sidebar_callback = kwargs.get('sidebar_callback', None)
        self.session = session
        self.parent = parent
        if instance is not None:
            self.instance = instance
        else:
            self.instance = self.model()

        self.fields = {}
        for section in self.enabled_fields:
            for attribute_cls in self.instance.attributes.attributes_cls.get(section, []):
                if not attribute_cls.readonly:
                    self.fields[attribute_cls.clsname()] = self.instance.attributes.get(attribute_cls.clsname()).form_field()
                
        self.total_value_fields = {}

    def validate(self):
        return True

    def process(self, save=False):
        if self.validate():
            for name, field in self.fields.items():
                self.instance.attributes.get(name).base_value = field.value

            if save:
                if self.instance.id is not None:
                    self.instance = self.session.merge(self.instance)
                else:
                    self.session.add(self.instance)
                self.session.commit()
            if self.sidebar_callback is not None:
                self.sidebar_callback()
            return self.instance
        else:
            raise ValidationError 


    def update(self,):
        self.instance = self.process()
        self.instance.attributes.sync()
        self.sync_field_values()

    def sync_field_values(self):
        for name, field in self.fields.items():
            field.value = self.instance.attributes.get(name).base_value

        for name, field in self.total_value_fields.items():
            field.setText(str(self.instance.attributes.get(name).value))
            field.setToolTip(self.modifier_tooltip(name))

    def modifier_tooltip(self, name):

        attribute = self.instance.attributes.get(name)
        lines = []
        for modifier_name, value in attribute.modifiers_descriptions:
            value 
            if type(value) == int:
                if value > 0:
                    value = "+{0}".format(value)

            lines.append("{0} : {1}".format(modifier_name, value))

        if not lines:
            text = "Aucun modificateur"
        else:
            text = "Modificateurs\n\n" + "- {0} : {1}\n".join(lines)

        return text

    def save(self):
        char = self.process(save=True)
        char.attributes.sync()

    def save_and_new(self):
        """Save current instance and display a form for a new one"""
        self.save()
        self.parent.central_widget = "character.create"

    def display(self):
        form = QtGui.QWidget()
        form_layout = QtGui.QVBoxLayout()

        for section in self.enabled_fields:
            # Create field groups 

            s = QtGui.QGroupBox(section)
            s_layout = QtGui.QGridLayout()

            row = 0

            total_enabled = False
            if section  in ("abilities", 'defense'):
                total_enabled = True
                # add abilities specific headers
                s_layout.addWidget(QtGui.QLabel(_('Valeur de base')), 0, 1)
                s_layout.addWidget(QtGui.QLabel(_('Valeur totale')), 0, 2)
                row = 1

            for attribute_cls in self.instance.attributes.attributes_cls.get(section, []):
                if not attribute_cls.readonly:
               
                    # instanciate fields
                    # get label and fields
                    name = attribute_cls.clsname()
                    attribute = self.instance.attributes.get(name)
                    field = self.fields[name]
                    widgets = field.display()
                    column = 0

                    for widget in widgets:
                        # Widget is just a string, so create a label
                        if isinstance(widget, str) or isinstance(widget, unicode):
                            widget = QtGui.QLabel(widget)

                        s_layout.addWidget(widget, row, column)                    
                        column += 1

                        # Add signal to keep field value synced with character changes
                        if hasattr(widget, 'keep_synced') and widget.keep_synced and hasattr(widget, 'value_changed'):
                            widget.value_changed.connect(self.update)

                        if total_enabled:
                            total_value_widget = QtGui.QLabel(str(self.instance.attributes.get(name).value))
                            self.total_value_fields[name] = total_value_widget
                            s_layout.addWidget(total_value_widget, row, column)
                    row += 1
            s.setLayout(s_layout)
            form_layout.addWidget(s)

        actions = QtGui.QGroupBox(_('Actions'))
        actions_layout = QtGui.QHBoxLayout()

        save_and_edit = QtGui.QPushButton(Icon('save-continue.png'), _(u"Sauvegarder et\ncontinuer l'édition"), self.parent)
        save_and_edit.clicked.connect(lambda: self.save())
        actions_layout.addWidget(save_and_edit)

        save_and_new = QtGui.QPushButton(Icon('save-new.png'), _(u"Sauvegarder et\najouter un nouveau"), self.parent)
        save_and_new.clicked.connect(lambda: self.save_and_new())
        actions_layout.addWidget(save_and_new)

        actions.setLayout(actions_layout)
        form_layout.addWidget(actions)

        self.sync_field_values()
        form.setLayout(form_layout)
        scroll_area = QtGui.QScrollArea()
        scroll_area.setWidget(form)
        return scroll_area