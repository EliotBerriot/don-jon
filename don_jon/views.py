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

class CharacterList(View, QtGui.QWidget):
    fields = ('name', 'level', 'race', 'id', )
    def __init__(self, *args, **kwargs):
        super(CharacterList, self).__init__(*args, **kwargs)
        self.layout = QtGui.QVBoxLayout()

        queryset = self.get_queryset()
        self.list = QtGui.QTableWidget(queryset.count()+1, len(self.fields), self.parent)
        self.list.setHorizontalHeaderLabels([_(f) for f in self.fields])
        row = 0
        for character in queryset:
            column = 0
            for field in self.fields:
                i = QtGui.QTableWidgetItem(str(getattr(character, field)))
                self.list.setItem(row, column, i)
                column += 1
            row += 1

        self.list.setSortingEnabled(True)
        self.list.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.layout.addWidget(self.list)
        self.setLayout(self.layout) 

    def get_queryset(self):
        try:
            c = session.query(Character).count()
        except:
            Base.metadata.create_all(database) 
        queryset = session.query(Character)
        return queryset

    def process(self, **kwargs):
        return self