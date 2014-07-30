#!/usr/bin/python
# -*- coding: utf-8 -*-
from settings import database_session as session, database, Base
from models import Character
from utils import ugettext_lazy as _
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
        super(CharacterCreate, self).__init__(*args, **kwargs)
        self.layout = QtGui.QVBoxLayout() 
        self.layout.addLayout(CharacterForm(session=session, parent=self.parent).display())
        self.setLayout(self.layout) 

    def process(self, **kwargs):
        return self

class TableItem(QtGui.QTableWidgetItem):
    def __init__(self, content, instance, parent):
        super(TableItem, self).__init__(content)
        self.parent = parent
        self.instance = instance

class CharacterDetail(QtGui.QWidget):
    
    def __init__(self, instance=None, parent=None):
        super(CharacterDetail, self).__init__()
        self.layout = QtGui.QVBoxLayout()
        self.instance = instance
        self.parent = parent
        self.layout.addWidget(QtGui.QLabel(self.instance.name))
        self.setLayout(self.layout)

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
        self.list.cellClicked.connect(self.update_sidebar)
        self.layout.addWidget(self.list)

        self.setLayout(self.layout) 

    def update_sidebar(self, row, column):
        instance = self.list.itemAt(row, column).instance
        if self.current_sidebar is not None:
            self.layout.removeWidget(self.current_sidebar)
            self.current_sidebar.setParent(None)

        self.current_sidebar = CharacterDetail(instance=instance, parent=self)
        self.layout.addWidget(self.current_sidebar)

    def get_queryset(self):
        try:
            c = session.query(Character).count()
        except:
            Base.metadata.create_all(database) 
        queryset = session.query(Character)
        return queryset

    def process(self, **kwargs):
        return self