#!/usr/bin/python
# -*- coding: utf-8 -*-
from settings import database_session as session, database, Base, env
from models import Character
from utils import ugettext_lazy as _, reverse
from collections import OrderedDict
import os

class View(object):
    def __init__(self, parent=None, **kwargs):
        super(View, self).__init__()
        self.parent = parent
        self.kwargs = kwargs

    def __call__(self, **kwargs):
        return self.process(**kwargs)

    def process(self, **kwargs):
        return None

class TestOne(View):

    def process(self, **kwargs):
        return self.kwargs

from PySide import QtGui
from forms import CharacterForm

class CharacterCreate(View, QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        instance = kwargs.pop('instance', None)
        super(CharacterCreate, self).__init__(*args, **kwargs)
        self.layout = QtGui.QVBoxLayout() 
        self.layout.addLayout(CharacterForm(session=session, parent=self.parent, instance=instance).display())
        self.setLayout(self.layout) 

    def process(self, **kwargs):
        return self

class TableItem(QtGui.QTableWidgetItem):
    def __init__(self, content, instance, parent):
        super(TableItem, self).__init__(content)
        self.parent = parent
        self.instance = instance

class ImproperlyConfigured(Exception):
    pass

class NoSuchTemplate(Exception):
    pass

class TemplateView(QtGui.QTextBrowser):
    """API inspired from django"""
    template_name = ""
    def __init__(self, *args, **kwargs):
        self.parent = kwargs.get("parent", None)
        super(TemplateView, self).__init__(self.parent)
        if not self.template_name:
            raise ImproperlyConfigured("Please define a template_name attribute")
        self.setHtml(self.render_template())

    def render_template(self):
        try:
            template = env.get_template(self.template_name)
        except:
            raise NoSuchTemplate("Cannot find template '{0} in templates directory".format(self.template_name))
        return template.render(self.get_context_data())

    def get_context_data(self, **kwargs):
        return {"getattr": getattr,}

class CharacterDetail(TemplateView):

    template_name = "character.detail.html"
    def __init__(self, instance=None, **kwargs):
        self.instance = instance
        super(CharacterDetail, self).__init__(**kwargs)

    def get_context_data(self, **kwargs):
        context = super(CharacterDetail, self).get_context_data(**kwargs)
        context["instance"] = self.instance

        return context


class CharacterList(View, QtGui.QWidget):
    fields = ('name', 'level', 'race', 'id', )
    def __init__(self, *args, **kwargs):
        super(CharacterList, self).__init__(*args, **kwargs)
        self.layout = QtGui.QHBoxLayout()
        self.current_sidebar = None
        self.queryset = self.get_queryset()
        self.list = QtGui.QTableWidget(self.queryset.count()+1, len(self.fields), self.parent)
        self.list.setHorizontalHeaderLabels([_(f) for f in self.fields])
        row = 0
        for character in self.queryset:
            column = 0
            for field in self.fields:
                i = TableItem(str(getattr(character, field)), instance=character, parent=self)
                self.list.setItem(row, column, i)
                column += 1
            row += 1

        self.list.setSortingEnabled(True)
        self.list.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.list.itemClicked.connect(self.update_sidebar)
        self.list.itemDoubleClicked.connect(self.edit_character)
        self.layout.addWidget(self.list)

        self.setLayout(self.layout) 

    def update_sidebar(self, item):
        widget = item
        instance = widget.instance
        if self.current_sidebar is not None:
            self.layout.removeWidget(self.current_sidebar)
            self.current_sidebar.setParent(None)

        self.current_sidebar = CharacterDetail(instance=instance, parent=self)
        self.layout.addWidget(self.current_sidebar)

    def edit_character(self, item):
        try:
            instance = item.instance
        except:
            intance = None
        if instance is not None:
            print(instance.name)
            self.parent.central_widget = reverse('character.create', instance=instance, parent=self.parent)

    def get_queryset(self):
        try:
            c = session.query(Character).count()
        except:
            Base.metadata.create_all(database) 
        queryset = session.query(Character)
        return queryset

    def process(self, **kwargs):
        return self